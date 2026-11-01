"""041: ordinary native-owned hold through renderer pause, resume and release."""
import collections
import hashlib
import math
import struct
import traceback
import config
from solo_entry import setup,entry
from lifecycle import activate,frame
from jni_arrays import InputArrays
from interruption_services import InterruptionServices
from boundaries import PC_SKIPS
from unicorn import UC_HOOK_CODE,UC_HOOK_MEM_WRITE
from unicorn.arm64_const import UC_ARM64_REG_PC,UC_ARM64_REG_SP

CASES=['hold_uninterrupted','hold_retained_pause_resume',
       'hold_up_during_pause_repress','hold_cancel_during_pause_repress']
OBSERVE={0xee197c,0xee29a8,0xee29e8,0xe4e4dc,0xe2ea48,0x1870de0,
 0x173b358,0x1862a14,0x18649b8,0x18649bc,0xd92558,0xd925fc,0x1576aa4,
 0xa5b8ac,0xf2914c,0xa56170,0x1793f8c,0x17371d8,0x13d3f44,0x9effe0,
 0x18be2f8,0x10a7550,0x1866038,0x14858d4,0x14557b4,0xf8056c,
 0xf80904,0x1730290,0x868e54,0xbe31a8,0xdda71c,0xd8dc50,0x1556de4,
 0x194ff80,0xeec024,0xf9a50c,0x13073c4,0xeec1cc,
 0xe0e5f4,0xd7654c,0xf46250,0xf4f2e0,0x170fafc,0x165211c,
 0x10f5288,0x1652168,0xbd4e60,0xb9e0d0,0x18d60cc,0x190cf7c,0xa48168,0xe31764,0x9e74f4,
 0x1091204,0x979fe0,0x1632d78,0x1632db0,0x17effac,0xf6c964,
 0x16c90bc,0x18c9ba4,0xfbf24c,0xffa914,0x1980970,0x159bdec,
 0x145502c,0xf1cc14,0x1631d78,0xc27d34,0x1600bb0}


