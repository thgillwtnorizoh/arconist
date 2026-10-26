"""Two equal-time JNI DOWNs with overlapping native contacts, in both orders."""
import collections
import math
import struct
from unicorn import UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm64_const import UC_ARM64_REG_PC, UC_ARM64_REG_SP
from solo_entry import setup, entry
from lifecycle import activate, frame
from boundaries import PC_SKIPS

OBSERVE = {0x1870de0, 0xdf4a58, 0xb01d6c, 0x173b358, 0x1862a14,
           0x18640d8, 0x18640dc, 0x11ea120, 0x1576aa4,
           0xbe31a8, 0xdda71c, 0x194ff80, 0xeec024, 0xeec080,
           0x13073c4, 0xeec1cc, 0xeec4f0, 0xf6b514,
           0x160ce28, 0x965e28, 0x1730290, 0x868e54, 0xf9a50c}


def run_case(reverse):
    n = setup(True)  # New Uc/ELF/global state/heap for this case; no saved snapshot.
    n.prepare_runtime()
    n.call(0x1054f24)
    n.observe |= OBSERVE
    construction, refreshes, ground, lanes, candidates, acceptance = [], [], [], [], [], []

    def effective():
        t = n.q(n.model + 0x30)
        return n.i(t + 0x20) - n.i(t + 0x28)

    def observe(u, address, size, data):
        if address == 0x18640d8:
            source = n.x(27)
            construction.append({'parsed_type': n.typename(source), 'parsed_time': n.i(source + 0x18),
                                 'raw_integer_position': n.i(n.q(source + 0x20) + 8),
                                 'note': hex(n.x(0)), 'native_initializer_elf_va': hex(n.x(8)),
                                 'time_argument': n.x(1), 'position': hex(n.x(2))})
        elif address == 0x18640dc:
            construction[-1].update(initializer_return=n.x(0) & 1,
                                    returned_note=hex(n.x(25)), vtable_elf_va=hex(n.q(n.x(25))),
                                    runtime_type=n.typename(n.x(25)))
        elif address == 0xeec080:
            refreshes.append({'phase': n.phase, 'wall': n.now, 'E': effective(),
                              'touch': hex(n.x(26)), 'generated_id': n.i(n.x(26) + 0x34)})
        elif address == 0x13073c4:
            sp = u.reg_read(UC_ARM64_REG_SP)
            ground.append({'phase': n.phase, 'point': [n.f(sp + 0x28 + 4 * i) for i in range(3)]})
        elif address == 0xeec1cc:
            lanes.append({'phase': n.phase, 'primary': n.x(0) & 0xffffffff,
                          'secondary': n.x(0) >> 32})
        elif address == 0xeec4f0:
            candidates.append({'phase': n.phase, 'touch': hex(n.x(26)),
                               'notes': [hex(p) for p in n.items(n.x(19), 0xb8)]})
        elif address == 0x965e28:
            p = n.x(0)
            acceptance.append({'phase': n.phase, 'note': hex(p), 'E': n.x(1),
                               'generated_id': n.x(2) & 0xffffffff, 'consumed_before': n.u.mem_read(p + 0xd, 1)[0],
                               'lr_elf_va': hex(n.x(30))})
    for a in [0x18640d8, 0x18640dc, 0xeec080, 0x13073c4, 0xeec1cc, 0xeec4f0, 0x965e28]:
        n.u.hook_add(UC_HOOK_CODE, observe, begin=a, end=a)
    n.trace = []; n.visual = []; n.animationTrace = []; n.downstream = []
    n.env = n.alloc(8); n.now = 1000
    entry(n)
    activate(n)
    scene, model = n.scene, n.model
    chart, score = n.q(model + 0x28), n.q(model + 0x38)
    gauge = n.items(score, 0xa0)[0]
    taps = [p for p in n.items(chart, 0x20) if n.typename(p) == '12LogicTapNote']
    assert len(taps) == len(set(taps)) == len(construction) == 2, 'two original tap products required'
    by_lane = {n.i(n.q(p + 0x20) + 0x10): p for p in taps}
    assert set(by_lane) == {2, 5}, ('unexpected native lanes', list(by_lane))
    assert n.i(chart + 0xb8) == 2, 'native denominator must be two'
    assert all(n.i(p + 0x18) == n.i(p + 0x1c) == 1500 for p in taps)
    assert all(n.q(p) == 0x1af4278 and n.u.mem_read(p + 0x54, 1)[0] == 1 for p in taps)
    for row in construction:
        p = int(row['note'], 16)
        assert row['initializer_return'] == 1 and row['returned_note'] == row['note']
        assert row['runtime_type'] == '12LogicTapNote' and row['parsed_time'] == row['time_argument'] == 1500
        assert int(row['position'], 16) == n.q(p + 0x20)
        assert n.i(n.q(p + 0x20) + 0x10) == row['raw_integer_position'] + 1
    assert sorted(r['raw_integer_position'] for r in construction) == [1, 4]
    maps = n.maps(model)
    index_keys = {str(lane): [[k for k, members in group.items() if p in members] for group in maps]
                  for lane, p in by_lane.items()}
    assert all(any(groups) for groups in index_keys.values()), 'both notes need native index membership'
    listener = n.state(model)['listener']
    assert listener['registered'] == listener['enabled'] == 1 and listener['paused'] == 0
    assert n.sceneInitReturn == 1 and n.q(scene + 0x3e0) == model and n.q(scene + 0x3e8) == chart
    assert n.q(n.director + 0x140) == scene and n.q(n.director + 0x148) == 0
    writes = []
    def consumption_write(u, access, where, size, value, data):
        p = next(p for p in taps if p + 0xd <= where <= p + 0x13)
        writes.append({'note': hex(p), 'offset': hex(where - p), 'size': size, 'value': value,
                       'before': int.from_bytes(u.mem_read(where, size), 'little'),
                       'pc_elf_va': hex(u.reg_read(UC_ARM64_REG_PC)), 'phase': n.phase})
    for p in taps:
        n.u.hook_add(UC_HOOK_MEM_WRITE, consumption_write, begin=p + 0xd, end=p + 0x13)

    frame(n, n.now + 1, 'chord preroll')
    anchor = frame(n, n.now + 3001, 'chord native music anchor')
    assert anchor['E'] == 0
    chord_frame = frame(n, n.now + 1500 - effective(), 'chord judgment frame')
    assert chord_frame['E'] == chord_frame['lastModelE'] == 1500
    assert sum(e['pc'] == '0x10a7550' for e in chord_frame['lifecycle']) == 1
    assert set(taps).issubset(n.items(model, 0xa0)), 'both notes must be active before first DOWN'
    # External target centers: native lane2/5 within conservative [-850,-425)
    # and (425,850] intervals, respectively. Original selector semantics include
    # broader outer ranges; no claim that these are universal outer hitbox bounds.
    assert n.i(model + 0x148) == 0 and n.f(model + 0x60) == 1 and n.f(model + 0x74) == 0
    camera = n.q(n.q(model + 0x20) + 0x2a8)
    contacts = {}
    for android_id, lane in [(42, 2), (43, 5)]:
        point, out = n.alloc(12), n.alloc(8)
        world = [425.0 * (lane - 3.5), 0.0, 0.0]
        for i, value in enumerate(world):
            n.wf(point + 4 * i, value)
        n.call(0xbdbb70, camera, point, regs={8: out})
        xy = [n.f(out), n.f(n.director + 0x184) - n.f(out + 4)]
        assert all(math.isfinite(v) for v in xy)
        contacts[android_id] = {'lane': lane, 'note': hex(by_lane[lane]), 'world_target': world, 'jni_xy': xy}

    def score_state():
        return {'score': n.i(score + 0x14), 'shining': n.i(score + 0x20), 'PURE': n.i(score + 0x24),
                'FAR': n.i(score + 0x28), 'LOST': n.i(score + 0x2c), 'health': n.f(gauge + 0x10)}

    def mapping():
        out = []
        def walk(p):
            if not p:
                return
            walk(n.q(p))
            slot = n.i(p + 0x28)
            touch = n.q(0x1beef90 + slot * 8)
            out.append({'android_id': struct.unpack('<q', n.u.mem_read(p + 0x20, 8))[0], 'slot': slot,
                        'touch': hex(touch), 'generated_id': n.i(touch + 0x34),
                        'touch_slot': n.i(touch + 0xc)})
            walk(n.q(p + 8))
        walk(n.q(0x1bf1a90))
        return out

    snapshots = []
    def snapshot(label):
        row = {'label': label, 'wall': n.now, 'E': effective(), 'director_frame': n.i(n.director + 0x134),
               'mapping': mapping(), 'engine_mask': n.i(0x1bfebd4),
               'retained': [{'touch': hex(p), 'generated_id': n.i(p + 0x34)} for p in n.items(model, 0xd0)],
               'notes': {str(lane): {'pointer': hex(p), 'time': n.i(p + 0x18),
                                    'input_enabled': n.u.mem_read(p + 0x54, 1)[0],
                                    'missed': n.u.mem_read(p + 0xc, 1)[0],
                                    'consumed': n.u.mem_read(p + 0xd, 1)[0], 'accepted_id': n.i(p + 0x10)}
                         for lane, p in sorted(by_lane.items())}, 'score': score_state()}
        snapshots.append(row)
        return row

    before = snapshot('before_downs')
    assert not before['mapping'] and not before['retained'] and before['engine_mask'] == 0
    assert all(r['consumed'] == r['missed'] == 0 for r in before['notes'].values())
    order = [43, 42] if reverse else [42, 43]
    for index, pid in enumerate(order):
        n.phase = 'down_' + str(pid)
        n.call(0xbe31a8, n.env, 0, pid, 987000 + pid, fs=(*contacts[pid]['jni_xy'], .5))
        row = snapshot(n.phase)
        assert row['wall'] == before['wall'] and row['E'] == 1500 and row['director_frame'] == before['director_frame']
        assert {m['android_id'] for m in row['mapping']} == set(order[:index + 1])
        assert len(row['retained']) == index + 1 and row['engine_mask'].bit_count() == index + 1
        assert {r['touch'] for r in row['retained']} == {m['touch'] for m in row['mapping']}
        assert len({m['generated_id'] for m in row['mapping']}) == index + 1
        assert all(m['slot'] == m['touch_slot'] for m in row['mapping'])
        for m in row['mapping']:
            note = row['notes'][str(contacts[m['android_id']]['lane'])]
            assert note['consumed'] == 1 and note['accepted_id'] == m['generated_id'] and note['missed'] == 0
        assert sum(r['consumed'] for r in row['notes'].values()) == index + 1
        assert row['score']['PURE'] == row['score']['shining'] == index + 1
        assert row['score']['FAR'] == row['score']['LOST'] == 0
        assert candidates[-1]['notes'] == [contacts[pid]['note']], 'other lane must not enter candidate vector'
        assert lanes[-1]['primary'] == contacts[pid]['lane'] and lanes[-1]['secondary'] == 0
        assert all(abs(a - b) < .5 for a, b in zip(ground[-1]['point'], contacts[pid]['world_target']))
    both = snapshots[-1]
    assert len({m['touch'] for m in both['mapping']}) == len({m['slot'] for m in both['mapping']}) == 2
    assert snapshots[1]['retained'][0] in both['retained'], 'second DOWN must preserve first retained Touch'
    assert {r['touch'] for r in refreshes} == {m['touch'] for m in both['mapping']}
    assert [r['E'] for r in refreshes] == [1500, 1500] and len({r['wall'] for r in refreshes}) == 1
    for index, pid in enumerate(order):
        n.phase = 'up_' + str(pid)
        n.call(0xdda71c, n.env, 0, pid, 988000 + pid, fs=(*contacts[pid]['jni_xy'], 0))
        row = snapshot(n.phase)
        assert {m['android_id'] for m in row['mapping']} == set(order[index + 1:])
        assert len(row['retained']) == 1 - index and row['engine_mask'].bit_count() == 1 - index
        assert row['notes'] == both['notes'] and row['score'] == both['score']
    final = snapshots[-1]
    assert final['engine_mask'] == 0 and final['mapping'] == final['retained'] == []
    assert all(n.q(0x1beef90 + m['slot'] * 8) == 0 for m in both['mapping'])
    assert final['score']['score'] == 10000002 and math.isclose(final['score']['health'], 80.4000015258789, abs_tol=1e-6)
    counts = collections.Counter(e['pc'] for e in n.events)
    for a in [0xee197c, 0xee29a8, 0xee29e8, 0xe4e4dc, 0xe2ea48, 0x1870de0, 0x173b358, 0x1862a14, 0x11ea120]:
        assert counts[hex(a)] == 1, (hex(a), counts[hex(a)])
    for a in [0x18640d8, 0x18640dc, 0xbe31a8, 0xdda71c, 0x194ff80, 0xeec024,
              0xf6b514, 0x160ce28, 0x965e28, 0x1730290, 0xf9a50c]:
        assert counts[hex(a)] == 2, (hex(a), counts[hex(a)])
    assert counts['0xdd0f90'] == counts['0x868e54'] == counts['0xc27d34'] == 0 and n.q(score + 0x68) == 0
    assert len(acceptance) == 2 and {a['note'] for a in acceptance} == {hex(p) for p in taps}
    for a in acceptance:
        assert a['E'] == 1500 and a['consumed_before'] == 0 and a['lr_elf_va'] == '0x17302ec'
        m = next(m for m in both['mapping'] if m['generated_id'] == a['generated_id'])
        assert contacts[m['android_id']]['note'] == a['note']
    recorders = [e for e in n.events if e['pc'] == '0x1730290']
    for e, a in zip(recorders, acceptance):
        assert e['x'][1] == a['note'] and int(e['x'][4], 16) == 1500
        assert int(e['x'][5], 16) == a['generated_id'] and e['lr'] == '0x160cf48'
    assert len(writes) == 4
    assert all(w['pc_elf_va'] == ('0x965e68' if w['offset'] == '0xd' else '0x965e6c') for w in writes)
    assert all(sum(w['note'] == hex(p) and w['offset'] == '0xd' and w['before'] == 0 and w['value'] == 1 for w in writes) == 1 for p in taps)
    for p in taps:
        assert any(e['pc'] == '0x1576aa4' and int(e['x'][0], 16) == model and int(e['x'][1], 16) == p for e in n.events)
    eligibility = [e for e in n.soloTrace if e['pc'] == '0xee2214']
    assert len(eligibility) == 1 and int(eligibility[0]['x'][0], 16) == 1
    assert n.u.mem_read(n.menu + 0x490, 1)[0] == 1
    constructor = [e for e in n.menuTrace if e['pc'] == '0xe4e4dc'][0]
    assert constructor['lr'] == '0xee29ec' and int(constructor['x'][0], 16) == scene
    forbidden = {0xe4e4dc, 0xe2ea48, 0x10a7550, 0x1862a14, 0x1576aa4, 0xeec024,
                 0xf6b514, 0x160ce28, 0x965e28, 0x1730290, 0x868e54, 0xf9a50c}
    assert not forbidden.intersection(n.host_calls) and not forbidden.intersection(n.hooks)
    return {'case': 'reverse' if reverse else 'forward', 'down_order': order,
            'construction': construction, 'native_chart': {'N': n.i(chart + 0xb8), 'end': n.i(chart + 0xbc),
              'main_objects': len(n.items(chart, 0x20)), 'index_keys_by_lane': index_keys},
            'native_objects': {'scene': hex(scene), 'model': hex(model), 'chart': hex(chart), 'score': hex(score)},
            'startup': {'eligibility': 1, 'request_latch': 1, 'initializer_return': n.sceneInitReturn,
                        'constructor_lr_elf_va': constructor['lr'], 'listener': listener},
            'anchor': anchor, 'chord_frame': chord_frame, 'contacts': contacts,
            'native_time_refreshes': refreshes, 'native_ground': ground, 'native_lane_results': lanes,
            'native_candidates': candidates, 'snapshots': snapshots, 'acceptance': acceptance,
            'consumption_writes': writes, 'recorder_entries': recorders, 'final_score': final['score'],
            'native_call_counts': {hex(a): counts[hex(a)] for a in OBSERVE | {0xee197c, 0xee29a8, 0xee29e8, 0xe4e4dc, 0xe2ea48, 0xc27d34}},
            'checks': {'native_note_construction_and_index': True, 'same_time_downs': True,
                       'two_concurrent_contacts': True, 'lane_specific_candidates': True,
                       'note_contact_identity': True, 'unique_consumption': True, 'native_up_cleanup': True,
                       'no_host_judgment_or_state_repair': True},
            'endpoint': {'running_scene': hex(n.q(n.director + 0x140)), 'pending': n.q(n.director + 0x148),
                         'result_cache': n.q(score + 0x68), 'E': effective()}}


