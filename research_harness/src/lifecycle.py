# Consolidated 019/021/023 lifecycle driver; no native callback is invoked directly.
from resources import *

def frame(n, wall, label):
    n.now = wall
    n.phase = label
    before = len(n.lifecycle)
    n.call(24723340, n.director)
    row = {'label': label, 'wall': wall, 'running': hex(n.q(n.director + 320)), 'pending': hex(n.q(n.director + 328)), 'directorFrame': n.i(n.director + 308), 'sceneStamp': n.i(n.scene + 1232), 'E': n.i(n.q(n.model + 48) + 32) - n.i(n.q(n.model + 48) + 40), 'lastModelE': n.i(29332456), 'lifecycle': n.lifecycle[before:]}
    n.trace.append(row)
    print('DIRECTOR_FRAME', json.dumps(row), flush=True)
    return row

def snapshot(n, label):
    row = {'label': label, 'wall': n.now, 'menu': hex(n.menu), 'state': hex(n.selection), 'difficulty': n.i(n.selection + 40), 'gameScene': hex(n.scene), 'shutter': hex(n.loadingShutter), 'running': hex(n.q(n.director + 320)), 'pending': hex(n.q(n.director + 328)), 'dispatcher': n.u.mem_read(n.dispatcher + 292, 1)[0], 'model': hex(n.q(n.scene + 992)), 'callbackCount': sum((e['pc'] == '0x963094' for e in n.events)), 'actions': n.action_state(), 'timers': n.timers()}
    n.menuStates.append(row)
    print('MENU_STATE', json.dumps(row), flush=True)
    return row

def activate(n):
    n.menuStates = []
    n.loadingShutter = n.q(n.director + 328)
    n.loadingInfo = n.alloc(1536)
    n.call(20005276, n.loadingInfo)
    n.call(n.q(n.q(n.loadingShutter) + 488), n.loadingShutter, n.loadingInfo)
    n.wq(n.loadingShutter + 784, n.loadingInfo)
    n.hooks[10815428] = lambda: n.u.reg_write(UC_ARM64_REG_PC, 10820076)
    n.hooks[26672556] = lambda: n.u.reg_write(UC_ARM64_REG_PC, 26673068)
    n.hooks[10820316] = lambda: n.u.reg_write(UC_ARM64_REG_PC, 10821948)
    n.phase = '021 Director consumes native menu replacement'
    n.call(24723340, n.director)
    snapshot(n, 'loading activated')
    for dt in [0, 0.25, 0, 0.4, 0.4, 0.4]:
        n.tick(dt)
        snapshot(n, 'loading dt ' + str(dt))
    n.model = n.q(n.scene + 992)
    assert n.model
    n.endingRoot = n.q(n.scene + 968)
    n.endingTimeline = n.q(n.scene + 976)
    n.owned = [{'offset': hex(o), 'p': hex(n.q(n.scene + o)), 'type': n.typename(n.q(n.scene + o)) if n.q(n.scene + o) else None} for o in [768, 944, 952, 960, 968, 976, 992, 1000, 1240]]
    for dt in [0, 0.2, 0.2, 0, 0, 0.1, 0.1, 0.1, 0, 2.5, 0, 0.2, 0.2, 0.2, 0.2, 0]:
        n.tick(dt)
    for j in range(40):
        if n.q(n.director + 328) == n.scene:
            break
        n.tick(0.2)
    snapshot(n, 'loading closing progressed')
    n.phase = '021 Director final loading activation attempt'
    n.call(24723340, n.director)
    snapshot(n, 'loading final activation attempt')
    assert n.q(n.director + 320) == n.scene and n.q(n.director + 328) == 0

def ending(n):
    for dt in [0, 4]:
        n.tick(dt)
    n.animationTrace.append(n.animation_state('end registered'))
    assert n.animationTrace[-1]['continuations'] == 0
    for dt in [0, 0.4, 0.4, 0.03, 0.01, 0.02]:
        n.tick(dt)
        row = n.animation_state('dt ' + str(dt))
        n.animationTrace.append(row)
        print('ENDING', json.dumps(row), flush=True)
    assert n.animationTrace[-3]['frame'] == 49 and n.animationTrace[-3]['continuations'] == 0
    assert n.animationTrace[-2]['frame'] == 50 and n.animationTrace[-2]['continuations'] == 1
    for dt in [2, 0.3]:
        n.tick(dt)
    assert n.resultScenes and len(n.transitionRequests) == 2
    print('RESULT_TRANSITION', list(map(hex, n.resultScenes)), list(map(hex, n.transitionRequests)), flush=True)

