"""Expedition030 blocked native camera-construction diagnostic; never claims reset coverage."""
import collections
import hashlib
import traceback
import config
from unicorn import UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm64_const import UC_ARM64_REG_PC
from solo_entry import setup, entry
from lifecycle import activate, frame
from boundaries import PC_SKIPS

OBSERVE = {0x1930604, 0x1870de0, 0x138f560, 0x173b358, 0x1862a14,
           0x1651e88, 0x81d3e4, 0x1576aa4, 0x1393474, 0x851514,
           0xf8056c, 0x192b5c8, 0x10a2b94, 0x13a7938, 0xf1b510,
           0x16c5bc8, 0x121253c, 0xc7820c, 0xb3dc38,
           0x13d3f44, 0xd630b8, 0x9effe0, 0x12a5a80,
           0xb0bd74, 0x15beb20, 0xf14f9c, 0xbe31a8, 0xdda71c,
           0x160ce28, 0x965e28, 0x1730290, 0x868e54}


def run():
    evidence = {'status': 'fail', 'fixture': 'native_camera_overlap.aff',
                'reset_fixture': 'native_camera_reset.aff (candidate; not executed)',
                'gates': {'overlap_control': 'incomplete', 'overlap_with_reset': 'not_run'},
                'pc_skips_elf_va': PC_SKIPS, 'native_failures': []}
    try:
        return investigate(evidence)
    except Exception as exc:
        evidence['native_failures'].append({'type': type(exc).__name__, 'message': str(exc),
            'line': traceback.extract_tb(exc.__traceback__)[-1].lineno})
        return evidence


