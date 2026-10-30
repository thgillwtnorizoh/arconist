"""040: native-owned Settings production, offset selection and judgment clock."""
import collections
import hashlib
import math
import traceback
import config
import solo_entry
from settings_backend_services import OffsetNative, signed32
from lifecycle import activate, frame
from boundaries import PC_SKIPS
from unicorn import UC_HOOK_CODE, UC_HOOK_MEM_READ, UC_HOOK_MEM_WRITE
from unicorn.arm64_const import UC_ARM64_REG_PC, UC_ARM64_REG_SP

CASES = [
    ('A_baseline',0,{'audio_preset':0,'offset_int_2':0,'bt_offset':80},0),
    ('B_regular',0,{'audio_preset':0,'offset_int_2':80,'bt_offset':200},80),
    ('C_alternate',0,{'audio_preset':1,'offset_int_2':0,'bt_offset':80},80),
    ('D_combined',120,{'audio_preset':0,'offset_int_2':80,'bt_offset':200},200),
    ('legacy_optional',0,{'audio_preset':0,'offset_int':100,'bt_offset':200},80),
]
OBSERVE = {0xee197c,0xee2214,0xee29a8,0xee29e8,0xe4e4dc,0xe2ea48,
    0x1870de0,0x173b358,0x1862a14,0x18640d8,0x18640dc,0x1576aa4,
    0x1576b98,0xfbfd04,0xfbfed0,0xfbfef8,0xfbff4c,0xfbff54,0xfbff78,
    0x8db04c,0x1271200,0x16c90bc,0x16c9170,0x16c9194,0x16c9198,0x16c91e0,
    0x1735d7c,0x1793f8c,0x18be2f8,0x10a7550,0x10fd1c0,0xf8056c,
    0xbe31a8,0xdda71c,0x194ff80,0xeec024,0xeec080,0x13073c4,0xeec1cc,
    0xeec4e0,0xeec4f0,0xf6b514,0x160ce28,0x160cec0,0x160ce74,
    0x965e28,0x1730290,0x868e54,0xc27d34,0x1600bb0}


