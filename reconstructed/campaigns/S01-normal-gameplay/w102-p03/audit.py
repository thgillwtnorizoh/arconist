#!/usr/bin/env python3
"""Offline blocked-ledger audit. Does not import/start a native VM."""
import json,hashlib,subprocess,re
from pathlib import Path
P=Path(__file__).resolve().parent;ROOT=P.parents[3];checks=[]
def check(label,ok):
 checks.append(label)
 assert ok,label
x=json.loads((P/'native-ledger.json').read_text());s=x['scenes'][0];cmd=json.loads((P/'command.json').read_text())
check('one reserved scene',x['budget']['reserved']==1);check('budget limit4',x['budget']['limit']==4);check('one scene ledger',len(x['scenes'])==1);check('blocked Scene A',s['status']=='blocked');check('exact ABI failure',s['error']=='unhandled import 0x1a6e300 asin caller=0x17d26c8');check('native exit1',cmd['exitCode']==1)
check('captured ledger checksum',hashlib.sha256((P/'native-ledger.json').read_bytes()).hexdigest()==cmd['ledgerSha256'])
for name in ['run.py','fixtures.json']:
 f=P/name;raw=f.read_bytes();original=subprocess.check_output(['git','show',x['sourceSha']+':'+str(f.relative_to(ROOT))],cwd=ROOT);check('Git frozen source '+name,raw==original)
check('executed driver checksum',hashlib.sha256((P/'run.py').read_bytes()).hexdigest()==x['driverSha256'])
for f in json.loads((P/'fixtures.json').read_text()):
 b=(ROOT/f['path']).read_bytes();check('fixture bytes '+f['scene'],hashlib.sha256(b).hexdigest()==f['sha256'] and b.decode()==f['raw']);check('fixture frozen Git '+f['scene'],b==subprocess.check_output(['git','show',x['sourceSha']+':'+f['path']],cwd=ROOT))
check('two ground factory products',len([r for r in s['production'] if r['stage']=='prepared'])==2);check('tap and hold RTTI',{r['type'] for r in s['production'] if r['stage']=='prepared'}=={'12LogicTapNote','13LogicHoldNote'})
check('one original child factory',len(s['factories'])==1 and s['factories'][0]['type']=='15LogicArcTapNote');child=s['factories'][0]['pointer'];check('native child backlink write',any(r['object']==child and r['pc']=='0x1865514' and r['offset']=='0x90' for r in s['writes']));check('native geometry writer',any(r['object']==child and r['pc']=='0x1925888' for r in s['writes']))
check('count helper completed',len(s['countProducer'])==1 and isinstance(s['countProducer'][0].get('N'),int));check('native main-sort observed',bool(s['mainSortCalls']))
for name in ['candidates','visits','stops','classifiers','spatial','recorders','events','lanes']:check('unexecuted input '+name,s[name]==[])
check('later scenes not run',cmd['notRunScenes']==3);check('no claimed input permutation',json.loads((P/'sorting-permutations.json').read_text())['status']=='NOT RUN')
for f in P.glob('*.json'):json.loads(f.read_text())
for link in re.findall(r'\[[^\]]*\]\(([^)]+)\)',(P.parent/'W102-P03-report.md').read_text()):check('report link '+link,(P.parent/link).exists())
out=dict(status='PASS blocked-evidence audit only; native assignment BLOCKED',checks=len(checks),failures=0,skips=0,nativeScenesCreated=0,nativeCompleted=0,nativeBlocked=1,notRunScenes=3,details=checks)
(P/'audit-receipt.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='details'}))
