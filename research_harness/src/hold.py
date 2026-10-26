"""Two fresh native-owned hold runs; read-only observers, JNI inputs, no state repair."""
import collections
import math
import struct
from unicorn import UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm64_const import UC_ARM64_REG_PC, UC_ARM64_REG_SP
from solo_entry import setup, entry
from lifecycle import activate, frame
from boundaries import PC_SKIPS

OBSERVE = {0x1870de0, 0xdf4a58, 0xb01d6c, 0x139b96c, 0x923240, 0x173b358, 0x1862a14, 0x18649b8,
           0x1446490, 0x18649bc, 0xd92558, 0xd925fc, 0x11ea120, 0xc052f4, 0x1576aa4,
           0x1866030, 0x14858d4, 0x14557b4, 0xf8056c, 0xc6e938,
           0x1730290, 0x868e54, 0xbe31a8, 0xdda71c, 0x194ff80,
           0xeec024, 0xf9a50c, 0x13073c4, 0xeec1cc, 0x1485afc, 0xf80904}


def run_case(interrupted):
    # Every invocation creates a new Uc, ELF mapping, native globals and heap.
    n = setup(True)
    n.prepare_runtime()
    n.call(0x1054f24)
    n.observe |= OBSERVE
    parsed, created, generated, activations, projections, guards = [], [], [], [], [], []

    def observe(u, address, size, data):
        if address == 0x18649b8:
            source, position = n.x(27), n.q(n.x(27) + 0x20)
            parsed.append({'parsed_type': n.typename(source), 'start': n.i(source + 0x18),
                           'end': n.i(source + 0x1c), 'raw_integer_position': n.i(position + 8),
                           'factory_start': n.x(1), 'factory_end': n.x(2),
                           'runtime_position': hex(n.x(3))})
        elif address == 0x18649bc:
            p = n.x(0)
            created.append({'pointer': hex(p), 'vtable_elf_va': hex(n.q(p)), 'type': n.typename(p)})
        elif address == 0xd925fc:
            p = n.x(1)
            generated.append({'hold': hex(n.x(0) - 0x78), 'time': n.i(p),
                              'weight': n.i(p + 4), 'resolved': n.u.mem_read(p + 8, 1)[0]})
        elif address == 0x14557b4:
            p = n.x(1)
            activations.append({'E': n.x(2), 'hold': hex(n.x(0)), 'touch': hex(p),
                                'generated_id': n.i(p + 0x34), 'phase': n.phase})
        elif address == 0x13073c4:
            sp = u.reg_read(UC_ARM64_REG_SP)
            projections.append({'phase': n.phase, 'ground': [n.f(sp + 0x28 + 4 * i) for i in range(3)]})
        elif address == 0xf80904:
            guards.append({'record': records.index(n.x(14) - 8), 'resolved': n.x(15) & 255, 'phase': n.phase})
    for a in [0x18649b8, 0x18649bc, 0xd925fc, 0x14557b4, 0x13073c4, 0xf80904]:
        n.u.hook_add(UC_HOOK_CODE, observe, begin=a, end=a)
    n.trace = []; n.visual = []; n.animationTrace = []; n.downstream = []
    n.env = n.alloc(8); n.now = 1000
    entry(n)
    activate(n)
    scene, model = n.scene, n.model
    chart, timeline, score = n.q(model + 0x28), n.q(model + 0x30), n.q(model + 0x38)
    gauge = n.items(score, 0xa0)[0]
    holds = [p for p in n.items(chart, 0x20) if n.typename(p) == '13LogicHoldNote']
    assert len(holds) == len(parsed) == len(created) == 1
    hold = holds[0]
    assert created[0]['pointer'] == hex(hold) and n.q(hold) == 0x1b2eda8
    assert parsed[0]['start'] == parsed[0]['factory_start'] == n.i(hold + 0x18) == 1000
    assert parsed[0]['end'] == parsed[0]['factory_end'] == n.i(hold + 0x1c) == 2000
    position = n.q(hold + 0x20)
    assert parsed[0]['raw_integer_position'] == 3 and parsed[0]['runtime_position'] == hex(position)
    lane = n.i(position + 0x10)
    assert lane == 4 and n.f(hold + 0x70) == 250
    records = list(range(n.q(hold + 0x78), n.q(hold + 0x80), 12))
    assert [(n.i(p), n.i(p + 4), n.u.mem_read(p + 8, 1)[0]) for p in records] == [
        (1250, 1, 0), (1500, 1, 0), (1750, 1, 0)]
    assert [(r['time'], r['weight'], r['resolved']) for r in generated] == [(1250, 1, 0), (1500, 1, 0), (1750, 1, 0)]
    assert all(r['hold'] == hex(hold) for r in generated)
    assert n.i(chart + 0xb8) == 3 and n.i(chart + 0xbc) == 2500
    maps = n.maps(model)
    index_keys = [[k for k, pointers in group.items() if hold in pointers] for group in maps]
    assert any(index_keys), ('hold absent from original spatial index', index_keys)
    listener = n.state(model)['listener']
    assert listener['registered'] == listener['enabled'] == 1 and listener['paused'] == 0
    assert n.sceneInitReturn == 1 and n.q(scene + 0x3e0) == model and n.q(scene + 0x3e8) == chart
    assert n.q(n.director + 0x140) == scene and n.q(n.director + 0x148) == 0
    resolved_writes, flag_writes = [], []

    def resolution(u, access, where, size, value, data):
        resolved_writes.append({'record': records.index(where - 8), 'time': n.i(where - 8),
                                'before': n.u.mem_read(where, 1)[0], 'value': value, 'size': size,
                                'pc_elf_va': hex(u.reg_read(UC_ARM64_REG_PC)), 'phase': n.phase})
    for p in records:
        n.u.hook_add(UC_HOOK_MEM_WRITE, resolution, begin=p + 8, end=p + 8)

    def flags(u, access, where, size, value, data):
        flag_writes.append({'offset': hex(where - hold), 'value': value, 'size': size,
                            'pc_elf_va': hex(u.reg_read(UC_ARM64_REG_PC)), 'phase': n.phase})
    for start, end in [(hold + 0x64, hold + 0x65), (hold + 0xa8, hold + 0xa8)]:
        n.u.hook_add(UC_HOOK_MEM_WRITE, flags, begin=start, end=end)

    def effective():
        return n.i(timeline + 0x20) - n.i(timeline + 0x28)

    def score_state():
        return {'score': n.i(score + 0x14), 'shining': n.i(score + 0x20),
                'PURE': n.i(score + 0x24), 'FAR': n.i(score + 0x28), 'LOST': n.i(score + 0x2c),
                'health': n.f(gauge + 0x10)}

    def engine_mapping():
        out = []
        def walk(p):
            if not p:
                return
            walk(n.q(p))
            slot = n.i(p + 0x28)
            touch = n.q(0x1beef90 + slot * 8)
            out.append({'android_id': struct.unpack('<q', n.u.mem_read(p + 0x20, 8))[0],
                        'slot': slot, 'touch': hex(touch), 'generated_id': n.i(touch + 0x34)})
            walk(n.q(p + 8))
        walk(n.q(0x1bf1a90))
        return out

    states = []
    def snapshot(label):
        row = {'label': label, 'wall': n.now, 'E': effective(),
               'latch': n.u.mem_read(hold + 0xa8, 1)[0],
               'contact_flags': list(n.u.mem_read(hold + 0x64, 2)),
               'retained': [{'touch': hex(p), 'generated_id': n.i(p + 0x34)} for p in n.items(model, 0xd0)],
               'engine_mask': n.i(0x1bfebd4), 'engine_mapping': engine_mapping(),
               'resolved': [n.u.mem_read(p + 8, 1)[0] for p in records], 'result': score_state()}
        states.append(row)
        return row

    def advance(target):
        row = frame(n, n.now + target - effective(), 'hold E' + str(target))
        assert row['E'] == row['lastModelE'] == target
        assert sum(e['pc'] == '0x10a7550' for e in row['lifecycle']) == 1
        return snapshot('frame_' + str(target))

    frame(n, n.now + 1, 'hold preroll')
    anchor = frame(n, n.now + 3001, 'hold native music anchor')
    assert anchor['E'] == 0
    advance(1000)
    # External contact target from native-created lane4 and the original ordinary
    # selector's world interval [0,425), 0x13074d0..e0. This is an input-plane
    # center, not a host-written note position or a claim of rendered geometry.
    assert n.i(model + 0x148) == 0 and n.f(position + 0x14) == 1.0
    world = [425.0 * (lane - 3.5), 0.0, 0.0]
    point, out = n.alloc(12), n.alloc(8)
    for i, value in enumerate(world):
        n.wf(point + 4 * i, value)
    camera = n.q(n.q(model + 0x20) + 0x2a8)
    n.call(0xbdbb70, camera, point, regs={8: out})
    xy = [n.f(out), n.f(n.director + 0x184) - n.f(out + 4)]
    assert all(math.isfinite(v) for v in xy)
    inputs = []

    def event(down, android_id, label):
        n.phase = label
        n.call(0xbe31a8 if down else 0xdda71c, n.env, 0, android_id,
               (987000 if down else 988000) + android_id, fs=(*xy, .5 if down else 0))
        row = snapshot(label)
        inputs.append({'down': down, 'android_id': android_id, 'E': row['E'],
                       'mapping_after': row['engine_mapping']})
        if down:
            assert len(row['retained']) == len(row['engine_mapping']) == row['engine_mask'] == 1
            mapping = row['engine_mapping'][0]
            assert mapping['android_id'] == android_id and mapping['touch'] == row['retained'][0]['touch']
        else:
            assert row['retained'] == row['engine_mapping'] == [] and row['engine_mask'] == 0
        return row

    first = event(True, 42, 'first_down')
    assert first['latch'] == 1 and first['contact_flags'] == [0, 0]
    assert advance(1001)['contact_flags'] == [1, 1]
    advance(1124)
    advance(1125)
    advance(1200)
    if interrupted:
        up = event(False, 42, 'first_up')
        assert up['latch'] == 1 and up['contact_flags'] == [1, 1]
    cleared = advance(1201)
    assert cleared['latch'] == 1 and cleared['contact_flags'] == ([0, 0] if interrupted else [1, 1])
    advance(1300)
    if interrupted:
        second = event(True, 43, 'replacement_down')
        assert second['contact_flags'] == [0, 0] and second['latch'] == 1
        assert second['retained'][0]['touch'] != first['retained'][0]['touch']
        assert second['retained'][0]['generated_id'] != first['retained'][0]['generated_id']
    assert advance(1301)['contact_flags'] == [1, 1]
    for target in [1374, 1375, 1624, 1625, 1626]:
        advance(target)
    before_terminal = score_state()
    event(False, 43 if interrupted else 42, 'terminal_up')
    final = advance(1627)
    assert final['contact_flags'] == [0, 0] and final['latch'] == 1
    assert score_state() == before_terminal
    by_label = {r['label']: r for r in states}
    for label, pure, resolved in [('frame_1124', 0, [0, 0, 0]), ('frame_1125', 1, [1, 0, 0]),
                                  ('frame_1374', 1, [1, 0, 0]), ('frame_1375', 2, [1, 1, 0]),
                                  ('frame_1624', 2, [1, 1, 0]), ('frame_1625', 3, [1, 1, 1])]:
        assert by_label[label]['result']['PURE'] == pure and by_label[label]['resolved'] == resolved
    for row in states:
        result = row['result']
        assert result['shining'] == result['PURE'] and result['FAR'] == result['LOST'] == 0
        assert result['score'] == int(10000000 * result['PURE'] / n.i(chart + 0xb8)) + result['shining']
        assert sum(row['resolved']) == result['PURE']
    assert final['result']['PURE'] == 3 and final['result']['score'] == 10000003
    assert math.isclose(final['result']['health'], 80.5999984741211, abs_tol=1e-6)
    assert len(resolved_writes) == 3 and sorted(w['record'] for w in resolved_writes) == [0, 1, 2]
    assert all(w['before'] == 0 and w['value'] == w['size'] == 1 and w['pc_elf_va'] == '0xf80924' for w in resolved_writes)
    assert {g['record'] for g in guards if g['resolved'] == 1} == {0, 1, 2}
    assert any(w['phase'] == 'hold E1201' and w['pc_elf_va'] == '0x1866038' and w['value'] == 0 for w in flag_writes)
    if interrupted:
        assert any(a['touch'] == second['retained'][0]['touch'] and a['E'] == 1301 for a in activations)
    assert all(a['hold'] == hex(hold) for a in activations)
    assert projections and all(abs(p['ground'][0] - world[0]) < .5 and abs(p['ground'][2]) < .5 for p in projections)
    counts = collections.Counter(e['pc'] for e in n.events)
    for a in [0x1870de0, 0xdf4a58, 0xb01d6c, 0x173b358, 0x1862a14, 0x1446490, 0x18649bc,
              0xd92558, 0xc052f4, 0xee197c, 0xee29a8, 0xee29e8, 0xe4e4dc, 0xe2ea48]:
        assert counts[hex(a)] == 1, (hex(a), counts[hex(a)])
    assert counts['0x139b96c'] > 0  # Statement parser: timing and hold both enter it.
    assert counts['0xd925fc'] == counts['0x1730290'] == 3 and counts['0x868e54'] == 0
    for a in [0xbe31a8, 0xdda71c, 0x194ff80, 0xeec024, 0xf9a50c]:
        assert counts[hex(a)] == (2 if interrupted else 1), (hex(a), counts[hex(a)])
    assert counts['0xdd0f90'] == counts['0xc27d34'] == 0 and n.q(score + 0x68) == 0
    eligibility = [e for e in n.soloTrace if e['pc'] == '0xee2214']
    assert len(eligibility) == 1 and int(eligibility[0]['x'][0], 16) == 1
    assert n.u.mem_read(n.menu + 0x490, 1)[0] == 1
    constructor = [e for e in n.menuTrace if e['pc'] == '0xe4e4dc'][0]
    assert constructor['lr'] == '0xee29ec' and int(constructor['x'][0], 16) == scene
    recorders = [e for e in n.events if e['pc'] == '0x1730290']
    assert [int(e['x'][4], 16) for e in recorders] == [1125, 1375, 1625]
    assert all(int(e['x'][1], 16) == hold and e['lr'] == '0xf809a8' for e in recorders)
    assert any(e['pc'] == '0x1576aa4' and int(e['x'][0], 16) == model and
               int(e['x'][1], 16) == hold for e in n.events)
    forbidden = {0xe4e4dc, 0xe2ea48, 0x10a7550, 0x1862a14, 0x1446490, 0xd92558,
                 0xc052f4, 0x1576aa4, 0xeec024, 0x14858d4, 0x14557b4, 0xf8056c, 0x1730290, 0x868e54, 0xf9a50c}
    assert not forbidden.intersection(n.host_calls) and not forbidden.intersection(n.hooks)
    return {'case': 'release_reacquisition' if interrupted else 'uninterrupted',
            'native_objects': {'scene': hex(scene), 'model': hex(model), 'chart': hex(chart),
                               'timeline': hex(timeline), 'score': hex(score), 'hold': created[0],
                               'position': hex(position), 'records': [hex(p) for p in records]},
            'parsed': parsed[0], 'generated_records': generated,
            'chart': {'lane': lane, 'normalized_position': n.f(position + 0x14), 'interval': n.f(hold + 0x70),
                      'N': n.i(chart + 0xb8), 'end': n.i(chart + 0xbc), 'main_objects': len(n.items(chart, 0x20)),
                      'hold_index_keys': index_keys, 'timing_group': n.i(hold + 0x50),
                      'effective_speed': n.f(chart + 0xf4),
                      'precomputed_depths': [n.i(hold + 0x38), n.i(hold + 0x3c)]},
            'startup': {'initializer_return': n.sceneInitReturn, 'eligibility': 1, 'request_latch': 1,
                        'listener': listener, 'anchor_wall': anchor['wall'], 'anchor_E': anchor['E']},
            'projection': {'routine_elf_va': '0xbdbb70', 'external_lane_plane_target': world,
                           'jni_xy': xy, 'native_ground_checks': projections},
            'inputs': inputs, 'states': states, 'activations': activations,
            'native_resolution_writes': resolved_writes, 'native_resolved_guard_checks': guards,
            'native_flag_writes': flag_writes,
            'recorder_entries': recorders, 'final': final['result'],
            'native_call_counts': {hex(a): counts[hex(a)] for a in OBSERVE | {0xee197c, 0xee29a8, 0xee29e8, 0xe4e4dc, 0xe2ea48, 0xc27d34}},
            'checks': {'native_construction': True, 'native_checkpoint_generation': True,
                       'native_spatial_admission': True, 'native_frame_contact_changes': True,
                       'three_unique_native_resolutions': True, 'jni_cleanup': True,
                       'no_direct_host_handoffs': True},
            'endpoint': {'E': effective(), 'running_scene': hex(n.q(n.director + 0x140)),
                         'pending': n.q(n.director + 0x148), 'result_cache': n.q(score + 0x68)}}