def run():
    forward, reverse = run_case(False), run_case(True)
    assert forward['final_score'] == reverse['final_score']
    assert forward['native_chart']['N'] == reverse['native_chart']['N'] == 2
    for lane in ['2', '5']:
        a, b = forward['snapshots'][-1]['notes'][lane], reverse['snapshots'][-1]['notes'][lane]
        assert (a['time'], a['consumed'], a['missed']) == (b['time'], b['consumed'], b['missed']) == (1500, 1, 0)
    return {'status': 'pass', 'fixture': 'native_chord.aff/offline-solo/sayonarahatsukoi/0',
            'fresh_emulator_per_case': True, 'forward': forward, 'reverse': reverse,
            'comparison': {'same_native_N_and_lane_time_consumption': True, 'equal_native_score_and_gauge': True,
                           'both_contact_lifetimes_overlap': True, 'both_native_cleanups_pass': True,
                           'heap_addresses_and_generated_ID_assignment_not_compared_across_emulators': True},
            'supplied_interfaces': 'Unchanged ordinary 024-026 platform/ABI/catalog/settings/profile/resource/audio/GPU services; external chart/clock/JNI inputs; no new service or skip',
            'pc_skips_elf_va': PC_SKIPS, 'native_failures': [],
            'endpoint': 'E1500 after both UPs; no chord completion/results/SQLite replay'}
