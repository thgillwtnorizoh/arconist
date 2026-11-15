# A01 — Independent normal gameplay completeness audit

## UEP-001 checkpoint

- Project / Campaign / Actor / Assignment: Arconist / S01 Normal Gameplay / Work1 / A01, issue #2.
- Status: VERIFIED CHECKPOINT for source-grounded documentation; subsystem remains OPEN.
- Starting SHA: `618fb55dc987c9bc4b172c5d7038b8b4bfae4b21`, identical to remote main at start.
- Published SHA: supplied in final handoff; publication changes documentation only.
- Exact production assessed: `ab349d441dfa02f3c1ff97d6d0b8837c6ebb8f0e`. R010 publication `1274b60d56cf20f95c3c354f362d779eb566268b` and supplied start are descendants. Exact independently runtime-tested SHA: NONE / NOT RUN in A01.
- Objective/profile: inventory all normal solo requirements against R010 Windows/Godot/C# engineering profile without narrowing scope to its supported fixtures. Functional changes: none. Integrations inspected: parser→groups/depth→contacts/geometry→recorders/results, bridge/audio/modal and frontend rendering/input.
- Evidence/confidence: original evidence retains native-integrated, native-isolated, instruction-backed, inferred, blocked and unknown labels. Current source findings are static inspection; historical VERIFIED COMPONENT tests are Work2 development evidence. No A01 production row is INDEPENDENTLY VERIFIED. ENGINEERING substitutions and DISCREPANCY entries remain explicit; fresh Windows runtime is UNVERIFIED RUNTIME by Work1.
- Tests: documentation/source/ancestry/preservation checks only; see validation below. Runtime, build, CI and new native experiments NOT RUN. No new CI or artifact build is claimed.
- Coverage gained: audited61 inherited original feature requirements plus accuracy, final corpus and independent acceptance requirements; all16 provisional domains retained. Remaining: implementation breadth, interaction QA, blocked applicability/producer paths, final integrated owner acceptance.
- Discrepancies/blockers: D01–D16; G006/007/009/010 remain unresolved, never automatically excluded.
- Updated records: coverage-register.md, dependency-register.md, discrepancy-register.md, this report; append-only reconstructed/contexts.md.
- Next bounded task: HQ-01 applicability decisions and Work1 W1-01 independent baseline/corpus; Work2 W2-01 integration may be authorized against sufficiently established evidence. No R011 automatically selected.
- Subsystem: **OPEN**.

## Source identity and method

Verified GitHub main through connected GitHub API, cloned current repository and checked ancestry to the supplied tested/publication SHAs. The only paths differing from tested R010 to starting main are campaign README, coverage register, reconstruction history and R010 validation documentation; production core/bridge/frontend/tests/reference bytes are identical. Consequently implementation findings apply to the exact tested R010 production as well as the audited head.

Read permanent instructions, complete campaign charter/provisional register, reconstruction history and R001–R010 validation findings. Inspected actual Chart.cs, TimingGroup.cs, Arc.cs, ArcTap.cs, LinkedArc.cs, Kernel.cs, GameplaySession.cs, BgmController.cs, Main.cs and SpatialTrack.cs; checked existing core/bridge/headless suites, native-normalized reference directories and original fixture/report links. Reused Scout003's preserved61-feature original inventory and its E001–E042/030-R evidence ledger, reconciled against current backlog/context and changed implementation. Historical original research is not reclassified as new native execution. A01 does not re-open the original archive to answer every unknown.

Original archive identity used by this research chain: main ARM64 library SHA256 `3eaca4e6dabb3395f276f8915698d57675757d0df0970e716b23a3dc201c79be`, Build ID `17d660edbf37ca78beefc32e07672c97419ddce6`. No fresh ARM64 execution is claimed. Attached project introduction preserves the English/evidence/preservation remit. Proprietary source bytes are not published.

## Findings and closure matrix

The complete per-requirement findings are in [coverage-register.md](coverage-register.md); dependencies/execution acceptance are in [dependency-register.md](dependency-register.md), differences and historical conflicts in [discrepancy-register.md](discrepancy-register.md).

