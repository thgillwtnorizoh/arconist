#!/usr/bin/env python3
"""W102-P01: at most three fresh native scenes; refuses reuse of a budget/output."""
import argparse,collections,contextlib,hashlib,json,math,os,sys,traceback,subprocess
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
sys.path.insert(0,str(ROOT/'research_harness/src'))
from observe import Observer,FORBIDDEN
import config,arc_tap
from solo_entry import setup,entry
from lifecycle import activate,frame
from arc_tap_services import install
from jni_arrays import InputArrays

class Budget:
 def __init__(self,path):
  self.path=Path(path);self.path.parent.mkdir(parents=True,exist_ok=True);self.data={'assignment':'W102-P01','limit':3,'reservedScenes':0,'scenes':[]}
  with self.path.open('x') as f:json.dump(self.data,f,indent=2)
 def reserve(self,id):
  assert self.data['reservedScenes']<3,'three-scene budget exhausted'
  self.data['reservedScenes']+=1;self.data['scenes'].append({'id':id,'state':'reserved BEFORE native setup; no retries permitted'})
  self.flush()
 def done(self,state):self.data['scenes'][-1]['state']=state;self.flush()
 def flush(self):self.path.write_text(json.dumps(self.data,indent=2)+'\n')

def binding(name):
 p=HERE/'fixtures'/name;config._fixture_name=str(p.resolve())
 raw=p.read_bytes();return {'file':name,'sha256':hashlib.sha256(raw).hexdigest(),'rawAff':raw.decode(),'boundary':'unchanged external AFF resource-provider bytes only'}

def select_parent(n,obs):
 parents=[p for p in n.items(n.q(n.model+0x28),0x20) if n.typename(p)=='12LogicArcNote'];assert len(parents)==1,'expected native-created parent missing';obs.parent=parents[0];return parents[0]

def run_control(budget,out):
 out.update(id='scene1-E025',fixture=binding('single_control.aff'),status='running')
 original=arc_tap.setup;box={}
 def observed_setup(available):
  budget.reserve(out['id']);n=original(available);obs=Observer(n,out);box.update(n=n,obs=obs);return n
 arc_tap.setup=observed_setup
 try:
  out['historicalE025']=arc_tap.run()
  n,obs=box['n'],box['obs'];select_parent(n,obs);obs.snapshot('historical duplicate cleanup')
  frame(n,n.now+1,'P01 control next-frame cleanup');obs.snapshot('control next frame')
  obs.finish();out['status']='pass';budget.done('PASS; stopped before completion/results')
 finally:
  arc_tap.setup=original
  if box:out['lastNativePc']=hex(box['n'].u.reg_read(__import__('unicorn.arm64_const',fromlist=['UC_ARM64_REG_PC']).UC_ARM64_REG_PC))

