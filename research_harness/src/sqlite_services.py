# Recovered research adapter; consolidated for Expedition 024.
import config
import sys, json, struct
from pathlib import Path
from elftools.elf.elffile import ELFFile
from chart_services import LoadingNative
from unicorn.arm64_const import *

class PersistenceNative(LoadingNative):

    def __init__(self, native_sqlite=False):
        self.sizes = {}
        super().__init__()
        self.native_sqlite = native_sqlite
        self.sql = []
        self.statements = {}
        self.nativeSqlCalls = []
        self.io = []
        with config.elf_stream() as f:
            e = ELFFile(f)
            self.exports = {s.name: s['st_value'] for s in e.get_section_by_name('.dynsym').iter_symbols() if s['st_value']}
        self.observe = self.observe | {20271828, 19553888, 14925908, 26653228, 14961756, 12634024, 23071664, 20009016, 19551604, 17649840, 14429648, 14839364}
        self.returns = {}
        self.sqlmeta = {}
        self.apiByAddress = {self.exports[name]: name for name in ['sqlite3_prepare', 'sqlite3_prepare_v2', 'sqlite3_bind_int', 'sqlite3_bind_text', 'sqlite3_step', 'sqlite3_finalize']}
        self.hooks[27712592] = lambda: self.ret(len(self.cstr(self.x(0))))
        self.hooks[27712512] = self.string_insert
        self.hooks[27712528] = lambda: (self.putstr(self.x(8), self.cstr(self.x(0)) + self.string(self.x(1))), self.ret())
        self.errno = self.alloc(8)
        self.wi(self.errno, 2)
        for a, name in self.imports.items():
            if name.startswith('pthread_mutex'):
                self.hooks[a] = lambda: self.ret(0)
            elif name == 'pthread_self':
                self.hooks[a] = lambda: self.ret(4660)
            elif name == 'malloc_usable_size':
                self.hooks[a] = lambda: self.ret(self.sizes[self.x(0)])
            elif name == 'realloc':
                self.hooks[a] = self.realloc
            elif name == 'getpid':
                self.hooks[a] = lambda: self.ret(1)
            elif name == 'gettimeofday':
                self.hooks[a] = self.gettimeofday
            elif name == 'open':
                self.hooks[a] = self.open_external
            elif name == '__errno':
                self.hooks[a] = lambda: self.ret(self.errno)
            elif name == 'time':
                self.hooks[a] = self.time_service

    def time_service(self):
        if self.x(0):
            self.wq(self.x(0), 1700000000)
        self.ret(1700000000)

    def open_external(self):
        path = self.cstr(self.x(0)).decode()
        self.io.append(path)
        assert path == '/dev/urandom', path
        self.ret(-1)

    def gettimeofday(self):
        self.wq(self.x(0), 1700000000)
        self.wq(self.x(0) + 8, 0)
        self.ret(0)

    def alloc(self, n):
        p = super().alloc(n)
        self.sizes[p] = n
        return p

    def string_insert(self):
        p = self.x(0)
        b = self.string(p)
        i = self.x(1)
        self.stringret(p, b[:i] + self.cstr(self.x(2)) + b[i:])

    def oncode(self, u, a, size, ud):
        if self.native_sqlite and a in self.returns:
            for record in self.returns.pop(a):
                if 'out' in record:
                    h = self.q(record.pop('out'))
                    record['stmt'] = hex(h)
                    self.sqlmeta[h] = record['sql']
                record['rc'] = self.x(0) & 4294967295
        if self.native_sqlite and a in self.apiByAddress:
            name = self.apiByAddress[a]
            row = {'api': name, 'caller': hex(self.x(30))}
            if 'prepare' in name:
                row.update({'sql': self.cstr(self.x(1)).decode(), 'out': self.x(3)})
                self.returns.setdefault(self.x(30), []).append(row)
            else:
                row.update({'stmt': hex(self.x(0)), 'sql': self.sqlmeta.get(self.x(0))})
                if name == 'sqlite3_bind_int':
                    row.update({'index': self.x(1), 'value': self.x(2) & 4294967295})
                if name == 'sqlite3_bind_text':
                    row.update({'index': self.x(1), 'value': self.cstr(self.x(2)).decode()})
            self.sql.append(row)
        if self.native_sqlite and a in self.imports and self.imports[a].startswith('sqlite3_') and (self.imports[a] in self.exports):
            self.nativeSqlCalls.append(self.imports[a])
            u.reg_write(UC_ARM64_REG_PC, self.exports[self.imports[a]])
            return
        super().oncode(u, a, size, ud)

    def realloc(self):
        old, size = (self.x(0), self.x(1))
        new = self.alloc(size)
        if old:
            self.u.mem_write(new, bytes(self.u.mem_read(old, min(self.sizes[old], size))))
        self.ret(new)

    def open_db(self):
        h = self.alloc(8)
        rc = self.call(self.exports['sqlite3_open'], self.newstr(':memory:') + 1, h)
        assert rc == 0, rc
        self.sqlite = self.q(h)
        self.db = self.alloc(512)
        self.wq(self.db, self.sqlite)
        self.wb(self.db + 256, 1)
        self.exec_sql(self.cstr(5480747).decode())
        self.exec_sql(self.cstr(5554205).decode())
        self.exec_sql(self.cstr(5437071).decode())
        self.exec_sql(self.cstr(5712242).decode())

    def exec_sql(self, sql):
        err = self.alloc(8)
        rc = self.call(self.exports['sqlite3_exec'], self.sqlite, self.newstr(sql) + 1 if len(sql) < 23 else self.q(self.newstr(sql) + 16), 0, 0, err)
        if rc:
            raise RuntimeError('SQLite rc=' + str(rc) + ' ' + (self.cstr(self.q(err)).decode() if self.q(err) else '') + ' SQL=' + sql)

    def query(self, sql):
        ptr = self.alloc(8)
        s = self.newstr(sql)
        p = s + 1 if self.u.mem_read(s, 1)[0] & 1 == 0 else self.q(s + 16)
        rc = self.call(self.exports['sqlite3_prepare_v2'], self.sqlite, p, -1, ptr, 0)
        assert rc == 0, rc
        stmt = self.q(ptr)
        count = self.call(self.exports['sqlite3_column_count'], stmt)
        cols = []
        for i in range(count):
            cols.append(self.cstr(self.call(self.exports['sqlite3_column_name'], stmt, i)).decode())
        rows = []
        while True:
            rc = self.call(self.exports['sqlite3_step'], stmt)
            if rc == 101:
                break
            assert rc == 100, rc
            vals = []
            for i in range(count):
                typ = self.call(self.exports['sqlite3_column_type'], stmt, i)
                if typ == 5:
                    vals.append(None)
                elif typ == 3:
                    vals.append(self.cstr(self.call(self.exports['sqlite3_column_text'], stmt, i)).decode())
                else:
                    v = self.call(self.exports['sqlite3_column_int64'], stmt, i)
                    vals.append(v - (1 << 64) if v >> 63 else v)
            rows.append(dict(zip(cols, vals)))
        self.call(self.exports['sqlite3_finalize'], stmt)
        return rows

    def result(self, score=9000000, category=1, song='expedition013', difficulty=2, partition=0, mode=0, date=100):
        r = self.alloc(256)
        self.wq(r, 28333248)
        self.wi(r + 12, 700255)
        self.wi(r + 16, score)
        self.wb(r + 177, 1)
        self.wi(r + 20, 10)
        self.wi(r + 24, 10)
        self.wi(r + 28, 1)
        self.wi(r + 32, 1)
        self.wi(r + 36, 1)
        self.wi(r + 40, 80)
        self.wi(r + 48, date)
        self.putstr(r + 56, song)
        self.wi(r + 80, difficulty)
        self.wi(r + 84, mode)
        self.wi(r + 88, partition)
        if category == 0:
            self.wi(r + 40, -1)
        elif category == 2:
            self.wi(r + 32, 0)
        elif category == 3:
            self.wi(r + 32, 0)
            self.wi(r + 28, 0)
        elif category == 4:
            self.wi(r + 84, 1)
        elif category == 5:
            self.wi(r + 84, 2)
        assert self.call(19551604, r) == category
        return r