def run_case(case,e):
    e.update(status='running',gates={'construction':'incomplete','hold_control':'not_run',
       'lifecycle':'not_run','contact_continuity':'not_run','checkpoints_cleanup':'not_run'})
    config.configure(config.archive_path,'gameplay_interruption')
    e['fixture']={'name':'native_hold.aff','sha256':hashlib.sha256(config.fixture_text().encode()).hexdigest()}
    n=setup(True);n.prepare_runtime();n.observe |= OBSERVE
    parsed=[];created=[];generated=[];activations=[];guards=[];resolutions=[];writes=[]
    entries=[];recorders=[];captures=[];notifications=[];states=[];counts=collections.Counter()
    objects={};records=[];custom_events={};pending={};return_hooks=set()
    e.update(parsed_holds=parsed,created_holds=created,generated_checkpoints=generated,
       activations=activations,resolved_guards=guards,resolutions=resolutions,native_writes=writes,
       function_entries=entries,recorders=recorders,resume_capture_producers=captures,
       custom_events=notifications,states=states,native_call_counts=counts)

    def effective():
        t=objects['timeline'];return n.i(t+0x20)-n.i(t+0x28)
    def score_state():
        s,g=objects['score'],objects['gauge']
        return {'N':n.i(s+0xc),'score':n.i(s+0x14),'combo':n.i(s+0x1c),
          'shining':n.i(s+0x20),'PURE':n.i(s+0x24),'FAR':n.i(s+0x28),
          'LOST':n.i(s+0x2c),'health':n.f(g+0x10)}
    def mapping():
        out=[]
        def walk(p):
            if not p:return
            walk(n.q(p));slot=n.i(p+0x28);touch=n.q(0x1beef90+slot*8)
            out.append({'android_id':n.q(p+0x20),'slot':slot,'touch_slot':n.i(touch+0xc),
                        'touch':hex(touch),'generated_id':n.i(touch+0x34),'timestamp':n.q(touch+0x40)})
            walk(n.q(p+8))
        walk(n.q(0x1bf1a90));return out
    def snapshot(label):
        t,h=objects['timeline'],objects['hold']
        row={'label':label,'phase':n.phase,'wall':n.now,'E':effective(),
          'timeline':{'R':n.i(t+0x20),'P':n.i(t+0x24),'C':n.i(t+0x28),
            'O':n.i(t+0x30),'A':n.i(t+0x34),'B':n.i(t+0x38),
            'origins':[n.q(t+0x10),n.q(t+0x18)],'paused':n.u.mem_read(t+0x2c,1)[0]},
          'pause':{'scene':n.u.mem_read(n.scene+0x4b0,1)[0],
            'model':n.u.mem_read(n.model+0x138,1)[0],
            'mode148':n.i(n.model+0x148),'finished':n.u.mem_read(n.model+0x139,1)[0],
            'director_stopped':n.u.mem_read(n.director+0x220,1)[0],
            'director_scheduler_pause':n.u.mem_read(n.director+0x130,1)[0]},
          'listener':n.state(n.model)['listener'],'dispatcher_enabled':n.u.mem_read(n.dispatcher+0x124,1)[0],
          'director_frame':n.i(n.director+0x134),'scene_stamp':n.i(n.scene+0x4d0),
          'latch':n.u.mem_read(h+0xa8,1)[0],'activity':list(n.u.mem_read(h+0x64,2)),
          'mapping':mapping(),'mask':n.i(0x1bfebd4),
          'slots':[hex(n.q(0x1beef90+8*i)) for i in range(2)],
          'retained':[hex(p) for p in n.items(n.model,0xd0)],
          'resolved':[n.u.mem_read(p+8,1)[0] for p in records],
          'score':score_state(),'calls':dict(counts),'result_cache':hex(n.q(objects['score']+0x68)),
          'pause_UI':{'active':n.u.mem_read(service.pause+0x2d8,1)[0],
                      'parent':hex(n.q(service.pause+0x148)),
                      'decoration':hex(n.q(service.pause+0x2e8))}}
        states.append(row);return row
    def written(u,access,address,size,value,ud):
        pc=hex(u.reg_read(UC_ARM64_REG_PC))
        for i,p in enumerate(records):
            if address==p+8:
                resolutions.append({'record':i,'time':n.i(p),'before':n.u.mem_read(address,1)[0],
                   'value':value,'size':size,'pc_elf_va':pc,'phase':n.phase,'E':effective()})
                return
        for kind,(base,extent) in e.get('_watch_objects',{}).items():
            if base<=address<base+extent:
                writes.append({'object':kind,'offset':hex(address-base),'size':size,
                  'before':int.from_bytes(u.mem_read(address,size),'little'),'value':value,
                  'pc_elf_va':pc,'phase':n.phase,'wall':n.now,'E_before':effective()});return
    def returned(u,pc,size,ud):
        if pending.get(pc):
            row=pending[pc].pop();row['after']=score_state()
    def observe(u,pc,size,ud):
        counts[hex(pc)]+=1
        if pc==0x18649b8:
            p=n.x(27);parsed.append({'pointer':hex(p),'type':n.typename(p),
               'start':n.i(p+0x18),'end':n.i(p+0x1c),'raw_lane':n.i(n.q(p+0x20)+8),
               'native_start':n.x(1),'native_end':n.x(2),'position':hex(n.x(3))})
        elif pc==0x18649bc:
            p=n.x(0);created.append({'pointer':hex(p),'type':n.typename(p),'vtable_elf_va':hex(n.q(p))})
        elif pc==0xd925fc:
            p=n.x(1);generated.append({'hold':hex(n.x(0)-0x78),'time':n.i(p),'weight':n.i(p+4),
                                      'resolved':n.u.mem_read(p+8,1)[0]})
        elif pc in [0xf2914c,0xa56170]:
            captures.append({'pc_elf_va':hex(pc),'destination':hex(n.x(0) if pc==0xf2914c else n.x(1)),
                             'vtable':hex(n.x(9)),'captured_pause_layer':hex(n.x(8))})
        if not objects:return
        if pc==0x14557b4:
            activations.append({'hold':hex(n.x(0)),'touch':hex(n.x(1)),
                'generated_id':n.i(n.x(1)+0x34),'E':n.x(2),'phase':n.phase})
        elif pc==0xf80904:
            guards.append({'record':records.index(n.x(14)-8),'resolved':n.x(15)&255,
                           'E':effective(),'phase':n.phase})
        elif pc==0x13073c4:
            sp=u.reg_read(UC_ARM64_REG_SP)
            e.setdefault('unprojections',[]).append([n.f(sp+0x28+4*i) for i in range(3)])
        elif pc==0xeec1cc:e.setdefault('lane_returns',[]).append([n.x(0)&0xffffffff,n.x(0)>>32])
        elif pc in [0x1730290,0x868e54] and n.x(1)==objects['hold']:
            row={'kind':'accepted' if pc==0x1730290 else 'miss','pc_elf_va':hex(pc),
              'lr_elf_va':hex(n.x(30)),'hold':hex(n.x(1)),'native_time':n.x(4),
              'E':effective(),'phase':n.phase,'before':score_state()}
            recorders.append(row);lr=n.x(30);pending.setdefault(lr,[]).append(row)
            if lr not in return_hooks:
                u.hook_add(UC_HOOK_CODE,returned,begin=lr,end=lr);return_hooks.add(lr)
        if pc in {0xe0e5f4,0xf46250,0xf4f2e0,0x170fafc,0x165211c,0x10f5288,0x1652168,
            0xbd4e60,0xb9e0d0,0x18d60cc,0x190cf7c,0xa48168,0xe31764,0x9e74f4,0x1091204,0x979fe0,
            0x1632d78,0x1632db0,0x17effac,0x18c9ba4,0xfbf24c,0xf9a50c,0x1556de4}:
            entries.append({'pc_elf_va':hex(pc),'lr_elf_va':hex(n.x(30)),
                'x':[hex(n.x(i)) for i in range(4)],'E':effective(),'wall':n.now,'phase':n.phase})
        elif pc==0xffa914:
            name=n.string(n.x(1)).decode();custom_events[n.x(0)]=name
        elif pc==0x1980970 and n.x(1) in custom_events and n.i(n.x(1)+0xc)==6:
            notifications.append({'event':custom_events[n.x(1)],'dispatcher':hex(n.x(0)),
                'phase':n.phase,'wall':n.now,'pc_elf_va':hex(pc),'native_event_type':6})
    for pc in OBSERVE:n.u.hook_add(UC_HOOK_CODE,observe,begin=pc,end=pc)
    n.call(0x1930604);n.call(0x1054f24)
    n.trace=[];n.visual=[];n.animationTrace=[];n.downstream=[];n.env=n.alloc(8);n.now=1000
    entry(n);activate(n)
    chart,t,score=n.q(n.model+0x28),n.q(n.model+0x30),n.q(n.model+0x38)
    holds=[p for p in n.items(chart,0x20) if n.typename(p)=='13LogicHoldNote'];assert len(holds)==1
    h=holds[0];objects.update(scene=n.scene,model=n.model,chart=chart,timeline=t,score=score,
                             gauge=n.items(score,0xa0)[0],hold=h)
    records.extend(range(n.q(h+0x78),n.q(h+0x80),12))
    assert len(parsed)==len(created)==1 and created[0]['pointer']==hex(h)
    assert parsed[0]['raw_lane']==3 and n.i(n.q(h+0x20)+0x10)==4
    assert n.i(h+0x18)==1000 and n.i(h+0x1c)==2000 and n.f(h+0x70)==250
    assert [(n.i(p),n.i(p+4),n.u.mem_read(p+8,1)[0]) for p in records]==[(1250,1,0),(1500,1,0),(1750,1,0)]
    assert [(r['time'],r['weight'],r['resolved']) for r in generated]==[(1250,1,0),(1500,1,0),(1750,1,0)]
    assert n.i(chart+0xb8)==n.i(score+0xc)==3 and n.i(chart+0xbc)==2500
    maps=n.maps(n.model);keys=[[k for k,ps in g.items() if h in ps] for g in maps];assert any(keys)
    assert n.sceneInitReturn==1 and n.q(n.scene+0x3e0)==n.model and n.q(n.scene+0x3e8)==chart
    assert n.q(n.director+0x140)==n.scene and n.q(n.director+0x148)==0
    service=InterruptionServices(n,e.setdefault('platform_ui_audio',{}))
    arrays=InputArrays(n)
    assert any(r['destination']==hex(service.callback) and r['captured_pause_layer']==hex(service.pause)
               and r['vtable']=='0x1b7d700' for r in captures)
    e.update(objects={k:hex(p) for k,p in objects.items()},chart={'N':n.i(chart+0xb8),
        'end':n.i(chart+0xbc),'group':n.i(h+0x50),'input_enabled':n.u.mem_read(h+0x54,1)[0],
        'hold_index_keys':keys,'md5':n.string(chart+0xf8).decode()},
        checkpoints=[{'pointer':hex(p),'time':n.i(p),'weight':n.i(p+4)} for p in records])
    watch={'hold':(h,0xb0),'scene':(n.scene,0x4e0),'model':(n.model,0x160),
           'timeline':(t,0x40),'director':(n.director,0x230),'pause_layer':(service.pause,0x300)}
    e['_watch_objects']=watch
    for kind,lo,hi in [('hold',0x64,0x65),('hold',0xa8,0xa8),('scene',0x4b0,0x4b0),
       ('model',0x138,0x139),('model',0x148,0x14b),('timeline',0x20,0x3b),
       ('director',0x130,0x130),('director',0x220,0x220),('pause_layer',0x2d8,0x2d8)]:
        base=watch[kind][0];n.u.hook_add(UC_HOOK_MEM_WRITE,written,begin=base+lo,end=base+hi)
    for p in records:n.u.hook_add(UC_HOOK_MEM_WRITE,written,begin=p+8,end=p+8)
    e['gates']['construction']='pass';e['gates']['hold_control']='incomplete'
    snapshot('activation')
    def advance(E,label=None):
        r=frame(n,n.now+E-effective(),label or '041 frame E'+str(E))
        assert r['E']==r['lastModelE']==E
        assert sum(v['pc']=='0x10a7550' for v in r['lifecycle'])==1
        return snapshot(label or 'frame_'+str(E))
    frame(n,n.now+1,'041 preroll');anchor=frame(n,n.now+3001,'041 native music anchor');assert anchor['E']==0
    advance(1000)
    point,out=n.alloc(12),n.alloc(8);world=[212.5,0.,0.]
    for i,v in enumerate(world):n.wf(point+4*i,v)
    camera=n.q(n.q(n.model+0x20)+0x2a8);n.call(0xbdbb70,camera,point,regs={8:out})
    xy=[n.f(out),n.f(n.director+0x184)-n.f(out+4)];assert all(math.isfinite(v) for v in xy)
    e['projection']={'camera':hex(camera),'world':world,'jni_xy':xy}
    def event(kind,pid,label):
        n.phase=label
        if kind=='cancel':
            args=[arrays.array([v],fmt) for v,fmt in zip([pid,*xy,0.],'ifff')]
            n.call(0xd8dc50,n.env,0,*args,988000+pid)
        else:n.call(0xbe31a8 if kind=='down' else 0xdda71c,n.env,0,pid,
                    (987000 if kind=='down' else 988000)+pid,fs=(*xy,.5 if kind=='down' else 0))
        return snapshot(label)
    first=event('down',42,'first_DOWN42');assert first['latch']==1 and first['activity']==[0,0]
    first_touch=first['retained'][0]
    assert first['mapping'][0]['android_id']==42 and first['mapping'][0]['touch']==first_touch
    assert advance(1001)['activity']==[1,1]
    advance(1125);pre=advance(1200);e['gates']['hold_control']='pass'
    replacement=False
    if case!='hold_uninterrupted':
        e['gates']['lifecycle']='incomplete'
        n.phase='renderer_background';n.call(0xe0e5f4,n.env,0);bg=snapshot('background')
        assert bg['pause']['scene']==bg['pause']['model']==bg['timeline']['paused']==bg['pause']['director_stopped']==1
        assert bg['E']==1200 and bg['retained']==[first_touch] and bg['score']==pre['score']
        if case in ['hold_up_during_pause_repress','hold_cancel_during_pause_repress']:
            kind='up' if case=='hold_up_during_pause_repress' else 'cancel'
            terminal=event(kind,42,'paused_'+kind.upper()+'42')
            assert not terminal['mapping'] and not terminal['retained'] and terminal['mask']==0
            assert terminal['score']==bg['score'] and terminal['latch']==1
            replacement=True
        before=snapshot('before_stopped_frame');n.now+=60000;n.phase='stopped_renderer_frame'
        n.call(0x17371d8,n.director);stopped=snapshot('stopped_frame')
        assert all(stopped['calls'].get(pc,0)==before['calls'].get(pc,0) for pc in ['0x1793f8c','0x13d3f44','0x10a7550','0x16c90bc'])
        assert stopped['timeline']==before['timeline'] and stopped['E']==1200
        n.phase='renderer_foreground';n.call(0xf4f2e0,n.env,0);fg=snapshot('foreground_before_frame')
        assert fg['pause']['director_stopped']==0 and fg['pause']['scene']==fg['pause']['model']==fg['timeline']['paused']==1
        paused=advance(1200,'foreground_paused_frame')
        assert paused['timeline']['C']-pre['timeline']['C']==60000 and paused['activity']==[0,0]
        assert paused['latch']==1 and paused['score']==pre['score'] and paused['resolved']==pre['resolved']
        assert paused['retained']==([] if replacement else [first_touch])
        n.phase='explicit_native_resume';service.resume();resumed=snapshot('after_explicit_resume')
        assert resumed['pause']['scene']==resumed['pause']['model']==resumed['timeline']['paused']==0
        assert resumed['E']==1200 and resumed['timeline']['C']==paused['timeline']['C']
        assert resumed['retained']==paused['retained'] and resumed['score']==pre['score']
        e['gates']['lifecycle']='pass'
    else:e['gates']['lifecycle']='not_applicable_control'
    e['gates']['contact_continuity']='incomplete'
    post=advance(1201)
    assert post['activity']==([0,0] if replacement else [1,1]) and post['latch']==1
    advance(1300)
    if replacement:
        second=event('down',43,'replacement_DOWN43')
        assert len(second['retained'])==1 and second['retained'][0]!=first_touch
        assert second['mapping'][0]['generated_id']!=first['mapping'][0]['generated_id']
        assert second['activity']==[0,0] and second['latch']==1
        active_touch=second['retained'][0]
    else:active_touch=first_touch
    assert advance(1301)['activity']==[1,1]
    assert any(a['touch']==active_touch and a['E']==1301 for a in activations)
    e['gates']['contact_continuity']='pass';e['gates']['checkpoints_cleanup']='incomplete'
    for E in [1375,1625,1626]:advance(E)
    before_up=score_state();event('up',43 if replacement else 42,'terminal_UP')
    final=advance(1627);e['final']=final
    assert final['activity']==[0,0] and final['latch']==1 and final['score']==before_up
    assert not final['mapping'] and not final['retained'] and final['mask']==0 and final['slots']==['0x0','0x0']
    assert len(resolutions)==3 and sorted(r['record'] for r in resolutions)==[0,1,2]
    assert all(r['before']==0 and r['value']==r['size']==1 and r['pc_elf_va']=='0xf80924' for r in resolutions)
    assert len(recorders)==3 and all(r['kind']=='accepted' and r['lr_elf_va']=='0xf809a8' for r in recorders)
    assert [r['E'] for r in recorders]==[1125,1375,1625]
    assert not any(r['phase'] in ['renderer_background','stopped_renderer_frame','foreground_paused_frame',
         'explicit_native_resume','paused_UP42','paused_CANCEL42'] for r in recorders)
    assert final['score']=={'N':3,'score':10000003,'combo':3,'shining':3,'PURE':3,'FAR':0,'LOST':0,'health':80.5999984741211}
    assert all(r['pause']['mode148']==0 and r['listener']['registered']==r['listener']['enabled']==1
         and r['listener']['paused']==0 and r['dispatcher_enabled']==1 for r in states)
    assert not any(w['object']=='model' and w['offset']=='0x148' for w in writes)
    if case!='hold_uninterrupted':
        assert [r['event'] for r in notifications if 'event_come_to_' in r['event']]==['event_come_to_background','event_come_to_foreground']
        assert any(r['pc_elf_va']=='0x165211c' and r['x'][0]==hex(n.scene) for r in entries)
        calls=e['platform_ui_audio']['provider_calls']
        assert any(w['object']=='pause_layer' and w['pc_elf_va']=='0x18d60fc' and w['before']==1 and w['value']==0 for w in writes)
        assert n.hooks.get(0xb9e0d0) is None and counts['0xb9e0d0']==counts['0x18d60cc']==1
        assert [(r['virtual'],r['x1']) for r in calls if r['virtual'] in ['0x30','0x40']]==[('0x30',1),('0x40',1200),('0x30',0)]
    forbidden={0xb9e0d0,0x18d60cc,0x165211c,0x10f5288,0xe31764,0x9e74f4,0x1866038,0x14557b4,
               0xf8056c,0xf80924,0x1730290,0x868e54,0xeec024,0xf9a50c,0x10a7550}
    assert not forbidden.intersection(n.host_calls) and not forbidden.intersection(n.hooks)
    e['gates']['checkpoints_cleanup']='pass';e['jni_array_services']=arrays.calls
    e['touch_events']=[r for r in n.touchEvents if r['wall']>=first['wall']]
    assert [r['action'] for r in e['touch_events']]==([0,3,0,2] if case=='hold_cancel_during_pause_repress' else [0,2,0,2] if replacement else [0,2])
    e['status']='pass';e.pop('_watch_objects')
    e['not_run']=['AppActivity_nativePause_nativeResume_ready_paths','arc_optional','results_sqlite','Android_VM_GLThread','physical_audio_output']


