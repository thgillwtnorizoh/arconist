"""039: original AFF scene controls, scalar producers and paired JNI lane probes."""
import collections
import hashlib
import math
import struct
import traceback
import config
from unicorn import UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm64_const import UC_ARM64_REG_PC, UC_ARM64_REG_SP
from solo_entry import setup, entry
from lifecycle import activate, frame
from boundaries import PC_SKIPS

OBSERVE = {
    0xee197c,0xee29a8,0xee29e8,0xe4e4dc,0xe2ea48,0x1870de0,0x7f2628,
    0x1090060,0x173b358,0x1862a14,0x1864128,0x1864134,0x1864138,
    0x18645f4,0x18648f8,0x18649fc,0x1792e18,0x18641b4,
    0x18640d8,0x18640dc,0x11ea120,0x173bf2c,0x1576aa4,0x1576b98,
    0xfbfd04,0x10fd1c0,0x1793f8c,0x18be2f8,0x10a7550,0x10a763c,0x10a76f8,
    0xf8056c,0xf8071c,0xf8078c,0xf807fc,0xf80824,0xf80828,0x1514c64,0xd59c24,
    0xbe31a8,0xdda71c,0x194ff80,0xf9a50c,0xeec024,0xeec080,
    0x130733c,0x13073c4,0x13073f8,0xeec1cc,0xeec4e0,0xeec4f0,0xf6b514,
    0x160ce28,0x160ce58,0x160ce6c,0x160ce74,0x160cec0,0x965e28,
    0x1730290,0x868e54,0xc27d34,0x1600bb0,
}
PROBES = [('secondary',40.0,42),('outer',950.0,43)]


