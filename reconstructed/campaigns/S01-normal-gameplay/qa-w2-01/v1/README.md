# QA-W2-01 v1 — independently specified mixed-profile comparisons

Work1 tests **unchanged production `49e7c263a36aebcc0316e010a629c6bfdf205f6d`**.
These files do not replace the R010-pinned `independent-corpus/`. Frozen case JSON
contains AFF hashes, applicable requirements, evidence, schedules and expected
intermediate fields. The driver is a separately versioned extension of Work1's
previous adapter/comparator, explicitly selecting S01Mixed. Production outputs
are observations, never an expectation-generation input.

Use official SDK10.0.402/runtime10.0.13 and NETStandard.Library.Ref2.1.0, as described
in the preserved W1-01-C01 report. Godot is unnecessary for this CLI suite.
Set PATH/DOTNET_ROOT to the installation and DOTNET_PROCESSOR_COUNT=1. From repo root:

```bash
python reconstructed/campaigns/S01-normal-gameplay/qa-w2-01/v1/run.py \
  --production-root . --output /tmp/qa-w2-01-receipt.json \
  --raw-output /tmp/qa-w2-01-full-runtime.json
```

The runner verifies every tracked core/bridge file against the exact production
commit, rejects extra compile sources and fixture checksum drift, builds Release,
executes actual core/bridge sessions and records the first differing event/field.
Receipt projections include **only asserted fields**; an exposed but unasserted
snapshot is not independently verified. Complete transient snapshots are available
at --raw-output and are not published as original evidence. JSON arrays enforce
length/order; health and geometry-stage outputs enforce signed IEEE754 bits;
only native decimal cache-distance transcriptions use explicit 0.00005 tolerance.
Audio is an inspectable fake backend, sky inputs already projected internal
coordinates. No graphics, audible output or physical-device equivalence follows.

`results/receipt.json`:37/37 cases,16,760 scalar assertions;33 runnable and4
engineering compatibility rejection cases, each checking the intended guard message. `results/historical-independent.json`
records46 unchanged Work1 cases against the new source with default R010 profile.
Its old manifest's ab349d4 identity remains historical provenance. The old pinned
Python runner is deliberately not used to admit changed source. Four original
producer-blocked cases remain NOT RUN/NOT VERIFIED and are not counted as passes.
`results/historical-commands.json` separately records341 Work2 CLI groups. No
Work2-authored group is added to the independent case count.

`results/comparator-controls.json` records three expected comparator failures
from temporary expectation copies: one geometry bit, crossing fresh/old distance,
and instantaneous reacquisition. Frozen cases/production are unchanged by these
controls. `results/authoring-diagnostics.json` preserves draft errors and their
source-based corrections. See the report for all limitations and evidence grades.

Independent derivations:

- Six curves: E003 evaluator0x180a190; I=sin(u*pi/2),
  O=1-f32(sin((u+1)*pi/2)), native curve-specific Ex/Ey. Use endpoint integers
  X=-255/255,Y=200/400 at declared H500, then f32 local displacement/absoluteY/Z*u.
  u=0,.125,.25,.5,.75,.875,1. Z=-8089 from the independent178/4/120 scale chain.
  Multiply negative Z by **floating** zero to preserve -0. Native evidence is
  isolated with a host sine hook, not Android-libm bit-equivalence.
- Full mixed38 count:11 enabled ground taps+4 hold units+9 sine-arc units+
  6 crossing units+7 linked units+1 trace child.12 ground objects retain the
  disabled tap. Six stored linked records account for seven calls. End24120 is
  latest enabled ground24000+120, later than long-note bounds. Five groups.
- Full perfect schedule: independent component eligibility ledger (checkpoint
  minus half interval, clamped to successor admission) and discrete hit times.
  Per-unit gain=f32(f32(219/2.5)/38); H starts0 and adds/clamps **once per unit**;
  all-PURE score=floor(10000000*pure/38)+shining. Source JSON contains every
  intermediate expected count/score/health, including pause and final result.
  Fixed analytic trajectories supply inputs; no target is read from production.
- Shared negative: N8 ordinary gain=f32(f32(204/2.5)/8). FAR first adds half gain,
  four PURE add full gain, then three LOST subtract2 individually. E003 recorded
  release gate blocks arc reacquisition; the retained hold latch reacquires.
  Expected final PURE4/FAR1/LOST3, score5625004; health bits are in the case.

The 38-unit whole session and cross-mechanic extensions are RECONSTRUCTED
INTEGRATION. They were never executed as one chart by original ARM64 research.
E028 native two-contact rows, E025 child guard and E038 natural pair retain their
original integrated evidence; expiry beyond original stop points is explicitly
instruction-backed. Compatibility guards are ENGINEERING, not native rejection.
S01 OPEN. No subsequent execution is authorized by this suite.
