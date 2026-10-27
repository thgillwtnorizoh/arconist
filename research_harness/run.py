#!/usr/bin/env python3
"""One-process native regression. Outputs are external to the package by default."""
import argparse
import contextlib
import io
import json
import sys
import traceback
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / 'src'))
import config

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--archive', required=True, help='External read-only arccopy.zip')
    parser.add_argument('--scenario', choices=['ordinary', 'arc_tap', 'hold', 'chord', 'moving_arc', 'timing_group', 'camera_reset', 'track_fade', 'cpu_note'], default='ordinary')
    parser.add_argument('--output', default='regression-result.json')
    parser.add_argument('--unavailable-song', action='store_true', help='Run native negative eligibility control instead')
    parser.add_argument('--verbose', action='store_true', help='Print adapter diagnostics to stderr')
    args = parser.parse_args()
    result = {'status': 'fail', 'binary_sha256': None, 'native_failures': []}
    try:
        if not __debug__:
            raise ValueError('Python optimization disables native regression assertions; run without -O')
        if args.scenario != 'ordinary' and args.unavailable_song:
            raise ValueError('--unavailable-song is only supported by the ordinary scenario')
        result['binary_sha256'] = config.configure(args.archive, args.scenario)
        # Historical adapter print statements remain optional diagnostics, never JSON evidence.
        with contextlib.redirect_stdout(sys.stderr if args.verbose else io.StringIO()):
            if args.scenario == 'cpu_note':
                from cpu_note import run
                result.update(run())
            elif args.scenario == 'track_fade':
                from track_fade import run
                result.update(run())
            elif args.scenario == 'camera_reset':
                from camera_reset import run
                result.update(run())
            elif args.scenario == 'timing_group':
                from timing_group import run
                result.update(run())
            elif args.scenario == 'moving_arc':
                from moving_arc import run
                result.update(run())
            elif args.scenario == 'chord':
                from chord import run
                result.update(run())
            elif args.scenario == 'hold':
                from hold import run
                result.update(run())
            elif args.scenario == 'arc_tap':
                from arc_tap import run
                result.update(run())
            else:
                from regression import run
                result.update(run(args.unavailable_song))
    except Exception as exc:
        result['status'] = 'fail'
        result['native_failures'] = [{'type': type(exc).__name__, 'message': str(exc), 'location': traceback.extract_tb(exc.__traceback__)[-1].name if exc.__traceback__ else None}]
        if args.verbose:
            traceback.print_exc()
    output = Path(args.output).expanduser().resolve()
    try:
        if output == Path(args.archive).expanduser().resolve():
            raise ValueError('Output must not overwrite the external archive')
        if output.is_relative_to(Path(__file__).resolve().parent):
            raise ValueError('Choose an output path outside research_harness')
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(result, indent=2) + '\n')
    except Exception as exc:
        print(f'Cannot write report: {exc}', file=sys.stderr)
        return 2
    print(f"{result['status'].upper()}: {output}")
    return 0 if result['status'] == 'pass' else 1

if __name__ == '__main__':
    sys.exit(main())
