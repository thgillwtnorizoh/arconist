"""038: original linker/generation producers and a retained JNI successor contact."""
import collections
import hashlib
import math
import struct
import traceback
import config
from unicorn import UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm64_const import UC_ARM64_REG_PC, UC_ARM64_REG_D0, UC_ARM64_REG_D8, UC_ARM64_REG_SP
from solo_entry import setup, entry
from lifecycle import activate, frame
from arc_tap_services import install as install_obj_abi
from boundaries import PC_SKIPS

OBSERVE = {
    0xee197c,0xee29a8,0xee29e8,0xe4e4dc,0xe2ea48,0x1870de0,0x924c18,
    0x173b358,0x1862a14,0x178f7fc,0x178f864,0xc664f8,0xd51220,0xd93594,
    0x125e474,0x125e610,0x125e630,0x125e640,0x125e658,0x125e69c,
    0x125e784,0x125e5c8,0x165286c,0x1205bf4,0x173bd60,0x1925084,0x969190,
    0x173bdf0,0x173bdfc,0x173bd9c,0xba81e8,0xba81fc,0xd92558,0xd925fc,
    0xba8200,0xba8248,0xba8274,0xba8278,0xba827c,0x11ea120,0x173bf2c,
    0x1576aa4,0x1576b98,0x10fd1c0,0x10fd8b8,0x1793f8c,0x18be2f8,
    0x10a7550,0x19f3d4c,0x95d61c,0x95d6e8,0x95d6f4,
    0xbe31a8,0xdda71c,0x194ff80,0xeec024,0xf9a50c,0x14858d4,0x1485aa8,
    0xad11b0,0xc98570,
    0xc98490,0xc98648,0xc98664,0x927384,0x15dfe2c,0x15dfe60,
    0x15dfe6c,0x15dfef8,0x15dff4c,0x15dffd4,0x15e015c,
    0x15e01b8,0x15a90c4,0x13db7a0,0xf8056c,0xf80904,
    0x1730290,0x868e54,0xc27d34,0x1600bb0,
}