def run():
    control = run_case(False)
    interrupted = run_case(True)
    assert control['final'] == interrupted['final']
    for key in ['lane', 'interval', 'N', 'end', 'main_objects', 'hold_index_keys']:
        assert control['chart'][key] == interrupted['chart'][key]
    common = ['frame_1125', 'frame_1200', 'frame_1201', 'frame_1300', 'frame_1301',
              'frame_1375', 'frame_1625', 'frame_1627']
    comparison = []
    for label in common:
        a = next(r for r in control['states'] if r['label'] == label)
        b = next(r for r in interrupted['states'] if r['label'] == label)
        assert a['resolved'] == b['resolved'] and a['result'] == b['result']
        comparison.append({'label': label, 'control': a, 'release_reacquisition': b})
    return {'status': 'pass', 'fixture': 'native_hold.aff/offline-solo/sayonarahatsukoi/0',
            'fresh_emulator_per_case': True, 'control': control, 'release_reacquisition': interrupted,
            'comparison': comparison, 'checks': {'same_native_outputs': True, 'distinct_replacement_touch': True,
                                                 'latch_survives_activity_clearing': True, 'no_duplicate_resolution': True},
            'supplied_interfaces': 'Unchanged 024 ordinary platform/ABI/catalog/settings/profile/resource/audio/GPU services; no new service or skip',
            'pc_skips_elf_va': PC_SKIPS, 'native_failures': [],
            'endpoint': 'E1627 after terminal cleanup; no hold completion/results/SQLite replay'}
