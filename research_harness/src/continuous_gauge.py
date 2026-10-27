"""Producer-gated special-gauge audit. No special character/ability is fabricated.

Only ordinary_control enters gameplay. Each target producer phase inspects a fresh
fixture and the original input contracts, then stops before unjustified selection.
"""
import collections
import json
import math
import struct
import traceback
import zipfile
from unicorn import UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm64_const import UC_ARM64_REG_PC
import config
from solo_entry import setup, entry
from lifecycle import activate, frame
from boundaries import PC_SKIPS

OBSERVE = {0xee197c, 0xee29a8, 0xee29e8, 0xe2ea48, 0x96b358, 0x100ec3c,
           0xa44128, 0x7ac3cc, 0xca5ec8, 0xaf8734, 0x118e220, 0x9e979c,
           0x179727c, 0x1003b90, 0xfbfd04, 0x14f0a94, 0x13e00b4,
           0x12c5070, 0x160a3b8, 0x10a7550, 0xa126f4, 0x83dd70,
           0x83ddd8, 0x83df48, 0x18e2d6c, 0xa3b33c, 0x1a6e120,
           0xbe31a8, 0xdda71c, 0x1730290, 0x16e4ab0, 0x868e54,
           0xc27d34, 0x1600bb0}
FLOAT_FIELDS = {0x10: 'H', 0x14: 'L', 0x18: 'U', 0x20: 'p', 0x24: 'floor',
                0x28: 'override', 0x2c: 'baseline', 0x30: 'accumulator',
                0x34: 'positive', 0x38: 'negative', 0x40: 'F', 0x44: 'recovery', 0x8c: 'base_gain'}


def account_boundary(n):
    c = n.q(n.account + 0x58)
    return {'classification': 'External supplied input', 'account': hex(n.account),
            'selected_character': hex(c), 'selected_id': n.i(c + 0xc),
            'selected_character_vtable': hex(n.q(c)), 'selected_ability': hex(n.q(c + 0xd0)),
            'character_rows': [hex(p) for p in n.items(n.account, 0x18)],
            'fallback_row': hex(n.q(n.account + 0x68)),
            'getter_elf_va': '0xb688e0 (existing supplied account service)',
            'original_character_initializer_called_by_driver': 0x100ec3c in n.host_calls,
            'origin': 'Existing prepare_app character49 shell, not an original owned-character initializer product'}


def metadata():
    with zipfile.ZipFile(config.archive_path) as archive:
        chars = json.loads(archive.read('assets/char/characters.json'))
    return {c['character_id']: c for c in chars}


