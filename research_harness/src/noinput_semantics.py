"""036: native attribute/count/input/expiry/result comparison, without state repair."""
import collections
import hashlib
import math
import struct
import traceback
import config
from unicorn import UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm64_const import UC_ARM64_REG_PC, UC_ARM64_REG_FP, UC_ARM64_REG_SP
from solo_entry import setup, entry
from lifecycle import activate, frame
from boundaries import PC_SKIPS

OBSERVE = {0xee197c,0xee29a8,0xee29e8,0xe4e4dc,0xe2ea48,0x1870de0,
    0x8c847c,0x8c85c0,0x8c89f4,0x8c8a14,0x8c8a18,0x173b358,0x1862a14,
    0x18640d8,0x18640dc,0x18640ec,0x18640f4,0x186560c,0x1865628,0x1865658,0x18655f8,
    0x11ea120,0x11ea188,0x173bf2c,0x173bf3c,0x173c22c,0x173c24c,
    0x1576aa4,0x1576b98,0x10fd1c0,0x10fd8b8,0x1793f8c,0x18be2f8,0x10a7550,
    0xbe31a8,0xdda71c,0x194ff80,0xeec024,0xeec080,0x13073c4,0xeec1cc,
    0xeec304,0xeec4e0,0xeec4f0,0xf6b514,0x160ce28,0x160ce74,
    0x965e28,0x1730290,0x868e54,0xf8056c,0xf80654,0xf80a58,0xf9a50c,
    0x10a7d50,0xc27d34,0x1600bb0,0x1600c4c,0x1600d80,0x1315038,0x131505c,0x12a5574}