def investigate(evidence):
    config.configure(config.archive_path, 'camera_reset')
    n = setup(True)
    n.prepare_runtime()
    n.observe |= OBSERVE
    parsed, decisions, property_writes, scheduling, runtime_actions = [], [], [], [], []
    evidence.update(parsed_camera_controls=parsed, builder_decisions=decisions,
                    native_property_writes=property_writes, native_scheduling=scheduling,
                    native_runAction_entries=runtime_actions)
    pending = None
    chart_pointer = None

    def written(u, access, where, size, value, data):
        property_writes.append({'address': hex(where), 'size': size, 'value': value,
                               'pc_elf_va': hex(u.reg_read(UC_ARM64_REG_PC)), 'phase': n.phase})

    def observe(u, a, size, data):
        nonlocal pending, chart_pointer
        if a == 0x173b358:
            chart_pointer = n.x(0)
            u.hook_add(UC_HOOK_MEM_WRITE, written, begin=chart_pointer+0x110, end=chart_pointer+0x110)
        elif a == 0x1863e4c:
            p = n.x(0)  # Original dynamic_cast accepted a parsed CameraControl.
            parsed.append({'pointer': hex(p), 'type': n.typename(p), 'vtable_elf_va': hex(n.q(p)),
                           'time': n.i(p+0x18), 'values': [n.f(p+o) for o in range(0x1c,0x34,4)],
                           'easing': n.string(p+0x38).decode(), 'duration': n.i(p+0x50)})
        elif a == 0x1863e58:
            c = n.x(9)
            pending = {'parsed': hex(n.x(22)), 'chart': hex(c), 'song_id': n.string(n.q(c+0x10)).decode(),
                       'chart_110': n.u.mem_read(c+0x110,1)[0], 'native_branch_byte': n.x(8)&0xff,
                       'predicate_elf_va': '0x1863e58'}
        elif a == 0x186453c:
            pending.update(song_exception_comparison=n.x(19)&0xffffffff,
                           rejection_branch_elf_va=hex(a))
        elif a == 0x1863d60 and pending is not None:
            pending['observed_next_elf_va'] = hex(a)
            decisions.append(pending)
            pending = None
        elif a in (0x13d3f44,0xd630b8,0x9effe0) and n.phase.startswith('camera_sample_'):
            scheduling.append({'pc_elf_va':hex(a),'phase':n.phase,'wall':n.now,
                               'dt_f32':n.s(0),'lr_elf_va':hex(n.x(30))})
        elif a == 0xc7820c and n.phase.startswith('camera_sample_'):
            runtime_actions.append({'target':hex(n.x(0)),'action':hex(n.x(1)),
                                    'type':n.typename(n.x(1)),'phase':n.phase})
    for a in [0x173b358,0x1863e4c,0x1863e58,0x186453c,0x1863d60,
              0x13d3f44,0xd630b8,0x9effe0,0xc7820c]:
        n.u.hook_add(UC_HOOK_CODE, observe, begin=a, end=a)
    n.phase='030 complete original static initializer'
    n.call(0x1930604)
    n.call(0x1054f24)
    n.trace=[]; n.visual=[]; n.animationTrace=[]; n.downstream=[]
    n.env=n.alloc(8); n.now=1000
    entry(n)
    activate(n)
    scene,model=n.scene,n.model
    chart=n.q(model+0x28); rig=n.q(model+0x20)
    cameras=[n.q(rig+0x2a8),n.q(rig+0x2b0)]
    evidence['objects']={'scene':hex(scene),'model':hex(model),'chart':hex(chart),'rig':hex(rig),
                         'primary':hex(cameras[0]),'secondary':hex(cameras[1]),
                         'scheduler':hex(n.scheduler),'manager':hex(n.manager)}
    assert chart==chart_pointer and n.sceneInitReturn==1
    assert n.q(scene+0x3e0)==model and n.q(scene+0x3e8)==chart
    assert n.q(n.director+0x140)==scene and n.q(n.director+0x148)==0
    listener=n.state(model)['listener']
    assert listener['registered']==listener['enabled']==1 and listener['paused']==0
    assert n.typename(rig)=='16CameraController' and len(set(cameras))==2
    assert all(n.typename(p)=='N7cocos2d6CameraE' for p in cameras)
    assert all(n.q(p+0x1b0)==n.manager for p in [rig]+cameras)
    objects=n.items(chart,0x20)
    camera_controls=[p for p in objects if n.typename(p)=='18LogicCameraControl']
    taps=[p for p in objects if n.typename(p)=='12LogicTapNote']
    assert len(parsed)==len(decisions)==2 and len(taps)==1
    assert [p['time'] for p in parsed]==[600,900]
    assert [p['easing'] for p in parsed]==['l','qi'] and all(p['duration']==2000 for p in parsed)
    assert [p['values'] for p in parsed]==[[600.,0.,0.,0.,0.,0.],[0.,0.,0.,0.,0.,15.]]
    assert all(d['chart_110']==d['native_branch_byte']==d['song_exception_comparison']==0 and
               d['song_id']=='sayonarahatsukoi' and d['observed_next_elf_va']=='0x1863d60' for d in decisions)
    assert any(w['pc_elf_va']=='0x173c3cc' and w['value']==0 and w['size']==1 for w in property_writes)
    assert not camera_controls, 'Different native construction outcome; reassess this blocked diagnostic'
    tap=taps[0]
    assert n.i(tap+0x18)==n.i(tap+0x1c)==1500 and n.i(n.q(tap+0x20)+0x10)==4
    assert n.i(chart+0xb8)==1 and n.i(chart+0xbc)==1620
    assert any(tap in ps for mp in n.maps(model) for ps in mp.values())
    digest=n.string(chart+0xf8).decode()
    assert digest==hashlib.md5(config.fixture_text().encode()).hexdigest()
    evidence.update(initializer_return=n.sceneInitReturn,listener=listener,whole_chart_md5=digest,
                    chart_110=n.u.mem_read(chart+0x110,1)[0],native_N=n.i(chart+0xb8),chart_end=n.i(chart+0xbc),
                    runtime_camera_controls=[hex(p) for p in camera_controls],
                    native_tap={'pointer':hex(tap),'lane':4,'time':1500})

    def effective():
        t=n.q(model+0x30)
        return n.i(t+0x20)-n.i(t+0x28)

    def state(label):
        return {'label':label,'E':effective(),'wall':n.now,'rig_latch':n.u.mem_read(rig+0x2a0,1)[0],
                'home':[n.f(rig+0x2c4+4*i) for i in range(3)],
                'look_at':[n.f(rig+0x2b8+4*i) for i in range(3)],
                'cameras':[{'pointer':hex(p),'position':[n.f(p+o) for o in [0x38,0x3c,0x40]],
                            'euler':[n.f(p+o) for o in [0xc,0x10,0x14]],
                            'quaternion':[n.f(p+0x1c+4*i) for i in range(4)],
                            'node_flags':n.i(p+0x130),'mask':int.from_bytes(n.u.mem_read(p+0x412,2),'little'),
                            'cached_view':[n.f(p+0x2e8+4*i) for i in range(16)],
                            'cached_PV':[n.f(p+0x368+4*i) for i in range(16)]} for p in cameras],
                'action_manager':n.action_state(),'tap_active':tap in n.items(model,0xa0)}
    evidence['states']=[state('native scene activated')]
    frame(n,n.now+1,'camera preroll')
    anchor=frame(n,n.now+3001,'camera native music anchor')
    assert anchor['E']==0
    evidence['anchor']=anchor
    for E in [500,600,601,900,901]:
        label='camera_sample_'+str(E)
        row=frame(n,n.now+E-effective(),label)
        assert row['E']==row['lastModelE']==E
        evidence['states'].append(state(label))
        calls=[s for s in scheduling if s['phase']==label]
        assert [s['pc_elf_va'] for s in calls]==['0x13d3f44','0xd630b8','0x9effe0']
        assert all(s['dt_f32']==calls[0]['dt_f32'] for s in calls)
    assert all(not any(int(r['target'],16) in [rig]+cameras for r in s['action_manager']) for s in evidence['states'])
    assert not runtime_actions
    counts=collections.Counter(e['pc'] for e in n.events)
    for a in [0x1870de0,0x173b358,0x1862a14,0xe2ea48,0xee197c,0xee29a8,0xee29e8]:
        assert counts[hex(a)]==1
    assert counts['0x138f560']==2
    for a in [0x1651e88,0x81d3e4,0x192b5c8,0x10a2b94,0x13a7938,0xb0bd74,0xbe31a8,0x965e28,0x1730290,0x868e54]:
        assert counts[hex(a)]==0,(hex(a),counts[hex(a)])
    assert n.u.mem_read(n.menu+0x490,1)[0]==1
    assert any(e['pc']=='0xee2214' and int(e['x'][0],16)==1 for e in n.soloTrace)
    forbidden={0x1651e88,0x81d3e4,0x192b5c8,0x10a2b94,0x13a7938,0xb0bd74,0xf14f9c,
               0x12a5a80,0x10a7550,0xe2ea48,0xeec024,0x965e28,0x1730290}
    assert not forbidden.intersection(n.host_calls) and not forbidden.intersection(n.hooks)
    evidence.update(native_call_counts={hex(a):counts[hex(a)] for a in OBSERVE|{0xee197c,0xee29a8,0xee29e8,0xe2ea48}},
        gates={'overlap_control':'blocked_before_runtime_camera_construction','overlap_with_reset':'not_run'},
        blocker={'predicate_elf_va':'0x186453c','edge':'0x186453c -> 0x1863d60',
                 'contract':'Camera record retained only if chart+0x110 != 0 or Song ID equals designant',
                 'observed':'chart+0x110=0, Song=sayonarahatsukoi, exception result=0; both records omitted',
                 'upstream':'Original173c3cc writes0 after native digest/named-song property selection',
                 'minimum_remedy':'Separately justify an original camera-permitted catalog/chart context and its ordinary eligibility; never assign chart+0x110 or fabricate a digest'},
        native_failures=[{'type':'NativeCameraConstructionExcluded','message':'Original builder omitted both parsed camera controls; overlap gate failed and reset/JNI stages were not run'}],
        scientific_checks={'native_parser_and_builder_rejection_observed':True,'native_scene_and_Scheduler_execute':True,
                           'no_camera_action_or_judgment_state_repair':True},
        supplied_services='Unchanged024-029 catalog/settings/profile/platform/ABI/resource/clock/audio/GPU services; synthetic AFF; original1930604; no new service/skip',
        endpoint={'E':effective(),'running_scene':hex(n.q(n.director+0x140)),
                  'pending':n.q(n.director+0x148),'dispatcher_enabled':n.u.mem_read(n.dispatcher+0x124,1)[0],
                  'JNI_projection':'not_attempted','reset':'not_executed'})
    return evidence  # A scientifically characterized exclusion is still a failed camera regression.
