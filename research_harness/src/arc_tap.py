"""Native AFF parent/child construction and JNI hit/duplicate scenario; stops before results."""
import collections
import math
from unicorn import UC_HOOK_CODE, UC_HOOK_MEM_READ, UC_HOOK_MEM_WRITE
from unicorn.arm64_const import UC_ARM64_REG_PC, UC_ARM64_REG_SP
from solo_entry import setup, entry
from lifecycle import activate, frame
from boundaries import PC_SKIPS
from arc_tap_services import install


def run():
    n = setup(True)
    abi = install(n)
    n.prepare_runtime()
    n.call(0x1054f24)
    addresses = {0xc2cb1c, 0x924b50, 0x173b358, 0x1862a14, 0x1864e18,
                 0x173a778, 0x1864e1c, 0x178f7fc, 0x1925084, 0x11ea120,
                 0xeec024, 0xeec47c, 0xeec480, 0x927384, 0x160ce28,
                 0xc78814, 0x1730290, 0xbe31a8, 0xdda71c, 0x194ff80}
    n.observe |= addresses
    parsed, created, writes, spatial, consumed_reads = [], [], [], [], []

    def observe(u, address, size, data):
        if address == 0x1864e18:
            arc = n.x(27)
            begin, end = n.q(arc + 0x70), n.q(arc + 0x78)
            parsed.append({'mode': n.i(arc + 0x68), 'times': [n.i(p) for p in range(begin, end, 4)],
                           'endpoints': [n.f(arc + off) for off in [0x20, 0x24, 0x40, 0x44]],
                           'child_time_argument': n.x(0), 'pc': hex(address)})
        elif address == 0x1864e1c:
            child = n.x(0)
            created.append({'pointer': hex(child), 'vtable': hex(n.q(child)),
                            'type': n.typename(child), 'ref_at_factory_return': n.i(child + 8)})
            def written(u, access, where, size, value, data):
                writes.append({'pc': hex(u.reg_read(UC_ARM64_REG_PC)), 'offset': hex(where - child),
                               'size': size, 'value': hex(value)})
            def read(u, access, where, size, value, data):
                consumed_reads.append({'pc': hex(u.reg_read(UC_ARM64_REG_PC)),
                                       'phase': n.phase, 'consumed': n.u.mem_read(child + 0xd, 1)[0]})
            u.hook_add(UC_HOOK_MEM_WRITE, written, begin=child + 0x80, end=child + 0x97)
            u.hook_add(UC_HOOK_MEM_READ, read, begin=child + 0xd, end=child + 0xd)
        elif address == 0xeec480:
            sp = u.reg_read(UC_ARM64_REG_SP)
            spatial.append({'phase': n.phase, 'accepted': n.x(0) & 1, 'child': hex(n.x(28)),
                            'target_xy': [n.f(sp + 0x38), n.f(sp + 0x3c)],
                            'projected_point': [n.f(sp + 0x40 + i * 4) for i in range(3)]})
    for address in [0x1864e18, 0x1864e1c, 0xeec480]:
        n.u.hook_add(UC_HOOK_CODE, observe, begin=address, end=address)
    n.trace = []; n.visual = []; n.animationTrace = []; n.downstream = []
    n.env = n.alloc(8); n.now = 1000
    entry(n)
    activate(n)
    scene, model = n.scene, n.model
    assert n.sceneInitReturn == 1
    chart = n.q(model + 0x28)
    parents = [p for p in n.items(chart, 0x20) if n.typename(p) == '12LogicArcNote']
    assert len(parents) == 1 and len(created) == 1 and len(parsed) == 1
    parent = parents[0]
    children = n.items(parent, 0x120)
    assert len(children) == 1
    child = children[0]
    assert hex(child) == created[0]['pointer'] and 'LogicArcTapNote' in created[0]['type']
    assert n.q(child + 0x90) == parent and n.i(parent + 0xa4) == 1
    assert parsed[0]['mode'] == 1 and parsed[0]['times'] == [1500]
    assert parsed[0]['endpoints'] == [.5, .5, .5, .5]
    assert n.i(child + 0x18) == parsed[0]['child_time_argument'] == 1500
    assert any(w['offset'] == '0x90' and int(w['value'], 16) == parent and w['pc'] == '0x1865514' for w in writes)
    assert any(w['offset'] == '0x80' and w['pc'] == '0x1925888' for w in writes)
    assert any(w['offset'] == '0x88' and w['pc'] == '0x192588c' for w in writes)
    total = n.i(chart + 0xb8)
    assert total == 1, ('unexpected native denominator', total)
    assert n.i(child + 0x50) == n.i(parent + 0x50)
    geometry = [n.f(child + 0x80 + i * 4) for i in range(3)]
    assert all(math.isfinite(v) for v in geometry)
    frame(n, n.now + 1, 'arc-tap preroll')
    row = frame(n, n.now + 3001, 'arc-tap native music anchor')
    row = frame(n, n.now + n.i(child + 0x18) - row['E'], 'arc-tap judgment frame')
    assert row['E'] == 1500 and n.q(n.director + 0x140) == scene
    # The ordinary candidate uses geometry XY + quantized parent X on the Z=0 input plane.
    # Sampler-local geometry Z is recorded, not overwritten or assumed to be this input plane.
    assert n.u.mem_read(chart + 0x110, 1)[0] == 0
    world = [geometry[0] + int(850 * n.f(n.q(parent + 0x20) + 0x14) - 425), geometry[1], 0.0]
    point, out = n.alloc(12), n.alloc(8)
    for i, value in enumerate(world):
        n.wf(point + i * 4, value)
    camera = n.q(n.q(model + 0x20) + 0x2a8)
    n.call(0xbdbb70, camera, point, regs={8: out})
    contact = [n.f(out), n.f(n.director + 0x184) - n.f(out + 4)]
    assert all(math.isfinite(v) for v in contact)
    score = n.q(model + 0x38)
    gauge = n.items(score, 0xa0)[0]
    def state():
        return {'score': n.i(score + 0x14), 'shining': n.i(score + 0x20),
                'PURE': n.i(score + 0x24), 'FAR': n.i(score + 0x28), 'LOST': n.i(score + 0x2c),
                'health': n.f(gauge + 0x10), 'consumed': n.u.mem_read(child + 0xd, 1)[0]}
    before = state()
    for pid, phase in [(42, 'arc_tap_positive'), (43, 'arc_tap_duplicate')]:
        n.phase = phase
        n.call(0xbe31a8, n.env, 0, pid, 987000 + pid, fs=(*contact, .5))
        n.call(0xdda71c, n.env, 0, pid, 988000 + pid, fs=(*contact, 0))
        assert len(n.items(model, 0xd0)) == 0 and n.i(0x1bfebd4) == 0
        if pid == 42:
            after = state()
        else:
            duplicate = state()
    counts = collections.Counter(e['pc'] for e in n.events)
    assert before['PURE'] == before['consumed'] == 0
    assert after['PURE'] - before['PURE'] == after['shining'] - before['shining'] == 1
    assert after['FAR'] == after['LOST'] == 0 and after['consumed'] == 1
    assert after['score'] == 10000000 + after['shining']  # native N=1, all-PURE path
    assert duplicate == after
    assert len(spatial) == 2 and all(s['accepted'] == 1 and s['child'] == hex(child) for s in spatial)
    assert any(r['phase'] == 'arc_tap_duplicate' and r['consumed'] == 1 and r['pc'] == '0x180cf28' for r in consumed_reads)
    assert counts['0xc78814'] == counts['0x1730290'] == 1
    assert counts['0x160ce28'] == counts['0xbe31a8'] == counts['0xdda71c'] == counts['0x194ff80'] == 2
    assert [e['x'][1] for e in n.events if e['pc'] == '0x160ce28'] == [hex(child), hex(child)]
    assert [e['x'][0] for e in n.events if e['pc'] == '0xc78814'] == [hex(child)]
    assert counts['0xee197c'] == counts['0xe4e4dc'] == counts['0xe2ea48'] == 1 and counts['0xdd0f90'] == 0
    assert counts['0xc27d34'] == 0 and n.q(score + 0x68) == 0
    forbidden = {0xe4e4dc, 0xe2ea48, 0x1862a14, 0x173a778, 0x178f7fc, 0x1925084,
                 0x10a7550, 0xc78814, 0x160ce28, 0x1730290}
    assert not forbidden.intersection(n.host_calls)
    assert not forbidden.intersection(n.hooks)
    assert n.q(scene + 0x3e0) == model and n.q(scene + 0x3e8) == chart and n.q(child + 0x90) == parent
    return {'status': 'pass', 'fixture': 'native_arc_tap.aff', 'parsed_arc': parsed[0],
            'native_call_counts': {hex(a): counts[hex(a)] for a in addresses | {0xee197c, 0xe4e4dc, 0xe2ea48, 0xc27d34}},
            'native_objects': {'game_scene': hex(scene), 'model': hex(model), 'chart': hex(chart),
                               'parent': hex(parent), 'parent_vtable': hex(n.q(parent)), 'parent_mode': n.i(parent + 0xa4),
                               'child': created[0], 'child_ref': n.i(child + 8), 'child_parent': hex(n.q(child + 0x90))},
            'native_chart': {'judgment_units': total, 'end': n.i(chart + 0xbc), 'main_objects': len(n.items(chart, 0x20)),
                             'timing_group': n.i(child + 0x50), 'input_mode110': 0},
            'construction_writes': writes, 'native_child_geometry': geometry,
            'projection': {'routine_elf_va': '0xbdbb70', 'world_input_plane_point': world, 'jni_xy': contact, 'effective_time': row['E']},
            'spatial_checks': spatial, 'before': before, 'after_hit': after, 'after_duplicate': duplicate,
            'consumption_guard_reads': consumed_reads, 'abi_services': dict(collections.Counter(x['service'] for x in abi)),
            'sscanf_formats': sorted(set(x['format'] for x in abi if x['service'] == 'sscanf')),
            'resource_paths': sorted(set(x['path'] for x in n.resourceLog if x['path'].endswith(('.obj', '.mtl')))),
            'identity_checks': {'native_parent_child_links': True, 'native_geometry_writes': True,
                                'same_child_judged': True, 'duplicate_spatially_eligible': True,
                                'native_consumption_guard': True, 'no_direct_host_builder_or_judge': True},
            'pc_skips_elf_va': PC_SKIPS, 'native_failures': [],
            'endpoint': 'after duplicate cleanup; no completion/results/SQLite replay'}
