"""Producer-first flick diagnostic; a parsed class never substitutes runtime logic.

The verified ordinary builder has no FlickNote dispatch. Remain failed/blocked
unless a legitimate runtime producer and admission are independently established.
"""
import collections
import hashlib
import struct
import traceback
from elftools.elf.elffile import ELFFile
from unicorn import UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm64_const import UC_ARM64_REG_PC
import config
from solo_entry import setup, entry
from lifecycle import activate
from boundaries import PC_SKIPS

CAST_SITES = [0x1862f3c, 0x18632d4, 0x18636c4, 0x1863820, 0x1863a30,
              0x1863db4, 0x1863e44, 0x1864120, 0x18644a8, 0x1864624,
              0x1865620, 0x1865654]
OBSERVE = {0x1870de0, 0xdf4a58, 0x814384, 0xb01d6c, 0xa3ab64,
           0x173b358, 0x1862a14, 0x1576aa4, 0xae6740, 0xd7e290,
           0x1315a90, 0xae6e38, 0x14858d4, 0x16e0548, 0xbe31a8, 0x1706960,
           0xdda71c, 0x1730290, 0x868e54}


def producer_survey(n):
    """Inspect only known flick descriptors, their references and one allocation candidate.

    This is static evidence. The short ADRP/LDR scan is not a general decompiler
    or a proof excluding arbitrary indirect producers.
    """
    with config.elf_stream() as f:
        e = ELFFile(f)
        rels = [r for r in e.get_section_by_name('.rela.dyn').iter_relocations()
                if r['r_addend'] == 0x1a89ca0]
        refs = [{'location_elf_va': hex(r['r_offset']), 'relocation_type': r['r_info_type']} for r in rels]
        symbols = [s.name for s in e.get_section_by_name('.dynsym').iter_symbols() if 'flick' in s.name.lower()]
        text = e.get_section_by_name('.text'); buf, base = text.data(), text['sh_addr']
        loads, helper_callers = set(), []
        for i in range(0, len(buf) - 3, 4):
            w = struct.unpack_from('<I', buf, i)[0]; pc = base + i
            if w & 0xfc000000 == 0x94000000:
                imm = w & 0x3ffffff
                if imm & (1 << 25): imm -= 1 << 26
                if pc + 4 * imm == 0x16e0548: helper_callers.append(hex(pc))
            if w & 0x9f000000 != 0x90000000: continue
            imm = ((w >> 29) & 3) | (((w >> 5) & 0x7ffff) << 2)
            if imm & (1 << 20): imm -= 1 << 21
            if (pc & ~0xfff) + (imm << 12) != 0x1b96000: continue
            rd = w & 31
            for j in range(i + 4, min(i + 36, len(buf) - 3), 4):
                v = struct.unpack_from('<I', buf, j)[0]
                if v & 0xfc000000 in (0x14000000, 0x94000000): break
                if v & 0x9f000000 == 0x90000000 and v & 31 == rd: break
                if (v >> 5) & 31 != rd: continue
                if v & 0xffc00000 != 0xf9400000: continue
                if ((v >> 10) & 0xfff) * 8 == 0x4d0: loads.add(base + j)
                if v & 31 == rd: break
        raw = []
        needle = struct.pack('<Q', 0x1a89ca0)
        for section in e.iter_sections():
            if section['sh_type'] != 'SHT_PROGBITS' or not section['sh_flags'] & 2 or section['sh_flags'] & 4: continue
            data = section.data(); offset = data.find(needle)
            while offset >= 0:
                if offset % 8 == 0: raw.append(hex(section['sh_addr'] + offset))
                offset = data.find(needle, offset + 1)
    assert refs == [{'location_elf_va': '0x1b964d0', 'relocation_type': 1027}]
    assert not symbols and not raw and n.q(0x1b964d0) == 0x1a89ca0
    renderer_vtable = n.q(0x1b96b90) + 0x10
    renderer_type = n.cstr(n.q(n.q(renderer_vtable - 8) + 8)).decode()
    assert renderer_type == '15RenderFlickNote' and renderer_vtable == 0x1b7b680
    assert n.q(renderer_vtable + 0x538) == 0x1315a90
    return {'classification': 'Type/descriptor evidence only',
            'logic_typeinfo_elf_va': '0x1a89ca0', 'logic_name': n.cstr(n.q(0x1a89ca8)).decode(),
            'base_typeinfo_elf_va': hex(n.q(0x1a89cb0)),
            'relocation_references': refs, 'raw_aligned_data_references': raw, 'flick_dynamic_symbols': symbols,
            'known_got_loads_elf_va': [hex(a) for a in sorted(loads)],
            'gesture_helper_direct_callers_elf_va': helper_callers,
            'concrete_logic_vtable': None, 'logic_allocation_or_initializer': None,
            'alternative_candidate': {'classification': 'Disconfirmed candidate',
                'function_elf_va': '0xae6740', 'condition_elf_va': '0xae6e30',
                'allocation_callsite_elf_va': '0xae6e38', 'allocation_bytes': 0x2d0,
                'vtable_store_elf_va': '0xae6e60', 'vtable_elf_va': hex(renderer_vtable),
                'actual_type': renderer_type, 'initializer_elf_va': '0x1315a90',
                'input_logic_link_store_elf_va': '0x1315ae4',
                'reason': 'Creates RenderFlickNote using an already-existing logic object; does not produce LogicFlickNote'},
            'other_references': {'0xb166b0': 'Renderer traversal RTTI consumer',
                '0xe66008': 'Existing renderer/feedback consumer', '0xf8067c': 'Existing-note lifecycle dispatch',
                '0x11ea158': 'Existing-note judgment count', '0x1485cd8': 'Continuous-input cast'},
            'scope': 'Complete ordinary builder dispatch; known RTTI/GOT/relative and raw data references, short ADRP/LDR references, dynamic symbols and direct helper callers; one renderer-allocation candidate. Arbitrary indirect/special-mode producers remain unknown',
            'alternate_context': 'Not attempted: no instruction-backed alternative logic producer justifies changing mode/catalog'}


