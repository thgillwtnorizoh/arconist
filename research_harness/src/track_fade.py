"""Bounded native trackdisplay eligibility diagnostic. Failed gates never become callback tests."""
import collections
import hashlib
import traceback
import config
from unicorn import UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm64_const import UC_ARM64_REG_PC
from solo_entry import setup, entry
from lifecycle import activate
from boundaries import PC_SKIPS

OBSERVE = {0x1930604,0x1870de0,0x7f2628,0x1090060,0x173b358,0x1862a14,
           0x1792e18,0x1576aa4,0xa3937c,0x16a3a6c,0xf8056c,0xf80824,
           0x1514c64,0x10846c0,0x81565c,0x1501dfc,0xef18e8,0x18ebfa4,
           0x13d3f44,0xd630b8,0x9effe0}


def run():
    result={'status':'fail','fixture':'native_track_fade.aff',
            'replacement_fixture':'native_track_fade_replace.aff (unexecuted candidate)',
            'gates':{'single_fade':'incomplete','replacement':'not_run'},
            'native_failures':[],'pc_skips_elf_va':PC_SKIPS}
    try:
        return investigate(result)
    except Exception as exc:
        result['native_failures'].append({'type':type(exc).__name__,'message':str(exc),
                                         'line':traceback.extract_tb(exc.__traceback__)[-1].lineno})
        return result


