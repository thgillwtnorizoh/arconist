"""Read-only native observers. No emulator writes or substituted semantic calls."""
import collections,struct
from unicorn import UC_HOOK_CODE,UC_HOOK_MEM_WRITE
from unicorn.arm64_const import UC_ARM64_REG_PC,UC_ARM64_REG_SP

PCS={0xee197c,0xe4e4dc,0xe2ea48,0x173b358,0x1862a14,0x173a778,0x178f7fc,0x1925084,0x11ea120,0x173bf2c,0x1864e18,0x1864e1c,0x1865468,0x1576aa4,0xeec4e0,0xeec4f0,0xeec480,0x160ce28,0x160cec0,0xeec56c,0x180cf28,0x13b73ac,0x1730290,0x868e54,0x10a7550,0x14858d4,0x15dfe2c,0xc78814,0xc27d34,0x1600bb0,0xbe31a8,0xdda71c,0x1706960,0xf9a50c}
FORBIDDEN={0xe4e4dc,0xe2ea48,0x173b358,0x1862a14,0x173a778,0x178f7fc,0x1925084,0x11ea120,0x10a7550,0x160ce28,0xc78814,0x1730290,0x868e54}

class Observer:
 def __init__(self,n,out):
  self.n=n;self.out=out;self.children=[];self.parent=None;self.pending={};self.return_hooks=set();self.classifiers=[];self.counts=collections.Counter()
  for key in ['parsed','factories','writes','countProducer','candidates','classifiers','spatial','guardReads','recorders','bodyAcceptances','events']:out[key]=[]
  for pc in PCS:n.u.hook_add(UC_HOOK_CODE,self.code,begin=pc,end=pc)
 def byte(self,p):return self.n.u.mem_read(p,1)[0]
 def effective(self):
  n=self.n
  if not getattr(n,'model',0):return None
  t=n.q(n.model+0x30);return n.i(t+0x20)-n.i(t+0x28)
 def score(self):
  n=self.n
  if not getattr(n,'model',0):return None
  s=n.q(n.model+0x38);gs=n.items(s,0xa0)
  if not gs:return None
  g=gs[0]
  return dict(N=n.i(s+0xc),score=n.i(s+0x14),combo=n.i(s+0x1c),shining=n.i(s+0x20),PURE=n.i(s+0x24),FAR=n.i(s+0x28),LOST=n.i(s+0x2c),health=n.f(g+0x10),healthBits=struct.unpack('<I',n.u.mem_read(g+0x10,4))[0],result=hex(n.q(s+0x68)))
 def record_state(self,p):
  n=self.n
  return [dict(pointer=hex(r),time=n.i(r),weight=n.i(r+4),resolved=self.byte(r+8)) for r in range(n.q(p+0x78),n.q(p+0x80),12)]
 def child(self,p):
  n=self.n
  return dict(pointer=hex(p),type=n.typename(p),time=n.i(p+0x18),end=n.i(p+0x1c),parent=hex(n.q(p+0x90)),group=n.i(p+0x50),input=self.byte(p+0x54),geometry=[n.f(p+0x80+i*4) for i in range(3)],missed=self.byte(p+0xc),consumed=self.byte(p+0xd),contact=n.i(p+0x10))
 def snapshot(self,label):
  n=self.n;p=self.parent;model=n.model;s=n.q(model+0x38)
  row=dict(label=label,wall=n.now,E=self.effective(),lastModelE=n.i(29332456),score=self.score(),contacts=[dict(pointer=hex(t),generatedId=n.i(t+0x34),slot=n.i(t+0xc),xy=[n.f(t+0x1c),n.f(t+0x20)]) for t in n.items(model,0xd0)],mask=n.i(0x1bfebd4),androidMapSize=n.q(0x1bf1a98),active=[hex(x) for x in n.items(model,0xa0)],children=[self.child(c) for c in n.items(p,0x120)],parent=dict(pointer=hex(p),mode=n.i(p+0xa4),activity=list(n.u.mem_read(p+0x64,2)),cache=self.byte(p+0xd0),records=self.record_state(p),color=hex(n.q(p+0xb0)),owner=n.i(n.q(p+0xb0)+0x28)),finishedResult=hex(n.q(s+0x68)))
  self.out['events'].append(row);return row
 def written(self,u,access,address,size,value,data):
  p,kind=data
  self.out['writes'].append(dict(phase=self.n.phase,pc=hex(u.reg_read(UC_ARM64_REG_PC)),object=hex(p),kind=kind,offset=hex(address-p),size=size,value=value))
 def returned(self,u,pc,size,data):
  queue=self.pending.get(pc)
  if queue:
   row=queue.pop();row['after']=self.score();row['returnValue']=self.n.x(0)&0xffffffff
 def code(self,u,pc,size,data):
  n=self.n;o=self.out;self.counts[hex(pc)]+=1
  if pc==0x1864e18:
   a=n.x(27);b,e=n.q(a+0x70),n.q(a+0x78);o['parsed'].append(dict(mode=n.i(a+0x68),start=n.i(a+0x18),end=n.i(a+0x1c),times=[n.i(p) for p in range(b,e,4)],childArgument=n.x(0)&0xffffffff))
  elif pc==0x1864e1c:
   p=n.x(0);self.children.append(p);o['factories'].append(dict(pointer=hex(p),type=n.typename(p),vtable=hex(n.q(p)),time=n.i(p+0x18)))
   for lo,hi,kind in [(0xc,0xd,'guard'),(0x80,0x97,'geometry/backlink')]:u.hook_add(UC_HOOK_MEM_WRITE,self.written,(p,kind),begin=p+lo,end=p+hi)
  elif pc==0x11ea120:o['countProducer'].append(dict(chart=hex(n.x(0)),lower=n.x(1)&0xffffffff,upper=n.x(2)&0xffffffff,caller=hex(n.x(30))))
  elif pc==0x173bf2c:o['countProducer'][-1]['N']=n.x(0)&0xffffffff
  elif pc in [0xeec4e0,0xeec4f0]:
   m=n.x(19);o['candidates'].append(dict(phase=n.phase,E=self.effective(),stage='beforeSort' if pc==0xeec4e0 else 'afterSort',items=[dict(pointer=hex(p),time=n.i(p+0x18),missed=self.byte(p+0xc),consumed=self.byte(p+0xd)) for p in n.items(m,0xb8)]))
  elif pc==0x160ce28:
   row=dict(phase=n.phase,E=self.effective(),child=hex(n.x(1)),generatedId=n.x(2)&0xffffffff,missed=self.byte(n.x(1)+0xc),consumed=self.byte(n.x(1)+0xd));o['classifiers'].append(row);self.classifiers.append(row)
  elif pc==0x160cec0 and self.classifiers:self.classifiers[-1]['nativeAbsoluteError']=n.x(9)&0xffffffff
  elif pc==0xeec56c and self.classifiers:self.classifiers.pop()['consumesInput']=n.x(0)&1
  elif pc==0xeec480:
   sp=u.reg_read(UC_ARM64_REG_SP);o['spatial'].append(dict(phase=n.phase,E=self.effective(),child=hex(n.x(28)),accepted=n.x(0)&1,target=[n.f(sp+0x38),n.f(sp+0x3c)],point=[n.f(sp+0x40+i*4) for i in range(3)]))
  elif pc in [0x180cf28,0x13b73ac] and n.x(0) in self.children:o['guardReads'].append(dict(phase=n.phase,pc=hex(pc),child=hex(n.x(0)),value=self.byte(n.x(0)+(0xd if pc==0x180cf28 else 0xc))))
  elif pc in [0x1730290,0x868e54]:
   lr=n.x(30);row=dict(phase=n.phase,E=self.effective(),recorder=hex(pc),caller=hex(lr),note=hex(n.x(1)),judgmentId=(n.x(2)&0xffffffff) if pc==0x1730290 else 'LOST',before=self.score());o['recorders'].append(row);self.pending.setdefault(lr,[]).append(row)
   if lr not in self.return_hooks:u.hook_add(UC_HOOK_CODE,self.returned,begin=lr,end=lr);self.return_hooks.add(lr)
  elif pc==0x15dfe2c:o['bodyAcceptances'].append(dict(phase=n.phase,E=self.effective(),parent=hex(n.x(0)),touch=hex(n.x(1)),generatedId=n.i(n.x(1)+0x34)))
 def ownership(self):
  n=self.n;p=self.parent;model=n.model;chart=n.q(model+0x28);children=n.items(p,0x120)
  assert set(children)==set(self.children) and len(children)==len(self.children),'factory/parent identity mismatch'
  assert all(n.q(c+0x90)==p for c in children),'native backlink missing'
  assert all(any(w['object']==hex(c) and w['offset']=='0x90' and w['pc']=='0x1865514' for w in self.out['writes']) for c in children),'original backlink writer missing'
  assert all(any(w['object']==hex(c) and w['pc']=='0x1925888' for w in self.out['writes']) for c in children),'original child geometry writer missing'
  assert n.q(n.scene+0x3e0)==model and n.q(n.scene+0x3e8)==chart
  assert n.sceneInitReturn==1 and n.q(n.director+0x140)==n.scene
  listener=n.state(model)['listener'];assert listener['registered']==listener['enabled']==1 and listener['paused']==0
  assert any(p in members for group in n.maps(model) for members in group.values()),'parent original index missing'
  assert all(all(__import__('math').isfinite(v) for v in self.child(c)['geometry']) for c in children),'nonfinite native child geometry'
  assert not FORBIDDEN.intersection(n.host_calls),'direct semantic call'
  assert not FORBIDDEN.intersection(n.hooks),'semantic replacement hook'
  self.out['nativeObjects']=dict(scene=hex(n.scene),model=hex(model),chart=hex(chart),parent=hex(p),parentType=n.typename(p),parentMode=n.i(p+0xa4),children=[self.child(c) for c in children],N=n.i(chart+0xb8),end=n.i(chart+0xbc),mainContainsParent=p in n.items(chart,0x20),mainContainsChildren=[c in n.items(chart,0x20) for c in children],index=[{str(k):[hex(x) for x in v] for k,v in group.items() if p in v or any(c in v for c in children)} for group in n.maps(model)],listener=n.state(model)['listener'],records=self.record_state(p))
 def finish(self):
  self.ownership();n=self.n;assert not n.items(n.model,0xd0) and n.i(0x1bfebd4)==0 and n.q(0x1bf1a98)==0,'contact cleanup incomplete'
  assert self.score()['result']=='0x0' and self.counts['0xc27d34']==0 and self.counts['0x1600bb0']==0,'results boundary crossed'
  assert all('after' in r for r in self.out['recorders']),'incomplete recorder return'
  self.out['callCounts']=dict(self.counts);self.out['directHostCalls']=[hex(x) for x in n.host_calls];self.out['semanticReplacementHooks']=[]
