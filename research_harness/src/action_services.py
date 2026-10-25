# Recovered research adapter; consolidated for Expedition 024.
import config
import json, sys, collections
from pathlib import Path
import results_services as exp014, arm64 as recover
from results_services import CompletionNative
from unicorn.arm64_const import *

class ActionNative(CompletionNative):

    def __init__(self):
        super().__init__()
        self.actions = []
        self.phase = 'setup'
        self.activation = []
        self.observe = self.observe | {13687828, 18962412, 24541832, 22641940, 17688696, 21750060, 16166400, 9215268, 13074956, 11787320, 10420192, 14037176, 25925220, 24723340, 26741104, 25808064, 8240828, 15814556, 25599056, 19552896, 25807776, 19974956, 26434764, 18386108, 22075600, 9317232, 20084720, 12149948, 14835872, 14113896, 10134232, 8256444, 15775712}
        self.hooks.pop(23740940, None)
        self.hooks.pop(14113896, None)
        self.hooks[23740984] = self.supply_panels
        self.hooks[10256784] = self.service
        self.hooks[18962460] = lambda: self.u.reg_write(UC_ARM64_REG_PC, 18962508)

    def supply_panels(self):
        tr = self.x(19)
        self.wq(tr + 768, self.left)
        self.wq(tr + 776, self.right)
        self.u.reg_write(UC_ARM64_REG_PC, 23742680)

    def action_state(self):
        out = []
        p = self.q(self.manager + 16)
        while p:
            array = self.q(p)
            data = self.q(array + 16)
            out.append({'entry': hex(p), 'target': hex(self.q(p + 8)), 'paused': self.u.mem_read(p + 33, 1)[0], 'actions': [hex(self.q(data + 8 * i)) for i in range(self.q(array))]})
            p = self.q(p + 56)
        return out

    def tree(self, p):
        typ = self.typename(p)
        v = self.q(p)
        o = {'p': hex(p), 'type': typ, 'vt': hex(v), 'ref': self.i(p + 8), 'duration': self.f(p + 48), 'target': hex(self.q(p + 24)), 'originalTarget': hex(self.q(p + 32))}
        if typ.endswith('SequenceE'):
            o['children'] = [self.tree(self.q(p + 64)), self.tree(self.q(p + 72))]
            o['split'] = self.f(p + 80)
            o['last'] = self.i(p + 84)
        elif typ.endswith('EaseCubicActionOutE'):
            o['inner'] = self.tree(self.q(p + 64))
        elif 'MoveTo' in typ:
            o['raw'] = {hex(i): [self.f(p + i), self.f(p + i + 4)] for i in range(64, 112, 8)}
        elif 'CallFunc' in typ:
            fn = self.q(p + 112)
            o['function'] = {'p': hex(fn), 'vt': hex(self.q(fn)), 'type': self.typename(fn), 'method': hex(self.q(fn + 8)), 'adjustment': self.q(fn + 16), 'this': hex(self.q(fn + 24))}
        return o

    def oncode(self, u, a, size, ud):
        if hasattr(self, 'actions') and a == 13074956:
            self.actions.append({'node': self.x(0), 'action': self.x(1), 'phase': self.phase})
        super().oncode(u, a, size, ud)

    def typename(self, p):
        return self.cstr(self.q(self.q(self.q(p) - 8) + 8)).decode() if p else ''