def run_case(name, aff_offset, values, expected_offset, e):
    e.update(status='running',gates={'settings_producer':'incomplete',
        'native_scene_offset':'not_run','music_anchor':'not_run',
        'effective_time_judgment':'not_run','cleanup':'not_run'}, settings_producer={})
    config.configure(config.archive_path,'offset_aff120' if aff_offset else 'settings_offset_clock')
    text=config.fixture_text()
    e['fixture']={'name':config._fixture_name,'sha256':hashlib.sha256(text.encode()).hexdigest(),
                  'external_AudioOffset':aff_offset}
    previous=solo_entry.SoloNative
    try:
        solo_entry.SoloNative=lambda:OffsetNative(values,e['settings_producer'])
        n=solo_entry.setup(True)
    finally:
        solo_entry.SoloNative=previous
    e['gates']['settings_producer']='pass'
    n.prepare_runtime();n.observe |= OBSERVE
    objects={};counts=collections.Counter();writes=[];settings_reads=[];consumers=[]
    timeline_calls=[];startup_predicates=[];music=[];states=[];candidates=[]
    classifiers=[];recorders=[];inputs=[];steady_samples=[];returns={};installed=set()
    e.update(native_writes=writes,settings_reads=settings_reads,offset_consumers=consumers,
        native_call_counts=counts,timeline_updates=timeline_calls,startup_predicates=startup_predicates,
        music_start_requests=music,states=states,candidates=candidates,classifiers=classifiers,
        recorders=recorders,input_entries=inputs,steady_clock_samples=steady_samples)
    settings_values=[n.i(n.settings+4*i) for i in range(3)]

    def timeline():
        t=objects.get('timeline')
        if not t:return None
        R,C,A=n.i(t+0x20),n.i(t+0x28),n.i(t+0x34)
        steady=n.u.mem_read(t+0x2d,1)[0]
        E=signed32(R-C) if steady else signed32(A-C-(3000 if A<=0 else 0))
        return {'pointer':hex(t),'steady_origin':n.q(t+0x10),'system_origin':n.q(t+0x18),
            'R':R,'C':C,'O':n.i(t+0x30),'A':A,'B':n.i(t+0x38),'E':E,
            'paused':n.u.mem_read(t+0x2c,1)[0],'steady_mode':steady,
            'music_started':n.u.mem_read(t+0x2e,1)[0]}
    def score_state():
        if 'score' not in objects:return None
        s,g=objects['score'],objects['gauge']
        return {'N':n.i(s+0xc),'score':n.i(s+0x14),'combo':n.i(s+0x1c),
            'PURE':n.i(s+0x24),'FAR':n.i(s+0x28),'LOST':n.i(s+0x2c),
            'shining':n.i(s+0x20),'health':n.f(g+0x10)}
    def mapping():
        rows=[]
        def walk(p):
            if not p:return
            walk(n.q(p));slot=n.i(p+0x28);touch=n.q(0x1beef90+slot*8)
            rows.append({'android_id':n.q(p+0x20),'slot':slot,'touch':hex(touch),
                'touch_slot':n.i(touch+0xc),'generated_id':n.i(touch+0x34),
                'stored_event_timestamp':n.q(touch+0x40)})
            walk(n.q(p+8))
        walk(n.q(0x1bf1a90));return rows
    def state(label):
        p=objects['tap'];t=timeline()
        row={'label':label,'phase':n.phase,'wall':n.now,
            'delta_since_music_request':n.now-music[0]['wall'] if music else None,
            'timeline':t,'last_model_E':n.i(0x1bf93e8),'director_frame':n.i(n.director+0x134),
            'scene_stamp':n.i(n.scene+0x4d0),'score':score_state(),
            'note':{'pointer':hex(p),'time':n.i(p+0x18),'lane':n.i(n.q(p+0x20)+0x10),
                    'active':p in n.items(n.model,0xa0),'input_enabled':n.u.mem_read(p+0x54,1)[0],
                    'missed':n.u.mem_read(p+0xc,1)[0],'consumed':n.u.mem_read(p+0xd,1)[0],
                    'accepted_id':n.i(p+0x10)},
            'mapping':mapping(),'retained':[hex(p) for p in n.items(n.model,0xd0)],
            'slots':[hex(n.q(0x1beef90+8*i)) for i in range(2)],'mask':n.i(0x1bfebd4),
            'finished':n.u.mem_read(n.model+0x139,1)[0],
            'result_cache':hex(n.q(objects['score']+0x68))}
        assert n.q(n.app+0x70)==n.settings
        assert [n.i(n.settings+4*i) for i in range(3)]==settings_values
        states.append(row);return row
    def written(u,access,address,size,value,ud):
        kind,base=next(((k,p) for k,p in objects.items() if k in
            ['chart','model','timeline','tap','score','gauge'] and p<=address<p+
            {'chart':0xc8,'model':0x38,'timeline':0x40,'tap':0x80,'score':0x30,'gauge':0x14}[k]),('unknown',address))
        writes.append({'object':kind,'pointer':hex(base),'offset':hex(address-base),
            'pc_elf_va':hex(u.reg_read(UC_ARM64_REG_PC)),'phase':n.phase,'wall':n.now,
            'size':size,'before':int.from_bytes(u.mem_read(address,size),'little'),'value':value})
    def settings_read(u,access,address,size,value,ud):
        settings_reads.append({'pc_elf_va':hex(u.reg_read(UC_ARM64_REG_PC)),
            'address':hex(address),'offset':hex(address-n.settings),'size':size,
            'value':int.from_bytes(u.mem_read(address,size),'little'),'phase':n.phase})
    n.u.hook_add(UC_HOOK_MEM_READ,settings_read,begin=n.settings,end=n.settings+0xb)
    def returned(u,pc,size,ud):
        if returns.get(pc):
            r=returns[pc].pop();r['returned']=signed32(n.x(0))
            if r['kind']=='steady_ms':r['returned_ms']=signed32(n.x(0))
            if r['kind']=='timeline_update':r['after']=timeline()
            if r['kind']=='recorder':r['after']=score_state()
    def on_return(r):
        pc=n.x(30);returns.setdefault(pc,[]).append(r)
        if pc not in installed:
            n.u.hook_add(UC_HOOK_CODE,returned,begin=pc,end=pc);installed.add(pc)
    def observe(u,pc,size,ud):
        counts[hex(pc)]+=1
        if pc==0x173b358:
            objects['chart']=n.x(0)
            u.hook_add(UC_HOOK_MEM_WRITE,written,begin=n.x(0)+0xc4,end=n.x(0)+0xc7)
        elif pc==0xfbfd04:
            objects['model']=n.x(0)
            e['native_model_initializer']={'pointer':hex(n.x(0)),'lr_elf_va':hex(n.x(30))}
            u.hook_add(UC_HOOK_MEM_WRITE,written,begin=n.x(0)+0x30,end=n.x(0)+0x37)
        elif pc==0xfbfed0:
            consumers.append({'stage':'settings_owner_read','pc_elf_va':hex(pc),
                'app':hex(n.q(n.x(23))),'settings':hex(n.q(n.q(n.x(23))+0x70)),
                'chart':hex(n.q(n.x(19)+0x28))})
        elif pc==0xfbfef8:
            consumers.append({'stage':'selected_offset_address','address':hex(n.x(8)),
                'preset_operand':signed32(n.x(10)),'chart_offset_operand':signed32(n.x(20))})
        elif pc==0xfbff4c:
            objects['timeline']=n.x(25)
            n.protected_results.append((n.x(25)+0x10,n.x(25)+0x3c))
            u.hook_add(UC_HOOK_MEM_WRITE,written,begin=n.x(25)+0x10,end=n.x(25)+0x3b)
            consumers.append({'stage':'native_addition','chart_operand':signed32(n.x(20)),
                'user_operand':signed32(n.x(24)),'timeline':hex(n.x(25))})
        elif pc==0x18640d8:
            p=n.x(27);objects['tap']=n.x(0)
            e['tap_builder']={'pointer':hex(n.x(0)),'parsed':hex(p),'parsed_type':n.typename(p),
                'time':n.i(p+0x18),'raw_lane':n.i(n.q(p+0x20)+8),'initializer_elf_va':hex(n.x(8))}
        elif pc==0x18640dc:
            e['tap_builder'].update(initializer_return=n.x(0),runtime_type=n.typename(n.x(25)),
                returned_note=hex(n.x(25)),vtable_elf_va=hex(n.q(n.x(25))))
        elif pc==0x1576b98 and n.x(19)==objects.get('tap'):
            e['tap_index_producer']={'lo':signed32(n.x(23)),'hi':signed32(n.x(24))}
        elif pc==0x1271200:
            r={'kind':'steady_ms','phase':n.phase,'wall':n.now,'supplied_ns':n.now*1000000,
               'lr_elf_va':hex(n.x(30))};steady_samples.append(r);on_return(r)
        elif pc==0x8db04c:
            e.setdefault('model_starts',[]).append({'model':hex(n.x(0)),
                'steady_epoch':n.x(1),'system_epoch':n.x(2),'lr_elf_va':hex(n.x(30)),'wall':n.now})
        elif pc==0x16c90bc:
            r={'kind':'timeline_update','phase':n.phase,'wall':n.now,
                'lr_elf_va':hex(n.x(30)),'pointer':hex(n.x(0)),'before':timeline()}
            timeline_calls.append(r);on_return(r)
        elif pc==0x16c9170:
            startup_predicates.append({'phase':n.phase,'wall':n.now,
                'E_operand':signed32(n.x(9)),'negative_O_operand':signed32(n.x(10)),
                'paused_operand':n.x(8)&255})
        elif pc==0x16c9194:
            music.append({'wall':n.now,'phase':n.phase,'manager':hex(n.x(0)),
                'callsite_elf_va':hex(pc),'target_elf_va':'0x1735d7c',
                'return_elf_va':'0x16c9198','request_entry_timeline':timeline()})
        elif pc==0x1735d7c:
            music[-1]['lr_elf_va']=hex(n.x(30))
            music[-1]['external_audio_boundary']='Existing service; argument observed at original BL before the service executes'
        elif pc in [0x16c9198,0x16c91e0]:
            music[-1]['after_request_before_compensation' if pc==0x16c9198 else 'after_native_compensation']=timeline()
        elif pc in [0xbe31a8,0xdda71c,0x194ff80,0xeec024,0xeec080]:
            inputs.append({'pc_elf_va':hex(pc),'phase':n.phase,'wall':n.now,'timeline':timeline()})
        elif pc==0x13073c4:
            sp=u.reg_read(UC_ARM64_REG_SP)
            e.setdefault('unprojection',[]).append([n.f(sp+0x28+4*i) for i in range(3)])
        elif pc==0xeec1cc:
            e.setdefault('lanes',[]).append([n.x(0)&0xffffffff,n.x(0)>>32])
        elif pc in [0xeec4e0,0xeec4f0]:
            candidates.append({'stage':'before_sort' if pc==0xeec4e0 else 'after_sort',
                'E':timeline()['E'],'notes':[hex(p) for p in n.items(n.x(19),0xb8)]})
        elif pc==0x160ce28:
            classifiers.append({'note':hex(n.x(1)),'generated_id':n.x(2),'timeline':timeline()})
        elif pc==0x160cec0:
            classifiers[-1].update(abs_error=signed32(n.x(9)),native_E=signed32(n.x(4)))
        elif pc==0x160ce74:classifiers[-1]['consumes']=n.x(23)&1
        elif pc in [0x1730290,0x868e54] and n.x(1)==objects.get('tap'):
            r={'kind':'recorder','operation':'accepted' if pc==0x1730290 else 'miss',
               'pc_elf_va':hex(pc),'lr_elf_va':hex(n.x(30)),'note':hex(n.x(1)),
               'judgment_id':n.x(2),'generated_id':n.x(5),'E':timeline()['E'],'before':score_state()}
            recorders.append(r);on_return(r)
    for pc in OBSERVE:n.u.hook_add(UC_HOOK_CODE,observe,begin=pc,end=pc)
    n.call(0x1930604);n.call(0x1054f24)
    n.trace=[];n.visual=[];n.animationTrace=[];n.downstream=[]
    n.env=n.alloc(8);n.now=1000
    solo_entry.entry(n);activate(n)
    model=n.model;chart=n.q(model+0x28);t=n.q(model+0x30);s=n.q(model+0x38)
    objects.update(score=s,gauge=n.items(s,0xa0)[0])
    taps=[p for p in n.items(chart,0x20) if n.typename(p)=='12LogicTapNote']
    assert taps==[objects['tap']] and chart==objects['chart'] and t==objects['timeline']
    p=taps[0];lane=n.i(n.q(p+0x20)+0x10)
    assert n.sceneInitReturn==1 and n.q(n.director+0x140)==n.scene and n.q(n.director+0x148)==0
    assert n.q(n.scene+0x3e0)==model and n.q(n.scene+0x3e8)==chart
    assert e['tap_builder']['raw_lane']==3 and lane==4 and n.i(p+0x18)==1500
    assert n.i(chart+0xc4)==aff_offset and n.i(t+0x30)==expected_offset
    assert n.i(chart+0xb8)==n.i(s+0xc)==1 and n.i(chart+0xbc)==1620
    listener=n.state(model)['listener'];assert listener['registered']==listener['enabled']==1 and listener['paused']==0
    maps=n.maps(model);index=[[k for k,ps in g.items() if p in ps] for g in maps]
    assert any(index)
    e.update(objects={**{k:hex(v) for k,v in objects.items()},'scene':hex(n.scene)},application=hex(n.app),settings=hex(n.settings),
        chart={'AudioOffset':n.i(chart+0xc4),'N':n.i(chart+0xb8),'end':n.i(chart+0xbc),
               'md5':n.string(chart+0xf8).decode(),'tap_index':index},listener=listener)
    e['gates']['native_scene_offset']='pass'
    for base,lo,hi in [(p,0xc,0x13),(s,0x14,0x2f),(objects['gauge'],0x10,0x13)]:
        n.u.hook_add(UC_HOOK_MEM_WRITE,written,begin=base+lo,end=base+hi)
    state('activation')
    frame(n,n.now+1,'040 original preroll');state('preroll')
    boundary=timeline()['steady_origin']+3000-timeline()['O']
    assert boundary>=n.now
    frame(n,boundary,'040 strict music-start equality');equal=state('music_boundary_equal')
    assert equal['timeline']['E']==-expected_offset and not music and equal['timeline']['music_started']==0
    frame(n,boundary+1,'040 native music-start crossing');anchor=state('music_anchor')
    assert len(music)==1 and anchor['timeline']['E']==-expected_offset
    assert music[0]['after_native_compensation']['E']==-expected_offset
    assert music[0]['request_entry_timeline']['E']==1-expected_offset
    assert music[0]['lr_elf_va']=='0x16c9198'
    assert music[0]['manager']==hex(n.q(n.app+0x10)) and n.q(n.app+0x10)!=0
    assert anchor['timeline']['music_started']==anchor['timeline']['steady_mode']==1
    e['gates']['music_anchor']='pass'
    # Measurement Δ is external bookkeeping relative to the observed request.
    start_wall=music[0]['wall']
    frame(n,start_wall+1500,'040 equal music-relative elapsed sample');sample=state('equal_delta1500')
    e['equal_elapsed_sample']=sample
    assert sample['timeline']['E']==1500-expected_offset and sample['note']['active']
    assert sample['score']['PURE']==sample['score']['FAR']==sample['score']['LOST']==0
    if sample['timeline']['E']!=1500:
        frame(n,n.now+1500-sample['timeline']['E'],'040 native aligned judgment frame')
    aligned=state('aligned_before_DOWN');e['aligned_sample']=aligned
    assert aligned['timeline']['E']==1500 and aligned['delta_since_music_request']==1500+expected_offset
    assert aligned['note']['active'] and not aligned['note']['consumed'] and not aligned['note']['missed']
    camera=n.q(n.q(model+0x20)+0x2a8)
    world=[425.0*(lane-3.5),0.,0.];point,out=n.alloc(12),n.alloc(8)
    for i,v in enumerate(world):n.wf(point+4*i,v)
    n.call(0xbdbb70,camera,point,regs={8:out})
    xy=[n.f(out),n.f(n.director+0x184)-n.f(out+4)]
    assert all(math.isfinite(v) for v in xy)
    e['projection']={'camera':hex(camera),'world_input_target':world,'jni_xy':xy,
        'director_dimensions':[n.f(n.director+0x180),n.f(n.director+0x184)]}
    model_count=counts['0x10a7550']
    n.phase='040 JNI DOWN42 aligned E1500'
    n.call(0xbe31a8,n.env,0,42,987042,fs=(*xy,.5));down=state('after_DOWN')
    assert counts['0x10a7550']==model_count and down['timeline']['E']==1500
    assert len(down['mapping'])==len(down['retained'])==1 and down['mask'].bit_count()==1
    m=down['mapping'][0];assert m['android_id']==42 and m['touch_slot']==m['slot'] and down['retained']==[m['touch']]
    n.phase='040 JNI UP42 aligned E1500'
    n.call(0xdda71c,n.env,0,42,988042,fs=(*xy,0));up=state('after_UP')
    assert not up['mapping'] and not up['retained'] and up['mask']==0 and up['slots']==['0x0','0x0']
    assert up['score']==down['score'] and up['note']==down['note']
    frame(n,n.now+1,'040 native post-UP duplicate control');final=state('final')
    e['final']=final
    assert final['timeline']['O']==expected_offset and final['score']==up['score']
    assert len(classifiers)==len(recorders)==1
    assert classifiers[0]['note']==hex(p) and classifiers[0]['abs_error']==0 and classifiers[0]['consumes']==1
    assert all(r['notes']==[hex(p)] and r['E']==1500 for r in candidates) and len(candidates)==2
    assert recorders[0]['operation']=='accepted' and recorders[0]['lr_elf_va']=='0x160cf48'
    assert recorders[0]['generated_id']==m['generated_id']==final['note']['accepted_id']
    assert final['note']['consumed']==1 and final['note']['missed']==0
    assert final['score']=={'N':1,'score':10000001,'combo':1,'PURE':1,'FAR':0,'LOST':0,
                           'shining':1,'health':80.19999694824219}
    assert e['lanes']==[[4,0]] and all(abs(a-b)<.5 for a,b in zip(e['unprojection'][0],world))
    assert consumers[0]['app']==hex(n.app) and consumers[0]['settings']==hex(n.settings)
    assert consumers[0]['chart']==hex(chart)
    assert any(r['pc_elf_va']=='0xfbfef8' and r['offset']==('0x4' if values['audio_preset']==0 else '0x8') for r in settings_reads)
    if name=='legacy_optional':
        assert any(r['key']=='offset_int_2' and not r['present'] and r['returned']==-2147483648 for r in e['settings_producer']['getters'])
        assert any(w['offset']=='0x4' and w['pc_elf_va']=='0x1a02c64' and w['value']==80 for w in e['settings_producer']['writes'])
    else:
        assert not any(r['key']=='offset_int' for r in e['settings_producer']['getters'])
    for off,pc in [('0x0','0x1a02b88'),('0x4','0x1a02c30'),('0x8','0x1a02c94')]:
        assert any(w['offset']==off and w['pc_elf_va']==pc for w in e['settings_producer']['writes'])
    assert any(w['object']=='timeline' and w['offset']=='0x30' and w['pc_elf_va']=='0xfbff54' and w['value']==expected_offset for w in writes)
    assert any(w['object']=='timeline' and w['offset']=='0x28' and w['pc_elf_va']=='0x16c91d8' for w in writes)
    assert any(w['object']=='chart' and w['offset']=='0xc4' and w['value']==aff_offset for w in writes)
    assert all(a not in n.host_calls and a not in n.hooks for a in [0x1a02b48,0xfbfd04,
        0x16c90bc,0x8db04c,0xeec024,0x160ce28,0x1730290,0x868e54])
    assert 0x1735d7c not in n.host_calls and n.hooks[0x1735d7c] == n.service
    e['audio_start_boundary']='Existing inert audio-manager entry1735d7c; native timeline BL/latch/compensation execute, manager body/provider/output not run'
    e['gates']['effective_time_judgment']=e['gates']['cleanup']='pass'
    e.update(status='pass',not_run=['full_later_application_startup','fixed_elapsed_input_optional',
        'completion_results_sqlite','physical_audio_output','automatic_bluetooth_routing'],
        validation='Native producer/caller/owner/consumer, strict anchor and original JNI evidence; host arithmetic is an assertion/schedule oracle only.')


