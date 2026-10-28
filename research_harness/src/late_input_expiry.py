"""035: observe two original JNI/Director interleavings without prescribing outcomes."""
import collections
import hashlib
import math
import struct
import traceback
from unicorn import UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm64_const import UC_ARM64_REG_PC, UC_ARM64_REG_SP
import config
from solo_entry import setup, entry
from lifecycle import activate, frame
from boundaries import PC_SKIPS

OBSERVE = {0xee197c, 0xee29a8, 0xee29e8, 0xe4e4dc, 0xe2ea48,
           0x1870de0, 0xdf4a58, 0xb01d6c, 0x173b358, 0x1862a14,
           0x18640d8, 0x18640dc, 0x11ea120, 0x1576aa4, 0xbdbb70,
           0x1793f8c, 0x18be2f8, 0x10a7550, 0xf8056c,
           0xbe31a8, 0xdda71c, 0x194ff80, 0xeec024, 0xeec080,
           0x13073c4, 0xeec1cc, 0xeec4e0, 0xf6b514, 0xeec4f0,
           0x160ce28, 0x160ce58, 0x160ce6c, 0x160cec0, 0x160ce74, 0xeec56c, 0xeec570,
           0x965e28, 0x1730290, 0x868e54, 0xf9a50c, 0xf80a58,
           0xc27d34, 0x1600bb0}


