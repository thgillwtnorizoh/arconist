# Recovered research adapter; consolidated for Expedition 024.
import config
import json, sys, struct, collections, zipfile, math
from pathlib import Path
import chart_services as exp010, arm64 as recover
from chart_services import LoadingNative
from unicorn.arm64_const import *

class BootstrapNative(LoadingNative):

    def __init__(self):
        super().__init__()
        self.events = []
        self.services = []
        self.refs = []
        self.phase = 'initial environment'
        self.allocations = []
        self.calls = collections.deque(maxlen=100)
        self.projections = []
        self.touchEvents = []
        for a in [18981100, 12427364, 27209280]:
            self.hooks.pop(a, None)
        for a in [21495368, 14081176]:
            self.hooks[a] = self.ref_boundary
        self.hooks[27712416] = lambda: self.stringret(self.x(0), self.cstr(self.x(1)))
        self.hooks[27712528] = lambda: self.stringret(self.x(8), self.cstr(self.x(0)) + self.string(self.x(1)))
        self.hooks[27712512] = lambda: self.stringret(self.x(0), self.string(self.x(0))[:self.x(1)] + self.cstr(self.x(2)) + self.string(self.x(0))[self.x(1):])
        self.hooks[27713104] = lambda: self.ret(1700000000)
        self.hooks[27712480] = lambda: self.ret(self.now * 1000)
        self.hooks[27715008] = lambda: (self.wq(self.x(0), self.now // 1000), self.wq(self.x(0) + 8, self.now % 1000 * 1000), self.ret(0))
        self.hooks[26070300] = self.service
        self.hooks[27713264] = self.next_prime
        self.tlsValues = {}
        for a, name in self.imports.items():
            if name.startswith('pthread_mutex') or name in ['pthread_once', 'pthread_key_delete']:
                self.hooks[a] = lambda: self.ret(0)
            elif name == 'pthread_getspecific':
                self.hooks[a] = lambda: self.ret(self.tlsValues.get(self.x(0), 0))
            elif name == 'pthread_setspecific':
                self.hooks[a] = lambda: (self.tlsValues.__setitem__(self.x(0), self.x(1)), self.ret(0))
            elif name == 'pthread_key_create':
                self.hooks[a] = lambda: (self.wi(self.x(0), 123), self.ret(0))
            elif name == 'pthread_self':
                self.hooks[a] = lambda: self.ret(1)
            elif 'random_deviceclE' in name:
                self.hooks[a] = lambda: self.ret(305419896)
            elif 'random_device' in name:
                self.hooks[a] = lambda: self.ret()
            elif name in ['glDisable', 'glEnable', 'glBlendFunc', 'glDepthMask', 'glClearDepthf', 'glViewport', 'glClearColor', 'glClear']:
                self.hooks[a] = self.service
            elif name in ['fmodf', 'sinf', 'cosf', 'tanf', 'sqrtf', 'acosf', 'asinf', 'atanf', 'atan2f', 'powf']:
                op = {'fmodf': math.fmod, 'sinf': math.sin, 'cosf': math.cos, 'tanf': math.tan, 'sqrtf': math.sqrt, 'acosf': math.acos, 'asinf': math.asin, 'atanf': math.atan, 'atan2f': math.atan2, 'powf': math.pow}[name]
                binary = name in ['fmodf', 'atan2f', 'powf']
                self.hooks[a] = lambda op=op, binary=binary: (self.s(0, op(self.s(0), self.s(1)) if binary else op(self.s(0))), self.ret())
        self.observe = self.observe | {13235952, 16514308, 15000796, 14871112, 19971568, 12157388, 26488776, 21957268, 10384628, 17462608, 22506148, 23071664, 18981100, 19535444, 18506868, 26656768, 25772740, 25901932, 20005276, 14318224, 8495288, 16379968, 14390900, 25944824, 26541952, 15646756, 24314512, 12746036, 25657020, 10260672, 10756732}

    def ref_boundary(self):
        if self.x(0) == 0:
            self.ret()

    def next_prime(self):
        n = max(2, self.x(0))
        while any((n % d == 0 for d in range(2, math.isqrt(n) + 1))):
            n += 1
        self.ret(n)

    def oncode(self, u, a, size, ud):
        if hasattr(self, 'touchEvents') and a == 26741104 and (self.i(self.x(1) + 12) == 0):
            ev = self.x(1)
            self.touchEvents.append({'wall': self.now, 'action': self.i(ev + 32), 'mask': self.i(29354964), 'touches': [{'p': hex(t), 'vtable': hex(self.q(t)), 'slot': self.i(t + 12), 'contactBeforeListener': self.i(t + 52), 'xy': [self.f(t + 28), self.f(t + 32)], 'pressure': self.f(t + 44), 'timestamp': self.q(t + 64)} for t in self.items(ev, 40)]})
        if hasattr(self, 'projections') and a in [15647180, 15647212]:
            sp = u.reg_read(UC_ARM64_REG_SP)
            self.projections.append({'pc': hex(a), 'lanes': hex(self.x(0)), 'ground': [self.f(sp + 144 + i * 4) for i in range(3)]})
            print('PROJECT', self.projections[-1])
        if hasattr(self, 'calls') and self.phase == 'native GameScene init prefix':
            w = self.i(a) & 4294967295
            if w & 4227858432 == 2483027968:
                imm = w & 67108863
                imm = imm - (1 << 26) if imm & 1 << 25 else imm
                self.calls.append((hex(a), hex(a + imm * 4), hex(self.x(0))))
        if hasattr(self, 'events') and a in self.observe:
            self.events.append({'pc': hex(a), 'lr': hex(self.x(30)), 'phase': self.phase, 'x': [hex(self.x(i)) for i in range(8)], 'wall': self.now})
        if hasattr(self, 'refs') and a in [21495368, 14081176] and (self.x(0) > 67108864):
            self.refs.append({'pc': hex(a), 'object': hex(self.x(0)), 'before': self.i(self.x(0) + 8), 'phase': self.phase})
        if 27709440 <= a < 27711856 and a not in self.hooks:
            return
        super().oncode(u, a, size, ud)

    def badmem(self, u, access, a, size, value, ud):
        return super().badmem(u, access, a, size, value, ud)

    def service(self):
        self.services.append({'pc': hex(self.u.reg_read(UC_ARM64_REG_PC)), 'lr': hex(self.x(30)), 'x0': hex(self.x(0)), 'phase': self.phase})
        self.ret(0)

    def typename(self, p):
        return self.cstr(self.q(self.q(self.q(p) - 8) + 8)).decode() if p else ''

    def prepare_app(self):
        app = self.q(self.q(28925784))
        self.app = app
        self.settings = self.alloc(1024)
        self.wq(app + 112, self.settings)
        self.wi(self.settings + 12, 40)
        self.audio = self.alloc(2048)
        self.wq(app + 16, self.audio)
        self.wf(self.audio + 712, 1)
        self.wq(app + 176, self.alloc(1792))
        self.account = self.alloc(256)
        self.character = self.alloc(512)
        self.wi(self.character + 12, 49)
        self.wq(self.account + 88, self.character)
        self.hooks[11962592] = lambda: self.ret(self.account)
        self.wq(app + 136, self.alloc(1536))
        self.wq(app + 224, self.alloc(256))
        provider = self.alloc(512)
        pvt = self.alloc(256)
        self.wq(provider, pvt)
        self.wq(app + 64, provider)
        for off in range(0, 256, 8):
            self.wq(pvt + off, 67117056)
        self.hooks[67117056] = self.service
        self.hooks[22101028] = lambda: self.ret(0)
        self.wq(app + 72, provider)
        self.settingsBackend = self.alloc(256)
        backendVt = self.alloc(256)
        self.wq(self.settingsBackend, backendVt)
        self.hooks[25848716] = lambda: self.ret(self.settingsBackend)
        for off in range(0, 256, 8):
            addr = 67112960 + off
            self.wq(backendVt + off, addr)
            self.hooks[addr] = (lambda: self.ret(self.x(2))) if off in [0, 8] else lambda: self.ret()
        self.phase = 'selected original ELF initializers'
        for a in [26237896, 21798880, 20180700]:
            self.call(a)
        self.phase = 'initial environment'
        self.hooks[14116172] = lambda: self.ret(provider)
        for a in [13629900, 14807660, 13114136]:
            self.hooks[a] = self.service

    def native_engine(self):
        self.phase = 'native Director getInstance'
        self.hooks[26205424] = self.service
        self.director = self.call(10756732)
        self.scheduler = self.q(self.director + 160)
        self.manager = self.q(self.director + 168)
        self.dispatcher = self.q(self.director + 176)
        self.view = self.alloc(768)
        self.wq(self.view, 28446048)
        self.wf(self.view + 72, 1)
        self.wf(self.view + 76, 1)
        self.wf(self.view + 20, 1280)
        self.wf(self.view + 24, 720)
        for a in [26385872, 23953656, 15852860]:
            self.hooks[a] = self.service
        self.hooks[16195856] = lambda: self.u.reg_write(UC_ARM64_REG_PC, 16195928)
        self.phase = 'native Director GLView attachment'
        self.call(16195752, self.director, self.view)
        assert self.u.mem_read(self.dispatcher + 292, 1)[0] == 1

    def load_chart(self, text=None, load=True):
        text = config.fixture_text() if text is None else text
        self.song, self.diff = exp010.metadata(self, songid='expedition018')
        provider = self.alloc(256)
        self.wq(provider, 27953904)
        self.hooks[12164516] = lambda: self.ret(provider)
        self.putstr(29291056, 'songs')
        self.paths = []

        def bytes_service():
            self.paths.append(self.string(self.x(1)).decode())
            self.putstr(self.q(self.x(2) + 8), text)
            self.ret(0)
        self.hooks[14124124] = bytes_service
        self.hooks[12178596] = lambda: (self.putstr(self.x(8), ''), self.ret())
        self.hooks[23416748] = lambda: (self.putstr(self.x(8), ''), self.ret())
        self.hooks[27372844] = self.service
        self.phase = 'native chart load'
        return self.call(24012708, 0, self.song, 2, 0, 40, 0, 1) if load else None

    def state(self, m):
        c = self.q(m + 40)
        t = self.q(m + 48)
        s = self.q(m + 56)
        listener = self.q(m + 336)
        return {'model': hex(m), 'vtable': hex(self.q(m)), 'type': self.typename(m), 'chart': hex(c), 'chartRef': self.i(c + 8), 'timeline': hex(t), 'timelineType': self.typename(t), 'timelineRef': self.i(t + 8), 'score': hex(s), 'scoreType': self.typename(s), 'scoreRef': self.i(s + 8), 'gauges': [(hex(g), self.typename(g), self.f(g + 16)) for g in self.items(s, 160)], 'flags': {hex(o): list(self.u.mem_read(m + o, 1))[0] for o in [312, 313, 314, 317, 328]}, 'delegate': hex(self.q(m + 64)), 'cameraRig': hex(self.q(m + 32)), 'indexGroupHeaders': [hex(p) for p in self.items(m, 136)], 'activeCount': len(self.items(m, 160)), 'contacts': len(self.items(m, 208)), 'listener': {'p': hex(listener), 'registered': self.u.mem_read(listener + 96, 1)[0], 'priority': self.i(listener + 100), 'paused': self.u.mem_read(listener + 112, 1)[0], 'enabled': self.u.mem_read(listener + 113, 1)[0]} if listener else None}
