"""037: original mixed candidate arbitration and retained-contact observations."""
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
    0xee197c,0xee29a8,0xee29e8,0xe4e4dc,0xe2ea48,0x1870de0,0xdf4a58,0xb01d6c,
    0x139b96c,0x923240,0x173b358,0x1862a14,0x18640d8,0x18640dc,0x18649b8,
    0x1446490,0x18649bc,0xd92558,0xd925fc,0x11ea120,0x173bf2c,0x1576aa4,
    0x1576b98,0x10fd1c0,0x10fd8b8,0x1793f8c,0x18be2f8,0x10a7550,
    0xbe31a8,0xdda71c,0x194ff80,0xf9a50c,0xeec024,0xeec080,0x13073c4,
    0xeec1cc,0xeec304,0xeec4c0,0xeec4cc,0xeec4e0,0xeec4f0,0xf6b514,
    0xeec53c,0xeec56c,0xeec570,0xeec6ec,0xeec6f4,
    0x160ce28,0x160ce58,0x160ce6c,0x160ce74,0x160cec0,0x965e28,
    0x1866038,0x14858d4,0x1485dac,0x1485e60,0x14557b4,0x14557ec,
    0xf8056c,0xf80904,0x1730290,0x868e54,0xc6e938,0xc27d34,0x1600bb0,
}