def run_case(frame_first, evidence):
    evidence.update(status='running', gates={'native_scene_chart':'incomplete',
        'shared_precondition':'not_run','arbitration':'not_run','cleanup':'not_run'})
    n = setup(True)
    n.prepare_runtime()
    n.call(0x1930604)
    n.call(0x1054f24)
    n.observe |= OBSERVE
    counts = collections.Counter()
    products, candidates, classifiers, recorders, writes, snapshots, calls = [], [], [], [], [], [], []
    evidence.update(construction=products, candidates=candidates, classifiers=classifiers,
                    recorders=recorders, native_writes=writes, snapshots=snapshots,
                    decisive_calls=calls, native_call_counts=counts)
    targets = {}
    pending_classifier = []
    returns, installed_returns = {}, set()

    def effective():
        t = n.q(n.model + 0x30)
        return n.i(t + 0x20) - n.i(t + 0x28)

    def score_state():
        s, g = targets['score'], targets['gauge']
        return {'score': n.i(s+0x14), 'combo': n.i(s+0x1c), 'shining': n.i(s+0x20),
                'PURE': n.i(s+0x24), 'FAR': n.i(s+0x28), 'LOST': n.i(s+0x2c),
                'health': n.f(g+0x10)}

    def notes_state():
        active = n.items(n.model, 0xa0)
        return {str(t): {'pointer': hex(p), 'time': n.i(p+0x18),
                        'end_time': n.i(p+0x1c), 'lane': n.i(n.q(p+0x20)+0x10),
                        'input_enabled': n.u.mem_read(p+0x54,1)[0],
                        'missed': n.u.mem_read(p+0xc,1)[0],
                        'consumed': n.u.mem_read(p+0xd,1)[0],
                        'accepted_id': n.i(p+0x10), 'active': p in active,
                        'depth': n.i(p+0x30)} for t,p in targets['notes'].items()}

    def mapping():
        rows = []
        def walk(p):
            if not p: return
            walk(n.q(p))
            slot = n.i(p+0x28); touch = n.q(0x1beef90+slot*8)
            rows.append({'android_id': struct.unpack('<q', n.u.mem_read(p+0x20,8))[0],
                         'slot': slot, 'touch_slot': n.i(touch+0xc), 'touch': hex(touch),
                         'generated_id': n.i(touch+0x34)})
            walk(n.q(p+8))
        walk(n.q(0x1bf1a90))
        return rows

    def snapshot(label):
        r = {'label': label, 'wall': n.now, 'E': effective(), 'last_model_E': n.i(29332456),
             'director_frame': n.i(n.director+0x134), 'scene_stamp': n.i(n.scene+0x4d0),
             'notes': notes_state(), 'score': score_state(), 'mapping': mapping(),
             'retained': [hex(p) for p in n.items(n.model,0xd0)], 'mask': n.i(0x1bfebd4),
             'finished': n.u.mem_read(n.model+0x139,1)[0],
             'result_cache': hex(n.q(targets['score']+0x68))}
        snapshots.append(r)
        return r

    def returned(u, pc, size, unused):
        if returns.get(pc):
            row = returns[pc].pop()
            row.update(after=score_state(), note_after=notes_state()[str(row['note_time'])],
                       return_observed=True)

    def observe(u, pc, size, unused):
        counts[hex(pc)] += 1
        if pc == 0x18640d8:
            source = n.x(27)
            products.append({'parsed': hex(source), 'parsed_type': n.typename(source),
                'parsed_time': n.i(source+0x18), 'raw_lane': n.i(n.q(source+0x20)+8),
                'note': hex(n.x(0)), 'time_argument': n.x(1), 'position': hex(n.x(2)),
                'initializer_elf_va': hex(n.x(8))})
        elif pc == 0x18640dc:
            products[-1].update(return_value=n.x(0), returned_note=hex(n.x(25)),
                runtime_type=n.typename(n.x(25)), vtable_elf_va=hex(n.q(n.x(25))))
        if not targets: return
        if pc in {0xbe31a8,0xdda71c,0x194ff80,0xeec024,0xeec080,0xf8056c,0x10a7550}:
            calls.append({'pc_elf_va':hex(pc),'lr_elf_va':hex(n.x(30)), 'phase':n.phase,
                          'wall':n.now,'E':effective(),'director_frame':n.i(n.director+0x134)})
        if pc in {0xeec4e0,0xeec4f0}:
            candidates.append({'stage':'before_sort' if pc==0xeec4e0 else 'after_sort',
                'phase':n.phase,'E':effective(),'pointers':[hex(p) for p in n.items(n.x(19),0xb8)],
                'times':[n.i(p+0x18) for p in n.items(n.x(19),0xb8)]})
        elif pc == 0x160ce28:
            row={'note':hex(n.x(1)), 'note_time':n.i(n.x(1)+0x18), 'generated_id':n.x(2),
                 'E':effective(),'phase':n.phase,'lr_elf_va':hex(n.x(30))}
            classifiers.append(row); pending_classifier.append(row)
        elif pc == 0x160cec0:
            pending_classifier[-1].update(native_abs_error=n.x(9)&0xffffffff, native_E=n.x(4)&0xffffffff)
        elif pc == 0x160ce58:
            pending_classifier[-1]['missed_guard_return']=n.x(0)&0xffffffff
        elif pc == 0x160ce6c:
            pending_classifier[-1]['consumed_guard_return']=n.x(0)&0xffffffff
        elif pc == 0x160ce74:
            row=pending_classifier.pop()
            row.update(consumes=n.x(23)&1, note_after=notes_state()[str(row['note_time'])])
        elif pc == 0xeec56c:
            classifiers[-1]['caller_branch_w0']=n.x(0)&0xffffffff
        elif pc == 0xeec570:
            evidence.setdefault('iteration_stops',[]).append({'pc_elf_va':hex(pc),
                'note':hex(n.x(25)),'E':effective(),'phase':n.phase})
        elif pc in {0x1730290,0x868e54} and n.x(1) in targets['notes'].values():
            row={'kind':'accepted' if pc==0x1730290 else 'miss', 'pc_elf_va':hex(pc),
                 'lr_elf_va':hex(n.x(30)), 'note':hex(n.x(1)), 'note_time':n.i(n.x(1)+0x18),
                 'E':effective(), 'native_time_argument':n.x(4) if pc==0x1730290 else n.x(2),
                 'judgment_id':n.x(2) if pc==0x1730290 else None,
                 'generated_id':n.x(5) if pc==0x1730290 else None,
                 'phase':n.phase,'before':score_state(),'note_before':notes_state()[str(n.i(n.x(1)+0x18))]}
            recorders.append(row)
            ret=n.x(30); returns.setdefault(ret,[]).append(row)
            if ret not in installed_returns:
                n.u.hook_add(UC_HOOK_CODE,returned,begin=ret,end=ret);installed_returns.add(ret)
        elif pc == 0xf80a58 and n.x(26) in targets['notes'].values():
            calls.append({'pc_elf_va':hex(pc),'phase':n.phase,'note':hex(n.x(26)),
                          'native_E':n.x(2)&0xffffffff,'native_cutoff':n.x(8)&0xffffffff})
        elif pc == 0x13073c4:
            sp=u.reg_read(UC_ARM64_REG_SP)
            evidence.setdefault('unprojected',[]).append([n.f(sp+0x28+4*i) for i in range(3)])
        elif pc == 0xeec1cc:
            evidence.setdefault('selected_lanes',[]).append({'primary':n.x(0)&0xffffffff,'secondary':n.x(0)>>32})

    for pc in OBSERVE:n.u.hook_add(UC_HOOK_CODE,observe,begin=pc,end=pc)
    n.trace=[];n.visual=[];n.animationTrace=[];n.downstream=[]
    n.env=n.alloc(8);n.now=1000
    entry(n);activate(n)
    model,scene=n.model,n.scene;chart=n.q(model+0x28);score=n.q(model+0x38)
    taps=[p for p in n.items(chart,0x20) if n.typename(p)=='12LogicTapNote']
    by_time={n.i(p+0x18):p for p in taps}
    assert len(taps)==len(products)==2 and set(by_time)=={1000,1109}
    targets.update(notes=by_time,score=score,gauge=n.items(score,0xa0)[0])
    assert n.sceneInitReturn==1 and n.q(scene+0x3e0)==model and n.q(scene+0x3e8)==chart
    assert n.q(n.director+0x140)==scene and n.q(n.director+0x148)==0
    listener=n.state(model)['listener']
    assert listener['registered']==listener['enabled']==1 and listener['paused']==0
    assert n.i(chart+0xb8)==2
    for row in products:
        p=int(row['note'],16)
        assert row['return_value']==1 and row['returned_note']==row['note']
        assert row['parsed_type']=='10SimpleNote' and row['runtime_type']=='12LogicTapNote'
        assert row['parsed_time']==row['time_argument']==n.i(p+0x18)==n.i(p+0x1c)
        assert row['raw_lane']==3 and n.i(n.q(p+0x20)+0x10)==row['raw_lane']+1
    maps=n.maps(model)
    index={str(t):[[k for k,ps in g.items() if p in ps] for g in maps] for t,p in by_time.items()}
    assert all(any(v) for v in index.values())
    evidence['gates']['native_scene_chart']='pass'
    rig=n.q(model+0x20);camera=n.q(rig+0x2a8)
    evidence.update(objects={'scene':hex(scene),'model':hex(model),'chart':hex(chart),
        'timeline':hex(n.q(model+0x30)),'score':hex(score),'gauge':hex(targets['gauge']),
        'rig':hex(rig),'camera':hex(camera)},listener=listener,
        chart={'N':n.i(chart+0xb8),'end':n.i(chart+0xbc),'index_by_time':index,
               'md5':n.string(chart+0xf8).decode(),
               'timings':[[{'pointer':hex(p),'start':n.i(p+0x10),'end':n.i(p+0x14),
                            'scaled_bpm':n.f(p+0x18),'bpm':n.f(p+0x20),'scale':n.f(p+0x28)} for p in n.items(g)] for g in n.items(chart,0x38)]})
    assert evidence['chart']['md5']==hashlib.md5(config.fixture_text().encode()).hexdigest()
    def written(u, access, where, size, value, unused):
        note=next((p for p in taps if p+0xc<=where<=p+0x13),None)
        writes.append({'object':'note' if note else 'score_or_health','note':hex(note) if note else None,
            'address':hex(where),'offset':hex(where-note) if note else None,'size':size,
            'before':int.from_bytes(u.mem_read(where,size),'little'),'value':value,
            'pc_elf_va':hex(u.reg_read(UC_ARM64_REG_PC)),'phase':n.phase})
    for p in taps:n.u.hook_add(UC_HOOK_MEM_WRITE,written,begin=p+0xc,end=p+0x13)
    n.u.hook_add(UC_HOOK_MEM_WRITE,written,begin=score+0x14,end=score+0x2f)
    n.u.hook_add(UC_HOOK_MEM_WRITE,written,begin=targets['gauge']+0x10,end=targets['gauge']+0x13)
    frame(n,n.now+1,'035 preroll')
    anchor=frame(n,n.now+3001,'035 native music anchor');assert anchor['E']==0
    preframe=frame(n,n.now+1000-effective(),'035 shared E1000')
    assert preframe['E']==preframe['lastModelE']==1000
    pre=snapshot('shared_precondition')
    assert all(v['active'] and v['input_enabled']==1 and v['missed']==v['consumed']==0 for v in pre['notes'].values())
    assert all(pre['score'][k]==0 for k in ['score','combo','shining','PURE','FAR','LOST'])
    assert pre['mapping']==pre['retained']==[] and pre['mask']==pre['finished']==0
    assert int(pre['result_cache'],16)==0
    evidence['gates']['shared_precondition']='pass'
    lane=next(iter(pre['notes'].values()))['lane'];world=[425.*(lane-3.5),0.,0.]
    point,out=n.alloc(12),n.alloc(8)
    for i,v in enumerate(world):n.wf(point+4*i,v)
    n.call(0xbdbb70,camera,point,regs={8:out})
    xy=[n.f(out),n.f(n.director+0x184)-n.f(out+4)]
    assert all(math.isfinite(x) for x in xy)
    evidence.update(anchor=anchor,pre_frame=preframe,projection={'world':world,'jni_xy':xy,'native_lane':lane})
    n.now+=1110-effective()  # External clock only; the native input/frame updater derives E.
    if frame_first:
        row=frame(n,n.now,'035 comparison_frame');assert row['E']==row['lastModelE']==1110
        assert sum(e['pc']=='0x10a7550' for e in row['lifecycle'])==1
        evidence['comparison_frame']=row;snapshot('after_frame_before_down')
    before_model=counts['0x10a7550']
    n.phase='035 comparison_DOWN';n.call(0xbe31a8,n.env,0,42,987042,fs=(*xy,.5))
    down=snapshot('after_DOWN')
    assert down['E']==1110 and counts['0x10a7550']==before_model
    assert len(down['mapping'])==len(down['retained'])==1 and down['mask'].bit_count()==1
    m=down['mapping'][0]
    assert m['android_id']==42 and m['touch_slot']==m['slot'] and down['retained']==[m['touch']]
    n.phase='035 comparison_UP';n.call(0xdda71c,n.env,0,42,988042,fs=(*xy,0))
    up=snapshot('after_UP')
    assert up['mapping']==up['retained']==[] and up['mask']==0
    assert n.q(0x1beef90+m['slot']*8)==0 and up['score']==down['score'] and up['notes']==down['notes']
    if not frame_first:
        row=frame(n,n.now,'035 comparison_frame');assert row['E']==row['lastModelE']==1110
        assert sum(e['pc']=='0x10a7550' for e in row['lifecycle'])==1
        evidence['comparison_frame']=row
    final=snapshot('after_both_operations')
    assert not final['finished'] and int(final['result_cache'],16)==0
    assert final['E']==1110 and n.q(n.director+0x140)==scene and n.q(n.director+0x148)==0
    assert evidence['selected_lanes']==[{'primary':lane,'secondary':0}]
    assert all(abs(a-b)<.5 for a,b in zip(evidence['unprojected'][0],world))
    assert classifiers and recorders and candidates and evidence.get('iteration_stops')
    assert all(c['E']==1110 and c.get('consumes')==c.get('caller_branch_w0') for c in classifiers)
    assert all(r.get('return_observed') for r in recorders)
    evidence['gates'].update(arbitration='pass',cleanup='pass')
    # Check recorder-derived changes, without requiring a particular historical outcome.
    assert final['score']['LOST']==sum(r['after']['LOST']-r['before']['LOST'] for r in recorders)
    assert final['score']['PURE']==sum(r['after']['PURE']-r['before']['PURE'] for r in recorders)
    for p in taps:
        assert sum(w['object']=='note' and w['note']==hex(p) and w['offset']=='0xc' and w['before']==0 and w['value']==1 for w in writes)<=1
        assert sum(w['object']=='note' and w['note']==hex(p) and w['offset']=='0xd' and w['before']==0 and w['value']==1 for w in writes)<=1
    forbidden={0xe4e4dc,0xe2ea48,0x1862a14,0x1576aa4,0x10a7550,0xf8056c,0xeec024,
               0xf6b514,0x160ce28,0x965e28,0x1730290,0x868e54,0xf9a50c}
    assert not forbidden.intersection(n.host_calls) and not forbidden.intersection(n.hooks)
    for a in [0xee197c,0xee29a8,0xee29e8,0xe4e4dc,0xe2ea48,0x1870de0,0x173b358,0x1862a14]:assert counts[hex(a)]==1
    assert counts['0xbe31a8']==counts['0xdda71c']==counts['0x194ff80']==1
    eligibility=[e for e in n.soloTrace if e['pc']=='0xee2214'];assert len(eligibility)==1 and int(eligibility[0]['x'][0],16)==1
    ctor=[e for e in n.menuTrace if e['pc']=='0xe4e4dc'];assert len(ctor)==1 and ctor[0]['lr']=='0xee29ec'
    assert n.u.mem_read(n.menu+0x490,1)[0]==1
    evidence.update(status='pass',startup={'eligibility':1,'latch':1,'initializer_return':n.sceneInitReturn,
        'constructor_lr_elf_va':ctor[0]['lr']},final=final,
        native_call_counts={hex(pc):counts[hex(pc)] for pc in OBSERVE},no_direct_host_gameplay_handoff=True)


