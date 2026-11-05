# R001 normalized native reference observations

Source authority is the unchanged repository at
`0c174c6e481158ae73e4d7c18afabaa670794d2d`. These JSON references were manually
transcribed from published native observations and instruction-backed behavior,
before running the reconstruction. They are not reconstruction-generated goldens
or complete raw emulator traces. No fresh ARM64 run is claimed in R001: the original
external ZIP and old generated raw JSON are absent. Reproduction of the original
oracle remains possible using the preserved harness and an externally supplied ZIP.

| Reference/field | Authority |
|---|---|
| ordinary chart/time/lane/count/end | `research_harness/fixtures/ordinary_two_tap.aff`; 010 sections 4/7/validation, 008 section 4 |
| ordinary input/UP/frame sequence and E2122 completion sample | `research_harness/src/regression.py:run` |
| ordinary final score/PURE/FAR/LOST/live and integer H/category | 024 observed clean-run table; `regression.py:verify` |
| ordinary per-hit shining/score/combo/flags/health | 002 acceptance and integer score, 006 ordinary gain/recorders, 008/010 integrated two-tap behavior; instruction-backed intermediate normalization |
| ordinary maximum combo/early/late/recorded-vs-final LOST | 006 recorders/snapshot, 042 confirmed recorder stores; same on-time ordinary path |
| both late charts/count/end | 035 synthetic AFF and construction section; unchanged `native_late_input_expiry.aff` |
| late E1000 precondition and candidates | 035 shared precondition and original projection |
| input-first E1110 classifier, stopping note, guards, counters/H/score/combo/cleanup/active membership | 035 Case A and outcome table |
| frame-first E1110 expiry then guard skip/PURE, counters/H/score/combo/cleanup/active membership | 035 Case B and outcome table |
| wall-to-effective arithmetic and startup | 005/008/040; ordinary relative epoch translated to 0, preroll1, music anchor3002/C2 |

The native trace's absolute clock epoch is intentionally normalized: all actions
after anchor retain the same effective time and explicit input-versus-frame order.
`timestampMs` is optional input payload, deliberately unused by ordinary judgment;
005/008 show that the callback refreshes the Timeline rather than judging by the
stored Touch timestamp. Camera/JNI screen coordinates are replaced with internal
lane inputs. This adapter substitution does not claim native projection fidelity.

IDs are `tap:sourceOrdinal:time:internalLane`. They are derived from parsed AFF and
do not encode heap pointers. Candidate arrays compare exact order and length.
Classification traces distinguish `LOST` consuming the input from the successful
note-consumption flag, and preserve `guard_missed`/`guard_consumed` visits.

Each reference checkpoint is a projection onto observed or explicitly
instruction-backed fields. Unspecified properties are not asserted. Arrays are
exact; numeric comparisons are exact; health uses signed IEEE-754 float32 bit
patterns (40.20000076293945 -> 1109445837, 80.4000015258789 -> 1117834445).
These bits are direct encoding of the reported native values, not a tolerance.
Object projections do not authorize missing mandatory fields: the checked fields
are reviewable in each JSON. The comparator reports the first divergent checkpoint
and field, and a regression deliberately corrupts intermediate combo/candidates
while retaining the correct final result.

R001 does not invent a completed GameResult for the 035 scenarios. They end at
E1110, unfinished with null result, as the original experiment does.
