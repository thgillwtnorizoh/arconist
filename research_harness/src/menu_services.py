# Recovered research adapter; consolidated for Expedition 024.
import config
from track_services import *

class MenuNative(TrackNative):

    def __init__(self):
        super().__init__()
        self.menuTrace = []
        self.zeroStringSources = []
        self.originalStringCopy = self.hooks[27712080]
        self.hooks[27712080] = self.checked_string_copy
        self.observe |= {24462400, 22110388, 17650176, 26013584, 22617344, 14487440, 20543372, 26377168, 9842972, 21950616}

    def checked_string_copy(self):
        if self.x(1) == 0:
            self.zeroStringSources.append(hex(self.x(30)))
            raise RuntimeError('null native std::string source at ' + hex(self.x(30)))
        self.originalStringCopy()

    def oncode(self, u, a, size, ud):
        if a not in self.hooks and a not in self.observe and (not 27711856 <= a < 27754496):
            return
        if a == 9842972:
            self.sceneInitReturn = self.x(0)
            print('NATIVE_GAME_SCENE_INIT_RETURN', self.sceneInitReturn, flush=True)
        if hasattr(self, 'menuTrace') and a in self.observe and (a in [24462400, 22110388, 17650176, 22617344, 14487440, 15000796, 14871112, 20543372, 26377168, 10260672, 9842836, 21950616]):
            row = {'pc': hex(a), 'lr': hex(self.x(30)), 'x': [hex(self.x(i)) for i in range(8)], 'phase': self.phase, 'wall': self.now}
            self.menuTrace.append(row)
            print('MENU_EVENT', row, flush=True)
            if a == 15000796:
                self.scene = self.x(0)
                sp = u.reg_read(UC_ARM64_REG_SP)
                row['stack'] = [self.q(sp + i * 8) for i in range(6)]
        super().oncode(u, a, size, ud)

    def call(self, a, *args, **kw):
        try:
            return super().call(a, *args, **kw)
        except RuntimeError as e:
            if not str(e).startswith('did not return'):
                raise
            stop = kw.get('stop', 67109120)
            for chunk in range(8):
                pc = self.u.reg_read(UC_ARM64_REG_PC)
                print('021_BUDGET', chunk, hex(pc), flush=True)
                self.u.emu_start(pc, stop, count=5000000)
                if self.u.reg_read(UC_ARM64_REG_PC) == stop:
                    return self.x(0)
            raise
