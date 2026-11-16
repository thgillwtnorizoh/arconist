# S01 — Audited coverage register / A01

Status: OPEN. Audit source: `618fb55dc987c9bc4b172c5d7038b8b4bfae4b21`; exact production assessed: `ab349d441dfa02f3c1ff97d6d0b8837c6ebb8f0e`. Every production statement below refers to that immutable SHA; current main production bytes match it. Component tests were NOT rerun by Work1. No row is INDEPENDENTLY VERIFIED by A01. Historical owner acceptance of R001–R010 is preserved; final integrated S01 owner qualification is still required.

Stable parent IDs S01-01–S01-16 from the provisional register remain domain anchors; numbered child requirements below refine them. No requirement is owner-approved excluded. M = mandatory functional behavior; H = applicability/boundary requires Headquarters decision and stays OPEN. E evidence retains native-integrated/isolated/instruction-backed/inferred/blocked/unknown scopes from [Scout003](../../../scouts/003_native_gameplay_coverage_and_reconstruction_gap_audit.md) (link corrected below). CONFIRMED ORIGINAL describes the original evidence only; source inspection is not executed production verification. RECONSTRUCTED/ENGINEERING implementations may have historical VERIFIED COMPONENT development evidence, never automatically independent QA.

Each entry includes a closure test, owner qualification, actor/priority, dependency and discrepancy. Native evidence cited below is inherited from unchanged Scout003 and its linked E001–E042 reports; current implementation findings replace only the old reconstruction column, not historical native conclusions.

## S01-01.01 — Typed AFF grammar and headers

- Applicability/status: **M; OPEN — partial implemented profile; historical VERIFIED COMPONENT only**. H is a decision gate, not exclusion; platform/artwork may be external only if S01 behavior remains functional.
- Required original/evidence: E002 `0x923240`, integer/float helpers; E010 `0x1870de0`, `0x10dbff8`. Historical confidence: **NI valid fixtures; IB broader grammar**; preserve the full report's supplied-object/runtime limits. Original behavior target: Typed AFF grammar and headers; uncertainty: Invalid/exponent/locale/nonfinite compatibility is not complete.
- Production at `ab349d441dfa02f3c1ff97d6d0b8837c6ebb8f0e`: `reconstructed/core/Chart.cs`. Typed regex/scanner; unknown headers, floating positions, signed times, unsupported modes rejected. Not full native lexer compatibility.
- Tests/reference coverage: `reference_traces/r001/`, corresponding `reconstructed/validation/R001.md` and core/bridge/Godot development suites. Expectations and execution described there are Work2 provenance; **independent exact-SHA QA NOT RUN / NOT ESTABLISHED**.
- Dependencies/discrepancy: Parser, chart; **D01**, see [dependency register](dependency-register.md) and [discrepancy register](discrepancy-register.md).
- Closure/owner requirement: independently derive event-level expected results from the cited original source, exercise supported and rejected boundaries plus this feature in a mixed chart; owner qualifies visible targets, physical input/audio where relevant, completion and replay on final Windows corpus. Prior isolated checkpoint approval alone cannot close this row.
- Remaining work/priority/actor: W2-01; P0 for scope/blocker decisions or critical chart/contact dependencies, P1 implementation/QA, P2 exact fidelity after functional equivalence. Work 2 extend per mechanic; keep explicit unsupported/error policy rather than mimic native noncompletion is historical advice, not authorization. No new execution starts in A01.

## S01-01.02 — Whole chart initialization and judgment units

- Applicability/status: **M; OPEN — partial implemented profile; historical VERIFIED COMPONENT only**. H is a decision gate, not exclusion; platform/artwork may be external only if S01 behavior remains functional.
- Required original/evidence: E010 `0x173b358→0x1862a14`, count `0x11ea120` before bars; E038/E036 refinements. Historical confidence: **NI**; preserve the full report's supplied-object/runtime limits. Original behavior target: Whole chart initialization and judgment units; uncertainty: Special chart/digest flags and zero-unit charts remain bounded.
- Production at `ab349d441dfa02f3c1ff97d6d0b8837c6ebb8f0e`: `reconstructed/core/Chart.cs`. Units include enabled taps, hold records, arc weights/children; supported initialization only; no general control/bar objects.
- Tests/reference coverage: `reference_traces/r004/`, corresponding `reconstructed/validation/R004.md` and core/bridge/Godot development suites. Expectations and execution described there are Work2 provenance; **independent exact-SHA QA NOT RUN / NOT ESTABLISHED**.
- Dependencies/discrepancy: Parser, runtime, results; **D01**, see [dependency register](dependency-register.md) and [discrepancy register](discrepancy-register.md).
- Closure/owner requirement: independently derive event-level expected results from the cited original source, exercise supported and rejected boundaries plus this feature in a mixed chart; owner qualifies visible targets, physical input/audio where relevant, completion and replay on final Windows corpus. Prior isolated checkpoint approval alone cannot close this row.
- Remaining work/priority/actor: W2-01; P0 for scope/blocker decisions or critical chart/contact dependencies, P1 implementation/QA, P2 exact fidelity after functional equivalence. Work 2 introduce typed initialization and per-unit counting; bars never inflate N is historical advice, not authorization. No new execution starts in A01.

## S01-07.01 — Independent timing groups

- Applicability/status: **M; OPEN — partial implemented profile; historical VERIFIED COMPONENT only**. H is a decision gate, not exclusion; platform/artwork may be external only if S01 behavior remains functional.
- Required original/evidence: E029 `native_timing_group.aff`, per-group `0xcf918c`, `0x1576aa4`. Historical confidence: **NI**; preserve the full report's supplied-object/runtime limits. Original behavior target: Independent timing groups; uncertainty: Arbitrary attributes/group lifetime variants not covered.
- Production at `ab349d441dfa02f3c1ff97d6d0b8837c6ebb8f0e`: `reconstructed/core/TimingGroup.cs`. One extra nonnested tap-only group; hardcoded default120/group60, density1 and bounded duration/count. Mixed long-note groups rejected.
- Tests/reference coverage: `reference_traces/r010/`, corresponding `reconstructed/validation/R010.md` and core/bridge/Godot development suites. Expectations and execution described there are Work2 provenance; **independent exact-SHA QA NOT RUN / NOT ESTABLISHED**.
- Dependencies/discrepancy: Parser, group timing, index/render; **D02**, see [dependency register](dependency-register.md) and [discrepancy register](discrepancy-register.md).
- Closure/owner requirement: independently derive event-level expected results from the cited original source, exercise supported and rejected boundaries plus this feature in a mixed chart; owner qualifies visible targets, physical input/audio where relevant, completion and replay on final Windows corpus. Prior isolated checkpoint approval alone cannot close this row.
- Remaining work/priority/actor: W2-01; P0 for scope/blocker decisions or critical chart/contact dependencies, P1 implementation/QA, P2 exact fidelity after functional equivalence. Work 2 add group-local timing/depth/index; preserve group identity is historical advice, not authorization. No new execution starts in A01.

## S01-07.02 — Requested speed and tempo changes

- Applicability/status: **M; OPEN — partial implemented profile; historical VERIFIED COMPONENT only**. H is a decision gate, not exclusion; platform/artwork may be external only if S01 behavior remains functional.
- Required original/evidence: E010 `0xe17528`, `0xbe2b98`; E029 requested4→4.044943809509277 with metadata178. Historical confidence: **NI**; preserve the full report's supplied-object/runtime limits. Original behavior target: Requested speed and tempo changes; uncertainty: Metadata/special-flag breadth absent.
- Production at `ab349d441dfa02f3c1ff97d6d0b8837c6ebb8f0e`: `reconstructed/core/TimingGroup.cs`. Positive default timing; requested speed normalizes by metadata. No timing changes inside arcs.
- Tests/reference coverage: `reference_traces/r010/`, corresponding `reconstructed/validation/R010.md` and core/bridge/Godot development suites. Expectations and execution described there are Work2 provenance; **independent exact-SHA QA NOT RUN / NOT ESTABLISHED**.
- Dependencies/discrepancy: Metadata, timing; **D02**, see [dependency register](dependency-register.md) and [discrepancy register](discrepancy-register.md).
- Closure/owner requirement: independently derive event-level expected results from the cited original source, exercise supported and rejected boundaries plus this feature in a mixed chart; owner qualifies visible targets, physical input/audio where relevant, completion and replay on final Windows corpus. Prior isolated checkpoint approval alone cannot close this row.
- Remaining work/priority/actor: W2-01; P0 for scope/blocker decisions or critical chart/contact dependencies, P1 implementation/QA, P2 exact fidelity after functional equivalence. Work 2 preserve f32 stages and requested versus effective speed; expose bounded settings later is historical advice, not authorization. No new execution starts in A01.

## S01-07.03 — Negative BPM / reverse scroll

- Applicability/status: **M; OPEN — partial implemented profile; historical VERIFIED COMPONENT only**. H is a decision gate, not exclusion; platform/artwork may be external only if S01 behavior remains functional.
- Required original/evidence: E007 isolated scroll; E029 `native_reverse_scroll.aff` at1200/−60. Historical confidence: **NI bounded group; NX wider arithmetic**; preserve the full report's supplied-object/runtime limits. Original behavior target: Negative BPM / reverse scroll; uncertainty: General fresh-jump/reversal extrema not established by one retained-tap fixture.
- Production at `ab349d441dfa02f3c1ff97d6d0b8837c6ebb8f0e`: `reconstructed/core/TimingGroup.cs`. Only group1 +60 to -60; members must occur reversal+300; no default reverse or reverse noinput.
- Tests/reference coverage: `reference_traces/r010/`, corresponding `reconstructed/validation/R010.md` and core/bridge/Godot development suites. Expectations and execution described there are Work2 provenance; **independent exact-SHA QA NOT RUN / NOT ESTABLISHED**.
- Dependencies/discrepancy: Parser, timing, signed index, rendering; **D02**, see [dependency register](dependency-register.md) and [discrepancy register](discrepancy-register.md).
- Closure/owner requirement: independently derive event-level expected results from the cited original source, exercise supported and rejected boundaries plus this feature in a mixed chart; owner qualifies visible targets, physical input/audio where relevant, completion and replay on final Windows corpus. Prior isolated checkpoint approval alone cannot close this row.
- Remaining work/priority/actor: W2-01; P0 for scope/blocker decisions or critical chart/contact dependencies, P1 implementation/QA, P2 exact fidelity after functional equivalence. Work 2 preserve admission hysteresis and signed calculations; P06 only for broader claim is historical advice, not authorization. No new execution starts in A01.

## S01-01.03 — Negative timestamps and unusual numeric grammar

- Applicability/status: **H; OPEN**. H is a decision gate, not exclusion; platform/artwork may be external only if S01 behavior remains functional.
- Required original/evidence: E002 leading minus emits float; E010 malformed lexer limits. Historical confidence: **IB / UN**; preserve the full report's supplied-object/runtime limits. Original behavior target: Negative timestamps and unusual numeric grammar; uncertainty: Negative integer-position/time grammar and downstream validity not established.
- Production at `ab349d441dfa02f3c1ff97d6d0b8837c6ebb8f0e`: `reconstructed/core/Chart.cs`, `Kernel.cs`, Godot frontend. No complete implementation found in inspected core/frontend. Absent: nonnegative integer time required at Scout003 is historical only; current restrictions do not supply this missing behavior.
- Tests/reference coverage: No direct production-native reference established for this full requirement; historical native fixtures remain reusable. Expectations and execution described there are Work2 provenance; **independent exact-SHA QA NOT RUN / NOT ESTABLISHED**.
- Dependencies/discrepancy: Parser, runtime; **D01**, see [dependency register](dependency-register.md) and [discrepancy register](discrepancy-register.md).
- Closure/owner requirement: independently derive event-level expected results from the cited original source, exercise supported and rejected boundaries plus this feature in a mixed chart; owner qualifies visible targets, physical input/audio where relevant, completion and replay on final Windows corpus. Prior isolated checkpoint approval alone cannot close this row.
- Remaining work/priority/actor: W2-01; P0 for scope/blocker decisions or critical chart/contact dependencies, P1 implementation/QA, P2 exact fidelity after functional equivalence. P10 only if actual required content needs it; keep rejection until then is historical advice, not authorization. No new execution starts in A01.

## S01-07.04 — `noinput`

- Applicability/status: **M; OPEN — partial implemented profile; historical VERIFIED COMPONENT only**. H is a decision gate, not exclusion; platform/artwork may be external only if S01 behavior remains functional.
- Required original/evidence: E036 `0x8c8a14→0x18640f4`, N branch `0x11ea188`, expiry `0xf80654`; paired fixtures. Historical confidence: **NI ordinary taps**; preserve the full report's supplied-object/runtime limits. Original behavior target: `noinput`; uncertainty: No-input holds/arcs not joined in that pair; rendering not proved absent.
- Production at `ab349d441dfa02f3c1ff97d6d0b8837c6ebb8f0e`: `reconstructed/core/Chart.cs`. Only separate-group taps; flags exclude N/end/input/expiry while retaining active/index state.
- Tests/reference coverage: `reference_traces/r010/`, corresponding `reconstructed/validation/R010.md` and core/bridge/Godot development suites. Expectations and execution described there are Work2 provenance; **independent exact-SHA QA NOT RUN / NOT ESTABLISHED**.
- Dependencies/discrepancy: Parser, N/end, index, input, result; **D02**, see [dependency register](dependency-register.md) and [discrepancy register](discrepancy-register.md).
- Closure/owner requirement: independently derive event-level expected results from the cited original source, exercise supported and rejected boundaries plus this feature in a mixed chart; owner qualifies visible targets, physical input/audio where relevant, completion and replay on final Windows corpus. Prior isolated checkpoint approval alone cannot close this row.
- Remaining work/priority/actor: W2-01; P0 for scope/blocker decisions or critical chart/contact dependencies, P1 implementation/QA, P2 exact fidelity after functional equivalence. Work 2 preserve indexed/active disabled objects while excluding input/N/end/expiry; P07 for long-note extension is historical advice, not authorization. No new execution starts in A01.

## S01-08.01 — Lane widening / secondary eligibility

