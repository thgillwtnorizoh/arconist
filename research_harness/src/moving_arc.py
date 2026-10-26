"""Native moving/crossing arc gates. Host chooses JNI inputs, never arc/owner state."""
import collections
import math
import struct
import traceback
import config
from unicorn import UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm64_const import UC_ARM64_REG_PC, UC_ARM64_REG_SP
from solo_entry import setup, entry
from lifecycle import activate, frame
from arc_tap_services import install as install_obj_abi
from jni_arrays import InputArrays
from boundaries import PC_SKIPS

OBSERVE = {0x1930604, 0x1870de0, 0xc2cb1c, 0x924b50, 0x173b358, 0x1862a14,
           0x178f7fc, 0xc664f8, 0x17cb97c, 0xd93594, 0x1925084, 0x1576aa4,
           0x19f3d4c, 0x14858d4, 0xc98490, 0x927384, 0xc98648,
           0x15dfe2c, 0x15a90c4, 0x13db7a0, 0x19f439c,
           0x1730290, 0x868e54, 0xbe31a8, 0x1706960, 0x160b710, 0x10e7008, 0xdda71c, 0xf9a50c}
SPATIAL_GLOBALS = {0x1c0094c: 180, 0x1bef2e0: 100, 0x1bee968: 250, 0x1bf6c9c: 550}