def downstream(n):
    rs = n.resultScenes[0]
    sh = n.transitionRequests[-1]
    session = n.q(rs + 744)
    assert n.q(session + 24) == n.result
    frame(n, n.now, 'Director activates native shutter')

    def snap(label):
        row = {'label': label, 'wall': n.now, 'running': hex(n.q(n.director + 320)), 'pending': hex(n.q(n.director + 328)), 'stack': [hex(p) for p in n.items(n.director, 344)], 'dispatcherEnabled': n.u.mem_read(n.dispatcher + 292, 1)[0], 'callbacks': dict(collections.Counter((e['pc'] for e in n.events if e['pc'] in ['0x147dee8', '0x963094', '0x891150', '0xdc2c48', '0x13552d4', '0x12a5e60', '0x113af20']))), 'actions': n.action_state(), 'timers': n.timers()}
        n.downstream.append(row)
        print('DOWNSTREAM', json.dumps(row), flush=True)
        return row
    snap('shutter entered')
    for dt in [0, 0.25, 0.25, 0.25]:
        n.tick(dt)
        snap('opening ' + str(dt))
    scores = n.query('SELECT * FROM scores')
    clears = n.query('SELECT * FROM clearTypes')
    print('SQLITE_READBACK', scores, clears, flush=True)
    for dt in [0, 0.2, 0.2, 0, 0, 0.1, 0.1, 0.1, 0]:
        n.tick(dt)
        snap('closing ' + str(dt))
    assert n.q(n.director + 328) == rs
    frame(n, n.now, 'Director final results activation')
    last = snap('results active')
    assert n.q(n.director + 320) == rs and n.q(n.director + 328) == 0 and (last['stack'] == [hex(rs)]) and (last['dispatcherEnabled'] == 1)
    for dt in [0, 0.25, 1, 5]:
        n.tick(dt)
    frame(n, n.now, 'additional Director result frame')
    snap('additional updates')
    assert n.query('SELECT * FROM scores') == scores and n.query('SELECT * FROM clearTypes') == clears
    counts = collections.Counter((e['pc'] for e in n.events))
    for a in [26983888, 27594836, 21487336, 15774860, 26153408, 9842836, 8982864, 14429256, 20271828, 19553888]:
        assert counts[hex(a)] == (2 if a == 9842836 else 1), (hex(a), counts[hex(a)])
    assert n.q(n.q(n.model + 56) + 104) == n.result and n.q(session + 24) == n.result
    assert scores[0]['score'] == 10000002 and scores[0]['date'] == 1700000000 and (clears[0]['clearType'] == 3)
    data = {'initializerReturn': n.sceneInitReturn, 'identity': {'gameScene': hex(n.scene), 'model': hex(n.model), 'chart': hex(n.q(n.model + 40)), 'timeline': hex(n.q(n.model + 48)), 'scoreState': hex(n.q(n.model + 56)), 'result': hex(n.result), 'endingRoot': hex(n.endingRoot), 'endingTimeline': hex(n.endingTimeline), 'session': hex(session), 'resultScene': hex(rs), 'shutter': hex(sh), 'director': hex(n.director), 'scheduler': hex(n.scheduler), 'manager': hex(n.manager), 'dispatcher': hex(n.dispatcher)}, 'result': n.resultSummary, 'sceneOwned': n.owned, 'hierarchy': hierarchy(n, n.endingRoot), 'tracks': [{'p': hex(t), 'tag': n.i(t + 64), 'frames': len(n.items(t, 16)), 'frameNodeSets': [hex(n.q(f + 56)) for f in n.items(t, 16)]} for t in n.items(n.endingTimeline, 80)], 'sceneFrames': n.trace, 'animation': n.animationTrace, 'downstream': n.downstream, 'counts': dict(counts), 'scores': scores, 'clears': clears, 'animationEvents': n.animationEvents, 'resources': n.resourceLog, 'textureRequests': n.textureRequests, 'touchEvents': n.touchEvents, 'events': n.events, 'refs': n.refs, 'services': n.services, 'sql': n.sql, 'paths': n.paths, 'symbolRelocations': n.symbolRelocations, 'glCalls': collections.Counter((x['name'] for x in n.glCalls)), 'hookInventory': {hex(a): {'name': n.imports.get(a, getattr(f, '__name__', '')), 'entries': n.count[a]} for a, f in n.hooks.items()}, 'boundaryRegistry': {hex(k): v for k, v in n.boundaries.items()}}
    n.observations = data
    print('PASS_019_CONTINUOUS', json.dumps({k: data[k] for k in ['initializerReturn', 'identity', 'result', 'counts', 'scores', 'clears']}), flush=True)