- Applicability/status: **M; OPEN**. H is a decision gate, not exclusion; platform/artwork may be external only if S01 behavior remains functional.
- Required original/evidence: E039 `0x1792e18`, strict `0xf8071c`, `0x1514c64`, G/W stores `0x10a763c/0x10a76f8`; three fixtures. Historical confidence: **NI**; preserve the full report's supplied-object/runtime limits. Original behavior target: Lane widening / secondary eligibility; uncertainty: Visible widening consumers remain partial.
- Production at `ab349d441dfa02f3c1ff97d6d0b8837c6ebb8f0e`: `reconstructed/core/Chart.cs`, `Kernel.cs`, Godot frontend. No complete implementation found in inspected core/frontend. Absent; Down only2–5 and ground picker clips X at Scout003 is historical only; current restrictions do not supply this missing behavior.
- Tests/reference coverage: No direct production-native reference established for this full requirement; historical native fixtures remain reusable. Expectations and execution described there are Work2 provenance; **independent exact-SHA QA NOT RUN / NOT ESTABLISHED**.
- Dependencies/discrepancy: Parser, frame, input, rendering; **D13**, see [dependency register](dependency-register.md) and [discrepancy register](discrepancy-register.md).
- Closure/owner requirement: independently derive event-level expected results from the cited original source, exercise supported and rejected boundaries plus this feature in a mixed chart; owner qualifies visible targets, physical input/audio where relevant, completion and replay on final Windows corpus. Prior isolated checkpoint approval alone cannot close this row.
- Remaining work/priority/actor: W2-03; P0 for scope/blocker decisions or critical chart/contact dependencies, P1 implementation/QA, P2 exact fidelity after functional equivalence. Work 2 implement both transitions and lane pair; do not call kind5 a demonstrated FOV change is historical advice, not authorization. No new execution starts in A01.

## S01-14.01 — Chart completion and unit reconciliation

- Applicability/status: **M; OPEN — partial implemented profile; historical VERIFIED COMPONENT only**. H is a decision gate, not exclusion; platform/artwork may be external only if S01 behavior remains functional.
- Required original/evidence: E006/E009 `0x10a7b38`, `0x1600bb0`; E036/E042 completion/cache. Historical confidence: **NI ordinary; IB special extensions**; preserve the full report's supplied-object/runtime limits. Original behavior target: Chart completion and unit reconciliation; uncertainty: Special+6000/+2000 and result flags lack ordinary producer proof.
- Production at `ab349d441dfa02f3c1ff97d6d0b8837c6ebb8f0e`: `reconstructed/core/Kernel.cs`. Supported chart-end/cache and recorded versus reconciled LOST. No full corpus closure.
- Tests/reference coverage: `reference_traces/r010/`, corresponding `reconstructed/validation/R010.md` and core/bridge/Godot development suites. Expectations and execution described there are Work2 provenance; **independent exact-SHA QA NOT RUN / NOT ESTABLISHED**.
- Dependencies/discrepancy: Clock, active list, N, result; **D10**, see [dependency register](dependency-register.md) and [discrepancy register](discrepancy-register.md).
- Closure/owner requirement: independently derive event-level expected results from the cited original source, exercise supported and rejected boundaries plus this feature in a mixed chart; owner qualifies visible targets, physical input/audio where relevant, completion and replay on final Windows corpus. Prior isolated checkpoint approval alone cannot close this row.
- Remaining work/priority/actor: W1-01; P0 for scope/blocker decisions or critical chart/contact dependencies, P1 implementation/QA, P2 exact fidelity after functional equivalence. Work 2 use supported-object end rules; final LOST is not retroactive miss damage is historical advice, not authorization. No new execution starts in A01.

## S01-12.01 — AFF/user/profile offsets

- Applicability/status: **M; OPEN — partial implemented profile; historical VERIFIED COMPONENT only**. H is a decision gate, not exclusion; platform/artwork may be external only if S01 behavior remains functional.
- Required original/evidence: E005; E040 Settings owner `0x1a146a0→0x1a02b48`, add `0xfbff4c`, store `0xfbff54`. Historical confidence: **NI settings→judgment; IB missing-key defaults**; preserve the full report's supplied-object/runtime limits. Original behavior target: AFF/user/profile offsets; uncertainty: Real route detection/preferences file parsing absent.
- Production at `ab349d441dfa02f3c1ff97d6d0b8837c6ebb8f0e`: `reconstructed/core/../godot/bridge/GameplaySession.cs`. Explicit supplied regular/alternate values; current/legacy settings producer and persistent preferences not fully reproduced.
- Tests/reference coverage: `reference_traces/r005/`, corresponding `reconstructed/validation/R005.md` and core/bridge/Godot development suites. Expectations and execution described there are Work2 provenance; **independent exact-SHA QA NOT RUN / NOT ESTABLISHED**.
- Dependencies/discrepancy: Config, chart, clock, audio; **D11**, see [dependency register](dependency-register.md) and [discrepancy register](discrepancy-register.md).
- Closure/owner requirement: independently derive event-level expected results from the cited original source, exercise supported and rejected boundaries plus this feature in a mixed chart; owner qualifies visible targets, physical input/audio where relevant, completion and replay on final Windows corpus. Prior isolated checkpoint approval alone cannot close this row.
- Remaining work/priority/actor: W2-03; P0 for scope/blocker decisions or critical chart/contact dependencies, P1 implementation/QA, P2 exact fidelity after functional equivalence. Work 2 add configuration boundary and explicit profile; preserve migration exactly once is historical advice, not authorization. No new execution starts in A01.

## S01-12.02 — Preroll, startup and effective clock

- Applicability/status: **M; OPEN — partial implemented profile; historical VERIFIED COMPONENT only**. H is a decision gate, not exclusion; platform/artwork may be external only if S01 behavior remains functional.
- Required original/evidence: E005/E040 `0x8db04c`, `0x16c90bc`, request `0x16c9194`, C/B stores. Historical confidence: **NI clock/request; IB full alternatives**; preserve the full report's supplied-object/runtime limits. Original behavior target: Preroll, startup and effective clock; uncertainty: Audible scheduling/backend readiness unmeasured.
- Production at `ab349d441dfa02f3c1ff97d6d0b8837c6ebb8f0e`: `reconstructed/core/Kernel.cs`. Strict request before compensation; shared monotonic steady A0 clock.
- Tests/reference coverage: `reference_traces/r005/`, corresponding `reconstructed/validation/R005.md` and core/bridge/Godot development suites. Expectations and execution described there are Work2 provenance; **independent exact-SHA QA NOT RUN / NOT ESTABLISHED**.
- Dependencies/discrepancy: Clock, audio adapter; **D11**, see [dependency register](dependency-register.md) and [discrepancy register](discrepancy-register.md).
- Closure/owner requirement: independently derive event-level expected results from the cited original source, exercise supported and rejected boundaries plus this feature in a mixed chart; owner qualifies visible targets, physical input/audio where relevant, completion and replay on final Windows corpus. Prior isolated checkpoint approval alone cannot close this row.
- Remaining work/priority/actor: W2-03; P0 for scope/blocker decisions or critical chart/contact dependencies, P1 implementation/QA, P2 exact fidelity after functional equivalence. Work 2 connect request callback without making audio position authoritative is historical advice, not authorization. No new execution starts in A01.

## S01-12.03 — Synchronization, seek and drift

- Applicability/status: **M; OPEN — partial implemented profile; historical VERIFIED COMPONENT only**. H is a decision gate, not exclusion; platform/artwork may be external only if S01 behavior remains functional.
- Required original/evidence: E005 `0x9e74f4`, `0xa19088`; FMOD provider `0x270a8/0x35b38`. Historical confidence: **NI resume requests E041; NX/IB provider math; UN drift policy**; preserve the full report's supplied-object/runtime limits. Original behavior target: Synchronization, seek and drift; uncertainty: No demonstrated continuous drift servo, output latency or all adjustment-mode state.
- Production at `ab349d441dfa02f3c1ff97d6d0b8837c6ebb8f0e`: `reconstructed/core/Kernel.cs`. Pause resume uses E-B; arbitrary seek/adjustment A modes and drift equivalence not implemented.
- Tests/reference coverage: `reference_traces/r006/`, corresponding `reconstructed/validation/R006.md` and core/bridge/Godot development suites. Expectations and execution described there are Work2 provenance; **independent exact-SHA QA NOT RUN / NOT ESTABLISHED**.
- Dependencies/discrepancy: Clock, audio, lifecycle; **D11**, see [dependency register](dependency-register.md) and [discrepancy register](discrepancy-register.md).
- Closure/owner requirement: independently derive event-level expected results from the cited original source, exercise supported and rejected boundaries plus this feature in a mixed chart; owner qualifies visible targets, physical input/audio where relevant, completion and replay on final Windows corpus. Prior isolated checkpoint approval alone cannot close this row.
- Remaining work/priority/actor: W2-03; P0 for scope/blocker decisions or critical chart/contact dependencies, P1 implementation/QA, P2 exact fidelity after functional equivalence. Work 2 ordinary E−B seek; P08 for extra modes; never invent a native drift controller is historical advice, not authorization. No new execution starts in A01.

## S01-02.01 — Ordinary ground taps

- Applicability/status: **M; OPEN — partial implemented profile; historical VERIFIED COMPONENT only**. H is a decision gate, not exclusion; platform/artwork may be external only if S01 behavior remains functional.
- Required original/evidence: E002 `0x160ce28/0x965e28`; E024/E035/E042. Historical confidence: **NI**; preserve the full report's supplied-object/runtime limits. Original behavior target: Ordinary ground taps; uncertainty: Equal-start stability and unusual positions unverified.
- Production at `ab349d441dfa02f3c1ff97d6d0b8837c6ebb8f0e`: `reconstructed/core/Kernel.cs`. Ordinary taps, lanes2–5 and shared tap classifier; outer raw lanes parse but cannot be selected.
- Tests/reference coverage: `reference_traces/r001/`, corresponding `reconstructed/validation/R001.md` and core/bridge/Godot development suites. Expectations and execution described there are Work2 provenance; **independent exact-SHA QA NOT RUN / NOT ESTABLISHED**.
- Dependencies/discrepancy: Parser, clock, input, recorder; **D03**, see [dependency register](dependency-register.md) and [discrepancy register](discrepancy-register.md).
- Closure/owner requirement: independently derive event-level expected results from the cited original source, exercise supported and rejected boundaries plus this feature in a mixed chart; owner qualifies visible targets, physical input/audio where relevant, completion and replay on final Windows corpus. Prior isolated checkpoint approval alone cannot close this row.
- Remaining work/priority/actor: W2-02; P0 for scope/blocker decisions or critical chart/contact dependencies, P1 implementation/QA, P2 exact fidelity after functional equivalence. Preserve existing core/oracles while adding types is historical advice, not authorization. No new execution starts in A01.

## S01-03.01 — Ordinary hold construction/checkpoints

- Applicability/status: **M; OPEN — partial implemented profile; historical VERIFIED COMPONENT only**. H is a decision gate, not exclusion; platform/artwork may be external only if S01 behavior remains functional.
- Required original/evidence: E001 `0x17cb97c/0xd92558`; E026/E037 whole AFF→factory `0x1446490`. Historical confidence: **NI; IB other interval/duration branches**; preserve the full report's supplied-object/runtime limits. Original behavior target: Ordinary hold construction/checkpoints; uncertainty: Broad tempo/short/zero-duration edge cases need declared scope.
- Production at `ab349d441dfa02f3c1ff97d6d0b8837c6ebb8f0e`: `reconstructed/core/Chart.cs`. Positive holds >=2ms, raw lanes1–4; finite interior checkpoint constraints and generation caps.
- Tests/reference coverage: `reference_traces/r004/`, corresponding `reconstructed/validation/R004.md` and core/bridge/Godot development suites. Expectations and execution described there are Work2 provenance; **independent exact-SHA QA NOT RUN / NOT ESTABLISHED**.
- Dependencies/discrepancy: Parser, long-note records, N/end/index; **D01**, see [dependency register](dependency-register.md) and [discrepancy register](discrepancy-register.md).
- Closure/owner requirement: independently derive event-level expected results from the cited original source, exercise supported and rejected boundaries plus this feature in a mixed chart; owner qualifies visible targets, physical input/audio where relevant, completion and replay on final Windows corpus. Prior isolated checkpoint approval alone cannot close this row.
- Remaining work/priority/actor: W2-01; P0 for scope/blocker decisions or critical chart/contact dependencies, P1 implementation/QA, P2 exact fidelity after functional equivalence. Work 2 R004; no artificial start/release judgment is historical advice, not authorization. No new execution starts in A01.

## S01-03.02 — Hold latch, activity and reacquisition

- Applicability/status: **M; OPEN — partial implemented profile; historical VERIFIED COMPONENT only**. H is a decision gate, not exclusion; platform/artwork may be external only if S01 behavior remains functional.
- Required original/evidence: E026 `0xeec6f0`, reset `0x1866038`, activation `0x14557b4`; native_hold.aff. Historical confidence: **NI**; preserve the full report's supplied-object/runtime limits. Original behavior target: Hold latch, activity and reacquisition; uncertainty: No persistent exclusive hold owner is established.
- Production at `ab349d441dfa02f3c1ff97d6d0b8837c6ebb8f0e`: `reconstructed/core/Kernel.cs`. Separate latch/activity/records; replacement retained contact and multiple sustaining contacts.
- Tests/reference coverage: `reference_traces/r004/`, corresponding `reconstructed/validation/R004.md` and core/bridge/Godot development suites. Expectations and execution described there are Work2 provenance; **independent exact-SHA QA NOT RUN / NOT ESTABLISHED**.
- Dependencies/discrepancy: Retained contacts, frame order, release; **D10**, see [dependency register](dependency-register.md) and [discrepancy register](discrepancy-register.md).
- Closure/owner requirement: independently derive event-level expected results from the cited original source, exercise supported and rejected boundaries plus this feature in a mixed chart; owner qualifies visible targets, physical input/audio where relevant, completion and replay on final Windows corpus. Prior isolated checkpoint approval alone cannot close this row.
- Remaining work/priority/actor: W1-01; P0 for scope/blocker decisions or critical chart/contact dependencies, P1 implementation/QA, P2 exact fidelity after functional equivalence. Work 2 distinct latch/activity/resolution; replacement contact can sustain is historical advice, not authorization. No new execution starts in A01.

## S01-03.03 — Hold versus same-lane taps

