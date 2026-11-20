#!/usr/bin/env python3
"""Read-only ELF validation of the postmortem. No emulator or native calls."""
import argparse
import hashlib
import io
import json
import zipfile
from pathlib import Path

from capstone import Cs, CS_ARCH_ARM64, CS_MODE_LITTLE_ENDIAN
from elftools.elf.elffile import ELFFile


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--archive', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    here = Path(__file__).resolve().parent
    source = json.loads((here / 'mode-normalization-source.json').read_text())
    with zipfile.ZipFile(args.archive) as archive:
        raw = archive.read('lib/arm64-v8a/libcocos2dcpp.so')
    assert hashlib.sha256(raw).hexdigest() == source['librarySha256']
    elf = ELFFile(io.BytesIO(raw))
    build_id = next(note['n_desc'] for section in elf.iter_sections()
                    if section['sh_type'] == 'SHT_NOTE'
                    for note in section.iter_notes()
                    if note['n_type'] == 'NT_GNU_BUILD_ID')
    assert build_id == '17d660edbf37ca78beefc32e07672c97419ddce6'
    decoder = Cs(CS_ARCH_ARM64, CS_MODE_LITTLE_ENDIAN)
    rows = []
    for anchor in source['anchors']:
        va = int(anchor['va'], 16)
        segment = next(s for s in elf.iter_segments()
                       if s['p_type'] == 'PT_LOAD'
                       and s['p_vaddr'] <= va
                       and va + 4 <= s['p_vaddr'] + s['p_filesz'])
        offset = segment['p_offset'] + va - segment['p_vaddr']
        instruction_bytes = raw[offset:offset + 4]
        assert instruction_bytes.hex() == anchor['bytes']
        instruction = next(decoder.disasm(instruction_bytes, va))
        decoded = instruction.mnemonic + ' ' + instruction.op_str
        assert decoded == anchor['decoded']
        rows.append(dict(va=anchor['va'], bytes=instruction_bytes.hex(), decoded=decoded))
    receipt = dict(status='PASS static ELF validation only',
                   checks=2 + 2 * len(rows), failures=0, skips=0,
                   nativeFreshScenes=0, librarySha256=source['librarySha256'],
                   buildId=build_id, anchors=rows)
    Path(args.output).write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps(receipt))


if __name__ == '__main__':
    main()