def run_case(case,evidence):
    evidence.update(status='running',gates={'construction':'incomplete',
        'dispatch_interpolation':'not_run','jni_geometry_judgment':'not_run','cleanup':'not_run'})
    config.configure(config.archive_path,{'control':'lane_widening',
        'camera':'widen_camera','lanes':'widen_lanes'}[case])
    evidence['fixture']={'name':config._fixture_name,
        'sha256':hashlib.sha256(config.fixture_text().encode()).hexdigest()}
    n=setup(True);n.prepare_runtime();n.observe |= OBSERVE
    counts=collections.Counter();chart_ptr=None;model_ptr=None;target={}
    parsed=[];classifications=[];builder=[];control_products=[];tap_products=[]
    writes=[];index=[];dispatch=[];setters=[];interpolation=[];states=[]
    candidates=[];classifiers=[];recorders=[];input_calls=[];frame_calls=[]
    return_records={};return_hooks=set();pending_classifier=[];pending_builder=None
    evidence.update(parsed_controls=parsed,classifications=classifications,builder=builder,
        runtime_control_products=control_products,tap_products=tap_products,
        native_writes=writes,index_producer=index,dispatch=dispatch,setters=setters,
        interpolation=interpolation,states=states,candidates=candidates,classifiers=classifiers,
        recorders=recorders,input_calls=input_calls,frame_calls=frame_calls,native_call_counts=counts)

    def signed32(v):return struct.unpack('<i',struct.pack('<I',v&0xffffffff))[0]
    def effective():
        t=n.q(n.model+0x30);return n.i(t+0x20)-n.i(t+0x28)
    def widening():
        p=model_ptr
        return {'G':n.f(p+0x60),'W':n.f(p+0x74),'previous_G':n.f(p+0x64),
            'camera_transition':{'start':n.i(p+0x54),'direction':n.i(p+0x58),'duration':n.f(p+0x5c)},
            'lane_transition':{'start':n.i(p+0x68),'direction':n.i(p+0x6c),'duration':n.f(p+0x70)}}
    def score_state():
        p,g=target['score'],target['gauge']
        return {'N':n.i(p+0xc),'score':n.i(p+0x14),'combo':n.i(p+0x1c),
            'PURE':n.i(p+0x24),'FAR':n.i(p+0x28),'LOST':n.i(p+0x2c),
            'shining':n.i(p+0x20),'health':n.f(g+0x10)}
    def note_state():
        active=n.items(n.model,0xa0)
        return {str(lane):{'pointer':hex(p),'time':n.i(p+0x18),'end':n.i(p+0x1c),
            'position':hex(n.q(p+0x20)),'lane':lane,'group':n.i(p+0x50),
            'input_enabled':n.u.mem_read(p+0x54,1)[0],
            'missed':n.u.mem_read(p+0xc,1)[0],'consumed':n.u.mem_read(p+0xd,1)[0],
            'accepted_id':n.i(p+0x10),'active':p in active} for lane,p in target['notes'].items()}
    def control_state():
        return [{'pointer':hex(p),'time':n.i(p+0x18),'end':n.i(p+0x1c),
            'group':n.i(p+0x50),'kind':n.i(p+0x64),'float':n.f(p+0x68),'integer':n.i(p+0x6c),
            'flags_0c_0d':list(n.u.mem_read(p+0xc,2)),
            'active':p in n.items(n.model,0xa0)} for p in target['controls']]
    def mapping():
        rows=[]
        def walk(p):
            if not p:return
            walk(n.q(p));slot=n.i(p+0x28);touch=n.q(0x1beef90+slot*8)
            rows.append({'android_id':struct.unpack('<q',n.u.mem_read(p+0x20,8))[0],
                'slot':slot,'touch_slot':n.i(touch+0xc),'touch':hex(touch),
                'generated_id':n.i(touch+0x34)})
            walk(n.q(p+8))
        walk(n.q(0x1bf1a90));return rows
    def state(label):
        row={'label':label,'phase':n.phase,'wall':n.now,'E':effective(),
            'last_model_E':n.i(29332456),'director_frame':n.i(n.director+0x134),
            'scene_stamp':n.i(n.scene+0x4d0),'widening':widening(),'notes':note_state(),
            'controls':control_state(),'score':score_state(),'mapping':mapping(),
            'retained':[hex(p) for p in n.items(n.model,0xd0)],'mask':n.i(0x1bfebd4),
            'finished':n.u.mem_read(n.model+0x139,1)[0],
            'result_cache':hex(n.q(target['score']+0x68))}
        states.append(row);return row
    def written(u,access,where,size,value,unused):
        obj=None;kind=None
        if chart_ptr and where==chart_ptr+0x110:obj=chart_ptr;kind='chart'
        elif model_ptr and model_ptr+0x54<=where<model_ptr+0x78:obj=model_ptr;kind='model_widening'
        else:
            for row in control_products:
                p=int(row['pointer'],16)
                if p<=where<p+0x70:obj=p;kind='control';break
            for row in tap_products:
                p=int(row['pointer'],16)
                if p<=where<p+0x80:obj=p;kind='tap';break
        writes.append({'pc_elf_va':hex(u.reg_read(UC_ARM64_REG_PC)),'phase':n.phase,
            'object':kind or 'score_or_health','pointer':hex(obj) if obj else None,
            'offset':hex(where-obj) if obj else None,'address':hex(where),'size':size,
            'before':int.from_bytes(u.mem_read(where,size),'little'),'value':value})
    def returned(u,pc,size,unused):
        if return_records.get(pc):
            row=return_records[pc].pop()
            if row['category']=='classification':row['return_kind']=n.x(0)&0xffffffff
            else:row.update(after=score_state(),return_observed=True)
    def on_return(row,lr):
        return_records.setdefault(lr,[]).append(row)
        if lr not in return_hooks:
            n.u.hook_add(UC_HOOK_CODE,returned,begin=lr,end=lr);return_hooks.add(lr)

    def observe(u,pc,size,unused):
        nonlocal chart_ptr,model_ptr,pending_builder
        counts[hex(pc)]+=1
        if pc==0x173b358:
            chart_ptr=n.x(0)
            u.hook_add(UC_HOOK_MEM_WRITE,written,begin=chart_ptr+0x110,end=chart_ptr+0x110)
        elif pc==0xfbfd04:
            model_ptr=n.x(0)
            evidence['native_model_initializer']={'pointer':hex(model_ptr),'lr_elf_va':hex(n.x(30))}
            u.hook_add(UC_HOOK_MEM_WRITE,written,begin=model_ptr+0x54,end=model_ptr+0x77)
        elif pc==0x1090060:
            row={'category':'classification','identifier':n.string(n.x(0)).decode(),
                 'lr_elf_va':hex(n.x(30)),'phase':n.phase}
            classifications.append(row);on_return(row,n.x(30))
        elif pc==0x1864128:
            p=n.x(0);parsed.append({'pointer':hex(p),'type':n.typename(p),
                'time':n.i(p+0x18),'identifier':n.string(p+0x20).decode(),
                'float':n.f(p+0x38),'integer':n.i(p+0x3c)})
        elif pc==0x1864134:
            pending_builder={'parsed':hex(n.x(27)),'chart_property_110':n.x(8)&255,'comparisons':[]}
            builder.append(pending_builder)
        elif pc in {0x18645f4,0x18648f8,0x18649fc}:
            pending_builder['comparisons'].append({'pc_elf_va':hex(pc),'kind':n.x(0)&0xffffffff,
                'against':{0x18645f4:4,0x18648f8:5,0x18649fc:6}[pc]})
        elif pc==0x1864138:pending_builder['admitted_at_elf_va']=hex(pc)
        elif pc==0x1792e18:
            p=n.x(0);row={'pointer':hex(p),'time_argument':n.x(1),'kind_argument':n.x(2),
                'float_argument':n.s(0),'integer_argument':n.x(3),'lr_elf_va':hex(n.x(30))}
            control_products.append(row)
            for lo,hi in [(p+0xc,p+0x1f),(p+0x50,p+0x55),(p+0x64,p+0x6f)]:
                u.hook_add(UC_HOOK_MEM_WRITE,written,begin=lo,end=hi)
        elif pc==0x18641b4:
            p=n.x(22);control_products[-1].update(initializer_return=n.x(0),
                runtime_type=n.typename(p),vtable_elf_va=hex(n.q(p)))
        elif pc==0x18640d8:
            p=n.x(27);tap_products.append({'pointer':hex(n.x(0)),'parsed':hex(p),
                'parsed_type':n.typename(p),'time':n.i(p+0x18),'raw_lane':n.i(n.q(p+0x20)+8),
                'position':hex(n.x(2)),'initializer_elf_va':hex(n.x(8))})
        elif pc==0x18640dc:
            p=n.x(25);tap_products[-1].update(initializer_return=n.x(0),returned_note=hex(p),
                runtime_type=n.typename(p),vtable_elf_va=hex(n.q(p)))
        elif pc==0x11ea120:
            evidence['count_producer']={'chart':hex(n.x(0)),'lo':n.x(1),'hi':n.x(2),
                'lr_elf_va':hex(n.x(30)),'main_before_bars':len(n.items(n.x(0),0x20))}
        elif pc==0x173bf2c:evidence['count_producer']['return_N']=n.x(0)&0xffffffff
        elif pc==0x1576b98:
            known={int(r['pointer'],16) for r in tap_products+control_products}
            if n.x(19) in known:index.append({'object':hex(n.x(19)),
                'type':n.typename(n.x(19)),'lo':n.x(23)&0xffffffff,'hi':n.x(24)&0xffffffff})
        if not target:return
        if pc==0x10a7550:frame_calls.append({'pc_elf_va':hex(pc),'phase':n.phase,'wall':n.now})
        elif pc in {0x10a763c,0x10a76f8}:
            interpolation.append({'pc_elf_va':hex(pc),'field':'G' if pc==0x10a763c else 'W',
                'model':hex(n.x(19)),'native_E':n.i(0x1bf93e8),'value_s0':n.s(0),
                'phase':n.phase,'transition':widening()})
        elif pc in {0xf8071c,0xf8078c,0xf807fc} and n.x(26) in target['controls']:
            evidence.setdefault('event_time_predicates',[]).append({'pc_elf_va':hex(pc),'event':hex(n.x(26)),
                'E_operand':signed32(n.x(1)),'end_operand':signed32(n.x(10)),
                'phase':n.phase,'processed_flags':list(n.u.mem_read(n.x(26)+0xc,2))})
        elif pc in {0xf80824,0x1514c64}:
            dispatch.append({'pc_elf_va':hex(pc),'event':hex(n.x(1)),
                'owner':hex(n.x(0)),'lr_elf_va':hex(n.x(30)),
                'E':effective(),'phase':n.phase,'widening_before':widening()})
        elif pc==0xf80828:
            dispatch.append({'pc_elf_va':hex(pc),'E':effective(),'phase':n.phase,
                             'widening_after':widening(),'control_after':control_state()})
        elif pc==0xd59c24:
            setters.append({'pc_elf_va':hex(pc),'model':hex(n.x(0)),'time_argument':n.x(1),
                'direction_argument':n.x(2),'duration_s0':n.s(0),'lr_elf_va':hex(n.x(30)),
                'E':effective(),'phase':n.phase})
        elif pc in {0xbe31a8,0xdda71c,0x194ff80,0xeec024,0xeec080}:
            input_calls.append({'pc_elf_va':hex(pc),'phase':n.phase,'E':effective(),'wall':n.now})
        elif pc==0x13073c4:
            sp=u.reg_read(UC_ARM64_REG_SP)
            evidence.setdefault('unprojections',[]).append({'phase':n.phase,
                'point':[n.f(sp+0x28+4*i) for i in range(3)]})
        elif pc==0x13073f8:
            evidence.setdefault('lane_operands',[]).append({'phase':n.phase,
                'native_truncated_X':signed32(n.x(20)),'depth_gt_minus500':n.x(22)&1,
                'depth_lt_500':n.x(23)&1,'widening':widening()})
        elif pc==0xeec1cc:
            evidence.setdefault('lanes',[]).append({'phase':n.phase,'E':effective(),
                'primary':n.x(0)&0xffffffff,'secondary':n.x(0)>>32})
        elif pc in {0xeec4e0,0xeec4f0}:
            ps=n.items(n.x(19),0xb8)
            candidates.append({'phase':n.phase,'E':effective(),
                'stage':'before_sort' if pc==0xeec4e0 else 'after_sort',
                'notes':[{'pointer':hex(p),'lane':n.i(n.q(p+0x20)+0x10),
                          'time':n.i(p+0x18)} for p in ps]})
        elif pc==0x160ce28:
            r={'note':hex(n.x(1)),'generated_id':n.x(2),'phase':n.phase,'E':effective()}
            classifiers.append(r);pending_classifier.append(r)
        elif pc==0x160ce58:pending_classifier[-1]['missed_guard']=n.x(0)&0xffffffff
        elif pc==0x160ce6c:pending_classifier[-1]['consumed_guard']=n.x(0)&0xffffffff
        elif pc==0x160cec0:pending_classifier[-1]['abs_error']=n.x(9)&0xffffffff
        elif pc==0x160ce74:pending_classifier.pop()['consumes']=n.x(23)&1
        elif pc in {0x1730290,0x868e54} and n.x(1) in target['notes'].values():
            r={'category':'recorder','kind':'accepted' if pc==0x1730290 else 'miss',
                'pc_elf_va':hex(pc),'note':hex(n.x(1)),'lr_elf_va':hex(n.x(30)),
                'E':effective(),'phase':n.phase,'judgment_id':n.x(2) if pc==0x1730290 else None,
                'generated_id':n.x(5) if pc==0x1730290 else None,'before':score_state()}
            recorders.append(r);on_return(r,n.x(30))

    for pc in OBSERVE:n.u.hook_add(UC_HOOK_CODE,observe,begin=pc,end=pc)
    n.call(0x1930604);n.call(0x1054f24)
    n.trace=[];n.visual=[];n.animationTrace=[];n.downstream=[]
    n.env=n.alloc(8);n.now=1000
    entry(n);activate(n)
    scene,model=n.scene,n.model;chart=n.q(model+0x28);score=n.q(model+0x38)
    owner=n.q(scene+0x300)
    controls=[p for p in n.items(chart,0x20) if n.typename(p)=='17LogicSceneControl']
    taps=[p for p in n.items(chart,0x20) if n.typename(p)=='12LogicTapNote']
    notes={n.i(n.q(p+0x20)+0x10):p for p in taps}
    target.update(notes=notes,controls=controls,score=score,gauge=n.items(score,0xa0)[0])
    evidence.update(objects={'scene':hex(scene),'model':hex(model),'chart':hex(chart),
        'timeline':hex(n.q(model+0x30)),'score':hex(score),'gauge':hex(target['gauge']),
        'camera':hex(n.q(n.q(model+0x20)+0x2a8)),'control_owner':hex(owner),
        'control_owner_type':n.typename(owner),'owner_visual_feature':n.u.mem_read(owner+0x2c8,1)[0]},
        chart={'N':n.i(chart+0xb8),'end':n.i(chart+0xbc),'main_objects':len(n.items(chart,0x20)),
            'property_110':n.u.mem_read(chart+0x110,1)[0],'md5':n.string(chart+0xf8).decode()},
        runtime_controls=control_state())
    assert chart==chart_ptr and model==model_ptr
    assert n.q(owner+0x2a0)==model and n.q(owner+0x2c0)==chart
    assert n.sceneInitReturn==1 and n.q(scene+0x3e0)==model and n.q(scene+0x3e8)==chart
    assert n.q(n.director+0x140)==scene and n.q(n.director+0x148)==0
    listener=n.state(model)['listener'];evidence['listener']=listener
    assert listener['registered']==listener['enabled']==1 and listener['paused']==0
    assert len(taps)==len(tap_products)==2 and set(notes)=={3,6}
    for r in tap_products:
        p=int(r['pointer'],16)
        assert r['initializer_return']==1 and r['returned_note']==r['pointer']
        assert r['time']==n.i(p+0x18)==n.i(p+0x1c)==1500
        assert n.i(n.q(p+0x20)+0x10)==r['raw_lane']+1
        assert n.i(p+0x50)==0 and n.u.mem_read(p+0x54,1)[0]==1
    expected_kind={'control':None,'camera':5,'lanes':6}[case]
    assert len(controls)==len(control_products)==len(parsed)==(0 if case=='control' else 1)
    if controls:
        p=controls[0];r=control_products[0]
        assert parsed[0]['identifier']==('enwidencamera' if case=='camera' else 'enwidenlanes')
        assert parsed[0]['time']==r['time_argument']==n.i(p+0x18)==500
        assert r['initializer_return']==1 and r['runtime_type']=='17LogicSceneControl'
        assert n.i(p+0x64)==r['kind_argument']==expected_kind
        assert parsed[0]['float']==r['float_argument']==n.f(p+0x68)==500.
        assert parsed[0]['integer']==r['integer_argument']==n.i(p+0x6c)==1
        assert builder[0]['chart_property_110']==0 and builder[0]['admitted_at_elf_va']=='0x1864138'
    assert n.i(chart+0xb8)==n.i(score+0xc)==evidence['count_producer']['return_N']
    assert evidence['chart']['md5']==hashlib.md5(config.fixture_text().encode()).hexdigest()
    maps=n.maps(model)
    evidence['chart']['index']={hex(p):[[k for k,ps in g.items() if p in ps] for g in maps]
                               for p in taps+controls}
    assert all(any(gs) for gs in evidence['chart']['index'].values())
    assert any(w['object']=='chart' and w['pc_elf_va']=='0x173c3cc' and w['value']==0 for w in writes)
    for p in taps:n.u.hook_add(UC_HOOK_MEM_WRITE,written,begin=p+0xc,end=p+0x13)
    n.u.hook_add(UC_HOOK_MEM_WRITE,written,begin=score+0x14,end=score+0x2f)
    n.u.hook_add(UC_HOOK_MEM_WRITE,written,begin=target['gauge']+0x10,end=target['gauge']+0x13)
    evidence['gates']['construction']='pass';state('activation')

    camera=n.q(n.q(model+0x20)+0x2a8)
    def camera_state():
        return {'pointer':hex(camera),'position':[n.f(camera+0x38+4*i) for i in range(3)],
            'euler':[n.f(camera+0xc+4*i) for i in range(3)],'fov':n.f(camera+0x3f8),
            'P':[n.f(camera+0x2a8+4*i) for i in range(16)],
            'V':[n.f(camera+0x2e8+4*i) for i in range(16)],
            'world':[n.f(camera+0x328+4*i) for i in range(16)],
            'PV':[n.f(camera+0x368+4*i) for i in range(16)]}
    def project(x):
        point,out=n.alloc(12),n.alloc(8)
        for i,v in enumerate([x,0.,0.]):n.wf(point+4*i,v)
        n.call(0xbdbb70,camera,point,regs={8:out})
        xy=[n.f(out),n.f(n.director+0x184)-n.f(out+4)]
        assert all(math.isfinite(v) for v in xy)
        return {'world':[x,0.,0.],'jni_xy':xy}
    def advance(E):
        row=frame(n,n.now+E-effective(),'039 frame E'+str(E))
        assert row['E']==row['lastModelE']==E
        assert sum(e['pc']=='0x10a7550' for e in row['lifecycle'])==1
        return state('frame_'+str(E))
    frame(n,n.now+1,'039 preroll');anchor=frame(n,n.now+3001,'039 native music anchor')
    assert anchor['E']==0;evidence['anchor']=anchor
    baseline_points={name:project(x) for name,x,pid in PROBES}
    evidence['camera_at_anchor']=camera_state();evidence['anchor_projections']=baseline_points
    state('anchor')
    evidence['gates']['dispatch_interpolation']='incomplete'
    for E in [500,501,502,750,1000,1500]:advance(E)
    evidence['gates']['dispatch_interpolation']='pass'
    contacts=[];evidence['contacts']=contacts
    evidence['gates']['jni_geometry_judgment']='incomplete'
    for name,x,pid in PROBES:
        projected=project(x);assert projected==baseline_points[name]
        pre=state(name+'_before_DOWN');assert all(r['active'] for r in pre['notes'].values())
        n.phase='039 DOWN_'+name;models=counts['0x10a7550'];start_recorders=len(recorders)
        n.call(0xbe31a8,n.env,0,pid,987000+pid,fs=(*projected['jni_xy'],.5))
        down=state(name+'_after_DOWN')
        assert counts['0x10a7550']==models and down['E']==pre['E']==1500
        assert len(down['mapping'])==len(down['retained'])==1 and down['mask'].bit_count()==1
        m=down['mapping'][0]
        assert m['android_id']==pid and m['touch_slot']==m['slot'] and down['retained']==[m['touch']]
        assert all(abs(a-b)<.5 for a,b in zip(evidence['unprojections'][-1]['point'],projected['world']))
        contact={'name':name,'android_id':pid,'projection':projected,'mapping':m,
            'lanes':evidence['lanes'][-1],'unprojection':evidence['unprojections'][-1],
            'native_lane_operands':evidence['lane_operands'][-1],
            'before':pre,'after_DOWN':down,'recorder_entries':recorders[start_recorders:]}
        contacts.append(contact)
        n.phase='039 UP_'+name;n.call(0xdda71c,n.env,0,pid,988000+pid,fs=(*projected['jni_xy'],0))
        up=state(name+'_after_UP');contact['after_UP']=up
        assert up['mapping']==up['retained']==[] and up['mask']==0
        assert n.q(0x1beef90+m['slot']*8)==0
        assert up['score']==down['score'] and up['notes']==down['notes']
    evidence['camera_at_judgment']=camera_state()
    evidence['gates']['jni_geometry_judgment']='pass';evidence['gates']['cleanup']='incomplete'
    before_next=score_state();final=advance(1501)
    assert final['score']==before_next and final['mapping']==final['retained']==[] and final['mask']==0
    assert final['finished']==0 and int(final['result_cache'],16)==0
    assert counts['0xc27d34']==counts['0x1600bb0']==0
    assert counts['0xbe31a8']==counts['0xdda71c']==counts['0x194ff80']==2
    assert len(candidates)==4 and all(r.get('return_observed') for r in recorders)
    for k in ['PURE','FAR','LOST','shining']:
        assert sum(r['after'][k]-r['before'][k] for r in recorders)==final['score'][k]
    # Preserve the relationships observed in the first native diagnostic.
    # These assertions check native production and causal lane admission,
    # rather than accepting an assumed final score as the whole experiment.
    by_label={r['label']:r for r in states}
    assert evidence['chart']['N']==2 and evidence['chart']['end']==1620
    assert evidence['objects']['owner_visual_feature']==evidence['chart']['property_110']==0
    assert all(r['return_kind']==expected_kind for r in classifications) if controls else not classifications
    if controls:
        assert counts['0x1514c64']==counts['0xf80824']==1
        assert [d['E'] for d in dispatch]==[501,501,501]
        handler=next(d for d in dispatch if d['pc_elf_va']=='0x1514c64')
        assert handler['owner']==hex(owner) and handler['event']==hex(controls[0])
        assert handler['lr_elf_va']=='0xf80828'
        assert by_label['frame_500']['controls'][0]['flags_0c_0d']==[0,0]
        assert by_label['frame_501']['controls'][0]['flags_0c_0d']==[0,1]
        assert by_label['frame_501']['controls'][0]['active'] and not by_label['frame_502']['controls'][0]['active']
        marked=[w for w in writes if w['object']=='control' and w['offset']=='0xd' and w['value']==1]
        assert len(marked)==1 and marked[0]['before']==0 and marked[0]['pc_elf_va']=='0x897e98'
        assert any(r['E_operand']==500 and r['end_operand']==500 for r in evidence['event_time_predicates'])
        assert any(r['E_operand']==501 and r['end_operand']==500 for r in evidence['event_time_predicates'])
        phase_writes=[w for w in writes if w['phase']=='039 frame E501' and w['object']=='model_widening']
        pcs=[w['pc_elf_va'] for w in phase_writes]
        store_pc='0xd59c24' if case=='camera' else '0x1514d08'
        assert pcs.index('0x10a763c')<pcs.index('0x10a76f8')<pcs.index(store_pc)
        selected='camera_transition' if case=='camera' else 'lane_transition'
        other='lane_transition' if case=='camera' else 'camera_transition'
        assert by_label['frame_501']['widening'][selected]=={'start':500,'direction':1,'duration':500.}
        assert all(r['widening'][other]==by_label['anchor']['widening'][other] for r in states)
        assert [c['against'] for c in builder[0]['comparisons']]==([4,5] if case=='camera' else [4,5,6])
    else:
        assert counts['0x1514c64']==counts['0xf80824']==counts['0xd59c24']==0
        assert dispatch==setters==[]
    observed_trajectory={'control':[(1.,0.)]*5,
        'camera':[(1.,0.),(1.0019999742507935,0.),(1.25,0.),(1.5,0.),(1.5,0.)],
        'lanes':[(1.,0.),(1.,0.004000000189989805),(1.,0.5),(1.,1.),(1.,1.)]}[case]
    for E,(G,W) in zip([501,502,750,1000,1500],observed_trajectory):
        s=by_label['frame_'+str(E)]['widening']
        assert s['G']==G and s['W']==W
    if case=='camera':
        assert len(setters)==1 and setters[0]['model']==hex(model)
        assert setters[0]['time_argument']==500 and setters[0]['direction_argument']==1
        assert setters[0]['duration_s0']==500. and setters[0]['lr_elf_va']=='0x1514ce8'
    else:assert setters==[]
    expected_lanes={'control':[(4,0),(5,0)],'camera':[(4,3),(5,0)],'lanes':[(4,0),(6,0)]}[case]
    accepted_lane={'control':None,'camera':3,'lanes':6}[case]
    for contact,(primary,secondary) in zip(contacts,expected_lanes):
        assert contact['lanes']['primary']==primary and contact['lanes']['secondary']==secondary
        operands=contact['native_lane_operands']
        assert operands['depth_gt_minus500']==operands['depth_lt_500']==1
        phase=contact['lanes']['phase']
        rows=[c for c in candidates if c['phase']==phase]
        wanted=[hex(notes[accepted_lane])] if accepted_lane in [primary,secondary] else []
        assert all([r['pointer'] for r in c['notes']]==wanted for c in rows)
    assert len({c['mapping']['touch'] for c in contacts})==2
    assert len({c['mapping']['generated_id'] for c in contacts})==2
    assert counts['0x868e54']==0
    assert len(recorders)==len(classifiers)==(0 if case=='control' else 1)
    if accepted_lane is not None:
        assert recorders[0]['note']==hex(notes[accepted_lane]) and recorders[0]['judgment_id']==0
        assert recorders[0]['lr_elf_va']=='0x160cf48'
        assert classifiers[0]['abs_error']==0 and classifiers[0]['consumes']==1
    for lane,row in final['notes'].items():
        assert row['consumed']==int(int(lane)==accepted_lane) and row['missed']==0
    assert len([w for w in writes if w['object']=='tap' and w['offset']=='0xd' and w['value']==1])==len(recorders)
    assert {k:v for k,v in evidence['camera_at_anchor'].items() if k!='pointer'}=={
        k:v for k,v in evidence['camera_at_judgment'].items() if k!='pointer'}
    forbidden={0xe4e4dc,0xe2ea48,0x173b358,0x1862a14,0x1792e18,0x1514c64,0xd59c24,
        0x1576aa4,0x10a7550,0x130733c,0xeec024,0xf6b514,0x160ce28,0x965e28,
        0x1730290,0x868e54,0xf8056c,0xf9a50c}
    assert not forbidden.intersection(n.host_calls) and not forbidden.intersection(n.hooks)
    assert any(e['pc']=='0xee2214' and int(e['x'][0],16)==1 for e in n.soloTrace)
    assert n.u.mem_read(n.menu+0x490,1)[0]==1
    evidence.update(status='pass',final=final,
        native_call_counts={hex(pc):counts[hex(pc)] for pc in OBSERVE},all_gameplay_handoffs_native=True,
        assertion_scope='Native control admission/dispatch/store order, G/W trajectories, original lane outputs, candidate/note identity, unique recorder and cleanup; no host gameplay arithmetic')
    evidence['gates']['cleanup']='pass'