- Applicability/status: **M; OPEN — partial implemented profile; historical VERIFIED COMPONENT only**. H is a decision gate, not exclusion; platform/artwork may be external only if S01 behavior remains functional.
- Required original/evidence: E037 A1/A2/B, `0xeec6f4` stop, consumed guard then continuation. Historical confidence: **NI three histories**; preserve the full report's supplied-object/runtime limits. Original behavior target: Hold versus same-lane taps; uncertainty: Arbitrary equal-start/all-type conflict policy remains unverified.
- Production at `ab349d441dfa02f3c1ff97d6d0b8837c6ebb8f0e`: `reconstructed/core/Kernel.cs`. Older hold latch1→1 still stops DOWN; chronological tap/hold paths retained.
- Tests/reference coverage: `reference_traces/r004/`, corresponding `reconstructed/validation/R004.md` and core/bridge/Godot development suites. Expectations and execution described there are Work2 provenance; **independent exact-SHA QA NOT RUN / NOT ESTABLISHED**.
- Dependencies/discrepancy: Candidate sort, initial/continuous split; **D10**, see [dependency register](dependency-register.md) and [discrepancy register](discrepancy-register.md).
- Closure/owner requirement: independently derive event-level expected results from the cited original source, exercise supported and rejected boundaries plus this feature in a mixed chart; owner qualifies visible targets, physical input/audio where relevant, completion and replay on final Windows corpus. Prior isolated checkpoint approval alone cannot close this row.
- Remaining work/priority/actor: W1-01; P0 for scope/blocker decisions or critical chart/contact dependencies, P1 implementation/QA, P2 exact fidelity after functional equivalence. R004 reproduce hold-first starvation and tap-first two-DOWN path; do not “fix” native order is historical advice, not authorization. No new execution starts in A01.

## S01-04.01 — Ordinary arc geometry

- Applicability/status: **M; OPEN — partial implemented profile; historical VERIFIED COMPONENT only**. H is a decision gate, not exclusion; platform/artwork may be external only if S01 behavior remains functional.
- Required original/evidence: E003 `0x1925084/0x180a190`; E028 moving native geometry, native_moving_arc.aff. Historical confidence: **NI linear moving; NX other curve math**; preserve the full report's supplied-object/runtime limits. Original behavior target: Ordinary arc geometry; uncertainty: Degenerate curves/height production and exact visual topology bounded.
- Production at `ab349d441dfa02f3c1ff97d6d0b8837c6ebb8f0e`: `reconstructed/core/Arc.cs`. Linear s/none only; normalized coordinates0..1, colors0/1, no internal tempo changes.
- Tests/reference coverage: `reference_traces/r007/`, corresponding `reconstructed/validation/R007.md` and core/bridge/Godot development suites. Expectations and execution described there are Work2 provenance; **independent exact-SHA QA NOT RUN / NOT ESTABLISHED**.
- Dependencies/discrepancy: Parser, geometry, timing, cache, renderer; **D04**, see [dependency register](dependency-register.md) and [discrepancy register](discrepancy-register.md).
- Closure/owner requirement: independently derive event-level expected results from the cited original source, exercise supported and rejected boundaries plus this feature in a mixed chart; owner qualifies visible targets, physical input/audio where relevant, completion and replay on final Windows corpus. Prior isolated checkpoint approval alone cannot close this row.
- Remaining work/priority/actor: W2-01; P0 for scope/blocker decisions or critical chart/contact dependencies, P1 implementation/QA, P2 exact fidelity after functional equivalence. Work 2 initial linear arc; port literal arithmetic when adding curves is historical advice, not authorization. No new execution starts in A01.

## S01-04.02 — Continuous arc eligibility and ownership

- Applicability/status: **M; OPEN — partial implemented profile; historical VERIFIED COMPONENT only**. H is a decision gate, not exclusion; platform/artwork may be external only if S01 behavior remains functional.
- Required original/evidence: E009 `0xc98490→0x927384→0x15dfe2c→0x15a90c4`; E028. Historical confidence: **NI under services; NX wider ownership boundaries**; preserve the full report's supplied-object/runtime limits. Original behavior target: Continuous arc eligibility and ownership; uncertainty: Arbitrary mode/color/branching/release histories not all joined.
- Production at `ab349d441dfa02f3c1ff97d6d0b8837c6ebb8f0e`: `reconstructed/core/Kernel.cs`. Shared color owner/claimed IDs and release gate; no proximity-bypass state/update.
- Tests/reference coverage: `reference_traces/r007/`, corresponding `reconstructed/validation/R007.md` and core/bridge/Godot development suites. Expectations and execution described there are Work2 provenance; **independent exact-SHA QA NOT RUN / NOT ESTABLISHED**.
- Dependencies/discrepancy: Continuous positions, camera, color IDs; **D05**, see [dependency register](dependency-register.md) and [discrepancy register](discrepancy-register.md).
- Closure/owner requirement: independently derive event-level expected results from the cited original source, exercise supported and rejected boundaries plus this feature in a mixed chart; owner qualifies visible targets, physical input/audio where relevant, completion and replay on final Windows corpus. Prior isolated checkpoint approval alone cannot close this row.
- Remaining work/priority/actor: W2-01; P0 for scope/blocker decisions or critical chart/contact dependencies, P1 implementation/QA, P2 exact fidelity after functional equivalence. Work 2 shared LogicColor equivalent and global claimed IDs; separate contact departure from UP is historical advice, not authorization. No new execution starts in A01.

## S01-04.03 — Arc checkpoints and result recording

- Applicability/status: **M; OPEN — partial implemented profile; historical VERIFIED COMPONENT only**. H is a decision gate, not exclusion; platform/artwork may be external only if S01 behavior remains functional.
- Required original/evidence: E009 ordinary arc→GameResult; E028 actual unique records; E038 weighted calls. Historical confidence: **NI scoped**; preserve the full report's supplied-object/runtime limits. Original behavior target: Arc checkpoints and result recording; uncertainty: Moving/linked native-owned fixtures stop before results.
- Production at `ab349d441dfa02f3c1ff97d6d0b8837c6ebb8f0e`: `reconstructed/core/Kernel.cs`. Per-record weighted recorder calls and ordinary result composition; generic geometry/group behavior absent.
- Tests/reference coverage: `reference_traces/r009/`, corresponding `reconstructed/validation/R009.md` and core/bridge/Godot development suites. Expectations and execution described there are Work2 provenance; **independent exact-SHA QA NOT RUN / NOT ESTABLISHED**.
- Dependencies/discrepancy: Geometry cache, activity, long-note recorder, gauge/N; **D04**, see [dependency register](dependency-register.md) and [discrepancy register](discrepancy-register.md).
- Closure/owner requirement: independently derive event-level expected results from the cited original source, exercise supported and rejected boundaries plus this feature in a mixed chart; owner qualifies visible targets, physical input/audio where relevant, completion and replay on final Windows corpus. Prior isolated checkpoint approval alone cannot close this row.
- Remaining work/priority/actor: W2-01; P0 for scope/blocker decisions or critical chart/contact dependencies, P1 implementation/QA, P2 exact fidelity after functional equivalence. Work 2 preserve per-unit recorders and run completed reconstructed arc sessions; P05 for unverified conflicts is historical advice, not authorization. No new execution starts in A01.

## S01-04.04 — Moving/crossing arc color bypass

- Applicability/status: **M; OPEN — partial implemented profile; historical VERIFIED COMPONENT only**. H is a decision gate, not exclusion; platform/artwork may be external only if S01 behavior remains functional.
- Required original/evidence: E028 `0x19f439c/0x19f43a0`, native_crossing_arcs.aff. Historical confidence: **NI two contacts; NX E009 one-contact prepared overlaps**; preserve the full report's supplied-object/runtime limits. Original behavior target: Moving/crossing arc color bypass; uncertainty: Exact distance200 and one-contact moving crossing not swept.
- Production at `ab349d441dfa02f3c1ff97d6d0b8837c6ebb8f0e`: `reconstructed/core/Kernel.cs`. No E028 crossing proximity bypass implementation; Claim rejects foreign owned/claimed contacts.
- Tests/reference coverage: `reference_traces/r007/`, corresponding `reconstructed/validation/R007.md` and core/bridge/Godot development suites. Expectations and execution described there are Work2 provenance; **independent exact-SHA QA NOT RUN / NOT ESTABLISHED**.
- Dependencies/discrepancy: Cache update order, colors, continuous input; **D05**, see [dependency register](dependency-register.md) and [discrepancy register](discrepancy-register.md).
- Closure/owner requirement: independently derive event-level expected results from the cited original source, exercise supported and rejected boundaries plus this feature in a mixed chart; owner qualifies visible targets, physical input/audio where relevant, completion and replay on final Windows corpus. Prior isolated checkpoint approval alone cannot close this row.
- Remaining work/priority/actor: W2-01; P0 for scope/blocker decisions or critical chart/contact dependencies, P1 implementation/QA, P2 exact fidelity after functional equivalence. Work 2 retain sequential mixed-cache comparisons and timestamp+500 expiry; P05 for expanded scope is historical advice, not authorization. No new execution starts in A01.

## S01-04.05 — Connected arc linking/checkpoint production

- Applicability/status: **M; OPEN — partial implemented profile; historical VERIFIED COMPONENT only**. H is a decision gate, not exclusion; platform/artwork may be external only if S01 behavior remains functional.
- Required original/evidence: E038 `0x125e474`, defaults `0x178f8fc`, successor `0x125e784`, fold `0xba8274/78`. Historical confidence: **NI constant two-segment chain**; preserve the full report's supplied-object/runtime limits. Original behavior target: Connected arc linking/checkpoint production; uncertainty: Branching/curved/near-tolerance connection coverage partial.
- Production at `ab349d441dfa02f3c1ff97d6d0b8837c6ebb8f0e`: `reconstructed/core/LinkedArc.cs`. One exact adjacent constant color0 pair at120BPM/density1 with duration residues; group history empty/window0.
- Tests/reference coverage: `reference_traces/r009/`, corresponding `reconstructed/validation/R009.md` and core/bridge/Godot development suites. Expectations and execution described there are Work2 provenance; **independent exact-SHA QA NOT RUN / NOT ESTABLISHED**.
- Dependencies/discrepancy: Chart linking, geometry, record weights, color/group; **D06**, see [dependency register](dependency-register.md) and [discrepancy register](discrepancy-register.md).
- Closure/owner requirement: independently derive event-level expected results from the cited original source, exercise supported and rejected boundaries plus this feature in a mixed chart; owner qualifies visible targets, physical input/audio where relevant, completion and replay on final Windows corpus. Prior isolated checkpoint approval alone cannot close this row.
- Remaining work/priority/actor: W1-02; P0 for scope/blocker decisions or critical chart/contact dependencies, P1 implementation/QA, P2 exact fidelity after functional equivalence. Work 2 later separate milestone; root0/successor1, N7, preserve link/group state is historical advice, not authorization. No new execution starts in A01.

## S01-05.01 — Arc-tap parent/child production and judgment

- Applicability/status: **M; OPEN — partial implemented profile; historical VERIFIED COMPONENT only**. H is a decision gate, not exclusion; platform/artwork may be external only if S01 behavior remains functional.
- Required original/evidence: E025 `0x173a778`, parent link `0x1865514`, `0xc78814`, native_arc_tap.aff. Historical confidence: **NI one trace-parent child; IB other branches**; preserve the full report's supplied-object/runtime limits. Original behavior target: Arc-tap parent/child production and judgment; uncertainty: Broad parent modes/multiple-child conflicts not joined.
- Production at `ab349d441dfa02f3c1ff97d6d0b8837c6ebb8f0e`: `reconstructed/core/ArcTap.cs`. Exactly one strict-interior child on trace linear color0 parent; no ordinary arc children; ground/child proximity rejected by240ms policy.
- Tests/reference coverage: `reference_traces/r008/`, corresponding `reconstructed/validation/R008.md` and core/bridge/Godot development suites. Expectations and execution described there are Work2 provenance; **independent exact-SHA QA NOT RUN / NOT ESTABLISHED**.
- Dependencies/discrepancy: Arc parent geometry, child collection, initial spatial input, recorder; **D07**, see [dependency register](dependency-register.md) and [discrepancy register](discrepancy-register.md).
- Closure/owner requirement: independently derive event-level expected results from the cited original source, exercise supported and rejected boundaries plus this feature in a mixed chart; owner qualifies visible targets, physical input/audio where relevant, completion and replay on final Windows corpus. Prior isolated checkpoint approval alone cannot close this row.
- Remaining work/priority/actor: W1-02; P0 for scope/blocker decisions or critical chart/contact dependencies, P1 implementation/QA, P2 exact fidelity after functional equivalence. Work 2 standalone arc-tap milestone after sky projection; child is tap-tier judged once is historical advice, not authorization. No new execution starts in A01.

## S01-06.01 — Flick gesture and timing

- Applicability/status: **H; BLOCKED**. H is a decision gate, not exclusion; platform/artwork may be external only if S01 behavior remains functional.
- Required original/evidence: E009 `0x16e0548`: distance>106, angle<45°, bound ID; E033 builder discard `0x1864628`. Historical confidence: **NX predicate; IB callers; BL producer**; preserve the full report's supplied-object/runtime limits. Original behavior target: Flick gesture and timing; uncertainty: No original LogicFlickNote constructor/vtable/owning caller found.
- Production at `ab349d441dfa02f3c1ff97d6d0b8837c6ebb8f0e`: `reconstructed/core/Chart.cs`, `Kernel.cs`, Godot frontend. No complete implementation found in inspected core/frontend. Absent at Scout003 is historical only; current restrictions do not supply this missing behavior.
- Tests/reference coverage: No direct production-native reference established for this full requirement; historical native fixtures remain reusable. Expectations and execution described there are Work2 provenance; **independent exact-SHA QA NOT RUN / NOT ESTABLISHED**.
- Dependencies/discrepancy: Reachable logic factory, coordinates, input, recorder; **D16**, see [dependency register](dependency-register.md) and [discrepancy register](discrepancy-register.md).
- Closure/owner requirement: independently derive event-level expected results from the cited original source, exercise supported and rejected boundaries plus this feature in a mixed chart; owner qualifies visible targets, physical input/audio where relevant, completion and replay on final Windows corpus. Prior isolated checkpoint approval alone cannot close this row.
- Remaining work/priority/actor: W1-03; P0 for scope/blocker decisions or critical chart/contact dependencies, P1 implementation/QA, P2 exact fidelity after functional equivalence. P03 producer-first; a renderer/parser/RTTI name is insufficient is historical advice, not authorization. No new execution starts in A01.

## S01-02.02 — Simultaneous separated-lane chords

