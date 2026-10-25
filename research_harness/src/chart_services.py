# Recovered research adapter; consolidated for Expedition 024.
import config
import re, struct, json, sys, hashlib
from pathlib import Path
from elftools.elf.elffile import ELFFile
from unicorn.arm64_const import *
from arm64 import Native

class BoundaryError(Exception):
    pass

class LoadingNative(Native):

    def __init__(self):
        super().__init__()
        self.streams = {}
        self.boundaries = {}
        self.imports = {}
        self.texttrace = []
        with config.elf_stream() as f:
            e = ELFFile(f)
            syms = e.get_section_by_name('.dynsym')
            plt = e.get_section_by_name('.plt')
            for idx, r in enumerate(e.get_section_by_name('.rela.plt').iter_relocations()):
                self.imports[plt['sh_addr'] + 32 + idx * 16] = syms.get_symbol(r['r_info_sym']).name
        self.observe = self.observe | {25628128, 14633560, 11541868, 17678328, 24359768, 25569812, 8088072, 19260532, 18784544, 15477340, 9307372, 16821860, 12795912, 12604148, 12463000, 14230872, 24012708, 20387652, 14775592, 26751996, 23152584}
        for a in [27712080, 27712384]:
            self.hooks[a] = lambda: self.stringret(self.x(0), self.string(self.x(1)))
        self.hooks[27712544] = self.substr
        self.hooks[27712320] = self.memchr
        self.hooks[27712128] = self.memcmp
        self.hooks[27713232] = lambda: self.ret()
        self.hooks[27712912] = lambda: self.ret(0)
        self.hooks[27712768] = lambda: self.ret(int(self.u.mem_read(self.x(0), 1)[0] == 0))
        self.hooks[27712800] = lambda: (self.wb(self.x(0), 1), self.ret())
        self.hooks[27712816] = lambda: self.ret()
        self.hooks[27711904] = lambda: self.ret(0)
        self.hooks[27715776] = self.reserve
        self.hooks[27713792] = lambda: self.ret((self.cstr(self.x(0)) > self.cstr(self.x(1))) - (self.cstr(self.x(0)) < self.cstr(self.x(1))))
        self.hooks[27712096] = self.compare
        self.hooks[27712256] = lambda: self.stringret(self.x(0), self.string(self.x(0)) + bytes(self.u.mem_read(self.x(1), self.x(2))))
        self.hooks[27712288] = lambda: self.stringret(self.x(0), self.string(self.x(0)) + self.cstr(self.x(1)))
        self.hooks[27712928] = lambda: self.stringret(self.x(0), self.string(self.x(0)) + bytes([self.x(1) & 255]))
        self.hooks[27712432] = lambda: self.stringret(self.x(0), self.cstr(self.x(1)))
        self.hooks[27713952] = self.erase
        self.hooks[27714048] = lambda: self.ret(int(chr(self.x(0) & 255).isspace()))
        self.hooks[17334036] = self.stream_init
        self.hooks[11560744] = lambda: self.ret()
        self.hooks[27714064] = lambda: self.number(True)
        self.hooks[27714096] = lambda: self.number(False)
        self.hooks[27712896] = lambda: self.ret(self.parse_num(self.cstr(self.x(0)), False))
        self.hooks[27713872] = self.atof
        self.hooks[27712352] = lambda: (self.putstr(self.x(8), str(self.x(0) & 4294967295)), self.ret())
        for a, name in self.imports.items():
            if name == '__cxa_allocate_exception':
                self.hooks[a] = lambda: self.ret(self.alloc(self.x(0)))
            if name == '__cxa_throw':
                self.hooks[a] = self.throw
        table = self.alloc(512)
        for c in range(128):
            self.wb(table + c + 1, 1 if 65 <= c <= 90 else 2 if 97 <= c <= 122 else 4 if 48 <= c <= 57 else 0)
        tableptr = self.alloc(8)
        self.wq(tableptr, table)
        self.wq(28926312, tableptr)
        self.hooks[27712864] = lambda: (_ for _ in ()).throw(BoundaryError('native out_of_range'))

    def oncode(self, u, a, size, ud):
        if a in [25628128, 17678328, 14633560]:
            self.texttrace.append((hex(a), self.string(self.x(1) if a == 14633560 else self.x(0)).decode()))
        if a in self.hooks:
            self.boundaries[a] = self.boundaries.get(a, 0) + 1
        try:
            super().oncode(u, a, size, ud)
        except RuntimeError as e:
            raise RuntimeError(str(e) + ' ' + self.imports.get(a, '') + ' caller=' + hex(self.x(30)))

    def string(self, p):
        first = self.u.mem_read(p, 1)[0]
        return bytes(self.u.mem_read(self.q(p + 16), self.q(p + 8))) if first & 1 else bytes(self.u.mem_read(p + 1, first >> 1))

    def putstr(self, p, b):
        if isinstance(b, str):
            b = b.encode()
        self.u.mem_write(p, bytes(24))
        if len(b) < 23:
            self.wb(p, len(b) * 2)
            self.u.mem_write(p + 1, b + b'\x00')
        else:
            cap = len(b) + 16 & ~15
            d = self.alloc(cap)
            self.u.mem_write(d, b + b'\x00')
            self.wq(p, cap | 1)
            self.wq(p + 8, len(b))
            self.wq(p + 16, d)
        return p

    def stringret(self, p, b):
        self.putstr(p, b)
        self.ret(p)

    def newstr(self, b):
        return self.putstr(self.alloc(24), b)

    def substr(self):
        b = self.string(self.x(1))
        start = self.x(2)
        length = self.x(3)
        if start > len(b):
            raise BoundaryError('string substring out_of_range: pos=' + str(start) + ' size=' + str(len(b)))
        self.stringret(self.x(0), b[start:] if length == 18446744073709551615 else b[start:start + length])

    def memchr(self):
        p = self.x(0)
        idx = bytes(self.u.mem_read(p, self.x(2))).find(bytes([self.x(1) & 255]))
        self.ret(0 if idx < 0 else p + idx)

    def memcmp(self):
        a = bytes(self.u.mem_read(self.x(0), self.x(2)))
        b = bytes(self.u.mem_read(self.x(1), self.x(2)))
        self.ret((a > b) - (a < b))

    def compare(self):
        a = self.string(self.x(0))[self.x(1):]
        length = self.x(2)
        if length != 18446744073709551615:
            a = a[:length]
        b = bytes(self.u.mem_read(self.x(3), self.x(4)))
        self.ret((a > b) - (a < b))

    def erase(self):
        p = self.x(0)
        b = self.string(p)
        i = self.x(1)
        count = self.x(2)
        self.stringret(p, b[:i] + b[i + count:])

    def reserve(self):
        p = self.x(0)
        size = self.x(1)
        b = self.string(p)
        current = (self.q(p) & ~1) - 1 if self.u.mem_read(p, 1)[0] & 1 else 22
        if size > current:
            cap = size + 16 & ~15
            data = self.alloc(cap)
            self.u.mem_write(data, b + b'\x00')
            self.wq(p, cap | 1)
            self.wq(p + 8, len(b))
            self.wq(p + 16, data)
        self.ret()

    def stream_init(self):
        self.streams[self.x(0)] = self.string(self.x(1))
        self.ret()

    def parse_num(self, b, isfloat):
        match = re.match(b'\\s*([+-]?(?:\\d+(?:\\.\\d*)?|\\.\\d+)(?:[eE][+-]?\\d+)?)' if isfloat else b'\\s*([+-]?\\d+)', b)
        return (float(match[1]) if isfloat else int(match[1])) if match else 0

    def number(self, isfloat):
        v = self.parse_num(self.streams[self.x(0)], isfloat)
        (self.wf if isfloat else self.wi)(self.x(1), v)
        self.ret()

    def atof(self):
        v = self.parse_num(self.cstr(self.x(0)), True)
        self.u.reg_write(UC_ARM64_REG_D0, struct.unpack('<Q', struct.pack('<d', v))[0])
        self.ret()

    def throw(self):
        raise BoundaryError('native __cxa_throw typeinfo=' + hex(self.x(1)) + ' object=' + hex(self.x(0)) + ' caller=' + hex(self.x(30)))

    def headers(self, p):
        out = {}

        def walk(a):
            if not a:
                return
            walk(self.q(a))
            out[self.string(a + 32).decode()] = self.string(a + 56).decode()
            walk(self.q(a + 8))
        walk(self.q(p + 8))
        return out

    def parse(self, text):
        return self.call(25628128, self.newstr(text), 1)
A = config.fixture_text()

def metadata(n, bpm=120, difficulty=2, override=0, songid='expedition010'):
    song = n.alloc(768)
    n.putstr(song, songid)
    n.wf(song + 392, bpm)
    diff = n.alloc(512)
    n.wi(diff + 292, difficulty)
    n.wf(diff + 80, override)
    for i in range(5):
        n.wq(song + 552 + i * 8, diff)
    return (song, diff)
