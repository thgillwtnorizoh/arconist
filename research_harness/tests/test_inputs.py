"""Fast CLI validation tests. No native binary or original assets are embedded."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import zipfile

RUNNER = Path(__file__).resolve().parents[1] / 'run.py'

class InputTests(unittest.TestCase):
    def invoke(self, archive, output, *flags):
        return subprocess.run([sys.executable, str(RUNNER), '--archive', str(archive),
                               '--output', str(output), *flags], capture_output=True, text=True)

    def test_missing_archive(self):
        with tempfile.TemporaryDirectory() as directory:
            p = Path(directory)
            run = self.invoke(p / 'missing.zip', p / 'result.json')
            self.assertEqual(run.returncode, 1)
            data = json.loads((p / 'result.json').read_text())
            self.assertEqual(data['status'], 'fail')
            self.assertIn('Archive not found', data['native_failures'][0]['message'])

    def test_wrong_binary_hash(self):
        with tempfile.TemporaryDirectory() as directory:
            p = Path(directory)
            with zipfile.ZipFile(p / 'wrong.zip', 'w') as archive:
                archive.writestr('lib/arm64-v8a/libcocos2dcpp.so', b'not-the-original-library')
            run = self.invoke(p / 'wrong.zip', p / 'result.json')
            self.assertEqual(run.returncode, 1)
            data = json.loads((p / 'result.json').read_text())
            self.assertIn('SHA-256 mismatch', data['native_failures'][0]['message'])

    @unittest.skipUnless(os.environ.get('ARCONIST_TEST_ARCHIVE'), 'Set ARCONIST_TEST_ARCHIVE for native negative test')
    def test_unavailable_song(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / 'result.json'
            run = self.invoke(os.environ['ARCONIST_TEST_ARCHIVE'], output, '--unavailable-song')
            self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
            data = json.loads(output.read_text())
            self.assertEqual(data['test'], 'unavailable_song_rejected')
            self.assertFalse(data['game_scene_constructed'])