def run_case(noinput, evidence):
    evidence.update(status='running',gates={'construction':'incomplete','input':'not_run',
                                         'expiry_completion':'not_run'})
    config.configure(config.archive_path,'noinput_group' if noinput else 'noinput_semantics')
    n=setup(True);n.prepare_runtime();n.call(0x1930604);n.call(0x1054f24)
    n.observe |= OBSERVE
    counts=collections.Counter();target={};taps=set();chart_pointer=None
    products=[];parser=[];writes=[];end_checks=[];count_checks=[];input_checks=[];expiry_checks=[]
    candidates=[];classifiers=[];recorders=[];snapshots=[];index=[];admissions=[];calls=[];lifetimes=[]
    evidence.update(construction=products,parser=parser,native_writes=writes,end_checks=end_checks,
        count_checks=count_checks,input_checks=input_checks,expiry_checks=expiry_checks,
        candidates=candidates,classifiers=classifiers,recorders=recorders,snapshots=snapshots,
        index_producer=index,admissions=admissions,calls=calls,group_lifetime_stores=lifetimes,
        native_call_counts=counts)
    pending=[];returns={};return_hooks=set();active_end=None

    def effective():
        t=n.q(n.model+0x30);return n.i(t+0x20)-n.i(t+0x28)

    def score_state():
        s=target['score'];g=target['gauge']
        return {'N':n.i(s+0xc),'score':n.i(s+0x14),'combo':n.i(s+0x1c),
                'shining':n.i(s+0x20),'PURE':n.i(s+0x24),'FAR':n.i(s+0x28),
                'LOST':n.i(s+0x2c),'health':n.f(g+0x10)}

    def note_state():
        active=n.items(n.model,0xa0)
        return {str(g):{'pointer':hex(p),'time':n.i(p+0x18),'lane':n.i(n.q(p+0x20)+0x10),
            'group':n.i(p+0x50),'input_enabled':n.u.mem_read(p+0x54,1)[0],
            'missed':n.u.mem_read(p+0xc,1)[0],'consumed':n.u.mem_read(p+0xd,1)[0],
            'accepted_id':n.i(p+0x10),'active':p in active,'depth':n.i(p+0x30)}
            for g,p in target['notes'].items()}

    def mapping():
        rows=[]
        def walk(p):
            if not p:return
            walk(n.q(p));slot=n.i(p+0x28);touch=n.q(0x1beef90+slot*8)
            rows.append({'android_id':struct.unpack('<q',n.u.mem_read(p+0x20,8))[0],
                'slot':slot,'touch_slot':n.i(touch+0xc),'touch':hex(touch),
                'generated_id':n.i(touch+0x34)})
            walk(n.q(p+8))
        walk(n.q(0x1bf1a90));return rows

    def snapshot(label):
        row={'label':label,'wall':n.now,'E':effective(),'notes':note_state(),'score':score_state(),
             'mapping':mapping(),'mask':n.i(0x1bfebd4),'retained':[hex(p) for p in n.items(n.model,0xd0)],
             'finished':n.u.mem_read(n.model+0x139,1)[0],
             'cached_result':hex(n.q(target['score']+0x68)),
             'group_descriptors':[{'pointer':hex(p),'bytes_0_3':list(n.u.mem_read(p,4)),
                                   'end':n.i(p+4)} for p in n.items(target['chart'],0x50)]}
        snapshots.append(row);return row

    def written(u,access,where,size,value,unused):
        p=next((p for p in taps if p<=where<p+0x80),None)
        row={'address':hex(where),'note':hex(p) if p else None,'offset':hex(where-p) if p else None,
             'size':size,'before':int.from_bytes(u.mem_read(where,size),'little'),'value':value,
             'pc_elf_va':hex(u.reg_read(UC_ARM64_REG_PC)),'phase':n.phase}
        if chart_pointer and chart_pointer+0xb8<=where<chart_pointer+0xc0:
            row['chart_offset']=hex(where-chart_pointer)
        writes.append(row)

    def returned(u,pc,size,unused):
        if returns.get(pc):
            r=returns[pc].pop();r.update(after=score_state(),returned=True)

    def observe(u,pc,size,unused):
        nonlocal chart_pointer,active_end
        counts[hex(pc)]+=1
        if pc==0x8c85c0:
            fp=u.reg_read(UC_ARM64_REG_FP);lo,hi=n.q(fp-0x40),n.q(fp-0x38)
            parser.append({'pc_elf_va':hex(pc),'attribute_tokens':[n.string(p).decode() for p in range(lo,hi,24)]})
        elif pc==0x8c89f4:
            parser.append({'pc_elf_va':hex(pc),'attribute':n.string(n.x(21)).decode(),
                           'comparison_return_w0':n.x(0)&0xffffffff})
        elif pc==0x8c8a14:
            p=n.x(25);parser.append({'pc_elf_va':hex(pc),'parsed':hex(p),'type':n.typename(p),
                'flag_before':n.u.mem_read(p+0xc,1)[0],'native_store_value':0})
        elif pc==0x8c8a18 and parser and parser[-1]['pc_elf_va']=='0x8c8a14':
            parser[-1]['flag_after']=n.u.mem_read(n.x(25)+0xc,1)[0]
        elif pc==0x173b358:
            chart_pointer=n.x(0)
            u.hook_add(UC_HOOK_MEM_WRITE,written,begin=chart_pointer+0xb8,end=chart_pointer+0xbf)
        elif pc==0x18640d8:
            p=n.x(27);products.append({'parsed':hex(p),'parsed_type':n.typename(p),
                'time':n.i(p+0x18),'parsed_flag':n.u.mem_read(p+0xc,1)[0],
                'raw_lane':n.i(n.q(p+0x20)+8),'note':hex(n.x(0)),
                'position':hex(n.x(2)),'timing_argument':hex(n.x(3)),
                'initializer_elf_va':hex(n.x(8))})
        elif pc==0x18640dc:
            p=n.x(25);taps.add(p);products[-1].update(initializer_return=n.x(0),
                runtime_type=n.typename(p),returned_note=hex(p),vtable_elf_va=hex(n.q(p)))
            u.hook_add(UC_HOOK_MEM_WRITE,written,begin=p+0x50,end=p+0x55)
            u.hook_add(UC_HOOK_MEM_WRITE,written,begin=p+0xc,end=p+0x13)
        elif pc==0x18640f4:
            products[-1]['input_store']={'pc_elf_va':hex(pc),'parsed':hex(n.x(27)),
                'native_w8':n.x(8)&0xff,'note':hex(n.x(25))}
        elif pc==0x186560c and n.x(24) in taps:
            active_end={'note':hex(n.x(24)),'input_enabled':n.x(8)&0xff,
                'pc_elf_va':hex(pc),'end_before':n.i(chart_pointer+0xbc)}
            end_checks.append(active_end)
        elif pc==0x18655f8 and active_end is not None:
            active_end.update(observed_next_loop_elf_va=hex(pc),end_after=n.i(chart_pointer+0xbc));active_end=None
        elif pc==0x1865628 and active_end is not None:
            active_end['native_note_end_w20']=n.x(20)&0xffffffff
        elif pc==0x1865658 and active_end is not None:
            active_end['native_end_candidate_w28']=n.x(28)&0xffffffff
        elif pc==0x11ea120:
            evidence['count_producer']={'chart':hex(n.x(0)),'lo_time':n.x(1),
                'hi_time':n.x(2),'lr_elf_va':hex(n.x(30)),
                'main_objects_before_bars':len(n.items(n.x(0),0x20))}
        elif pc==0x11ea188 and n.x(26) in taps:
            count_checks.append({'note':hex(n.x(26)),'input_enabled':n.x(8)&0xff,
                                 'running_N':n.x(20),'pc_elf_va':hex(pc)})
        elif pc==0x173bf2c:
            evidence['count_producer']['returned_N']=n.x(0)&0xffffffff
        elif pc==0x173bf3c:
            evidence['main_objects_after_bars']=len(n.items(chart_pointer,0x20))
        elif pc in {0x173c22c,0x173c24c}:
            lifetimes.append({'pc_elf_va':hex(pc),'descriptor':hex(n.x(12) if pc==0x173c22c else n.x(8)),
                              'value':n.x(11) if pc==0x173c22c else n.x(9)})
        elif pc==0x1576b98 and n.x(19) in taps:
            index.append({'note':hex(n.x(19)),'group':n.i(n.x(19)+0x50),
                          'lo':n.x(23)&0xffffffff,'hi':n.x(24)&0xffffffff})
        elif pc==0x10fd8b8 and n.x(28) in taps:
            admissions.append({'note':hex(n.x(28)),'native_min_depth':n.x(23)&0xffffffff,
                               'limit':n.x(27),'phase':n.phase})
        if not target:return
        if pc==0xeec304 and n.x(27) in taps:
            input_checks.append({'note':hex(n.x(27)),'group':n.i(n.x(27)+0x50),
                                 'input_enabled':n.x(8)&0xff,'phase':n.phase,'E':effective()})
        elif pc==0xf80654 and n.x(26) in taps:
            expiry_checks.append({'note':hex(n.x(26)),'input_enabled':n.x(8)&0xff,
                                  'phase':n.phase,'E':effective()})
        elif pc in {0xeec4e0,0xeec4f0}:
            candidates.append({'stage':'before_sort' if pc==0xeec4e0 else 'after_sort',
                'phase':n.phase,'E':effective(),'notes':[hex(p) for p in n.items(n.x(19),0xb8)]})
        elif pc==0x160ce28:
            r={'note':hex(n.x(1)),'E':effective(),'phase':n.phase,'contact':n.x(2)}
            classifiers.append(r);pending.append(r)
        elif pc==0x160ce74:pending.pop()['consumes']=n.x(23)&1
        elif pc in {0x1730290,0x868e54} and n.x(1) in taps:
            r={'pc_elf_va':hex(pc),'kind':'accepted' if pc==0x1730290 else 'miss',
               'note':hex(n.x(1)),'E':effective(),'lr_elf_va':hex(n.x(30)),
               'phase':n.phase,'before':score_state()}
            recorders.append(r);ret=n.x(30);returns.setdefault(ret,[]).append(r)
            if ret not in return_hooks:u.hook_add(UC_HOOK_CODE,returned,begin=ret,end=ret);return_hooks.add(ret)
        elif pc==0x13073c4:
            sp=u.reg_read(UC_ARM64_REG_SP)
            evidence.setdefault('unprojections',[]).append({'phase':n.phase,'point':[n.f(sp+0x28+4*i) for i in range(3)]})
        elif pc==0xeec1cc:
            evidence.setdefault('lanes',[]).append({'phase':n.phase,'primary':n.x(0)&0xffffffff,'secondary':n.x(0)>>32})
        elif pc in {0x10a7550,0xf8056c,0x10a7d50,0xc27d34,0x1600bb0}:
            calls.append({'pc_elf_va':hex(pc),'lr_elf_va':hex(n.x(30)),
                          'phase':n.phase,'E':effective(),'x0':hex(n.x(0))})
        elif pc==0x1600c4c:
            evidence['snapshot_reconciliation']={'N':n.i(target['score']+0xc),
                'N_minus_PURE_FAR':n.x(11)&0xffffffff,'recorded_LOST':n.x(13)&0xffffffff,
                'selector_d1':n.x(12)&0xff}
        elif pc==0x1600d80:
            evidence['native_snapshot_product']={'score_state':hex(n.x(19)),'result':hex(n.x(0))}
        elif pc==0x131505c:
            evidence['getter_denominator']=n.x(4)&0xffffffff

    for pc in OBSERVE:n.u.hook_add(UC_HOOK_CODE,observe,begin=pc,end=pc)
    n.trace=[];n.visual=[];n.animationTrace=[];n.downstream=[];n.env=n.alloc(8);n.now=1000
    entry(n);activate(n)
    scene,model=n.scene,n.model;chart=n.q(model+0x28);score=n.q(model+0x38)
    by_group={n.i(p+0x50):p for p in taps}
    target.update(chart=chart,score=score,gauge=n.items(score,0xa0)[0],notes=by_group)
    assert set(by_group)=={0,1} and len(taps)==len(products)==2
    assert n.sceneInitReturn==1 and n.q(scene+0x3e0)==model and n.q(scene+0x3e8)==chart==chart_pointer
    assert set(taps)=={p for p in n.items(chart,0x20) if n.typename(p)=='12LogicTapNote'}
    assert n.q(n.director+0x140)==scene and n.q(n.director+0x148)==0
    listener=n.state(model)['listener'];assert listener['registered']==listener['enabled']==1 and listener['paused']==0
    tls=n.items(chart,0x38);descriptors=n.items(chart,0x50);assert len(tls)==len(descriptors)==2
    for row in products:
        p=int(row['note'],16);g=n.i(p+0x50)
        assert row['initializer_return']==1 and row['returned_note']==row['note']
        assert row['runtime_type']=='12LogicTapNote' and row['parsed_type']=='10SimpleNote'
        assert row['time']==n.i(p+0x18)==n.i(p+0x1c)==1500
        assert n.i(n.q(p+0x20)+0x10)==row['raw_lane']+1
        assert row['parsed_flag']==row['input_store']['native_w8']==n.u.mem_read(p+0x54,1)[0]
        assert n.q(p+0x48)==int(row['timing_argument'],16) in n.items(tls[g])
    assert parser[0]['attribute_tokens']==(['noinput'] if noinput else [])
    assert any(r.get('pc_elf_va')=='0x8c8a14' and r.get('flag_after')==0 for r in parser)==noinput
    maps=n.maps(model)
    membership={str(g):{'header':hex(n.items(model,0x88)[g]),
        'keys':[k for k,ps in maps[g].items() if p in ps]} for g,p in by_group.items()}
    assert len(index)==2 and all(m['keys'] for m in membership.values())
    evidence.update(objects={'scene':hex(scene),'model':hex(model),'chart':hex(chart),
        'timeline':hex(n.q(model+0x30)),'score':hex(score),'gauge':hex(target['gauge']),
        'rig':hex(n.q(model+0x20)),'camera':hex(n.q(n.q(model+0x20)+0x2a8))},
        listener=listener,initializer_return=n.sceneInitReturn,
        chart={'N':n.i(chart+0xb8),'end':n.i(chart+0xbc),'main_objects':len(n.items(chart,0x20)),
               'md5':n.string(chart+0xf8).decode(),'membership':membership,
               'timings':[[{'pointer':hex(p),'start':n.i(p+0x10),'end':n.i(p+0x14),
                    'raw_bpm':n.f(p+0x20),'scale':n.f(p+0x28)} for p in n.items(tl)] for tl in tls]})
    assert n.i(score+0xc)==n.i(chart+0xb8)==evidence['count_producer']['returned_N']
    assert evidence['chart']['md5']==hashlib.md5(config.fixture_text().encode()).hexdigest()
    evidence['gates']['construction']='pass';snapshot('activation')
    frame(n,n.now+1,'036 preroll');anchor=frame(n,n.now+3001,'036 native music anchor');assert anchor['E']==0
    row=frame(n,n.now+1500-effective(),'036 E1500');assert row['E']==row['lastModelE']==1500
    pre=snapshot('before_inputs');assert all(p['active'] and not p['missed'] and not p['consumed'] for p in pre['notes'].values())
    assert all(pre['score'][k]==0 for k in ['PURE','FAR','LOST','score','combo'])
    contacts=[];evidence.update(anchor=anchor,contacts=contacts);camera=n.q(n.q(model+0x20)+0x2a8)
    for g,pid in [(1,42),(0,43)]:
        lane=n.i(n.q(by_group[g]+0x20)+0x10);world=[425.*(lane-3.5),0.,0.]
        point,out=n.alloc(12),n.alloc(8)
        for i,v in enumerate(world):n.wf(point+4*i,v)
        n.call(0xbdbb70,camera,point,regs={8:out});xy=[n.f(out),n.f(n.director+0x184)-n.f(out+4)]
        assert all(math.isfinite(v) for v in xy)
        contact={'group':g,'android_id':pid,'world':world,'jni_xy':xy};contacts.append(contact)
        evidence['gates']['input']='incomplete';before_models=counts['0x10a7550']
        n.phase='036 DOWN group'+str(g);n.call(0xbe31a8,n.env,0,pid,987000+pid,fs=(*xy,.5))
        down=snapshot('after_DOWN_group'+str(g));contact['mapping']=down['mapping']
        assert down['E']==1500 and counts['0x10a7550']==before_models
        assert len(down['mapping'])==len(down['retained'])==1 and down['mask'].bit_count()==1
        m=down['mapping'][0];assert m['android_id']==pid and m['slot']==m['touch_slot']
        assert down['retained']==[m['touch']]
        assert evidence['lanes'][-1]['primary']==lane
        assert all(abs(a-b)<.5 for a,b in zip(evidence['unprojections'][-1]['point'],world))
        n.phase='036 UP group'+str(g);n.call(0xdda71c,n.env,0,pid,988000+pid,fs=(*xy,0))
        up=snapshot('after_UP_group'+str(g));assert up['mapping']==up['retained']==[] and up['mask']==0
        assert n.q(0x1beef90+m['slot']*8)==0 and up['score']==down['score'] and up['notes']==down['notes']
    evidence['gates']['input']='pass';evidence['gates']['expiry_completion']='incomplete'
    end=n.i(chart+0xbc);assert end>=1500
    for E in sorted(set([1501,1600,1601,end,end+1])):
        if n.u.mem_read(model+0x139,1)[0]:break
        r=frame(n,n.now+E-effective(),'036 expiry E'+str(E));assert r['E']==r['lastModelE']==E
        assert sum(e['pc']=='0x10a7550' for e in r['lifecycle'])==1
        snapshot('frame_'+str(E))
    result=n.q(score+0x68);assert n.u.mem_read(model+0x139,1)[0]==1 and result
    assert evidence['native_snapshot_product']=={'score_state':hex(score),'result':hex(result)}
    evidence['native_result']={'pointer':hex(result),'recorded_LOST':n.i(score+0x2c),
        'shining':n.i(result+0x14),'PURE':n.i(result+0x18),'FAR':n.i(result+0x1c),
        'LOST':n.i(result+0x20),'health':n.i(result+0x28),'score_d1':n.u.mem_read(score+0xd1,1)[0]}
    n.phase='036 read-only native result getters'
    evidence['native_result']['score']=n.call(0x1315038,result)
    evidence['native_result']['clear']=n.call(0x12a5574,result)
    evidence['native_result']['getter_scope']='original read-only getters on native completion product; no result factory call'
    final=snapshot('endpoint');assert final['mapping']==final['retained']==[] and final['mask']==0
    assert counts['0xc27d34']==counts['0x1600bb0']==1
    assert sum(r['after']['LOST']-r['before']['LOST'] for r in recorders)==n.i(score+0x2c)
    assert all(r.get('returned') for r in recorders)
    assert counts['0xbe31a8']==counts['0xdda71c']==counts['0x194ff80']==2
    assert len(candidates)==4 and len(input_checks)>=2 and expiry_checks
    forbidden={0xe4e4dc,0xe2ea48,0x173b358,0x1862a14,0x1576aa4,0x10fd1c0,0x10a7550,
               0xeec024,0xf6b514,0x160ce28,0x1730290,0x868e54,0xf8056c,0x1600bb0,0xc27d34}
    assert not forbidden.intersection(n.host_calls) and not forbidden.intersection(n.hooks)
    eligibility=[e for e in n.soloTrace if e['pc']=='0xee2214'];assert len(eligibility)==1 and int(eligibility[0]['x'][0],16)==1
    assert n.u.mem_read(n.menu+0x490,1)[0]==1
    evidence.update(status='pass',native_call_counts={hex(pc):counts[hex(pc)] for pc in OBSERVE},
        final=final,all_gameplay_handoffs_native=True)
    evidence['gates']['expiry_completion']='pass'