def run():
    result={'status':'fail','fixture':'native_late_input_expiry.aff',
        'fresh_emulator_per_case':True,'input_first':{'status':'not_run'},'frame_first':{'status':'not_run'},
        'pc_skips_elf_va':PC_SKIPS,'new_boundaries':[], 'native_failures':[],
        'services':'Unchanged ordinary catalog/account/settings/platform/ABI/resources/audio/GPU services; external synthetic AFF, wall clock and JNI inputs',
        'completion_results_sqlite':'not_run; stop at E1110'}
    try:
        run_case(False,result['input_first'])
        run_case(True,result['frame_first'])
        a,b=result['input_first'],result['frame_first']
        pa,pb=a['snapshots'][0],b['snapshots'][0]
        def normalized(p):
            return {'E':p['E'],'last_model_E':p['last_model_E'],'score':p['score'],'finished':p['finished'],
                    'notes':{t:{k:v for k,v in n.items() if k!='pointer'} for t,n in p['notes'].items()},
                    'mapping':p['mapping'],'retained':p['retained'],'mask':p['mask'],
                    'director_frame':p['director_frame'],'scene_stamp':p['scene_stamp']}
        assert normalized(pa)==normalized(pb)
        assert a['projection']==b['projection']
        result.update(status='pass',comparison={'equivalent_native_precondition':True,
            'same_projection':True,'different_outcomes':a['final']['score']!=b['final']['score'],
            'input_first_score':a['final']['score'],'frame_first_score':b['final']['score'],
            'historical_outcome_was_not_required':True})
    except Exception as exc:
        for name in ['input_first','frame_first']:
            if result[name]['status']=='running': result[name]['status']='fail'
        result['native_failures'].append({'type':type(exc).__name__,'message':str(exc),
            'line':traceback.extract_tb(exc.__traceback__)[-1].lineno})
    return result
