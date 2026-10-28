"""030-R input/provenance diagnostic: no Designant entitlement is invented."""
import collections
import hashlib
import json
import re
import traceback
import zipfile
from pathlib import Path

import config
from boundaries import PC_SKIPS
from lifecycle import activate, frame
from solo_entry import setup, entry
from unicorn import UC_HOOK_CODE


def digest(data):
    return hashlib.sha256(data).hexdigest()


def inspect_materials(directory):
    root = Path(directory).expanduser().resolve()
    if not root.is_dir():
        raise ValueError('Designant materials directory not found')
    charts = []
    for difficulty in range(4):
        path = root / f'{difficulty}.aff'
        if not path.is_file():
            raise ValueError(f'Missing external Designant material: {path.name}')
        data = path.read_bytes()
        text = data.decode('utf-8')
        if not text.startswith('AudioOffset:0\n-\n'):
            raise ValueError(f'Unexpected AFF header in {path.name}; do not rewrite original bytes')
        # Lexical inventory only. This is not the original AFF parser or a grammar validator.
        cameras = re.findall(r'camera\(([^;]*)\);', text)
        charts.append({'filename': path.name, 'bytes': len(data), 'sha256': digest(data),
                       'format': 'UTF-8 AFF text', 'native_parser_executed': False,
                       'camera_fields_lexical': [s.split(',') for s in cameras],
                       'commands_lexical': sorted(set(re.findall(r'\b([a-z]+)\(', text))),
                       'line_count': len(text.splitlines())})
    audio = root / 'base.ogg'
    if not audio.is_file():
        raise ValueError('Missing external Designant material: base.ogg')
    data = audio.read_bytes()
    if not data.startswith(b'OggS') or b'\x01vorbis' not in data[:100]:
        raise ValueError('base.ogg is not the inspected Ogg/Vorbis format')
    with zipfile.ZipFile(config.archive_path) as archive:
        catalog_bytes = archive.read('assets/songs/songlist')
        matches = [s for s in json.loads(catalog_bytes)['songs'] if s['id'] == 'designant']
        if len(matches) != 1:
            raise ValueError('Original archive must contain exactly one Designant catalog record')
        song = matches[0]
        paths = [p for p in archive.namelist() if 'designant' in p.lower()]
        packs = json.loads(archive.read('assets/songs/packlist'))['packs'] if 'assets/songs/packlist' in archive.namelist() else []
        pack_matches = [p for p in packs if p['id'] == song['set']]
    if song['set'] != 'lephon' or song['purchase'] != 'lephon' or song['bpm_base'] != 200:
        raise ValueError('Unexpected original Designant catalog contract')
    fields = ['id', 'idx', 'set', 'purchase', 'bpm_base', 'side', 'remote_dl',
              'world_unlock', 'byd_local_unlock', 'version']
    return {'charts': charts,
            'audio': {'filename': audio.name, 'bytes': len(data), 'sha256': digest(data),
                      'format': 'Ogg/Vorbis', 'native_audio_loading': 'not_run'},
            'catalog_source': 'original archive assets/songs/songlist',
            'catalog_sha256': digest(catalog_bytes),
            'catalog_fields': {k: song[k] for k in fields},
            'difficulty_flags': [{k: d[k] for k in ['ratingClass', 'hidden_until', 'hidden_until_unlocked']}
                                 for d in song['difficulties']],
            'archive_designant_paths': paths,
            'archived_packlist': {'present': bool(packs),
                                  'matching_pack_ids': [p['id'] for p in pack_matches],
                                  'meaning': 'descriptive catalog; not ownership or an asserted prerequisite'},
            'compatibility': 'matching song metadata and text format; native chart compatibility not_run',
            'account_purchase_or_unlock_records_supplied': False,
            'packlist_requested_or_required': False}


