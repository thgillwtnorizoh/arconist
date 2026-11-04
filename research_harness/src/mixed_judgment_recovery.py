"""042: two fresh native-owned mixed-judgment sessions, including final results.

Hooks below observe instructions/memory only. Native gameplay state is never
assigned; the only scenario inputs are AFF, wall clock and projected JNI events.
"""
import collections
import hashlib
import math
import struct
import traceback
from unicorn import UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm64_const import UC_ARM64_REG_PC, UC_ARM64_REG_SP
import config
from solo_entry import setup, entry
from lifecycle import activate, frame, ending
from boundaries import PC_SKIPS

TIMES = (1000, 1500, 2000, 2500, 3000, 3500)
OBSERVE = {
    0xee197c, 0xee29a8, 0xee29e8, 0xe4e4dc, 0xe2ea48,
    0x1870de0, 0xdf4a58, 0xb01d6c, 0x173b358, 0x1862a14,
    0x18640d8, 0x18640dc, 0x11ea120, 0x173bf2c, 0x1576aa4,
    0x1576b98, 0x10fd1c0, 0x10fd8b8, 0xbdbb70,
    0x1793f8c, 0x18be2f8, 0x10a7550, 0xf8056c, 0xf80a58,
    0xbe31a8, 0xdda71c, 0x194ff80, 0xeec024, 0xeec080,
    0x13073c4, 0xeec1cc, 0xeec4e0, 0xf6b514, 0xeec4f0,
    0x160ce28, 0x160cec0, 0x160ce74, 0xeec56c,
    0x965e28, 0x1730290, 0x868e54, 0x1730350, 0x16e4ab0,
    0x1869e90, 0x133fac8, 0xe43b80, 0xa126f4, 0x83dd70,
    0x14f0a94, 0x13e00b4, 0x12c5070, 0x160a3b8,
    0x173057c, 0x1730584, 0x868fdc, 0x10a7d50,
    0xc27d34, 0x1600bb0, 0x1600c4c, 0x1600d80, 0x1600da8,
    0x1315038, 0x131505c, 0x12a5574,
    0x891684, 0x89219c, 0x8921b8, 0x147dee8, 0x891150,
    0xdc2c48, 0x13552d4, 0x12a5e60,
}


def results_continuation(n, e):
    """Reuse native ending; observe the existing shutter schedule generically.

    lifecycle.downstream's two-PURE-specific assertions remain unchanged.
    This observer neither supplies result fields nor calls persistence writers.
    """
    out = e['results_sqlite']
    out['status'] = 'running'
    ending(n)
    rs = n.resultScenes[0]
    session = n.q(rs + 0x2e8)
    assert n.q(session + 0x18) == n.result
    out.update(scene=hex(rs), scene_type=n.typename(rs), session=hex(session),
               session_result=hex(n.q(session + 0x18)))
    frame(n, n.now, '042 Director activates native results shutter')
    for dt in [0, .25, .25, .25]:
        n.tick(dt)
    out.update(scores=n.query('SELECT * FROM scores'),
               clearTypes=n.query('SELECT * FROM clearTypes'))
    for dt in [0, .2, .2, 0, 0, .1, .1, .1, 0]:
        n.tick(dt)
    assert n.q(n.director + 0x148) == rs
    frame(n, n.now, '042 Director activates native results scene')
    assert n.q(n.director + 0x140) == rs and n.q(n.director + 0x148) == 0
    assert n.u.mem_read(n.dispatcher + 0x124, 1)[0] == 1
    assert n.items(n.director, 0x158) == [rs]
    for dt in [0, .25, 1, 5]:
        n.tick(dt)
    frame(n, n.now, '042 additional native results update')
    assert n.query('SELECT * FROM scores') == out['scores']
    assert n.query('SELECT * FROM clearTypes') == out['clearTypes']
    r = e['native_result']
    assert len(out['scores']) == len(out['clearTypes']) == 1
    expected = dict(songId='sayonarahatsukoi', songDifficulty=0, score=r['score'],
                    shinyPerfectCount=r['shining'], perfectCount=r['PURE'],
                    nearCount=r['FAR'], missCount=r['LOST'], health=r['health'])
    assert all(out['scores'][0][k] == v for k, v in expected.items())
    assert out['clearTypes'][0]['clearType'] == r['category']
    assert n.native_sqlite and 'sqlite3_step' in n.nativeSqlCalls
    out.update(status='pass', unchanged_after_extra_updates=True,
        native_sqlite_calls=dict(collections.Counter(n.nativeSqlCalls)),
        running_scene=hex(n.q(n.director + 0x140)), pending=0,
        dispatcher_enabled=1, result_cache_equals_session=True,
        timeline_tracks=len(n.items(n.endingTimeline, 0x50)))


