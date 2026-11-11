#!/usr/bin/env python3
"""R005: logged technical checks and Windows packaging; never GUI playtesting."""
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
    for chart in ('practice.aff', 'ordinary_two_tap.aff', 'mixed_practice.aff', 'native_hold.aff', 'hold_first.aff', 'tap_first.aff', 'audible_practice.aff', 'audible_aff120.aff'):
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
    LOGS = OUT / 'r005-evidence'
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
    package = OUT / 'r005-windows'
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
        'READY FOR HUMAN QUALIFICATION. R005 acceptance pending. Godot audio output is not human qualification.\n', encoding='utf-8')
    files = sorted(f for f in package.rglob('*') if f.is_file())
    manifest = {f.relative_to(package).as_posix(): sha(f) for f in files}
    (package / 'SHA256SUMS.txt').write_text(''.join(f'{v}  {k}\n' for k, v in manifest.items()), encoding='utf-8')
    archive = OUT / 'Arconist-R005-Windows-x64.zip'
    with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for f in sorted(package.rglob('*')):
            if f.is_file():
                z.write(f, 'Arconist-R005/' + f.relative_to(package).as_posix())
    # Validate CRCs and every extracted payload hash, independently of source paths.
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        z.extractall(LOGS / 'extracted')
    extracted = LOGS / 'extracted/Arconist-R005'
    for name, expected in manifest.items():
        assert sha(extracted / name) == expected, name
    assert sha(extracted / 'SHA256SUMS.txt') == sha(package / 'SHA256SUMS.txt')
    report.update(source_commit=source, branch='main',
                  archive=archive.name, archive_bytes=archive.stat().st_size, archive_sha256=sha(archive),
                  payload_files=len(manifest), zip_crc_and_extracted_hashes='PASS')
    (LOGS / 'package-integrity.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    shutil.copyfile(package / 'SHA256SUMS.txt', LOGS / 'WINDOWS-PAYLOAD-SHA256SUMS.txt')
    (LOGS / 'WINDOWS-ZIP-SHA256.txt').write_text(report['archive_sha256'] + '  ' + archive.name + '\n', encoding='utf-8')
    shutil.copyfile(ROOT / 'reconstructed/validation/R005.md', LOGS / 'R005.md')
    evidence_zip = OUT / 'Arconist-R005-Technical-Evidence.zip'
    with zipfile.ZipFile(evidence_zip, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for f in sorted(LOGS.rglob('*')):
            if f.is_file() and f.relative_to(LOGS).parts[0] not in ('extracted', 'previous-export'):
                z.write(f, 'Arconist-R005-Evidence/' + f.relative_to(LOGS).as_posix())
    with zipfile.ZipFile(evidence_zip) as z:
        assert z.testzip() is None
    print(json.dumps(report, indent=2))
    print('READY FOR HUMAN QUALIFICATION — no Windows execution or GUI interaction performed.')


if __name__ == '__main__':
    main()
