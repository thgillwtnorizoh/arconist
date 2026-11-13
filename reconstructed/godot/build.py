#!/usr/bin/env python3
"""R010: logged technical checks and Windows packaging; never GUI playtesting."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import struct
import subprocess
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / 'reconstructed/godot'
OUT = ROOT / 'reconstructed/out'
DATA = 'data_Arconist.Godot_windows_x86_64'


def sha(path):
    with path.open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()


def run(name, args, cwd=ROOT):
    print(name, flush=True)
    result = subprocess.run([str(a) for a in args], cwd=cwd, env=ENV,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    ledger=LOGS/'commands.json'
    commands=json.loads(ledger.read_text()) if ledger.exists() else []
    commands.append(dict(name=name,args=[str(a) for a in args],cwd=str(cwd),exit_code=result.returncode))
    ledger.write_text(json.dumps(commands,indent=2))
    text = result.stdout.decode('utf-8', errors='replace')
    (LOGS / (name + '.log')).write_text(
        json.dumps([str(a) for a in args]) + '\n' + text +
        '\nEXIT_CODE=' + str(result.returncode) + '\n', encoding='utf-8')
    # Godot can return zero even after its .NET exporter fails.
    if result.returncode or re.search(r'(?m)^\s*(?:ERROR:|SCRIPT ERROR:)', text):
        raise RuntimeError(f'{name} failed; see {LOGS}')
    return text


def pe_x64(path):
    with path.open('rb') as f:
        assert f.read(2) == b'MZ', path
        f.seek(0x3c)
        offset = struct.unpack('<I', f.read(4))[0]
        f.seek(offset)
        assert f.read(6) == b'PE\0\0\x64\x86', path


def verify(package, templates):
    required = ['Arconist.exe', 'Arconist.pck'] + [DATA + '/' + f for f in (
        'Arconist.Godot.dll', 'Arconist.Core.dll', 'Arconist.Bridge.dll',
        'GodotSharp.dll',
        'Arconist.Godot.deps.json', 'Arconist.Godot.runtimeconfig.json',
        'coreclr.dll', 'hostfxr.dll', 'hostpolicy.dll', 'clrjit.dll',
        'System.Private.CoreLib.dll', 'System.Runtime.dll')]
    for item in required:
        assert (package / item).is_file() and (package / item).stat().st_size, item
    assert sha(package / 'Arconist.exe') == sha(templates / 'windows_release_x86_64.exe')
    for item in ['Arconist.exe'] + [DATA + '/' + f for f in (
            'coreclr.dll', 'hostfxr.dll', 'hostpolicy.dll', 'clrjit.dll')]:
        pe_x64(package / item)
    config = json.loads((package / DATA / 'Arconist.Godot.runtimeconfig.json').read_text())
    runtime = config['runtimeOptions']
    assert runtime['tfm'] == 'net10.0' and 'framework' not in runtime
    assert any(f['name'] == 'Microsoft.NETCore.App' and f['version'] == '10.0.13'
               for f in runtime['includedFrameworks'])
    deps = json.loads((package / DATA / 'Arconist.Godot.deps.json').read_text())
    assert deps['runtimeTarget']['name'].endswith('/win-x64')
    # Validate the actual exported runtime/native dependency closure. GodotPlugins
    # belongs to the editor and is intentionally absent from an exported game.
    assets = []
    for library in deps['targets'][deps['runtimeTarget']['name']].values():
        for kind in ('runtime', 'native', 'resources'):
            for name, metadata in library.get(kind, {}).items():
                # deps.json retains NuGet asset paths (e.g. lib/net8.0/...);
                # dotnet publish flattens runtime/native files into the output.
                relative = Path(metadata.get('locale', '')) / Path(name).name if kind == 'resources' else Path(name).name
                path = package / DATA / relative
                assert path.is_file() and path.stat().st_size, name
                assets.append(str(relative))
    pck = (package / 'Arconist.pck').read_bytes()
    assert pck[:4] == b'GDPC'
    for chart in ('practice.aff', 'ordinary_two_tap.aff', 'mixed_practice.aff', 'native_hold.aff', 'hold_first.aff', 'tap_first.aff', 'audible_practice.aff', 'audible_aff120.aff', 'sky_practice.aff', 'native_moving_arc.aff', 'arctap_practice.aff', 'native_arc_tap.aff', 'linked_practice.aff', 'native_linked_arc_successors.aff','native_timing_group.aff','native_reverse_scroll.aff','native_noinput_group.aff','grouped_practice.aff'):
        assert (PROJECT / 'content' / chart).read_bytes() in pck, chart
    music = PROJECT / 'content/audio/clockwork_steps.wav.bytes'
    music_manifest = json.loads((ROOT / 'reconstructed/audio/manifest.json').read_text())
    assert sha(music) == music_manifest['wav_sha256']
    assert music.read_bytes() in pck, 'The exported PCK must contain the exact raw WAV carrier.'
    assert b'sourcelink.json' not in pck
    return {'required_files': required, 'dependency_assets_verified': len(assets), 'runtime': runtime,
            'pe_architecture': 'AMD64', 'template_executable_sha256': sha(package / 'Arconist.exe'),
            'practice_and_reference_bytes_in_pck': True, 'music_wav_sha256': music_manifest['wav_sha256'], 'music_frames': music_manifest['frames'], 'music_duration_seconds': 32,
            'windows_launch': 'NOT RUN', 'human_qualification': 'PENDING'}


def main():
    global ENV, LOGS
    if not __debug__:
        raise RuntimeError('Validation requires Python assertions enabled.')
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--godot', type=Path, required=True)
    p.add_argument('--pack-probe-godot', type=Path, required=True, help='Matching Godot4.7.2 standard executable for headless exported-PCK inspection')
    p.add_argument('--templates', type=Path, required=True, help='4.7.2 mono templates.tpz')
    p.add_argument('--notices', type=Path, required=True, help='Folder of Godot and .NET license notices')
    a = p.parse_args()
    godot = a.godot.resolve()
    ENV = os.environ.copy()
    ENV.update(GODOT_NUPKGS=str(godot.parent / 'GodotSharp/Tools/nupkgs'),
               DOTNET_PROCESSOR_COUNT='1', MSBuildEnableWorkloadResolver='false',
               DOTNET_CLI_TELEMETRY_OPTOUT='1', GODOT_SILENCE_ROOT_WARNING='1')
    if subprocess.check_output(['git', 'status', '--porcelain'], cwd=ROOT, text=True).strip():
        raise RuntimeError('Commit all source changes before the qualification build.')
    LOGS = OUT / 'r010-evidence'
    LOGS.mkdir(parents=True, exist_ok=False)  # Never overwrite an earlier attempt.
    version = run('godot-version', [godot, '--version'])
    assert version.strip().startswith('4.7.2.stable.mono.')
    run('dotnet-info', ['dotnet', '--info'])
    probe_version = run('pack-probe-version', [a.pack_probe_godot.resolve(), '--version'])
    assert probe_version.strip().startswith('4.7.2.stable.')
    run('compose-original-soundtrack', [sys.executable, ROOT / 'reconstructed/audio/compose.py',
        '--output', PROJECT / 'content/audio/clockwork_steps.wav.bytes', '--report', LOGS / 'offline-waveform.json'])
    waveform = json.loads((LOGS / 'offline-waveform.json').read_text())
    expected = json.loads((ROOT / 'reconstructed/audio/manifest.json').read_text())
    assert all(waveform[key] == value for key, value in expected.items())
    shutil.copyfile(ROOT / 'reconstructed/audio/manifest.json', PROJECT / 'content/audio/manifest.json')
    tools = OUT / 'r002-tools'
    tools.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(a.templates) as z:
        assert z.read('templates/version.txt').decode().strip() == '4.7.2.stable.mono'
        for kind in ('debug', 'release'):
            for suffix in ('', '_console'):
                name = f'windows_{kind}_x86_64{suffix}.exe'
                (tools / name).write_bytes(z.read('templates/' + name))
    common = ['-m:1', '-nr:false']
    # Explicit project config also supplies fresh hosts' missing targeting packs.
    run('restore', ['dotnet', 'restore', PROJECT / 'Arconist.Godot.csproj',
                    '--configfile', PROJECT / 'NuGet.Config', *common])
    run('core-build', ['dotnet', 'build', 'reconstructed/Arconist.slnx', '-c', 'Release',
                      '--configfile', 'reconstructed/NuGet.Config', *common])
    run('core-tests', ['dotnet', 'reconstructed/tests/bin/Release/net10.0/Arconist.Tests.dll', '.'])
    for scenario in ('ordinary', 'input-first', 'frame-first'):
        chart = 'ordinary_two_tap' if scenario == 'ordinary' else 'native_late_input_expiry'
        run(scenario, ['dotnet', 'reconstructed/headless/bin/Release/net10.0/Arconist.Headless.dll',
                       f'research_harness/fixtures/{chart}.aff',
                       f'reference_traces/r001/{scenario}.schedule.json', LOGS / (scenario + '.json'),
                       '--reference', f'reference_traces/r001/{scenario}.reference.json'])
    run('r004-build', ['dotnet', 'build', 'reconstructed/hold-tests/Arconist.Hold.Tests.csproj',
                         '-c', 'Release', *common])
    run('r004-core-bridge-tests', ['dotnet', 'reconstructed/hold-tests/bin/Release/net10.0/Arconist.Hold.Tests.dll',
                                  '.', LOGS / 'r004-core'])
    run('r005-build', ['dotnet', 'build', 'reconstructed/audio-tests/Arconist.Audio.Tests.csproj', '-c', 'Release', *common])
    run('r005-core-audio-tests', ['dotnet', 'reconstructed/audio-tests/bin/Release/net10.0/Arconist.Audio.Tests.dll', '.', LOGS / 'r005-core'])
    run('r006-build', ['dotnet', 'build', 'reconstructed/pause-tests/Arconist.Pause.Tests.csproj', '-c', 'Release', *common])
    run('r006-core-pause-tests', ['dotnet', 'reconstructed/pause-tests/bin/Release/net10.0/Arconist.Pause.Tests.dll', '.', LOGS / 'r006-core'])
    run('r007-core-build', ['dotnet', 'build', 'reconstructed/arc-tests/Arconist.Arc.Tests.csproj', '-c', 'Release', *common])
    run('r007-core-tests', ['dotnet', 'reconstructed/arc-tests/bin/Release/net10.0/Arconist.Arc.Tests.dll', '.', LOGS / 'r007-core'])
    run('r007-bridge-build', ['dotnet', 'build', 'reconstructed/arc-bridge-tests/Arconist.Arc.Bridge.Tests.csproj', '-c', 'Release', *common])
    run('r007-bridge-tests', ['dotnet', 'reconstructed/arc-bridge-tests/bin/Release/net10.0/Arconist.Arc.Bridge.Tests.dll', '.', LOGS / 'r007-bridge'])
    run('r008-core-build', ['dotnet', 'build', 'reconstructed/arctap-tests/Arconist.ArcTap.Tests.csproj', '-c', 'Release', *common])
    run('r008-core-tests', ['dotnet', 'reconstructed/arctap-tests/bin/Release/net10.0/Arconist.ArcTap.Tests.dll', '.', LOGS / 'r008-core'])
    run('r008-bridge-build', ['dotnet', 'build', 'reconstructed/arctap-bridge-tests/Arconist.ArcTap.Bridge.Tests.csproj', '-c', 'Release', *common])
    run('r008-bridge-tests', ['dotnet', 'reconstructed/arctap-bridge-tests/bin/Release/net10.0/Arconist.ArcTap.Bridge.Tests.dll', '.', LOGS / 'r008-bridge'])
    run('r009-core-build', ['dotnet', 'build', 'reconstructed/linked-tests/Arconist.Linked.Tests.csproj', '-c', 'Release', *common])
    run('r009-core-tests', ['dotnet', 'reconstructed/linked-tests/bin/Release/net10.0/Arconist.Linked.Tests.dll', '.', LOGS / 'r009-core'])
    run('r009-bridge-build', ['dotnet', 'build', 'reconstructed/linked-bridge-tests/Arconist.Linked.Bridge.Tests.csproj', '-c', 'Release', *common])
    run('r009-bridge-tests', ['dotnet', 'reconstructed/linked-bridge-tests/bin/Release/net10.0/Arconist.Linked.Bridge.Tests.dll', '.', LOGS / 'r009-bridge'])
    run('r010-core-build', ['dotnet','build','reconstructed/group-tests/Arconist.Group.Tests.csproj','-c','Release',*common])
    run('r010-core-tests', ['dotnet','reconstructed/group-tests/bin/Release/net10.0/Arconist.Group.Tests.dll','.',LOGS/'r010-core'])
    run('r010-bridge-build', ['dotnet','build','reconstructed/group-bridge-tests/Arconist.Group.Bridge.Tests.csproj','-c','Release',*common])
    run('r010-bridge-tests', ['dotnet','reconstructed/group-bridge-tests/bin/Release/net10.0/Arconist.Group.Bridge.Tests.dll','.',LOGS/'r010-bridge'])
    run('godot-build', ['dotnet', 'build', PROJECT / 'Arconist.Godot.csproj', '-c', 'Debug', *common])
    run('bridge-build', ['dotnet', 'build', PROJECT / 'tests/Arconist.Bridge.Tests.csproj',
                         '-c', 'Debug', *common])
    run('bridge-tests', ['dotnet', PROJECT / 'tests/bin/Debug/net10.0/Arconist.Bridge.Tests.dll'])
    run('import', [godot, '--headless', '--editor', '--path', PROJECT, '--import', '--quit'])
    run('spatial-tests', [godot, '--headless', '--path', PROJECT, '--', '--spatial-tests',
                           '--evidence-dir=' + str(LOGS / 'spatial')])
    run('r004-headless-tests', [godot, '--headless', '--path', PROJECT, '--', '--hold-tests',
                                '--evidence-dir=' + str(LOGS / 'holds')])
    run('r005-headless-audio-tests', [godot, '--headless', '--path', PROJECT, '--', '--audio-tests',
                                     '--evidence-dir=' + str(LOGS / 'audio')])
    run('r006-headless-pause-tests', [godot, '--headless', '--path', PROJECT, '--', '--pause-tests',
                                     '--evidence-dir=' + str(LOGS / 'pause')])
    run('r007-headless-arc-tests', [godot, '--headless', '--path', PROJECT, '--', '--arc-tests', '--evidence-dir=' + str(LOGS / 'arcs')])
    run('r008-headless-arctap-tests', [godot, '--headless', '--path', PROJECT, '--', '--arctap-tests', '--evidence-dir=' + str(LOGS / 'arctaps')])
    run('r009-headless-linked-tests', [godot, '--headless', '--path', PROJECT, '--', '--linked-tests', '--evidence-dir=' + str(LOGS / 'linked')])
    run('r010-headless-group-tests', [godot,'--headless','--path',PROJECT,'--','--group-tests','--evidence-dir='+str(LOGS/'timing-groups')])
    for path, count in [('r007-core/core-tests.json',31), ('r007-bridge/bridge-tests.json',10), ('arcs/arc-tests.json',13), ('r008-core/arctap-core-tests.json',41), ('r008-bridge/arctap-bridge-tests.json',12), ('arctaps/arctap-tests.json',12), ('r009-core/linked-core-tests.json',25), ('r009-bridge/linked-bridge-tests.json',10), ('linked/linked-tests.json',12),('r010-core/group-core-tests.json',28),('r010-bridge/group-bridge-tests.json',11),('timing-groups/group-tests.json',14)]:
        result = json.loads((LOGS / path).read_text())
        assert result['passed'] == count and result['failed'] == 0 and result['skipped'] == 0, path
    package = OUT / 'r010-windows'
    if package.exists():
        shutil.move(str(package), str(LOGS / 'previous-export'))
    package.mkdir()
    run('windows-export', [godot, '--headless', '--path', PROJECT, '--export-release', 'Windows x64'])
    # Keep the actual .NET exporter logger, beyond Godot's top-level stdout.
    data_home = Path(ENV.get('APPDATA', '')) / 'Godot' if os.name == 'nt' else Path(ENV.get('XDG_DATA_HOME', str(Path.home() / '.local/share'))) / 'godot'
    msbuild_logs = list((data_home / 'mono/build_logs').glob('*_ExportRelease/msbuild_log.txt'))
    if not msbuild_logs:
        raise RuntimeError('Exporter MSBuild diagnostics were not found.')
    shutil.copyfile(max(msbuild_logs, key=lambda f: f.stat().st_mtime), LOGS / 'godot-msbuild-export.log')
    run('exported-pck-audio-probe', [a.pack_probe_godot.resolve(), '--headless', '--main-pack',
        package / 'Arconist.pck', '--script', ROOT / 'reconstructed/audio/export_probe.gd', '--', LOGS / 'exported-audio-probe.json'])
    exported_audio = json.loads((LOGS / 'exported-audio-probe.json').read_text())
    assert exported_audio['status'] == 'PASS' and exported_audio['sha256'] == expected['wav_sha256']
    expected_charts = {f.name:sha(f) for f in sorted((PROJECT/'content').glob('*.aff'))}
    assert len(expected_charts) == 18
    (LOGS/'expected-content.json').write_text(json.dumps(expected_charts,indent=2))
    run('exported-pck-chart-probe', [a.pack_probe_godot.resolve(), '--headless', '--main-pack', package/'Arconist.pck', '--script', ROOT/'reconstructed/arctap/export_probe.gd', '--', LOGS/'expected-content.json', LOGS/'exported-chart-probe.json'])
    exported_charts=json.loads((LOGS/'exported-chart-probe.json').read_text())
    assert exported_charts['status']=='PASS' and len(exported_charts['resources'])==18
    report = verify(package, tools)
    assert sorted(x.name for x in a.notices.iterdir()) == [
        'DOTNET-LICENSE.txt', 'DOTNET-THIRD-PARTY-NOTICES.txt', 'GODOT-COPYRIGHT.txt', 'GODOT-LICENSE.txt']
    shutil.copytree(a.notices, package / 'notices')
    shutil.copyfile(ROOT / 'reconstructed/audio/LICENSE-CC0.txt', package / 'notices/Clockwork-Steps-CC0.txt')
    shutil.copyfile(PROJECT / 'PLAYER.txt', package / 'README.txt')
    source = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    (package / 'SOURCE.txt').write_text(
        'https://github.com/thgillwtnorizoh/arconist\nbranch: main\ncommit: ' + source +
        '\nGodot 4.7.2 .NET; SDK 10.0.402; bundled runtime 10.0.13\n'
        'READY FOR HUMAN QUALIFICATION. R010 acceptance pending. Godot audio output is not human qualification.\n', encoding='utf-8')
    files = sorted(f for f in package.rglob('*') if f.is_file())
    manifest = {f.relative_to(package).as_posix(): sha(f) for f in files}
    (package / 'SHA256SUMS.txt').write_text(''.join(f'{v}  {k}\n' for k, v in manifest.items()), encoding='utf-8')
    archive = OUT / 'Arconist-R010-Windows-x64.zip'
    with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for f in sorted(package.rglob('*')):
            if f.is_file():
                z.write(f, 'Arconist-R010/' + f.relative_to(package).as_posix())
    # Validate CRCs and every extracted payload hash, independently of source paths.
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        z.extractall(LOGS / 'extracted')
    extracted = LOGS / 'extracted/Arconist-R010'
    for name, expected in manifest.items():
        assert sha(extracted / name) == expected, name
    assert sha(extracted / 'SHA256SUMS.txt') == sha(package / 'SHA256SUMS.txt')
    report.update(source_commit=source, branch='main',
                  archive=archive.name, archive_bytes=archive.stat().st_size, archive_sha256=sha(archive),
                  payload_files=len(manifest), zip_crc_and_extracted_hashes='PASS')
    (LOGS / 'package-integrity.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    shutil.copyfile(package / 'SHA256SUMS.txt', LOGS / 'WINDOWS-PAYLOAD-SHA256SUMS.txt')
    (LOGS / 'WINDOWS-ZIP-SHA256.txt').write_text(report['archive_sha256'] + '  ' + archive.name + '\n', encoding='utf-8')
    shutil.copyfile(ROOT / 'reconstructed/validation/R010.md', LOGS / 'R010.md')
    baseline = '8f351b77b2a247497f2062c786cca09842c78ea3'
    changed = subprocess.check_output(['git','diff','--name-status',baseline,source],cwd=ROOT,text=True)
    (LOGS / 'changed-files.txt').write_text(changed)
    baseline_files = subprocess.check_output(['git','ls-tree','-r','--name-only',baseline],cwd=ROOT,text=True).splitlines()
    inventory=[]
    for name in baseline_files:
        old=subprocess.check_output(['git','rev-parse',baseline+':'+name],cwd=ROOT,text=True).strip()
        new=subprocess.check_output(['git','rev-parse',source+':'+name],cwd=ROOT,text=True).strip()
        protected=not name.startswith('reconstructed/')
        if protected: assert old==new,name
        inventory.append(dict(path=name,before=old,after=new,identical=old==new,protected=protected))
    prior=subprocess.check_output(['git','show',baseline+':reconstructed/contexts.md'],cwd=ROOT)
    assert (ROOT/'reconstructed/contexts.md').read_bytes().startswith(prior)
    (LOGS/'preservation.json').write_text(json.dumps(dict(baseline=baseline,source=source,all_research_preserved=True,history_prefix_bytes=len(prior),inventory=inventory),indent=2))
    development=Path(ENV.get('ARCONIST_DEVELOPMENT_EVIDENCE',''))
    if str(development)!='.' and development.is_dir(): shutil.copytree(development, LOGS/'development',ignore=shutil.ignore_patterns('extracted'))
    toolchain = {str(f.resolve()):sha(f) for f in [a.templates,godot,a.pack_probe_godot.resolve()]}
    (LOGS/'toolchain-sha256.json').write_text(json.dumps(toolchain,indent=2))
    evidence_zip = OUT / 'Arconist-R010-Technical-Evidence.zip'
    with zipfile.ZipFile(evidence_zip, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for f in sorted(LOGS.rglob('*')):
            if f.is_file() and f.relative_to(LOGS).parts[0] not in ('extracted', 'previous-export'):
                z.write(f, 'Arconist-R010-Evidence/' + f.relative_to(LOGS).as_posix())
    with zipfile.ZipFile(evidence_zip) as z:
        assert z.testzip() is None
    print(json.dumps(report, indent=2))
    print('READY FOR HUMAN QUALIFICATION — no Windows execution or GUI interaction performed.')


if __name__ == '__main__':
    main()