def run_two(budget,out,ordinary):
 out.update(id='scene3-ordinary-two' if ordinary else 'scene2-trace-two',fixture=binding('ordinary_two.aff' if ordinary else 'trace_two.aff'),status='running')
 budget.reserve(out['id']);n=setup(True);abi=install(n);n.prepare_runtime();obs=Observer(n,out)
 # Observation is attached before actual ordinary owning entry. No native semantic function is host-invoked.
 n.call(0x1054f24);n.trace=[];n.visual=[];n.animationTrace=[];n.downstream=[];n.env=n.alloc(8);n.now=1000
 entry(n);activate(n);p=select_parent(n,obs);obs.ownership()
 children=n.items(p,0x120);assert len(children)==2 and len(set(children))==2,'native child multiplicity producer incomplete'
 assert [n.i(c+0x18) for c in children]==[1250,1500],'unexpected native child order/times'
 assert n.i(p+0xa4)==(0 if ordinary else 1),'native parent mode disagrees with supplied AFF'
 chart=n.q(n.model+0x28);actualN=n.i(chart+0xb8)
 out['prediction']={'conditionalW102N':5 if ordinary else 2,'nativeObservedN':actualN,'agrees':actualN==(5 if ordinary else 2),'neverWrittenByDriver':True}
 assert n.u.mem_read(chart+0x110,1)[0]==0,'unexpected input plane mode'
 camera=n.q(n.q(n.model+0x20)+0x2a8);out['projection']=[]
 def project(child,dx=0):
  world=[n.f(child+0x80)+int(n.f(n.q(p+0x20)+0x14)*850-425)+dx,n.f(child+0x84),0.0]
  src,dst=n.alloc(12),n.alloc(8)
  for i,v in enumerate(world):n.wf(src+4*i,v)
  n.call(0xbdbb70,camera,src,regs={8:dst});xy=[n.f(dst),n.f(n.director+0x184)-n.f(dst+4)]
  assert all(math.isfinite(x) for x in xy)
  out['projection'].append(dict(child=hex(child),worldPlane=world,childSamplerZ=n.f(child+0x88),jni=xy,displaced=dx!=0));return xy
 points=[project(c) for c in children];displaced=project(children[0],2000)
 arrays=InputArrays(n);out['jniArrayCalls']=arrays.calls
 def child_records():return [r for r in out['recorders'] if r['note'] in {hex(c) for c in children}]
 def event(label,fn):
  n.phase=label;fn();return obs.snapshot(label)
 def advance(e,label):
  old=obs.effective();assert old is not None and e>=old,'backward E schedule'
  def do():
   row=frame(n,n.now+e-old,label);assert row['E']==row['lastModelE']==e
  return event(label,do)
 def down(pid,xy,label):return event(label,lambda:n.call(0xbe31a8,n.env,0,pid,987000+pid,fs=(*xy,.5)))
 def up(pid,label):return event(label,lambda:n.call(0xdda71c,n.env,0,pid,988000+pid,fs=(*points[0],0)))
 frame(n,n.now+1,'P01 preroll');row=frame(n,n.now+3001,'P01 native music anchor');assert row['E']==0
 advance(1000,'admit parent and children')
 if ordinary:
  down(42,points[0],'body contact DOWN before child windows')
  advance(1001,'ordinary continuous body claim');advance(1125,'first body checkpoint')
 advance(1250,'first child frame')
 before=len(out['recorders']);down(43,displaced,'displaced DOWN negative');assert len(out['recorders'])==before,'displaced input recorded judgment';up(43,'displaced UP')
 down(44,points[0],'first child fresh DOWN');up(44,'first child UP');assert obs.byte(children[0]+0xd)==1,'first native child not consumed'
 before=len(out['recorders']);down(45,points[0],'first child fresh-ID duplicate');assert len(out['recorders'])==before,'duplicate recorded';
 if not ordinary:
  # Retain this duplicate DOWN for native JNI MOVE/frame negative through child2.
  retained=45
 else:up(45,'first duplicate UP');retained=42
 advance(1375,'retained frame; body checkpoint if ordinary')
 before=len(child_records());advance(1500,'second child time WITHOUT fresh DOWN')
 event('native MOVE at second child',lambda:arrays.move([(retained,*points[1],.5)],989500))
 advance(1500,'repeat FRAME after MOVE without fresh DOWN')
 assert len(child_records())==before and obs.byte(children[1]+0xd)==0,'MOVE/frame awarded child'
 if not ordinary:up(45,'retained duplicate UP')
 down(46,points[1],'second child fresh DOWN');up(46,'second child UP');assert obs.byte(children[1]+0xd)==1,'second native child not consumed'
 before=len(out['recorders']);down(47,points[1],'second child fresh-ID duplicate');assert len(out['recorders'])==before,'second duplicate recorded';up(47,'second duplicate UP')
 if ordinary:
  advance(1625,'last ordinary body checkpoint');up(42,'body owner UP');advance(1626,'ordinary next-frame cleanup')
 else:advance(1501,'trace next-frame cleanup')
 out['final']=obs.snapshot('stopped before results');obs.finish()
 out['abiServices']=dict(collections.Counter(x['service'] for x in abi));out['status']='pass';budget.done('PASS; stopped before completion/results')

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--archive',required=True);ap.add_argument('--output',required=True);ap.add_argument('--budget',required=True);a=ap.parse_args()
 assert __debug__,'Do not disable assertions';output=Path(a.output);assert not output.exists(),'refuse overwrite/reexecution';assert not Path(a.budget).exists(),'existing budget: no new native scenes authorized'
 config.configure(a.archive,'arc_tap');budget=Budget(a.budget);output.parent.mkdir(parents=True,exist_ok=True)
 result={'assignment':'W102-P01','status':'running','sourceBaseSha':'a9628c139e449dffd3e3a5fef3bb5b74414be9d3','executionCheckoutSha':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'nativeLibrarySha256':config.EXPECTED_SHA256,'scriptSha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [HERE/'run.py',HERE/'observe.py']},'sceneLimit':3,'scenes':[],'nativeFailures':[]}
 for id in range(3):
  scene={};result['scenes'].append(scene)
  try:
   if id==0:run_control(budget,scene)
   else:run_two(budget,scene,id==2)
  except Exception as e:
   scene['status']='blocked';scene['failure']={'type':type(e).__name__,'message':str(e),'traceback':traceback.format_exc()};result['nativeFailures'].append(scene['failure']);result['status']='blocked';budget.done('BLOCKED; no retry and later scenes NOT RUN');break
  finally:
   result['budget']=budget.data;output.write_text(json.dumps(result,indent=2)+'\n')
 if result['status']=='running':result['status']='pass' if all(s.get('prediction',{}).get('agrees',True) for s in result['scenes']) else 'discrepancy'
 result['notRunScenes']=3-len(result['scenes']);output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'status':result['status'],'reservedScenes':budget.data['reservedScenes'],'notRunScenes':result['notRunScenes'],'failures':result['nativeFailures']}));return 0 if result['status']=='pass' else 1
if __name__=='__main__':sys.exit(main())