| Area | Implemented bounded component | Required remaining closure |
|---|---|---|
| AFF/runtime | Typed notes, positive timing, one extra tap group | Native-compatible required forms, group counts/attributes and mixed group objects; no assumption every malformed-native behavior is desirable |
| Holds/taps | Latch/activity separation, chronological blocking, reacquisition and per-unit scoring | Independent mixed-chart production QA and valid variants beyond authored fixtures |
| Arcs | Linear sampled geometry/ownership; exact constant linked pair | Curves, tempo/group variants, crossing bypass, generalized links and real group window semantics |
| Arc-taps | One child on trace parent | Multiple children, ordinary-parent applicability, mixed/conflict ordering instead of240ms rejection |
| Input | Managed IDs, MOVE/UP/CANCEL, ground/sky rays | General simultaneous sky inputs, equal-key/type contention and shared widening geometry |
| Timing groups | Restricted E029/E036 tap paths | Multiple mixed-note groups, general reverse/noinput and required stop/attribute semantics; zero BPM applicability needs original evidence |
| Controls | Default camera and geometric substitutes | E039 missing gameplay widening; permission-gated camera/reset/fade/hide/angles need applicability and producer dispositions |
| Score/gauge/results | Ordinary default counters/gain/result cache | Independent event-level verification; accuracy definition and character/gauge dependencies cannot be guessed |
| Audio/lifecycle | BGM request/seek/pause contract and explicit modal resume | SFX/calibration/required seek/configuration breadth, final mixed-chart audible qualification and backend errors |
| Session/presentation | Bundled18 chart choices, placeholder visuals/results/replay | Representative realistic corpus, complete supported data/resource preparation, perception/input alignment and final session qualification |
| Flick/characters | No production support | G009/G010 remain OPEN scope/producer blockers, not exclusions |

The largest critical-path limitation is combinatorial compatibility: the grouped parser rejects holds/arcs entirely, trace parents reject multiple/ordinary children, arc code accepts only s/none and restricts timing, and nearby arcs must satisfy the single constant-pair linker. Passing each checkpoint does not make these compatible within one ordinary chart.

Source-confirmed crossing gap: original E028 cache/proximity path can bypass color ownership; production Claim only supports exclusive owner/claimed-ID logic and lacks that bypass producer. This is already researched behavior, so Work2 should not commission another generic crossing expedition before implementing it.

Separate missing behavior from missing fidelity. Curves/cache/ownership, timing/noinput/unit accounting, G/W lane selection, modal recovery and visible reachable targets are functional semantics. Original textures, particles and shutter artwork can be separate only with a recorded decision that perception/play is preserved. Hidegroup is not noinput. Identical sampled camera matrices in E039 do not make widening cosmetic.

## Existing validation provenance

R001–R010 reports preserve development tests and technical package evidence. R010 reports449 groups (395 prior+29 core+11 bridge+14 Godot), three9/6/6-event native-normalized standalone comparisons, zero failures/skips and47 command exits0 at tested SHA ab349d4. These counts were not reproduced by A01 and are not independent Work1 QA. Reference JSONs were transcribed from original evidence and consumed by Work2 tests; their original-derived expectations do not change the authorship of the test execution.

R010's initial deferred diagnostic snapshots were repaired by materialization; later serialized-evidence assertions passed according to Work2. Preserve both failed evidence and corrected test source; no production kernel divergence is asserted from that reporting error.

Reconstruction history records owner R010 qualification of six specified scenarios and R001–R009 acceptance. A01 preserves that authority; it does not rerun or expand owner acceptance. The campaign charter explicitly requires a later whole-S01 corpus/owner gate.

## Validation commands and limits

Actual commands include `git clone`, GitHub branches/main fetch, `git merge-base --is-ancestor ab349d441dfa02f3c1ff97d6d0b8837c6ebb8f0e HEAD`, `git diff --name-only ab349d441dfa02f3c1ff97d6d0b8837c6ebb8f0e HEAD`, source/report reads with rg/Python, and document/prefix/tree validation. Publication verification checks immutable remote tree/content and expected main head without force. Final handoff records counts and final SHA.