def run():
    evidence={'status':'fail','control':{'status':'not_run'},'noinput':{'status':'not_run'},
              'fresh_emulator_per_case':True,'native_failures':[],'pc_skips_elf_va':PC_SKIPS,
              'new_boundaries':[],'results_sqlite':'not_run; stop after native completion snapshot'}
    try:
        run_case(False,evidence['control']);run_case(True,evidence['noinput'])
        a,b=evidence['control'],evidence['noinput']
        evidence.update(status='pass',comparison={'control_N':a['chart']['N'],'noinput_N':b['chart']['N'],
            'control_end':a['chart']['end'],'noinput_end':b['chart']['end'],
            'control_final':a['native_result'],'noinput_final':b['native_result'],
            'group_flags':{k:[r['parsed_flag'] for r in evidence[k]['construction']] for k in ['control','noinput']},
            'input_outcome_was_observed_not_prescribed':True},
            external_services='Unchanged ordinary catalog/account/settings/ABI/platform/resources/audio/GPU; synthetic AFF, wall clock and JNI events',
            end_time_disambiguation={'status':'not_run',
                'reason':'per-note native end-loop flag checks and end-time loads distinguish filtering from an unchanged maximum',
                'scope':'only the primary equal-time pair was executed; no later-note variant is claimed'})
    except Exception as exc:
        for k in ['control','noinput']:
            if evidence[k]['status']=='running':evidence[k]['status']='fail'
        evidence['native_failures'].append({'type':type(exc).__name__,'message':str(exc),
            'line':traceback.extract_tb(exc.__traceback__)[-1].lineno})
    return evidence