def ordinary_control(evidence):
    """Observe the unchanged base-song boundary; never relabel it as Designant."""
    n = setup(True)
    n.prepare_runtime()
    points = {0x17c45f4, 0x193baa8, 0x17c4628, 0x10a1b04, 0x18c898c,
              0x10a1c8c, 0x10a1cb8, 0xee2214, 0xee25bc, 0xee29a8,
              0xee29e8, 0xe4e4dc, 0xe2ea48, 0x96311c, 0x10a7550}
    observations = []
    evidence['ordinary_control'] = {'status': 'incomplete', 'native_observations': observations}

    def observe(u, pc, size, data):
        row = {'pc_elf_va': hex(pc), 'lr_elf_va': hex(n.x(30)),
               'x0': hex(n.x(0)), 'phase': n.phase}
        if pc == 0x10a1c8c:
            row['song_purchase_pointer_return'] = hex(n.x(0))
        observations.append(row)

    for pc in points:
        n.u.hook_add(UC_HOOK_CODE, observe, begin=pc, end=pc)
    n.phase = '030R unchanged ordinary static initialization'
    n.call(0x1930604)
    n.call(0x1054f24)
    n.trace = []; n.visual = []; n.animationTrace = []; n.downstream = []
    n.env = n.alloc(8); n.now = 1000
    entry(n)
    activate(n)
    scene, model = n.scene, n.model
    chart = n.q(model + 0x28)
    assert n.sceneInitReturn == 1
    assert n.q(scene + 0x3e0) == model and n.q(scene + 0x3e8) == chart
    assert n.q(n.director + 0x140) == scene and n.q(n.director + 0x148) == 0
    assert n.string(n.song) == b'sayonarahatsukoi'
    assert n.string(n.song + 0x198) == b'base' and n.q(n.song + 0x190) == 0
    assert n.u.mem_read(n.menu + 0x490, 1)[0] == 1
    assert any(r['pc_elf_va'] == '0xee2214' and r['x0'] == '0x1' for r in observations)
    assert sum(r['pc_elf_va'] == '0x10a1c8c' and r['x0'] == '0x0' for r in observations) == 2
    frame(n, n.now + 1, '030R unchanged ordinary visitation control')
    listener = n.state(model)['listener']
    assert listener['registered'] == listener['enabled'] == 1 and listener['paused'] == 0
    assert any(r['pc_elf_va'] == '0x10a7550' for r in observations)
    assert n.q(n.localState + 0x288) == 0
    assert n.q(n.localState + 0x298) == 0
    assert not n.items(n.account, 0x18)
    forbidden = {0xe4e4dc, 0xe2ea48, 0x10a7550, 0x192b5c8, 0x1651e88, 0xb0bd74,
                 0x10a1b04, 0x17c45f4, 0x965e28, 0x1730290}
    assert not forbidden.intersection(n.host_calls) and not forbidden.intersection(n.hooks)
    # Instruction-backed evidence from the verified mapped ELF, not an executed target rejection.
    instruction_pcs = [0x18c898c, 0x10a1c88, 0x10a1c8c, 0x10a1c94, 0x10a1c98,
                       0x10a1c9c, 0x10a1ca0, 0x10a1cb8, 0x10a1ccc,
                       0x17c46a0, 0x17c46a4, 0x17c46f8, 0x17c470c, 0x17c4714,
                       0xf2bee0, 0xf2bee4, 0x169eb70, 0x169eb74, 0x17c478c,
                       0x17c4794, 0x1863e54, 0x1863e58, 0x186453c]
    evidence['instruction_backed_contract'] = {
        'classification': 'Instruction-backed but unexecuted for Designant',
        'instruction_words_le': {hex(pc): bytes(n.u.mem_read(pc, 4)).hex() for pc in instruction_pcs},
        'purchase_reference': '0x18c898c loads Song+0x190; catalog text is not that object',
        'local_ownership': '0x10a1c9c reads local+0x288; zero takes 0x10a1ca0 -> 0x10a1ccc (false)',
        'other_routes': '17c46f8+ optional purchase flags/ownership/unlock checks; full Designant outcome unexecuted',
        'camera_builder': 'chart+0x110 or exact designant exception; not executed for supplied charts'}
    counts = collections.Counter(r['pc_elf_va'] for r in observations)
    evidence['ordinary_control'].update(status='pass', song_id='sayonarahatsukoi', difficulty=0,
        scene=hex(scene), model=hex(model), chart=hex(chart), native_initializer_return=n.sceneInitReturn,
        selected_song_purchase_pointer=0, native_call_counts=dict(counts), listener=listener,
        running_scene=hex(n.q(n.director+0x140)), pending_scene=n.q(n.director+0x148),
        dispatcher_enabled=n.u.mem_read(n.dispatcher+0x124,1)[0],
        source_state={'classification': 'External supplied input; bounded harness storage, not a real account',
                      'local_purchase_count_288': n.q(n.localState+0x288),
                      'local_song_hash_bucket_count_298': n.q(n.localState+0x298),
                      'owned_account_characters': len(n.items(n.account,0x18)),
                      'designant_purchase_object': 'not_produced',
                      'designant_unlock_state': 'unknown; not supplied'})


def run(materials_directory):
    evidence = {'status': 'fail', 'research_designation': '030-R',
                'gates': {'A_designant_selection': 'incomplete', 'B_runtime_camera': 'not_run',
                          'C_overlap': 'not_run', 'D_reset': 'not_run', 'E_JNI_projection': 'not_run'},
                'pc_skips_elf_va': PC_SKIPS, 'native_failures': [],
                'designant_native_selection_attempted': False,
                'designant_scene': None, 'designant_chart': None, 'native_chart_digest': None,
                'designant_chart_property': None, 'target_builder_decision': None,
                'new_gameplay_skips': [], 'host_gauge_camera_or_entitlement_repairs': False}
    try:
        if not materials_directory:
            raise ValueError('--designant-materials is required for camera_designant')
        evidence['materials'] = inspect_materials(materials_directory)
        ordinary_control(evidence)
        evidence['gates']['A_designant_selection'] = 'blocked_before_native_selection'
        evidence['blocker'] = {
            'type': 'NativeDesignantSelectionProvenanceUnavailable',
            'first_missing_interface': 'coherent purchased-Song descriptor and justified local ownership/unlock input',
            'native_contract_elf_va': '0x18c898c / 0x10a1b04 / 0x17c45f4',
            'conditional_failure_edge': '0x10a1ca0 -> 0x10a1ccc when local+0x288 == 0',
            'classification': 'bounded observed source state plus original instructions; NOT an executed Designant rejection',
            'minimum_remedy': 'recover original purchase-object/catalog mapping and genuine ownership/unlock producer data or an evidence-backed non-entitlement route; no fabricated account record',
            'packlist_requirement': 'not established; no missing-packlist diagnosis',
            'original_chart_native_compatibility': 'not_run after Gate A stop'}
        evidence['native_failures'].append({'type': evidence['blocker']['type'],
                                           'message': 'Original materials supply content/catalog, not the missing selection/ownership producer; later gates not run'})
        evidence['services'] = 'Unchanged ordinary catalog/account/profile/settings/platform/ABI/resources/audio/GPU/clock services; external materials inspected read-only, not installed into a fabricated Designant Song'
        evidence['scope'] = 'No Designant object/eligibility result, camera event/action/reset or JNI judgment is manufactured'
    except Exception as exc:
        evidence['native_failures'].append({'type': type(exc).__name__, 'message': str(exc),
                                           'line': traceback.extract_tb(exc.__traceback__)[-1].lineno})
    return evidence
