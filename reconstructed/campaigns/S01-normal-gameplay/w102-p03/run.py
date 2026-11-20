#!/usr/bin/env python3
"""Four reserved-before-setup scenes; read-only semantic observations, no retries."""
import sys,json,hashlib,argparse,subprocess,traceback,math,collections
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];sys.path[:0]=[str(HERE.parent/'w102-p01'),str(ROOT/'research_harness/src')]
from observe import Observer
import config
from solo_entry import setup,entry
from lifecycle import activate,frame
from arc_tap_services import install
from jni_arrays import InputArrays
from unicorn import UC_HOOK_CODE

def scene(spec,out):
 raw=(ROOT/spec['path']).read_bytes();assert hashlib.sha256(raw).hexdigest()==spec['sha256'];config._fixture_name=str((ROOT/spec['path']).resolve());out['fixture']=spec
 n=setup(True);abi=install(n);n.prepare_runtime();obs=Observer(n,out);out.update(production=[],visits=[],stops=[],lanes=[],mainSortCalls=[]);visited={}
 def hook(u,pc,size,data):
  if pc in [0x18640d8,0x18649b8]:
   a=n.x(27);out['production'].append(dict(stage='parsed',kind='tap' if pc==0x18640d8 else 'hold',pointer=hex(a),start=n.i(a+0x18),end=n.i(a+0x1c),rawLane=n.i(n.q(a+0x20)+8)))
  elif pc in [0x18640dc,0x18649bc]:
   a=n.x(25) if pc==0x18640dc else n.x(0);out['production'].append(dict(stage='prepared',pointer=hex(a),type=n.typename(a),start=n.i(a+0x18),end=n.i(a+0x1c)))
  elif pc==0x7b6a08:out['mainSortCalls'].append(dict(begin=hex(n.x(0)),end=hex(n.x(1)),caller=hex(n.x(30))))
  elif pc==0xeec53c:
   a=n.q(n.x(20));visited[n.phase]=a;out['visits'].append(dict(phase=n.phase,note=hex(a),type=n.typename(a),start=n.i(a+0x18)))
  elif pc in [0xeec570,0xeec6f4]:out['stops'].append(dict(phase=n.phase,note=hex(visited.get(n.phase,0)),reason='classifier_true' if pc==0xeec570 else 'hold_latch',pc=hex(pc)))
  elif pc==0xeec6ec:out.setdefault('latches',[]).append(dict(phase=n.phase,note=hex(n.x(0)),before=n.u.mem_read(n.x(0)+0xa8,1)[0]))
  elif pc==0xeec1cc:out['lanes'].append(dict(phase=n.phase,primary=n.x(0)&0xffffffff,secondary=n.x(0)>>32))
 for pc in [0x18640d8,0x18649b8,0x18640dc,0x18649bc,0x7b6a08,0xeec53c,0xeec570,0xeec6f4,0xeec6ec,0xeec1cc]:n.u.hook_add(UC_HOOK_CODE,hook,begin=pc,end=pc)
 n.call(0x1930604);n.call(0x1054f24);n.trace=[];n.visual=[];n.animationTrace=[];n.downstream=[];n.env=n.alloc(8);n.now=1000;entry(n);activate(n)
 chart=n.q(n.model+0x28);parents=[p for p in n.items(chart,0x20) if n.typename(p)=='12LogicArcNote'];assert len(parents)==1,'missing original parent';obs.parent=parents[0];obs.ownership()
 def notes():
  rows=[]
  for a in n.items(chart,0x20):
   t=n.typename(a)
   if t not in ['12LogicArcNote','12LogicTapNote','13LogicHoldNote']:continue
   row=dict(pointer=hex(a),type=t,start=n.i(a+0x18),end=n.i(a+0x1c),group=n.i(a+0x50),input=n.u.mem_read(a+0x54,1)[0],active=a in n.items(n.model,0xa0))
   if t!='12LogicArcNote':row.update(lane=n.i(n.q(a+0x20)+0x10),consumed=n.u.mem_read(a+0xd,1)[0],missed=n.u.mem_read(a+0xc,1)[0])
   if t=='13LogicHoldNote':row.update(latch=n.u.mem_read(a+0xa8,1)[0],activity=list(n.u.mem_read(a+0x64,2)),records=obs.record_state(a))
   rows.append(row)
  return rows
 out['preparedMain']=notes();out['index']=[{str(k):[hex(a) for a in v] for k,v in g.items()} for g in n.maps(n.model)]
 camera=n.q(n.q(n.model+0x20)+0x2a8);world=[212.5,0.,0.];src,dst=n.alloc(12),n.alloc(8)
 for i,v in enumerate(world):n.wf(src+i*4,v)
 n.call(0xbdbb70,camera,src,regs={8:dst});xy=[n.f(dst),n.f(n.director+0x184)-n.f(dst+4)];assert all(math.isfinite(v) for v in xy);out['projection']=dict(world=world,jni=xy)
 frame(n,n.now+1,'preroll');r=frame(n,n.now+3001,'music anchor');assert r['E']==0
 frame(n,n.now+1500,'E1500 admission');out['beforeInput']=notes();obs.snapshot('before DOWN42')
 def action(down,pid):
  n.phase=('DOWN' if down else 'UP')+str(pid);n.call(0xbe31a8 if down else 0xdda71c,n.env,0,pid,987000+pid,fs=(*xy,.5 if down else 0));row=obs.snapshot(n.phase);row['mainNotes']=notes()
 action(True,42);action(True,43)
 if spec['scene']=='two-retained':
  arrays=InputArrays(n);n.phase='MOVE42 while both retained';arrays.move([(42,*xy,.5)],989500);obs.snapshot(n.phase);action(True,44);action(False,44)
 # All DOWNs above occur at one E without an intervening model FRAME.
 action(False,42);action(False,43);frame(n,n.now+1,'final cleanup E1501');out['final']=obs.snapshot('final cleanup');out['finalMain']=notes();obs.finish();out['status']='completed';out['abiServices']=dict(collections.Counter(a['service'] for a in abi))

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--archive',required=True);ap.add_argument('--budget',required=True);ap.add_argument('--output',required=True);a=ap.parse_args();assert __debug__
 dest=Path(a.output);assert not dest.exists() and not Path(a.budget).exists(),'refuse retry';config.configure(a.archive,'arc_tap')
 result=dict(assignment='W102-P03',sourceSha=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),driverSha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),librarySha256=config.EXPECTED_SHA256,scenes=[]);budget=dict(limit=4,reserved=0,scenes=[])
 with Path(a.budget).open('x') as f:json.dump(budget,f)
 for spec in json.loads((HERE/'fixtures.json').read_text()):
  assert budget['reserved']<4;budget['reserved']+=1;budget['scenes'].append(dict(scene=spec['scene'],status='reserved BEFORE setup'));Path(a.budget).write_text(json.dumps(budget,indent=2))
  out={};result['scenes'].append(out)
  try:scene(spec,out);budget['scenes'][-1]['status']='completed'
  except Exception as e:out.update(status='blocked',error=str(e),traceback=traceback.format_exc());budget['scenes'][-1]['status']='blocked'
  finally:result['budget']=budget;dest.write_text(json.dumps(result,indent=2)+'\n');Path(a.budget).write_text(json.dumps(budget,indent=2))
  if out['status']=='blocked':break
 print(json.dumps(budget));return 0 if all(s['status']=='completed' for s in result['scenes']) and len(result['scenes'])==4 else 1
if __name__=='__main__':sys.exit(main())