def run():
    evidence = {'status': 'fail', 'scenario': 'flick_producer', 'fixture': 'native_flick_probe.aff',
                'gates': {'whole_aff_and_builder': 'incomplete', 'runtime_producer': 'incomplete',
                          'gameplay_admission': 'not_run', 'jni_gesture': 'not_run'},
                'pc_skips_elf_va': PC_SKIPS, 'native_failures': []}
    try:
        return investigate(evidence)
    except Exception as exc:
        evidence['native_failures'].append({'type': type(exc).__name__, 'message': str(exc),
                                           'line': traceback.extract_tb(exc.__traceback__)[-1].lineno})
        return evidence


def investigate(evidence):
    n = setup(True)
    n.prepare_runtime()
    n.observe |= OBSERVE
    parsed, casts, decisions, parsed_writes, render_checks = [], [], [], [], collections.Counter()
    evidence.update(parsed_flicks=parsed, native_casts=casts, builder_decisions=decisions,
                    parsed_native_writes=parsed_writes, render_candidate_comparison_counts=render_checks)
    chart = None
    current = None

    def written(u, access, where, size, value, data):
        parsed_writes.append({'offset': hex(where - data), 'size': size, 'value': value,
                             'pc_elf_va': hex(u.reg_read(UC_ARM64_REG_PC))})

    def object_state(p):
        name = n.typename(p)
        return {'pointer': hex(p), 'type': name, 'vtable_elf_va': hex(n.q(p)),
                'group': n.i(p + (0x50 if 'Logic' in name else 8)), 'time': n.i(p + 0x18)}

    def observe(u, a, size, data):
        nonlocal chart, current
        if a == 0xa3ad40:
            p = n.x(0)
            evidence['parsed_allocation'] = {'pointer': hex(p), 'bytes': 0x30, 'callsite_elf_va': '0xa3ad3c'}
            u.hook_add(UC_HOOK_MEM_WRITE, written, p, begin=p, end=p + 0x2f)
        elif a == 0xa3ad68:
            p = n.x(0)
            row = object_state(p)
            row.update(floats=[n.f(p + 0x1c + 4*i) for i in range(4)],
                       initializer='Inline native stores a3ad4c-a3ad64')
            parsed.append(row)
        elif a == 0x1862a14:
            chart = n.x(0); source = n.x(1)
            evidence['builder_input'] = {'chart': hex(chart), 'parsed_chart': hex(source),
                'parsed_events': [object_state(p) for p in n.items(source, 0x18)],
                'runtime_vector_before': [hex(p) for p in n.items(chart, 0x20)]}
        elif a == 0x1863d80:
            p = n.x(23)
            current = {**object_state(p), 'casts': [],
                       'runtime_size_before': len(n.items(chart, 0x20))}
        elif a in CAST_SITES:
            ti = n.x(2)
            row = {'callsite_elf_va': hex(a), 'input': hex(n.x(0)),
                   'source_typeinfo_elf_va': hex(n.x(1)), 'target_typeinfo_elf_va': hex(ti),
                   'target_name': n.cstr(n.q(ti + 8)).decode()}
            casts.append(row)
            if current is not None and row['input'] == current['pointer']: current['casts'].append(row)
        elif a - 4 in CAST_SITES:
            casts[-1]['result'] = hex(n.x(0))
            if a == 0x1864628 and current is not None:
                current.update(last_cast_result=hex(n.x(0)), branch_elf_va=hex(a))
        elif a == 0x1863d60 and current is not None:
            current.update(observed_next_elf_va=hex(a), runtime_size_after=len(n.items(chart, 0x20)))
            decisions.append(current); current = None
        elif a == 0x18655b4:
            evidence['builder_runtime_products'] = [object_state(p) for p in n.items(chart, 0x20)]
        elif a == 0xae6e30:
            # Compare operands are RTTI name pointers, not constructor arguments.
            actual = n.cstr(n.x(8)).decode(); required = n.cstr(n.x(9)).decode()
            render_checks[actual + ' == ' + required + ': ' + str(n.x(8) == n.x(9))] += 1
    points = [0xa3ad40, 0xa3ad68, 0x1862a14, 0x1863d80, 0x1863d60, 0x1864628, 0x18655b4, 0xae6e30]
    for a in set(points + CAST_SITES + [a + 4 for a in CAST_SITES]):
        n.u.hook_add(UC_HOOK_CODE, observe, begin=a, end=a)
    n.phase = '033 complete original static initializer'
    n.call(0x1930604); n.call(0x1054f24)
    evidence['producer_survey'] = producer_survey(n)
    n.trace = []; n.visual = []; n.animationTrace = []; n.downstream = []
    n.env = n.alloc(8); n.now = 1000
    entry(n)
    activate(n)
    scene, model = n.scene, n.model
    assert chart == n.q(model + 0x28) == n.q(scene + 0x3e8)
    runtime = n.items(chart, 0x20)
    types = [n.typename(p) for p in runtime]
    evidence.update(objects={'scene': hex(scene), 'model': hex(model), 'chart': hex(chart)},
                    initializer_return=n.sceneInitReturn, runtime_objects=[object_state(p) for p in runtime if n.typename(p) != '8LogicBar'],
                    runtime_object_types=dict(collections.Counter(types)),
                    native_N=n.i(chart + 0xb8), chart_end=n.i(chart + 0xbc),
                    whole_chart_md5=n.string(chart + 0xf8).decode(),
                    active_objects=[hex(p) for p in n.items(model, 0xa0)], listener=n.state(model)['listener'])
    assert evidence['listener']['registered'] == evidence['listener']['enabled'] == 1
    assert evidence['listener']['paused'] == 0
    assert len(parsed) == 1 and parsed[0]['type'] == '9FlickNote' and parsed[0]['vtable_elf_va'] == '0x1b653c0'
    assert parsed[0]['time'] == 1500 and parsed[0]['floats'] == [0., .5, 1., 0.] and parsed[0]['group'] == 0
    assert not n.items(model, 0xd0) and n.i(0x1bfebd4) == 0 and n.q(0x1bf1a90) == 0
    assert types.count('12LogicTapNote') == 1 and set(types) == {'8LogicBar', '12LogicTapNote'} and n.i(chart + 0xb8) == 1 and n.i(chart + 0xbc) == 1620
    flick = next(d for d in decisions if d['type'] == '9FlickNote')
    assert flick['pointer'] == parsed[0]['pointer'] and flick['last_cast_result'] == '0x0'
    assert flick['branch_elf_va'] == '0x1864628' and flick['observed_next_elf_va'] == '0x1863d60'
    assert [c['target_name'] for c in flick['casts']] == ['10SimpleNote', '13CameraControl', '12SceneControl', '8HoldNote', '7ArcNote']
    assert all(c['result'] == '0x0' for c in flick['casts'])
    assert flick['runtime_size_before'] == flick['runtime_size_after']
    assert n.sceneInitReturn == 1 and n.q(n.director + 0x140) == scene and n.q(n.director + 0x148) == 0
    assert n.q(scene + 0x3e0) == model and n.q(n.q(scene + 0x300) + 0x2b8)
    tap = next(p for p in runtime if n.typename(p) == '12LogicTapNote')
    assert n.i(tap + 0x18) == 1500 and n.i(n.q(tap + 0x20) + 0x10) == 4
    evidence['control_tap_index_keys'] = [[k for k, ps in g.items() if tap in ps] for g in n.maps(model)]
    assert any(evidence['control_tap_index_keys'])
    assert n.q(tap + 0x40) and n.typename(n.q(tap + 0x40)) == '13RenderTapNote'
    assert evidence['whole_chart_md5'] == hashlib.md5(config.fixture_text().encode()).hexdigest()
    counts = collections.Counter(e['pc'] for e in n.events)
    evidence['native_call_counts'] = {hex(a): counts[hex(a)] for a in OBSERVE | {0xee197c, 0xee29a8, 0xee29e8, 0xe2ea48}}
    for a in [0xee197c, 0xee29a8, 0xee29e8, 0xe2ea48, 0x1870de0, 0xa3ab64, 0x1862a14]: assert counts[hex(a)] == 1
    for a in [0x1315a90, 0x16e0548, 0xbe31a8, 0x1706960, 0xdda71c, 0xae6e38, 0x1730290, 0x868e54]: assert counts[hex(a)] == 0
    forbidden = {0x1870de0, 0xa3ab64, 0x1862a14, 0x1315a90, 0x16e0548, 0x14858d4, 0x1730290, 0x868e54, 0xe2ea48}
    assert not forbidden.intersection(n.host_calls) and not forbidden.intersection(n.hooks)
    evidence.update(gates={'whole_aff_and_builder': 'verified_native_execution', 'runtime_producer': 'blocked',
                          'gameplay_admission': 'not_run_no_runtime_flick', 'jni_gesture': 'not_run_gate_A_failed'},
        blocker={'branch_elf_va': '0x1864628', 'observed_edge': '0x1864628 -> 0x1863d60',
                 'cause': 'All five original parsed-type casts fail; default branch omits FlickNote',
                 'minimum_prerequisite': 'A concrete original LogicFlickNote allocation/initializer and reachable caller producing valid owned state; no justified alternate context found'},
        native_failures=[{'type': 'NativeFlickProducerUnresolved',
                          'message': 'Whole AFF creates FlickNote but native builder omits it; inspected renderer allocation is a consumer, not a runtime logic producer. Gesture gate not entered.'}],
        supplied_services='Unchanged024-032 ABI/RTTI/string/stream/platform/catalog/profile/settings/resource/clock/graphics/audio boundaries; synthetic AFF; no new service or PC skip. Original base traversal stays at its existing boundary in this construction diagnostic.',
        endpoint={'running_scene': hex(n.q(n.director + 0x140)), 'pending': n.q(n.director + 0x148),
                  'retained_contacts': len(n.items(model, 0xd0)), 'engine_mask': n.i(0x1bfebd4),
                  'jni_input': 'not_executed', 'native_runtime_flicks': 0, 'mapping_root': n.q(0x1bf1a90)})
    return evidence  # Deliberate fail: successful observation does not pass the producer gate.
