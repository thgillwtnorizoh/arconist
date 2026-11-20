from pathlib import Path
import subprocess,json,os
root=Path.cwd();b=root/'reconstructed/campaigns/S01-normal-gameplay';out=Path('/tmp/qa-w2-01-history');out.mkdir(parents=True,exist_ok=True);env=dict(os.environ);env.update(DOTNET_NOLOGO='1',DOTNET_CLI_TELEMETRY_OPTOUT='1',DOTNET_PROCESSOR_COUNT='1')
records=[]
def run(c):
 r=subprocess.run(c,capture_output=True,text=True,env=env);rec=dict(command=c,exit=r.returncode,stdout=r.stdout,stderr=r.stderr);records.append(rec);print(c[-1],r.returncode,flush=True);return r
historical=json.loads((b/'independent-corpus/results/c01/historical-commands.json').read_text())
for suite in historical:
 for rec in suite['logs']:
  c=[str(x).replace('/workspace/scratch/e83b3992fd3d/toolchain-c01/dotnet/dotnet','dotnet').replace('/workspace/scratch/e83b3992fd3d/c01',str(root)).replace('/tmp/c01-historical','/tmp/qa-historical') for x in rec['command']];run(c)
p=root/'reconstructed/mixed-tests/Arconist.Mixed.Tests.csproj';run(['dotnet','build',str(p),'-c','Release','-m:1','-nr:false']);run(['dotnet',str(p.parent/'bin/Release/net10.0/Arconist.Mixed.Tests.dll'),str(root),'/tmp/qa-historical/mixed-tests'])
# Old independent fixture files and manifest remain immutable. Outer identity records actual tested SHA.
p=b/'independent-corpus/driver/Driver.csproj';run(['dotnet','build',str(p),'-c','Release','-p:ProductionRoot='+str(root),'-m:1','-nr:false']);run(['dotnet',str(p.parent/'bin/Release/net10.0/Driver.dll'),str(b/'independent-corpus'),'/tmp/qa-historical-independent.json'])
(out/'historical-commands.json').write_text(json.dumps(records,indent=2)+'\n')
print('commands',len(records),'nonzero',sum(r['exit']!=0 for r in records),flush=True)
