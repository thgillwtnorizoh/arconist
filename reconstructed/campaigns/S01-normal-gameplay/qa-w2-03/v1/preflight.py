#!/usr/bin/env python3
"""Read-only prerequisite/source inventory; writes only its evidence receipt.
Never invokes dotnet, restore, build, a native VM, or production assemblies.
"""
import argparse,hashlib,json,os,platform,shutil,subprocess,zipfile
from pathlib import Path
SHA='0007c7719eb9b3ea377230a55d6fcfaedbe29898'
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--production-root',required=True);ap.add_argument('--workspace',required=True);ap.add_argument('--output',required=True);a=ap.parse_args();prod=Path(a.production_root).resolve();workspace=Path(a.workspace).resolve()
 def git(*args):return subprocess.check_output(['git',*args],cwd=prod)
 assert git('rev-parse','HEAD').decode().strip()==SHA,'wrong production checkout'
 files=git('ls-tree','-r','--name-only',SHA,'reconstructed/core','reconstructed/godot/bridge','reconstructed/records').decode().splitlines();hashes={}
 for name in files:
  b=(prod/name).read_bytes();assert b==git('show',SHA+':'+name),name;hashes[name]=hashlib.sha256(b).hexdigest()
 home=Path.home();candidates=[Path('/tmp/qa202-dotnet'),Path('/usr/share/dotnet'),Path('/usr/lib/dotnet'),Path('/usr/local/share/dotnet'),Path('/opt/dotnet'),home/'.dotnet',Path('/home/agent/.dotnet')]
 dotnet=shutil.which('dotnet')
 if dotnet:candidates.append(Path(dotnet).resolve().parent)
 roots=[]
 for p in dict.fromkeys(candidates):
  roots.append(dict(path=str(p),exists=p.exists(),host=(p/'dotnet').is_file(),sdks=[q.name for q in (p/'sdk').glob('*')] if (p/'sdk').is_dir() else [],runtimes=[str(q.relative_to(p)) for q in (p/'shared').glob('*/*')] if (p/'shared').is_dir() else [],netstandardRef=(p/'packs/NETStandard.Library.Ref/2.1.0').is_dir()))
 packages=[home/'.nuget/packages/netstandard.library.ref/2.1.0',Path('/tmp/qa202-dotnet/packs/NETStandard.Library.Ref/2.1.0')]
 assemblyNames={'Arconist.Core.dll','Arconist.Bridge.dll','Arconist.Records.dll'}
 assemblies=[str(p.relative_to(workspace)) for p in workspace.rglob('Arconist.*.dll') if p.name in assemblyNames]
 configs={name:(prod/name).read_text() for name in ['reconstructed/NuGet.Config','reconstructed/godot/NuGet.Config']}
 archive=workspace/'project_sources/01-arccopy.zip';binary=None
 if archive.exists():
  with zipfile.ZipFile(archive) as z:binary=hashlib.sha256(z.read('lib/arm64-v8a/libcocos2dcpp.so')).hexdigest()
 assert binary=='3eaca4e6dabb3395f276f8915698d57675757d0df0970e716b23a3dc201c79be'
 blockers=[]
 if not any(r['host'] and r['sdks'] and r['runtimes'] for r in roots):blockers.append('No already available .NET SDK/runtime host found in PATH or enumerated standard/prior locations.')
 if not any(r['netstandardRef'] for r in roots) and not any(p.is_dir() for p in packages):blockers.append('NETStandard.Library.Ref 2.1.0 absent from enumerated SDK/package-cache locations.')
 if not assemblies:blockers.append('No exact-build Core/Bridge/Records assembly set available in workspace; no binary provenance fallback.')
 out=dict(status='BLOCKED' if blockers else 'READINESS REQUIRES MANUAL PROVENANCE REVIEW',productionSha=SHA,runtimeTested=False,environment=platform.platform(),python=platform.python_version(),dotnetOnPath=dotnet,toolchainLocations=roots,referencePackageLocations=[dict(path=str(p),exists=p.is_dir()) for p in packages],workspaceAssemblyCandidates=assemblies,nugetConfigurations=configs,godotBundledSource=dict(configuredValue=os.environ.get('GODOT_NUPKGS'),exists=bool(os.environ.get('GODOT_NUPKGS') and Path(os.environ['GODOT_NUPKGS']).is_dir())),sourceFileSha256=hashes,sourceFileCount=len(hashes),archiveLibrarySha256=binary,blockers=blockers,buildAttempts=0,restoreAttempts=0,installAttempts=0,runtimePass=0,runtimeFail=0,runtimeSkip=0,notRun=['A original rule comparisons','B actual session result/save','C disk fresh-process durability','D regressions and mutation discrimination'],firstProductionDifference=None)
 Path(a.output).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out));return 2 if blockers else 0
if __name__=='__main__':raise SystemExit(main())