def run_case(recovery, e):
    e.update(status='running', gates={k:'not_run' for k in
        ['construction', 'pure_far', 'lost_combo_break', 'post_break', 'completion', 'cleanup']},
        construction=[], index_insertions=[], admissions=[], snapshots=[], candidates=[],
        classifiers=[], recorders=[], native_writes=[], expiry_guards=[],
        decisive_calls=[], gauge_applications=[], combo_instructions=[],
        inputs=[], score_gauge_producers=[], results_sqlite={'status':'not_run'}, save_gate=[])
    n = setup(True)
    n.prepare_runtime()
    n.call(0x1930604)
    n.call(0x1054f24)
    n.observe |= OBSERVE
    counts = collections.Counter()
    taps, target, returns, installed = set(), {}, {}, set()
    pending = []
    chart_pointer = 0

    def effective():
        t = n.q(n.model + 0x30)
        return n.i(t + 0x20) - n.i(t + 0x28)

    def score_state():
        s, g = target['score'], target['gauge']
        return dict(N=n.i(s+0xc), max_combo=n.i(s+0x10), score=n.i(s+0x14),
            combo=n.i(s+0x1c), shining=n.i(s+0x20), PURE=n.i(s+0x24),
            FAR=n.i(s+0x28), LOST=n.i(s+0x2c), health=n.f(g+0x10),
            mode=n.i(s+0x94), gauge_id=n.i(g+0xa0))

    def note_state():
        active = n.items(n.model, 0xa0)
        return {str(t):dict(pointer=hex(p), time=n.i(p+0x18),
            lane=n.i(n.q(p+0x20)+0x10), group=n.i(p+0x50),
            input_enabled=n.u.mem_read(p+0x54,1)[0],
            missed=n.u.mem_read(p+0xc,1)[0], consumed=n.u.mem_read(p+0xd,1)[0],
            accepted_id=n.i(p+0x10), active=p in active, depth=n.i(p+0x30))
            for t,p in target['notes'].items()}

    def mapping():
        rows = []
        def walk(p):
            if not p:
                return
            walk(n.q(p))
            slot = n.i(p+0x28)
            touch = n.q(0x1beef90+slot*8)
            rows.append(dict(android_id=struct.unpack('<q', n.u.mem_read(p+0x20,8))[0],
                slot=slot, touch_slot=n.i(touch+0xc), touch=hex(touch),
                generated_id=n.i(touch+0x34)))
            walk(n.q(p+8))
        walk(n.q(0x1bf1a90))
        return rows

    def snapshot(label):
        t = n.q(n.model+0x30)
        row = dict(label=label, wall=n.now, E=effective(), last_model_E=n.i(0x1bf93e8),
            timeline=dict(steady_origin=n.q(t+0x10),system_origin=n.q(t+0x18),
                R=n.i(t+0x20),C=n.i(t+0x28),O=n.i(t+0x30),A=n.i(t+0x34),B=n.i(t+0x38),
                paused=n.u.mem_read(t+0x2c,1)[0],steady=n.u.mem_read(t+0x2d,1)[0]),
            director_frame=n.i(n.director+0x134), scene_stamp=n.i(n.scene+0x4d0),
            notes=note_state(), score=score_state(), mapping=mapping(),
            retained=[hex(p) for p in n.items(n.model,0xd0)], mask=n.i(0x1bfebd4),
            finished=n.u.mem_read(n.model+0x139,1)[0],
            result_cache=hex(n.q(target['score']+0x68)))
        e['snapshots'].append(row)
        return row

    def written(u, access, where, size, value, unused):
        p = next((p for p in taps if p <= where < p+0x80), None)
        owner = p or (target.get('score',0) if target.get('score',0) <= where < target.get('score',0)+0xd3 else target.get('gauge',0))
        e['native_writes'].append(dict(object='note' if p else 'score' if owner==target.get('score') else 'gauge',
            note=hex(p) if p else None, offset=hex(where-owner), size=size,
            before=int.from_bytes(u.mem_read(where,size),'little'), value=value,
            pc_elf_va=hex(u.reg_read(UC_ARM64_REG_PC)), phase=n.phase,
            E=effective() if target else None))

    def returned(u, pc, size, unused):
        if returns.get(pc):
            row = returns[pc].pop()
            row.update(after=score_state(), note_after=note_state()[str(row['note_time'])],
                       return_observed=True)

    def observe(u, pc, size, unused):
        nonlocal chart_pointer
        counts[hex(pc)] += 1
        if pc in {0x14f0a94,0x13e00b4,0x12c5070,0x160a3b8}:
            e['score_gauge_producers'].append(dict(pc_elf_va=hex(pc),lr_elf_va=hex(n.x(30)),
                x=[hex(n.x(i)) for i in range(8)],s0=n.s(0),phase=n.phase))
        if pc == 0x173b358:
            chart_pointer = n.x(0)
        elif pc == 0x18640d8:
            p = n.x(27)
            e['construction'].append(dict(parsed=hex(p), parsed_type=n.typename(p),
                parsed_time=n.i(p+0x18), parsed_input=n.u.mem_read(p+0xc,1)[0],
                raw_lane=n.i(n.q(p+0x20)+8), note=hex(n.x(0)),
                time_argument=n.x(1), position=hex(n.x(2)),
                timing_argument=hex(n.x(3)), initializer_elf_va=hex(n.x(8))))
        elif pc == 0x18640dc:
            p = n.x(25)
            taps.add(p)
            e['construction'][-1].update(initializer_return=n.x(0), returned_note=hex(p),
                runtime_type=n.typename(p), vtable_elf_va=hex(n.q(p)))
            u.hook_add(UC_HOOK_MEM_WRITE, written, begin=p+0xc, end=p+0x13)
        elif pc == 0x11ea120:
            e['count_producer'] = dict(chart=hex(n.x(0)), lr_elf_va=hex(n.x(30)),
                main_objects_before_bars=len(n.items(n.x(0),0x20)))
        elif pc == 0x173bf2c:
            e['count_producer']['returned_N'] = n.x(0)&0xffffffff
        elif pc == 0x1576b98 and n.x(19) in taps:
            e['index_insertions'].append(dict(note=hex(n.x(19)),group=n.i(n.x(19)+0x50),
                lo=n.x(23)&0xffffffff,hi=n.x(24)&0xffffffff))
        elif pc == 0x10fd8b8 and n.x(28) in taps:
            e['admissions'].append(dict(note=hex(n.x(28)),depth=n.x(23)&0xffffffff,
                limit=n.x(27),phase=n.phase))
        if not target:
            return
        if pc in {0xbe31a8,0xdda71c,0x194ff80,0xeec080,0x10a7550,0xf8056c,
                   0x10a7d50,0xc27d34,0x1600bb0}:
            e['decisive_calls'].append(dict(pc_elf_va=hex(pc),lr_elf_va=hex(n.x(30)),
                phase=n.phase,wall=n.now,E=effective(),x0=hex(n.x(0))))
        if pc in {0xeec4e0,0xeec4f0}:
            ps = n.items(n.x(19),0xb8)
            e['candidates'].append(dict(stage='before_sort' if pc==0xeec4e0 else 'after_sort',
                phase=n.phase,E=effective(),pointers=[hex(p) for p in ps],
                times=[n.i(p+0x18) for p in ps]))
        elif pc == 0x160ce28:
            row = dict(note=hex(n.x(1)),note_time=n.i(n.x(1)+0x18),generated_id=n.x(2),
                phase=n.phase,E=effective(),lr_elf_va=hex(n.x(30)))
            e['classifiers'].append(row)
            pending.append(row)
        elif pc == 0x160cec0:
            pending[-1].update(native_abs_error=n.x(9)&0xffffffff,native_E=n.x(4)&0xffffffff,
                               first_threshold=25,next_threshold=50,far_limit=100)
        elif pc == 0x160ce74:
            pending.pop()['consumes'] = n.x(23)&1
        elif pc == 0xeec56c:
            e['classifiers'][-1]['caller_return'] = n.x(0)&0xffffffff
        elif pc in {0x1730290,0x868e54} and n.x(1) in taps:
            row = dict(kind='accepted' if pc==0x1730290 else 'miss',pc_elf_va=hex(pc),
                lr_elf_va=hex(n.x(30)),note=hex(n.x(1)),note_time=n.i(n.x(1)+0x18),
                E=effective(),native_time_argument=n.x(4) if pc==0x1730290 else n.x(2),
                judgment_id=n.x(2) if pc==0x1730290 else None,
                generated_id=n.x(5) if pc==0x1730290 else None,phase=n.phase,
                before=score_state(),note_before=note_state()[str(n.i(n.x(1)+0x18))])
            e['recorders'].append(row)
            ret = n.x(30)
            returns.setdefault(ret,[]).append(row)
            if ret not in installed:
                u.hook_add(UC_HOOK_CODE,returned,begin=ret,end=ret)
                installed.add(ret)
        elif pc == 0x133fac8 and n.x(0)==target['gauge']:
            e['gauge_applications'].append(dict(phase=n.phase,E=effective(),
                lr_elf_va=hex(n.x(30)),H_before=n.f(n.x(0)+0x10),gain=n.s(0),damage=n.s(1)))
        elif pc in {0x173057c,0x1730584,0x868fdc}:
            e['combo_instructions'].append(dict(pc_elf_va=hex(pc),phase=n.phase,E=effective(),
                combo_before=n.i(target['score']+0x1c),max_before=n.i(target['score']+0x10),
                store_value=0 if pc==0x868fdc else n.x(8)&0xffffffff))
        elif pc == 0xf80a58 and n.x(26) in taps:
            e['expiry_guards'].append(dict(note=hex(n.x(26)),note_time=n.i(n.x(26)+0x18),
                native_E=n.x(2)&0xffffffff,native_cutoff=n.x(8)&0xffffffff,phase=n.phase))
        elif pc == 0x13073c4:
            sp = u.reg_read(UC_ARM64_REG_SP)
            e.setdefault('unprojections',[]).append(dict(phase=n.phase,
                point=[n.f(sp+0x28+4*i) for i in range(3)]))
        elif pc == 0xeec1cc:
            e.setdefault('selected_lanes',[]).append(dict(primary=n.x(0)&0xffffffff,secondary=n.x(0)>>32))
        elif pc == 0x1600c4c:
            e['snapshot_reconciliation'] = dict(N=n.i(target['score']+0xc),
                N_minus_PURE_FAR=n.x(11)&0xffffffff,recorded_LOST=n.x(13)&0xffffffff,
                selector_d1=n.x(12)&0xff)
        elif pc == 0x1600d80:
            e['snapshot_product'] = dict(score_state=hex(n.x(19)),result=hex(n.x(0)))
        elif pc == 0x131505c:
            e.setdefault('result_getter_denominators',[]).append(n.x(4)&0xffffffff)
        elif pc in {0x891684,0x89219c,0x8921b8}:
            rs=n.x(20)
            session=n.q(rs+0x2e8)
            result=n.q(session+0x18)
            e['save_gate'].append(dict(pc_elf_va=hex(pc),scene=hex(rs),
                gate_byte=n.u.mem_read(rs+0x2f8,1)[0],result_b0=n.u.mem_read(result+0xb0,1)[0],
                session_mode=n.i(session+0x20)))

    for pc in OBSERVE:
        n.u.hook_add(UC_HOOK_CODE,observe,begin=pc,end=pc)
    n.trace=[]; n.visual=[]; n.animationTrace=[]; n.downstream=[]
    n.env=n.alloc(8); n.now=1000
    entry(n); activate(n)
    scene, model = n.scene, n.model
    chart, score = n.q(model+0x28), n.q(model+0x38)
    notes = {n.i(p+0x18):p for p in taps}
    target.update(notes=notes,score=score,gauge=n.items(score,0xa0)[0])
    assert len(taps)==len(e['construction'])==6 and set(notes)==set(TIMES)
    assert set(taps)=={p for p in n.items(chart,0x20) if n.typename(p)=='12LogicTapNote'}
    assert n.sceneInitReturn==1 and n.q(scene+0x3e0)==model and n.q(scene+0x3e8)==chart==chart_pointer
    assert n.q(n.director+0x140)==scene and n.q(n.director+0x148)==0
    assert n.i(chart+0xb8)==n.i(score+0xc)==e['count_producer']['returned_N']==6
    assert n.i(chart+0xbc)==3620
    listener=n.state(model)['listener']
    assert listener['registered']==listener['enabled']==1 and listener['paused']==0
    for r in e['construction']:
        p=int(r['note'],16)
        assert r['returned_note']==r['note'] and r['initializer_return']==1
        assert r['parsed_type']=='10SimpleNote' and r['runtime_type']=='12LogicTapNote'
        assert r['parsed_time']==r['time_argument']==n.i(p+0x18)==n.i(p+0x1c)
        assert r['raw_lane']==3 and n.i(n.q(p+0x20)+0x10)==4 and n.i(p+0x50)==0
        assert n.u.mem_read(p+0x54,1)[0]==r['parsed_input']==1
    maps=n.maps(model)
    index={str(t):[k for k,ps in maps[0].items() if p in ps] for t,p in notes.items()}
    assert len(e['index_insertions'])==6 and all(index.values())
    assert n.q(target['gauge']+0xa8)==score and n.q(score+0x60)==chart
    rig=n.q(model+0x20); camera=n.q(rig+0x2a8)
    e.update(objects=dict(scene=hex(scene),model=hex(model),chart=hex(chart),
        timeline=hex(n.q(model+0x30)),score=hex(score),gauge=hex(target['gauge']),
        rig=hex(rig),camera=hex(camera)),listener=listener,
        chart=dict(N=n.i(chart+0xb8),end=n.i(chart+0xbc),index_by_time=index,
            main_objects=len(n.items(chart,0x20)),md5=n.string(chart+0xf8).decode(),
            timings=[[dict(pointer=hex(p),start=n.i(p+0x10),bpm=n.f(p+0x20),scale=n.f(p+0x28))
                for p in n.items(g)] for g in n.items(chart,0x38)]))
    assert e['chart']['md5']==hashlib.md5(config.fixture_text().encode()).hexdigest()
    for lo,hi in [(0xc,0x2f),(0x68,0x6f),(0xd0,0xd2)]:
        n.u.hook_add(UC_HOOK_MEM_WRITE,written,begin=score+lo,end=score+hi)
    for lo,hi in [(0x10,0x13),(0x1d,0x1d)]:
        n.u.hook_add(UC_HOOK_MEM_WRITE,written,begin=target['gauge']+lo,end=target['gauge']+hi)
    initial=snapshot('native_initialization')
    assert initial['score']['mode']==initial['score']['gauge_id']==0
    assert all(initial['score'][k]==0 for k in ['score','combo','max_combo','PURE','FAR','LOST','health'])
    assert all(not r['missed'] and not r['consumed'] for r in initial['notes'].values())
    e['gates']['construction']='pass'
    frame(n,n.now+1,'042 preroll')
    e['anchor']=frame(n,n.now+3001,'042 native music anchor')
    assert e['anchor']['E']==0
    world=[425.*(4-3.5),0.,0.]
    point,out=n.alloc(12),n.alloc(8)
    for i,v in enumerate(world):
        n.wf(point+4*i,v)
    n.call(0xbdbb70,camera,point,regs={8:out})
    xy=[n.f(out),n.f(n.director+0x184)-n.f(out+4)]
    assert all(math.isfinite(v) for v in xy)
    e['projection']=dict(world=world,jni_xy=xy,native_lane=4)

    def at(E):
        row=frame(n,n.now+E-effective(),'042 frame E'+str(E))
        assert row['E']==row['lastModelE']==E
        assert sum(x['pc']=='0x10a7550' for x in row['lifecycle'])==1
        return snapshot('frame_'+str(E))

    def contact(E,t,pid):
        at(E)
        pre=snapshot('before_DOWN_'+str(t))
        assert pre['notes'][str(t)]['active'] and not pre['notes'][str(t)]['consumed']
        n.phase='042 DOWN tap'+str(t)
        before_models=counts['0x10a7550']
        n.call(0xbe31a8,n.env,0,pid,987000+pid,fs=(*xy,.5))
        down=snapshot('after_DOWN_'+str(t))
        assert down['E']==E and counts['0x10a7550']==before_models
        assert len(down['mapping'])==len(down['retained'])==1 and down['mask'].bit_count()==1
        m=down['mapping'][0]
        assert m['android_id']==pid and m['slot']==m['touch_slot'] and down['retained']==[m['touch']]
        assert e['selected_lanes'][-1]==dict(primary=4,secondary=0)
        assert all(abs(a-b)<.5 for a,b in zip(e['unprojections'][-1]['point'],world))
        n.phase='042 UP tap'+str(t)
        n.call(0xdda71c,n.env,0,pid,988000+pid,fs=(*xy,0))
        up=snapshot('after_UP_'+str(t))
        assert up['mapping']==up['retained']==[] and up['mask']==0
        assert n.q(0x1beef90+m['slot']*8)==0
        assert up['score']==down['score'] and up['notes']==down['notes']
        e['inputs'].append(dict(note_time=t,E=E,android_id=pid,mapping=m,
            before=pre['score'],after=down['score'],cleanup=True))

    contact(1000,1000,42)
    contact(1500,1500,43)
    at(2000)
    contact(2060,2000,44)
    assert [r['judgment_id'] for r in e['recorders']]==[0,0,2]
    assert [r['note_time'] for r in e['recorders']]==[1000,1500,2000]
    assert [r.get('native_abs_error') for r in e['classifiers']]==[0,0,60]
    e['gates']['pure_far']='pass'
    at(2500)
    boundary=at(2600)
    assert boundary['score']['LOST']==0 and boundary['score']['combo']==boundary['score']['max_combo']==3
    assert not boundary['notes']['2500']['missed'] and boundary['notes']['2500']['active']
    broken=at(2601)
    assert broken['score']['LOST']==1 and broken['score']['combo']==0 and broken['score']['max_combo']==3
    assert broken['notes']['2500']['missed']==1
    assert [r['kind'] for r in e['recorders']]==['accepted']*3+['miss']
    assert e['recorders'][-1]['note_time']==2500 and e['recorders'][-1]['E']==2601
    assert all(not broken['notes'][str(t)]['consumed'] and not broken['notes'][str(t)]['missed'] for t in [3000,3500])
    e['post_break']=broken
    e['gates']['lost_combo_break']='pass'
    if recovery:
        contact(3000,3000,45)
        contact(3500,3500,46)
        after=at(3501)
        assert after['score']['combo']==2 and after['score']['max_combo']==3
    else:
        at(3000)
        b=at(3100);assert b['score']['LOST']==1
        b=at(3101);assert b['score']['LOST']==2
        at(3500)
        b=at(3600);assert b['score']['LOST']==2
        after=at(3601);assert after['score']['LOST']==3 and after['score']['combo']==0
    e['gates']['post_break']='pass'
    before=at(3620)
    assert before['finished']==0 and int(before['result_cache'],16)==0
    final=at(3621)
    r=n.q(score+0x68)
    assert final['finished']==1 and r and e['snapshot_product']==dict(score_state=hex(score),result=hex(r))
    n.result=r
    n.phase='042 read-only original result getters'
    result=dict(pointer=hex(r),stored_score=n.i(r+0x10),shining=n.i(r+0x14),PURE=n.i(r+0x18),
        FAR=n.i(r+0x1c),LOST=n.i(r+0x20),recorded_LOST=n.i(r+0x24),health=n.i(r+0x28),
        max_combo=n.i(r+0x60),mode=n.i(r+0x54),b0=n.u.mem_read(r+0xb0,1)[0],
        b1=n.u.mem_read(r+0xb1,1)[0],b3=n.u.mem_read(r+0xb3,1)[0],
        score_d1=n.u.mem_read(score+0xd1,1)[0],score_d2=n.u.mem_read(score+0xd2,1)[0],
        score=n.call(0x1315038,r),category=n.call(0x12a5574,r))
    e['native_result']=result
    assert result['recorded_LOST']==result['LOST']==final['score']['LOST']
    assert result['stored_score']==result['score']==final['score']['score']
    assert result['max_combo']==final['score']['max_combo']==3
    assert result['health']==math.floor(final['score']['health'])
    assert result['PURE']+result['FAR']+result['LOST']==6
    assert result['PURE']==(4 if recovery else 2) and result['FAR']==1
    assert counts['0xc27d34']==counts['0x1600bb0']==1
    assert all(counts[hex(pc)]==1 for pc in [0x14f0a94,0x13e00b4,0x12c5070,0x160a3b8])
    e['gates']['completion']='pass'
    assert final['mapping']==final['retained']==[] and final['mask']==0
    assert len(e['recorders'])==6 and all(r.get('return_observed') for r in e['recorders'])
    assert len({r['note'] for r in e['recorders']})==6
    assert all(r['lr_elf_va']==('0xf80b74' if r['kind']=='miss' else
        '0x160cfd0' if r['judgment_id']==2 else '0x160cf48') for r in e['recorders'])
    assert all(c['consumes']==c['caller_return']==1 for c in e['classifiers'])
    assert all(e['candidates'][i]['times']==sorted(e['candidates'][i]['times'])
        for i in range(1,len(e['candidates']),2))
    assert [x['combo_before'] for x in e['combo_instructions'] if x['pc_elf_va']=='0x868fdc']==([3] if recovery else [3,0,0])
    assert [x['store_value'] for x in e['combo_instructions'] if x['pc_elf_va']=='0x1730584']==[1,2,3]
    assert len(e['gauge_applications'])==6
    for r in e['recorders']:
        a,b=r['before'],r['after']
        if r['kind']=='miss':
            assert b['LOST']==a['LOST']+1 and b['combo']==0 and b['max_combo']==a['max_combo']
        else:
            assert b['combo']==a['combo']+1 and b['max_combo']==max(a['max_combo'],b['combo'])
        assert b['score']==(10000000*(2*b['PURE']+b['FAR'])//(2*b['N']))+b['shining']
    for p in taps:
        for offset in ['0xc','0xd']:
            assert sum(w['note']==hex(p) and w['offset']==offset and w['before']==0 and w['value']==1 for w in e['native_writes'])<=1
    e['gates']['cleanup']='pass'
    e['final_gameplay']=final
    n.resultSummary=dict(p=hex(n.result),score=result['score'],PURE=result['PURE'],FAR=result['FAR'],
        LOST=result['LOST'],health=result['health'],liveHealth=final['score']['health'],clear=result['category'])
    try:
        results_continuation(n,e)
    except Exception as exc:
        e['results_sqlite'].update(status='incomplete',failure=dict(type=type(exc).__name__,
            message=str(exc),line=traceback.extract_tb(exc.__traceback__)[-1].lineno),
            pc_elf_va=hex(n.u.reg_read(UC_ARM64_REG_PC)))
    e['snapshot_cache_observations']=dict(entries=counts['0x1600bb0'],
        product_stores=counts['0x1600d80'],
        repeated_snapshot_request='not_run; no second original owning request in tested ending chain',same_cache=n.q(score+0x68)==n.result,
        no_direct_snapshot_request=True)
    forbidden={0xe4e4dc,0xe2ea48,0x173b358,0x1862a14,0x1576aa4,0x10fd1c0,0x10a7550,
        0xeec024,0xf6b514,0x160ce28,0x965e28,0x1730290,0x868e54,0xf8056c,0x1600bb0,
        0xc27d34,0x147dee8,0x13552d4,0x12a5e60}
    assert not forbidden.intersection(n.host_calls) and not forbidden.intersection(n.hooks)
    eligibility=[x for x in n.soloTrace if x['pc']=='0xee2214']
    assert len(eligibility)==1 and int(eligibility[0]['x'][0],16)==1
    assert all(counts[hex(pc)]==1 for pc in [0xee197c,0xe4e4dc,0xe2ea48,0x1870de0,0x173b358,0x1862a14])
    assert counts['0xbe31a8']==counts['0xdda71c']==counts['0x194ff80']==(5 if recovery else 3)
    e.update(status='pass',native_call_counts=dict(counts),frames=n.trace,
        all_gameplay_handoffs_native=True,host_calls_elf_va=[hex(p) for p in n.host_calls],
        hook_inventory={hex(a):dict(name=n.imports.get(a,getattr(f,'__name__','')),entries=n.count[a]) for a,f in n.hooks.items()},
        boundary_registry={hex(a):v for a,v in n.boundaries.items()})


def run():
    evidence=dict(status='fail',fixture='native_mixed_judgment_recovery.aff',
        fixture_sha256=hashlib.sha256(config.fixture_text().encode()).hexdigest(),
        fresh_emulator_per_case=True,mixed_recovery={'status':'not_run'},
        mixed_no_recovery={'status':'not_run'},native_failures=[],pc_skips_elf_va=PC_SKIPS,
        new_boundaries=[],all_pure_reference='not_run; required paired histories suffice',
        services='Inherited ordinary catalog/profile/account/settings/platform/clock/JNI/ABI/resources/audio/GPU/allocator/autorelease; external synthetic AFF, wall clock, camera-projected JNI inputs')
    try:
        run_case(True,evidence['mixed_recovery'])
        run_case(False,evidence['mixed_no_recovery'])
        a,b=evidence['mixed_recovery'],evidence['mixed_no_recovery']
        def normalized(p):
            return dict(E=p['E'],wall=p['wall'],timeline=p['timeline'],score=p['score'],finished=p['finished'],
                notes={t:{k:v for k,v in r.items() if k!='pointer'} for t,r in p['notes'].items()},
                mask=p['mask'],mapping=p['mapping'],retained=p['retained'],
                director_frame=p['director_frame'],scene_stamp=p['scene_stamp'])
        assert normalized(a['post_break'])==normalized(b['post_break'])
        assert a['projection']==b['projection']
        assert all(a['chart'][k]==b['chart'][k] for k in ['N','end','md5','index_by_time','main_objects'])
        def prefix(rows):
            return [{k:r[k] for k in ['kind','note_time','E','judgment_id','before','after','lr_elf_va']} for r in rows[:4]]
        assert prefix(a['recorders'])==prefix(b['recorders'])
        evidence.update(status='pass',comparison=dict(equivalent_pre_break=True,
            identical_prefix_recorder_ledger=True,same_projection=True,
            recovery=a['native_result'],no_recovery=b['native_result'],
            recovery_live=a['final_gameplay']['score'],no_recovery_live=b['final_gameplay']['score']))
    except Exception as exc:
        for name in ['mixed_recovery','mixed_no_recovery']:
            if evidence[name]['status']=='running':
                evidence[name]['status']='fail'
        evidence['native_failures'].append(dict(type=type(exc).__name__,message=str(exc),
            line=traceback.extract_tb(exc.__traceback__)[-1].lineno))
    return evidence