Environment: Linux shell and Python3; `command -v dotnet` returned no installed tool. No toolchain installation was needed for source audit. C#/Godot build/regression, native emulator scenarios, Windows export/launch, audio-output measurements, OS input injection, automated screenshot/GUI qualification and new native experiments: **NOT RUN**. No runtime pass count is invented. Initial large shell read outputs were truncated; narrower source sections and direct structured file processing were used for audit generation/checking rather than treating missing output as tested behavior.

Mandatory document checks: all relative links resolve; all61 original feature rows retained with stable domain children; all16 parent domains have coverage; all discrepancy and follow-up IDs resolve; every protected parent file remains identical; reconstruction history old bytes are an exact prefix. Coverage of tests beyond the declared fixtures remains NOT VERIFIED until W1-01.

## Publication and stop

Exactly five authorized paths change: four campaign documents (coverage replacement, dependency/discrepancy/audit additions) and reconstruction history append. Campaign charter, root context/backlog, original reports, all production, tests, fixtures, reference JSONs and earlier validation reports remain untouched. No issue comment/message is sent. GitHub publication is a normal child commit with expected-head guard and remote readback. Exact publication SHA is in the final handoff because it cannot be embedded into its own commit.

Stop after this documentation checkpoint. No new expedition, implementation, Unity or subsystem acceptance follows. **S01 OPEN.**

## Focused test-source inventory

- `reconstructed/arc-bridge-tests/Program.cs`: source inspected for test names/reference assertions and explicit supported/rejected profiles; execution NOT RUN.
- `reconstructed/arc-tests/Program.cs`: source inspected for test names/reference assertions and explicit supported/rejected profiles; execution NOT RUN.
- `reconstructed/arctap-bridge-tests/Program.cs`: source inspected for test names/reference assertions and explicit supported/rejected profiles; execution NOT RUN.
- `reconstructed/arctap-tests/Program.cs`: source inspected for test names/reference assertions and explicit supported/rejected profiles; execution NOT RUN.
- `reconstructed/audio-tests/Program.cs`: source inspected for test names/reference assertions and explicit supported/rejected profiles; execution NOT RUN.
- `reconstructed/group-bridge-tests/Program.cs`: source inspected for test names/reference assertions and explicit supported/rejected profiles; execution NOT RUN.
- `reconstructed/group-tests/Program.cs`: source inspected for test names/reference assertions and explicit supported/rejected profiles; execution NOT RUN.
- `reconstructed/hold-tests/Program.cs`: source inspected for test names/reference assertions and explicit supported/rejected profiles; execution NOT RUN.
- `reconstructed/linked-bridge-tests/Program.cs`: source inspected for test names/reference assertions and explicit supported/rejected profiles; execution NOT RUN.
- `reconstructed/linked-tests/Program.cs`: source inspected for test names/reference assertions and explicit supported/rejected profiles; execution NOT RUN.
- `reconstructed/pause-tests/Program.cs`: source inspected for test names/reference assertions and explicit supported/rejected profiles; execution NOT RUN.
- `reconstructed/tests/Program.cs`: source inspected for test names/reference assertions and explicit supported/rejected profiles; execution NOT RUN.
- [r001 reference provenance](../../../reference_traces/r001/README.md): original normalization and fixture boundaries retained.
- [r004 reference provenance](../../../reference_traces/r004/README.md): original normalization and fixture boundaries retained.
- [r005 reference provenance](../../../reference_traces/r005/README.md): original normalization and fixture boundaries retained.
- [r006 reference provenance](../../../reference_traces/r006/README.md): original normalization and fixture boundaries retained.
- [r007 reference provenance](../../../reference_traces/r007/README.md): original normalization and fixture boundaries retained.
- [r008 reference provenance](../../../reference_traces/r008/README.md): original normalization and fixture boundaries retained.
- [r009 reference provenance](../../../reference_traces/r009/README.md): original normalization and fixture boundaries retained.
- [r010 reference provenance](../../../reference_traces/r010/README.md): original normalization and fixture boundaries retained.

Audit tooling failures retained: initial history append used a non-ASCII bytes literal and failed before mutation; repaired using UTF-8 encoding. First link check found an over-deep Scout relative link; corrected and checks rerun. Neither failure altered production or earlier history.
