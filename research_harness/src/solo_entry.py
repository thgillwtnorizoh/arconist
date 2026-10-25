# Recovered research adapter; consolidated for Expedition 024.
import config
from menu_services import MenuNative
from track_services import *
from unicorn import UC_HOOK_MEM_READ

class SoloNative(MenuNative):

    def __init__(self):
        super().__init__()
        self.soloTrace = []
        self.observe |= {15604092, 15606292, 24921588, 26458792, 26751996, 11317532, 17439492, 19912288, 16221820, 8636968, 25811708, 15607216, 15607228, 15608228, 15608232, 15608296, 15608300, 15608508, 15608520, 19323932, 26458832, 11317848, 17440260, 19912536, 16222440, 8638244, 24921712, 9842972, 21950616}

    def oncode(self, u, a, size, ud):
        if hasattr(self, 'soloTrace') and a in self.observe and (a in {15604092, 15606292, 24921588, 26458792, 11317532, 17439492, 19912288, 16221820, 8636968, 25811708, 15607216, 15607228, 15608228, 15608232, 15608296, 15608300, 15608508, 15608520, 19323932, 26458832, 11317848, 17440260, 19912536, 16222440, 8638244, 24921712}):
            row = {'pc': hex(a), 'lr': hex(self.x(30)), 'x': [hex(self.x(i)) for i in range(8)], 'phase': self.phase, 'wall': self.now}
            self.soloTrace.append(row)
            print('SOLO_EVENT', row, flush=True)
            if a == 15608296:
                row['stack'] = [self.q(u.reg_read(UC_ARM64_REG_SP) + i * 8) for i in range(6)]
        super().oncode(u, a, size, ud)

    def null_read(self, u, access, a, size, value, ud):
        raise RuntimeError('native low-page read addr=' + hex(a) + ' pc=' + hex(u.reg_read(UC_ARM64_REG_PC)))

def setup(available):
    n = SoloNative()
    n.prepare_app()
    n.native_engine()
    n.load_chart(load=False)
    n.putstr(n.song, 'sayonarahatsukoi')
    n.display_metadata()
    n.resource_services()
    for a in [25983552, 8835096, 12463352, 23990720, 16545704, 11336160, 18560508, 19515684, 16874116, 20897548]:
        n.hooks[a] = n.service
    n.hooks[21678532] = lambda: n.ret(n.song if n.string(n.x(1)) == n.string(n.song) else 0)
    n.wi(n.diff + 292, 0)
    n.putstr(n.diff + 184, 'sayonarahatsukoi')
    n.putstr(n.song + 408, 'base')
    n.wf(n.song + 392, 178)
    n.wb(n.song + 592, int(available))
    n.wq(n.song + 400, 0)
    n.wb(n.song + 352, 0)
    n.wi(n.diff + 236, 0)
    n.wb(n.diff + 240, 0)
    n.wq(n.diff, 0)
    n.modeSetting = n.alloc(8)
    n.wi(n.modeSetting, 0)
    n.wq(n.app + 192, n.modeSetting)
    n.localState = n.alloc(1024)
    n.wq(n.app + 56, n.localState)
    n.profileState = n.alloc(512)
    n.wq(n.app + 40, n.profileState)
    n.menu = n.alloc(1424)
    n.phase = '022 original SongSelectScene constructor'
    n.call(24462400, n.menu, 0, 0)
    n.selection = n.q(n.q(n.menu + 872))
    n.phase = '022 original selected pair setter'
    n.call(21950616, n.q(n.menu + 872), n.song, 0)
    n.params = n.alloc(40)
    n.phase = '022 fixture ready'
    print('SOLO_FIXTURE', {'app': hex(n.app), 'menu': hex(n.menu), 'state': hex(n.selection), 'song': hex(n.song), 'diff': hex(n.diff), 'available': n.u.mem_read(n.song + 592, 1)[0], 'mpActive': n.u.mem_read(n.q(n.app + 176) + 8, 1)[0], 'mode': n.i(n.modeSetting), 'specialIndexMap': [hex(n.q(29332968 + i * 8)) for i in range(4)]}, flush=True)
    n.u.hook_add(UC_HOOK_MEM_READ, n.null_read, begin=0, end=4095)
    return n

def entry(n):
    n.phase = '022 ordinary offline startGameScene'
    return n.call(15604092, n.menu, n.song, 0, 0, 0, 40, 0, n.params)
