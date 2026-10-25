# Recovered research adapter; consolidated for Expedition 024.
import config
import json, sys, collections, zipfile, math
from pathlib import Path
import results_services as exp014, action_services as exp015, arm64 as recover
from transition_services import FinalNative
from unicorn.arm64_const import *

class EndingNative(FinalNative):

    def __init__(self):
        super().__init__()
        self.hooks.pop(27594836, None)
        self.uiTextures = []
        self.animationEvents = []
        self.observe = self.observe | {27594836, 27309564, 9014764, 9958884, 22760504, 26229228, 25529404, 14086748, 8216892, 23556720, 21487336, 25777480, 23796492, 16965268, 27332576, 19183512, 8950828, 22813072, 26456156, 24196980, 13203092, 23556720, 8217392, 22760828, 22760704, 20993192}
        for addr, name in self.imports.items():
            if name in ['sinf', 'cosf', 'acosf', 'sqrtf']:
                op = {'sinf': math.sin, 'cosf': math.cos, 'acosf': math.acos, 'sqrtf': math.sqrt}[name]
                self.hooks[addr] = lambda op=op: (self.s(0, op(self.s(0))), self.ret())
        self.hooks[27712416] = lambda: self.stringret(self.x(0), self.cstr(self.x(1)))

    def animation_state(self, label):
        a = self.endingTimeline
        return {'label': label, 'wall': self.now, 'pointer': hex(a), 'vtable': hex(self.q(a)), 'ref': self.i(a + 8), 'frame': self.i(a + 132), 'range': [self.i(a + 136), self.i(a + 140)], 'speed': self.f(a + 120), 'interval': self.f(a + 124), 'time': __import__('struct').unpack('<d', self.u.mem_read(a + 112, 8))[0], 'playing': self.u.mem_read(a + 128, 1)[0], 'loop': self.u.mem_read(a + 144, 1)[0], 'target': hex(self.q(a + 32)), 'frameCallbackCount': self.q(a + 272), 'animationInfoCount': self.q(a + 296), 'root': hex(self.endingRoot), 'rootRef': self.i(self.endingRoot + 8), 'rootRunning': self.u.mem_read(self.endingRoot + 448, 1)[0], 'rootParent': hex(self.q(self.endingRoot + 328)), 'sceneRef': self.i(self.scene + 8), 'continuations': sum((e['pc'] == '0x147dee8' for e in self.events)), 'actions': self.action_state(), 'timers': self.timers()}

    def oncode(self, u, a, size, ud):
        if hasattr(self, 'animationEvents') and a in {27594836, 25529404, 8216892, 23556720, 21487336}:
            d = {'pc': hex(a), 'lr': hex(self.x(30)), 'phase': self.phase, 'wall': self.now, 'x0': hex(self.x(0)), 'x1': hex(self.x(1)), 'x2': hex(self.x(2))}
            if a == 27594836:
                fn = self.q(self.x(1) + 32)
                d['inputFunction'] = {'p': hex(fn), 'vtable': hex(self.q(fn)), 'capture': hex(self.q(fn + 8))}
            if a == 25529404:
                fn = self.q(self.x(2) + 32)
                cap = self.q(fn + 64)
                d.update(name=self.string(self.x(1)).decode(), wrapper=hex(fn), wrapperVtable=hex(self.q(fn)), wrapperScene=hex(self.q(fn + 16)), continuation=hex(cap), continuationVtable=hex(self.q(cap)), continuationScene=hex(self.q(cap + 8)))
            if a == 23556720:
                fn = self.q(self.x(0) + 64)
                d.update(wrapperScene=hex(self.q(self.x(0) + 16)), continuation=hex(fn), continuationVtable=hex(self.q(fn)), continuationScene=hex(self.q(fn + 8)))
            if a == 21487336:
                d.update(scene=hex(self.q(self.x(0) + 8)))
            self.animationEvents.append(d)
        super().oncode(u, a, size, ud)
