"""Original traversal-driven tap CPU refresh, judgment removal and miss hiding.

Only this scenario restores the existing inert base Node::visit after loading.
No renderer updater, active-list mutation or visibility setter is called by the host.
"""
import collections
import math
import traceback
from unicorn import UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm64_const import UC_ARM64_REG_PC, UC_ARM64_REG_SP
from solo_entry import setup, entry
from lifecycle import activate, frame
from boundaries import PC_SKIPS


def run_case(judged, evidence):
    n = setup(True)
    n.prepare_runtime()
    n.call(0x1930604)
    n.call(0x1054f24)
    counts = collections.Counter()
    construction, calls, writes, snapshots, processed = [], [], [], [], []
    track_products = []
    target = {}
    evidence.update(construction=construction, snapshots=snapshots, native_calls=calls, native_writes=writes, processed_predicates=processed)
    addresses = {0x86a104, 0x12970c4, 0xae6740, 0xd7e290, 0x12967e4,
                 0x10a7550, 0x19069a0, 0x960288, 0xb1638c, 0xb16468,
                 0xcf2640, 0xf20c28, 0xf20c78, 0xf20c9c, 0xf20cb0,
                 0x129c954, 0x10fd608, 0x965e28, 0x1730290, 0x868e54,
                 0xbe31a8, 0xdda71c, 0xeec024, 0x160ce28, 0x194ff80,
                 0x15a30b8, 0xcfc550, 0x129c924, 0xee197c, 0xee29a8, 0xee29e8,
                 0xe2ea48, 0x173b358, 0x1862a14, 0x1576aa4, 0x13073c4, 0xeec1cc, 0xeec4f0}

    def observe(u, a, size, data):
        counts[hex(a)] += 1
        if a == 0x12967e4:
            track_products.append(n.x(0))
        if a == 0xd7e290:
            row = {'renderer': hex(n.x(0)), 'logic': hex(n.x(1)), 'caller_return_elf_va': hex(n.x(30))}
            construction.append(row)
            ret = n.x(30)
            def initialized(uc, pc, length, unused):
                if 'return' not in row:
                    row['return'] = n.x(0)
                    row['vtable_elf_va'] = hex(n.q(int(row['renderer'], 16)))
                    row['logic_after'] = hex(n.q(int(row['renderer'], 16) + 0x2a8))
            n.u.hook_add(UC_HOOK_CODE, initialized, begin=ret, end=ret)
        if not target:
            return
        r, p = target['renderer'], target['logic']
        if a in {0xcf2640, 0xf20c28} and n.x(0) == r:
            calls.append({'pc': hex(a), 'lr_elf_va': hex(n.x(30)), 'renderer': hex(n.x(0)),
                          'x1_on_entry': n.x(1), 'phase': n.phase,
                          'director_frame': n.i(n.director + 0x134)})
        elif a in {0x10a7550, 0x960288, 0xb1638c, 0x19069a0}:
            calls.append({'pc': hex(a), 'lr_elf_va': hex(n.x(30)), 'target': hex(n.x(0)), 'phase': n.phase})
        elif a in {0xf20c78, 0xf20c9c, 0xf20cb0}:
            processed.append({'pc': hex(a), 'phase': n.phase, 'w0': n.x(0) & 0xffffffff,
                              'end_depth': n.i(p + 0x34), 'consumed': n.u.mem_read(p + 0xd, 1)[0],
                              'missed': n.u.mem_read(p + 0xc, 1)[0]})
        elif a == 0x13073c4:
            sp = u.reg_read(UC_ARM64_REG_SP)
            calls.append({'pc': hex(a), 'phase': n.phase, 'world_intersection': [n.f(sp + 0x28 + 4*i) for i in range(3)]})
        elif a == 0xeec1cc:
            calls.append({'pc': hex(a), 'phase': n.phase, 'primary_lane': n.x(0) & 0xffffffff, 'secondary_lane': n.x(0) >> 32})
        elif a == 0xeec4f0:
            calls.append({'pc': hex(a), 'phase': n.phase, 'candidates': [hex(v) for v in n.items(n.x(19), 0xb8)]})
        elif a == 0x129c924 and n.x(0) in {r, n.scene}:
            calls.append({'pc': hex(a), 'phase': n.phase, 'node': hex(n.x(0)), 'lr_elf_va': hex(n.x(30))})
        elif a == 0xcfc550 and n.x(0) == r:
            calls.append({'pc': hex(a), 'phase': n.phase, 'renderer_draw_virtual': True})
        elif a == 0x129c954 and n.x(0) == r:
            calls.append({'pc': hex(a), 'phase': n.phase, 'visible_argument': n.x(8) & 0xff})
        elif a == 0x10fd608 and n.x(26) == p:
            calls.append({'pc': hex(a), 'phase': n.phase, 'remove_condition': n.x(8) & 0xffffffff})
        elif a == 0x15a30b8 and n.x(0) == r:
            calls.append({'pc': hex(a), 'phase': n.phase, 'renderer_detach': True})
    for a in addresses:
        n.u.hook_add(UC_HOOK_CODE, observe, begin=a, end=a)
    n.trace = []; n.visual = []; n.animationTrace = []; n.downstream = []
    n.env = n.alloc(8); n.now = 1000
    entry(n)
    activate(n)
    model, scene = n.model, n.scene
    chart, score = n.q(model + 0x28), n.q(model + 0x38)
    assert len(track_products) == 1, track_products
    track = track_products[0]
    # Use the actual original initializer product and verify its owner relationship.
    evidence.update(scene=hex(scene), model=hex(model), chart=hex(chart), track=hex(track))
    assert n.q(n.q(scene + 0x300) + 0x2b8) == track
    assert n.typename(track) == '10TrackLayer', ('scene TrackLayer', hex(track), n.typename(track))
    logic = [p for p in n.items(chart, 0x20) if n.typename(p) == '12LogicTapNote']
    assert len(logic) == 1
    p = logic[0]
    renderers = n.items(track, 0x3b8)
    taps = [r for r in renderers if n.typename(r) == '13RenderTapNote']
    assert len(taps) == len(construction) == 1, (len(taps), construction)
    r = taps[0]
    assert n.q(r) == 0x1acde18 and n.q(r + 0x2a8) == p and n.q(p + 0x40) == r
    assert construction[0]['return'] == 1 and construction[0]['logic_after'] == hex(p), construction
    assert n.i(chart + 0xb8) == 1 and n.i(p + 0x18) == n.i(p + 0x1c) == 1500
    lane = n.i(n.q(p + 0x20) + 0x10)
    assert lane == 4 and n.sceneInitReturn == 1 and n.i(chart + 0xbc) == 1620
    assert n.q(n.director + 0x140) == scene and n.q(n.director + 0x148) == 0
    assert any(p in members for group in n.maps(model) for members in group.values())
    listener = n.state(model)['listener']
    assert listener['registered'] == listener['enabled'] == 1 and listener['paused'] == 0
    child = n.q(r + 0x2b8)
    children = n.items(n.q(r + 0x140))
    assert child in children and n.q(child + 0x148) == r
    target.update(renderer=r, logic=p)
    destructor_calls = []
    destructor_vas = {n.q(n.q(r)), n.q(n.q(r) + 8)}
    def destructed(u, a, size, data):
        if n.x(0) == r:
            destructor_calls.append({'pc': hex(a), 'phase': n.phase})
    for a in destructor_vas:
        n.u.hook_add(UC_HOOK_CODE, destructed, begin=a, end=a)
    for label, obj, begin, end in [('renderer', r, r + 0x2a0, r + 0x2a7),
                                  ('position', r, r + 0x38, r + 0x43),
                                  ('visibility', r, r + 0x1c1, r + 0x1c1),
                                  ('opacity', r, r + 0x1d0, r + 0x1d1),
                                  ('quad', child, child + 0x3dc, child + 0x43b),
                                  ('logic_resolution', p, p + 0xc, p + 0x13)]:
        def written(u, access, where, size, value, data, label=label, obj=obj):
            writes.append({'object': label, 'offset': hex(where - obj), 'size': size,
                           'value': value, 'before': int.from_bytes(u.mem_read(where, size), 'little'),
                           'pc_elf_va': hex(u.reg_read(UC_ARM64_REG_PC)), 'phase': n.phase})
        n.u.hook_add(UC_HOOK_MEM_WRITE, written, begin=begin, end=end)

    def effective():
        t = n.q(model + 0x30)
        return n.i(t + 0x20) - n.i(t + 0x28)

    def snapshot(label):
        row = {'label': label, 'E': effective(), 'wall': n.now,
               'director_frame': n.i(n.director + 0x134), 'scene_stamp': n.i(scene + 0x4d0),
               'track_refresh_stamp': n.i(track + 0x3dc), 'active': p in n.items(model, 0xa0),
               'chart_owned': p in n.items(chart, 0x20), 'renderer_retained': r in n.items(track, 0x3b8),
               'logic_renderer': hex(n.q(p + 0x40)), 'renderer_logic': hex(n.q(r + 0x2a8)),
               'renderer_parent': hex(n.q(r + 0x148)), 'child_parent': hex(n.q(child + 0x148)),
               'depth': [n.i(p + 0x30), n.i(p + 0x34)],
               'consumed': n.u.mem_read(p + 0xd, 1)[0], 'missed': n.u.mem_read(p + 0xc, 1)[0],
               'input_enabled': n.u.mem_read(p + 0x54, 1)[0],
               'cache_xy': [n.i(r + 0x2a0), n.i(r + 0x2a4)],
               'node_position': [n.f(r + 0x38 + 4 * i) for i in range(3)],
               'quad_positions': [[n.f(child + 0x3dc + 24 * j + 4 * i) for i in range(3)] for j in range(4)],
               'visible': n.u.mem_read(r + 0x1c1, 1)[0],
               'opacity': list(n.u.mem_read(r + 0x1d0, 2)),
               'child_visible': n.u.mem_read(child + 0x1c1, 1)[0],
               'child_opacity': list(n.u.mem_read(child + 0x1d0, 2)),
               'counts': dict(counts), 'tap_refreshes': sum(c['pc'] == '0xf20c28' for c in calls),
               'score': {'score': n.i(score + 0x14), 'shining': n.i(score + 0x20), 'PURE': n.i(score + 0x24),
                         'FAR': n.i(score + 0x28), 'LOST': n.i(score + 0x2c),
                         'health': n.f(n.items(score, 0xa0)[0] + 0x10)}}
        snapshots.append(row)
        return row

    initial = snapshot('native renderer before original traversal')
    assert initial['tap_refreshes'] == 0
    # Restore the complete original Node visit, not a hand-selected renderer callback.
    assert 0x129c924 in n.hooks
    del n.hooks[0x129c924]
    frame(n, n.now + 1, 'cpu native preroll')
    assert frame(n, n.now + 3001, 'cpu native music anchor')['E'] == 0
    for e in [1000, 1300, 1499, 1500]:
        before = len(calls)
        f = frame(n, n.now + e - effective(), 'cpu E' + str(e))
        row = snapshot('E' + str(e))
        assert f['E'] == f['lastModelE'] == e and row['active']
        updates = [c for c in calls[before:] if c['pc'] == '0xf20c28']
        assert len(updates) == 1 and updates[0]['lr_elf_va'] == '0xb1646c' and [c['x1_on_entry'] for c in calls[before:] if c['pc'] == '0xcf2640'] == [e]
        assert sum(c['pc'] == '0x10a7550' for c in calls[before:]) == 1
        assert sum(c['pc'] == '0x19069a0' for c in calls[before:]) == 1
        assert n.q(track + 0x2c8) == model + 0xa0
        assert row['cache_xy'] == [212, 4]
        assert row['node_position'] == [212.0, 4.0, float(row['depth'][0])]
        assert row['visible'] == 1 and all(math.isfinite(v) for xyz in row['quad_positions'] for v in xyz)
    # Gate A is established before any judgment or the fresh no-input case.
    assert any(w['object'] == 'quad' for w in writes)
    assert any(w['object'] == 'position' for w in writes)
    if judged:
        camera = n.q(n.q(model + 0x20) + 0x2a8)
        point, out = n.alloc(12), n.alloc(8)
        for i, v in enumerate([425.0 * (lane - 3.5), 0.0, 0.0]):
            n.wf(point + 4 * i, v)
        n.call(0xbdbb70, camera, point, regs={8: out})
        xy = [n.f(out), n.f(n.director + 0x184) - n.f(out + 4)]
        n.phase = 'cpu JNI DOWN42 E1500'
        n.call(0xbe31a8, n.env, 0, 42, 987042, fs=(*xy, .5))
        hit = snapshot('after native judgment')
        assert hit['consumed'] == 1 and hit['score']['PURE'] == hit['score']['shining'] == 1
        assert [c['candidates'] for c in calls if c['pc'] == '0xeec4f0'] == [[hex(p)]]
        assert [c['primary_lane'] for c in calls if c['pc'] == '0xeec1cc'] == [lane]
        assert math.isclose(hit['score']['health'], 80.19999694824219, abs_tol=1e-6)
        assert hit['score']['score'] == 10000001 and hit['score']['FAR'] == hit['score']['LOST'] == 0
        n.phase = 'cpu JNI UP42 E1500'
        n.call(0xdda71c, n.env, 0, 42, 988042, fs=(*xy, 0))
        assert not n.items(model, 0xd0) and n.i(0x1bfebd4) == 0 and n.q(0x1bf1a90) == 0
    else:
        xy = None
    for e in [1501, 1537, 1538, 1600, 1601, 1602]:
        frame(n, n.now + e - effective(), 'cpu E' + str(e))
        snapshot('E' + str(e))
    final = snapshots[-1]
    assert final['chart_owned'] and final['renderer_retained'] and not final['active']
    assert final['logic_renderer'] == hex(r) and final['renderer_logic'] == hex(p)
    assert not any(c.get('renderer_detach') for c in calls) and not destructor_calls
    assert counts['0x965e28'] == counts['0x1730290'] == int(judged)
    assert counts['0x868e54'] == int(not judged)
    if judged:
        assert final['consumed'] == 1 and final['missed'] == 0 and final['visible'] == 1
        assert final['tap_refreshes'] == next(s for s in snapshots if s['label'] == 'E1500')['tap_refreshes']
    else:
        by_time = {s['label']: s for s in snapshots}
        assert by_time['E1538']['depth'][1] >= 301 and by_time['E1538']['visible'] == 1
        assert by_time['E1600']['missed'] == 0 and by_time['E1600']['visible'] == 1
        assert by_time['E1601']['missed'] == 1 and by_time['E1601']['visible'] == 0
        assert by_time['E1601']['active'] and final['missed'] == 1 and final['visible'] == 0
        assert final['tap_refreshes'] == by_time['E1601']['tap_refreshes']
        assert len([w for w in writes if w['object'] == 'visibility' and w['value'] == 0]) == 1
    forbidden = {0xf20c28, 0xcf2640, 0xb1638c, 0x960288, 0x19069a0, 0x10a7550,
                 0x965e28, 0x1730290, 0x868e54, 0xeec024, 0x160ce28}
    assert not forbidden.intersection(n.host_calls) and not forbidden.intersection(n.hooks)
    assert all(counts[hex(a)] == 1 for a in [0xee197c, 0xee29a8, 0xee29e8, 0xe2ea48])
    assert any(c['pc'] == '0x129c924' and c.get('node') == hex(r) for c in calls)
    assert any(c['pc'] == '0x960288' and c['target'] == hex(track) for c in calls)
    assert any(c['pc'] == '0xb1638c' and c['lr_elf_va'] == '0x96030c' for c in calls)
    assert all(counts[hex(a)] for a in [0x86a104, 0x12970c4, 0xae6740, 0x12967e4])
    return {'status': 'pass', 'case': 'judged_tap' if judged else 'unjudged_expiry',
            'identities': {'scene': hex(scene), 'model': hex(model), 'chart': hex(chart), 'track': hex(track),
                           'logic': hex(p), 'renderer': hex(r), 'child': hex(child)},
            'construction': construction, 'native_lane': lane, 'N': n.i(chart + 0xb8), 'chart_end': n.i(chart + 0xbc),
            'destructor_calls': destructor_calls, 'destructor_elf_vas': [hex(a) for a in sorted(destructor_vas)],
            'render_collection_types': dict(collections.Counter(n.typename(v) for v in renderers)),
            'renderer_children': [hex(v) for v in children], 'listener': listener,
            'jni_xy': xy, 'snapshots': snapshots, 'native_calls': calls,
            'processed_predicates': processed, 'native_writes': writes, 'native_counts': dict(counts),
            'final': final, 'host_calls_elf_va': [hex(a) for a in n.host_calls]}


def run():
    cases = []
    evidence = {}
    try:
        cases.append(run_case(True, evidence))
        evidence = {}
        cases.append(run_case(False, evidence))
    except Exception as exc:
        return {'status': 'fail', 'scenario': 'cpu_note', 'completed_cases': cases, 'partial_case': evidence,
                'native_failures': [{'type': type(exc).__name__, 'message': str(exc), 'line': traceback.extract_tb(exc.__traceback__)[-1].lineno}]}
    return {'status': 'pass', 'scenario': 'cpu_note', 'fixture': 'native_cpu_note.aff',
            'fresh_emulator_per_case': True, 'judged_tap': cases[0], 'unjudged_expiry': cases[1],
            'boundaries': {'restored_original_traversal': '0x129c924 after native activation; scoped to cpu_note',
                           'new_services': [], 'new_pc_skips': [], 'inherited_pc_skips': PC_SKIPS,
                           'retained_services': 'Existing libc/C++ABI, platform/JNI, clock/audio, catalog/profile/settings, resource and GL services; swap/framebuffer suppression and allocator/autorelease boundaries unchanged',
                           'gpu_pixels_and_complete_reclamation': 'Not verified'}}
