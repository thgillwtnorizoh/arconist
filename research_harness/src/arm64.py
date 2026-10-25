# Recovered research adapter; consolidated for Expedition 024.
import config
import struct, math, json
from pathlib import Path
from collections import Counter
from unicorn import Uc, UC_ARCH_ARM64, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_INVALID
from unicorn.arm64_const import *
from elftools.elf.elffile import ELFFile

class Native:

    def __init__(self):
        self.host_calls = []
        self.u = Uc(UC_ARCH_ARM64, UC_MODE_ARM)
        self.u.mem_map(0, 34603008)
        self.u.mem_map(67108864, 34603008)
        with config.elf_stream() as f:
            e = ELFFile(f)
            for s in e.iter_segments():
                if s['p_type'] == 'PT_LOAD':
                    self.u.mem_write(s['p_vaddr'], s.data())
            for r in e.get_section_by_name('.rela.dyn').iter_relocations():
                if r['r_info_type'] == 1027:
                    self.wq(r['r_offset'], r['r_addend'])
        self.heap = 68157440
        self.now = 0
        self.hooks = {}
        self.count = Counter()
        self.history = []
        self.u.reg_write(UC_ARM64_REG_TPIDR_EL0, 101646336)
        self.u.hook_add(UC_HOOK_CODE, self.oncode)
        self.u.hook_add(UC_HOOK_MEM_INVALID, self.badmem)
        for a in [27711936, 27712832, 27713680, 27713296]:
            self.hooks[a] = lambda: self.ret(self.alloc(self.x(0)))
        self.hooks[27717136] = lambda: self.ret(self.alloc(self.x(0) * self.x(1)))
        for a in [18981100, 21495368, 14081176, 17483496, 27711968, 27713696, 27209280]:
            self.hooks[a] = lambda: self.ret()
        for a in [27711952, 27712240]:
            self.hooks[a] = self.copy
        self.hooks[27712304] = self.memset
        self.hooks[27712208] = lambda: self.ret(len(self.cstr(self.x(0))))
        for a in [27712080, 27712384]:
            self.hooks[a] = lambda: self.copy(24)
        self.hooks[27712400] = self.cast
        self.hooks[27712608] = lambda: self.ret(self.now * 1000000)
        self.hooks[27712480] = lambda: self.ret(0)
        self.hooks[27713104] = lambda: self.ret(0)
        self.hooks[17280860] = lambda: self.ret(0)
        self.hooks[14825612] = lambda: self.ret(0)
        self.hooks[12427364] = lambda: self.ret(0)
        self.hooks[67109120] = lambda: self.u.emu_stop()
        self.hooks[67109376] = lambda: self.ret(0)
        app = self.alloc(4096)
        self.wq(self.q(28925784), app)
        self.wq(app + 120, self.alloc(256))

    def badmem(self, u, access, a, size, value, ud):
        print('BADMEM', hex(a), size, 'PC', hex(u.reg_read(UC_ARM64_REG_PC)))
        return False

    def x(self, i, v=None):
        reg = UC_ARM64_REG_X0 + i if i <= 28 else [UC_ARM64_REG_X29, UC_ARM64_REG_X30][i - 29]
        if v is not None:
            self.u.reg_write(reg, v & 18446744073709551615)
        return self.u.reg_read(reg)

    def s(self, i, v=None):
        if v is not None:
            self.u.reg_write(UC_ARM64_REG_S0 + i, struct.unpack('<I', struct.pack('<f', v))[0])
        return struct.unpack('<f', struct.pack('<I', self.u.reg_read(UC_ARM64_REG_S0 + i)))[0]

    def q(self, a):
        return struct.unpack('<Q', self.u.mem_read(a, 8))[0]

    def i(self, a):
        return struct.unpack('<i', self.u.mem_read(a, 4))[0]

    def f(self, a):
        return struct.unpack('<f', self.u.mem_read(a, 4))[0]

    def wq(self, a, v):
        self.u.mem_write(a, struct.pack('<Q', v & 18446744073709551615))

    def wi(self, a, v):
        self.u.mem_write(a, struct.pack('<I', v & 4294967295))

    def wf(self, a, v):
        self.u.mem_write(a, struct.pack('<f', v))

    def wb(self, a, v):
        self.u.mem_write(a, bytes([v]))

    def alloc(self, n):
        assert n < 16777216, hex(n)
        p = self.heap
        self.heap += max(n, 1) + 63 & ~63
        assert self.heap < 100663296
        self.u.mem_write(p, bytes(n))
        return p

    def ret(self, v=None):
        if v is not None:
            self.x(0, v)
        self.u.reg_write(UC_ARM64_REG_PC, self.x(30))

    def cstr(self, a):
        out = b''
        while self.u.mem_read(a, 1) != b'\x00':
            out += self.u.mem_read(a, 1)
            a += 1
        return out

    def copy(self, n=None):
        self.u.mem_write(self.x(0), bytes(self.u.mem_read(self.x(1), self.x(2) if n is None else n)))
        self.ret()

    def memset(self):
        self.u.mem_write(self.x(0), bytes([self.x(1) & 255]) * self.x(2))
        self.ret()

    def cast(self):
        obj = self.x(0)
        target = self.x(2)
        if not obj:
            self.ret(0)
            return
        typ = self.q(self.q(obj) - 8)
        for _ in range(12):
            if typ == target:
                self.ret(obj)
                return
            parent = self.q(typ + 16)
            if not parent or parent >= 34603008:
                break
            typ = parent
        self.ret(0)

    def oncode(self, u, a, size, ud):
        if a in self.observe:
            self.count[a] += 1
            self.history.append((a, self.x(0), self.x(1), self.x(2), self.x(3), self.x(4)))
        if a in self.hooks:
            self.count[a] += 1
            self.hooks[a]()
        elif 27709440 <= a < 27754496:
            raise RuntimeError('unhandled import ' + hex(a))

    def call(self, a, *xs, fs=(), stop=67109120, regs=None, stack=None):
        self.host_calls.append(a)
        self.u.reg_write(UC_ARM64_REG_SP, 101576704)
        self.x(30, 67109120)
        for i, v in enumerate(xs):
            self.x(i, v)
        for i, v in enumerate(fs):
            self.s(i, v)
        if regs:
            for i, v in regs.items():
                self.x(i, v)
        if stack:
            for off, v in stack.items():
                self.wq(101576704 + off, v)
        self.u.emu_start(a, stop, count=5000000)
        pc = self.u.reg_read(UC_ARM64_REG_PC)
        if pc != stop:
            raise RuntimeError('did not return ' + hex(a) + ' pc ' + hex(pc))
        return self.x(0)

    def vec(self, owner, off, items):
        buf = self.alloc(max(8, len(items) * 8))
        for i, v in enumerate(items):
            self.wq(buf + i * 8, v)
        for o, v in [(0, buf), (8, buf + len(items) * 8), (16, buf + max(8, len(items) * 8))]:
            self.wq(owner + off + o, v)
        return buf

    def items(self, owner, off=0):
        return [self.q(a) for a in range(self.q(owner + off), self.q(owner + off + 8), 8)]

    def maps(self, model):
        out = []
        for hdr in self.items(model, 136):
            d = {}

            def walk(p):
                if not p:
                    return
                walk(self.q(p))
                d[self.i(p + 32)] = self.items(p, 40)
                walk(self.q(p + 8))
            walk(self.q(hdr + 8))
            out.append(d)
        return out
    observe = {22506148, 17813952, 24314512, 8818260, 21518548, 27213132, 16254316, 22712516}
