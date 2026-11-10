# R004 native observation references

Transcribed independently from the published original ARM64 observations at
bc7f3b2f47c93093ec9be2da825ab1018db3e956. These are partial observations,
not fabricated raw emulator output and not reconstruction-generated goldens.
No original ARM64 experiment is rerun by this reconstruction.

- E026: excavations/026_native_hold_reacquisition_and_checkpoint_continuity.md,
  control/repress table and checkpoint/gauge table; research_harness/src/hold.py.
- E037: excavations/037_native_mixed_hold_tap_arbitration_and_contact_continuity.md,
  sections4–8; research_harness/src/mixed_hold_tap.py. A1/A2 have different histories.
- E008 section12 / E009 section10: overdue1750 unmissed2249, missed2250;
  final2501 PURE2/LOST1/score6666668/liveH51.733333587646484/resultH51/category0.
- E001 generator and E010 full initializer: interval/N/end/density propagation.
- E027 chord: original native_chord.aff, two orders, P2/score10000002/H80.4000015258789.

native-cases.json event times are E-relative test stimuli. The adapter primes
Timeline at wall0 and3002, then uses wallE+3002; it never assigns clock fields.
Arrays of record flags are source-order, not generated reference data. Contact IDs
are normalized generation order0/1, pointer42/43 as in the supplied stimuli.
Checkpoint recorder owner is unspecified/-1; activating contacts are a separate
continuous-pass observation. No native completion is claimed for E026/E037;
reconstructed completed sessions are tested separately.