def run():
    result={'status':'fail','cases':{},'fresh_emulator_per_case':True,'native_failures':[],
        'pc_skips_elf_va':PC_SKIPS,'new_gameplay_pc_skips':[],
        'new_service':'040 isolated typed persistence getters at the existing external backend; existing resource services available earlier for native application prefix',
        'application_boundary':'Original owner executes from1a146a0 through complete loader return1a14770; later unrelated app initialization is not run. Original-produced app/Settings persist into ordinary GameScene.',
        'supplied_services':'Existing ordinary catalog/account/profile/platform/clock/JNI/ABI/resources/audio/graphics/allocator/autorelease; controlled persisted dictionary and synthetic AFF. No actual preference file format or device audio timing.'}
    for name,aff,values,O in CASES:
        e={};result['cases'][name]=e
        try:run_case(name,aff,values,O,e)
        except Exception as exc:
            failure={'case':name,'type':type(exc).__name__,'message':str(exc),
                'location':traceback.extract_tb(exc.__traceback__)[-1].name if exc.__traceback__ else None,
                'traceback':traceback.format_exc()}
            e.update(status='fail',failure=failure);result['native_failures'].append(failure)
            if name=='A_baseline' or e['gates']['settings_producer']!='pass':
                for later,*_ in CASES[CASES.index((name,aff,values,O))+1:]:
                    result['cases'][later]={'status':'not_run','reason':'Required producer/control gate failed'}
                return result
    if result['native_failures']:return result
    result['comparison']={name:{'loaded_settings':e['settings_producer']['loaded_fields'],
        'O':e['aligned_sample']['timeline']['O'],'music_start_wall':e['music_start_requests'][0]['wall'],
        'anchor_E':e['music_start_requests'][0]['after_native_compensation']['E'],
        'E_at_delta1500':e['equal_elapsed_sample']['timeline']['E'],
        'delta_at_E1500':e['aligned_sample']['delta_since_music_request'],
        'JNI_xy':e['projection']['jni_xy'],'score':e['final']['score']}
        for name,e in result['cases'].items()}
    result['status']='pass';return result
