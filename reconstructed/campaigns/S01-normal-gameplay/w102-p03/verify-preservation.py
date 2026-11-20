#!/usr/bin/env python3
"""Verify the staged or published P01 tree; never starts native execution."""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
BASE = '69b2b272cff47211091da767840f16a9d56b943b'
EXECUTED = 'f595c7e4bce057efa02d3d587900045e7680effe'
CAMPAIGN = 'reconstructed/campaigns/S01-normal-gameplay/'
PACK = CAMPAIGN + 'w102-p03/'
APPENDS = {CAMPAIGN + name for name in (
    'coverage-register.md', 'dependency-register.md', 'discrepancy-register.md')}
APPENDS.add('reconstructed/contexts.md')


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--candidate', default='INDEX')
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    candidate = args.candidate
    original_paths = git('ls-tree', '-rz', '--name-only', BASE).decode().split('\0')[:-1]
    target_paths = (git('ls-files', '-z') if candidate == 'INDEX' else
                    git('ls-tree', '-rz', '--name-only', candidate)).decode().split('\0')[:-1]
    target = set(target_paths)
    assert set(original_paths) <= target, 'Deleted historical path'
    prefixes, protected, changed = [], [], []
    read = lambda path: git('show', (':' if candidate == 'INDEX' else candidate + ':') + path)
    for path in original_paths:
        before = git('show', BASE + ':' + path)
        after = read(path)
        if path in APPENDS:
            assert after.startswith(before) and len(after) > len(before), path
            prefixes.append(dict(path=path, prefixBytes=len(before), prefixSha256=digest(before),
                                 bytesAfter=len(after), suffixBytes=len(after) - len(before)))
            changed.append(dict(path=path, status='append-only', sha256=digest(after)))
        else:
            assert before == after, 'Historical/protected source changed: ' + path
            protected.append(path + '\0' + digest(before))
    for path in sorted(target - set(original_paths)):
        assert path.startswith(PACK) or path == CAMPAIGN + 'W102-P03-report.md', path
        # This inventory cannot contain its own final content hash.
        changed.append(dict(path=path, status='added', sha256=None if path == PACK +
                            'preservation.json' else digest(read(path))))
    for name in ('run.py', 'fixtures.json'):
        path = PACK + name
        assert read(path) == git('show', EXECUTED + ':' + path), path
    if candidate != 'INDEX':
        for ancestor in (BASE, EXECUTED, 'e18aa1819f962d0fb3b80ca255fc92cda0f63208',
                         '49e7c263a36aebcc0316e010a629c6bfdf205f6d'):
            subprocess.run(['git', 'merge-base', '--is-ancestor', ancestor, candidate],
                           cwd=ROOT, check=True)
    receipt = dict(status='PASS preservation', baselineSha=BASE, executionSourceSha=EXECUTED,
                   candidate=candidate, originalFileCount=len(original_paths),
                   protectedByteIdentical=len(protected),
                   protectedManifestSha256=digest('\n'.join(sorted(protected)).encode()),
                   appendOnly=prefixes, changedPaths=sorted(changed, key=lambda row: row['path']),
                   changedPathCount=len(changed), deletions=0, productionChanges=0,
                   historicalTestChanges=0, executedDriverChanges=0, nativeScenesCreated=0,
                   selfHashExclusion='preservation.json only; remote readback checks its bytes')
    Path(args.output).write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps({key: value for key, value in receipt.items()
                      if key not in ('changedPaths', 'appendOnly')}))


if __name__ == '__main__':
    main()
