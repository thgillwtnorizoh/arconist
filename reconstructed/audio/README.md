# Clockwork Steps — original R005 music

Original synthetic instrumental composed and synthesized for this reconstruction,
dedicated to the public domain under [CC0-1.0](LICENSE-CC0.txt). No imported melody,
sample, commercial asset, original Android song or external audio library is used.
Explicit pitch/chord/melody score and integer oscillator/percussion synthesis live
in compose.py; Python standard library only.

32seconds,120BPM,mono22050Hz PCM16,705600frames. Four count-in beats precede the
first chart note at2s. Melody/bass/chords/percussion follow a half-second beat grid.
Final quarter-second fades; the game stops at results. manifest.json is the
published expected asset identity, not generated test output.

```text
python reconstructed/audio/compose.py --output reconstructed/godot/content/audio/clockwork_steps.wav.bytes --report reconstructed/out/waveform.json
```

Build also copies manifest.json beside the ignored generated carrier. Finished
PCK bundles audio; no runtime composing/download required. Exact WAV SHA256:
`612793dc6723570841eac96457bdd8d8c659461fcb0d177fd22e93b7cd19961c`.
PCM SHA256:`89f45c583387720f9d599db432426f854b38a29da9cc67e6beea80c44423dbb1`.
Peak24000,RMS3293.095426129316; all64 beat windows have first50ms RMS>300.
Offline signal checks do not establish anyone heard the track.

The .wav.bytes suffix preserves raw WAV through export. The adapter validates the
narrow PCM format before LoadFromBuffer. First preflight found a real packaging
failure: an imported .wav raw path returned0 bytes from PCK. Carrier repairs it
without changing PCM/clock. The actual-PCK probe checks exact hash,32s decoder,
non-looping state and AudioStreamPlayer Play/Stop under headless Dummy output.
Its initial scene-tree setup error was repaired by deferring until the root enters
the tree. Failed diagnostics are retained in technical evidence.

Godot output is an engineering substitution for FMOD, without hardware calibration,
playhead feedback, drift correction or SFX. Audible output and perceived timing
require owner qualification on Windows.