- Applicability/status: **M; OPEN — partial implemented profile; historical VERIFIED COMPONENT only**. H is a decision gate, not exclusion; platform/artwork may be external only if S01 behavior remains functional.
- Required original/evidence: E027 native_chord.aff, both DOWN orders, two retained Touches at E1500. Historical confidence: **NI two software deliveries**; preserve the full report's supplied-object/runtime limits. Original behavior target: Simultaneous separated-lane chords; uncertainty: Atomic MotionEvent batching/physical simultaneity not covered.
- Production at `ab349d441dfa02f3c1ff97d6d0b8837c6ebb8f0e`: `reconstructed/core/Kernel.cs`. Multiple logical keyboard contacts supported; software ordering, not physical multi-pointer transport proof.
- Tests/reference coverage: `reference_traces/r004/`, corresponding `reconstructed/validation/R004.md` and core/bridge/Godot development suites. Expectations and execution described there are Work2 provenance; **independent exact-SHA QA NOT RUN / NOT ESTABLISHED**.
- Dependencies/discrepancy: Contact identity, input ordering, taps; **D10**, see [dependency register](dependency-register.md) and [discrepancy register](discrepancy-register.md).
- Closure/owner requirement: independently derive event-level expected results from the cited original source, exercise supported and rejected boundaries plus this feature in a mixed chart; owner qualifies visible targets, physical input/audio where relevant, completion and replay on final Windows corpus. Prior isolated checkpoint approval alone cannot close this row.
- Remaining work/priority/actor: W1-01; P0 for scope/blocker decisions or critical chart/contact dependencies, P1 implementation/QA, P2 exact fidelity after functional equivalence. Work 2 add independent native-normalized chord validation; retain IDs across DOWN/UP is historical advice, not authorization. No new execution starts in A01.

## S01-10.01 — General mixed-note arbitration

- Applicability/status: **M; OPEN — partial implemented profile; historical VERIFIED COMPONENT only**. H is a decision gate, not exclusion; platform/artwork may be external only if S01 behavior remains functional.
- Required original/evidence: E004 signed-start comparator; E035 tap/tap; E037 hold/tap; E025 child path. Historical confidence: **NI specified pairs; IB/UN all combinations**; preserve the full report's supplied-object/runtime limits. Original behavior target: General mixed-note arbitration; uncertainty: Hold/arc/child/flick conflicts and equal-start stability are not collectively tested.
- Production at `ab349d441dfa02f3c1ff97d6d0b8837c6ebb8f0e`: `reconstructed/core/Kernel.cs`. Tap/hold chronology implemented; ground/child conflicts rejected; broader same-time cross-type policy unverified.
- Tests/reference coverage: `reference_traces/r008/`, corresponding `reconstructed/validation/R008.md` and core/bridge/Godot development suites. Expectations and execution described there are Work2 provenance; **independent exact-SHA QA NOT RUN / NOT ESTABLISHED**.
- Dependencies/discrepancy: All candidate types, shared input, continuous pass; **D07**, see [dependency register](dependency-register.md) and [discrepancy register](discrepancy-register.md).
- Closure/owner requirement: independently derive event-level expected results from the cited original source, exercise supported and rejected boundaries plus this feature in a mixed chart; owner qualifies visible targets, physical input/audio where relevant, completion and replay on final Windows corpus. Prior isolated checkpoint approval alone cannot close this row.
- Remaining work/priority/actor: W1-02; P0 for scope/blocker decisions or critical chart/contact dependencies, P1 implementation/QA, P2 exact fidelity after functional equivalence. Implement proven pairs now; P05 for one demanded conflict, not a universal policy is historical advice, not authorization. No new execution starts in A01.

## S01-02.03 — Initial selection, sorting, consuming return

- Applicability/status: **M; OPEN — partial implemented profile; historical VERIFIED COMPONENT only**. H is a decision gate, not exclusion; platform/artwork may be external only if S01 behavior remains functional.
- Required original/evidence: E004 `0xeec024/0xf6b514`; E035/E037. Historical confidence: **NI; IB comparator**; preserve the full report's supplied-object/runtime limits. Original behavior target: Initial selection, sorting, consuming return; uncertainty: Equal-start sort stability unknown.
- Production at `ab349d441dfa02f3c1ff97d6d0b8837c6ebb8f0e`: `reconstructed/core/Kernel.cs`. Signed start then source order; equal-start tie is engineering choice, not demonstrated native stable sort.
- Tests/reference coverage: `reference_traces/r001/`, corresponding `reconstructed/validation/R001.md` and core/bridge/Godot development suites. Expectations and execution described there are Work2 provenance; **independent exact-SHA QA NOT RUN / NOT ESTABLISHED**.
- Dependencies/discrepancy: Input, active list, clock; **D10**, see [dependency register](dependency-register.md) and [discrepancy register](discrepancy-register.md).
- Closure/owner requirement: independently derive event-level expected results from the cited original source, exercise supported and rejected boundaries plus this feature in a mixed chart; owner qualifies visible targets, physical input/audio where relevant, completion and replay on final Windows corpus. Prior isolated checkpoint approval alone cannot close this row.
- Remaining work/priority/actor: W1-01; P0 for scope/blocker decisions or critical chart/contact dependencies, P1 implementation/QA, P2 exact fidelity after functional equivalence. Preserve chronological signed-start key and guards; P05 if tie fidelity is needed is historical advice, not authorization. No new execution starts in A01.

## S01-10.02 — Continuous contact movement

- Applicability/status: **M; OPEN — partial implemented profile; historical VERIFIED COMPONENT only**. H is a decision gate, not exclusion; platform/artwork may be external only if S01 behavior remains functional.
- Required original/evidence: E011 JNI `0x1706960→0x160b710`; E028 nine MOVE arrays. Historical confidence: **NI under JNI-array service**; preserve the full report's supplied-object/runtime limits. Original behavior target: Continuous contact movement; uncertainty: Actual Android queue and malformed arrays outside coverage.
- Production at `ab349d441dfa02f3c1ff97d6d0b8837c6ebb8f0e`: `reconstructed/core/Kernel.cs`. Move/MoveSpatial update retained lane/sky without initial judgment; frontend reprojects held mouse.
- Tests/reference coverage: `reference_traces/r007/`, corresponding `reconstructed/validation/R007.md` and core/bridge/Godot development suites. Expectations and execution described there are Work2 provenance; **independent exact-SHA QA NOT RUN / NOT ESTABLISHED**.
- Dependencies/discrepancy: Contact positions/current/previous, projection, frame; **D10**, see [dependency register](dependency-register.md) and [discrepancy register](discrepancy-register.md).
- Closure/owner requirement: independently derive event-level expected results from the cited original source, exercise supported and rejected boundaries plus this feature in a mixed chart; owner qualifies visible targets, physical input/audio where relevant, completion and replay on final Windows corpus. Prior isolated checkpoint approval alone cannot close this row.
- Remaining work/priority/actor: W1-01; P0 for scope/blocker decisions or critical chart/contact dependencies, P1 implementation/QA, P2 exact fidelity after functional equivalence. Work 2 add MOVE/retained positions without judging taps again on MOVE is historical advice, not authorization. No new execution starts in A01.

## S01-10.03 — Three contact identities and retention

- Applicability/status: **M; OPEN — partial implemented profile; historical VERIFIED COMPONENT only**. H is a decision gate, not exclusion; platform/artwork may be external only if S01 behavior remains functional.
- Required original/evidence: E004/E011 Android ID→slot0–14→generated ID; E027/E028. Historical confidence: **NI**; preserve the full report's supplied-object/runtime limits. Original behavior target: Three contact identities and retention; uncertainty: Counter wrap/physical identity not covered.
- Production at `ab349d441dfa02f3c1ff97d6d0b8837c6ebb8f0e`: `reconstructed/core/Kernel.cs`. Pointer/generated identities managed; no engine15-slot transport emulation.
- Tests/reference coverage: `reference_traces/r004/`, corresponding `reconstructed/validation/R004.md` and core/bridge/Godot development suites. Expectations and execution described there are Work2 provenance; **independent exact-SHA QA NOT RUN / NOT ESTABLISHED**.
- Dependencies/discrepancy: Input, lifetime, ownership; **D10**, see [dependency register](dependency-register.md) and [discrepancy register](discrepancy-register.md).
- Closure/owner requirement: independently derive event-level expected results from the cited original source, exercise supported and rejected boundaries plus this feature in a mixed chart; owner qualifies visible targets, physical input/audio where relevant, completion and replay on final Windows corpus. Prior isolated checkpoint approval alone cannot close this row.
- Remaining work/priority/actor: W1-01; P0 for scope/blocker decisions or critical chart/contact dependencies, P1 implementation/QA, P2 exact fidelity after functional equivalence. Portable model keeps stable retained identity; engine slots may remain documented adapter choice is historical advice, not authorization. No new execution starts in A01.

## S01-10.04 — Release and CANCEL

- Applicability/status: **M; OPEN — partial implemented profile; historical VERIFIED COMPONENT only**. H is a decision gate, not exclusion; platform/artwork may be external only if S01 behavior remains functional.
- Required original/evidence: E011 `0xdda71c/0xd8dc50→0xf9a50c`; E026/E041. Historical confidence: **NI**; preserve the full report's supplied-object/runtime limits. Original behavior target: Release and CANCEL; uncertainty: Release clock depends on current Timeline E; not event timestamp.
- Production at `ab349d441dfa02f3c1ff97d6d0b8837c6ebb8f0e`: `reconstructed/core/Kernel.cs`. Up/Cancel release owner and retention; activity clears next frame.
- Tests/reference coverage: `reference_traces/r006/`, corresponding `reconstructed/validation/R006.md` and core/bridge/Godot development suites. Expectations and execution described there are Work2 provenance; **independent exact-SHA QA NOT RUN / NOT ESTABLISHED**.
- Dependencies/discrepancy: Input, colors, long-note reset; **D10**, see [dependency register](dependency-register.md) and [discrepancy register](discrepancy-register.md).
- Closure/owner requirement: independently derive event-level expected results from the cited original source, exercise supported and rejected boundaries plus this feature in a mixed chart; owner qualifies visible targets, physical input/audio where relevant, completion and replay on final Windows corpus. Prior isolated checkpoint approval alone cannot close this row.
- Remaining work/priority/actor: W1-01; P0 for scope/blocker decisions or critical chart/contact dependencies, P1 implementation/QA, P2 exact fidelity after functional equivalence. Work 2 release actual retained contact and owners once; next frame clears activity is historical advice, not authorization. No new execution starts in A01.

## S01-04.06 — Arc reacquisition / departure

- Applicability/status: **M; OPEN — partial implemented profile; historical VERIFIED COMPONENT only**. H is a decision gate, not exclusion; platform/artwork may be external only if S01 behavior remains functional.
- Required original/evidence: E003/E009 `0x13db7a0`, gate `min(4*interval,1000)`; E028 terminal release. Historical confidence: **NI prepared surrounding release test; NX isolated claim boundaries**; preserve the full report's supplied-object/runtime limits. Original behavior target: Arc reacquisition / departure; uncertainty: Full native-owned prolonged lift/repress trajectory not yet joined.
- Production at `ab349d441dfa02f3c1ff97d6d0b8837c6ebb8f0e`: `reconstructed/core/Kernel.cs`. Release-time gate and departure activity present in supported arc profile; broader native-owned trajectories not independently tested.
- Tests/reference coverage: `reference_traces/r007/`, corresponding `reconstructed/validation/R007.md` and core/bridge/Godot development suites. Expectations and execution described there are Work2 provenance; **independent exact-SHA QA NOT RUN / NOT ESTABLISHED**.
- Dependencies/discrepancy: Colors, clock, input, checkpoints; **D05**, see [dependency register](dependency-register.md) and [discrepancy register](discrepancy-register.md).
- Closure/owner requirement: independently derive event-level expected results from the cited original source, exercise supported and rejected boundaries plus this feature in a mixed chart; owner qualifies visible targets, physical input/audio where relevant, completion and replay on final Windows corpus. Prior isolated checkpoint approval alone cannot close this row.
- Remaining work/priority/actor: W2-01; P0 for scope/blocker decisions or critical chart/contact dependencies, P1 implementation/QA, P2 exact fidelity after functional equivalence. Work 2 literal ordinary gate; P05 only for native-owned extension is historical advice, not authorization. No new execution starts in A01.

## S01-10.05 — Ground and sky spatial projection

- Applicability/status: **M; OPEN — partial implemented profile; historical VERIFIED COMPONENT only**. H is a decision gate, not exclusion; platform/artwork may be external only if S01 behavior remains functional.
- Required original/evidence: E004 `0x16d3dcc/0x129dee0/0x130733c/0x927384`; E025/E028/E039. Historical confidence: **NI selected probes; NX edge sweeps**; preserve the full report's supplied-object/runtime limits. Original behavior target: Ground and sky spatial projection; uncertainty: Full feature-camera and every resolution mode bounded.
- Production at `ab349d441dfa02f3c1ff97d6d0b8837c6ebb8f0e`: `reconstructed/core/../godot/SpatialTrack.cs`. GroundY0 and skyZ0 actual Camera3D rays; fixed ordinary clamps, clipped outer X and safe-ray rejection.
- Tests/reference coverage: `reference_traces/r007/`, corresponding `reconstructed/validation/R007.md` and core/bridge/Godot development suites. Expectations and execution described there are Work2 provenance; **independent exact-SHA QA NOT RUN / NOT ESTABLISHED**.
- Dependencies/discrepancy: Camera, view conversion, geometry, G/W; **D03**, see [dependency register](dependency-register.md) and [discrepancy register](discrepancy-register.md).
- Closure/owner requirement: independently derive event-level expected results from the cited original source, exercise supported and rejected boundaries plus this feature in a mixed chart; owner qualifies visible targets, physical input/audio where relevant, completion and replay on final Windows corpus. Prior isolated checkpoint approval alone cannot close this row.
- Remaining work/priority/actor: W2-02; P0 for scope/blocker decisions or critical chart/contact dependencies, P1 implementation/QA, P2 exact fidelity after functional equivalence. Work 2 add Z0 sky plane and exact clamps/bounds separately; retain declared safety policy is historical advice, not authorization. No new execution starts in A01.

## S01-10.06 — Multitouch/capacity and ordering

