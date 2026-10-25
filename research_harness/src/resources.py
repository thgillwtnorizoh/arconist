# Recovered research adapter; consolidated for Expedition 024.
import config
import json, sys, struct, collections, zipfile, hashlib, re, faulthandler
from pathlib import Path
from bootstrap import BootstrapNative
from elftools.elf.elffile import ELFFile
from sqlite_services import PersistenceNative
from results_services import CompletionNative
from action_services import ActionNative
from ending_services import EndingNative
from unicorn.arm64_const import *

class ResourceNative(BootstrapNative):

    def __init__(self):
        super().__init__()
        self.resourceLog = []
        self.nativeCalls = collections.deque(maxlen=160)
        self.blHistory = []
        self.mapProbes = []
        self.instructionCache = {}
        self.archive = zipfile.ZipFile(config.archive_path)
        with config.elf_stream() as f:
            e = ELFFile(f)
            syms = e.get_section_by_name('.dynsym')
            exports = {s.name: s['st_value'] for s in syms.iter_symbols() if s['st_value']}
            self.symbolRelocations = 0
            for r in e.get_section_by_name('.rela.dyn').iter_relocations():
                if r['r_info_type'] in [257, 1025]:
                    v = syms.get_symbol(r['r_info_sym'])['st_value']
                    if v:
                        self.wq(r['r_offset'], v + r['r_addend'])
                        self.symbolRelocations += 1
        for a, name in self.imports.items():
            if name in exports and a not in self.hooks:
                self.hooks[a] = lambda target=exports[name]: self.u.reg_write(UC_ARM64_REG_PC, target)
        self.glCalls = []
        self.glNext = 1
        self.jumpBuffers = {}
        self.hooks[27713104] = self.time_service if hasattr(self, 'time_service') else self.resource_time
        self.hooks[27713728] = self.service
        for a, name in self.imports.items():
            if name.startswith('gl'):
                self.hooks[a] = lambda name=name: self.gl_service(name)
            elif name in ['setjmp', '_setjmp', 'sigsetjmp', '__sigsetjmp']:
                self.hooks[a] = self.setjmp
            elif name in ['longjmp', '_longjmp', 'siglongjmp']:
                self.hooks[a] = self.longjmp
            elif name == 'strstr':
                self.hooks[a] = self.strstr
            elif name == '__strlen_chk':
                self.hooks[a] = self.strlen_chk
            elif name == 'realloc':
                self.hooks[a] = self.runtime_realloc
            elif name == 'malloc_usable_size':
                self.hooks[a] = lambda: self.ret(self.allocationSizes[self.x(0)])
        self.hooks[27713088] = lambda: self.stringret(self.x(0), self.string(self.x(0))[:self.x(1)] + bytes(self.u.mem_read(self.x(2), self.x(3))) + self.string(self.x(0))[self.x(1):])
        self.hooks[27714240] = self.vsnprintf
        self.hooks[27716720] = self.rfind
        self.hooks[27712400] = self.cpp_cast
        self.observe = self.observe | {9809744, 17301376, 11519624, 8321760, 25653704, 25085072, 17721940, 14476752, 8835984, 27309564, 13976148, 18981272, 16368684, 13203092, 24196980, 21507380}

    def resource_time(self):
        if self.x(0):
            self.wq(self.x(0), 1700000000)
        self.ret(1700000000)

    def strlen_chk(self):
        length = len(self.cstr(self.x(0)))
        assert length < self.x(1)
        self.ret(length)

    def strstr(self):
        p = self.x(0)
        i = self.cstr(p).find(self.cstr(self.x(1)))
        self.ret(0 if i < 0 else p + i)

    def call(self, a, *args, **kw):
        try:
            return super().call(a, *args, **kw)
        except RuntimeError as e:
            if a != 14871112 or not str(e).startswith('did not return'):
                raise
            stop = kw.get('stop', 67109120)
            for chunk in range(4):
                pc = self.u.reg_read(UC_ARM64_REG_PC)
                print('OBSERVATION_BUDGET_EXTEND', chunk + 1, hex(pc), len(self.resourceLog), flush=True)
                self.u.emu_start(pc, stop, count=5000000)
                if self.u.reg_read(UC_ARM64_REG_PC) == stop:
                    return self.x(0)
            raise RuntimeError('GameScene initializer exceeded 25 million original instructions at ' + hex(self.u.reg_read(UC_ARM64_REG_PC)))

    def alloc(self, n):
        if not hasattr(self, 'allocationSizes'):
            self.allocationSizes = {}
        p = super().alloc(n)
        self.allocationSizes[p] = n
        return p

    def runtime_realloc(self):
        old, size = (self.x(0), self.x(1))
        if not size:
            self.ret(0)
            return
        p = self.alloc(size)
        if old:
            self.u.mem_write(p, bytes(self.u.mem_read(old, min(size, self.allocationSizes[old]))))
        self.ret(p)

    def setjmp(self):
        self.jumpBuffers[self.x(0)] = self.u.context_save()
        self.ret(0)

    def longjmp(self):
        buf, val = (self.x(0), self.x(1))
        self.u.context_restore(self.jumpBuffers[buf])
        self.ret(val or 1)

    def next_prime(self):
        if self.x(0) > 1000000:
            print('PRIME_BOUNDARY', hex(self.x(0)), 'lr', hex(self.x(30)), 'calls', json.dumps(list(self.nativeCalls)[-35:]), flush=True)
            raise RuntimeError('oversized next_prime input ' + hex(self.x(0)))
        super().next_prime()

    def vsnprintf(self):
        fmt = self.cstr(self.x(2)).decode()
        va = self.x(3)
        stack, gt, vt = (self.q(va), self.q(va + 8), self.q(va + 16))
        go, vo = (self.i(va + 24), self.i(va + 28))

        def arg(fp=False):
            nonlocal stack, go, vo
            if fp and vo < 0:
                p = vt + vo
                vo += 16
            elif not fp and go < 0:
                p = gt + go
                go += 8
            else:
                p = stack
                stack += 8
            return struct.unpack('<d', self.u.mem_read(p, 8))[0] if fp else self.q(p)

        def part(m):
            token = m.group()
            kind = token[-1]
            if token == '%%':
                return '%'
            v = arg(kind in 'fFeEgGaA')
            if kind == 's':
                v = self.cstr(v).decode(errors='replace') if v else '(null)'
            elif kind == 'p':
                return hex(v)
            elif kind in 'di':
                v = v - (1 << 64) if v >> 63 else v
            token = re.sub('(ll|l|z|h|j|t)(?=[diuoxX])', '', token)
            return token % v
        out = re.sub('%(?:%|[-+ #0]*[0-9]*(?:\\.[0-9]+)?(?:ll|l|z|h|j|t)?[sdiuoxXpcfFeEgG])', part, fmt).encode()
        if self.x(1):
            self.u.mem_write(self.x(0), out[:self.x(1) - 1] + b'\x00')
        self.ret(len(out))

    def texture_placeholder(self):
        self.phase = 'native graphics placeholder resource'
        self.placeholderSprite = self.call(8835984)
        self.placeholderTexture = self.call(20104300, self.q(self.director + 248), self.newstr('/cc_2x2_white_image'))
        assert self.placeholderTexture
        self.textureRequests = []

        def texture():
            self.textureRequests.append({'path': self.string(self.x(1)).decode(), 'lr': hex(self.x(30)), 'texture': hex(self.placeholderTexture)})
            self.ret(self.placeholderTexture)
        self.hooks[24557252] = texture

    def prepare_app(self):
        super().prepare_app()
        self.phase = 'native graphics-context registry static initializer'
        self.call(21770368)
        self.call(25768364)
        self.call(8956216)
        self.call(21344672)
        status = self.alloc(768)
        vt = self.alloc(256)
        self.wq(status, vt)
        self.wq(self.app + 128, status)
        for off in range(0, 256, 8):
            self.wq(vt + off, 67117056)
        self.hooks.pop(14825612, None)

    def gl_service(self, name):
        self.glCalls.append({'name': name, 'lr': hex(self.x(30))})
        if name in ['glCreateProgram', 'glCreateShader']:
            self.glNext += 1
            self.ret(self.glNext)
        elif name in ['glGetProgramiv', 'glGetShaderiv']:
            self.wi(self.x(2), 1 if self.x(1) in [35713, 35714] else 0)
            self.ret()
        elif name in ['glGenBuffers', 'glGenTextures', 'glGenVertexArrays', 'glGenFramebuffers', 'glGenRenderbuffers']:
            for i in range(self.x(0)):
                self.glNext += 1
                self.wi(self.x(1) + i * 4, self.glNext)
            self.ret()
        elif name == 'glGetIntegerv':
            self.wi(self.x(1), 4096 if self.x(0) == 3379 else 16)
            self.ret()
        elif name in ['glGetUniformLocation', 'glGetAttribLocation']:
            self.ret(-1)
        elif name == 'glGetError':
            self.ret(0)
        else:
            self.ret(0)

    def cpp_cast(self):
        obj, target = (self.x(0), self.x(2))
        if not obj:
            self.ret(0)
            return
        vt = self.q(obj)
        top = obj + struct.unpack('<q', self.u.mem_read(vt - 16, 8))[0]
        typ = self.q(vt - 8)
        found = []

        def visit(t, p, seen):
            if (t, p) in seen:
                return
            seen = seen | {(t, p)}
            if t == target:
                found.append(p)
            if not 0 < t < 34603008:
                return
            flags, count = (self.i(t + 16), self.i(t + 20))
            if 0 <= flags < 4 and 0 < count < 32:
                for i in range(count):
                    base = self.q(t + 24 + i * 16)
                    bits = struct.unpack('<q', self.u.mem_read(t + 32 + i * 16, 8))[0]
                    off = bits >> 8
                    if bits & 1:
                        off = struct.unpack('<q', self.u.mem_read(self.q(p) + off, 8))[0]
                    visit(base, p + off, seen)
            else:
                parent = self.q(t + 16)
                if 27262976 < parent < 29360128:
                    visit(parent, p, seen)
        visit(typ, top, set())
        self.ret(found[0] if found and len(set(found)) == 1 else 0)

    def rfind(self):
        b = self.string(self.x(0))
        pos = min(len(b) - 1, self.x(2))
        self.ret(b.rfind(bytes([self.x(1) & 255]), 0, pos + 1))

    def display_metadata(self):
        header = self.song + 32
        node = self.alloc(96)
        self.wq(node + 16, header + 8)
        self.wb(node + 24, 1)
        self.putstr(node + 32, 'en')
        self.putstr(node + 56, 'Expedition 019')
        self.wq(header, node)
        self.wq(header + 8, node)
        self.wq(header + 16, 1)
        self.putstr(self.app + 232, 'en')

    def resource_services(self):
        p = self.call(12164516)
        vt = self.q(p)
        self.provider = p
        self.hooks[self.q(vt + 80)] = lambda: self.stringret(self.x(8), self.string(self.x(1)))
        self.hooks[self.q(vt + 264)] = lambda: self.ret(int('assets/' + self.string(self.x(1)).decode() in self.archive.namelist()))
        self.hooks[self.q(vt + 48)] = self.resource_data
        self.texture_placeholder()
        aff_service = self.hooks[14124124]

        def file_string():
            path = self.string(self.x(1)).decode()
            if path.endswith('.aff'):
                aff_service()
                return
            member = 'assets/' + path
            b = self.archive.read(member) if member in self.archive.namelist() else b''
            self.resourceLog.append({'path': path, 'bytes': len(b), 'api': 'string reader', 'lr': hex(self.x(30))})
            self.putstr(self.q(self.x(2) + 8), b)
            self.ret(0)
        self.hooks[14124124] = file_string

    def resource_data(self):
        name = self.string(self.x(1)).decode()
        member = 'assets/' + name
        b = self.archive.read(member) if member in self.archive.namelist() else b''
        p = self.alloc(max(1, len(b)))
        self.u.mem_write(p, b)
        out = self.x(8)
        self.wq(out, p if b else 0)
        self.wq(out + 8, len(b))
        self.resourceLog.append({'path': name, 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest(), 'lr': hex(self.x(30)), 'data': hex(out)})
        self.ret()

    def oncode(self, u, a, size, ud):
        if hasattr(self, 'nativeCalls') and a == 20534784 and (len(self.mapProbes) < 8):
            self.mapProbes.append({'p': hex(self.x(0)), 'lr': hex(self.x(30)), 'args': [hex(self.x(i)) for i in range(3)], 'header': [hex(self.q(self.x(0) + i * 8)) for i in range(3)], 'calls': list(self.nativeCalls)[-10:]})
            print('MAP_PROBE', self.mapProbes[-1], flush=True)
        if hasattr(self, 'nativeCalls'):
            w = self.instructionCache.get(a)
            if w is None:
                w = self.i(a) & 4294967295
                self.instructionCache[a] = w
            if w & 4227858432 == 2483027968:
                imm = w & 67108863
                imm = imm - (1 << 26) if imm & 1 << 25 else imm
                self.nativeCalls.append([hex(a), hex(a + imm * 4), hex(self.x(0)), hex(self.x(1))])
            elif w & 4294966303 == 3594452992:
                self.nativeCalls.append([hex(a), 'blr ' + hex(self.x(w >> 5 & 31)), hex(self.x(0)), hex(self.x(1))])
        super().oncode(u, a, size, ud)

    def badmem(self, u, access, a, size, value, ud):
        return super().badmem(u, access, a, size, value, ud)

