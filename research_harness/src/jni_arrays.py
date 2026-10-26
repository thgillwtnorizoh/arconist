"""Bounded supplied JNIEnv array ABI from011; native JNI updates all actual Touches."""
import struct


class InputArrays:
    def __init__(self, n):
        self.n = n
        self.handles = {}
        self.calls = []
        table = n.alloc(0x700)
        n.wq(n.env, table)
        for offset, address, function in [(0x558, 0x4000400, self.length),
                                          (0x658, 0x4000410, lambda: self.region('i')),
                                          (0x668, 0x4000420, lambda: self.region('f'))]:
            assert address not in n.hooks, 'JNI adapter address collision'
            n.wq(table + offset, address)
            n.hooks[address] = function

    def array(self, values, kind):
        assert kind in ('i', 'f') and 1 <= len(values) <= 2
        handle = self.n.alloc(16)
        data = struct.pack('<' + kind * len(values), *values)
        self.handles[handle] = (kind, data)
        return handle

    def length(self):
        kind, data = self.handles[self.n.x(1)]
        self.calls.append({'service': 'GetArrayLength', 'length': len(data) // 4, 'caller': hex(self.n.x(30))})
        self.n.ret(len(data) // 4)

    def region(self, kind):
        actual, data = self.handles[self.n.x(1)]
        start, count = self.n.x(2), self.n.x(3)
        assert actual == kind and start <= len(data) // 4 and count <= len(data) // 4 - start
        self.n.u.mem_write(self.n.x(4), data[start * 4:(start + count) * 4])
        self.calls.append({'service': 'GetIntArrayRegion' if kind == 'i' else 'GetFloatArrayRegion',
                           'start': start, 'count': count, 'caller': hex(self.n.x(30))})
        self.n.ret()

    def move(self, points, stamp):
        # IDs, X, Y and pressure products only; these are external JNI arrays.
        arrays = [self.array([point[i] for point in points], kind) for i, kind in enumerate('ifff')]
        self.n.call(0x1706960, self.n.env, 0, *arrays, stamp)
