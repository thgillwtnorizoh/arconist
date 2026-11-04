# Reconstruction history (append-only)

## R001 preparation — 2026-11-05

Headquarters authorized independent ordinary-tap reconstruction with mandatory
gates A-G. Fresh isolated clone at 0c174c6e481158ae73e4d7c18afabaa670794d2d;
branch reconstruction/r001. Existing research is read-only for this mission.
Read RTK standing instructions, project README and inspected cumulative context,
backlog, native harness README, actual ordinary/late-input fixtures and source,
and relevant reports 002/005/006/008/009/010/024/035/042. The separately referenced
project introduction and original ZIP are not present in this checkout/workspace;
README/context preserve the introduction's research remit. The R001 instruction
supplies reconstruction authority. No fresh original-native execution is claimed.

Reference strategy: manually normalize published native observations and existing
native assertions with exact report/source paths and source commit. Expected
outputs are not computed by the reconstruction. Float32 health is compared by
bits, not decimal tolerance. IDs use chart ordinal/time/lane, never heap addresses.

Engineering boundary: headless events supply monotonic wall milliseconds and
already-resolved internal lanes; Android/JNI/camera projection is an adapter boundary.
Implement ordinary steady startup and separate input refresh versus frame range/
expiry updates. Positive ordinary default-group timing only. Unsupported syntax
fails explicitly. Equal-time candidate ties use source ordinal for determinism;
native tie stability is unverified and outside native compatibility claims.

## R001 development validation and repair — 2026-11-05

Initial restricted .NET build attempts returned exit1 before compilation (Windows
workload initialization/permissions); an authorized normal-permission build passed
with zero warnings/errors. Initial suite:35/36 passed, no skips; comparator negative
test failed with `A value of type 'System.Int32' cannot be converted to a
'System.Double'.` Fixed numeric comparison to parse invariant JSON numbers across
both DOM-backed and CLR-backed JsonValues; no assertion or expectation weakened.
Full suite then36/36; all three CLI native-reference comparisons exited0.

Trace audit found older-note E1110 depth889 versus035's published890. Current
depth must add the current float depth to the already-truncated precomputed native
depth (010 preprocessing), rather than add two untruncated float values. Corrected
that operation order and strengthened035 golden checkpoints with the published
E1000 depths0/-881 and E1110 depths890/8. The prior goldens did not assert depth;
this discrepancy and repair are preserved, not hidden by a relaxed comparison.

## R001 verified delivery — 2026-11-05

Final stricter validation:build0/zero warnings/errors;36/36 tests,zero failures,
zero skips; ordinary/input-first/frame-first CLI0 with9/6/6 computed events and
passing normalized native comparisons. Each replay test adds100 byte-identical
repetitions. CLI negative controls return1 for an intermediate combo mismatch
(`$.trace[3].combo: expected 99, actual 1`) and unsupported hold syntax; failure
output is preserved in ignored out/. No expected comparison was weakened.

Committed implementation09634fea52aec46c91b25e56640c55b4abc42fb6 was cloned into
an empty clean source copy and rebuilt/rerun:36/36,zero skipped,three real CLI
comparisons pass. All three clean JSON traces match final development output bytes.
Curated commands/environment/output hashes and initial failures are preserved in
validation/R001.md; raw traces/build outputs are excluded from publication.

Published reconstruction/r001 with ordinary non-force push. GitHub immutable
compare/readback and remote ref verify implementation09634f,main remains required
parent0c174c6.25 added paths; all118 preexisting Git blobs verified unchanged.
Final audit commit only updates validation/R001.md and appends this history.

R001 engineering gates A-G PASS. Minimum independent AFF/timestamped tap executable
is achieved; Headquarters audit/acceptance remains pending. Verified ordinary
boundary:024 full two-tap gameplay/result and035 controlled interleavings with
exact health bits/depth samples, guards,candidates and cleanup. No fresh native,
physical-device, Godot, Unity, audio or visual claim. Missing original ZIP and
standalone project introduction remain explicitly recorded; published native
reports/harness assertions are the oracle authority. R001 stops here; no R002,
additional expedition or production-engine work is initiated.