class RuntimeNative(ResourceNative, PersistenceNative):

    def __init__(self):
        super().__init__()
        self.native_sqlite = True
        self.transitionRequests = []
        self.resultScenes = []
        self.animationEvents = []
        self.lifecycle = []
        self.observe = self.observe | {12746036, 15058688, 26983888, 27594836, 25529404, 23556720, 21487336, 15774860, 26153408, 13702968, 25673928, 10483216, 24166920, 23740868, 9842836, 8982864, 14429256, 20271828, 19553888, 9842992, 26182636, 25616408, 11609784, 26672372, 11136676, 18067232, 22658540, 20791108, 14037176, 10420192, 24723340, 25944824, 13687828, 18962412, 21507380, 8216892, 8240828}
        for a in [18378608, 12870884, 26995904, 16882712, 17078360, 13107376, 10298648, 10256784, 11335832]:
            self.hooks[a] = self.service
        self.hooks[8982928] = self.init_save_segment
        self.hooks[8984200] = lambda: self.u.reg_write(UC_ARM64_REG_PC, 8987036)
        self.hooks[8987100] = lambda: self.u.reg_write(UC_ARM64_REG_PC, 8988896)
        self.hooks[23740984] = self.supply_panels
        self.hooks[18962460] = lambda: self.u.reg_write(UC_ARM64_REG_PC, 18962508)
        self.hooks[10483216] = lambda: self.resultScenes.append(self.x(0))
        self.hooks[10260672] = self.replacement_observer

    def replacement_observer(self):
        if self.x(1) and 'TransitionShutter' in self.typename(self.x(1)):
            self.transitionRequests.append(self.x(1))

    def prepare_runtime(self):
        self.open_db()
        self.wq(self.app + 48, self.db)
        self.left = self.alloc(1536)
        self.right = self.alloc(1536)
        for p in [self.left, self.right]:
            self.call(20005276, p)
            self.wf(p + 960, 100)
        control = self.q(self.app + 136)
        v = self.alloc(1408)
        self.wq(control, v)
        self.wq(v + 1288, 67110944)
        self.hooks[67110944] = self.service
        for a in [8305904, 24205096, 24337788, 17280860]:
            self.hooks[a] = self.service

    def tick(self, dt):
        self.phase = '019 original Scheduler dt ' + str(dt)
        self.now += round(dt * 1000)
        self.call(20791108, self.scheduler, fs=(dt,))

    def oncode(self, u, a, size, ud):
        if hasattr(self, 'animationEvents') and a in [25529404, 23556720, 21487336]:
            row = {'pc': hex(a), 'lr': hex(self.x(30)), 'wall': self.now}
            if a == 25529404:
                f = self.q(self.x(2) + 32)
                c = self.q(f + 64)
                row.update(wrapper=hex(f), wrapperScene=hex(self.q(f + 16)), continuation=hex(c), continuationScene=hex(self.q(c + 8)))
            elif a == 21487336:
                row['capture'] = hex(self.q(self.x(0) + 8))
            self.animationEvents.append(row)
        if hasattr(self, 'lifecycle') and a in [24723340, 20791108, 10420192, 25944824, 17462608]:
            self.lifecycle.append({'pc': hex(a), 'wall': self.now, 'frame': self.i(self.director + 308) if hasattr(self, 'director') else None, 'sceneStamp': self.i(self.scene + 1232) if hasattr(self, 'scene') else None})
        super().oncode(u, a, size, ud)
    init_save_segment = CompletionNative.init_save_segment
    supply_panels = ActionNative.supply_panels
    action_state = ActionNative.action_state
    timers = CompletionNative.timers
    animation_state = EndingNative.animation_state

def component_info(n, p):
    c = n.q(p + 456)
    out = []
    if not c:
        return out
    b = n.q(c + 16)
    while b:
        out.append({'name': n.string(b + 16).decode(errors='replace'), 'component': hex(n.q(b + 40)), 'type': n.typename(n.q(b + 40))})
        b = n.q(b)
    return out

def hierarchy(n, p):
    out = []

    def node(q, parent=None):
        row = {'p': hex(q), 'type': n.typename(q), 'vtable': hex(n.q(q)), 'name': n.string(q + 352).decode(errors='replace'), 'parent': hex(n.q(q + 328)), 'ref': n.i(q + 8), 'tag': n.i(q + 344), 'components': component_info(n, q)}
        out.append(row)
        for c in n.items(n.q(q + 320)):
            node(c, q)
    node(p)
    return out