def ordinary_control(evidence):
    n = setup(True)
    n.prepare_runtime()
    n.observe |= OBSERVE
    writes, creation, selection, updates, samples = [], [], [], [], []
    evidence.update(native_writes=writes, creation=creation, selection=selection,
                    temporal_calls=updates, samples=samples, account=account_boundary(n))

    def watched(u, access, address, size, value, data):
        label, obj = data
        writes.append({'object': label, 'offset': hex(address - obj), 'size': size, 'value': value,
                       'before': int.from_bytes(u.mem_read(address, size), 'little'),
                       'pc_elf_va': hex(u.reg_read(UC_ARM64_REG_PC)), 'phase': n.phase})

    def watch(label, obj, start, end):
        n.u.hook_add(UC_HOOK_MEM_WRITE, watched, (label, obj), begin=obj + start, end=obj + end)

    def observed(u, pc, size, unused):
        if pc == 0xe4e4dc:
            watch('scene', n.x(0), 0x324, 0x33f)
        elif pc == 0xee25e8:
            c = n.q(n.x(0) + 0x58)
            selection.append({'pc_elf_va': hex(pc), 'character': hex(c), 'id': n.i(c + 0xc),
                              'ability': hex(n.x(28)), 'native_next_if_null': '0xee25ac'})
        elif pc == 0xee25ac:
            selection.append({'pc_elf_va': hex(pc), 'native_action': 'mov w27,0: no accepted ability'})
        elif pc in {0xfbfd04, 0x13e00b4, 0x160a3b8}:
            label = {0xfbfd04: 'model', 0x13e00b4: 'score', 0x160a3b8: 'gauge'}[pc]
            creation.append({'pc_elf_va': hex(pc), 'object': label, 'pointer': hex(n.x(0)),
                             'lr_elf_va': hex(n.x(30)), 'arguments': [hex(n.x(i)) for i in range(8)]})
            if label == 'model':
                watch(label, n.x(0), 0x144, 0x147)
                watch(label, n.x(0), 0x80, 0x87)
            elif label == 'score':
                watch(label, n.x(0), 0x90, 0x97)
                watch(label, n.x(0), 0xc8, 0xcf)
        elif pc == 0x12c50b8:
            evidence['gauge_allocation'] = {'pointer': hex(n.x(0)), 'size': 0xd8,
                'allocator_initial_p': n.f(n.x(0) + 0x20),
                'initial_zero_classification': 'External allocator zeroing; native constructors execute next'}
            watch('gauge', n.x(0), 0xc, 0xd0)
        elif pc == 0x12c5188:
            evidence['gauge_initializer_return'] = n.x(0)
        elif pc in {0xa126f4, 0x83dd70}:
            updates.append({'pc_elf_va': hex(pc), 'object': hex(n.x(0)), 'E_argument': struct.unpack('<i', struct.pack('<I', n.x(1) & 0xffffffff))[0],
                            'phase': n.phase, 'lr_elf_va': hex(n.x(30))})
    for pc in [0xe4e4dc, 0xee25e8, 0xee25ac, 0xfbfd04, 0x13e00b4, 0x12c50b8,
               0x160a3b8, 0x12c5188, 0xa126f4, 0x83dd70]:
        n.u.hook_add(UC_HOOK_CODE, observed, begin=pc, end=pc)
    n.call(0x1930604); n.call(0x1054f24)
    n.trace = []; n.visual = []; n.animationTrace = []; n.downstream = []
    n.env = n.alloc(8); n.now = 1000
    entry(n); activate(n)
    scene, model = n.scene, n.model
    chart, score = n.q(model + 0x28), n.q(model + 0x38)
    gauges = n.items(score, 0xa0)
    mode_map = {}
    def visit(p):
        if not p: return
        visit(n.q(p))
        mode_map[n.i(p + 0x20)] = [n.i(a) for a in range(n.q(p + 0x28), n.q(p + 0x30), 4)]
        visit(n.q(p + 8))
    visit(n.q(0x1bf9650))
    assert all(mode_map[m] == [m] for m in [0, 6, 11]) and 0x1905bc8 in n.host_calls
    evidence['native_mode_map'] = {str(m): mode_map[m] for m in [0, 6, 11]}
    evidence['native_map_initializer_elf_va'] = '0x1905bc8 (original selected bootstrap initializer)'
    evidence['catalog_selection'] = {'song_id': n.string(n.song).decode(), 'difficulty': 0, 'set': n.string(n.song + 0x198).decode()}
    context = n.q(n.app + 0xe0)
    evidence['session_context'] = {'pointer': hex(context), 'word_38': n.i(context + 0x38)}
    assert len(gauges) == 1
    g = gauges[0]
    assert n.sceneInitReturn == evidence['gauge_initializer_return'] == 1
    assert n.q(scene + 0x330) == n.character and n.q(scene + 0x338) == 0
    assert n.i(scene + 0x324) == n.i(model + 0x144) == n.i(score + 0x94) == n.i(g + 0xa0) == 0
    assert n.q(g + 0xa8) == score and n.q(score + 0x60) == chart
    assert n.q(score + 0xc8) == n.q(g + 0xc8) == n.q(model + 0x80) == 0
    assert n.q(n.director + 0x140) == scene and n.q(n.director + 0x148) == 0

    def effective():
        t = n.q(model + 0x30)
        return n.i(t + 0x20) - n.i(t + 0x28)

    def sample(label):
        row = {'label': label, 'E': effective(), 'wall': n.now,
               'director_frame': n.i(n.director + 0x134),
               'outer_mode': n.i(score + 0x94), 'gauge_id': n.i(g + 0xa0),
               'fields': {name: n.f(g + off) for off, name in FLOAT_FIELDS.items()},
               'continuous_enabled': n.u.mem_read(g + 0x1d, 1)[0], 'last_update_E': n.i(g + 0xb4),
               'cap_enabled': n.u.mem_read(g + 0x1c, 1)[0], 'finished': n.u.mem_read(model + 0x139, 1)[0],
               'PURE': n.i(score + 0x24), 'LOST': n.i(score + 0x2c), 'score': n.i(score + 0x14)}
        samples.append(row); return row
    sample('ordinary activated')
    frame(n, n.now + 1, '034 ordinary preroll')
    assert frame(n, n.now + 3001, '034 ordinary music anchor')['E'] == 0
    for e in [500, 1000]:
        assert frame(n, n.now + e - effective(), '034 ordinary E' + str(e))['E'] == e
        sample('ordinary E' + str(e))
    tap = next(p for p in n.items(chart, 0x20) if n.typename(p) == '12LogicTapNote' and n.i(p + 0x18) == 1000)
    lane = n.i(n.q(tap + 0x20) + 0x10)
    camera = n.q(n.q(model + 0x20) + 0x2a8)
    point, out = n.alloc(12), n.alloc(8)
    for i, v in enumerate([425.0 * (lane - 3.5), 0., 0.]): n.wf(point + 4*i, v)
    n.call(0xbdbb70, camera, point, regs={8: out})
    xy = [n.f(out), n.f(n.director + 0x184) - n.f(out + 4)]
    n.phase = '034 ordinary JNI DOWN42'
    n.call(0xbe31a8, n.env, 0, 42, 987042, fs=(*xy, .5))
    n.phase = '034 ordinary JNI UP42'
    n.call(0xdda71c, n.env, 0, 42, 988042, fs=(*xy, 0))
    frame(n, n.now + 1, '034 ordinary E1001')
    final = sample('ordinary post-judgment E1001')
    assert final['PURE'] == 1 and final['LOST'] == 0
    assert math.isclose(final['fields']['H'], 40.20000076293945, abs_tol=1e-6)
    assert not n.items(model, 0xd0) and n.i(0x1bfebd4) == 0 and n.q(0x1bf1a90) == 0
    assert any(w['object'] == 'gauge' and w['pc_elf_va'] == '0x12c5144' and w['value'] == 0 for w in writes)
    counts = collections.Counter(e['pc'] for e in n.events)
    for a in [0xee197c, 0xee29a8, 0xee29e8, 0xe2ea48, 0xfbfd04, 0x13e00b4, 0x160a3b8, 0x1730290]:
        assert counts[hex(a)] == 1, (hex(a), counts[hex(a)])
    for a in [0x96b358, 0x100ec3c, 0xa44128, 0x7ac3cc, 0x118e220, 0x9e979c,
              0x179727c, 0x1003b90, 0x83ddd8, 0x83df48, 0x1a6e120, 0xc27d34, 0x1600bb0]:
        assert counts[hex(a)] == 0, (hex(a), counts[hex(a)])
    forbidden = {0xfbfd04, 0x13e00b4, 0x160a3b8, 0x83dd70, 0xa126f4, 0x1730290, 0x10a7550}
    assert not forbidden.intersection(n.host_calls) and not forbidden.intersection(n.hooks)
    evidence.update(status='pass', native_call_counts={hex(a): counts[hex(a)] for a in OBSERVE},
        initializer_return=n.sceneInitReturn, identities={'scene': hex(scene), 'model': hex(model),
        'chart': hex(chart), 'score': hex(score), 'gauge': hex(g), 'gauge_owner': hex(n.q(g + 0xa8))},
        jni_xy=xy, final=final,
        classification='Native-produced within the executed ordinary GameScene; no special ability or gauge selected')


