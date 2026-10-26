"""Optional original-native scenario test; requires the external archive, never canned output."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

@unittest.skipUnless(os.environ.get('ARCONIST_ARC_TAP_TEST_ARCHIVE'), 'Set ARCONIST_ARC_TAP_TEST_ARCHIVE for the native arc-tap test')
class ArcTapTest(unittest.TestCase):
    def test_native_construction_and_consumption(self):
        runner = Path(__file__).resolve().parents[1] / 'run.py'
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / 'arc-tap.json'
            result = subprocess.run([sys.executable, str(runner), '--archive',
                                     os.environ['ARCONIST_ARC_TAP_TEST_ARCHIVE'], '--scenario', 'arc_tap',
                                     '--output', str(output)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            data = json.loads(output.read_text())
            self.assertEqual(data['status'], 'pass')
            self.assertTrue(all(data['identity_checks'].values()))
            self.assertEqual(data['native_objects']['child']['pointer'], data['spatial_checks'][1]['child'])
            self.assertEqual(data['native_objects']['parent'], data['native_objects']['child_parent'])
            self.assertEqual(data['after_hit'], data['after_duplicate'])
            self.assertEqual(data['native_call_counts']['0xc78814'], 1)
