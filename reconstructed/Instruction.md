# Permanent reconstruction instructions

Authority: Headquarters, Project Arconist Reconstruction R001, received 2026-11-05.

Every reconstruction mission MUST define and achieve its minimum operational goal.
PASS requires the mandatory deliverable, successful build, actual execution, required
functionality, every mandatory acceptance test, reproducible evidence, and delivery
for independent inspection. Compilation, a mock, documentation, partial tests or a
matching final score alone cannot establish PASS. Any unmet mandatory condition is
FAIL. Never weaken acceptance after failure without explicit Headquarters authority;
never fabricate outputs, silently skip tests, delete assertions or weaken comparisons.
Preserve partial work and diagnostics on failure and state exact remaining blockers.
Headquarters alone accepts a milestone and authorizes progression.

Before future reconstruction work, read this file and contexts.md IN FULL.
contexts.md is append-only: record decisions, provenance, actual test evidence and
unresolved discrepancies. Original context.md, backlog, excavations, fixtures and
native harness are research authority; preserve them. Distinguish native-executed,
instruction-backed, reconstructed decisions, engineering substitutions and assumptions.
Do not promote interpretations into verified algorithms.

Roadmap: original ARM64 reference -> independent C# core -> Godot reference
prototype -> Unity production. Portable core targets .NET Standard 2.1; headless
tools use modern .NET. Verify compatibility. Godot and future Unity must share the
authoritative core and must not duplicate judgment/scoring. No Unity work in R001.
Work 2 owns reconstruction, not new expeditions or acceptance-policy changes.

R001 minimum: a standalone C# executable parses synthetic ordinary AFF tap charts,
processes timestamped frames and inputs deterministically, calculates gameplay
independently, and reproduces Expeditions 024 and 035. Native code may be consulted
during development but must not be loaded, imported, executed or emulated by the core
or runner. No Godot window is required. Do not expand scope before this goal is secure.

Mandatory gates (all required, no silent skips):

| Gate | Contract |
|---|---|
| A | Core/runner build and actually process AFF into a computed trace without engines/ELF. |
| B | Parse the established two-tap AFF into native-equivalent lanes/times/N/chart end. No hardcoded chart. |
| C | Deterministic explicit FRAME/DOWN/UP order, classification, expiry and same-time interleavings. |
| D | Expedition 024: PURE2/FAR0/LOST0, score10000002, float32 H80.4000015258789, integer H80, category3; intermediate timing/states agree. |
| E | Expedition 035 E1110: input-first older LOST consumes input; frame-first expires older then newer PURE. Compare notes, counters, score, combo, health and candidates. |
| F | Execute every mandatory regression including repeated replays; report commands, environment, exits/counts/failures. |
| G | Deliver source, runnable entry, instructions, traceable references and actual evidence; publish reviewable commit/branch without force push or unrelated research edits. |

Meaningful normalized comparisons include effective time, chart-derived note IDs,
candidate order, judgment, consumed/missed state, PURE/FAR/LOST, combo/max, score,
health, completion and GameResult. Report the first divergent event/field. Do not
compare heap pointers or generate goldens from the reconstruction.

Keep research, portable code, headless runner, tests and engine adapters separate.
All source belongs in Arconist. Do not commit original archives/assets/ELF, emulator
dumps, credentials, build products or temporary logs. Curated reference data and
reviewable validation summaries are permitted deliverables; raw generated traces
remain outside tracked source. Use isolated development and an R001 branch.

Deferred: graphical playability, full holds/arcs/arc-taps/flicks, skills/special
gauges, audio playback, Android packaging, production persistence and renderer
fidelity. Headless evidence is never physical-device or visual validation.

Report Result (PASS/FAIL/NOT RUN), What I Found, Implementation and Pseudocode,
Mandatory Acceptance Table A-G, Validation Commands, Publication, and Final
Reconstruction Boundary. Include verified SHA/branch, changed paths and preservation.
If a gate fails, preserve and deliver the failed state with errors/divergences and
targeted repair. Stop after R001; no R002/R003 or new expeditions without authority.

## Headquarters publication and human qualification policy — 2026-11-05

This section supersedes R001-era directions requiring reconstruction work to remain
on dedicated reconstruction/r00x branches until a separate merge. The official
integration and publication target for all subsequent Arconist reconstruction
missions and corrective orders is the repository's `main` branch. Work may use a
temporary safety branch during development, but must publish the resulting source,
validation report, and append-only contexts on `main` before reporting its work as
delivered. Never force-push, rewrite history, or overwrite unrelated original-native
research. Check current `main` ancestry and use a normal fast-forward or reviewed
non-destructive integration if another agent has advanced it. State the final `main`
SHA and release-asset location in every handoff. Original work can be committed as
FAIL/partial or READY FOR HUMAN QUALIFICATION with those labels clearly retained;
publication to `main` alone never means an accepted PASS.

All graphical interaction/playtesting automation is prohibited for prototype
qualification: no Computer Use operation of the game, SendInput, keyboard/mouse
injection, scripted graphical playthrough, or screenshot inspection offered as a
substitute for the owner's testing. Build/export/package validation, deterministic
unit tests and headless gameplay/spatial regressions remain permitted as technical
checks only. The project owner alone performs actual prototype launch, visual,
input, gameplay, results and replay qualification. Work must stop at READY FOR HUMAN
QUALIFICATION after a complete technical delivery, and Headquarters must not accept
the playable mission until the owner reports a satisfactory hands-on result.

R003-C01's Windows package was delivered for owner qualification; it is not
accepted as R003 PASS. The owner will test that specific build and report findings.
Do not launch R004 or Unity because source is now on `main`.
