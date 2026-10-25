"""023 experiment consolidated without runtime source extraction or scratch dependencies."""
import collections
import math
from solo_entry import setup, entry
from lifecycle import activate, frame, ending, downstream
from unicorn import UC_HOOK_CODE
from boundaries import PC_SKIPS


def verify(n, scene, model, initializer_return):
    data = n.observations
    counts = collections.Counter(e['pc'] for e in n.events)
    required = [0xee197c, 0xee29a8, 0xee29e8, 0xe4e4dc, 0xe2ea48,
                0xc27d34, 0x1600bb0, 0x19bbdd0, 0x1a51054, 0x147dee8,
                0xf0b48c, 0x18f11c0, 0xd11738, 0x187c0c8, 0x891150,
                0xdc2c48, 0x13552d4, 0x12a5e60]
    for address in required:
        assert counts[hex(address)] == 1, (hex(address), counts[hex(address)])
    assert counts['0xdd0f90'] == 0
    assert counts['0x963094'] == 2 and counts['0x113af20'] == 2
    for address in [0xbe31a8, 0xdda71c, 0x194ff80, 0xeec024, 0x160ce28]:
        assert counts[hex(address)] == 2, hex(address)
    eligibility = [e for e in n.soloTrace if e['pc'] == '0xee2214']
    assert len(eligibility) == 1 and int(eligibility[0]['x'][0], 16) == 1
    constructor = [e for e in n.menuTrace if e['pc'] == '0xe4e4dc'][0]
    assert constructor['lr'] == '0xee29ec' and int(constructor['x'][0], 16) == scene
    assert initializer_return == 1
    assert n.u.mem_read(n.menu + 0x490, 1)[0] == 1
    assert not any(a in n.host_calls for a in [0xe4e4dc, 0xe2ea48, 0x10a7550,
                   0x147dee8, 0x963094, 0xd11738, 0x13552d4, 0x12a5e60])
    assert any(e['pc'] == '0x10a7550' for r in n.trace for e in r['lifecycle'])
    assert n.scene == scene and n.model == model and n.q(scene + 0x3e0) == model
    rs = n.resultScenes[0]
    session = n.q(rs + 0x2e8)
    assert n.result != 0 and n.q(n.q(model + 0x38) + 0x68) == n.q(session + 0x18) == n.result
    assert 'NormalGameResultScene' in n.typename(rs)
    assert n.q(n.director + 0x140) == rs and n.q(n.director + 0x148) == 0
    assert n.u.mem_read(n.dispatcher + 0x124, 1)[0] == 1
    assert n.gateObservations[-1]['gateByte'] == n.gateObservations[-1]['resultB0'] == 0
    assert len(data['tracks']) == 24 and sum(t['frames'] for t in data['tracks']) == 85
    assert any(r['frame'] == 49 and r['continuations'] == 0 for r in n.animationTrace)
    assert any(r['frame'] == 50 and r['continuations'] == 1 for r in n.animationTrace)
    expected = dict(score=10000002, PURE=2, FAR=0, LOST=0, health=80, clear=3)
    assert all(n.resultSummary[k] == v for k, v in expected.items())
    assert math.isclose(n.resultSummary['liveHealth'], 80.4000015258789, abs_tol=1e-6)
    assert len(data['scores']) == len(data['clears']) == 1
    expected_score = dict(songId='sayonarahatsukoi', songDifficulty=0, score=10000002,
                          shinyPerfectCount=2, perfectCount=2, nearCount=0, missCount=0, health=80)
    assert all(data['scores'][0][k] == v for k, v in expected_score.items())
    assert all(data['clears'][0][k] == v for k, v in dict(songId='sayonarahatsukoi', songDifficulty=0, clearType=3).items())
    assert n.native_sqlite and 'sqlite3_step' in n.nativeSqlCalls
    for address in [0x17c45f4, 0xe4e4dc, 0xe2ea48, 0x19069a0, 0x147dee8, 0xdc2c48, 0x13552d4, 0x12a5e60]:
        assert address not in n.hooks, hex(address)
    return {'status': 'pass', 'fixture': 'ordinary_two_tap/offline-solo/sayonarahatsukoi/0',
            'entry_elf_va': '0xee197c', 'native_call_counts': {hex(a): counts[hex(a)] for a in required + [0x963094, 0xdd0f90, 0xbe31a8, 0xdda71c]},
            'identity_checks': {'same_game_scene': True, 'same_model': True, 'cache_equals_session_result': True,
                                'native_constructor_caller': True, 'no_direct_host_handoffs': True},
            'observed_emulated_pointers': data['identity'], 'result': n.resultSummary,
            'sqlite': {'engine': 'bundled ARM64', 'api_calls': dict(collections.Counter(n.nativeSqlCalls)),
                       'scores': data['scores'], 'clearTypes': data['clears'], 'unchanged_after_extra_updates': True},
            'final_director': {'running_scene_type': n.typename(rs), 'running_scene': hex(rs),
                               'pending': 0, 'dispatcher_enabled': True},
            'save_gate_observations': n.gateObservations, 'pc_skips_elf_va': PC_SKIPS,
            'native_failures': []}


