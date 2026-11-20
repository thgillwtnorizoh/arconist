from pathlib import Path
import json,shutil,subprocess,os,hashlib
root=Path.cwd();b=root/'reconstructed/campaigns/S01-normal-gameplay/qa-w2-01/v1';tmp=Path('/tmp/qa-comparator-controls');tmp.mkdir(exist_ok=True);shutil.copytree(b/'fixtures',tmp/'fixtures',dirs_exist_ok=True);(tmp/'cases').mkdir(exist_ok=True)
controls=[]
for name in ['CURVE-si','CROSS-E028','SHARED-cancel-focus-far-lost']:
 c=json.loads((b/'cases'/f'{name}.json').read_text())
 if name=='CURVE-si':c['geometry'][1]['expect']['xBits']+=1;target='$.geometry[1].xBits'
 elif name=='CROSS-E028':
  ev=next(ev for ev in c['events'] if ev['op']=='FRAME' and ev.get('e')==1750);ev['expect']['proximity'][0]['distance']={'approx':255.1575927734,'tolerance':.00005};target=f"$.events[{c['events'].index(ev)}].proximity[0].distance"
 else:c['events'][14]['expect']['arcs'][0]['holding']=True;target='$.events[14].arcs[0].holding'
 (tmp/'cases/mutant.json').write_text(json.dumps(c));(tmp/'manifest.json').write_text(json.dumps({'productionSha':'49e7c263a36aebcc0316e010a629c6bfdf205f6d','cases':['cases/mutant.json']}))
 r=subprocess.run(['dotnet',str(b/'driver/bin/Release/net10.0/Driver.dll'),str(tmp),str(tmp/'runtime.json')],capture_output=True,text=True);data=json.loads((tmp/'runtime.json').read_text());first=data['results'][0]['firstDifference'];assert r.returncode==1 and first.startswith(target),(name,r.returncode,first,target);controls.append({'id':name,'expectedExit':1,'actualExit':r.returncode,'firstDifference':first,'purpose':'deliberately corrupted expectation in temporary copy only; comparator sensitivity, not production failure'})
(tmp/'comparator-controls.json').write_text(json.dumps(controls,indent=2)+'\n')
# Outer receipt for immutable historical corpus: do not mislabel the embedded historical productionSha.
x=json.load(open('/tmp/qa-historical-independent.json'));legacy={'actualProductionSha':'49e7c263a36aebcc0316e010a629c6bfdf205f6d','historicalManifestProductionSha':x['productionSha'],'profile':'R010','passed':sum(r['status']=='PASS' for r in x['results']),'failed':sum(r['status']!='PASS' for r in x['results']),'firstDivergences':[{'id':r['id'],'firstDifference':r['firstDifference']} for r in x['results'] if r['status']!='PASS'],'cases':[{'id':r['id'],'status':r['status'],'events':len(r.get('trace',[]))} for r in x['results']],'rawOutputSha256':hashlib.sha256(Path('/tmp/qa-historical-independent.json').read_bytes()).hexdigest(),'blockedNotRun':['G-006','G-007','G-009','G-010']}
(tmp/'historical-independent.json').write_text(json.dumps(legacy,indent=2)+'\n')
print('3 comparator controls detected, historical',legacy['passed'])