def target_producer(mode, catalog):
    # Fresh emulator/heap; inspect unchanged supplied inputs, do not substitute target ID.
    n = setup(True)
    boundary = account_boundary(n)
    char_id, vt, selector, factory = {6: (35, 0x1ac18f0, 0x179727c, 0xca5ec8),
                                    11: (98, 0x1b5a168, 0x1003b90, 0xaf8734)}[mode]
    record = catalog[char_id]
    expected_skill = 'gauge_tempest' if mode == 6 else 'skill_insight_konzetsu'
    assert record['skill_id'] == expected_skill and record['is_available'] is False
    assert boundary['selected_id'] == 49 and boundary['selected_ability'] == boundary['fallback_row'] == '0x0'
    assert not boundary['character_rows'] and n.q(vt + 0x18) == 0x118e220 and n.q(vt + 0x58) == selector
    # Validate instruction-backed selector, not a host invocation of an unowned ability.
    assert bytes(n.u.mem_read(selector, 8)) == struct.pack('<II', 0x52800000 | (mode << 5), 0xd65f03c0)
    return {'status': 'blocked', 'fresh_emulator': True, 'native_target_selection_attempted': False,
        'metadata': {k: record[k] for k in ['character_id', 'name', 'skill_id', 'char_type', 'skill_unlock_level', 'is_available']},
        'metadata_source': 'External supplied input: unchanged assets/char/characters.json',
        'missing_enriched_record_keys': [k for k in ['frag', 'prog', 'overdrive', 'level', 'exp'] if k not in record],
        'enriched_record_contract': '96b358 consumes current character-stat records, not the archived base/max-stat schema; native callers include value.character/value.characters accessors',
        'account_boundary': boundary,
        'ability_path': {'classification': 'Instruction-backed but not executed',
            'metadata_update_entry_elf_va': '0x96b358', 'character_initializer_elf_va': '0x100ec3c',
            'owned_object_lookup': 'account+18 vector, compare character+c; fallback account+68',
            'missing_owner_skip_elf_va': '0x96b58c -> 0x96b424',
            'ability_assignment': '0x96c5fc -> 0xa44128 -> 0x7ac3cc; a4415c stores character+d0',
            'factory_branch_elf_va': '0x7ad700' if mode == 6 else '0x7aed58',
            'factory_elf_va': hex(factory), 'vtable_elf_va': hex(vt),
            'type': n.cstr(n.q(n.q(vt - 8) + 8)).decode(),
            'activation_elf_va': '0x118e220', 'acceptance_elf_va': '0x9e979c (requires activation return exactly1)',
            'selector_elf_va': hex(selector), 'selector_constant': mode,
            'native_activation_result': None, 'native_selector_result': None, 'ability_pointer': None},
        'blocker': {'type': 'NativeOwnedCharacterInputUnavailable',
            'cause': 'Current account boundary has neither a target character object nor fallback/owned-character rows; only an uninitialized character49 shell. No authentic enriched character-stat/account input is supplied.',
            'not_an_observed_availability_rejection': True,
            'minimum_prerequisite': 'A justified owned-character/account input and original metadata/ability initialization; no unlocking, level/stat or pointer fabrication'},
        'special_gauge': None, 'special_parameters': None,
        'stages': {'character_ability_factory': 'not_run_missing_owner', 'activation': 'not_run',
                   'gauge_selector': 'not_run', 'ScoreState_LifeBarState': 'not_run',
                   'temporal': 'not_run_producer_gate_failed', 'failure_completion': 'not_run'},
        'prohibited_direct_factory_calls': 0,
        'later_field_provenance': ({'classification': 'Instruction-backed but not executed',
            'p_default': 'Native12c50c4 bulk zero, then12c5144 deliberate zero of20..3f; not an account p input',
            'baseline_accumulator': '160a728 reads p;160a750/160a764 write baseline/accumulator;160a76c writes gain',
            'character_prog_tempest': 'Optional enriched-record prog_tempest subtracts from prog at96b780;100ec68 stores character stats. Not proven equivalent to LifeBarState p.',
            'later_p_writers_or_valid_range': 'Unknown; no valid mode6 session constructed'} if mode == 6 else {
            'classification': 'Instruction-backed but not executed',
            'context_gate': '160a484 ->126dc1c reads App+e0 context word+38',
            'conditional_reader': 'bda064 context mode;1223ad4 settings insightChallengeDefaultDifficulty;18e2d6c -> App+28/9e59e4 profile integer key decimal(context mode)+deinosphaineinRelief',
            'ordinary_context': 'Observed ordinary fixture has context+38=0; initializer would skip this profile read. Mode11 branch itself is unexecuted.',
            'special_context_vector': 'Only context mode6:160a5f0 ->a3b33c(songId), native returned vector+48 transfers to gauge+50 at160a624',
            'native_cap_fields': '160a578 rate+74;160a674 U100;160a678 cap enabled;83dd70 modifies caps from native state',
            'world_semantics_or_profile_value_producer': 'Unknown; conditional profile/session contract, not proof of a universal World dependency'})}