- Applicability/status: **M; OPEN — partial implemented profile; historical VERIFIED COMPONENT only**. H is a decision gate, not exclusion; platform/artwork may be external only if S01 behavior remains functional.
- Required original/evidence: E011 capacity15/mapping; E027 overlapping two-contact lifetimes. Historical confidence: **NI selected limits/orders; IB Java transport**; preserve the full report's supplied-object/runtime limits. Original behavior target: Multitouch/capacity and ordering; uncertainty: Real GLThread/OS batching, three-plus-contact interactions not verified generally.
- Production at `ab349d441dfa02f3c1ff97d6d0b8837c6ebb8f0e`: `reconstructed/core/../godot/Main.cs`. Keyboard contacts plus one mouse pointer; no general physical sky multitouch adapter.
- Tests/reference coverage: `reference_traces/r007/`, corresponding `reconstructed/validation/R007.md` and core/bridge/Godot development suites. Expectations and execution described there are Work2 provenance; **independent exact-SHA QA NOT RUN / NOT ESTABLISHED**.
- Dependencies/discrepancy: Input adapter, retention, scheduling; **D10**, see [dependency register](dependency-register.md) and [discrepancy register](discrepancy-register.md).
- Closure/owner requirement: independently derive event-level expected results from the cited original source, exercise supported and rejected boundaries plus this feature in a mixed chart; owner qualifies visible targets, physical input/audio where relevant, completion and replay on final Windows corpus. Prior isolated checkpoint approval alone cannot close this row.
- Remaining work/priority/actor: W1-01; P0 for scope/blocker decisions or critical chart/contact dependencies, P1 implementation/QA, P2 exact fidelity after functional equivalence. Work 2 bounded adapter; P09 requires platform source/device authority is historical advice, not authorization. No new execution starts in A01.

## S01-02.04 — FRAME versus DOWN versus UP order

- Applicability/status: **M; OPEN — partial implemented profile; historical VERIFIED COMPONENT only**. H is a decision gate, not exclusion; platform/artwork may be external only if S01 behavior remains functional.
- Required original/evidence: E008/E009/E011/E035, once-per-Director guard and separate refresh. Historical confidence: **NI**; preserve the full report's supplied-object/runtime limits. Original behavior target: FRAME versus DOWN versus UP order; uncertainty: OS selects real delivery order outside evidence.
- Production at `ab349d441dfa02f3c1ff97d6d0b8837c6ebb8f0e`: `reconstructed/core/Kernel.cs`. FRAME and DOWN kept distinct; UP cleanup does not refresh clock.
- Tests/reference coverage: `reference_traces/r001/`, corresponding `reconstructed/validation/R001.md` and core/bridge/Godot development suites. Expectations and execution described there are Work2 provenance; **independent exact-SHA QA NOT RUN / NOT ESTABLISHED**.
- Dependencies/discrepancy: Clock, input, active range; **D10**, see [dependency register](dependency-register.md) and [discrepancy register](discrepancy-register.md).
- Closure/owner requirement: independently derive event-level expected results from the cited original source, exercise supported and rejected boundaries plus this feature in a mixed chart; owner qualifies visible targets, physical input/audio where relevant, completion and replay on final Windows corpus. Prior isolated checkpoint approval alone cannot close this row.
- Remaining work/priority/actor: W1-01; P0 for scope/blocker decisions or critical chart/contact dependencies, P1 implementation/QA, P2 exact fidelity after functional equivalence. Keep explicit callback order; DOWN refreshes Timeline without FRAME expiry/range; UP does not advance clock in current ordinary contract is historical advice, not authorization. No new execution starts in A01.

## S01-11.01 — Tap judgment tiers and misses

- Applicability/status: **M; OPEN — partial implemented profile; historical VERIFIED COMPONENT only**. H is a decision gate, not exclusion; platform/artwork may be external only if S01 behavior remains functional.
- Required original/evidence: E002 `0x160ce28`, E035 late LOST, E042 FAR60/expiry. Historical confidence: **NI main paths; NX boundary sweep**; preserve the full report's supplied-object/runtime limits. Original behavior target: Tap judgment tiers and misses; uncertainty: Special-window producers unknown.
- Production at `ab349d441dfa02f3c1ff97d6d0b8837c6ebb8f0e`: `reconstructed/core/Kernel.cs`. Ordinary inclusive25/50/100/120 bands; strict expiry and separate consumed/missed guards.
- Tests/reference coverage: `reference_traces/r001/`, corresponding `reconstructed/validation/R001.md` and core/bridge/Godot development suites. Expectations and execution described there are Work2 provenance; **independent exact-SHA QA NOT RUN / NOT ESTABLISHED**.
- Dependencies/discrepancy: Clock, candidates, note guards; **D10**, see [dependency register](dependency-register.md) and [discrepancy register](discrepancy-register.md).
- Closure/owner requirement: independently derive event-level expected results from the cited original source, exercise supported and rejected boundaries plus this feature in a mixed chart; owner qualifies visible targets, physical input/audio where relevant, completion and replay on final Windows corpus. Prior isolated checkpoint approval alone cannot close this row.
- Remaining work/priority/actor: W1-01; P0 for scope/blocker decisions or critical chart/contact dependencies, P1 implementation/QA, P2 exact fidelity after functional equivalence. Retain inclusive25/50/100/120 and strict frame>end+100; consuming LOST differs from hit is historical advice, not authorization. No new execution starts in A01.

## S01-11.02 — Ordinary score, combo/max, recovery

- Applicability/status: **M; OPEN — partial implemented profile; historical VERIFIED COMPONENT only**. H is a decision gate, not exclusion; platform/artwork may be external only if S01 behavior remains functional.
- Required original/evidence: E006/E042 `0x1730290/0x868e54/0xe43b80`, mixed_judgment_recovery.aff. Historical confidence: **NI six-tap histories**; preserve the full report's supplied-object/runtime limits. Original behavior target: Ordinary score, combo/max, recovery; uncertainty: Additional special caps/flags not ordinary.
- Production at `ab349d441dfa02f3c1ff97d6d0b8837c6ebb8f0e`: `reconstructed/core/Kernel.cs`. Ordinary score/combo/max recovery implemented. No independent accuracy percentage contract/property.
- Tests/reference coverage: `reference_traces/r001/`, corresponding `reconstructed/validation/R001.md` and core/bridge/Godot development suites. Expectations and execution described there are Work2 provenance; **independent exact-SHA QA NOT RUN / NOT ESTABLISHED**.
- Dependencies/discrepancy: Recorder, N, gauge; **D09**, see [dependency register](dependency-register.md) and [discrepancy register](discrepancy-register.md).
- Closure/owner requirement: independently derive event-level expected results from the cited original source, exercise supported and rejected boundaries plus this feature in a mixed chart; owner qualifies visible targets, physical input/audio where relevant, completion and replay on final Windows corpus. Prior isolated checkpoint approval alone cannot close this row.
- Remaining work/priority/actor: W1-02; P0 for scope/blocker decisions or critical chart/contact dependencies, P1 implementation/QA, P2 exact fidelity after functional equivalence. Extend reference coverage without deriving expectations from new code is historical advice, not authorization. No new execution starts in A01.

## S01-11.03 — Ordinary live gauge

- Applicability/status: **M; OPEN — partial implemented profile; historical VERIFIED COMPONENT only**. H is a decision gate, not exclusion; platform/artwork may be external only if S01 behavior remains functional.
- Required original/evidence: E006 `0x160a67c/0x16e4ab0/0x133fac8`; E026/E028/E037/E042. Historical confidence: **NI selected trajectories; NX gain bands**; preserve the full report's supplied-object/runtime limits. Original behavior target: Ordinary live gauge; uncertainty: Song flag scale and skill variants outside current subset.
- Production at `ab349d441dfa02f3c1ff97d6d0b8837c6ebb8f0e`: `reconstructed/core/Kernel.cs`. Mode0/no-ability ordinary gain and2HP misses; skill/song-flag modifiers absent.
- Tests/reference coverage: `reference_traces/r004/`, corresponding `reconstructed/validation/R004.md` and core/bridge/Godot development suites. Expectations and execution described there are Work2 provenance; **independent exact-SHA QA NOT RUN / NOT ESTABLISHED**.
- Dependencies/discrepancy: N, recorder, f32 arithmetic; **D08**, see [dependency register](dependency-register.md) and [discrepancy register](discrepancy-register.md).
- Closure/owner requirement: independently derive event-level expected results from the cited original source, exercise supported and rejected boundaries plus this feature in a mixed chart; owner qualifies visible targets, physical input/audio where relevant, completion and replay on final Windows corpus. Prior isolated checkpoint approval alone cannot close this row.
- Remaining work/priority/actor: HQ-01; P0 for scope/blocker decisions or critical chart/contact dependencies, P1 implementation/QA, P2 exact fidelity after functional equivalence. Preserve gain discontinuities, per-unit clamp and derived hold/arc nonmatching exact-RTTI damage is historical advice, not authorization. No new execution starts in A01.

## S01-15.01 — Easy/hard/overflow and staged/special gauges

- Applicability/status: **H; BLOCKED**. H is a decision gate, not exclusion; platform/artwork may be external only if S01 behavior remains functional.
- Required original/evidence: E006 map `0x1905bc8`, `0x120dd34`, frame failure `0x10a7d74`; E034. Historical confidence: **NX/IB arithmetic; BL modes6/11 producer**; preserve the full report's supplied-object/runtime limits. Original behavior target: Easy/hard/overflow and staged/special gauges; uncertainty: Numeric support is not a legitimately selected skill/session; p and mode11 context unresolved.
- Production at `ab349d441dfa02f3c1ff97d6d0b8837c6ebb8f0e`: `reconstructed/core/Chart.cs`, `Kernel.cs`, Godot frontend. No complete implementation found in inspected core/frontend. Absent at Scout003 is historical only; current restrictions do not supply this missing behavior.
- Tests/reference coverage: No direct production-native reference established for this full requirement; historical native fixtures remain reusable. Expectations and execution described there are Work2 provenance; **independent exact-SHA QA NOT RUN / NOT ESTABLISHED**.
- Dependencies/discrepancy: Config/ability producer, gauge vector, frame/result; **D08**, see [dependency register](dependency-register.md) and [discrepancy register](discrepancy-register.md).
- Closure/owner requirement: independently derive event-level expected results from the cited original source, exercise supported and rejected boundaries plus this feature in a mixed chart; owner qualifies visible targets, physical input/audio where relevant, completion and replay on final Windows corpus. Prior isolated checkpoint approval alone cannot close this row.
- Remaining work/priority/actor: HQ-01; P0 for scope/blocker decisions or critical chart/contact dependencies, P1 implementation/QA, P2 exact fidelity after functional equivalence. Work 2 may port explicitly isolated components; P04 before native-equivalent special session claim is historical advice, not authorization. No new execution starts in A01.

## S01-15.02 — Character skills

- Applicability/status: **H; BLOCKED**. H is a decision gate, not exclusion; platform/artwork may be external only if S01 behavior remains functional.
- Required original/evidence: E006 full-key `0x7ac3cc`, hooks; E034 account/stat updater `0x96b358`. Historical confidence: **NX representative ability; IB broad factories; BL target ownership**; preserve the full report's supplied-object/runtime limits. Original behavior target: Character skills; uncertainty: Catalog alone lacks initialized owner/current stats/activation provenance.
- Production at `ab349d441dfa02f3c1ff97d6d0b8837c6ebb8f0e`: `reconstructed/core/Chart.cs`, `Kernel.cs`, Godot frontend. No complete implementation found in inspected core/frontend. Absent at Scout003 is historical only; current restrictions do not supply this missing behavior.
- Tests/reference coverage: No direct production-native reference established for this full requirement; historical native fixtures remain reusable. Expectations and execution described there are Work2 provenance; **independent exact-SHA QA NOT RUN / NOT ESTABLISHED**.
- Dependencies/discrepancy: Owned Character/stats, activation, gauge, chart modifiers; **D08**, see [dependency register](dependency-register.md) and [discrepancy register](discrepancy-register.md).
- Closure/owner requirement: independently derive event-level expected results from the cited original source, exercise supported and rejected boundaries plus this feature in a mixed chart; owner qualifies visible targets, physical input/audio where relevant, completion and replay on final Windows corpus. Prior isolated checkpoint approval alone cannot close this row.
- Remaining work/priority/actor: HQ-01; P0 for scope/blocker decisions or critical chart/contact dependencies, P1 implementation/QA, P2 exact fidelity after functional equivalence. P04 narrowly for one target; no arbitrary key splitting or forged ownership is historical advice, not authorization. No new execution starts in A01.

## S01-11.04 — Failure and ordinary final classification

- Applicability/status: **M; OPEN — partial implemented profile; historical VERIFIED COMPONENT only**. H is a decision gate, not exclusion; platform/artwork may be external only if S01 behavior remains functional.
- Required original/evidence: E006 completion-before-HP branch; E042 H58/27→category0; E024 H80→3. Historical confidence: **NI ordinary; NX/IB hard thresholds**; preserve the full report's supplied-object/runtime limits. Original behavior target: Failure and ordinary final classification; uncertainty: Special grace/flags not native-produced here.
- Production at `ab349d441dfa02f3c1ff97d6d0b8837c6ebb8f0e`: `reconstructed/core/Kernel.cs`. Ordinary final H>=70 categories; no selected hard/special threshold/grace/failure lifecycle.
- Tests/reference coverage: `reference_traces/r001/`, corresponding `reconstructed/validation/R001.md` and core/bridge/Godot development suites. Expectations and execution described there are Work2 provenance; **independent exact-SHA QA NOT RUN / NOT ESTABLISHED**.
- Dependencies/discrepancy: Frame order, mode, H/F, result; **D08**, see [dependency register](dependency-register.md) and [discrepancy register](discrepancy-register.md).
- Closure/owner requirement: independently derive event-level expected results from the cited original source, exercise supported and rejected boundaries plus this feature in a mixed chart; owner qualifies visible targets, physical input/audio where relevant, completion and replay on final Windows corpus. Prior isolated checkpoint approval alone cannot close this row.
- Remaining work/priority/actor: HQ-01; P0 for scope/blocker decisions or critical chart/contact dependencies, P1 implementation/QA, P2 exact fidelity after functional equivalence. Ordinary H0 continues; do not add universal mid-song zero-health failure is historical advice, not authorization. No new execution starts in A01.

## S01-11.05 — GameResult snapshot/getters