def run():
    cases={name:{'status':'not_run'} for name in ['control','camera','lanes']}
    evidence={'status':'fail','cases':cases,'native_failures':[],'fresh_emulator_per_case':True,
        'pc_skips_elf_va':PC_SKIPS,'new_boundaries':[],
        'results_sqlite':'not_run; stop at E1501 before unplayed-tap expiry',
        'external_services':'Unchanged ordinary catalog/account/settings/ABI/platform/resources/audio/GPU; synthetic AFF, wall clock and JNI inputs'}
    for name in cases:
        try:run_case(name,cases[name])
        except Exception as exc:
            cases[name]['status']='fail'
            detail={'case':name,'type':type(exc).__name__,'message':str(exc),
                    'line':traceback.extract_tb(exc.__traceback__)[-1].lineno}
            cases[name]['failure']=detail;evidence['native_failures'].append(detail)
            if name=='control':break
    if all(v['status']=='pass' for v in cases.values()):
        evidence.update(status='pass',comparison={name:{'widening':v['final']['widening'],
            'score':v['final']['score'],'lanes':[c['lanes'] for c in v['contacts']],
            'projection_equal_to_control':all(c['projection']==cases['control']['contacts'][i]['projection']
                for i,c in enumerate(v['contacts'])),
            'camera_transform_and_matrices_equal_to_control':
                {k:x for k,x in v['camera_at_judgment'].items() if k!='pointer'}==
                {k:x for k,x in cases['control']['camera_at_judgment'].items() if k!='pointer'}}
            for name,v in cases.items()})
        if not all(c['projection_equal_to_control'] and c['camera_transform_and_matrices_equal_to_control']
                   for c in evidence['comparison'].values()):
            evidence['status']='fail'
            evidence['native_failures'].append({'type':'NativePairedProjectionMismatch',
                'message':'Paired inputs/camera differ; preserve cases and reassess causal attribution'})
    return evidence
