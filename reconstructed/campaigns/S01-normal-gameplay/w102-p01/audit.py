#!/usr/bin/env python3
"""Offline validation/normalization of the one completed execution; never creates native scenes."""
import argparse,hashlib,json,struct,subprocess
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p):return json.loads(p.read_text())
def main():
 p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args();x=load(HERE/'native-ledger.json');cmd=load(HERE/'results/command.json');checks=0
 assert x['status']=='blocked' and cmd['exit']==1;checks+=1
 assert x['budget']['reservedScenes']==3 and x['sceneLimit']==3 and len(x['scenes'])==3;checks+=1
 assert [s['status'] for s in x['scenes']]==['pass','pass','blocked'];checks+=1
 assert sha((HERE/'native-ledger.json').read_bytes())==cmd['selectedSemanticLedgerSha256'];checks+=1
 for filename,digest in x['scriptSha256'].items():
  path=HERE/filename;original=subprocess.check_output(['git','show',x['executionCheckoutSha']+':'+str(path.relative_to(ROOT))],cwd=ROOT);assert sha(original)==digest==sha(path.read_bytes());checks+=1
 for s in x['scenes']:
  assert sha((HERE/'fixtures'/s['fixture']['file']).read_bytes())==s['fixture']['sha256'];checks+=1
  o=s['nativeObjects'];ps={c['pointer'] for c in o['children']};assert len(ps)==len(o['children']);checks+=1
  assert all(c['parent']==o['parent'] for c in o['children']);checks+=1
  assert all(c['type']=='15LogicArcTapNote' for c in o['children']);checks+=1
  assert s['countProducer'][-1]['N']==o['N'];checks+=1
 control,trace,ordinary=x['scenes'];assert control['historicalE025']['identity_checks']['native_consumption_guard'];checks+=1
 assert trace['nativeObjects']['N']==2 and trace['nativeObjects']['parentMode']==1;checks+=1
 assert len(trace['recorders'])==2 and all(r['recorder']=='0x1730290' for r in trace['recorders']);checks+=1
 assert all(r['note'] in {c['pointer'] for c in trace['nativeObjects']['children']} for r in trace['recorders']);checks+=1
 events={e['label']:e for e in trace['events']}
 assert events['displaced DOWN negative']['score']['PURE']==0;checks+=1
 assert events['first child fresh-ID duplicate']['score']['PURE']==1;checks+=1
 assert events['repeat FRAME after MOVE without fresh DOWN']['score']['PURE']==1 and events['repeat FRAME after MOVE without fresh DOWN']['children'][1]['consumed']==0;checks+=1
 assert events['second child fresh-ID duplicate']['score']['PURE']==2;checks+=1
 assert not trace['final']['contacts'] and trace['final']['mask']==trace['final']['androidMapSize']==0;checks+=1
 assert all(r['resolved']==0 for r in trace['final']['parent']['records']) and not trace['bodyAcceptances'];checks+=1
 assert all(e['finishedResult']=='0x0' for e in trace['events']);checks+=1
 f=lambda v:struct.unpack('<f',struct.pack('<f',v))[0];gain=f(f(f(200+f(2*.5))/2.5)/2);h=0;arithmetic=[]
 for i,r in enumerate(trace['recorders'],1):
  h=f(h+gain);bits=struct.unpack('<I',struct.pack('<f',h))[0];assert r['after']['healthBits']==bits;assert r['after']['score']==10000000*i//2+i;checks+=2;arithmetic.append(dict(unit=i,nativeHealthBits=bits,nativeScore=r['after']['score']))
 assert all(p['mode']==0 for p in ordinary['parsed']) and ordinary['nativeObjects']['parentMode']==1 and ordinary['nativeObjects']['N']==2;checks+=1
 assert ordinary['failure']['message']=='native parent mode disagrees with supplied AFF' and not ordinary['events'] and not ordinary['recorders'] and not ordinary['classifiers'];checks+=1
 out=dict(status='PASS offline evidence validation only; native experiment remains BLOCKED',checks=checks,failures=0,skips=0,nativeFreshScenesCreatedByAudit=0,executionSourceSha=x['executionCheckoutSha'],sceneStatuses=['PASS','PASS','BLOCKED before input'],N2='confirmed original trace count',N5='refuted for supplied false+children fixture; mode1/N2 observed',scene3Judgment='NOT RUN',arithmetic=arithmetic)
 dest=Path(a.output);dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
if __name__=='__main__':main()
