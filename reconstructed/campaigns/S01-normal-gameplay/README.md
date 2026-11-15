# S01 — Normal Gameplay Completeness Campaign

**Project:** Project Arconist — https://github.com/thgillwtnorizoh/arconist  
**Authority:** Headquarters / Owner, UEP-001 Revision 2.1 (November 2026)  
**Campaign:** S01 — Normal Gameplay  
**Status:** **OPEN**; no subsystem-level acceptance  
**Baseline for campaign initiation:** `1274b60d56cf20f95c3c354f362d779eb566268b` (R010 published main)  
**Historical checkpoints:** R001–R010 owner-accepted for their **declared bounded profiles**.  
**Next assignment:** Work 1 independent completion and coverage audit (see repository issue).  
**R011:** NOT AUTHORIZED by this charter.

## 1. Acceptance unit and objective

**S01, not an individual R-series execution, is the unit of completion.** Reconstruct the original game's **normal solo gameplay** as one integrated, genuinely playable subsystem. Completing a tap, arc, timing-group, or other bounded implementation is a *checkpoint* and does **not** close S01.

The intended outcome includes ordinary chart interpretation and runtime construction; all gameplay mechanics applicable to normal play; judgment, contact lifecycle and arbitration; timing/depth and chart controls; audio and offsets; ordinary gauge/score/results; pause/resume/replay; and the presentation required to perceive and perform gameplay correctly.

**Do not manufacture stage completion by restricting the supported features to existing test fixtures.** Work 1 must establish a source-grounded inventory of what normal gameplay actually requires. Features with unresolved original applicability remain OPEN for a Headquarters scope decision, not silently excluded.

The initial execution environment is the existing independently judged C# core with Godot Windows x64 qualification. This is an *engineering platform profile*, not a claim of Android hardware, original GPU, FMOD, online/account or full UI equivalence. The owner must approve any exclusion of a mechanic genuinely necessary for normal gameplay. Other campaigns may own artistic fidelity, menus, characters or platform services, but a needed gameplay dependency cannot disappear merely because it crosses a campaign boundary.

## 2. Roles and evidence

- **Headquarters:** decides stage boundaries, priority, unresolved discrepancy disposition, resource assignments, release acceptance and material scope changes.
- **Work 1 (original research and independent QA):** inventories original behavior, identifies producers/consumers/fixtures and gaps, develops independently established expected results, later checks Work 2 production at the **exact tested SHA**. Do not accept Work 2-generated output as an independent oracle.
- **Work 2 (implementation):** develops integrated behavior, C# development tests, Godot integration, builds, validated Windows packages and exact published checkpoints.
- **Owner:** physically qualifies Windows rendering, input, audio, results/replay and the eventual complete S01 scenario corpus; alone authorizes S01 final acceptance.

Evidence labels: CONFIRMED ORIGINAL (original executed), RECONSTRUCTED (interpretation), VERIFIED COMPONENT (tested production), INDEPENDENTLY VERIFIED (separate expectations/tests on production), ENGINEERING (explicit platform/design choice), UNVERIFIED RUNTIME, DISCREPANCY. Historical research also distinguishes native-integrated, native-isolated, instruction-backed, inferred, blocked and unknown. Preserve original provenance.

R001–R010's 449 reported development groups and prior owner qualifications remain valid **within their bounded checkpoints**. They are neither discarded nor retroactively relabeled independent subsystem QA.

## 3. Coverage and dependency control

The campaign's coverage register is `coverage-register.md`. Every applicable requirement must have:

1. Stable ID and original behavior / normal-play applicability.
2. Original source (Expedition/Scout/fixture and confidence, or explicitly missing).
3. Production source/commit and implemented profile.
4. Dependency and unresolved discrepancy, including cross-domain interactions.
5. Independent QA fixture/test, exact tested SHA and result.
6. Required Windows/human scenarios and qualification.
7. Status: OPEN, BLOCKED, VERIFIED COMPONENT, INDEPENDENTLY VERIFIED, or OWNER-APPROVED EXCLUSION (with explicit decision and rationale).

The register begins with **provisional** categories. Work 1 must independently reconcile them against Scout 003, the research backlog (including G-006/007/009/010), E001–E042, and current R010 production code. Do not mistake a research gate marked Verified for a fully reconstructed original feature.

Use one targeted research experiment only when an actual S01 requirement is blocked by missing original behavior. Reuse existing evidence before starting another native expedition. Preserve independent expectations and all historical tests.

## 4. S01 closure gates — all mandatory

S01 may be marked **OWNER-ACCEPTED** only when all of these conditions are met:

**G1 — Scope:** Headquarters approves a complete source-grounded normal-play requirement inventory and explicit compatibility profile; unresolved applicability and material exclusions have owner decisions.

**G2 — Coverage:** Every mandatory normal-play requirement and supported interaction is implemented and integrated, with no unapproved required gap or blocker.

**G3 — Evidence:** Original/reconstructed/engineering provenance and discrepancy decisions are recorded. No static analysis or fitted output is promoted to native runtime equivalence.

**G4 — Development verification:** Full historical regression preserved, new focused integration/corpus tests pass, exact commands/environments/exit counts/SHAs recorded; no silent skips.

**G5 — Independent verification:** Work 1 validates exact Work 2 production from independent original-derived expectations, identifies first differences and resolves or documents approved discrepancies.

**G6 — Delivery and runtime:** Actual Windows export, resource and package integrity, chart/audio integration, suitable representative gameplay corpus, and physical owner qualification pass. Prior per-feature qualifications are not a substitute for the final integrated S01 qualification.

**G7 — Publication:** Recovery state, coverage, dependency/discrepancy registers, fixture provenance, source SHAs, logs and limitations published non-destructively, with no unrelated files or original proprietary archive/assets added.

**G8 — Owner decision:** Explicit Headquarters/Owner acceptance after review. Until then: **S01 OPEN**.

## 5. Execution rules

Campaign S01 can have as many bounded executions as required. An execution ends at **VERIFIED CHECKPOINT**, **BLOCKED**, or **FAILED**, and is never represented as whole-stage completion by itself. Use the mandatory UEP-001 checkpoint report template, preserving starting/published/exact tested SHAs, confidence levels, commands, failures/not-run, gained coverage, remaining requirements, reproductions, and next dependency.

Old R001–R010 reports and previous bytes of `reconstructed/contexts.md` must remain intact. Append the owner's R010 acceptance and this S01 transition to reconstruction history. Never force-push.

**Next bounded task:** Work 1 audits R010 production against the original normal-play feature inventory and publishes a complete, independently sourced S01 coverage/dependency/discrepancy register with priority recommendations. The audit is *not* authorization to implement R011, rewrite research, start a new native experiment or declare S01 complete.

**Subsystem: OPEN.**