def run(unavailable=False):
    n = setup(not unavailable)
    if unavailable:
        entry(n)
        assert not hasattr(n, 'scene') and n.u.mem_read(n.menu + 0x490, 1)[0] == 0
        assert n.q(n.director + 0x148) == 0
        assert any(e['pc'] == '0xee2214' and int(e['x'][0], 16) == 0 for e in n.soloTrace)
        return {'status': 'pass', 'test': 'unavailable_song_rejected', 'game_scene_constructed': False, 'native_failures': []}
    n.prepare_runtime()
    n.phase = 'original registry initializer'
    n.call(0x1054f24)
    n.observe |= {0xbe31a8, 0xdda71c, 0x1600bb0, 0x1315038, 0x12a5574, 0x194ff80, 0xeec024, 0x160ce28, 0xc27d34}
    n.gateObservations = []
    def gate(u, a, size, ud):
        rs = n.x(20)
        session = n.q(rs + 0x2e8)
        result = n.q(session + 0x18)
        n.gateObservations.append({'pc': hex(a), 'gateByte': n.u.mem_read(rs + 0x2f8, 1)[0],
                                  'resultB0': n.u.mem_read(result + 0xb0, 1)[0], 'session_mode': n.i(session + 0x20)})
    for a in [0x891684, 0x89219c, 0x8921b8]:
        n.u.hook_add(UC_HOOK_CODE, gate, begin=a, end=a)
    n.trace = []; n.visual = []; n.animationTrace = []; n.downstream = []
    n.env = n.alloc(8); n.now = 1000
    entry(n)
    activate(n)
    scene, model, init_return = n.scene, n.model, n.sceneInitReturn
    assert init_return == 1 and n.q(n.director + 0x140) == scene
    frame(n, n.now + 1, 'solo preroll')
    row = frame(n, n.now + 3001, 'native music anchor')
    for target, x, pid in [(1000, 740, 42), (2000, 540, 43)]:
        row = frame(n, n.now + target - row['E'], 'native solo tap')
        assert row['E'] == target
        n.call(0xbe31a8, n.env, 0, pid, 987000 + pid, fs=(x, 700, .5))
        n.call(0xdda71c, n.env, 0, pid, 988000 + pid, fs=(x, 700, 0))
    frame(n, n.now + 2122 - row['E'], 'solo completion')
    score = n.q(model + 0x38); n.result = n.q(score + 0x68); r = n.result
    assert r
    g = n.items(score, 0xa0)[0]
    n.resultSummary = {'p': hex(r), 'score': n.call(0x1315038, r), 'PURE': n.i(r + 0x18),
                       'FAR': n.i(r + 0x1c), 'LOST': n.i(r + 0x20), 'health': n.i(r + 0x28),
                       'liveHealth': n.f(g + 0x10), 'clear': n.call(0x12a5574, r)}
    ending(n)
    downstream(n)
    return verify(n, scene, model, init_return)