def run_native(evidence):
    evidence.update(status='running',gates={'link_production':'incomplete',
        'generation_provenance':'not_run','index_admission':'not_run',
        'successor_contact':'not_run','records_cleanup':'not_run'})
    evidence['fixture']={'name':config._fixture_name,
        'sha256':hashlib.sha256(config.fixture_text().encode()).hexdigest()}
    n=setup(True);abi=install_obj_abi(n);n.prepare_runtime();n.observe |= OBSERVE
    arcs=set();groups=set();colors=set();records={};target={};returns={};return_hooks=set()
    counts=collections.Counter();parsed=[];factories=[];writes=[];link=[];generation=[]
    base_records=[];samples=[];index=[];states=[];spatial=[];claims=[];accepts=[]
    references=[];recorders=[];guards=[];releases=[];calls=[];admissions=[]
    evidence.update(parsed=parsed,factories=factories,native_writes=writes,linker=link,
        generation=generation,base_records=base_records,samples=samples,index_producer=index,
        states=states,spatial=spatial,claims=claims,accepts=accepts,linked_references=references,
        recorders=recorders,checkpoint_guards=guards,releases=releases,calls=calls,
        admissions=admissions,native_call_counts=counts)
    factory_pending=[];spatial_pending=[];color_pending=[]
    color_products=[];evidence['color_factory']=color_products

    def effective():
        t=n.q(n.model+0x30);return n.i(t+0x20)-n.i(t+0x28)

    def record_state(a):
        return [{'pointer':hex(p),'time':n.i(p),'weight':n.i(p+4),
            'resolved':n.u.mem_read(p+8,1)[0]} for p in range(n.q(a+0x78),n.q(a+0x80),12)]

    def score_state():
        s,g=target['score'],target['gauge']
        return {'N':n.i(s+0xc),'score':n.i(s+0x14),'combo':n.i(s+0x1c),
            'PURE':n.i(s+0x24),'FAR':n.i(s+0x28),'LOST':n.i(s+0x2c),
            'shining':n.i(s+0x20),'health':n.f(g+0x10)}

    def group_state(g):
        return {'pointer':hex(g),'type':n.typename(g),'vtable_elf_va':hex(n.q(g)),
            'bytes_10_13':list(n.u.mem_read(g+0x10,4)),'window_14':n.f(g+0x14),
            'timestamps':[n.i(p) for p in range(n.q(g+0x18),n.q(g+0x20),4)]}

    def color_state(c):
        return {'pointer':hex(c),'type':n.typename(c),'mapped':n.i(c+0x18),
            'owner':n.i(c+0x28),'release':n.i(c+0x2c),'bypass':n.u.mem_read(c+0x10,1)[0],
            'claimed_byte':n.u.mem_read(c+0x24,1)[0],'conflict':n.u.mem_read(c+0x30,1)[0]}

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

    def written(u,access,where,size,value,unused):
        obj=next((a for a in arcs if a<=where<a+0x180),None)
        kind='arc'
        if obj is None:obj=next((g for g in groups if g<=where<g+0x30),None);kind='group'
        if obj is None:obj=next((c for c in colors if c<=where<c+0x40),None);kind='color'
        record=next((p for ps in records.values() for p in ps if p<=where<p+12),None)
        if obj is None and record is not None:obj=record;kind='checkpoint'
        writes.append({'pc_elf_va':hex(u.reg_read(UC_ARM64_REG_PC)),'phase':n.phase,
            'object':kind if obj is not None else 'score_or_health','pointer':hex(obj) if obj else None,
            'offset':hex(where-obj) if obj else None,'address':hex(where),'size':size,
            'before':int.from_bytes(u.mem_read(where,size),'little'),'value':value,
            'checkpoint_time':n.i(record) if record is not None else None})

    def factory_return(u,pc,size,unused):
        row=factory_pending.pop();p=n.x(0)
        row.update(pointer=hex(p),type=n.typename(p),vtable_elf_va=hex(n.q(p)),
            mode=n.i(p+0xa4),color=hex(n.q(p+0xb0)),native_flag_a0=n.u.mem_read(p+0xa0,1)[0])

    def color_return(u,pc,size,unused):
        row=color_pending.pop();c=n.x(0);colors.add(c)
        row.update(pointer=hex(c),vtable_elf_va=hex(n.q(c)),state=color_state(c))
        for lo,hi in [(c+0x10,c+0x17),(c+0x22,c+0x30)]:
            u.hook_add(UC_HOOK_MEM_WRITE,written,begin=lo,end=hi)

    def recorder_return(u,pc,size,unused):
        if returns.get(pc):returns[pc].pop().update(after=score_state(),return_observed=True)

    def observe(u,pc,size,unused):
        counts[hex(pc)]+=1
        if pc==0x924c18:
            p=n.x(19);parsed.append({'pointer':hex(p),'type':n.typename(p),
                'start':n.i(p+0x18),'end':n.i(p+0x1c),'x':[n.f(p+0x20),n.f(p+0x24)],
                'y':[n.f(p+0x40),n.f(p+0x44)],'curve':n.string(p+0x28).decode(),
                'color':n.i(p+0x48),'mode':n.i(p+0x68)})
        elif pc==0x178f7fc:
            row={'start':n.x(0),'end':n.x(1),'lr_elf_va':hex(n.x(30))}
            factories.append(row);factory_pending.append(row);lr=n.x(30)
            if lr not in return_hooks:
                u.hook_add(UC_HOOK_CODE,factory_return,begin=lr,end=lr);return_hooks.add(lr)
        elif pc==0x178f864:
            a=n.x(0);arcs.add(a)
            for lo,hi in [(a+0x64,a+0x6c),(a+0x78,a+0x88),(a+0xa0,a+0xa0),
                          (a+0xb0,a+0xb7),(a+0xd0,a+0xe7),(a+0x138,a+0x157)]:
                u.hook_add(UC_HOOK_MEM_WRITE,written,begin=lo,end=hi)
        elif pc==0xd93594:
            row={'pc_elf_va':hex(pc),'lr_elf_va':hex(n.x(30)),
                 'mapped_argument_w0':n.x(0)&0xffffffff}
            color_products.append(row);color_pending.append(row);lr=n.x(30)
            if lr not in return_hooks:
                u.hook_add(UC_HOOK_CODE,color_return,begin=lr,end=lr);return_hooks.add(lr)
        elif pc==0x125e69c:
            g=n.x(25);groups.add(g)
            u.hook_add(UC_HOOK_MEM_WRITE,written,begin=g+0x10,end=g+0x2f)
            link.append({'pc_elf_va':hex(pc),'kind':'native_group_allocation',
                         'group':hex(g),'first_arc':hex(n.x(23))})
        elif pc==0x165286c:
            link.append({'pc_elf_va':hex(pc),'kind':'group_setter','arc':hex(n.x(0)),
                         'group_argument':hex(n.x(1))})
        elif pc==0x125e474:
            link.append({'pc_elf_va':hex(pc),'kind':'linker_entry','chart':hex(n.x(0)),
                         'lr_elf_va':hex(n.x(30))})
        elif pc in {0x125e610,0x125e630,0x125e640,0x125e658,0x125e784,0x125e5c8}:
            row={'pc_elf_va':hex(pc),'first_arc':hex(n.x(23)),'second_arc':hex(n.x(24))}
            if pc==0x125e610:row['abs_time_difference']=n.x(8)&0xffffffff
            elif pc==0x125e630:
                row.update(x_difference_double=struct.unpack('<d',struct.pack('<Q',u.reg_read(UC_ARM64_REG_D0)))[0],
                    x_threshold_double=struct.unpack('<d',struct.pack('<Q',u.reg_read(UC_ARM64_REG_D8)))[0])
            elif pc==0x125e640:row.update(successor_y=n.s(0),predecessor_end_y=n.s(1))
            elif pc==0x125e658:row.update(first_mode=n.x(9),second_mode=n.x(8))
            elif pc==0x125e784:row['linked_flag_store_w8']=n.x(8)&255
            link.append(row)
        elif pc in {0x173bdf0,0x173bdfc,0x173bd9c,0xba81e8,0xba81fc,0xd92558,0xba8248,0xba8274,0xba8278}:
            a=n.x(0) if pc in {0x173bd9c,0xba81e8,0xba81fc,0xd92558} else n.x(19) if pc>=0xba0000 and pc<0xbb0000 else n.x(25)
            row={'pc_elf_va':hex(pc),'arc':hex(a),'lr_elf_va':hex(n.x(30))}
            if pc==0x173bdf0:row['native_byte_a0']=n.u.mem_read(a+0xa0,1)[0]
            elif pc==0x173bdfc:row['boolean_w8']=n.x(8)&0xffffffff
            elif pc in {0x173bd9c,0xba81e8,0xba81fc,0xd92558}:
                row.update(argument_w1=n.x(1)&0xffffffff,native_byte_a0=n.u.mem_read(a+0xa0,1)[0])
                if pc==0x173bd9c:row['virtual_elf_va']=hex(n.x(9))
            elif pc==0xba8248:row.update(duration_div_interval_minus1=n.x(8)&0xffffffff,
                duration_minus2_div_interval=n.x(9)&0xffffffff)
            elif pc==0xba8274:row.update(old_end=hex(n.x(8)),new_end=hex(n.x(9)))
            elif pc==0xba8278:row.update(weight_store_address=hex(n.x(8)-0x14),weight_w10=n.x(10))
            generation.append(row)
        elif pc==0xd925fc:
            p=n.x(1);base_records.append({'arc':hex(n.x(0)-0x78),'time':n.i(p),
                'weight':n.i(p+4),'resolved':n.u.mem_read(p+8,1)[0],
                'pc_elf_va':hex(pc)})
        elif pc==0xba8200:
            a=n.x(19);ps=list(range(n.q(a+0x78),n.q(a+0x80),12));records[a]=ps
            generation.append({'pc_elf_va':hex(pc),'arc':hex(a),'base_records':record_state(a)})
            for p in ps:u.hook_add(UC_HOOK_MEM_WRITE,written,begin=p+4,end=p+8)
        elif pc==0xba827c:generation.append({'pc_elf_va':hex(pc),'arc':hex(n.x(19)),
            'final_records':record_state(n.x(19))})
        elif pc==0x969190 and n.x(0)-0xe8 in arcs:
            samples.append({'arc':hex(n.x(0)-0xe8),'point':[n.f(n.x(1)+4*i) for i in range(3)],
                            'lr_elf_va':hex(n.x(30))})
        elif pc==0x11ea120:
            evidence['count_producer']={'chart':hex(n.x(0)),'lo':n.x(1),'hi':n.x(2),
                'lr_elf_va':hex(n.x(30)),'main_objects_before_bars':len(n.items(n.x(0),0x20))}
        elif pc==0x173bf2c:evidence['count_producer']['return_N']=n.x(0)&0xffffffff
        elif pc==0x1576b98 and n.x(19) in arcs:
            index.append({'arc':hex(n.x(19)),'group':n.i(n.x(19)+0x50),
                          'lo':n.x(23)&0xffffffff,'hi':n.x(24)&0xffffffff})
        if not target:return
        if pc in {0x10a7550,0x14858d4,0xbe31a8,0xdda71c,0xf8056c}:
            calls.append({'pc_elf_va':hex(pc),'phase':n.phase,'E':effective(),'wall':n.now})
        if pc==0x10fd8b8 and n.x(28) in arcs:
            admissions.append({'arc':hex(n.x(28)),'phase':n.phase,'E':effective(),
                'min_depth_raw_u32':n.x(23)&0xffffffff,'limit':n.x(27)})
        elif pc==0xc98490:
            row={'arc':hex(n.x(2)),'initial':bool(n.x(3)&1),'phase':n.phase,'E':effective()}
            spatial.append(row);spatial_pending.append(row)
        elif pc==0xc98570 and spatial_pending:
            spatial_pending[-1].update(cache_flag_bool_w10=n.x(10)&0xffffffff,
                at_or_after_start_w9=n.x(9)&0xffffffff)
        elif pc==0xc98648:spatial_pending[-1]['spatial_accepted']=n.x(0)&1
        elif pc==0xc98664:spatial_pending.pop()['returned_eligible']=n.x(0)&1
        elif pc==0x927384 and spatial_pending:
            spatial_pending[-1].update(point=[n.f(n.x(1)+4*i) for i in range(3)],
                target=[n.f(n.x(2)+4*i) for i in range(2)])
        elif pc==0x15dfe2c:
            accepts.append({'arc':hex(n.x(0)),'touch':hex(n.x(1)),
                'generated_id':n.i(n.x(1)+0x34),'native_E':n.x(2),'phase':n.phase})
        elif pc==0x1485aa8:
            sp=u.reg_read(UC_ARM64_REG_SP)
            evidence.setdefault('continuous_unprojection_before_clamp',[]).append({
                'phase':n.phase,'E':effective(),'point':[n.f(sp+0x78+4*i) for i in range(3)]})
        elif pc==0xad11b0:
            evidence.setdefault('cache_setter',[]).append({'arc':hex(n.x(0)),
                'argument_w1':n.x(1)&0xffffffff,'lr_elf_va':hex(n.x(30)),
                'phase':n.phase,'E':effective()})
        elif pc==0x15a90c4:
            claims.append({'color':hex(n.x(0)),'generated_id':n.x(1)&0xffffffff,
                'native_E':n.x(2),'interval':n.x(3),'owner_before':n.i(n.x(0)+0x28),'phase':n.phase})
        elif pc==0x15dfe60:claims[-1]['accepted']=n.x(0)&1
        elif pc in {0x15dfe6c,0x15dfef8,0x15dff4c,0x15dffd4,0x15e015c,0x15e01b8}:
            a=n.x(19);row={'pc_elf_va':hex(pc),'arc':hex(a),'phase':n.phase,'E':effective(),
                'group':hex(n.q(a+0xe0)),'predecessor':hex(n.q(a+0x150)),
                'successors':[hex(p) for p in n.items(a,0x138)]}
            if pc==0x15dffd4:row.update(predecessor_record_w9=n.x(9)&0xffffffff,
                own_record_w10=n.x(10)&0xffffffff,successor_record_w11=n.x(11)&0xffffffff)
            references.append(row)
        elif pc==0x95d6f4:
            references.append({'pc_elf_va':hex(pc),'arc':hex(n.x(19)),'phase':n.phase,
                'E':effective(),'successor_mode_w10':n.x(10)&0xffffffff,
                'scope':'end cleanup returns before shared color reset if ordinary successor exists'})
        elif pc==0xf80904:
            p=n.x(14)-8
            if any(p in ps for ps in records.values()):guards.append({'record':hex(p),
                'time':n.i(p),'resolved':n.x(15)&255,'phase':n.phase,'E':effective()})
        elif pc in {0x1730290,0x868e54} and n.x(1) in arcs:
            row={'kind':'accepted' if pc==0x1730290 else 'miss','arc':hex(n.x(1)),
                'pc_elf_va':hex(pc),'lr_elf_va':hex(n.x(30)),'phase':n.phase,'E':effective(),
                'judgment_id':n.x(2) if pc==0x1730290 else None,'before':score_state()}
            recorders.append(row);ret=n.x(30);returns.setdefault(ret,[]).append(row)
            if ret not in return_hooks:
                u.hook_add(UC_HOOK_CODE,recorder_return,begin=ret,end=ret);return_hooks.add(ret)
        elif pc==0x13db7a0:
            releases.append({'color':hex(n.x(0)),'id':n.x(1)&0xffffffff,
                'owner_before':n.i(n.x(0)+0x28),'time_argument':n.x(2),
                'phase':n.phase,'lr_elf_va':hex(n.x(30))})

    for pc in OBSERVE:n.u.hook_add(UC_HOOK_CODE,observe,begin=pc,end=pc)
    n.phase='038 original static initializers';n.call(0x1930604);n.call(0x1054f24)
    n.trace=[];n.visual=[];n.animationTrace=[];n.downstream=[]
    n.env=n.alloc(8);n.now=1000
    entry(n);activate(n)
    scene,model=n.scene,n.model;chart=n.q(model+0x28);score=n.q(model+0x38)
    ordered=sorted(arcs,key=lambda a:n.i(a+0x18));assert len(ordered)==len(parsed)==len(factories)==2
    assert set(ordered)=={p for p in n.items(chart,0x20) if n.typename(p)=='12LogicArcNote'}
    first,second=ordered;color=n.q(first+0xb0);group=n.q(first+0xe0)
    target.update(score=score,gauge=n.items(score,0xa0)[0],ordered=ordered)
    assert color==n.q(second+0xb0) and n.typename(color)=='10LogicColor'
    assert colors=={color} and len(color_products)==1 and color_products[0]['pointer']==hex(color)
    assert group and group==n.q(second+0xe0) and group in groups
    assert n.typename(group)=='13LogicArcGroup'
    assert n.items(first,0x138)==[second] and n.q(second+0x150)==first
    assert n.items(second,0x138)==[] and n.q(first+0x150)==0
    assert all(n.i(a+0xa4)==0 and n.q(a)==0x1b91500 for a in ordered)
    for a,p in zip(ordered,sorted(parsed,key=lambda r:r['start'])):
        assert [n.i(a+0x18),n.i(a+0x1c)]==[p['start'],p['end']]
        assert p['x']==p['y']==[.5,.5] and p['curve']=='s' and p['mode']==0
    assert n.sceneInitReturn==1 and n.q(scene+0x3e0)==model and n.q(scene+0x3e8)==chart
    assert n.q(n.director+0x140)==scene and n.q(n.director+0x148)==0
    listener=n.state(model)['listener'];assert listener['registered']==listener['enabled']==1 and listener['paused']==0
    evidence['gates']['link_production']='pass'
    # Replace temporary base-vector ranges with the native final vectors only.
    for a in ordered:records[a]=list(range(n.q(a+0x78),n.q(a+0x80),12))
    assert all(records.values())
    native_N=n.i(chart+0xb8)
    assert native_N==evidence['count_producer']['return_N']==n.i(score+0xc)
    assert native_N==sum(n.i(p+4) for ps in records.values() for p in ps)
    assert all(any(r.get('pc_elf_va')=='0xd92558' and r['arc']==hex(a) for r in generation) for a in ordered)
    for a in ordered:
        pointer=hex(a);flag=n.u.mem_read(a+0xa0,1)[0]
        initial=[w for w in writes if w['object']=='arc' and w['pointer']==pointer and
                 w['offset']=='0xa0' and w['pc_elf_va']=='0x178f8fc']
        assert len(initial)==1 and initial[0]['size']==1 and initial[0]['value']==0
        rows=[r for r in generation if r['arc']==pointer]
        load=next(r for r in rows if r['pc_elf_va']=='0x173bdf0')
        boolean=next(r for r in rows if r['pc_elf_va']=='0x173bdfc')
        assert load['native_byte_a0']==flag and boolean['boolean_w8']==int(flag!=0)
        for pc in ['0x173bd9c','0xba81e8','0xba81fc','0xd92558']:
            r=next(r for r in rows if r['pc_elf_va']==pc)
            assert r['argument_w1']==boolean['boolean_w8']
        base=next(r['base_records'] for r in rows if r['pc_elf_va']=='0xba8200')
        final_records=next(r['final_records'] for r in rows if r['pc_elf_va']=='0xba827c')
        assert sum(r['weight'] for r in base)==sum(r['weight'] for r in final_records)
    assert any(w['pointer']==hex(second) and w['offset']=='0xa0' and
               w['pc_elf_va']=='0x125e784' and w['before']==0 and w['value']==1 for w in writes)
    evidence['gates']['generation_provenance']='pass'
    maps=n.maps(model);keys={hex(a):[[k for k,ps in g.items() if a in ps] for g in maps] for a in ordered}
    assert len(index)==2 and all(any(gs) for gs in keys.values())
    geometry=[{'arc':hex(a),'start':n.i(a+0x18),'end':n.i(a+0x1c),
        'color':hex(n.q(a+0xb0)),'group':hex(n.q(a+0xe0)),
        'predecessor_pointer':hex(n.q(a+0x150)),
        'successors':[hex(p) for p in n.items(a,0x138)],
        'flag_a0':n.u.mem_read(a+0xa0,1)[0],'interval':n.f(a+0x70),
        'timing':hex(n.q(a+0x48)),'input_enabled':n.u.mem_read(a+0x54,1)[0],
        'records':record_state(a),'points':[[n.f(p+4*i) for i in range(3)]
            for p in range(n.q(a+0xe8),n.q(a+0xf0),12)]} for a in ordered]
    assert all(len(g['points'])>1 for g in geometry) and all(any(s['arc']==g['arc'] for s in samples) for g in geometry)
    camera=n.q(n.q(model+0x20)+0x2a8)
    evidence.update(objects={'scene':hex(scene),'model':hex(model),'chart':hex(chart),
        'timeline':hex(n.q(model+0x30)),'score':hex(score),'gauge':hex(target['gauge']),
        'color':hex(color),'group':hex(group),'rig':hex(n.q(model+0x20)),'camera':hex(camera)},
        listener=listener,initializer_return=n.sceneInitReturn,geometry=geometry,
        chart={'N':native_N,'end':n.i(chart+0xbc),'main_objects':len(n.items(chart,0x20)),
            'md5':n.string(chart+0xf8).decode(),'index':keys},group_at_activation=group_state(group))
    assert evidence['chart']['md5']==hashlib.md5(config.fixture_text().encode()).hexdigest()
    evidence['gates']['index_admission']='pass'
    for lo,hi in [(score+0x14,score+0x2f),(target['gauge']+0x10,target['gauge']+0x13)]:
        n.u.hook_add(UC_HOOK_MEM_WRITE,written,begin=lo,end=hi)

    def f32(v):return struct.unpack('<f',struct.pack('<f',v))[0]
    def input_target(a):
        start=int(f32(f32(n.f(n.q(a+0x20)+0x14)*850)-425))
        return [start+n.f(a+0xd4),n.f(a+0xd8),0.]
    def state(label):
        row={'label':label,'phase':n.phase,'wall':n.now,'E':effective(),
            'arcs':[{'pointer':hex(a),'time':[n.i(a+0x18),n.i(a+0x1c)],
                'active_member':a in n.items(model,0xa0),'activity':list(n.u.mem_read(a+0x64,2)),
                'cache_enabled':n.u.mem_read(a+0xd0,1)[0],
                'cache_xy':[n.f(a+0xd4),n.f(a+0xd8)],'world_target':input_target(a),
                'depth':[n.i(a+0x30),n.i(a+0x34)],'records':record_state(a)} for a in ordered],
            'color':color_state(color),'group':group_state(group),'mapping':mapping(),
            'retained':[hex(p) for p in n.items(model,0xd0)],'mask':n.i(0x1bfebd4),
            'claimed_ids':[n.i(p) for p in range(n.q(0x1bfa3d8),n.q(0x1bfa3e0),4)],
            'score':score_state(),'finished':n.u.mem_read(model+0x139,1)[0],
            'result_cache':hex(n.q(score+0x68))}
        states.append(row);return row
    def advance(E):
        r=frame(n,n.now+E-effective(),'038 frame E'+str(E))
        assert r['E']==r['lastModelE']==E
        assert sum(e['pc']=='0x10a7550' for e in r['lifecycle'])==1
        return state('frame_'+str(E))
    state('activation')
    frame(n,n.now+1,'038 preroll');evidence['anchor']=frame(n,n.now+3001,'038 native music anchor')
    assert evidence['anchor']['E']==0
    pre=advance(1000);assert pre['arcs'][0]['active_member']
    world=input_target(first);point,out=n.alloc(12),n.alloc(8)
    for i,v in enumerate(world):n.wf(point+4*i,v)
    n.call(0xbdbb70,camera,point,regs={8:out});xy=[n.f(out),n.f(n.director+0x184)-n.f(out+4)]
    assert all(math.isfinite(v) for v in xy)
    evidence['projection']={'world':world,'jni_xy':xy,'source_arc':hex(first)}
    n.phase='038 JNI DOWN42';before_models=counts['0x10a7550']
    n.call(0xbe31a8,n.env,0,42,987042,fs=(*xy,.5));down=state('after_DOWN')
    assert counts['0x10a7550']==before_models and len(down['mapping'])==len(down['retained'])==1
    contact=down['mapping'][0];assert contact['android_id']==42 and contact['touch_slot']==contact['slot']
    assert down['retained']==[contact['touch']] and down['mask'].bit_count()==1
    evidence['contact']=contact;evidence['gates']['successor_contact']='incomplete'
    # Fixed X/Y fixture: no MOVE is needed; all caches/eligibility are observed,
    # and the same original JNI-created Touch remains retained throughout.
    for E in [1001,1125,1250,1375,1500,1625,1875,1876,2000,2001,2002,
              2126,2251,2376,2501,2626,2751,2876]:
        row=advance(E)
        assert row['mapping']==[contact] and row['retained']==[contact['touch']]
    before_up=states[-1]
    assert any(a['arc']==hex(second) and a['touch']==contact['touch'] for a in accepts)
    evidence['gates']['successor_contact']='pass';evidence['gates']['records_cleanup']='incomplete'
    n.phase='038 JNI UP42';n.call(0xdda71c,n.env,0,42,999042,fs=(*xy,0));up=state('after_UP')
    assert up['mapping']==up['retained']==[] and up['mask']==0
    assert n.q(0x1beef90+contact['slot']*8)==0 and up['score']==before_up['score']
    cleaned=advance(2877)
    assert cleaned['mapping']==cleaned['retained']==[] and cleaned['claimed_ids']==[]
    assert cleaned['color']['owner']==-1
    assert all(a['activity']==[0,0] for a in cleaned['arcs'])
    assert cleaned['score']==before_up['score'] and cleaned['finished']==0
    assert int(cleaned['result_cache'],16)==0
    resolved=[w for w in writes if w['object']=='checkpoint' and w['offset']=='0x8']
    assert len(resolved)==len({w['address'] for w in resolved})
    assert all(w['before']==0 and w['value']==w['size']==1 for w in resolved)
    assert len(resolved)==sum(len(ps) for ps in records.values())
    assert all(w['pc_elf_va']=='0xf80924' for w in resolved)
    assert all(r.get('return_observed') for r in recorders)
    for k in ['PURE','FAR','LOST','shining']:
        assert sum(r['after'][k]-r['before'][k] for r in recorders)==cleaned['score'][k]
    assert all(a['touch']==contact['touch'] and a['generated_id']==contact['generated_id'] for a in accepts)
    # These assertions preserve the actual first-run producer/consumer result;
    # the historical supplied flag and N8 are never required by the driver.
    assert len(recorders)==native_N and all(r['kind']=='accepted' for r in recorders)
    assert cleaned['score']['PURE']==cleaned['score']['shining']==native_N
    assert cleaned['score']['FAR']==cleaned['score']['LOST']==0
    assert all(r['judgment_id']==0 and r['lr_elf_va']=='0xf809a8' for r in recorders)
    for a,ps in records.items():
        phases={w['phase'] for w in resolved if any(w['address']==hex(p+8) for p in ps)}
        for phase in phases:
            native_units=sum(n.i(p+4) for p in ps if any(
                w['phase']==phase and w['address']==hex(p+8) for w in resolved))
            assert len([r for r in recorders if r['arc']==hex(a) and r['phase']==phase])==native_units
    by_label={s['label']:s for s in states}
    assert [a['activity'] for a in by_label['frame_2000']['arcs']]==[[1,1],[0,0]]
    assert [a['activity'] for a in by_label['frame_2001']['arcs']]==[[0,0],[1,1]]
    assert [a['active_member'] for a in by_label['frame_2002']['arcs']]==[False,True]
    during=[s for s in states if s['label'].startswith('frame_') and 1001<=s['E']<=2876]
    assert all(s['color']['owner']==contact['generated_id'] and s['color']['bypass']==0 for s in during)
    assert any(r['pc_elf_va']=='0x95d6f4' and r['arc']==hex(first) and
               r['E']==2002 and r['successor_mode_w10']==0 for r in references)
    assert any(r['pc_elf_va']=='0x15dffd4' and r['arc']==hex(first) and
               r['E']==2000 and r['successor_record_w11']==n.i(records[second][0]) for r in references)
    assert any(r['pc_elf_va']=='0x15dfe6c' and r['arc']==hex(second) and
               r['E']==2001 and r['predecessor']==hex(first) for r in references)
    assert all(s['group']['timestamps']==[] and s['group']['window_14']==0 for s in states)
    assert not any(r['pc_elf_va']=='0x15e015c' for r in references)
    assert by_label['after_UP']['group']['bytes_10_13']==[1,1,1,0]
    assert cleaned['group']['bytes_10_13']==[0,1,0,0]
    assert counts['0xbe31a8']==counts['0xdda71c']==counts['0x194ff80']==1
    assert counts['0xc27d34']==counts['0x1600bb0']==0
    forbidden={0xe4e4dc,0xe2ea48,0x173b358,0x1862a14,0x178f7fc,0x125e474,
        0x165286c,0xba81e8,0xd92558,0x1925084,0x1576aa4,0x10a7550,
        0x14858d4,0xc98490,0x927384,0x15dfe2c,0x15a90c4,0x13db7a0,
        0x1730290,0x868e54,0xf8056c}
    assert not forbidden.intersection(n.host_calls) and not forbidden.intersection(n.hooks)
    assert any(e['pc']=='0xee2214' and int(e['x'][0],16)==1 for e in n.soloTrace)
    assert n.u.mem_read(n.menu+0x490,1)[0]==1
    evidence.update(status='pass',final=cleaned,resolution_writes=resolved,
        native_call_counts={hex(pc):counts[hex(pc)] for pc in OBSERVE},
        supplied_obj_abi_calls=abi,all_gameplay_handoffs_native=True,
        assertion_scope='Original link/flag writers, generation register chain, native folded units, per-record recorder multiplicity, one retained contact across boundary and complete cleanup')
    evidence['gates']['records_cleanup']='pass'


def run():
    evidence={'status':'fail','native_failures':[],'pc_skips_elf_va':PC_SKIPS,
        'new_boundaries':[],'optional_comparison':'not_run; native producer and consumer observations first',
        'results_sqlite':'not_run; stop after successor records and cleanup',
        'external_services':'Unchanged ordinary catalog/account/settings/ABI/platform/resources/audio/GPU; synthetic AFF, wall clock and JNI event inputs'}
    try:run_native(evidence)
    except Exception as exc:
        evidence['status']='fail'
        evidence['native_failures'].append({'type':type(exc).__name__,'message':str(exc),
            'line':traceback.extract_tb(exc.__traceback__)[-1].lineno})
    return evidence
