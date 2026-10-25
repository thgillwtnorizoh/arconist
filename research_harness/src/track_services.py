# Recovered research adapter; consolidated for Expedition 024.
import config
import json, sys, math, struct, re, collections, importlib.util
from pathlib import Path
from resources import RuntimeNative, hierarchy
from unicorn import UC_HOOK_MEM_READ, UC_HOOK_MEM_WRITE
from unicorn.arm64_const import *

class TrackNative(RuntimeNative):

    def __init__(self):
        super().__init__()
        self.phase = '020 runtime support'
        self.abi = []
        self.trackEvents = []
        self.localeObjects = {}
        self.localeReads = []
        self.currentLocale = (1 << 64) - 1
        for a, name in self.imports.items():
            if name == 'sincosf':
                self.hooks[a] = self.sincosf
            elif name == 'pthread_cond_broadcast' or name == 'pthread_cond_signal':
                self.hooks[a] = lambda a=a: self.abi_return(a, 0)
            elif name == 'strncmp':
                self.hooks[a] = self.strncmp
            elif name == 'newlocale':
                self.hooks[a] = self.newlocale
            elif name == 'uselocale':
                self.hooks[a] = self.uselocale
            elif name == 'freelocale':
                self.hooks[a] = self.freelocale
        self.observe |= {25657020, 19490788, 10867676, 26241440, 13698416, 25953448, 19494792}
        self.hooks[19164312] = self.service
        self.hooks[22581816] = lambda: self.ret(4096)
        self.observe |= {13286948, 11316248, 17789124, 12844540}

    def prepare_app(self):
        super().prepare_app()
        self.phase = '020 original pixel-format registry static initializer'
        self.call(13286948)

    def abi_return(self, a, v):
        self.abi.append({'import': self.imports.get(a), 'pc': hex(a), 'lr': hex(self.x(30)), 'args': [hex(self.x(i)) for i in range(3)], 'return': hex(v)})
        self.ret(v)

    def sincosf(self):
        value = self.s(0)
        p, q = (self.x(0), self.x(1))
        self.wf(p, math.sin(value))
        self.wf(q, math.cos(value))
        self.abi.append({'import': 'sincosf', 'lr': hex(self.x(30)), 's0': value, 'sinOut': hex(p), 'cosOut': hex(q), 'sin': self.f(p), 'cos': self.f(q)})
        self.ret()

    def strncmp(self):
        a, b, count = (self.x(0), self.x(1), self.x(2))
        aa = []
        bb = []
        for i in range(count):
            av, bv = (self.u.mem_read(a + i, 1)[0], self.u.mem_read(b + i, 1)[0])
            if av != bv:
                self.ret(av - bv)
                return
            if av == 0:
                break
        self.ret(0)

    def newlocale(self):
        mask, namep, base = (self.x(0), self.x(1), self.x(2))
        name = self.cstr(namep).decode() if namep else None
        error = 22 if mask & ~8127 or name is None else 2 if name not in ['C', 'POSIX', 'C.UTF-8', 'en_US.UTF-8', ''] else 0
        if error:
            self.wi(self.errno, error)
            p = 0
        else:
            p = self.alloc(8)
            mb = 4 if not name or 'UTF-8' in name else 1
            self.wq(p, mb)
            self.localeObjects[p] = {'name': name, 'mask': mask, 'alive': True, 'mb_cur_max': mb}
            self.u.hook_add(UC_HOOK_MEM_READ, self.locale_read, begin=p, end=p + 7)
        self.abi.append({'import': 'newlocale', 'lr': hex(self.x(30)), 'mask': hex(mask), 'name': name, 'base': hex(base), 'return': hex(p), 'errno': error})
        self.ret(p)

    def locale_read(self, u, access, a, size, value, ud):
        self.localeReads.append({'pc': hex(u.reg_read(UC_ARM64_REG_PC)), 'addr': hex(a), 'size': size})

    def uselocale(self):
        p = self.x(0)
        old = self.currentLocale
        assert p in [0, (1 << 64) - 1] or (p in self.localeObjects and self.localeObjects[p]['alive']), hex(p)
        if p:
            self.currentLocale = p
        self.abi.append({'import': 'uselocale', 'lr': hex(self.x(30)), 'input': hex(p), 'previous': hex(old)})
        self.ret(old)

    def freelocale(self):
        p = self.x(0)
        assert p in self.localeObjects and self.localeObjects[p]['alive']
        self.localeObjects[p]['alive'] = False
        self.abi.append({'import': 'freelocale', 'lr': hex(self.x(30)), 'input': hex(p)})
        self.ret()

    def oncode(self, u, a, size, ud):
        if hasattr(self, 'trackEvents') and a in [25657020, 19490788, 10867676, 26241440, 19494792]:
            self.trackEvents.append({'pc': hex(a), 'lr': hex(self.x(30)), 'args': [hex(self.x(i)) for i in range(8)], 'phase': self.phase})
        super().oncode(u, a, size, ud)