- Applicability/status: **M; OPEN — partial implemented profile; historical VERIFIED COMPONENT only**. H is a decision gate, not exclusion; platform/artwork may be external only if S01 behavior remains functional.
- Required original/evidence: E006 `0x1600bb0/0x1315038/0x12a5574`; E036/E042. Historical confidence: **NI ordinary; IB unknown flag producers**; preserve the full report's supplied-object/runtime limits. Original behavior target: GameResult snapshot/getters; uncertainty: ScoreState+d1/d2, GameResult+b1 reachability unresolved.
- Production at `ab349d441dfa02f3c1ff97d6d0b8837c6ebb8f0e`: `reconstructed/core/Kernel.cs`. Cached ordinary default-flag result fields; special stored-score/selected-LOST flags absent.
- Tests/reference coverage: `reference_traces/r001/`, corresponding `reconstructed/validation/R001.md` and core/bridge/Godot development suites. Expectations and execution described there are Work2 provenance; **independent exact-SHA QA NOT RUN / NOT ESTABLISHED**.
- Dependencies/discrepancy: Counters/N, gauge, completion; **D09**, see [dependency register](dependency-register.md) and [discrepancy register](discrepancy-register.md).
- Closure/owner requirement: independently derive event-level expected results from the cited original source, exercise supported and rejected boundaries plus this feature in a mixed chart; owner qualifies visible targets, physical input/audio where relevant, completion and replay on final Windows corpus. Prior isolated checkpoint approval alone cannot close this row.
- Remaining work/priority/actor: W1-02; P0 for scope/blocker decisions or critical chart/contact dependencies, P1 implementation/QA, P2 exact fidelity after functional equivalence. Preserve recorded versus final LOST, floor(H), cached identity; P08 for a concrete flagged path is historical advice, not authorization. No new execution starts in A01.

## S01-13.01 — Ground track and tap placement

- Applicability/status: **M; OPEN — partial implemented profile; historical VERIFIED COMPONENT only**. H is a decision gate, not exclusion; platform/artwork may be external only if S01 behavior remains functional.
- Required original/evidence: E001/E007 `0xf20c28`; E020 native TrackBase/TrackLayer; E032 refresh. Historical confidence: **NI CPU; NX geometry fragments**; preserve the full report's supplied-object/runtime limits. Original behavior target: Ground track and tap placement; uncertainty: Mesh/material/artwork/GPU equivalence unproved.
- Production at `ab349d441dfa02f3c1ff97d6d0b8837c6ebb8f0e`: `reconstructed/core/../godot/SpatialTrack.cs`. Functional3D ground/taps/hold meshes; placeholder dimensions/materials.
- Tests/reference coverage: `reference_traces/r004/`, corresponding `reconstructed/validation/R004.md` and core/bridge/Godot development suites. Expectations and execution described there are Work2 provenance; **independent exact-SHA QA NOT RUN / NOT ESTABLISHED**.
- Dependencies/discrepancy: Depth, scene, camera, rendering; **D12**, see [dependency register](dependency-register.md) and [discrepancy register](discrepancy-register.md).
- Closure/owner requirement: independently derive event-level expected results from the cited original source, exercise supported and rejected boundaries plus this feature in a mixed chart; owner qualifies visible targets, physical input/audio where relevant, completion and replay on final Windows corpus. Prior isolated checkpoint approval alone cannot close this row.
- Remaining work/priority/actor: W2-02; P0 for scope/blocker decisions or critical chart/contact dependencies, P1 implementation/QA, P2 exact fidelity after functional equivalence. Work 2 visual iteration without changing judgment semantics is historical advice, not authorization. No new execution starts in A01.

## S01-13.02 — Sky/arc geometry and meshes

- Applicability/status: **M; OPEN — partial implemented profile; historical VERIFIED COMPONENT only**. H is a decision gate, not exclusion; platform/artwork may be external only if S01 behavior remains functional.
- Required original/evidence: E003/E007 sampler/segments `0x13b5ff8/0xd06628`; E028 geometry. Historical confidence: **NI sampled positions; NX cross-section; IB topology**; preserve the full report's supplied-object/runtime limits. Original behavior target: Sky/arc geometry and meshes; uncertainty: Exact UV/caps/zero-duration/material/height and missing textures.
- Production at `ab349d441dfa02f3c1ff97d6d0b8837c6ebb8f0e`: `reconstructed/core/../godot/SpatialTrack.cs`. Sampled linear ribbon/markers and target; H500 playable versus native fixtureH0 deliberately separate.
- Tests/reference coverage: `reference_traces/r007/`, corresponding `reconstructed/validation/R007.md` and core/bridge/Godot development suites. Expectations and execution described there are Work2 provenance; **independent exact-SHA QA NOT RUN / NOT ESTABLISHED**.
- Dependencies/discrepancy: Arc geometry/cache, renderer, resources; **D04**, see [dependency register](dependency-register.md) and [discrepancy register](discrepancy-register.md).
- Closure/owner requirement: independently derive event-level expected results from the cited original source, exercise supported and rejected boundaries plus this feature in a mixed chart; owner qualifies visible targets, physical input/audio where relevant, completion and replay on final Windows corpus. Prior isolated checkpoint approval alone cannot close this row.
- Remaining work/priority/actor: W2-01; P0 for scope/blocker decisions or critical chart/contact dependencies, P1 implementation/QA, P2 exact fidelity after functional equivalence. Work 2 ordinary arc visualization; P11 only for exact asset fidelity is historical advice, not authorization. No new execution starts in A01.

## S01-09.01 — Native camera defaults/matrices

- Applicability/status: **M; OPEN — partial implemented profile; historical VERIFIED COMPONENT only**. H is a decision gate, not exclusion; platform/artwork may be external only if S01 behavior remains functional.
- Required original/evidence: E007 `0x851514/0x9e2b60`; native-created rigs E018/E030. Historical confidence: **NI rig; NX resolution/action matrix probes**; preserve the full report's supplied-object/runtime limits. Original behavior target: Native camera defaults/matrices; uncertainty: Complete multi-camera layer/fidelity coverage absent.
- Production at `ab349d441dfa02f3c1ff97d6d0b8837c6ebb8f0e`: `reconstructed/core/../godot/SpatialTrack.cs`. Single engineering camera/view; grouped preset/apron, native two-mask composition absent.
- Tests/reference coverage: `reference_traces/r010/`, corresponding `reconstructed/validation/R010.md` and core/bridge/Godot development suites. Expectations and execution described there are Work2 provenance; **independent exact-SHA QA NOT RUN / NOT ESTABLISHED**.
- Dependencies/discrepancy: Viewport, camera, input; **D12**, see [dependency register](dependency-register.md) and [discrepancy register](discrepancy-register.md).
- Closure/owner requirement: independently derive event-level expected results from the cited original source, exercise supported and rejected boundaries plus this feature in a mixed chart; owner qualifies visible targets, physical input/audio where relevant, completion and replay on final Windows corpus. Prior isolated checkpoint approval alone cannot close this row.
- Remaining work/priority/actor: W2-02; P0 for scope/blocker decisions or critical chart/contact dependencies, P1 implementation/QA, P2 exact fidelity after functional equivalence. Work 2 state substitutions explicitly; do not treat F6 as native action is historical advice, not authorization. No new execution starts in A01.

## S01-09.02 — AFF camera actions, overlap and reset

- Applicability/status: **H; BLOCKED**. H is a decision gate, not exclusion; platform/artwork may be external only if S01 behavior remains functional.
- Required original/evidence: E007 NX actions/reset; E009 Scheduler action; E030 exclusion, E030-R upstream block. Historical confidence: **NX/IB parts; BL requested integration**; preserve the full report's supplied-object/runtime limits. Original behavior target: AFF camera actions, overlap and reset; uncertainty: Valid producer before overlap; child-target cancellation unknown.
- Production at `ab349d441dfa02f3c1ff97d6d0b8837c6ebb8f0e`: `reconstructed/core/Chart.cs`, `Kernel.cs`, Godot frontend. No complete implementation found in inspected core/frontend. Absent at Scout003 is historical only; current restrictions do not supply this missing behavior.
- Tests/reference coverage: No direct production-native reference established for this full requirement; historical native fixtures remain reusable. Expectations and execution described there are Work2 provenance; **independent exact-SHA QA NOT RUN / NOT ESTABLISHED**.
- Dependencies/discrepancy: Permitted chart/catalog, actions, camera/input; **D14**, see [dependency register](dependency-register.md) and [discrepancy register](discrepancy-register.md).
- Closure/owner requirement: independently derive event-level expected results from the cited original source, exercise supported and rejected boundaries plus this feature in a mixed chart; owner qualifies visible targets, physical input/audio where relevant, completion and replay on final Windows corpus. Prior isolated checkpoint approval alone cannot close this row.
- Remaining work/priority/actor: W1-03; P0 for scope/blocker decisions or critical chart/contact dependencies, P1 implementation/QA, P2 exact fidelity after functional equivalence. P01; no direct handler or chart+110 patch as proof is historical advice, not authorization. No new execution starts in A01.

## S01-09.03 — Track fade / trackdisplay

- Applicability/status: **H; BLOCKED**. H is a decision gate, not exclusion; platform/artwork may be external only if S01 behavior remains functional.
- Required original/evidence: E007 NX callback `0x1501dfc/0xef18e8`; E031 omission and owner+2c8=0. Historical confidence: **NX/IB parts; BL native dispatch/replacement**; preserve the full report's supplied-object/runtime limits. Original behavior target: Track fade / trackdisplay; uncertainty: Both construction and downstream feature gate need justified context.
- Production at `ab349d441dfa02f3c1ff97d6d0b8837c6ebb8f0e`: `reconstructed/core/Chart.cs`, `Kernel.cs`, Godot frontend. No complete implementation found in inspected core/frontend. Absent at Scout003 is historical only; current restrictions do not supply this missing behavior.
- Tests/reference coverage: No direct production-native reference established for this full requirement; historical native fixtures remain reusable. Expectations and execution described there are Work2 provenance; **independent exact-SHA QA NOT RUN / NOT ESTABLISHED**.
- Dependencies/discrepancy: Chart permission, control handler, Scheduler, track nodes; **D15**, see [dependency register](dependency-register.md) and [discrepancy register](discrepancy-register.md).
- Closure/owner requirement: independently derive event-level expected results from the cited original source, exercise supported and rejected boundaries plus this feature in a mixed chart; owner qualifies visible targets, physical input/audio where relevant, completion and replay on final Windows corpus. Prior isolated checkpoint approval alone cannot close this row.
- Remaining work/priority/actor: W1-03; P0 for scope/blocker decisions or critical chart/contact dependencies, P1 implementation/QA, P2 exact fidelity after functional equivalence. P02; admission exception alone does not prove visual permission is historical advice, not authorization. No new execution starts in A01.

## S01-07.05 — Hidegroup, angles, fadingholds, trace color

- Applicability/status: **M; OPEN**. H is a decision gate, not exclusion; platform/artwork may be external only if S01 behavior remains functional.
- Required original/evidence: E002 attributes; E007 `0x160a828`, conditional angle conversion, Ry*Rx. Historical confidence: **NX hide/angle components; IB/UN full attributes**; preserve the full report's supplied-object/runtime limits. Original behavior target: Hidegroup, angles, fadingholds, trace color; uncertainty: Native-owned attribute/control integration and several visual consumers unverified.
- Production at `ab349d441dfa02f3c1ff97d6d0b8837c6ebb8f0e`: `reconstructed/core/Chart.cs`, `Kernel.cs`, Godot frontend. No complete implementation found in inspected core/frontend. Absent at Scout003 is historical only; current restrictions do not supply this missing behavior.
- Tests/reference coverage: No direct production-native reference established for this full requirement; historical native fixtures remain reusable. Expectations and execution described there are Work2 provenance; **independent exact-SHA QA NOT RUN / NOT ESTABLISHED**.
- Dependencies/discrepancy: Groups, rendering, geometry, feature state; **D15**, see [dependency register](dependency-register.md) and [discrepancy register](discrepancy-register.md).
- Closure/owner requirement: independently derive event-level expected results from the cited original source, exercise supported and rejected boundaries plus this feature in a mixed chart; owner qualifies visible targets, physical input/audio where relevant, completion and replay on final Windows corpus. Prior isolated checkpoint approval alone cannot close this row.
- Remaining work/priority/actor: W1-03; P0 for scope/blocker decisions or critical chart/contact dependencies, P1 implementation/QA, P2 exact fidelity after functional equivalence. Implement bounded component only; P07 for a selected needed attribute is historical advice, not authorization. No new execution starts in A01.

## S01-08.02 — Widening visuals and special controls

- Applicability/status: **M; OPEN**. H is a decision gate, not exclusion; platform/artwork may be external only if S01 behavior remains functional.
- Required original/evidence: E007 kinds1–3; E039 equal camera endpoint matrices despite input change. Historical confidence: **IB/NX effects; UN full visuals**; preserve the full report's supplied-object/runtime limits. Original behavior target: Widening visuals and special controls; uncertainty: FOV/track-width consumers, redline/distort/debris content and gates.
- Production at `ab349d441dfa02f3c1ff97d6d0b8837c6ebb8f0e`: `reconstructed/core/Chart.cs`, `Kernel.cs`, Godot frontend. No complete implementation found in inspected core/frontend. Absent at Scout003 is historical only; current restrictions do not supply this missing behavior.
- Tests/reference coverage: No direct production-native reference established for this full requirement; historical native fixtures remain reusable. Expectations and execution described there are Work2 provenance; **independent exact-SHA QA NOT RUN / NOT ESTABLISHED**.
- Dependencies/discrepancy: Scene controls, resources, rendering; **D15**, see [dependency register](dependency-register.md) and [discrepancy register](discrepancy-register.md).
- Closure/owner requirement: independently derive event-level expected results from the cited original source, exercise supported and rejected boundaries plus this feature in a mixed chart; owner qualifies visible targets, physical input/audio where relevant, completion and replay on final Windows corpus. Prior isolated checkpoint approval alone cannot close this row.
- Remaining work/priority/actor: W1-03; P0 for scope/blocker decisions or critical chart/contact dependencies, P1 implementation/QA, P2 exact fidelity after functional equivalence. Keep G/W semantics separate; P02/P11 selected consumer only is historical advice, not authorization. No new execution starts in A01.

## S01-13.03 — Hold, arc-tap and flick mesh fidelity

