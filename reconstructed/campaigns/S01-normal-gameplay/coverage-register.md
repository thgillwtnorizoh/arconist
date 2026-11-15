# S01 — Provisional Normal Gameplay Coverage Register

**Owner:** Headquarters (provisional domain inventory); **next verifier:** Work 1  
**Campaign:** S01 — Normal Gameplay  
**Campaign baseline:** `1274b60d56cf20f95c3c354f362d779eb566268b` (R010)  
**Status:** **OPEN — NOT AN AUDIT PASS; NOT A COMPLETE ORIGINAL FEATURE INVENTORY**  
**Method:** UEP-001 Rev 2.1. Existing R-series acceptance is bounded and preserved.

## Meaning of the fields

This is an **initial routing register**, not evidence that the complete source has been independently audited. Every row remains OPEN until Work 1 establishes original applicability, scope, source confidence, exact production state and independent QA. *Checkpoint accepted* means only that the historical bounded R-series owner qualification was reported successful. Do not infer full feature coverage from it.

Allowed component conclusions: VERIFIED COMPONENT, INDEPENDENTLY VERIFIED, BLOCKED, OPEN, and OWNER-APPROVED EXCLUSION. An exclusion needs an explicit Headquarters decision. A research backlog item marked "Verified" does not automatically mean the reconstruction implements it.

| ID | Normal-play domain / outstanding completeness question | Existing sources to verify | Historical reconstruction checkpoints / concern | Original applicability & coverage | Independent QA at production SHA |
|---|---|---|---|---|---|
| S01-01 | AFF grammar, chart object construction, grouping, source ordering, supported ordinary data | E002, E010, E029, E036 | R001–R010 use bounded typed syntax; broad grammar unverified | OPEN — Work 1 inventory required | NOT ESTABLISHED |
| S01-02 | Ordinary taps, simultaneous chords and initial judgment ordering | E002, E004, E024, E027, E035 | R001–R004; bounded chord/conflict cases | OPEN — Work 1 inventory required | NOT ESTABLISHED |
| S01-03 | Ordinary holds: checkpoints, input latch/activity, release/reacquisition, timing edges | E001, E026, E037, E041 | R004/R006 accepted within subsets | OPEN — Work 1 inventory required | NOT ESTABLISHED |
| S01-04 | Ordinary arcs: linear/curved geometry, continuous judgment, moving and crossing colors | E003, E009, E028, E038 | R007/R009 restricted linear profiles; broader curve/overlap cases remain | OPEN — Work 1 inventory required | NOT ESTABLISHED |
| S01-05 | Arc-tap parent/child construction, multiple children, spatial/timing and mixed arbitration | E004, E025 | R008 single trace parent/child bounded profile | OPEN — Work 1 inventory required | NOT ESTABLISHED |
| S01-06 | Flick producer and gesture; decide whether applicable to normal play | E009, E033, G-009 | Native producer BLOCKED; no R-series implementation | OPEN — applicability unresolved | NOT ESTABLISHED |
| S01-07 | Per-group timing, negative BPM, reverse/stop, noinput and group attributes | E007, E010, E029, E036 | R010 one extra tap-only group; general cases remain | OPEN — Work 1 inventory required | NOT ESTABLISHED |
| S01-08 | Gameplay scene controls, lane widening, primary/secondary input geometry | E004, E039, G-015 | No R011 authorized; widening missing | OPEN — Work 1 inventory required | NOT ESTABLISHED |
| S01-09 | Gameplay-impacting camera/reset/fade controls, projection and visibility | E007, E030/030-R, E031/032, G-006/007 | Original producer/control paths BLOCKED in parts; cannot dismiss gameplay effects as cosmetic | OPEN — applicability/dependencies unresolved | NOT ESTABLISHED |
| S01-10 | Contact input identity, MOVE, UP/CANCEL, contention, priority, multispatial interaction | E004, E011, E027, E028, E035, E037, E041 | R003–R009 support subsets; generalized mixed conflicts pending | OPEN — Work 1 inventory required | NOT ESTABLISHED |
| S01-11 | Judgment, units/weights, miss/expiry, FAR/PURE, score/combo/max/health/failure | E006, E009, E026, E036, E038, E042 | R001–R010 tested scenarios; broader ordinary interactions need audit | OPEN — Work 1 inventory required | NOT ESTABLISHED |
| S01-12 | Audio timeline, start/offset, pause/resume, seek/focus and physical synchronization | E005, E012, E040–E041 | R005–R006 owner-tested; original FMOD/device latency not equivalent | OPEN — Work 1 inventory required | NOT ESTABLISHED |
| S01-13 | Gameplay-critical track/notes/HUD/projection/feedback and real input alignment | E003, E007, E032 and renderer evidence | Godot functional placeholders; artistic fidelity separate only if it does not affect play | OPEN — boundary approval required | NOT ESTABLISHED |
| S01-14 | Chart results/replay, session cleanup, realistic mixed-chart corpus and end-to-end use | E008–E010, E036, E042 | R001–R010 contain many small practice charts; no full S01 acceptance corpus | OPEN — Work 1 inventory required | NOT ESTABLISHED |
| S01-15 | Character/special gauge/chart effects that change *ordinary* normal gameplay | E006, E034, G-010 | Special 6/11 producer blocked; applicability vs later campaign unresolved | OPEN — owner classification required | NOT ESTABLISHED |
| S01-16 | Independent production QA, platform qualification, publication and owner S01 acceptance | E001–E042, R001–R010 validation and owner decisions | 449 groups reported R010; no stage-wide independent QA established | OPEN — requirements not satisfied | NOT ESTABLISHED |

## Work 1 completion requirements

For **every** row (split into finer requirements as necessary), publish an audited register recording:

- Requirement ID, whether genuinely required for ordinary solo gameplay, source-grounded behavior and compatibility conditions; unknowns remain OPEN, not excluded.
- Original source report, exact function/fixture and native-integrated vs isolated/instruction-backed/inferred/unknown classification.
- Current production file and method, **exact SHA**, supported/rejected behavior and confirmed missing integration; no speculation presented as implemented.
- Previous test/fixture and expected vs observed status, provenance/independence; missing tests explicitly NOT RUN.
- Human/Windows requirements, independent QA criteria and realistic cross-mechanic corpus cases.
- Dependency edges, discrepancy first-difference and blocker IDs (G-series when relevant), confidence, responsible actor and next bounded task.

Maintain a dependency register and discrepancy register in this campaign directory, or clearly linked distinct sections of the audited coverage register. Preserve histories of known observations and corrections rather than overwriting inconvenient evidence.

Do **not** report this provisional register as a completed audit. A new source-grounded Work 1 report and repository publication are required before Headquarters prioritizes the next reconstruction implementation checkpoint.

**S01: OPEN. R011: NOT AUTHORIZED.**
