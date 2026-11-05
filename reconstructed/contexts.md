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

## R002 authorization and implementation — 2026-11-05

Headquarters accepted R001 and authorized the first actual Windows Godot tap
prototype, directly from a295ec3c129c4fd8cea3e454c4165e2ef2d2249e on new branch
reconstruction/r002. Read Instruction.md and this full history before proceeding.
No merge to main, new native expedition, R003 or Unity authorization is inferred.

Used installed Godot4.7.2.stable.mono.official.ed1daf0bf, .NET SDK10.0.402/runtime
10.0.13, Windows x64. New Godot project references an engine-neutral session/input
bridge and the unchanged .NET Standard2.1 core via ProjectReference. Renderer/HUD
read core E/notes/state/result. One Godot monotonic tick source serves _Input and
_Process independently, with the core's ordinary3-second preroll; no input-triggered
Frame is inserted. Physical/logical D/F/J/K map to lanes2..5; mouse uses pointer100.
Focus loss releases contacts while time continues. These are frontend adapters,
not claims of original Android transport, native rendering or audio synchronization.

Implemented16-note original synthetic practice, selectable byte-identical two-tap
reference, start/results/replay, judgments/counters/health and core-time-driven
approaching shapes. New15-test bridge suite covers mapping/OS fallback/035 order,
cleanup/results/restart and related core behavior. All36 R001 tests and three
reference comparisons pass unchanged; no skip or reference rewrite.

