#!/usr/bin/env python3
"""Independent offline comparisons with immutable prior native trace and E006 math."""
import hashlib,json,struct,sys,subprocess
from pathlib import Path
P=Path(__file__).resolve().parent;old=P.parent/'w102-p01';x=json.loads((P/'native-ledger.json').read_text());ref=json.loads((old/'native-ledger.json').read_text())['scenes'][1]
checks=[];diff=[]
def check(field,expected,actual):
 checks.append(field)
 if expected!=actual:diff.append(dict(field=field,expected=expected,actual=actual))
check('budget.reserved',1,x['budget']['reservedScenes']);check('execution.completed','pass',x['status'])
check('driver hash',x['driverSha256'],hashlib.sha256((P/'run.py').read_bytes()).hexdigest())
check('fixture hash','cbf47e5c83e070533bee8bc1b1e31b59209e452d43b612832f3cd02fad2cb0e1',x['fixture']['sha256'])
for field in ['parentMode','N','end','mainContainsParent','mainContainsChildren','listener']:
 check('prepared.'+field,ref['nativeObjects'][field],x['beforeInput']['prepared'][field])
check('raw parsed modes',[0,0],[r['mode'] for r in x['parsed']])
check('normalization before store',0,x['normalization'][0]['storedMode']);check('normalization after store',1,x['normalization'][1]['storedMode'])
check('normalization writer PC','0xc66654',x['normalization'][0]['pc'])
for c in x['beforeInput']['prepared']['children']:check('native backlink '+str(c['time']),x['nativeObjects']['parent'],c['parent'])
check('event schedule',[e['label'] for e in ref['events']],[e['label'] for e in x['events']])
for a,b in zip(ref['events'],x['events']):
 label=a['label']
 for field in ['E','lastModelE','score','mask','androidMapSize','finishedResult']:
  check(label+'.'+field,a[field],b[field])
 for field in ['mode','activity','cache','owner']:
  check(label+'.parent.'+field,a['parent'][field],b['parent'][field])
 for field in ['time','end','group','input','geometry','missed','consumed','contact']:
  check(label+'.children.'+field,[c[field] for c in a['children']],[c[field] for c in b['children']])
 check(label+'.contact IDs',[c['generatedId'] for c in a['contacts']],[c['generatedId'] for c in b['contacts']])
check('recorder count',2,len(x['recorders']))
f=lambda v:struct.unpack('<f',struct.pack('<f',v))[0];gain=f(f(f(200+f(2*.5))/2.5)/2);h=0
for i,r in enumerate(x['recorders'],1):
 h=f(h+gain)
 for field,expected in [('healthBits',struct.unpack('<I',struct.pack('<f',h))[0]),('score',10000000*i//2+i),('PURE',i),('FAR',0),('LOST',0),('combo',i)]:check('callback'+str(i)+'.'+field,expected,r['after'][field])
 check('callback'+str(i)+'.recorder','0x1730290',r['recorder'])
check('no body accepts',[],x['bodyAcceptances']);check('cleanup contacts',[],x['final']['contacts']);check('result boundary','0x0',x['final']['finishedResult'])
for field in ['candidates','classifiers','spatial','guardReads']:
 def clean(obj):
  if isinstance(obj,dict):return {k:clean(v) for k,v in obj.items() if k not in ['pointer','child']}
  if isinstance(obj,list):return [clean(v) for v in obj]
  return obj
 check(field+' semantic ledger',clean(ref[field]),clean(x[field]))
check('prepared checkpoint times/weights',[(r['time'],r['weight'],r['resolved']) for r in ref['nativeObjects']['records']],[(r['time'],r['weight'],r['resolved']) for r in x['beforeInput']['prepared']['records']])
check('final checkpoint states',[(r['time'],r['weight'],r['resolved']) for r in ref['final']['parent']['records']],[(r['time'],r['weight'],r['resolved']) for r in x['final']['parent']['records']])
root=P.parents[3]
for path in [P/'run.py',old/'observe.py']:
 expected=subprocess.check_output(['git','show',x['executionSha']+':'+str(path.relative_to(root))],cwd=root)
 check('Git source identity '+path.name,hashlib.sha256(expected).hexdigest(),hashlib.sha256(path.read_bytes()).hexdigest())
out=dict(status='PASS'  if not diff else 'FAIL',checks=len(checks),passCount=len(checks)-len(diff),failCount=len(diff),skipCount=0,firstDifference=diff[0] if diff else None,allDifferences=diff,oracle='Immutable P01 Scene2 native ledger and independent E006 binary32 recurrence; not Work2 outputs',nativeScenesCreated=0)
(P/'audit-receipt.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out));sys.exit(bool(diff))
