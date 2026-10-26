"""Narrow libc services needed by the original archived OBJ reader, not a mesh parser."""
import ctypes
import math
import struct
from unicorn.arm64_const import UC_ARM64_REG_D0, UC_ARM64_REG_D1
import re


def install(n):
    observations = []
    libc = ctypes.CDLL(None)
    libc.sscanf.restype = ctypes.c_int

    def pow_double():
        def read(reg):
            return struct.unpack('<d', struct.pack('<Q', n.u.reg_read(reg)))[0]
        a, b = read(UC_ARM64_REG_D0), read(UC_ARM64_REG_D1)
        value = math.pow(a, b)
        n.u.reg_write(UC_ARM64_REG_D0, struct.unpack('<Q', struct.pack('<d', value))[0])
        observations.append({'service': 'pow', 'caller': hex(n.x(30)), 'args': [a, b], 'return': value})
        n.ret()

    def ldexp_double():
        value = struct.unpack('<d', struct.pack('<Q', n.u.reg_read(UC_ARM64_REG_D0)))[0]
        exponent = n.x(0) & 0xffffffff
        exponent = exponent - (1 << 32) if exponent & 0x80000000 else exponent
        result = math.ldexp(value, exponent)
        n.u.reg_write(UC_ARM64_REG_D0, struct.unpack('<Q', struct.pack('<d', result))[0])
        observations.append({'service': 'ldexp', 'caller': hex(n.x(30)), 'args': [value, exponent], 'return': result})
        n.ret()

    def strchr():
        pointer = n.x(0)
        index = (n.cstr(pointer) + b'\0').find(bytes([n.x(1) & 255]))
        result = 0 if index < 0 else pointer + index
        observations.append({'service': 'strchr', 'caller': hex(n.x(30)), 'found': index >= 0})
        n.ret(result)

    def vsprintf_checked():
        size, fmt, va = n.x(2), n.x(3), n.x(4)
        observations.append({'service': '__vsprintf_chk', 'caller': hex(n.x(30)), 'format': n.cstr(fmt).decode(), 'bound': size})
        n.x(1, size); n.x(2, fmt); n.x(3, va)
        n.vsnprintf()
        if n.x(0) >= size:
            raise RuntimeError('Checked OBJ formatting exceeds destination size')

    def strspn():
        accepted = set(n.cstr(n.x(1)))
        count = 0
        for value in n.cstr(n.x(0)):
            if value not in accepted:
                break
            count += 1
        observations.append({'service': 'strspn', 'caller': hex(n.x(30)), 'return': count})
        n.ret(count)

    def strcspn():
        rejected = set(n.cstr(n.x(1)))
        count = 0
        for value in n.cstr(n.x(0)):
            if value in rejected:
                break
            count += 1
        observations.append({'service': 'strcspn', 'caller': hex(n.x(30)), 'return': count})
        n.ret(count)

    def sscanf():
        text, fmt = n.cstr(n.x(0)), n.cstr(n.x(1))
        # Only the simple OBJ-reader conversion domain is supported. Fail closed elsewhere.
        if not re.fullmatch(rb'(?:\s|/|%[fds])+', fmt):
            raise RuntimeError('Unsupported OBJ sscanf format: ' + repr(fmt))
        kinds = re.findall(rb'%([fds])', fmt)
        if len(kinds) > 6 or len(text) >= 256:
            raise RuntimeError('OBJ sscanf exceeds bounded input/argument domain')
        outputs = [ctypes.c_float() if k == b'f' else ctypes.c_int() if k == b'd'
                   else ctypes.create_string_buffer(256) for k in kinds]
        count = libc.sscanf(ctypes.c_char_p(text), ctypes.c_char_p(fmt),
                            *(ctypes.byref(value) for value in outputs))
        for index in range(max(0, count)):
            value = outputs[index]
            data = value.value + b'\0' if kinds[index] == b's' else bytes(value)
            n.u.mem_write(n.x(index + 2), data)
        observations.append({'service': 'sscanf', 'caller': hex(n.x(30)),
                             'format': fmt.decode('ascii'), 'return': count})
        n.ret(count)

    for address, name in n.imports.items():
        if name == 'pow':
            n.hooks[address] = pow_double
        elif name == 'ldexp':
            n.hooks[address] = ldexp_double
        elif name == 'strchr':
            n.hooks[address] = strchr
        elif name == '__vsprintf_chk':
            n.hooks[address] = vsprintf_checked
        elif name == 'strspn':
            n.hooks[address] = strspn
        elif name == 'strcspn':
            n.hooks[address] = strcspn
        elif name == 'sscanf':
            n.hooks[address] = sscanf
    return observations
