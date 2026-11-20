#!/usr/bin/env python3
"""C01 one scene only. Native research differences are observations, not aborts."""
import argparse,collections,hashlib,json,math,sys,traceback,subprocess,zipfile
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
OLD=HERE.parent/'w102-p01'
sys.path[:0]=[str(OLD),str(ROOT/'research_harness/src')]
from observe import Observer
import config
from solo_entry import setup,entry
from lifecycle import activate,frame
from arc_tap_services import install
from jni_arrays import InputArrays
from unicorn import UC_HOOK_CODE

def binding(name):
 p=OLD/'fixtures'/name;raw=p.read_bytes()
 assert hashlib.sha256(raw).hexdigest()=='cbf47e5c83e070533bee8bc1b1e31b59209e452d43b612832f3cd02fad2cb0e1','fixture identity'
 config._fixture_name=str(p.resolve())
 return dict(path=str(p.relative_to(ROOT)),sha256=hashlib.sha256(raw).hexdigest(),rawAff=raw.decode())
def select_parent(n,obs):
 parents=[p for p in n.items(n.q(n.model+0x28),0x20) if n.typename(p)=='12LogicArcNote'];assert len(parents)==1,'native-owned parent missing';obs.parent=parents[0];return parents[0]
def watch_normalization(n,out):
 out['normalization']=[]
 def capture(u,pc,size,data):
  p=n.x(19)
  out['normalization'].append(dict(pc=hex(pc),parent=hex(p),storedMode=n.i(p+0xa4),sourceW24=n.x(24)&0xffffffff,storeW8=n.x(8)&0xffffffff))
 for pc in [0xc66654,0xc66658]:n.u.hook_add(UC_HOOK_CODE,capture,begin=pc,end=pc)
class Budget:
 def __init__(self,path):
  self.path=Path(path);self.data=dict(assignment='W102-P01-C01',limit=1,reservedScenes=0)
  with self.path.open('x') as f:json.dump(self.data,f)
 def reserve(self,id):
  assert self.data['reservedScenes']==0,'scene budget exceeded'
  self.data.update(reservedScenes=1,id=id,state='reserved before setup');self.path.write_text(json.dumps(self.data,indent=2))
 def done(self,state):self.data['state']=state;self.path.write_text(json.dumps(self.data,indent=2))
def run_scene(budget,out):
 ordinary=False # choose bounded child-only schedule, irrespective of prepared mode
 out.update(id='C01-false-two',fixture=binding('ordinary_two.aff'),status='running')
 budget.reserve(out['id']);n=setup(True);abi=install(n);n.prepare_runtime();obs=Observer(n,out); watch_normalization(n,out)
 # Observation is attached before actual ordinary owning entry. No native semantic function is host-invoked.
 n.call(0x1054f24);n.trace=[];n.visual=[];n.animationTrace=[];n.downstream=[];n.env=n.alloc(8);n.now=1000
 entry(n);activate(n);p=select_parent(n,obs);obs.ownership()
 children=n.items(p,0x120);assert len(children)==2 and len(set(children))==2,'native child multiplicity producer incomplete'
 out['observedChildOrder']=[n.i(c+0x18) for c in children]
 out['beforeInput']=dict(parsed=out['parsed'],prepared=out['nativeObjects'])
 chart=n.q(n.model+0x28);actualN=n.i(chart+0xb8)
 out['prediction']={'historicalRefutedN':5,'priorObservedN':2,'nativeObservedN':actualN,'agrees':actualN==2,'neverWrittenByDriver':True}
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
 before=len(out['recorders']);down(43,displaced,'displaced DOWN negative');up(43,'displaced UP')
 down(44,points[0],'first child fresh DOWN');up(44,'first child UP')
 before=len(out['recorders']);down(45,points[0],'first child fresh-ID duplicate');
 if not ordinary:
  # Retain this duplicate DOWN for native JNI MOVE/frame negative through child2.
  retained=45
 else:up(45,'first duplicate UP');retained=42
 advance(1375,'retained frame; body checkpoint if ordinary')
 before=len(child_records());advance(1500,'second child time WITHOUT fresh DOWN')
 event('native MOVE at second child',lambda:arrays.move([(retained,*points[1],.5)],989500))
 advance(1500,'repeat FRAME after MOVE without fresh DOWN')
 out['moveObservation']=dict(childRecorderCount=len(child_records()),before=before,secondConsumed=obs.byte(children[1]+0xd))
 if not ordinary:up(45,'retained duplicate UP')
 down(46,points[1],'second child fresh DOWN');up(46,'second child UP')
 before=len(out['recorders']);down(47,points[1],'second child fresh-ID duplicate');up(47,'second duplicate UP')
 if ordinary:
  advance(1625,'last ordinary body checkpoint');up(42,'body owner UP');advance(1626,'ordinary next-frame cleanup')
 else:advance(1501,'trace next-frame cleanup')
 out['final']=obs.snapshot('stopped before results');obs.ownership();out['callCounts']=dict(obs.counts);out['directHostCalls']=[hex(x) for x in n.host_calls];out['semanticReplacementHooks']=[]
 assert obs.score()['result']=='0x0' and obs.counts['0xc27d34']==0 and obs.counts['0x1600bb0']==0,'results boundary crossed'
 out['abiServices']=dict(collections.Counter(x['service'] for x in abi));out['status']='pass';budget.done('PASS; stopped before completion/results')

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--archive',required=True);ap.add_argument('--budget',required=True);ap.add_argument('--output',required=True);a=ap.parse_args()
 assert __debug__;dest=Path(a.output);assert not dest.exists() and not Path(a.budget).exists(),'refuse repeat/overwrite'
 raw=zipfile.ZipFile(a.archive).read('lib/arm64-v8a/libcocos2dcpp.so');assert hashlib.sha256(raw).hexdigest()==config.EXPECTED_SHA256
 config.configure(a.archive,'arc_tap');budget=Budget(a.budget)
 out=dict(assignment='W102-P01-C01',executionSha=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),driverSha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),librarySha256=hashlib.sha256(raw).hexdigest())
 try:run_scene(budget,out)
 except Exception as e:out.update(status='blocked',failure=dict(type=type(e).__name__,message=str(e),traceback=traceback.format_exc()));budget.done('BLOCKED no retry')
 finally:out['budget']=budget.data;dest.write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps(dict(status=out['status'],budget=budget.data)));return 0 if out['status']=='pass' else 1
if __name__=='__main__':sys.exit(main())
