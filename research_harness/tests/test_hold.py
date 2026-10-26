"""Opt-in native hold comparison; each case creates its own original-library runtime."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


@unittest.skipUnless(os.environ.get('ARCONIST_HOLD_TEST_ARCHIVE'), 'Set ARCONIST_HOLD_TEST_ARCHIVE for native hold comparison')
class HoldTest(unittest.TestCase):
    def test_release_reacquisition_and_checkpoints(self):
        runner = Path(__file__).resolve().parents[1] / 'run.py'
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / 'hold.json'
            result = subprocess.run([sys.executable, str(runner), '--archive',
                                     os.environ['ARCONIST_HOLD_TEST_ARCHIVE'], '--scenario', 'hold',
                                     '--output', str(output)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr + output.read_text())
            data = json.loads(output.read_text())
            self.assertEqual(data['status'], 'pass')
            self.assertTrue(data['fresh_emulator_per_case'])
            self.assertTrue(all(data['checks'].values()))
            a, b = data['control'], data['release_reacquisition']
            self.assertEqual(a['final'], b['final'])
            self.assertEqual(b['final']['score'], 10000003)
            self.assertEqual(b['native_call_counts']['0x1730290'], 3)
            self.assertEqual([r['time'] for r in b['native_resolution_writes']], [1250, 1500, 1750])
            contacts = [r['mapping_after'][0] for r in b['inputs'] if r['down']]
            self.assertNotEqual(contacts[0]['touch'], contacts[1]['touch'])
            self.assertNotEqual(contacts[0]['generated_id'], contacts[1]['generated_id'])
            self.assertEqual([r['android_id'] for r in contacts], [42, 43])