def run():
    result={'status':'fail','cases':{},'fresh_emulator_per_case':True,'native_failures':[],
        'pc_skips_elf_va':PC_SKIPS,'new_gameplay_pc_skips':[],
        'external_schedule':'Explicit renderer lifecycle/Widget enum/clock/JNI contacts; no automatic Android CANCEL',
        'scientific_boundary':'Existing ordinary catalog/account/settings/ABI/resources/graphics/clock services;012-style delegate/audio facades; original hide-menu processing retained. Actual scene/PauseLayer/capture/delegate remain native-owned.'}
    for case in CASES:
        e={};result['cases'][case]=e
        try:run_case(case,e)
        except Exception as exc:
            f={'case':case,'type':type(exc).__name__,'message':str(exc),'traceback':traceback.format_exc()}
            e.update(status='fail',failure=f);e.pop('_watch_objects',None);result['native_failures'].append(f)
            if case=='hold_uninterrupted':
                for later in CASES[1:]:result['cases'][later]={'status':'not_run','reason':'Control failed'}
                return result
    if result['native_failures']:return result
    control=result['cases'][CASES[0]]
    result['comparison']={}
    for case,e in result['cases'].items():
        if e['final']['score']!=control['final']['score'] or e['chart']!=control['chart']:
            result['native_failures'].append({'case':case,'type':'NativeComparisonMismatch','message':'Observed chart or output differs; full cases preserved'})
            return result
        result['comparison'][case]={'score':e['final']['score'],'final_C':e['final']['timeline']['C'],
           'final_E':e['final']['E'],'same_record_times':[r['E'] for r in e['recorders']]==[1125,1375,1625]}
    result['status']='pass';return result