def run():
    result = {'status': 'fail', 'scenario': 'continuous_gauge', 'fixture': 'ordinary_two_tap.aff (unchanged control)',
              'ordinary_control': {}, 'mode6_producer': {'status': 'not_run'}, 'mode11_producer': {'status': 'not_run'},
              'mode6_temporal': 'not_run', 'mode11_temporal': 'not_run', 'native_failures': [],
              'pc_skips_elf_va': PC_SKIPS, 'new_services': [], 'new_pc_skips': []}
    try:
        catalog = metadata()
        ordinary_control(result['ordinary_control'])
        result['mode6_producer'] = target_producer(6, catalog)
        result['mode11_producer'] = target_producer(11, catalog)
        result['native_failures'] = [{'type': 'NativeContinuousGaugeProducerBlocked',
            'message': 'Ordinary native gauge construction passes; neither target has a justified owned-character producer input. Special-mode activation, gauges, temporal and failure stages not run.'}]
        result['supplied_services'] = 'Existing ABI/platform/catalog/profile/settings/account/resource/clock/JNI/graphics/audio/allocator services unchanged; no special mode or gauge fields assigned. Each phase uses fresh state.'
        result['address_correction'] = {'classification': 'Instruction-backed',
            '0x13b5c2c': 'SpecialSceneArcahvChallenge factory, vtable1b022d8; not the ability gauge selector',
            'actual_solo_selector_callsite': 'ee2644 loads ability virtual+58; ee264c calls it'}
    except Exception as exc:
        result['native_failures'].append({'type': type(exc).__name__, 'message': str(exc),
                                          'line': traceback.extract_tb(exc.__traceback__)[-1].lineno})
    return result
