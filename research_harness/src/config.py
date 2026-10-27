"""Read-only external input; no application binary/resource is redistributed."""
import hashlib
import io
import zipfile
from pathlib import Path

BINARY_MEMBER = 'lib/arm64-v8a/libcocos2dcpp.so'
EXPECTED_SHA256 = '3eaca4e6dabb3395f276f8915698d57675757d0df0970e716b23a3dc201c79be'
archive_path = None
_binary = None
_fixture_name = 'ordinary_two_tap.aff'

def configure(path, scenario='ordinary'):
    global archive_path, _binary, _fixture_name
    _fixture_name = {'ordinary': 'ordinary_two_tap.aff', 'continuous_gauge': 'ordinary_two_tap.aff', 'arc_tap': 'native_arc_tap.aff',
                     'flick_producer': 'native_flick_probe.aff', 'cpu_note': 'native_cpu_note.aff', 'hold': 'native_hold.aff', 'chord': 'native_chord.aff',
                     'moving_arc': 'native_moving_arc.aff', 'crossing_arc': 'native_crossing_arcs.aff',
                     'timing_group': 'native_timing_group.aff', 'reverse_scroll': 'native_reverse_scroll.aff',
                     'camera_reset': 'native_camera_overlap.aff', 'camera_reset_variant': 'native_camera_reset.aff',
                     'track_fade': 'native_track_fade.aff', 'track_fade_replace': 'native_track_fade_replace.aff'}[scenario]
    archive_path = Path(path).expanduser().resolve()
    if not archive_path.is_file():
        raise ValueError(f'Archive not found: {archive_path}')
    try:
        with zipfile.ZipFile(archive_path) as archive:
            data = archive.read(BINARY_MEMBER)
    except (zipfile.BadZipFile, KeyError) as exc:
        raise ValueError(f'Archive must contain {BINARY_MEMBER}: {exc}') from exc
    actual = hashlib.sha256(data).hexdigest()
    if actual != EXPECTED_SHA256:
        raise ValueError(f'ARM64 binary SHA-256 mismatch: expected {EXPECTED_SHA256}, got {actual}')
    _binary = data
    return actual

def elf_stream():
    if _binary is None:
        raise RuntimeError('Configure and verify archive before native execution')
    return io.BytesIO(_binary)

def fixture_text():
    return (Path(__file__).resolve().parents[1] / 'fixtures' / _fixture_name).read_text()