Preserved failures: C# namespace ambiguities and nullable annotation compile errors;
first exporter returned0 but logged missing-solution ERROR and was treated as failed;
added genuine Godot solution. Controlled input initially exposed non-letter physical
code4194313 with valid logical letter code; fixed logical fallback and added exact
regression (including correcting Godot Unicode's long type). No core boundary,
test assertion or golden was weakened. Preliminary logs remain in ignored out/.

Actual graphical source run completes two-tap with PURE2/FAR0/LOST0/shining1,
score10000001,H80/category3. Separate exported Windows process completes practice
with PURE15/FAR1/LOST0/shining9,score9687509,max16,H80/category2. Restart resets all
state; wrong K atE2022 records no judgment, then all16 unique notes expire once,
ending PURE0/FAR0/LOST16,score0,H0/category0. Both export results occur atE24622;
all17 DOWN/UP pairs clean contacts to0. F8 saves actual viewport images; JSONL
contains7955 frame/input/state records across these final export runs.

This is controlled Windows SendInput testing using the computer-use skill, received
as genuine Godot InputEventKey callbacks, not internal synthetic judgments or a
claim of human/owner hands-on acceptance. The successful/missed/restart evidence is
from complete actual graphical sessions. Binary package includes the self-contained
.NET runtime and is launched without the editor; publication/readback and final
artifact verification are recorded in the R002 delivery addendum.

## R002 delivery verified — 2026-11-05

Implementation c6b869e0aca0d0a3127ec8f2c3e57d95e0d3fd1a published directly from
accepted R001 head on reconstruction/r002. Complete reproduction wrapper exits0:
36/36 R001,15/15 bridge,zero skips,three reference comparisons pass,Godot .NET
build/import/Windows export all successful. Both ZIP integrity checks and every
extracted Windows-package file hash pass. The extracted ZIP executable separately
starts, loads16 practice notes and renders actual gameplay, without the editor.
All tested graphical processes close normally with exit0.

Release https://github.com/thgillwtnorizoh/arconist/releases/tag/reconstruction-r002
targets implementation c6b869e. Windows ZIP75487796bytes, SHA-256
8f642712efc2c3d1ff90a7ed067ace28e7a278a7618892d43e8b2fc9ca6aa531;
evidence ZIP413744bytes, SHA-256
40290bdc95b9c42340c494dc21b136991f3e43fff5448ce6e996a89013cd8bfe.
GitHub API asset sizes/digests independently match these local tested artifacts.
No binary export or raw generated trace is committed; release evidence contains
actual viewport images, event logs and audit summary. Final audit commit changes
only this append-only history and validation/R002.md, not the tested playable code.

143 R001 baseline blobs audited:142 unchanged exactly; contexts.md retains its
entire prior byte prefix.19 changed paths:18 additions and the history append.
Remote main and reconstruction/r001 remain unchanged; no force push or main merge.
R002 mandatory A-H PASS at engineering delivery. Headquarters acceptance and the
owner's later hands-on testing remain separate. Stop here without R003/Unity or
another original-native expedition.

## R003 partial reconstruction — 2026-11-05

Headquarters authorized native-informed 3D track/spatial-input mission from exact
accepted R002 head fe9d460d40951edc3e1bd933d00b413a7522db28, branch
reconstruction/r003. Read Instruction.md, full existing reconstruction history,
Godot README, R001/R002 validation and relevant004/007/008/009/029/032/039/040
research before implementation. Original research and portable gameplay behavior
remain unchanged; no original-native expedition or Unity work was initiated.

Added real Node3D/Camera3D/BoxMesh track and note presentation under Godot, while
retaining shared core and bridge authority. Native axes uniformly divide by425;
ordinary integer centers -638/-213/212/637 and Y4 are preserved. Current depth
reads the existing timing integrator with integer-predepth/float-add/truncation.
Ground Y0 and judgment Z0 remain explicit. Single camera, FOV65, placeholder mesh
style, immediate resolve hiding, four-lane clipping and safe ray rejection are
engineering boundaries, not native GPU/camera calibration or physical touch claims.

Actual final individual tests pass36/36 R001,three independent native comparisons,
15/15 unchanged bridge and30/30 R003 actual Godot Camera3D groups,zero skips.
All ten E032 depth samples and E0350/-881,890/8 match. Initial resize evidence was
rejected because Godot refused direct viewport sizing; repaired test resizes its
container and asserts actual size. Final resize/projection run has no warnings.

Initial online NuGet advisory lookup failed; optional process-local offline restore
allows cached-package builds without relaxing compiler/test checks. Installed-editor
APPDATA/assembly startup failure was worked around with a complete local editor
copy/portable data and writable APPDATA. Actual source starts using OpenGL3.3 on
RTX3050/596.21 and reports4.7.2.NET/runtime10.0.13; its game window was enumerated.
Graphical helper capture/activation failed, reset/reconnection then explicitly
reported physical Escape stop. No further UI control or alternative OS-input
injection was issued. No accepted screenshot or complete controlled gameplay
session is claimed, and owner hands-on testing is not demanded.

Windows export fails in .NET Publish/GetTargetFrameworks after restore; its partial
EXE/PCK lacks the self-contained runtime and is not a distribution. Shell GitHub
auth/network attempts fail; connected GitHub creates R003 at the authorized parent
for partial-source preservation. R003 validation report records commands, failures,
geometry policy, status of every gate and targeted remaining work. Final publication
verification is recorded separately. R003 is FAIL: minimum playable3D Windows goal
has not been demonstrated; no gate is waived. G-006/G-007 remain blocked; stop at
R003 without main merge, R004, Unity or another native expedition.

## R003-C01 corrective export recovery — 2026-11-05 Asia/Bangkok

Headquarters orders recovery from 4305f1c22d628916b1f2e0b82bb7079d44067f5d
on reconstruction/r003. All automated graphical interaction/playtesting is now
prohibited. Compilation, deterministic and headless checks are technical evidence
only. Owner qualification controls acceptance; no R003 PASS or R004/Unity follows.
Read permanent instructions and this full history before work. Original research,
core, bridge, test assertions and 3D gameplay implementation remain untouched.

Fresh Ubuntu24.04 host, matching Godot4.7.2.NET ed1daf0bf and SDK10.0.402/runtime
10.0.13 reproduced the export Publish/GetTargetFrameworks failure, including exit0
and partial EXE/PCK without runtime. The Linux SDK lacked NETStandard.Library.Ref;
installed the official2.1.0 reference pack without altering the portable target.
Direct serialized publish succeeds with zero diagnostics. Process-local
DOTNET_PROCESSOR_COUNT=1 also lets the actual Godot exporter complete Publish.
The lower-level concurrency failure remains undiagnosed; this is an observed
build-process mitigation, not a proven gameplay defect or engine patch.

A subsequent resource-packing ERROR exposed bridge/obj sourcelink JSON indexed
before Publish removed it. Added .gdignore in bridge/tests; project references
still compile. Fresh import/export then completes without ERROR/WARNING lines.
Updated PowerShell driver to serialize SDK children and remove mandatory RTK use.
Added cross-platform logged build/package driver and owner launch instructions.
It requires fresh output/evidence, checks required files/AMD64/.NET runtime/PCK
fixture contents, ZIP CRCs and extracted hashes. Full delivery results follow.

The first packaging verifier incorrectly required the editor-only GodotPlugins
assembly in the Windows game. Rejected that packaging attempt at the assertion;
no ZIP was delivered. Corrected the required-file list and strengthened validation
to require every runtime/native/resource asset listed by the exported deps.json.
This changes the packaging checker only, not gameplay or regression expectations.
