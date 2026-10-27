"""Native grouped-depth/JNI control, then one fresh negative-tempo transition."""
import collections
import math
import traceback
import config
from unicorn import UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm64_const import UC_ARM64_REG_PC, UC_ARM64_REG_SP
from solo_entry import setup, entry
from lifecycle import activate, frame
from boundaries import PC_SKIPS

TIMES = [0, 1000, 1100, 1199, 1200, 1201, 1300, 1499, 1500]
OBSERVE = {0x1930604, 0x1870de0, 0x8c847c, 0x173b358, 0x1862a14,
           0xbe2b98, 0x18640d8, 0x18640dc, 0x11ea120, 0xcf918c,
           0x1576aa4, 0x10fd1c0, 0x1017d80, 0xbe31a8, 0xdda71c,
           0x194ff80, 0xeec024, 0xf6b514, 0x160ce28, 0x965e28,
           0x1730290, 0x868e54, 0xf9a50c}


def run_case(reverse, evidence):
    config.configure(config.archive_path, 'reverse_scroll' if reverse else 'timing_group')
    n = setup(True)  # No snapshots; new Uc, ELF/global state, heap and native scene.
    n.prepare_runtime()
    n.observe |= OBSERVE
    taps, construction, timing_init, integrals, queries, index, admissions = set(), [], [], [], [], [], []
    writes, depth_updates, ground, lanes, candidates, accepts, refreshes = [], [], [], [], [], [], []
    lifetimes = []
    evidence.update(status='incomplete', construction=construction, native_timing_initializers=timing_init,
                    native_integrals=integrals, native_queries=queries, native_note_writes=writes,
                    native_index_producer=index, native_admission_predicates=admissions,
                    native_acceptances=accepts, native_group_lifetime_stores=lifetimes)
    integral = None
    timing_pending = None

    def signed(v):
        v &= 0xffffffff
        return v - 0x100000000 if v & 0x80000000 else v

    def effective():
        t = n.q(n.model + 0x30)
        return n.i(t + 0x20) - n.i(t + 0x28)

    def write(u, access, where, size, value, data):
        p = next(p for p in taps if p <= where < p + 0x80)
        writes.append({'note': hex(p), 'offset': hex(where-p), 'size': size, 'value': value,
                       'before': int.from_bytes(u.mem_read(where, size), 'little'),
                       'pc_elf_va': hex(u.reg_read(UC_ARM64_REG_PC)), 'phase': n.phase})

    def observe(u, a, size, data):
        nonlocal integral, timing_pending
        if a == 0x18640d8:
            p = n.x(27)
            construction.append({'parsed': hex(p), 'parsed_type': n.typename(p), 'time': n.i(p+0x18),
                'raw_lane': n.i(n.q(p+0x20)+8), 'note': hex(n.x(0)),
                'position': hex(n.x(2)), 'timing_argument': hex(n.x(3)), 'initializer_elf_va': hex(n.x(8))})
        elif a == 0x18640dc:
            p = n.x(25)
            construction[-1].update(initializer_return=n.x(0)&1, returned_note=hex(p),
                                     type=n.typename(p), vtable_elf_va=hex(n.q(p)))
            taps.add(p)
            for start, end in [(p+0x30,p+0x3f), (p+0x50,p+0x55), (p+0xc,p+0x13)]:
                u.hook_add(UC_HOOK_MEM_WRITE, write, begin=start, end=end)
        elif a == 0xbe2b98:
            timing_pending = {'pointer': hex(n.x(0)), 'time_argument': signed(n.x(1)),
                              'float_arguments': [n.s(i) for i in range(3)], 'lr_elf_va': hex(n.x(30))}
        elif a == 0xbe2bf8:
            p = n.x(19)
            timing_pending.update(returning_success=n.x(0)&1, raw_bpm=n.f(p+0x20), scale=n.f(p+0x28),
                                   scaled_bpm=n.f(p+0x18))
            timing_init.append(timing_pending)
            timing_pending = None
        elif a == 0xcf918c:
            E = signed(n.x(1))
            integral = {'phase': n.phase, 'chart': hex(n.x(0)), 'E': E, 'group': signed(n.x(2)),
                        'lr_elf_va': hex(n.x(30)), 'contributions': []} if E in set(TIMES + [t+120 for t in TIMES]) else None
        elif a == 0xcf91b8 and integral is not None:
            p = n.x(10)
            integral['contributions'].append({'timing': hex(p), 'start': n.i(p+0x10), 'end': n.i(p+0x14),
                'bound': signed(n.x(11)), 'scale': n.f(p+0x28)})
        elif a == 0xcf91fc and integral is not None:
            integral['result_f32'] = n.s(0)
            integrals.append(integral)
            integral = None
        elif a == 0x1576b98 and n.x(19) in taps:
            index.append({'note': hex(n.x(19)), 'group': n.i(n.x(19)+0x50),
                          'lo': signed(n.x(23)), 'hi': signed(n.x(24)), 'phase': n.phase})
        elif a == 0x10fd708:
            sp = u.reg_read(UC_ARM64_REG_SP)
            queries.append({'phase': n.phase, 'group': n.x(11), 'A_f32': n.s(8),
                            'lo': signed(n.x(26)), 'hi': n.i(sp+0x2c), 'back': n.s(9)})
        elif a == 0x10fd8b8 and n.x(28) in taps:
            admissions.append({'phase': n.phase, 'note': hex(n.x(28)),
                               'min_depth': signed(n.x(23)), 'limit': signed(n.x(27))})
        elif a == 0x1017d80 and n.x(0) in taps:
            depth_updates.append({'phase': n.phase, 'note': hex(n.x(0)), 'E_argument': signed(n.x(1)),
                                  'native_group_offset_f32': n.s(0)})
        elif a in (0x173c22c,0x173c24c):
            lifetimes.append({'pc_elf_va':hex(a),'descriptor':hex(n.x(12) if a==0x173c22c else n.x(8)),
                              'value':signed(n.x(11) if a==0x173c22c else n.x(9))})
        elif a == 0xeec080:
            refreshes.append({'phase': n.phase, 'E': effective(), 'wall': n.now, 'touch': hex(n.x(26))})
        elif a == 0x13073c4:
            sp = u.reg_read(UC_ARM64_REG_SP)
            ground.append({'phase': n.phase, 'point': [n.f(sp+0x28+4*i) for i in range(3)]})
        elif a == 0xeec1cc:
            lanes.append({'phase': n.phase, 'primary': n.x(0)&0xffffffff, 'secondary': n.x(0)>>32})
        elif a == 0xeec4f0:
            candidates.append({'phase': n.phase, 'notes': [hex(p) for p in n.items(n.x(19),0xb8)]})
        elif a == 0x965e28:
            p = n.x(0)
            accepts.append({'phase': n.phase, 'note': hex(p), 'group': n.i(p+0x50),
                            'E': n.x(1), 'generated_id': n.x(2)&0xffffffff,
                            'consumed_before': n.u.mem_read(p+0xd,1)[0], 'lr_elf_va': hex(n.x(30))})
    for a in [0x18640d8,0x18640dc,0xbe2b98,0xbe2bf8,0xcf918c,0xcf91b8,0xcf91fc,
              0x1576b98,0x10fd708,0x10fd8b8,0x1017d80,0x173c22c,0x173c24c,
              0xeec080,0x13073c4,0xeec1cc,0xeec4f0,0x965e28]:
        n.u.hook_add(UC_HOOK_CODE, observe, begin=a, end=a)
    n.phase = '029 complete original static initializer'
    n.call(0x1930604)  # Original .init_array producer recovered028; no host global repair.
    n.call(0x1054f24)
    n.trace=[]; n.visual=[]; n.animationTrace=[]; n.downstream=[]
    n.env=n.alloc(8); n.now=1000
    entry(n)
    activate(n)
    scene, model = n.scene, n.model
    chart, score = n.q(model+0x28), n.q(model+0x38)
    evidence['objects']={'scene':hex(scene),'model':hex(model),'chart':hex(chart),'score':hex(score)}
    gauge = n.items(score,0xa0)[0]
    native_taps = {p for p in n.items(chart,0x20) if n.typename(p)=='12LogicTapNote'}
    assert taps == native_taps and len(taps)==len(construction)==2
    by_group = {n.i(p+0x50):p for p in taps}
    assert set(by_group)=={0,1} and n.i(chart+0xb8)==2 and n.i(chart+0xbc)==1620
    assert all(n.i(p+0x18)==n.i(p+0x1c)==1500 and n.q(p)==0x1af4278 for p in taps)
    assert [n.i(n.q(by_group[g]+0x20)+0x10) for g in [0,1]]==[5,2]
    assert all(c['initializer_return']==1 and c['note']==c['returned_note'] and c['type']=='12LogicTapNote' for c in construction)
    assert sorted(c['raw_lane'] for c in construction)==[1,4]
    timing_lists, descriptors = n.items(chart,0x38), n.items(chart,0x50)
    assert len(set(timing_lists))==len(set(descriptors))==2
    timings = [[{'pointer':hex(p),'start':n.i(p+0x10),'end':n.i(p+0x14),
                 'scaled_bpm':n.f(p+0x18),'raw_bpm':n.f(p+0x20),'scale':n.f(p+0x28)}
                for p in n.items(tl)] for tl in timing_lists]
    assert [len(t) for t in timings]==[1,2 if reverse else 1]
    assert timings[0][0]['raw_bpm']==120 and timings[1][0]['raw_bpm']==60
    assert all(t[0]['start']==-2147483648 and t[-1]['end']==1001620 for t in timings)
    if reverse:
        assert timings[1][0]['end']==timings[1][1]['start']==1200
        assert timings[1][1]['raw_bpm']==-60 and timings[1][1]['scale']==-timings[1][0]['scale']
    assert len(timing_init)==sum(map(len,timings)) and all(t['returning_success']==1 for t in timing_init)
    assert all(any(t['pointer']==hex(p) for t in timing_init) for tl in timing_lists for p in n.items(tl))
    assert [n.i(g+4) for g in descriptors]==[2147483647,2700]
    assert all(any(s['descriptor']==hex(p) and s['value']==n.i(p+4) for s in lifetimes) for p in descriptors)
    for c in construction:
        p=int(c['note'],16);g=n.i(p+0x50)
        assert int(c['timing_argument'],16)==n.q(p+0x48) in n.items(timing_lists[g])
    evidence['timings']=timings
    maps = n.maps(model)
    index_membership = {str(g):{'header':hex(n.items(model,0x88)[g]),
                              'keys':[k for k,ps in maps[g].items() if p in ps]} for g,p in by_group.items()}
    assert len(index)==2 and all(index_membership[str(g)]['keys']==list(range(r['lo'],r['hi']+1))
           for g,p in by_group.items() for r in index if r['note']==hex(p))
    assert all(index_membership[str(g)]['keys'] for g in by_group)
    assert all(p not in ps for g,p in by_group.items() for other,mp in enumerate(maps) if other!=g for ps in mp.values())
    listener = n.state(model)['listener']
    assert n.sceneInitReturn==1 and listener['registered']==listener['enabled']==1 and listener['paused']==0
    assert n.q(scene+0x3e0)==model and n.q(scene+0x3e8)==chart
    assert n.q(n.director+0x140)==scene and n.q(n.director+0x148)==0
    camera = n.q(n.q(model+0x20)+0x2a8)

    def score_state():
        return {'PURE':n.i(score+0x24),'shining':n.i(score+0x20),'FAR':n.i(score+0x28),
                'LOST':n.i(score+0x2c),'score':n.i(score+0x14),'health':n.f(gauge+0x10)}

    def snapshot(label):
        return {'label':label,'E':effective(),'wall':n.now,
                'notes':[{'pointer':hex(p),'group':g,'lane':n.i(n.q(p+0x20)+0x10),
                          'time':n.i(p+0x18),'position':hex(n.q(p+0x20)),
                          'selected_timing':hex(n.q(p+0x48)),
                          'current_depth':[n.i(p+0x30),n.i(p+0x34)],
                          'precomputed_depth':[n.i(p+0x38),n.i(p+0x3c)],
                          'active':p in n.items(model,0xa0),'input_enabled':n.u.mem_read(p+0x54,1)[0],
                          'missed':n.u.mem_read(p+0xc,1)[0],'consumed':n.u.mem_read(p+0xd,1)[0],
                          'accepted_id':n.i(p+0x10)} for g,p in sorted(by_group.items())],
                'groups':[{'index':g,'descriptor':hex(p),'active':n.u.mem_read(p,1)[0],
                           'end':n.i(p+4),'timing_list':hex(timing_lists[g])} for g,p in enumerate(descriptors)],
                'retained':[hex(p) for p in n.items(model,0xd0)],'map_size':n.q(0x1bf1a98),
                'engine_mask':n.i(0x1bfebd4),'score':score_state()}

    startup = snapshot('after loading activation')
    frame(n,n.now+1,'group preroll')
    anchor=frame(n,n.now+3001,'group native music anchor')
    assert anchor['E']==0
    states=[]
    evidence.update(startup=startup, states=states, index_membership=index_membership)
    for E in TIMES:
        label='sample_'+str(E)
        fr=frame(n,n.now+E-effective(),label)
        assert fr['E']==fr['lastModelE']==E and sum(e['pc']=='0x10a7550' for e in fr['lifecycle'])==1
        row=snapshot(label)
        row['native_queries']=[q for q in queries if q['phase']==label]
        row['native_integrals']=[i for i in integrals if i['phase']==label]
        assert len(row['native_queries'])==2 and {q['group'] for q in row['native_queries']}=={0,1}
        assert all(note['active'] and note['input_enabled']==1 and note['consumed']==note['missed']==0 for note in row['notes'])
        assert all(g['active']==1 for g in row['groups'])
        for note in row['notes']:
            q=next(q for q in row['native_queries'] if q['group']==note['group'])
            note['index_keys_in_query']=[k for k in index_membership[str(note['group'])]['keys'] if q['lo']<=k<=q['hi']]
            # Retention is independently checked above; an existing active note need not be readmitted.
            assert any(i['group']==note['group'] and i['E']==E for i in row['native_integrals'])
        states.append(row)
    assert all(note['current_depth']==[0,0] for note in states[-1]['notes'])
    assert states[1]['notes'][0]['current_depth']!=states[1]['notes'][1]['current_depth']
    grouped_depth={s['E']:s['notes'][1]['current_depth'][0] for s in states}
    if reverse:
        assert grouped_depth[1000]<grouped_depth[1100]<grouped_depth[1199]<grouped_depth[1200]
        assert grouped_depth[1200]>grouped_depth[1201]>grouped_depth[1300]>grouped_depth[1499]>grouped_depth[1500]
    else:
        assert all(a<b for a,b in zip(grouped_depth.values(),list(grouped_depth.values())[1:]))

    contacts=[]
    evidence['contacts']=contacts
    for g,p in sorted(by_group.items()):
        lane=n.i(n.q(p+0x20)+0x10)
        world=[425.0*(lane-3.5),0.0,0.0]  # Native selector's separated ordinary lane centers; not note depth.
        point,out=n.alloc(12),n.alloc(8)
        for i,v in enumerate(world): n.wf(point+4*i,v)
        n.call(0xbdbb70,camera,point,regs={8:out})
        xy=[n.f(out),n.f(n.director+0x184)-n.f(out+4)]
        assert all(math.isfinite(v) for v in xy)
        pid=42+g
        n.phase='down_group_'+str(g)
        n.call(0xbe31a8,n.env,0,pid,987000+pid,fs=(*xy,.5))
        down=snapshot(n.phase)
        assert down['E']==1500 and down['map_size']==len(down['retained'])==down['engine_mask'].bit_count()==1
        touch=n.items(model,0xd0)[0];slot=n.i(touch+0xc);generated=n.i(touch+0x34)
        assert n.q(0x1beef90+slot*8)==touch
        assert candidates[-1]['notes']==[hex(p)] and lanes[-1]['primary']==lane and lanes[-1]['secondary']==0
        assert all(abs(x-y)<.5 for x,y in zip(ground[-1]['point'],world))
        assert n.u.mem_read(p+0xd,1)[0]==1 and n.i(p+0x10)==generated
        assert score_state()['PURE']==score_state()['shining']==g+1
        n.phase='up_group_'+str(g)
        n.call(0xdda71c,n.env,0,pid,988000+pid,fs=(*xy,0))
        up=snapshot(n.phase)
        assert up['map_size']==up['engine_mask']==n.q(0x1beef90+slot*8)==0 and not up['retained']
        assert up['score']==down['score'] and up['notes']==down['notes']
        contacts.append({'group':g,'note':hex(p),'android_id':pid,'slot':slot,'touch':hex(touch),
                         'generated_id':generated,'world_target':world,'jni_xy':xy,'down':down,'up':up})
    final=snapshot('after both native UPs')
    assert final['score']['PURE']==final['score']['shining']==2 and final['score']['FAR']==final['score']['LOST']==0
    assert final['score']['score']==10000002 and math.isclose(final['score']['health'],80.4000015258789,abs_tol=1e-6)
    assert len(accepts)==2 and {a['note'] for a in accepts}=={hex(p) for p in taps}
    assert all(a['E']==1500 and a['consumed_before']==0 and a['lr_elf_va']=='0x17302ec' for a in accepts)
    assert len(refreshes)==2 and all(r['E']==1500 for r in refreshes)
    consumption=[w for w in writes if w['offset']=='0xd']
    assert len(consumption)==2 and all(w['before']==0 and w['value']==w['size']==1 and w['pc_elf_va']=='0x965e68' for w in consumption)
    for p in taps:
        assert any(w['note']==hex(p) and w['offset']=='0x50' and w['pc_elf_va']=='0x18640ec' and w['value']==n.i(p+0x50) for w in writes)
        assert any(w['note']==hex(p) and w['offset']=='0x38' and w['pc_elf_va']=='0x173c0d4' for w in writes)
        assert any(w['note']==hex(p) and w['offset']=='0x30' and w['pc_elf_va']=='0x1017d94' for w in writes)
        assert any(a['note']==hex(p) and a['min_depth']<a['limit']==300 for a in admissions)
    counts=collections.Counter(e['pc'] for e in n.events)
    for a in [0xee197c,0xee29a8,0xee29e8,0xe4e4dc,0xe2ea48,0x1930604,0x1870de0,0x8c847c,0x173b358,0x1862a14,0x11ea120]:
        assert counts[hex(a)]==1,(hex(a),counts[hex(a)])
    for a in [0xbe31a8,0xdda71c,0x194ff80,0xeec024,0xf6b514,0x160ce28,0x965e28,0x1730290,0xf9a50c]:
        assert counts[hex(a)]==2,(hex(a),counts[hex(a)])
    assert counts['0xdd0f90']==counts['0x868e54']==counts['0xc27d34']==0 and n.q(score+0x68)==0
    assert any(e['pc']=='0xee2214' and int(e['x'][0],16)==1 for e in n.soloTrace)
    assert n.u.mem_read(n.menu+0x490,1)[0]==1
    constructor=next(e for e in n.menuTrace if e['pc']=='0xe4e4dc')
    assert constructor['lr']=='0xee29ec' and int(constructor['x'][0],16)==scene
    forbidden={0xe4e4dc,0xe2ea48,0x10a7550,0x173b358,0x1862a14,0xbe2b98,0xcf918c,0x1576aa4,
               0x10fd1c0,0x1017d80,0xeec024,0xf6b514,0x160ce28,0x965e28,0x1730290,0x868e54}
    assert not forbidden.intersection(n.host_calls) and not forbidden.intersection(n.hooks)
    recorders=[e for e in n.events if e['pc']=='0x1730290']
    for r,a in zip(recorders,accepts):
        assert r['x'][1]==a['note'] and int(r['x'][4],16)==1500
        assert int(r['x'][5],16)==a['generated_id'] and r['lr']=='0x160cf48'
    assert n.u.mem_read(n.dispatcher+0x124,1)[0]==1
    return {'status':'pass','fixture':'native_reverse_scroll.aff' if reverse else 'native_timing_group.aff',
            'objects':{'scene':hex(scene),'model':hex(model),'chart':hex(chart),'camera':hex(camera),'score':hex(score)},
            'initializer_return':n.sceneInitReturn,'constructor_lr_elf_va':constructor['lr'],'listener':listener,
            'construction':construction,'N':n.i(chart+0xb8),'chart_end':n.i(chart+0xbc),
            'requested_speed':n.f(chart+0xf0),'normalized_speed':n.f(chart+0xf4),
            'native_timing_initializers':timing_init,'timings':timings,'startup':startup,
            'native_group_lifetime_stores':lifetimes,
            'native_index_producer':index,'index_membership':index_membership,'native_admission_predicates':admissions,
            'anchor':anchor,'states':states,'native_integrals':integrals,'native_depth_updates':depth_updates,
            'native_queries':queries,'native_note_writes':writes,'contacts':contacts,'native_input_time_refreshes':refreshes,
            'native_ground':ground,'native_lanes':lanes,'native_candidates':candidates,'native_acceptances':accepts,
            'recorders':[e for e in n.events if e['pc'] in ('0x1730290','0x868e54')],
            'native_call_counts':{hex(a):counts[hex(a)] for a in OBSERVE|{0xee197c,0xee29a8,0xee29e8,0xe4e4dc,0xe2ea48,0xc27d34}},
            'final':final,'checks':{'native_group_timing_depth_index_and_admission':True,'native_JNI_consumption':True,
                                   'native_cleanup':True,'no_host_timing_depth_index_or_note_repair':True},
            'final_director':{'running':hex(n.q(n.director+0x140)),'pending':n.q(n.director+0x148),
                              'dispatcher_enabled':n.u.mem_read(n.dispatcher+0x124,1)[0]}}