def investigate(result):
    config.configure(config.archive_path,'track_fade')
    n=setup(True)
    n.prepare_runtime()
    n.observe |= OBSERVE
    parsed,decisions,property_writes,owner_writes,owner_init,feature_copy=[],[],[],[],[],[]
    scheduling,track_registrations,track_unschedules=[],[],[]
    result.update(parsed_scene_controls=parsed,native_builder_decisions=decisions,
                  native_chart_property_writes=property_writes,native_owner_writes=owner_writes,
                  native_owner_initialization=owner_init,native_feature_copy=feature_copy,
                  native_scheduling=scheduling,track_registrations=track_registrations,
                  track_unschedules=track_unschedules)
    chart_pointer=None
    owner_pointer=None
    pending=None

    def written(u,access,where,size,value,data):
        data.append({'address':hex(where),'size':size,'value':value,
                     'pc_elf_va':hex(u.reg_read(UC_ARM64_REG_PC)),'phase':n.phase})

    def observe(u,a,size,data):
        nonlocal chart_pointer,owner_pointer,pending
        if a==0x173b358:
            chart_pointer=n.x(0)
            u.hook_add(UC_HOOK_MEM_WRITE,written,property_writes,begin=chart_pointer+0x110,end=chart_pointer+0x110)
        elif a==0x1864128:
            p=n.x(0)
            parsed.append({'pointer':hex(p),'type':n.typename(p),'vtable_elf_va':hex(n.q(p)),
                           'time':n.i(p+0x18),'kind_identifier':n.string(p+0x20).decode(),
                           'float_value':n.f(p+0x38),'integer_value':n.i(p+0x3c)})
        elif a==0x1864134:
            pending={'parsed':hex(n.x(27)),'chart':hex(n.x(8)) if n.x(8)>0xff else hex(chart_pointer),
                     'property_byte':n.x(8)&0xff,'pc_elf_va':hex(a),'classifications':[]}
        elif a in (0x18645f4,0x18648f8,0x18649fc) and pending is not None:
            pending['classifications'].append({'pc_elf_va':hex(a),'kind':n.x(0)&0xffffffff,
                                              'compared_with':{0x18645f4:4,0x18648f8:5,0x18649fc:6}[a]})
        elif a==0x186558c and pending is not None:
            pending.update(keep_result=n.x(19)&0xffffffff,rejection_branch_elf_va=hex(a))
        elif a==0x1863d60 and pending is not None:
            pending['observed_next_elf_va']=hex(a)
            decisions.append(pending)
            pending=None
        elif a==0xe2f5cc:
            owner_pointer=n.x(21)
            u.hook_add(UC_HOOK_MEM_WRITE,written,owner_writes,begin=owner_pointer+0x2c8,end=owner_pointer+0x2cf)
        elif a==0xa3937c:
            owner_init.append({'owner':hex(n.x(0)),'model':hex(n.x(1)),'rig':hex(n.x(2)),
                               'visual_wrapper':hex(n.x(3)),'track_collection':hex(n.x(4)),
                               'chart':hex(n.x(5)),'lr_elf_va':hex(n.x(30))})
        elif a==0xe2f618:
            feature_copy.append({'owner':hex(n.x(21)),'value':n.x(9)&0xff,
                                 'pc_elf_va':hex(a),'chart':hex(chart_pointer)})
        elif a in (0x13d3f44,0xd630b8,0x9effe0):
            scheduling.append({'pc_elf_va':hex(a),'dt_f32':n.s(0),'phase':n.phase,'wall':n.now,
                               'lr_elf_va':hex(n.x(30))})
        elif a==0x81565c and owner_pointer is not None and n.x(0)==owner_pointer:
            track_registrations.append({'owner':hex(n.x(0)),'key':n.string(n.x(3)).decode(),
                                        'interval':n.s(0),'repeat':n.x(2),'delay':n.s(1)})
        elif a==0x10846c0 and owner_pointer is not None and n.x(0)==owner_pointer:
            track_unschedules.append({'owner':hex(n.x(0)),'key':n.string(n.x(1)).decode()})
    for a in [0x173b358,0x1864128,0x1864134,0x18645f4,0x18648f8,0x18649fc,0x186558c,0x1863d60,
              0xe2f5cc,0xa3937c,0xe2f618,0x13d3f44,0xd630b8,0x9effe0,0x81565c,0x10846c0]:
        n.u.hook_add(UC_HOOK_CODE,observe,begin=a,end=a)
    n.phase='031 complete original static initializer'
    n.call(0x1930604)
    n.call(0x1054f24)
    n.trace=[];n.visual=[];n.animationTrace=[];n.downstream=[]
    n.env=n.alloc(8);n.now=1000
    entry(n)
    activate(n)  # Let original initialization establish the owner/feature producer; no fade driver.
    scene,model=n.scene,n.model
    chart=n.q(model+0x28);owner=n.q(scene+0x300)
    collection=n.q(owner+0x2b8)
    result['objects']={'scene':hex(scene),'model':hex(model),'chart':hex(chart),'owner':hex(owner),
                       'owner_type':n.typename(owner),'visual_wrapper':hex(n.q(owner+0x2b0)),
                       'track_collection':hex(collection),'track_collection_type':n.typename(collection),
                       'scheduler':hex(n.scheduler),'manager':hex(n.manager)}
    assert chart==chart_pointer and owner==owner_pointer
    assert n.sceneInitReturn==1 and n.q(scene+0x3e0)==model and n.q(scene+0x3e8)==chart
    assert n.q(n.director+0x140)==scene and n.q(n.director+0x148)==0
    assert n.typename(owner)=='29GameSceneVisualControlHandler'
    assert len(parsed)==len(decisions)==1
    assert parsed[0]['kind_identifier']=='trackdisplay' and parsed[0]['time']==600
    assert parsed[0]['float_value']==2.0 and parsed[0]['integer_value']==0
    assert decisions[0]['property_byte']==decisions[0]['keep_result']==0
    assert [c['kind'] for c in decisions[0]['classifications']]==[0,0,0]
    assert [c['compared_with'] for c in decisions[0]['classifications']]==[4,5,6]
    assert decisions[0]['observed_next_elf_va']=='0x1863d60'
    controls=[p for p in n.items(chart,0x20) if n.typename(p)=='17LogicSceneControl']
    assert not controls,'Construction outcome changed; reassess this blocked diagnostic'
    assert any(w['pc_elf_va']=='0x173c3cc' and w['value']==0 for w in property_writes)
    assert [w['pc_elf_va'] for w in owner_writes]==['0xe2f5cc','0xe2f5d4','0xe2f618']
    assert [w['value'] for w in owner_writes]==[0,255,0]
    assert len(feature_copy)==1 and feature_copy[0]['value']==0
    assert n.u.mem_read(owner+0x2c8,1)[0]==0 and n.i(owner+0x2cc)==255
    assert len(owner_init)==1
    init=owner_init[0]
    assert int(init['owner'],16)==owner and int(init['model'],16)==n.q(owner+0x2a0)==model
    assert int(init['chart'],16)==n.q(owner+0x2c0)==chart and int(init['track_collection'],16)==collection
    assert int(init['visual_wrapper'],16)==n.q(owner+0x2b0) and int(init['rig'],16)==n.q(owner+0x2a8)
    nodes=n.items(collection,0x300)
    result['native_track_collection']={'pointer':hex(collection),'vector_begin':hex(n.q(collection+0x300)),
        'vector_end':hex(n.q(collection+0x308)),
        'nodes':[{'pointer':hex(p),'type':n.typename(p),'opacity_setter_elf_va':hex(n.q(n.q(p)+0x470)),
                  'real_opacity_byte':n.u.mem_read(p+0x1d1,1)[0],
                  'displayed_opacity_byte':n.u.mem_read(p+0x1d0,1)[0]} for p in nodes]}
    taps=[p for p in n.items(chart,0x20) if n.typename(p)=='12LogicTapNote']
    assert len(taps)==1 and n.i(chart+0xb8)==1 and n.i(chart+0xbc)==1620
    tap=taps[0]
    assert n.i(tap+0x18)==1500 and n.i(n.q(tap+0x20)+0x10)==4
    assert any(tap in ps for group in n.maps(model) for ps in group.values())
    listener=n.state(model)['listener']
    assert listener['registered']==listener['enabled']==1 and listener['paused']==0
    assert not track_registrations and not track_unschedules and not n.timers()
    digest=n.string(chart+0xf8).decode()
    assert digest==hashlib.md5(config.fixture_text().encode()).hexdigest()
    counts=collections.Counter(e['pc'] for e in n.events)
    for a in [0xee197c,0xee29a8,0xee29e8,0xe2ea48,0x1870de0,0x173b358,0x1862a14,0xa3937c,0x7f2628]:
        assert counts[hex(a)]==1,(hex(a),counts[hex(a)])
    for a in [0x1792e18,0xf80824,0x1514c64,0x1501dfc,0xef18e8]:
        assert counts[hex(a)]==0,(hex(a),counts[hex(a)])
    assert counts['0x13d3f44']==counts['0xd630b8']==counts['0x9effe0']>0
    assert n.u.mem_read(n.menu+0x490,1)[0]==1
    assert any(e['pc']=='0xee2214' and int(e['x'][0],16)==1 for e in n.soloTrace)
    forbidden={0xe2ea48,0x1862a14,0x1792e18,0x1514c64,0x81565c,0x1501dfc,0xef18e8,0x10846c0,0x10a7550}
    assert not forbidden.intersection(n.host_calls) and not forbidden.intersection(n.hooks)
    result.update(initializer_return=n.sceneInitReturn,listener=listener,native_chart_N=n.i(chart+0xb8),
        chart_end=n.i(chart+0xbc),whole_chart_md5=digest,runtime_scene_controls=[],
        native_initial_feature=0,native_initial_owner_opacity=n.i(owner+0x2cc),
        timer_snapshot=n.timers(),native_call_counts={hex(a):counts[hex(a)] for a in OBSERVE|{0xee197c,0xee29a8,0xee29e8,0xe2ea48}},
        native_tap={'pointer':hex(tap),'time':n.i(tap+0x18),'lane':n.i(n.q(tap+0x20)+0x10)},
        gates={'single_fade':'blocked_at_original_runtime_construction','replacement':'not_run'},
        blocker={'branch_elf_va':'0x186558c','observed_edge':'0x186558c -> 0x1863d60',
                 'cause':'Native chart+0x110=0; kind0 fails fallback kinds4/5/6 and Song exceptions; parsed trackdisplay omitted',
                 'second_native_guard':'Original e2f618 copies chart+0x110 via16a3a6c to owner+0x2c8=0; handler1514cec would require nonzero',
                 'minimum_remedy':'Genuinely scene-control-permitted original chart/catalog context; no property, digest or owner-feature repair'},
        scientific_checks={'original_parsing_and_runtime_omission_observed':True,'native_feature_provenance':True,
                           'original_scene_and_Scheduler_execute':True,'no_feature_callback_timer_or_node_repair':True},
        native_failures=[{'type':'NativeTrackDisplayConstructionExcluded','message':'Original builder omits kind0 control; no first timer/callback/propagation; replacement not executed'}],
        supplied_services='Unchanged024-030 ABI/platform/catalog/profile/settings/resource/clock/graphics/audio services; synthetic AFF; original1930604; no new service/skip',
        endpoint={'running_scene':hex(n.q(n.director+0x140)),'pending':n.q(n.director+0x148),
                  'dispatcher_enabled':n.u.mem_read(n.dispatcher+0x124,1)[0],
                  'first_fade_callback':'not_executed','replacement':'not_run','node_propagation':'not_executed'})
    return result  # Eligibility characterization passes; requested fade regression still fails.