def run_case(crossing):
    # Reverify the same external archive and select only its supplied chart boundary.
    config.configure(config.archive_path, 'crossing_arc' if crossing else 'moving_arc')
    n = setup(True)
    abi = install_obj_abi(n)  # Reuse025's bounded libc services unchanged.
    n.prepare_runtime()
    n.observe |= OBSERVE
    parsed, factories, samples, spatial, proximity, claims, releases = [], [], [], [], [], [], []
    native_arcs, return_hooks = set(), set()

    def effective():
        t = n.q(n.model + 0x30)
        return n.i(t + 0x20) - n.i(t + 0x28)

    def factory_return(u, address, size, data):
        p = n.x(0)
        native_arcs.add(p)
        factories[-1].update(pointer=hex(p), type=n.typename(p), vtable_elf_va=hex(n.q(p)),
                             mode=n.i(p + 0xa4), curve=n.i(p + 0x15c),
                             color=hex(n.q(p + 0xb0)), mapped_color=n.i(n.q(p + 0xb0) + 0x18))

    def observe(u, address, size, data):
        if address == 0x924c18:
            p = n.x(19)
            parsed.append({'time': [n.i(p + 0x18), n.i(p + 0x1c)],
                           'x_endpoints': [n.f(p + 0x20), n.f(p + 0x24)],
                           'y_endpoints': [n.f(p + 0x40), n.f(p + 0x44)],
                           'curve': n.string(p + 0x28).decode(), 'color': n.i(p + 0x48), 'mode': n.i(p + 0x68)})
        elif address == 0x178f7fc:
            lr = n.x(30)
            factories.append({'caller_return_elf_va': hex(lr), 'time': [n.x(0), n.x(1)],
                              'x_endpoints': [n.f(n.x(2) + 0x14), n.f(n.x(3) + 0x14)]})
            if lr not in return_hooks:
                return_hooks.add(lr)
                u.hook_add(UC_HOOK_CODE, factory_return, begin=lr, end=lr)
        elif address == 0x969190 and n.x(0) - 0xe8 in native_arcs:
            samples.append({'arc': hex(n.x(0) - 0xe8), 'sample': [n.f(n.x(1) + 4*i) for i in range(3)],
                            'caller_return_elf_va': hex(n.x(30))})
        elif address == 0x927384 and n.phase.startswith(('position_', 'follow_')):
            spatial.append({'phase': n.phase, 'point': [n.f(n.x(1) + 4*i) for i in range(3)],
                            'target': [n.f(n.x(2) + 4*i) for i in range(2)]})
        elif address == 0xc98648 and spatial and 'accepted' not in spatial[-1]:
            spatial[-1]['accepted'] = n.x(0) & 1
        elif address == 0x19f439c:
            proximity.append({'phase': n.phase, 'arc_a': hex(n.x(22)), 'arc_b': hex(n.x(23)),
                              'distance': n.s(0), 'threshold': n.s(1)})
        elif address == 0x15a90c4:
            claims.append({'phase': n.phase, 'color': hex(n.x(0)), 'id': n.x(1) & 0xffffffff,
                           'E': n.x(2), 'interval': n.x(3)})
        elif address == 0x15dfe60:
            claims[-1]['accepted'] = n.x(0) & 1
        elif address == 0x13db7a0:
            p = n.x(0)
            releases.append({'phase': n.phase, 'color': hex(p), 'id': n.x(1) & 0xffffffff,
                             'time_argument': n.x(2), 'owner_before': n.i(p + 0x28),
                             'bypass': n.u.mem_read(p + 0x10, 1)[0], 'lr_elf_va': hex(n.x(30))})
    for a in [0x924c18, 0x178f7fc, 0x969190, 0x927384, 0xc98648, 0x19f439c, 0x15a90c4, 0x15dfe60, 0x13db7a0]:
        n.u.hook_add(UC_HOOK_CODE, observe, begin=a, end=a)
    globals_before = {hex(p): n.i(p) for p in SPATIAL_GLOBALS}
    n.phase = '028 complete original spatial/static initializer'
    n.call(0x1930604)  # Actual ELF .init_array member at1b95c90; not an interior-block skip.
    assert all(n.i(p) == value for p, value in SPATIAL_GLOBALS.items())
    globals_after = {hex(p): n.i(p) for p in SPATIAL_GLOBALS}
    n.call(0x1054f24)
    n.trace = []; n.visual = []; n.animationTrace = []; n.downstream = []
    n.env = n.alloc(8)
    arrays = InputArrays(n)
    n.now = 1000
    entry(n)
    activate(n)
    scene, model = n.scene, n.model
    chart, score = n.q(model + 0x28), n.q(model + 0x38)
    gauge = n.items(score, 0xa0)[0]
    arcs = sorted([p for p in n.items(chart, 0x20) if n.typename(p) == '12LogicArcNote'],
                  key=lambda p: n.f(n.q(p + 0x20) + 0x14))
    expected = 2 if crossing else 1
    assert len(arcs) == len(native_arcs) == len(factories) == len(parsed) == expected
    assert set(arcs) == native_arcs
    assert all(n.i(a + 0xa4) == n.i(a + 0x15c) == 0 and n.q(a) == 0x1b91500 for a in arcs)
    assert all(p['time'] == [1000, 2000] and p['mode'] == 0 and p['curve'] == 's' for p in parsed)
    assert all(p['y_endpoints'] == [.5, .5] and
               all(math.isclose(x, y, abs_tol=1e-7) for x, y in zip(sorted(p['x_endpoints']), [.2, .8])) for p in parsed), parsed
    assert all(n.i(a + 0x18) == 1000 and n.i(a + 0x1c) == 2000 for a in arcs)
    colors = [n.q(a + 0xb0) for a in arcs]
    assert len(set(colors)) == expected and all(n.typename(c) == '10LogicColor' for c in colors)
    records = {a: list(range(n.q(a + 0x78), n.q(a + 0x80), 12)) for a in arcs}
    count = n.i(chart + 0xb8)
    assert count == sum(n.i(p + 4) for ps in records.values() for p in ps) > 0
    assert all([(n.i(p), n.i(p + 4), n.u.mem_read(p + 8, 1)[0]) for p in ps] ==
               [(1250, 1, 0), (1500, 1, 0), (1750, 1, 0)] for ps in records.values())
    assert n.i(chart + 0xbc) == 2500
    maps = n.maps(model)
    assert all(any(a in members for group in maps for members in group.values()) for a in arcs)
    geometry = [{'arc': hex(a), 'color': hex(n.q(a + 0xb0)), 'mapped_color': n.i(n.q(a + 0xb0) + 0x18),
                 'group': hex(n.q(a + 0xe0)), 'successors': [hex(p) for p in n.items(a, 0x138)],
                 'interval': n.f(a + 0x70), 'timing_group': n.i(a + 0x50),
                 'points': [[n.f(p + 4*i) for i in range(3)] for p in range(n.q(a + 0xe8), n.q(a + 0xf0), 12)],
                 'records': [{'time': n.i(p), 'weight': n.i(p + 4)} for p in records[a]]} for a in arcs]
    assert all(len(g['points']) > 1 and not g['successors'] for g in geometry)
    assert all(any(s['arc'] == g['arc'] for s in samples) for g in geometry), 'native geometry append not observed'
    listener = n.state(model)['listener']
    assert n.sceneInitReturn == 1 and listener['registered'] == listener['enabled'] == 1 and listener['paused'] == 0
    assert n.q(scene + 0x3e0) == model and n.q(scene + 0x3e8) == chart
    assert n.q(n.director + 0x140) == scene and n.q(n.director + 0x148) == 0
    camera = n.q(n.q(model + 0x20) + 0x2a8)
    writes, resolved = [], []

    def written(u, access, where, size, value, data):
        writes.append({'phase': n.phase, 'address': hex(where), 'size': size, 'value': value,
                       'pc_elf_va': hex(u.reg_read(UC_ARM64_REG_PC))})
    for a, c in zip(arcs, colors):
        n.u.hook_add(UC_HOOK_MEM_WRITE, written, begin=a + 0xd4, end=a + 0xdb)
        for start, end in [(c + 0x10, c + 0x17), (c + 0x28, c + 0x30)]:
            n.u.hook_add(UC_HOOK_MEM_WRITE, written, begin=start, end=end)
        for p in records[a]:
            def resolution(u, access, where, size, value, data, arc=a, record=p):
                resolved.append({'arc': hex(arc), 'time': n.i(record), 'before': n.u.mem_read(record + 8, 1)[0],
                                 'value': value, 'size': size, 'phase': n.phase,
                                 'pc_elf_va': hex(u.reg_read(UC_ARM64_REG_PC))})
            n.u.hook_add(UC_HOOK_MEM_WRITE, resolution, begin=p + 8, end=p + 8)

    def f32(v):
        return struct.unpack('<f', struct.pack('<f', v))[0]

    def target(a):
        # Literal f32 quantization from c985e0..c98618, not AFF interpolation.
        start = int(f32(f32(n.f(n.q(a + 0x20) + 0x14) * 850) - 425))
        return [start + n.f(a + 0xd4), n.f(a + 0xd8), 0.0]

    def project(a):
        world = target(a)
        p, out = n.alloc(12), n.alloc(8)
        for i, value in enumerate(world):
            n.wf(p + 4*i, value)
        n.call(0xbdbb70, camera, p, regs={8: out})
        xy = [n.f(out), n.f(n.director + 0x184) - n.f(out + 4)]
        assert all(math.isfinite(v) for v in xy)
        return {'world': world, 'jni_xy': xy}

    states, inputs = [], []
    def state(label):
        row = {'label': label, 'wall': n.now, 'E': effective(), 'camera': hex(camera),
               'arcs': [{'pointer': hex(a), 'cache_xy': [n.f(a + 0xd4), n.f(a + 0xd8)],
                         'target': target(a), 'cache_enabled': n.u.mem_read(a + 0xd0, 1)[0],
                         'active': list(n.u.mem_read(a + 0x64, 2)),
                         'resolved': [n.u.mem_read(p + 8, 1)[0] for p in records[a]]} for a in arcs],
               'colors': [{'pointer': hex(c), 'mapped_id': n.i(c + 0x18), 'owner': n.i(c + 0x28),
                           'release': n.i(c + 0x2c), 'bypass': n.u.mem_read(c + 0x10, 1)[0],
                           'bypass_time': n.i(c + 0x14), 'conflict': n.u.mem_read(c + 0x30, 1)[0]} for c in colors],
               'claimed_ids': [n.i(p) for p in range(n.q(0x1bfa3d8), n.q(0x1bfa3e0), 4)],
               'touches': [{'pointer': hex(t), 'generated_id': n.i(t + 0x34), 'slot': n.i(t + 0xc),
                            'xy': [n.f(t + 0x1c), n.f(t + 0x20)],
                            'previous': [n.f(t + 0x24), n.f(t + 0x28)]} for t in n.items(model, 0xd0)],
               'mask': n.i(0x1bfebd4), 'android_map_size': n.q(0x1bf1a98),
               'score': {'PURE': n.i(score + 0x24), 'shining': n.i(score + 0x20), 'FAR': n.i(score + 0x28),
                         'LOST': n.i(score + 0x2c), 'score': n.i(score + 0x14), 'health': n.f(gauge + 0x10)}}
        if crossing:
            row['separation'] = math.dist(row['arcs'][0]['target'][:2], row['arcs'][1]['target'][:2])
        states.append(row)
        return row

    def advance(E, phase):
        row = frame(n, n.now + E - effective(), phase)
        assert row['E'] == row['lastModelE'] == E
        assert sum(e['pc'] == '0x10a7550' for e in row['lifecycle']) == 1

    frame(n, n.now + 1, 'moving preroll')
    anchor = frame(n, n.now + 3001, 'moving native music anchor')
    assert anchor['E'] == 0
    original_touches = None
    for index, E in enumerate([1000, 1001, 1125, 1250, 1300, 1375, 1500, 1625, 1750, 1875]):
        advance(E, 'position_' + str(E))
        state('position_' + str(E))
        projected = [project(a) for a in arcs]
        n.phase = 'jni_' + str(E)
        if index == 0:
            for i, p in enumerate(projected):
                n.call(0xbe31a8, n.env, 0, 42 + i, 987042 + i, fs=(*p['jni_xy'], .5))
        else:
            old = states[-1]['touches']
            arrays.move([(42 + i, *p['jni_xy'], .5) for i, p in enumerate(projected)], 988000 + E)
        event = state('jni_' + str(E))
        if original_touches is None:
            original_touches = event['touches']
        assert [t['pointer'] for t in event['touches']] == [t['pointer'] for t in original_touches]
        assert [t['generated_id'] for t in event['touches']] == [t['generated_id'] for t in original_touches]
        for i, t in enumerate(event['touches']):
            assert all(abs(x - f32(y)) < 1e-4 for x, y in zip(t['xy'], projected[i]['jni_xy']))
            if index:
                assert t['previous'] == old[i]['xy']
        inputs.append({'E': E, 'points': projected, 'touches': event['touches']})
        advance(E, 'follow_' + str(E))
        followed = state('follow_' + str(E))
        assert all(a['active'] == [1, 1] for a in followed['arcs']), followed
    before_up = states[-1]
    for i, p in enumerate(projected):
        n.phase = 'up_' + str(42+i)
        n.call(0xdda71c, n.env, 0, 42+i, 999042+i, fs=(*p['jni_xy'], 0))
    released = state('up')
    advance(1876, 'cleanup_frame')
    cleaned = state('cleanup')
    assert released['mask'] == released['android_map_size'] == 0 and not released['touches']
    assert all(n.q(0x1beef90 + t['slot'] * 8) == 0 for t in original_touches)
    assert all(c['owner'] == -1 for c in cleaned['colors']) and not cleaned['claimed_ids']
    assert all(a['active'] == [0, 0] for a in cleaned['arcs'])
    assert cleaned['score'] == before_up['score']
    assert all(len({r['arcs'][i]['cache_xy'][0] for r in states if r['E'] >= 1000}) > 4 for i in range(expected))
    assert all(any(w['address'] == hex(a+0xd4) and w['pc_elf_va'] == '0x19f423c' for w in writes) for a in arcs)
    assert len(resolved) == sum(len(ps) for ps in records.values())
    assert len({(w['arc'], w['time']) for w in resolved}) == len(resolved)
    assert all(w['before'] == 0 and w['value'] == w['size'] == 1 and w['pc_elf_va'] == '0xf80924' for w in resolved)
    assert cleaned['score']['PURE'] == cleaned['score']['shining'] == count
    assert cleaned['score']['FAR'] == cleaned['score']['LOST'] == 0 and cleaned['score']['score'] == 10000000 + count
    counts = collections.Counter(e['pc'] for e in n.events)
    assert counts['0x1706960'] == counts['0x160b710'] == counts['0x10e7008'] == 9
    assert counts['0x1730290'] == count and counts['0x868e54'] == counts['0xc27d34'] == 0
    assert counts['0xbe31a8'] == counts['0xdda71c'] == expected and counts['0x1925084'] == expected
    assert claims and any(c.get('accepted') == 1 for c in claims)
    assert spatial and all(s.get('accepted') == 1 for s in spatial if s['phase'].startswith('follow_') and not crossing)
    if crossing:
        follows = [s for s in states if s['label'].startswith('follow_')]
        assert follows[0]['separation'] > 200 and follows[-1]['separation'] > 200
        assert any(s['separation'] < 1 for s in follows), 'native positions did not cross'
        assert proximity and any(p['distance'] < p['threshold'] == 200 for p in proximity)
        assert any(all(c['bypass'] == 1 and c['owner'] == -1 for c in s['colors']) for s in follows)
    else:
        assert all(s['colors'][0]['owner'] == original_touches[0]['generated_id'] for s in states if s['label'].startswith('follow_'))
    for address in [0xee197c, 0xee29a8, 0xee29e8, 0xe4e4dc, 0xe2ea48, 0x1930604, 0x1870de0, 0x173b358, 0x1862a14]:
        assert counts[hex(address)] == 1, (hex(address), counts[hex(address)])
    assert counts['0xdd0f90'] == 0 and n.q(score+0x68) == 0
    assert any(e['pc'] == '0xee2214' and int(e['x'][0],16) == 1 for e in n.soloTrace)
    assert n.u.mem_read(n.menu+0x490,1)[0] == 1
    constructor = next(e for e in n.menuTrace if e['pc']=='0xe4e4dc')
    assert constructor['lr']=='0xee29ec' and int(constructor['x'][0],16)==scene
    forbidden = {0xe4e4dc, 0xe2ea48, 0x10a7550, 0x1862a14, 0x178f7fc, 0x1925084, 0x1576aa4,
                 0x19f3d4c, 0x14858d4, 0xc98490, 0x927384, 0x15dfe2c, 0x15a90c4, 0x13db7a0, 0x1730290, 0x868e54}
    assert not forbidden.intersection(n.host_calls) and not forbidden.intersection(n.hooks)
    return {'status':'pass', 'fixture':'native_crossing_arcs.aff' if crossing else 'native_moving_arc.aff',
            'native_objects':{'scene':hex(scene),'model':hex(model),'chart':hex(chart),'camera':hex(camera)},
            'initializer_return':n.sceneInitReturn, 'parsed_arcs':parsed, 'native_factory_returns':factories,
            'geometry':geometry, 'native_geometry_appends':samples, 'N':count, 'chart_end':n.i(chart+0xbc),
            'spatial_globals_before':globals_before, 'native_initialized_globals':globals_after,
            'geometry_height_global':n.i(0x1bf6d80), 'original_initializer_elf_va':'0x1930604',
            'anchor':anchor, 'states':states, 'inputs':inputs, 'spatial_checks':spatial,
            'proximity_checks':proximity, 'native_claims':claims, 'native_releases':releases,
            'native_state_writes':writes, 'native_record_writes':resolved,
            'recorders':[e for e in n.events if e['pc'] in ('0x1730290','0x868e54')],
            'jni_array_services':arrays.calls, 'reused_obj_abi':dict(collections.Counter(x['service'] for x in abi)),
            'native_call_counts':{hex(a):counts[hex(a)] for a in OBSERVE|{0xee197c,0xee29a8,0xee29e8,0xe4e4dc,0xe2ea48,0xc27d34}},
            'final_score':cleaned['score'], 'checks':{'native_geometry_and_camera':True,'same_touch_across_moves':True,
              'native_spatial_claim_activation':True,'unique_checkpoint_resolution':True,'native_cleanup':True,'no_host_gameplay_bridge':True}}


def run():
    control = run_case(False)  # Gate A must finish before any Gate B runtime is created.
    try:
        crossing = run_case(True)
    except Exception as exc:
        return {'status':'fail','moving_control':control,'crossing':{'status':'fail'},
                'native_failures':[{'type':type(exc).__name__,'message':str(exc),
                                    'location':traceback.extract_tb(exc.__traceback__)[-1].lineno}],
                'pc_skips_elf_va':PC_SKIPS}
    return {'status':'pass','fixture':'moving-single-and-two-color-crossing',
            'fresh_emulator_per_case':True,'moving_control':control,'crossing':crossing,
            'supplied_services':'Existing024-027 services; reused025 OBJ libc; bounded011-style JNIEnv arrays; original spatial static initializer now executed',
            'pc_skips_elf_va':PC_SKIPS,'native_failures':[],
            'endpoint':'E1876 after native UP/next-frame cleanup; no results/SQLite replay'}