def run():
    control,reverse={},{}
    try:
        control=run_case(False,control)  # Assertions finish before the reverse runtime is created.
        reverse=run_case(True,reverse)
        assert control['final']['score']==reverse['final']['score']
        assert [{k:v for k,v in t.items() if k!='pointer'} for t in control['timings'][0]]==[
                {k:v for k,v in t.items() if k!='pointer'} for t in reverse['timings'][0]]
    except Exception as exc:
        return {'status':'fail','grouped_control':control,'reverse_scroll':reverse,
                'native_failures':[{'type':type(exc).__name__,'message':str(exc),
                                    'line':traceback.extract_tb(exc.__traceback__)[-1].lineno}], 'pc_skips_elf_va':PC_SKIPS}
    return {'status':'pass','fixture':'independent-group-control-and-negative-tempo-transition',
            'fresh_emulator_per_case':True,'grouped_control':control,'reverse_scroll':reverse,
            'comparison':{'equal_native_N_and_score_gauge':True,'native_negative_tempo_depth_turn_and_JNI':True},
            'supplied_services':'Unchanged024-028 platform/ABI/catalog/settings/profile/resources/clock/JNI input/audio/GPU; original1930604 static initializer; no new service or gameplay skip',
            'pc_skips_elf_va':PC_SKIPS,'native_failures':[],
            'endpoint':'E1500 after native UPs; no completion/results/SQLite replay'}
