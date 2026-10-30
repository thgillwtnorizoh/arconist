"""040-only persistence facade and original application/Settings producer prefix.

The existing bootstrap's unused app/Settings shells are discarded before entry.
Original 1a146a0 allocates the replacement app and Settings, publishes both, and
calls the complete loader. We stop at its natural post-loader return boundary;
the unrelated later application initialization is not claimed executed.
"""
from solo_entry import SoloNative
from unicorn import UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm64_const import UC_ARM64_REG_PC


def signed32(v):
    v &= 0xffffffff
    return v - 0x100000000 if v & 0x80000000 else v


class OffsetNative(SoloNative):
    def __init__(self, values, evidence):
        self.offset_inputs = dict(values)
        self.offset_producer = evidence
        self.protected_results = []
        super().__init__()

    def check_host_write(self, address, size):
        for lo, hi in self.protected_results:
            if address < hi and address + size > lo:
                raise RuntimeError('Host write to protected native result ' + hex(address))

    def wi(self, address, value):
        self.check_host_write(address, 4)
        return super().wi(address, value)

    def wq(self, address, value):
        self.check_host_write(address, 8)
        return super().wq(address, value)

    def wf(self, address, value):
        self.check_host_write(address, 4)
        return super().wf(address, value)

    def wb(self, address, value):
        self.check_host_write(address, 1)
        return super().wb(address, value)

    def prepare_app(self):
        super().prepare_app()
        e = self.offset_producer
        e.update(status='running', getters=[], calls=[], writes=[], external_rebindings=[])
        old_app, old_settings = self.app, self.settings
        fields = {o: self.q(old_app + o) for o in
                  [0x10,0x28,0x30,0x38,0x40,0x48,0x50,0x58,0x68,0x78,
                   0x80,0x88,0xb0,0xc0,0xe0]}
        values = {'language':'en', 'installId':'expedition040-synthetic',
                  'highspeed_int':40, **self.offset_inputs}
        e.update(external_inputs=values, unused_bootstrap_shell={
            'app':hex(old_app), 'settings':hex(old_settings)},
            backend=hex(self.settingsBackend), owner_entry_elf_va='0x1a146a0',
            owner_observation_stop_elf_va='0x1a14770',
            full_application_initialization='not_run_after_settings_loader')
        vt = self.q(self.settingsBackend)

        def getter(off):
            key = self.cstr(self.x(1)).decode()
            default = (self.string(self.x(2)).decode() if off == 0x20 else
                       self.s(0) if off == 0x10 else signed32(self.x(2)))
            value = values.get(key, default)
            e['getters'].append({'phase':self.phase, 'backend':hex(self.x(0)),
                'virtual_offset':hex(off), 'key':key, 'default':default,
                'present':key in values, 'returned':value,
                'lr_elf_va':hex(self.x(30))})
            if off == 0x20:
                self.stringret(self.x(8), value)
            elif off == 0x10:
                self.s(0, value); self.ret()
            else:
                self.ret(value)
        for off in [0,8,0x10,0x20]:
            address = 0x4003800 + off
            self.wq(vt + off, address)
            self.hooks[address] = lambda off=off: getter(off)

        # Existing raw-resource services are needed earlier than load_chart here.
        provider = fields[0x48]
        self.hooks[0xb99da4] = lambda: self.ret(provider)
        self.hooks[0x1a1ad2c] = self.service
        for off in [0x48,0xa0]:
            address = 0x4003900 + off
            self.wq(self.q(provider) + off, address)
            self.hooks[address] = lambda: self.stringret(self.x(8), '')

        produced = {}
        def written(u, access, address, size, value, ud):
            base = produced['settings'] if address >= produced.get('settings',1<<64) and address < produced.get('settings',0)+0x90 else produced['app']
            e['writes'].append({'pc_elf_va':hex(u.reg_read(UC_ARM64_REG_PC)),
                'object':'settings' if base==produced.get('settings') else 'application',
                'pointer':hex(base), 'offset':hex(address-base), 'size':size,
                'before':int.from_bytes(u.mem_read(address,size),'little'), 'value':value})
        def observe(u, pc, size, ud):
            e['calls'].append({'pc_elf_va':hex(pc), 'lr_elf_va':hex(self.x(30)),
                'x0':hex(self.x(0)), 'x27':hex(self.x(27)), 'phase':self.phase})
            if pc == 0x1a1470c:
                produced['app'] = self.x(27)
                u.hook_add(UC_HOOK_MEM_WRITE,written,begin=produced['app']+0x70,
                           end=produced['app']+0x77)
            elif pc == 0x1a14768:
                produced['settings'] = self.x(0)
                self.protected_results.append((self.x(0),self.x(0)+0xc))
                u.hook_add(UC_HOOK_MEM_WRITE,written,begin=self.x(0),end=self.x(0)+0x8f)
        for pc in [0x1a146a0,0x15779f0,0x1a1470c,0x1a14728,0x1a14768,0x1a02b48]:
            self.u.hook_add(UC_HOOK_CODE,observe,begin=pc,end=pc)
        # Restore the original zero-initialized singleton before native creation;
        # the existing prepared shell is not consumed by this experiment.
        global_address = self.q(0x1b95f58)
        self.wq(global_address,0)
        def singleton_written(u,access,address,size,value,ud):
            e['writes'].append({'pc_elf_va':hex(u.reg_read(UC_ARM64_REG_PC)),
                'object':'application_singleton','pointer':hex(address),'offset':'0x0',
                'size':size,'before':self.q(address),'value':value})
        self.u.hook_add(UC_HOOK_MEM_WRITE,singleton_written,begin=global_address,end=global_address+7)
        self.phase = '040 original application/Settings owner prefix'
        self.call(0x1a146a0,0,fields[0x38],fields[0x40],fields[0x48],
                  fields[0x68],fields[0x88],fields[0x80],0,stop=0x1a14770)
        self.app = self.q(global_address)
        self.settings = self.q(self.app+0x70)
        assert self.app == produced['app'] and self.app != old_app
        assert self.settings == produced['settings'] and self.settings != old_settings
        assert any(w['object']=='application' and w['pc_elf_va']=='0x1a14768'
                   and w['value']==self.settings for w in e['writes'])
        assert next(r for r in e['calls'] if r['pc_elf_va']=='0x1a02b48')['lr_elf_va']=='0x1a14770'
        assert any(w['object']=='application_singleton' and w['pc_elf_va']=='0x1a1470c' and w['value']==self.app for w in e['writes'])
        self.protected_results.append((self.app+0x70,self.app+0x78))
        self.protected_results.append((global_address,global_address+8))
        e['application_singleton_address']=hex(global_address)
        for off,value in fields.items():
            if off in [0x40,0x48]:
                assert self.q(self.app+off)==value
                continue
            self.wq(self.app+off,value)
            e['external_rebindings'].append({'application_offset':hex(off),'pointer':hex(value)})
        e.update(status='pass',application=hex(self.app),settings=hex(self.settings),
                 loaded_fields={'preset':self.i(self.settings),'regular':self.i(self.settings+4),
                                'alternate':self.i(self.settings+8),'speed_tenths':self.i(self.settings+0xc)},
                 host_result_writes=0)
