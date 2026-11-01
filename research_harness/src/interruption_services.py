"""041: bounded012 AppDelegate/audio interfaces; native-owned UI is untouched."""
import struct


class InterruptionServices:
    def __init__(self,n,evidence):
        self.n=n;self.e=evidence
        scene=n.scene;ui=n.q(scene+0x3c0);root=n.q(ui+0x300)
        assert n.typename(ui)=='7UILayer' and n.typename(root)=='10PauseLayer'
        assert n.q(root+0x2e0)==scene+0x2f0
        assert n.q(scene+0x2f0)==0x1ae7470
        raw=bytes(n.u.mem_read(0x4100000,n.heap-0x4100000))
        needle=struct.pack('<Q',0x1b7d700);start=0;found=[]
        while True:
            i=raw.find(needle,start)
            if i<0:break
            p=0x4100000+i
            if p%8==0 and n.q(p+8)==root:found.append(p)
            start=i+1
        assert len(found)==1,'Original PauseLayer resume capture not uniquely present'
        self.callback=found[0];self.pause=root
        assert n.q(0x1b7d700+0x30)==0x1632d78
        delegate=n.alloc(0x100);n.wq(delegate,0x1a9a2d0)
        n.wq(0x1be4b90,delegate);n.hooks.pop(0xd7654c,None)
        n.hooks[0xfc3450]=n.service  # documented Android animation-interval service
        n.hooks.pop(0xb9e0d0,None)  # native-owned modal listeners require original dismissal
        audio=n.q(n.app+0x10);provider=n.alloc(0x100);vt=n.alloc(0x100)
        n.wq(provider,vt);n.wq(audio+0x2c0,provider)
        # Original10884ac -> ae2138 reads header+30. Empty external audio-query
        # state returns false natively and avoids an unrelated loop fade path.
        query=n.alloc(0x40);n.wq(audio+0x1a8,query)
        calls=[]
        evidence.update(app_delegate=hex(delegate),app_delegate_vtable_elf_va=hex(n.q(delegate)),
            background_virtual_elf_va=hex(n.q(n.q(delegate)+0x18)),
            foreground_virtual_elf_va=hex(n.q(n.q(delegate)+0x20)),
            native_ui=hex(ui),native_pause_layer=hex(root),
            original_resume_capture=hex(self.callback),capture_vtable_elf_va=hex(n.q(self.callback)),
            native_secondary_delegate=hex(n.q(root+0x2e0)),audio_manager=hex(audio),
            external_audio_provider=hex(provider),empty_audio_query_header=hex(query),
            provider_calls=calls,unmodified_native_ready=n.i(0x1bf9040),ui_rejection_flag_41b=n.u.mem_read(ui+0x41b,1)[0],
            scene_finished_49a=n.u.mem_read(scene+0x49a,1)[0],
            pause_active_before_background=n.u.mem_read(root+0x2d8,1)[0],ui_layout_and_callback='Native GameScene products; no host UI/capture/active writes',
            supplied='012-style AppDelegate singleton facade/original vtable, Android interval service, original UI hide retained, provider pause/seek/update/predicate; no native-ready flag assigned')
        for off in [0x30,0x40,0xb0,0xc8]:
            address=0x4005000+off
            assert address not in n.hooks
            n.wq(vt+off,address)
            def called(off=off):
                calls.append({'virtual':hex(off),'phase':n.phase,'wall':n.now,
                    'provider':hex(n.x(0)),'x1':n.x(1),'x2':n.x(2),
                    'lr_elf_va':hex(n.x(30)),'return_value':1 if off==0xc8 else 0})
                n.ret(1 if off==0xc8 else 0)
            n.hooks[address]=called
        self.event=n.alloc(4);n.wi(self.event,2)  # external Widget event enum

    def resume(self):
        n=self.n
        assert n.q(self.callback+8)==self.pause
        assert n.u.mem_read(self.pause+0x2d8,1)[0]==1
        n.call(n.q(n.q(self.callback)+0x30),self.callback,0,self.event)
