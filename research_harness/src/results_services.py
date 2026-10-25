# Recovered research adapter; consolidated for Expedition 024.
import config
import sys, json, struct
from pathlib import Path
from sqlite_services import PersistenceNative
import arm64 as recover
from unicorn.arm64_const import *

class CompletionNative(PersistenceNative):

    def __init__(self):
        super().__init__(True)
        self.events = []
        self.refs = []
        self.services = []
        self.phase = 'setup'
        self.uiPending = []
        self.transitionRequests = []
        self.resultScenes = []
        self.observe = self.observe | {17462608, 14860580, 12746036, 15058688, 22658540, 15373180, 20791108, 26983888, 21487336, 15774860, 26153408, 13702968, 25673928, 8982864, 14429256, 27594836, 10260672, 11246944, 10483216, 24166920, 23740868, 9842836, 9842964, 8984196}
        self.hooks.pop(18981100, None)
        for a in [21495368, 14081176]:
            self.hooks[a] = self.ref_boundary
        for a in [16401184, 18378608, 12870884, 26995904, 27594836, 16882712, 17078360, 11774780, 13107376]:
            self.hooks[a] = self.service
        self.hooks[27594836] = self.ui_completion
        self.hooks[10483216] = self.transition_shell
        self.hooks[23740940] = lambda: self.u.reg_write(UC_ARM64_REG_PC, 23743052)
        self.hooks[9842992] = lambda: self.u.reg_write(UC_ARM64_REG_PC, 9843540)
        self.hooks[10298648] = self.service
        self.hooks[14113896] = self.service
        self.hooks[10260672] = self.transition_request
        self.hooks[8982928] = self.init_save_segment
        self.hooks[8984200] = lambda: self.u.reg_write(UC_ARM64_REG_PC, 8987036)
        self.hooks[8987100] = lambda: self.u.reg_write(UC_ARM64_REG_PC, 8988896)
        self.hooks[19535444] = lambda: self.ret(self.camera)

    def ui_completion(self):
        fn = self.q(self.x(1) + 32)
        v = self.q(fn)
        clone = self.alloc(64)
        self.uiPending.append(clone)
        self.services.append({'pc': '0x1a51054', 'callback': hex(fn), 'clone': hex(clone), 'operator': hex(self.q(v + 48)), 'phase': self.phase})
        self.x(0, fn)
        self.x(1, clone)
        self.u.reg_write(UC_ARM64_REG_PC, self.q(v + 24))

    def transition_shell(self):
        self.resultScenes.append(self.x(0))
        self.services.append({'pc': '0x9ff610', 'resultScene': hex(self.x(0)), 'phase': self.phase})

    def init_save_segment(self):
        self.x(28, self.q(28925784))
        self.x(26, self.x(29) - 96)
        self.u.reg_write(UC_ARM64_REG_PC, 8984140)

    def transition_request(self):
        self.transitionRequests.append(self.x(1))

    def ref_boundary(self):
        if self.x(0) == 0:
            self.refs.append({'pc': hex(self.u.reg_read(UC_ARM64_REG_PC)), 'nullEnvironment': True})
            self.ret()

    def service(self):
        a = self.u.reg_read(UC_ARM64_REG_PC)
        self.services.append({'pc': hex(a), 'caller': hex(self.x(30)), 'phase': self.phase, 'x0': hex(self.x(0))})
        self.ret(0)

    def oncode(self, u, a, size, ud):
        if hasattr(self, 'events'):
            if a in self.observe:
                self.events.append({'pc': hex(a), 'caller': hex(self.x(30)), 'phase': self.phase, 'wall': self.now, 'x0': hex(self.x(0)), 'x1': hex(self.x(1)), 's0': self.s(0), 's1': self.s(1)})
            if a in [18981100, 21495368, 14081176] and self.x(0) > 67108864:
                self.refs.append({'pc': hex(a), 'caller': hex(self.x(30)), 'object': hex(self.x(0)), 'before': self.i(self.x(0) + 8), 'phase': self.phase})
        super().oncode(u, a, size, ud)

    def timers(self):
        entry = self.q(self.scheduler + 48)
        out = []
        while entry:
            array = self.q(entry)
            num = self.i(array)
            data = self.q(array + 16)
            out.append({'entry': hex(entry), 'target': hex(self.q(entry + 8)), 'paused': self.u.mem_read(entry + 33, 1)[0], 'timers': [{'p': hex(self.q(data + i * 8)), 'key': self.string(self.q(data + i * 8) + 112).decode(), 'elapsed': self.f(self.q(data + i * 8) + 24), 'delay': self.f(self.q(data + i * 8) + 40), 'interval': self.f(self.q(data + i * 8) + 44), 'fn': hex(self.q(self.q(data + i * 8) + 96))} for i in range(num)]})
            entry = self.q(entry + 56)
            if len(out) > 10:
                break
        return out