- Applicability/status: **M; OPEN — partial implemented profile; historical VERIFIED COMPONENT only**. H is a decision gate, not exclusion; platform/artwork may be external only if S01 behavior remains functional.
- Required original/evidence: E007 unresolved hold/flick/child topology; E025 native child mesh/resource construction. Historical confidence: **NI child CPU construction; IB/UN complete topology**; preserve the full report's supplied-object/runtime limits. Original behavior target: Hold, arc-tap and flick mesh fidelity; uncertainty: Full hold/flick/arc-tap draw geometry and materials not recovered.
- Production at `ab349d441dfa02f3c1ff97d6d0b8837c6ebb8f0e`: `reconstructed/core/../godot/SpatialTrack.cs`. Hold bodies/checkpoints and child meshes exist; flick absent, exact native topology unverified.
- Tests/reference coverage: `reference_traces/r008/`, corresponding `reconstructed/validation/R008.md` and core/bridge/Godot development suites. Expectations and execution described there are Work2 provenance; **independent exact-SHA QA NOT RUN / NOT ESTABLISHED**.
- Dependencies/discrepancy: Note types, geometry, resources, renderer; **D12**, see [dependency register](dependency-register.md) and [discrepancy register](discrepancy-register.md).
- Closure/owner requirement: independently derive event-level expected results from the cited original source, exercise supported and rejected boundaries plus this feature in a mixed chart; owner qualifies visible targets, physical input/audio where relevant, completion and replay on final Windows corpus. Prior isolated checkpoint approval alone cannot close this row.
- Remaining work/priority/actor: W2-02; P0 for scope/blocker decisions or critical chart/contact dependencies, P1 implementation/QA, P2 exact fidelity after functional equivalence. Work 2 render playable targets/bodies while keeping semantic state independent; P11 for one exact mesh consumer is historical advice, not authorization. No new execution starts in A01.

## S01-13.04 — Note disappearance/culling/lifetime

- Applicability/status: **M; OPEN — partial implemented profile; historical VERIFIED COMPONENT only**. H is a decision gate, not exclusion; platform/artwork may be external only if S01 behavior remains functional.
- Required original/evidence: E032 `0xb1638c→0xcf2640→0xf20c28`, judged versus missed. Historical confidence: **NI tap CPU**; preserve the full report's supplied-object/runtime limits. Original behavior target: Note disappearance/culling/lifetime; uncertainty: Other note types/destruction/GPU not proved.
- Production at `ab349d441dfa02f3c1ff97d6d0b8837c6ebb8f0e`: `reconstructed/core/../godot/SpatialTrack.cs`. Present immediately hides resolved taps with depth clips; differs from E032 retained visible renderer lifecycle.
- Tests/reference coverage: `reference_traces/r010/`, corresponding `reconstructed/validation/R010.md` and core/bridge/Godot development suites. Expectations and execution described there are Work2 provenance; **independent exact-SHA QA NOT RUN / NOT ESTABLISHED**.
- Dependencies/discrepancy: Active list, renderer, frame order; **D12**, see [dependency register](dependency-register.md) and [discrepancy register](discrepancy-register.md).
- Closure/owner requirement: independently derive event-level expected results from the cited original source, exercise supported and rejected boundaries plus this feature in a mixed chart; owner qualifies visible targets, physical input/audio where relevant, completion and replay on final Windows corpus. Prior isolated checkpoint approval alone cannot close this row.
- Remaining work/priority/actor: W2-02; P0 for scope/blocker decisions or critical chart/contact dependencies, P1 implementation/QA, P2 exact fidelity after functional equivalence. Work 2 fidelity task; do not alter core active admission to match mesh visibility is historical advice, not authorization. No new execution starts in A01.

## S01-13.05 — Hit feedback, conflict effects, particles

- Applicability/status: **M; OPEN — partial implemented profile; historical VERIFIED COMPONENT only**. H is a decision gate, not exclusion; platform/artwork may be external only if S01 behavior remains functional.
- Required original/evidence: E003/E007 `0x155241c/0x15a0eac`; E020 creates particles. Historical confidence: **NI construction; NX blending; IB/UN triggers**; preserve the full report's supplied-object/runtime limits. Original behavior target: Hit feedback, conflict effects, particles; uncertainty: Exact trigger/resource selection/counter lifecycle unresolved.
- Production at `ab349d441dfa02f3c1ff97d6d0b8837c6ebb8f0e`: `reconstructed/core/../godot/Main.cs`. Text/colored target feedback; exact native particle/SFX/conflict lifecycle absent.
- Tests/reference coverage: `reference_traces/r008/`, corresponding `reconstructed/validation/R008.md` and core/bridge/Godot development suites. Expectations and execution described there are Work2 provenance; **independent exact-SHA QA NOT RUN / NOT ESTABLISHED**.
- Dependencies/discrepancy: Recorder, arc state, render, resources; **D12**, see [dependency register](dependency-register.md) and [discrepancy register](discrepancy-register.md).
- Closure/owner requirement: independently derive event-level expected results from the cited original source, exercise supported and rejected boundaries plus this feature in a mixed chart; owner qualifies visible targets, physical input/audio where relevant, completion and replay on final Windows corpus. Prior isolated checkpoint approval alone cannot close this row.
- Remaining work/priority/actor: W2-02; P0 for scope/blocker decisions or critical chart/contact dependencies, P1 implementation/QA, P2 exact fidelity after functional equivalence. Work 2 transparent substitutes; P11 for one exact trigger is historical advice, not authorization. No new execution starts in A01.

## S01-14.02 — Ending/results transition

- Applicability/status: **H; OPEN — partial implemented profile; historical VERIFIED COMPONENT only**. H is a decision gate, not exclusion; platform/artwork may be external only if S01 behavior remains functional.
- Required original/evidence: E014–E017 native callbacks; E023/E024/E042 complete ordinary CPU continuation. Historical confidence: **NI with declared UI/GPU omissions**; preserve the full report's supplied-object/runtime limits. Original behavior target: Ending/results transition; uncertainty: Full visual/widget/progression not recovered.
- Production at `ab349d441dfa02f3c1ff97d6d0b8837c6ebb8f0e`: `reconstructed/core/../godot/Main.cs`. Result HUD/replay functional; original outro/shutter not reproduced.
- Tests/reference coverage: `reference_traces/r009/`, corresponding `reconstructed/validation/R009.md` and core/bridge/Godot development suites. Expectations and execution described there are Work2 provenance; **independent exact-SHA QA NOT RUN / NOT ESTABLISHED**.
- Dependencies/discrepancy: Completion/cache, scene/actions, resources; **D13**, see [dependency register](dependency-register.md) and [discrepancy register](discrepancy-register.md).
- Closure/owner requirement: independently derive event-level expected results from the cited original source, exercise supported and rejected boundaries plus this feature in a mixed chart; owner qualifies visible targets, physical input/audio where relevant, completion and replay on final Windows corpus. Prior isolated checkpoint approval alone cannot close this row.
- Remaining work/priority/actor: W2-03; P0 for scope/blocker decisions or critical chart/contact dependencies, P1 implementation/QA, P2 exact fidelity after functional equivalence. Work 2 separate transition milestone; preserve cached result before presentation is historical advice, not authorization. No new execution starts in A01.

## S01-12.04 — BGM playback and SFX

- Applicability/status: **M; OPEN — partial implemented profile; historical VERIFIED COMPONENT only**. H is a decision gate, not exclusion; platform/artwork may be external only if S01 behavior remains functional.
- Required original/evidence: E005 manager `0x1735d7c/0x107af5c`, FMOD provider `0x270a8/0x26e04`; E040 requests only. Historical confidence: **NI requests; NX/IB provider; UN audible output**; preserve the full report's supplied-object/runtime limits. Original behavior target: BGM playback and SFX; uncertainty: Physical latency, backend clock alignment and complete SFX policy unmeasured.
- Production at `ab349d441dfa02f3c1ff97d6d0b8837c6ebb8f0e`: `reconstructed/core/../godot/bridge/BgmController.cs`. Bundled BGM through Godot backend; no complete original interactive/scheduled SFX implementation.
- Tests/reference coverage: `reference_traces/r005/`, corresponding `reconstructed/validation/R005.md` and core/bridge/Godot development suites. Expectations and execution described there are Work2 provenance; **independent exact-SHA QA NOT RUN / NOT ESTABLISHED**.
- Dependencies/discrepancy: Audio resources/backend, Timeline events; **D11**, see [dependency register](dependency-register.md) and [discrepancy register](discrepancy-register.md).
- Closure/owner requirement: independently derive event-level expected results from the cited original source, exercise supported and rejected boundaries plus this feature in a mixed chart; owner qualifies visible targets, physical input/audio where relevant, completion and replay on final Windows corpus. Prior isolated checkpoint approval alone cannot close this row.
- Remaining work/priority/actor: W2-03; P0 for scope/blocker decisions or critical chart/contact dependencies, P1 implementation/QA, P2 exact fidelity after functional equivalence. Work 2 R005 audible taps, independently label Godot backend substitution; no drift claim is historical advice, not authorization. No new execution starts in A01.

## S01-12.05 — Pause/resume and contact continuity

- Applicability/status: **M; OPEN — partial implemented profile; historical VERIFIED COMPONENT only**. H is a decision gate, not exclusion; platform/artwork may be external only if S01 behavior remains functional.
- Required original/evidence: E012; E041 `0xe0e5f4/0xf4f2e0`, `0x165211c/0xe31764/0x9e74f4`, native pause UI/dismissal. Historical confidence: **NI native-owned hold/UI under services**; preserve the full report's supplied-object/runtime limits. Original behavior target: Pause/resume and contact continuity; uncertainty: Physical finger persistence/OS queue and other modes remain unproved.
- Production at `ab349d441dfa02f3c1ff97d6d0b8837c6ebb8f0e`: `reconstructed/core/../godot/bridge/GameplaySession.cs`. Modal pause, explicit resume, audio seek/unpause, contact retention/terminal cleanup and focus policy.
- Tests/reference coverage: `reference_traces/r006/`, corresponding `reconstructed/validation/R006.md` and core/bridge/Godot development suites. Expectations and execution described there are Work2 provenance; **independent exact-SHA QA NOT RUN / NOT ESTABLISHED**.
- Dependencies/discrepancy: Clock, audio, UI, contacts, lifecycle; **D11**, see [dependency register](dependency-register.md) and [discrepancy register](discrepancy-register.md).
- Closure/owner requirement: independently derive event-level expected results from the cited original source, exercise supported and rejected boundaries plus this feature in a mixed chart; owner qualifies visible targets, physical input/audio where relevant, completion and replay on final Windows corpus. Prior isolated checkpoint approval alone cannot close this row.
- Remaining work/priority/actor: W2-03; P0 for scope/blocker decisions or critical chart/contact dependencies, P1 implementation/QA, P2 exact fidelity after functional equivalence. Work 2 R006 separate milestone; foreground does not auto-resume gameplay is historical advice, not authorization. No new execution starts in A01.

## S01-14.03 — Scene construction, loading, restart/teardown

- Applicability/status: **M; OPEN — partial implemented profile; historical VERIFIED COMPONENT only**. H is a decision gate, not exclusion; platform/artwork may be external only if S01 behavior remains functional.
- Required original/evidence: E018–E024 `0xee197c→0xee29e8→0xe2ea48`; E016 final Director activation. Historical confidence: **NI ordinary CPU, UN full reclamation**; preserve the full report's supplied-object/runtime limits. Original behavior target: Scene construction, loading, restart/teardown; uncertainty: Native destruction/re-entry/cancellation breadth unknown.
- Production at `ab349d441dfa02f3c1ff97d6d0b8837c6ebb8f0e`: `reconstructed/core/../godot/bridge/GameplaySession.cs`. Fresh managed kernel/session and audio cleanup; native destructor/account lifecycle not emulated.
- Tests/reference coverage: `reference_traces/r006/`, corresponding `reconstructed/validation/R006.md` and core/bridge/Godot development suites. Expectations and execution described there are Work2 provenance; **independent exact-SHA QA NOT RUN / NOT ESTABLISHED**.
- Dependencies/discrepancy: Chart/resources, state, inputs, audio; **D13**, see [dependency register](dependency-register.md) and [discrepancy register](discrepancy-register.md).
- Closure/owner requirement: independently derive event-level expected results from the cited original source, exercise supported and rejected boundaries plus this feature in a mixed chart; owner qualifies visible targets, physical input/audio where relevant, completion and replay on final Windows corpus. Prior isolated checkpoint approval alone cannot close this row.
- Remaining work/priority/actor: W2-03; P0 for scope/blocker decisions or critical chart/contact dependencies, P1 implementation/QA, P2 exact fidelity after functional equivalence. Work 2 reset owned managed/audio/input state; P08 only if native teardown semantics demanded is historical advice, not authorization. No new execution starts in A01.

## S01-14.04 — Song metadata and selectable charts

- Applicability/status: **M; OPEN — partial implemented profile; historical VERIFIED COMPONENT only**. H is a decision gate, not exclusion; platform/artwork may be external only if S01 behavior remains functional.
- Required original/evidence: E010 filename/metadata interfaces; E021–E024 selected-pair/ordinary entry. Historical confidence: **NI supplied base-song context; IB production catalog**; preserve the full report's supplied-object/runtime limits. Original behavior target: Song metadata and selectable charts; uncertainty: Full native catalog/defaults/purchases/unlocks missing.
- Production at `ab349d441dfa02f3c1ff97d6d0b8837c6ebb8f0e`: `reconstructed/core/../godot/Main.cs`. 18 bundled synthetic chart choices; no general song/chart import/catalog flow.
- Tests/reference coverage: `reference_traces/r010/`, corresponding `reconstructed/validation/R010.md` and core/bridge/Godot development suites. Expectations and execution described there are Work2 provenance; **independent exact-SHA QA NOT RUN / NOT ESTABLISHED**.
- Dependencies/discrepancy: Metadata, chart/audio resources, config; **D13**, see [dependency register](dependency-register.md) and [discrepancy register](discrepancy-register.md).
- Closure/owner requirement: independently derive event-level expected results from the cited original source, exercise supported and rejected boundaries plus this feature in a mixed chart; owner qualifies visible targets, physical input/audio where relevant, completion and replay on final Windows corpus. Prior isolated checkpoint approval alone cannot close this row.
- Remaining work/priority/actor: W2-03; P0 for scope/blocker decisions or critical chart/contact dependencies, P1 implementation/QA, P2 exact fidelity after functional equivalence. Work 2 local manifest without claiming native entitlement; P01 only for legitimate permitted research input is historical advice, not authorization. No new execution starts in A01.

