#!/usr/bin/env python3
"""Validate independent source corpus; execute pinned production only with dotnet10.
Exit0 executed all selected comparisons passed;1 differences;2 execution BLOCKED.
--validate-only never claims production PASS. No expected files are rewritten.
"""
import argparse,hashlib,json,pathlib,shutil,subprocess,sys,platform
HERE=pathlib.Path(__file__).resolve().parent

def git(root,*args):return subprocess.check_output(['git','-C',str(root),*args])
def main():
 p=argparse.ArgumentParser();p.add_argument('--production-root',type=pathlib.Path,required=True);p.add_argument('--output',type=pathlib.Path,required=True);p.add_argument('--validate-only',action='store_true');a=p.parse_args()
 m=json.loads((HERE/'manifest.json').read_text());root=a.production_root.resolve();expected=m['productionSha'];checks=0
 try:
  git(root,'cat-file','-e',expected+'^{commit}')
  protected=[x for x in git(root,'ls-tree','-r','--name-only',expected).decode().splitlines() if x.startswith(('reconstructed/core/','reconstructed/godot/bridge/')) and x.endswith(('.cs','.csproj'))]
  for f in protected:
   if (root/f).read_bytes()!=git(root,'show',expected+':'+f):raise ValueError('production mismatch '+f)
  for f in m['cases']:
   c=json.loads((HERE/f).read_text());assert c['evidence'] and c['requirements'];assert c['classification'] in ('RUNNABLE','EXPECTED REJECTION','RESEARCH BLOCKED')
   assert hashlib.sha256((HERE/c['aff']).read_bytes()).hexdigest()==c['affSha256'];assert 'normalizedObjects'in c and 'events'in c
   if c['classification']=='RUNNABLE':assert any(ev.get('expect') for ev in c['events'])
   checks+=1
 except Exception as e:
  a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps({'status':'FAIL','firstDifference':'preflight: '+str(e)},indent=2));return 1
 dotnet=shutil.which('dotnet');version=None
 if dotnet:
  q=subprocess.run([dotnet,'--list-sdks'],capture_output=True,text=True);version=q.stdout
 available=bool(version and any(line.startswith('10.') for line in version.splitlines()))
 report={'status':'VALIDATED_CORPUS_ONLY' if a.validate_only else 'BLOCKED' if not available else 'RUNNING','productionSha':expected,'productionRuntimeTested':False,'environment':platform.platform(),'python':platform.python_version(),'dotnet':dotnet,'sdks':version,'structuralCasesValidated':checks,'protectedProductionFiles':len(protected),'runtimePassed':0,'runtimeFailed':0,'runtimeSkipped':0,'runtimeNotRun':checks,'firstDifference':None,'blocker':None if available else 'dotnet SDK10.x not installed/on PATH; C# driver NOT COMPILED/NOT RUN','independence':'Expectations unchanged; no production output used to create expected values'}
 a.output.parent.mkdir(parents=True,exist_ok=True)
 if a.validate_only or not available:a.output.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2));return 0 if a.validate_only else 2
 command=[dotnet,'run','--project',str(HERE/'driver/Driver.csproj'),'-c','Release','-p:ProductionRoot='+str(root),'--',str(HERE),str(a.output.resolve())]
 if a.output.exists():a.output.unlink()
 run=subprocess.run(command,capture_output=True,text=True)
 # Preserve raw compiler/runtime evidence separately; never turn failed compilation into comparisons.
 a.output.with_suffix('.log').write_text('COMMAND '+json.dumps(command)+'\n'+run.stdout+'\n'+run.stderr)
 if not a.output.exists():report.update(status='BLOCKED',blocker='Driver build/run produced no result; inspect log',command=command,exit=run.returncode);a.output.write_text(json.dumps(report,indent=2));return 2
 return run.returncode
if __name__=='__main__':sys.exit(main())