def run_case(case, evidence):
    evidence.update(status='running',gates={'construction':'incomplete',
        'arbitration':'not_run','continuity_checkpoints_cleanup':'not_run'})
    fixture='mixed_hold_tap_tap_first' if case=='tap_first' else 'mixed_hold_tap'
    config.configure(config.archive_path,fixture)
    evidence['fixture']={'name':config._fixture_name,
        'sha256':hashlib.sha256(config.fixture_text().encode()).hexdigest()}
    n=setup(True);n.prepare_runtime();n.call(0x1930604);n.call(0x1054f24)
    n.observe |= OBSERVE
    target={};counts=collections.Counter();products=[];generated=[];candidates=[]
    iterations=[];classifiers=[];stops=[];activations=[];guards=[];recorders=[]
    writes=[];snapshots=[];calls=[];index=[];admissions=[];input_checks=[]
    evidence.update(construction=products,generated_records=generated,candidates=candidates,
        iterations=iterations,classifiers=classifiers,iteration_stops=stops,
        activations=activations,checkpoint_guards=guards,recorders=recorders,
        native_writes=writes,snapshots=snapshots,calls=calls,index_producer=index,
        admissions=admissions,input_checks=input_checks,native_call_counts=counts)
    pending=[];returns={};return_hooks=set()

    def effective():
        t=n.q(n.model+0x30)
        return n.i(t+0x20)-n.i(t+0x28)

    def score_state():
        s,g=target['score'],target['gauge']
        return {'N':n.i(s+0xc),'score':n.i(s+0x14),'combo':n.i(s+0x1c),
            'shining':n.i(s+0x20),'PURE':n.i(s+0x24),'FAR':n.i(s+0x28),
            'LOST':n.i(s+0x2c),'health':n.f(g+0x10)}

    def checkpoint_state():
        return [{'pointer':hex(p),'time':n.i(p),'weight':n.i(p+4),
                 'resolved':n.u.mem_read(p+8,1)[0]} for p in target['records']]

    def note_state():
        active=n.items(n.model,0xa0)
        out={}
        for kind,p in target['notes'].items():
            out[kind]={'pointer':hex(p),'start':n.i(p+0x18),'end':n.i(p+0x1c),
                'position':hex(n.q(p+0x20)),'lane':n.i(n.q(p+0x20)+0x10),
                'group':n.i(p+0x50),'input_enabled':n.u.mem_read(p+0x54,1)[0],
                'missed':n.u.mem_read(p+0xc,1)[0],'consumed':n.u.mem_read(p+0xd,1)[0],
                'accepted_id':n.i(p+0x10),'active':p in active,'depth':n.i(p+0x30)}
        h=target['notes']['hold']
        out['hold'].update(latch=n.u.mem_read(h+0xa8,1)[0],
            activity=list(n.u.mem_read(h+0x64,2)),checkpoints=checkpoint_state())
        return out

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

    def snapshot(label):
        row={'label':label,'wall':n.now,'E':effective(),'last_model_E':n.i(29332456),
            'director_frame':n.i(n.director+0x134),'scene_stamp':n.i(n.scene+0x4d0),
            'notes':note_state(),'score':score_state(),'mapping':mapping(),
            'mask':n.i(0x1bfebd4),'retained':[hex(p) for p in n.items(n.model,0xd0)],
            'finished':n.u.mem_read(n.model+0x139,1)[0],
            'result_cache':hex(n.q(target['score']+0x68))}
        snapshots.append(row);return row

    def describe(ps):
        return [{'pointer':hex(p),'type':n.typename(p),'start':n.i(p+0x18),
                 'lane':n.i(n.q(p+0x20)+0x10)} for p in ps]

    def written(u,access,where,size,value,unused):
        kind=next((k for k,p in target['notes'].items() if p<=where<p+0xb0),None)
        record=next((p for p in target['records'] if where==p+8),None)
        writes.append({'address':hex(where),'size':size,
            'before':int.from_bytes(u.mem_read(where,size),'little'),'value':value,
            'pc_elf_va':hex(u.reg_read(UC_ARM64_REG_PC)),'phase':n.phase,
            'object':('checkpoint' if record else kind) or 'score_or_health',
            'offset':hex(where-target['notes'][kind]) if kind else None,
            'checkpoint_time':n.i(record) if record else None})

    def returned(u,pc,size,unused):
        if returns.get(pc):
            row=returns[pc].pop()
            row.update(after=score_state(),notes_after=note_state(),return_observed=True)

    def observe(u,pc,size,unused):
        counts[hex(pc)]+=1
        if pc in {0x18640d8,0x18649b8}:
            p=n.x(27);hold=pc==0x18649b8
            products.append({'kind':'hold' if hold else 'tap','parsed':hex(p),
                'parsed_type':n.typename(p),'start':n.i(p+0x18),'end':n.i(p+0x1c),
                'raw_lane':n.i(n.q(p+0x20)+8),
                'factory_or_initializer_elf_va':hex(0x1446490 if hold else n.x(8)),
                'position':hex(n.x(3) if hold else n.x(2)),
                'start_argument':n.x(1)})
        elif pc in {0x18640dc,0x18649bc}:
            p=n.x(0) if pc==0x18649bc else n.x(25)
            products[-1].update(pointer=hex(p),runtime_type=n.typename(p),
                vtable_elf_va=hex(n.q(p)),native_return=n.x(0))
        elif pc==0xd925fc:
            p=n.x(1);generated.append({'hold':hex(n.x(0)-0x78),
                'time':n.i(p),'weight':n.i(p+4),'resolved':n.u.mem_read(p+8,1)[0]})
        elif pc==0x11ea120:
            evidence['native_count_call']={'chart':hex(n.x(0)),
                'time_lo':n.x(1),'time_hi':n.x(2),'lr_elf_va':hex(n.x(30)),
                'main_before_bars':len(n.items(n.x(0),0x20))}
        elif pc==0x173bf2c:evidence['native_count_call']['return_N']=n.x(0)&0xffffffff
        elif pc==0x1576b98 and n.typename(n.x(19)) in {'13LogicHoldNote','12LogicTapNote'}:
            index.append({'note':hex(n.x(19)),'group':n.i(n.x(19)+0x50),
                'lo':n.x(23)&0xffffffff,'hi':n.x(24)&0xffffffff})
        if not target:return
        if pc in {0xbe31a8,0xdda71c,0x194ff80,0xeec024,0xeec080,
                  0x10a7550,0xf8056c,0x14858d4}:
            calls.append({'pc_elf_va':hex(pc),'phase':n.phase,'E':effective(),
                'wall':n.now,'lr_elf_va':hex(n.x(30))})
        if pc==0x10fd8b8 and n.x(28) in target['notes'].values():
            admissions.append({'note':hex(n.x(28)),'phase':n.phase,
                'min_depth_raw_u32':n.x(23)&0xffffffff,'limit':n.x(27)})
        elif pc==0xeec304 and n.x(27) in target['notes'].values():
            input_checks.append({'note':hex(n.x(27)),'input_enabled':n.x(8)&255,
                                 'phase':n.phase,'E':effective()})
        elif pc in {0xeec4c0,0xeec4cc}:
            evidence.setdefault('hold_collection_predicates',[]).append({
                'pc_elf_va':hex(pc),'phase':n.phase,'note':hex(n.x(1)),
                'E':effective(),'w8':n.x(8)&0xffffffff,'w9':n.x(9)&0xffffffff,
                'w10':n.x(10)&0xffffffff})
        elif pc in {0xeec4e0,0xeec4f0}:
            candidates.append({'stage':'before_sort' if pc==0xeec4e0 else 'after_sort',
                'phase':n.phase,'E':effective(),'notes':describe(n.items(n.x(19),0xb8))})
        elif pc==0xeec53c:
            iterations.append({'note':hex(n.q(n.x(20))),'phase':n.phase,'E':effective()})
        elif pc==0x160ce28:
            row={'note':hex(n.x(1)),'phase':n.phase,'E':effective(),
                'generated_id':n.x(2),'lr_elf_va':hex(n.x(30))}
            classifiers.append(row);pending.append(row)
        elif pc==0x160ce58:pending[-1]['missed_guard_return']=n.x(0)&0xffffffff
        elif pc==0x160ce6c:pending[-1]['consumed_guard_return']=n.x(0)&0xffffffff
        elif pc==0x160cec0:
            pending[-1].update(abs_error=n.x(9)&0xffffffff,native_E=n.x(4)&0xffffffff)
        elif pc==0x160ce74:pending.pop()['consumes']=n.x(23)&1
        elif pc==0xeec56c:classifiers[-1]['caller_w0']=n.x(0)&0xffffffff
        elif pc==0xeec570:
            stops.append({'reason':'tap_classifier_true','pc_elf_va':hex(pc),
                'note':hex(n.x(25)),'phase':n.phase,'E':effective()})
        elif pc==0xeec6ec:
            evidence.setdefault('latch_branches',[]).append({'hold':hex(n.x(0)),
                'phase':n.phase,'E':effective(),'latch_before':n.u.mem_read(n.x(0)+0xa8,1)[0]})
        elif pc==0xeec6f4:
            stops.append({'reason':'hold_latch','pc_elf_va':hex(pc),'note':hex(n.x(0)),
                'phase':n.phase,'E':effective(),'latch_after':n.u.mem_read(n.x(0)+0xa8,1)[0]})
        elif pc==0x1485dac:
            evidence.setdefault('continuous_latch_reads',[]).append({'hold':hex(n.x(0)),
                'phase':n.phase,'E':effective(),'latch':n.u.mem_read(n.x(0)+0xa8,1)[0]})
        elif pc==0x1485e60:
            evidence.setdefault('activation_callers',[]).append({'hold':hex(n.x(0)),
                'touch':hex(n.x(1)),'E':n.x(2),'virtual_elf_va':hex(n.x(8)),
                'phase':n.phase})
        elif pc==0x14557b4:
            activations.append({'hold':hex(n.x(0)),'touch':hex(n.x(1)),
                'generated_id':n.i(n.x(1)+0x34),'E':n.x(2),'phase':n.phase,
                'activity_before':list(n.u.mem_read(n.x(0)+0x64,2))})
        elif pc==0xf80904:
            r=n.x(14)-8
            if r in target['records']:
                guards.append({'record':hex(r),'time':n.i(r),'resolved':n.x(15)&255,
                               'phase':n.phase,'E':effective()})
        elif pc in {0x1730290,0x868e54} and n.x(1) in target['notes'].values():
            row={'kind':'accepted' if pc==0x1730290 else 'miss','note':hex(n.x(1)),
                'pc_elf_va':hex(pc),'lr_elf_va':hex(n.x(30)),'phase':n.phase,'E':effective(),
                'judgment_id':n.x(2) if pc==0x1730290 else None,
                'time_argument':n.x(4) if pc==0x1730290 else n.x(2),
                'contact_id_raw':n.x(5) if pc==0x1730290 else None,
                'before':score_state(),'notes_before':note_state()}
            recorders.append(row);ret=n.x(30);returns.setdefault(ret,[]).append(row)
            if ret not in return_hooks:
                u.hook_add(UC_HOOK_CODE,returned,begin=ret,end=ret);return_hooks.add(ret)
        elif pc==0x13073c4:
            sp=u.reg_read(UC_ARM64_REG_SP)
            evidence.setdefault('unprojections',[]).append({'phase':n.phase,
                'point':[n.f(sp+0x28+4*i) for i in range(3)]})
        elif pc==0xeec1cc:
            evidence.setdefault('lanes',[]).append({'phase':n.phase,
                'primary':n.x(0)&0xffffffff,'secondary':n.x(0)>>32})

    for pc in OBSERVE:n.u.hook_add(UC_HOOK_CODE,observe,begin=pc,end=pc)
    n.trace=[];n.visual=[];n.animationTrace=[];n.downstream=[]
    n.env=n.alloc(8);n.now=1000
    entry(n);activate(n)
    scene,model=n.scene,n.model;chart=n.q(model+0x28);score=n.q(model+0x38)
    found={k:[p for p in n.items(chart,0x20) if n.typename(p)==t]
           for k,t in [('hold','13LogicHoldNote'),('tap','12LogicTapNote')]}
    assert all(len(ps)==1 for ps in found.values()) and len(products)==2
    notes={k:ps[0] for k,ps in found.items()};hold,tap=notes['hold'],notes['tap']
    records=list(range(n.q(hold+0x78),n.q(hold+0x80),12))
    target.update(notes=notes,score=score,gauge=n.items(score,0xa0)[0],records=records)
    assert n.sceneInitReturn==1 and n.q(scene+0x3e0)==model and n.q(scene+0x3e8)==chart
    assert n.q(n.director+0x140)==scene and n.q(n.director+0x148)==0
    listener=n.state(model)['listener']
    assert listener['registered']==listener['enabled']==1 and listener['paused']==0
    expected_tap=950 if case=='tap_first' else 1250
    assert n.i(hold+0x18)==1000 and n.i(hold+0x1c)==2000 and n.i(tap+0x18)==expected_tap
    for row in products:
        p=notes[row['kind']]
        assert row['pointer']==hex(p) and row['raw_lane']==3
        assert n.i(n.q(p+0x20)+0x10)==row['raw_lane']+1
        assert n.i(p+0x50)==0 and n.u.mem_read(p+0x54,1)[0]==1
        assert row['position']==hex(n.q(p+0x20)) and row['start_argument']==row['start']==n.i(p+0x18)
    assert len(records)==len(generated)>0
    assert [(r['time'],r['weight'],r['resolved']) for r in generated]==[
        (n.i(p),n.i(p+4),n.u.mem_read(p+8,1)[0]) for p in records]
    assert all(r['hold']==hex(hold) for r in generated)
    assert n.i(chart+0xb8)==n.i(score+0xc)==evidence['native_count_call']['return_N']
    assert n.i(chart+0xb8)==sum(n.i(p+4) for p in records)+1
    maps=n.maps(model);keys={k:[[key for key,ps in g.items() if p in ps] for g in maps]
                            for k,p in notes.items()}
    assert len(index)==2 and all(any(groups) for groups in keys.values())
    rig=n.q(model+0x20);camera=n.q(rig+0x2a8)
    evidence.update(objects={'scene':hex(scene),'model':hex(model),'chart':hex(chart),
        'timeline':hex(n.q(model+0x30)),'score':hex(score),'gauge':hex(target['gauge']),
        'hold':hex(hold),'tap':hex(tap),'rig':hex(rig),'camera':hex(camera)},
        listener=listener,initializer_return=n.sceneInitReturn,
        chart={'N':n.i(chart+0xb8),'end':n.i(chart+0xbc),'index':keys,
            'main_objects':len(n.items(chart,0x20)),'md5':n.string(chart+0xf8).decode(),
            'checkpoint_interval':n.f(hold+0x70),'checkpoints':checkpoint_state(),
            'timings':[[{'pointer':hex(p),'start':n.i(p+0x10),'end':n.i(p+0x14),
                'bpm':n.f(p+0x20),'scale':n.f(p+0x28)} for p in n.items(g)] for g in n.items(chart,0x38)]})
    assert evidence['chart']['md5']==hashlib.md5(config.fixture_text().encode()).hexdigest()
    for p in notes.values():
        n.u.hook_add(UC_HOOK_MEM_WRITE,written,begin=p+0xc,end=p+0x13)
    for lo,hi in [(hold+0x64,hold+0x65),(hold+0xa8,hold+0xa8),
                  (score+0x14,score+0x2f),(target['gauge']+0x10,target['gauge']+0x13)]:
        n.u.hook_add(UC_HOOK_MEM_WRITE,written,begin=lo,end=hi)
    for p in records:n.u.hook_add(UC_HOOK_MEM_WRITE,written,begin=p+8,end=p+8)
    evidence['gates']['construction']='pass';snapshot('activation')

    def advance(E):
        r=frame(n,n.now+E-effective(),'037 frame E'+str(E))
        assert r['E']==r['lastModelE']==E
        assert sum(e['pc']=='0x10a7550' for e in r['lifecycle'])==1
        return snapshot('frame_'+str(E))

    frame(n,n.now+1,'037 preroll')
    evidence['anchor']=frame(n,n.now+3001,'037 native music anchor')
    assert evidence['anchor']['E']==0
    lane=n.i(n.q(hold+0x20)+0x10);assert n.i(n.q(tap+0x20)+0x10)==lane
    world=[425.*(lane-3.5),0.,0.];point,out=n.alloc(12),n.alloc(8)
    for i,v in enumerate(world):n.wf(point+4*i,v)
    n.call(0xbdbb70,camera,point,regs={8:out})
    xy=[n.f(out),n.f(n.director+0x184)-n.f(out+4)]
    assert all(math.isfinite(v) for v in xy)
    evidence['projection']={'world':world,'jni_xy':xy,'native_lane':lane}
    events=[];evidence['inputs']=events
    def event(down,pid,label):
        n.phase=label;before=snapshot(label+'_before');models=counts['0x10a7550']
        n.call(0xbe31a8 if down else 0xdda71c,n.env,0,pid,
               (987000 if down else 988000)+pid,fs=(*xy,.5 if down else 0))
        after=snapshot(label+'_after');events.append({'down':down,'android_id':pid,
            'phase':label,'E':effective(),'before':before,'after':after})
        assert counts['0x10a7550']==models and before['E']==after['E']
        assert len(after['mapping'])==len(after['retained'])==after['mask'].bit_count()
        assert {m['touch'] for m in after['mapping']}==set(after['retained'])
        assert all(m['touch_slot']==m['slot'] for m in after['mapping'])
        old={m['android_id']:m for m in before['mapping']}
        new={m['android_id']:m for m in after['mapping']}
        assert set(new)==(set(old)|{pid} if down else set(old)-{pid})
        for other in set(old)&set(new):assert old[other]==new[other]
        if down:
            assert pid not in old
            assert evidence['lanes'][-1]['primary']==lane
            assert all(abs(a-b)<.5 for a,b in zip(evidence['unprojections'][-1]['point'],world))
        else:
            assert before['score']==after['score'] and before['notes']==after['notes']
            assert n.q(0x1beef90+old[pid]['slot']*8)==0
        return after

    evidence['gates']['arbitration']='incomplete'
    if case=='hold_unlatched':
        pre=advance(1250);evidence['comparison_precondition']=pre
        assert all(v['active'] for v in pre['notes'].values())
        event(True,42,'037 A1 first_DOWN')
        advance(1251);advance(1252)
    elif case=='hold_latched':
        advance(1000);event(True,42,'037 A2 initial_DOWN')
        advance(1001);advance(1125)
        pre=advance(1250);evidence['comparison_precondition']=pre
        assert all(v['active'] for v in pre['notes'].values())
        both=event(True,43,'037 A2 second_DOWN')
        assert len(both['retained'])==2
        advance(1251);event(False,42,'037 A2 release_original')
        advance(1252)
    else:
        pre=advance(1000);evidence['comparison_precondition']=pre
        assert all(v['active'] for v in pre['notes'].values())
        event(True,42,'037 B first_DOWN')
        # A second eligible contact observes native resolved-tap guards and hold
        # selection at the same E, without an intervening model frame.
        both=event(True,43,'037 B second_DOWN')
        assert len(both['retained'])==2
        advance(1001);event(False,43,'037 B release_second')
        advance(1002);advance(1125);advance(1126)
    evidence['gates']['arbitration']='pass'
    evidence['gates']['continuity_checkpoints_cleanup']='incomplete'
    # Same bounded tail; ordinary expiry decides the unplayed competing tap.
    for E in [1350,1351,1375,1376,1625,1626]:advance(E)
    retained=mapping()
    for row in retained:event(False,row['android_id'],'037 terminal_UP_'+str(row['android_id']))
    final=advance(1627);evidence['final']=final
    assert final['mapping']==final['retained']==[] and final['mask']==0
    assert final['notes']['hold']['activity']==[0,0]
    assert final['finished']==0 and int(final['result_cache'],16)==0
    assert final['score']==events[-1]['after']['score']
    resolution_writes=[w for w in writes if w['object']=='checkpoint']
    assert len(resolution_writes)==len(records)==len({w['address'] for w in resolution_writes})
    assert all(w['before']==0 and w['value']==w['size']==1 for w in resolution_writes)
    assert all(w['pc_elf_va']=='0xf80924' for w in resolution_writes)
    assert all(r['resolved']==1 for r in final['notes']['hold']['checkpoints'])
    assert all(r.get('return_observed') for r in recorders)
    for field in ['PURE','FAR','LOST','shining']:
        assert sum(r['after'][field]-r['before'][field] for r in recorders)==final['score'][field]
    tap_consumptions=[w for w in writes if w['object']=='tap' and w['offset']=='0xd' and w['value']==1]
    assert len(tap_consumptions)<=1
    assert stops and candidates and activations and guards and resolution_writes
    assert all(a['hold']==hex(hold) for a in activations)
    assert all(a['virtual_elf_va']=='0x14557b4' for a in evidence['activation_callers'])
    # Preserve the causal relationships established by the initial native run,
    # rather than treating a matching final score as sufficient evidence.
    downs=[e for e in events if e['down']]
    assert len(candidates)==2*len(downs) and len(stops)==len(downs)
    for e in downs:
        rows=[c for c in candidates if c['phase']==e['phase']]
        assert [r['stage'] for r in rows]==['before_sort','after_sort']
        assert all({r['pointer'] for r in c['notes']}=={hex(hold),hex(tap)} for c in rows)
        times=[r['start'] for r in rows[1]['notes']];assert times==sorted(times)
        visits=[r['note'] for r in iterations if r['phase']==e['phase']]
        stop=[r for r in stops if r['phase']==e['phase']]
        assert len(stop)==1 and visits[-1]==stop[0]['note']
    assert any(w['offset']=='0x64' and w['value']==0 and w['pc_elf_va']=='0x1866038' for w in writes)
    assert any(w['offset']=='0x64' and w['value']==0x101 and w['pc_elf_va']=='0x14557ec' for w in writes)
    assert final['notes']['hold']['latch']==1
    hold_records=[r for r in recorders if r['note']==hex(hold)]
    assert len(hold_records)==sum(n.i(p+4) for p in records)
    assert all(r['kind']=='accepted' and r['judgment_id']==0 and
               r['lr_elf_va']=='0xf809a8' for r in hold_records)
    assert {g['time'] for g in guards if g['resolved']==1}=={n.i(p) for p in records}
    if case in {'hold_unlatched','hold_latched'}:
        assert classifiers==[] and all(s['reason']=='hold_latch' for s in stops)
        assert all(s['note']==hex(hold) for s in stops)
        tap_records=[r for r in recorders if r['note']==hex(tap)]
        assert len(tap_records)==1 and tap_records[0]['kind']=='miss'
        assert tap_records[0]['lr_elf_va']=='0xf80b74'
        assert final['notes']['tap']['missed']==1 and final['notes']['tap']['consumed']==0
    if case=='hold_latched':
        assert [r['latch_before'] for r in evidence['latch_branches']]==[0,1]
        second=downs[1]['after'];assert len(second['retained'])==2
        ids={m['android_id']:m for m in second['mapping']}
        assert len({m['generated_id'] for m in ids.values()})==2
        assert {a['touch'] for a in activations if a['E']==1251}==set(second['retained'])
        replacement=ids[43]['touch']
        assert [a['touch'] for a in activations if a['E']==1252]==[replacement]
        evidence['contact_continuity']={'coexisting_at_E1251':ids,
            'after_UP42_at_E1252':replacement,'exclusive_hold_owner_claimed':False}
    elif case=='tap_first':
        assert len(classifiers)==2
        assert classifiers[0]['abs_error']==50 and classifiers[0]['consumes']==1
        assert classifiers[1]['consumed_guard_return']==1 and classifiers[1]['consumes']==0
        assert [s['reason'] for s in stops]==['tap_classifier_true','hold_latch']
        first,second=[e['after'] for e in downs]
        assert first['notes']['hold']['latch']==0 and second['notes']['hold']['latch']==1
        assert first['E']==second['E']==1000 and first['wall']==second['wall']
        assert first['last_model_E']==second['last_model_E']
        ids={m['android_id']:m for m in second['mapping']}
        assert len({m['generated_id'] for m in ids.values()})==2
        assert {a['touch'] for a in activations if a['E']==1001}==set(second['retained'])
        original=ids[42]['touch']
        assert [a['touch'] for a in activations if a['E']==1002]==[original]
        assert first['notes']['tap']['accepted_id']==ids[42]['generated_id']
        tap_records=[r for r in recorders if r['note']==hex(tap)]
        assert len(tap_records)==1 and tap_records[0]['kind']=='accepted'
        assert tap_records[0]['judgment_id']==1 and tap_records[0]['lr_elf_va']=='0x160cf90'
        evidence['contact_continuity']={'coexisting_at_E1001':ids,
            'tap_judging_contact_sustains_hold_after_UP43':original,
            'exclusive_hold_owner_claimed':False}
    assert counts['0xbe31a8']==counts['0xdda71c']==counts['0x194ff80']
    assert counts['0xc27d34']==counts['0x1600bb0']==0
    forbidden={0xe4e4dc,0xe2ea48,0x173b358,0x1862a14,0x1446490,0xd92558,
        0x1576aa4,0x10fd1c0,0x10a7550,0xeec024,0xf6b514,0x160ce28,0x965e28,
        0x14858d4,0x14557b4,0xf8056c,0x1730290,0x868e54,0xf9a50c}
    assert not forbidden.intersection(n.host_calls) and not forbidden.intersection(n.hooks)
    eligibility=[e for e in n.soloTrace if e['pc']=='0xee2214']
    assert len(eligibility)==1 and int(eligibility[0]['x'][0],16)==1
    assert n.u.mem_read(n.menu+0x490,1)[0]==1
    evidence.update(status='pass',native_call_counts={hex(pc):counts[hex(pc)] for pc in OBSERVE},
        resolution_writes=resolution_writes,all_gameplay_handoffs_native=True,
        assertion_scope='Native ownership, chronological mixed candidates, stopping provenance, distinct retained contacts, continuous activation, unique records and cleanup; no host score calculation')
    evidence['gates']['continuity_checkpoints_cleanup']='pass'


def run():
    names=['hold_unlatched','hold_latched','tap_first']
    evidence={'status':'fail','cases':{k:{'status':'not_run'} for k in names},
        'fresh_emulator_per_case':True,'native_failures':[],'pc_skips_elf_va':PC_SKIPS,
        'new_boundaries':[],'results_sqlite':'not_run; stop at native E1627'}
    try:
        for case in names:run_case(case,evidence['cases'][case])
        evidence.update(status='pass',comparison={k:{'N':v['chart']['N'],'end':v['chart']['end'],
            'stops':v['iteration_stops'],'final_score':v['final']['score'],
            'final_notes':v['final']['notes']} for k,v in evidence['cases'].items()},
            external_services='Unchanged ordinary catalog/account/settings/ABI/platform/resources/audio/GPU; synthetic AFF, wall clock and JNI events',
            scientific_scope='Unequal start times, shared lane, specified contact histories; no universal contact exclusivity or equal-key priority claim')
    except Exception as exc:
        for v in evidence['cases'].values():
            if v['status']=='running':v['status']='fail'
        evidence['native_failures'].append({'type':type(exc).__name__,'message':str(exc),
            'line':traceback.extract_tb(exc.__traceback__)[-1].lineno})
    return evidence
