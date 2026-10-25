# Recovered research adapter; consolidated for Expedition 024.
import config
import json, sys, collections, math
from pathlib import Path
import action_services as exp015, results_services as exp014, arm64 as recover
from action_services import ActionNative
from unicorn.arm64_const import *

class FinalNative(ActionNative):

    def __init__(self):
        super().__init__()
        self.hooks.pop(9842992, None)
        self.moreTrees = []
        self.stateLog = []
        self.observe = self.observe | {9842992, 9843220, 9843476, 26182636, 25616408, 8632496, 13579408, 11609784, 26672372, 11136676, 19754796, 18067232, 14765452, 9591912, 25972176, 14331136, 22625104, 25085072, 22801184, 14460540, 25944824, 17319616, 22560936, 22600748, 19766800, 27374056, 7879724, 26741104, 9056060, 26488776, 26697880, 8249296, 25648020, 22644180, 23303488}
        self.hooks[11335832] = self.result_enter_feedback
        self.hooks[27713664] = lambda: (self.s(0, math.pow(self.s(0), self.s(1))), self.ret())
        self.hooks[27712480] = lambda: self.ret(self.now * 1000)

    def result_enter_feedback(self):
        self.services.append({'pc': '0xacf898', 'caller': hex(self.x(30)), 'phase': self.phase, 'manager': hex(self.x(0)), 'classification': self.x(1), 'character': hex(self.x(2))})
        self.ret(0)

    def timers(self):
        out = super().timers()
        for entry in out:
            for row in entry['timers']:
                p = int(row['p'], 16)
                row.update(vtable=hex(self.q(p)), type=self.typename(p), slots={hex(off): hex(self.q(p + off)) for off in range(64, 112, 8)})
                fn = int(row['fn'], 16)
                if fn:
                    row['function'] = {'vtable': hex(self.q(fn)), 'invoke': hex(self.q(self.q(fn) + 48)), 'capture': hex(self.q(fn + 8))}
        return out

    def badmem(self, u, access, a, size, value, ud):
        return super().badmem(u, access, a, size, value, ud)

    def tick(self, dt):
        self.phase = '016 Scheduler dt' + str(dt)
        self.now += round(dt * 1000)
        self.call(20791108, self.scheduler, fs=(dt,))

    def oncode(self, u, a, size, ud):
        if hasattr(self, 'moreTrees') and a == 13074956:
            p = self.x(1)
            self.moreTrees.append({'node': hex(self.x(0)), 'action': hex(p), 'type': self.typename(p), 'vtable': hex(self.q(p)), 'duration': self.f(p + 48), 'phase': self.phase, 'tree': self.tree16(p)})
        super().oncode(u, a, size, ud)

    def tree16(self, p):
        typ = self.typename(p)
        o = {'p': hex(p), 'type': typ, 'vtable': hex(self.q(p)), 'ref': self.i(p + 8), 'duration': self.f(p + 48), 'originalTarget': hex(self.q(p + 24)), 'target': hex(self.q(p + 32))}
        if typ.endswith('SequenceE'):
            o.update(children=[self.tree16(self.q(p + 64)), self.tree16(self.q(p + 72))], split=self.f(p + 80), last=self.i(p + 84))
        elif typ.endswith('EaseInE'):
            o.update(inner=self.tree16(self.q(p + 64)), rate=self.f(p + 72))
        elif typ.endswith('MoveByE'):
            o.update(delta=[self.f(p + 60), self.f(p + 64), self.f(p + 68)])
        elif typ.endswith('CallFuncE'):
            fn = self.q(p + 112)
            o['function'] = {'p': hex(fn), 'vt': hex(self.q(fn)), 'method': hex(self.q(fn + 8)), 'adjustment': self.q(fn + 16), 'this': hex(self.q(fn + 24))}
        return o