## S01-14.05 — Result persistence

- Applicability/status: **H; OPEN — partial implemented profile; historical VERIFIED COMPONENT only**. H is a decision gate, not exclusion; platform/artwork may be external only if S01 behavior remains functional.
- Required original/evidence: E013 `0xdc2c48/0x13552d4/0x12a5e60`; E023/E024/E042 native SQLite. Historical confidence: **NI private-memory DB; IB/error paths**; preserve the full report's supplied-object/runtime limits. Original behavior target: Result persistence; uncertainty: Native file path/durability/migrations/online submission unproved.
- Production at `ab349d441dfa02f3c1ff97d6d0b8837c6ebb8f0e`: `reconstructed/core/../godot/Main.cs`. Diagnostic logs do not implement best-score/clear persistence.
- Tests/reference coverage: `reference_traces/r001/`, corresponding `reconstructed/validation/R001.md` and core/bridge/Godot development suites. Expectations and execution described there are Work2 provenance; **independent exact-SHA QA NOT RUN / NOT ESTABLISHED**.
- Dependencies/discrepancy: Result, chart identity, DB/config; **D13**, see [dependency register](dependency-register.md) and [discrepancy register](discrepancy-register.md).
- Closure/owner requirement: independently derive event-level expected results from the cited original source, exercise supported and rejected boundaries plus this feature in a mixed chart; owner qualifies visible targets, physical input/audio where relevant, completion and replay on final Windows corpus. Prior isolated checkpoint approval alone cannot close this row.
- Remaining work/priority/actor: W2-03; P0 for scope/blocker decisions or critical chart/contact dependencies, P1 implementation/QA, P2 exact fidelity after functional equivalence. Work 2 own storage with explicit schema; strict score improvement, independent clear comparator is historical advice, not authorization. No new execution starts in A01.

## S01-15.03 — Mirror and chart modifiers

- Applicability/status: **H; OPEN**. H is a decision gate, not exclusion; platform/artwork may be external only if S01 behavior remains functional.
- Required original/evidence: E006 ability mirror+3b reaches loader `0x16e67a4`; E010 chart+cd/inclusion/metadata flag consumers. Historical confidence: **IB producer chain; NI ordinary nonmatching defaults**; preserve the full report's supplied-object/runtime limits. Original behavior target: Mirror and chart modifiers; uncertainty: Complete original mirror and special modifier behavior not independently joined.
- Production at `ab349d441dfa02f3c1ff97d6d0b8837c6ebb8f0e`: `reconstructed/core/Chart.cs`, `Kernel.cs`, Godot frontend. No complete implementation found in inspected core/frontend. Absent at Scout003 is historical only; current restrictions do not supply this missing behavior.
- Tests/reference coverage: No direct production-native reference established for this full requirement; historical native fixtures remain reusable. Expectations and execution described there are Work2 provenance; **independent exact-SHA QA NOT RUN / NOT ESTABLISHED**.
- Dependencies/discrepancy: Ability/config, chart construction, coordinates; **D08**, see [dependency register](dependency-register.md) and [discrepancy register](discrepancy-register.md).
- Closure/owner requirement: independently derive event-level expected results from the cited original source, exercise supported and rejected boundaries plus this feature in a mixed chart; owner qualifies visible targets, physical input/audio where relevant, completion and replay on final Windows corpus. Prior isolated checkpoint approval alone cannot close this row.
- Remaining work/priority/actor: HQ-01; P0 for scope/blocker decisions or critical chart/contact dependencies, P1 implementation/QA, P2 exact fidelity after functional equivalence. Keep plain ordinary mode; bound a separate modifier milestone before claiming compatibility, with one producer/coordinate comparison if requested is historical advice, not authorization. No new execution starts in A01.

## S01-12.06 — Configuration/preferences

- Applicability/status: **M; OPEN — partial implemented profile; historical VERIFIED COMPONENT only**. H is a decision gate, not exclusion; platform/artwork may be external only if S01 behavior remains functional.
- Required original/evidence: E010 speed selection; E040 loader/migration/profile. Historical confidence: **NI settings→Model under backend facade**; preserve the full report's supplied-object/runtime limits. Original behavior target: Configuration/preferences; uncertainty: Real persisted preferences backend/route auto-selection absent.
- Production at `ab349d441dfa02f3c1ff97d6d0b8837c6ebb8f0e`: `reconstructed/core/../godot/bridge/GameplaySession.cs`. Supplied profile values; persistent general settings/backend migration coverage incomplete.
- Tests/reference coverage: `reference_traces/r005/`, corresponding `reconstructed/validation/R005.md` and core/bridge/Godot development suites. Expectations and execution described there are Work2 provenance; **independent exact-SHA QA NOT RUN / NOT ESTABLISHED**.
- Dependencies/discrepancy: Config backend, chart, Timeline; **D11**, see [dependency register](dependency-register.md) and [discrepancy register](discrepancy-register.md).
- Closure/owner requirement: independently derive event-level expected results from the cited original source, exercise supported and rejected boundaries plus this feature in a mixed chart; owner qualifies visible targets, physical input/audio where relevant, completion and replay on final Windows corpus. Prior isolated checkpoint approval alone cannot close this row.
- Remaining work/priority/actor: W2-03; P0 for scope/blocker decisions or critical chart/contact dependencies, P1 implementation/QA, P2 exact fidelity after functional equivalence. Work 2 persist own settings and propagate explicit values; keep backend substitution visible is historical advice, not authorization. No new execution starts in A01.

## S01-12.07 — Offset calibration and device compensation

- Applicability/status: **H; OPEN**. H is a decision gate, not exclusion; platform/artwork may be external only if S01 behavior remains functional.
- Required original/evidence: E005 calibration lambda `0x192410c`: M+T−N−expected beat; provider output-property JNI `0x3cc90` in separate FMOD ELF. Historical confidence: **IB traced consumers; NX arithmetic; UN physical calibration accuracy**; preserve the full report's supplied-object/runtime limits. Original behavior target: Offset calibration and device compensation; uncertainty: No measured sensor/output latency or gameplay queue-age correction.
- Production at `ab349d441dfa02f3c1ff97d6d0b8837c6ebb8f0e`: `reconstructed/core/Chart.cs`, `Kernel.cs`, Godot frontend. No complete implementation found in inspected core/frontend. Absent at Scout003 is historical only; current restrictions do not supply this missing behavior.
- Tests/reference coverage: No direct production-native reference established for this full requirement; historical native fixtures remain reusable. Expectations and execution described there are Work2 provenance; **independent exact-SHA QA NOT RUN / NOT ESTABLISHED**.
- Dependencies/discrepancy: Audio position, Java timestamp age, settings UI; **D13**, see [dependency register](dependency-register.md) and [discrepancy register](discrepancy-register.md).
- Closure/owner requirement: independently derive event-level expected results from the cited original source, exercise supported and rejected boundaries plus this feature in a mixed chart; owner qualifies visible targets, physical input/audio where relevant, completion and replay on final Windows corpus. Prior isolated checkpoint approval alone cannot close this row.
- Remaining work/priority/actor: W2-03; P0 for scope/blocker decisions or critical chart/contact dependencies, P1 implementation/QA, P2 exact fidelity after functional equivalence. Work 2 may add a declared calibration tool; do not copy timestamp-age correction into normal judgment or invent buffer-size latency compensation is historical advice, not authorization. No new execution starts in A01.

## S01-16.01 — Android transport/device behavior

- Applicability/status: **H; OPEN**. H is a decision gate, not exclusion; platform/artwork may be external only if S01 behavior remains functional.
- Required original/evidence: E004/E011/E012 smali, JNI and lifecycle CPU tests. Historical confidence: **IB Java; NI native delivery; UN real platform queue**; preserve the full report's supplied-object/runtime limits. Original behavior target: Android transport/device behavior; uncertainty: Platform implementation absent from archive.
- Production at `ab349d441dfa02f3c1ff97d6d0b8837c6ebb8f0e`: `reconstructed/core/Chart.cs`, `Kernel.cs`, Godot frontend. No complete implementation found in inspected core/frontend. Absent, desktop adapter only at Scout003 is historical only; current restrictions do not supply this missing behavior.
- Tests/reference coverage: No direct production-native reference established for this full requirement; historical native fixtures remain reusable. Expectations and execution described there are Work2 provenance; **independent exact-SHA QA NOT RUN / NOT ESTABLISHED**.
- Dependencies/discrepancy: Android VM/GLThread, device clocks/input/audio; **D13**, see [dependency register](dependency-register.md) and [discrepancy register](discrepancy-register.md).
- Closure/owner requirement: independently derive event-level expected results from the cited original source, exercise supported and rejected boundaries plus this feature in a mixed chart; owner qualifies visible targets, physical input/audio where relevant, completion and replay on final Windows corpus. Prior isolated checkpoint approval alone cannot close this row.
- Remaining work/priority/actor: W2-03; P0 for scope/blocker decisions or critical chart/contact dependencies, P1 implementation/QA, P2 exact fidelity after functional equivalence. P09 requires separate platform authority; desktop reconstruction need not wait is historical advice, not authorization. No new execution starts in A01.

## S01-15.04 — Remote submission/progression/special scenes

- Applicability/status: **H; OPEN**. H is a decision gate, not exclusion; platform/artwork may be external only if S01 behavior remains functional.
- Required original/evidence: E006/E013 queue/pending `0x1246c98`; supplied in E024; E042 local saves only. Historical confidence: **IB limited serialization; UN full online lifecycle**; preserve the full report's supplied-object/runtime limits. Original behavior target: Remote submission/progression/special scenes; uncertainty: No complete authorization/delivery/persistence proof.
- Production at `ab349d441dfa02f3c1ff97d6d0b8837c6ebb8f0e`: `reconstructed/core/Chart.cs`, `Kernel.cs`, Godot frontend. No complete implementation found in inspected core/frontend. Absent at Scout003 is historical only; current restrictions do not supply this missing behavior.
- Tests/reference coverage: No direct production-native reference established for this full requirement; historical native fixtures remain reusable. Expectations and execution described there are Work2 provenance; **independent exact-SHA QA NOT RUN / NOT ESTABLISHED**.
- Dependencies/discrepancy: Account, network, special contexts, backend; **D13**, see [dependency register](dependency-register.md) and [discrepancy register](discrepancy-register.md).
- Closure/owner requirement: independently derive event-level expected results from the cited original source, exercise supported and rejected boundaries plus this feature in a mixed chart; owner qualifies visible targets, physical input/audio where relevant, completion and replay on final Windows corpus. Prior isolated checkpoint approval alone cannot close this row.
- Remaining work/priority/actor: W2-03; P0 for scope/blocker decisions or critical chart/contact dependencies, P1 implementation/QA, P2 exact fidelity after functional equivalence. Keep outside ordinary milestones; no online experiment authorized is historical advice, not authorization. No new execution starts in A01.

## Additional inventory and closure requirements

### S01-11.90 — Accuracy definition
Normal score, PURE/FAR/LOST, shining and combo are separate quantities. A distinct percentage accuracy display/formula is NOT VERIFIED from the inspected original evidence. Work1 must identify the actual original consumer or Headquarters must approve the exact UI meaning. Do not import osu!/community arithmetic. D09; W1-02; OPEN.

### S01-14.90 — Realistic integrated acceptance corpus
MANDATORY; OPEN. Prepare independently authored permitted synthetic charts covering long sessions, changing tempos, curves, links, children, chords, holds, multi-contact contention, reverse/noinput groups, widening, audio offsets, pause/cancel/reacquisition and completion/replay. Include mixed interactions rather than concatenating only isolated successful checkpoints. Every fixture needs raw bytes/hash, normalized typed objects, unit/end accounting, event ledger, f32/rounding expectations, expected failures and ownership lifecycle. Final Windows owner scenarios must cover keyboard ground plus adequate simultaneous sky input. Dependencies: all mandatory rows and applicability decisions; D10/D13.

### S01-16.90 — Independent verification and final acceptance
MANDATORY; OPEN. Work1 must run production at exact SHA against independently established expectations; compare intermediate candidate order, IDs, record weights/resolution, gauge bits, clock, score/result and cleanup, preserving historical suites. Work2 must build/export resources and report exact commands/results/artifacts. Owner then qualifies the integrated corpus; Headquarters records G1–G8 disposition. Neither this source audit nor449 development groups closes this requirement.

### Campaign-boundary decisions
HQ-01 must classify characters/gauges/mirror, special chart permissions, flick applicability, accuracy UI, configuration/local records, exact native outro, platform capacity and native artistic fidelity. Native Android queue/hardware and online progression may be separate engineering/platform campaigns; their functional dependencies on accepted S01 scope must be recorded. No exclusions are approved here. All16 provisional domains map to children above or S01-16.90.


## W1-01 preparation update — 2026-11-15

Independent corpus/driver prepared:50 scenarios,38 RUNNABLE specifications,8 EXPECTED REJECTION,4 RESEARCH BLOCKED. Actual source/checksum preflight exit2/BLOCKED: SDK10.x absent; Godot4.6.3 standard does not satisfy4.7.2.NET. No production test executed; no requirement upgraded to INDEPENDENTLY VERIFIED. W1-01-B01/B02 must be resolved before baseline verification. G006/007/009/010 and D01–D16 unchanged. See [W1-01-report.md](W1-01-report.md). S01 OPEN.


## W1-01-C01 executed CLI checkpoint — 2026-11-16

Pinned production ab349d441dfa02f3c1ff97d6d0b8837c6ebb8f0e now independently executed:38 baseline+8 rejection cases pass,0fail/skip; repeat byte-identical. Four producer-blocked cases remain NOT VERIFIED. Official SDK10.0.402/runtime10.0.13 plus reference pack2.1.0 installed in isolated workspace. Historical13 CLI suites319checks and three standalone comparisons pass separately with Work2 provenance. See [W1-01-C01-report.md](W1-01-C01-report.md) and results/c01/receipt.json. Only asserted fields in this bounded corpus gain independent verification; broad requirement statuses remain OPEN. W1-01-B01 recovered for CLI; Godot4.7.2.NET is not needed for this driver. G006/007/009/010, D01–D16 completeness gaps remain. Next recommendation: authorized coherent Work2 W2-01 integration plus Work1 graph/child reference closure. No implementation begun; S01 OPEN.
