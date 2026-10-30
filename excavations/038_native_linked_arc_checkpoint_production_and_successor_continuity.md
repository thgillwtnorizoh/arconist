# Expedition 038 — Native Linked-Arc Checkpoint Production & Successor Continuity

Native execution: 2026-10-29. Publication: 2026-10-30. **G-014**, selected by headquarters from Scout002 S2-C04.

## Result

**Verified for one ordinary native-owned two-segment arc chain.** Original whole-AFF initialization produces linked arcs, shared LogicColor and LogicArcGroup, native generation arguments0/1, six final checkpoint records representing **N7**, original index/admission and continuous JNI gameplay through the successor. Seven actual accepted recorder calls, no misses, and complete original contact cleanup are observed.

The ordinary initializer does **not** pass Expedition009's externally supplied flag1 to both arcs. Its root arc uses0 and its successor uses1. Native weight folding still produces a weight2 record. Final score10000007, PURE7/shining7/FAR0/LOST0/combo7, live H81.4000015258789. No linked object, generation argument, weight, owner, activity, index entry, counter or gauge state is assigned by Python.

All prior successful native scenarios and existing tests pass. The new scenario stops atE2877, before chart completion/results/SQLite. No new service, native dependency or gameplay PC skip is introduced.

## 1. Preparation and identities

Verified main/parent: `2e4e15aa820abc37ad0934eacbd8efec67ad5a26`; tree `30442bc868e522c35a2d4e683541e35911d75223`. No038 report existed. All73 locally present original repository blobs matched the parent before edits. The supplied introduction, cumulative context/backlog, S2-C04 mission, relevant002–004/008–011/018/022–025/028/035–037 research and current moving-arc/solo-entry/lifecycle/input-array/config/fixtures were reviewed. In particular,009 §16 is a prepared-generation-argument experiment and010 §6 establishes the original initialization order; neither substitutes for this producer gate.

External read-only archive member: `lib/arm64-v8a/libcocos2dcpp.so`,29217504 bytes. Fresh SHA-256:

```text
3eaca4e6dabb3395f276f8915698d57675757d0df0970e716b23a3dc201c79be
```

Actual environment: Python3.12.14, Unicorn2.1.4, pyelftools0.33; pins unchanged. Capstone5.0.7 is an external disassembly aid only, not a harness dependency. A fresh environment is prepared; this is not a new clean-install milestone. All instruction addresses below are **original ELF virtual addresses**. Heap values are observations, never required constants.

## 2. Original construction and ownership

New synthetic fixture `native_linked_arc_successors.aff`:

```aff
AudioOffset:0
TimingPointDensityFactor:1.0
-
timing(0,120.00,4.00);
arc(1000,2001,0.50,0.50,s,0.50,0.50,0,none,false);
arc(2001,3001,0.50,0.50,s,0.50,0.50,0,none,false);
```

Fixture SHA-256 `c0abe4ca157ea34888c27571081383284df5b7ca61e58cce3815ac41ecedd527`; native complete-text MD5 `272ccfa1e095179b455650d2bb329d0c`. No digest, Song ID, mode or feature property is patched. These are research bytes, not a released song chart.

Unchanged ordinary selection is `sayonarahatsukoi`, difficulty0/base/no purchase, mode0, speed40 tenths, null map/modifiers,40 zero PlayParameters bytes. Original static initializer `0x1930604` and registry `0x1054f24` execute. Original `0xee197c` eligibility1/request latch/allocation `0xee29a8`/constructor `0xee29e8`, loading and `0xe2ea48` return1 all execute. Director activates that same scene; native gameplay listener is registered/enabled/unpaused.

Original whole parser `0x1870de0`, arc parsing observed at `0x924c18`, and chart `0x173b358 → 0x1862a14` create both parsed ArcNotes. Times1000..2001/2001..3001, X/Y endpoints.5/.5, curve`s`, color0 and ordinary mode0 are preserved. Original `0x178f7fc → 0xc664f8` returns two `12LogicArcNote` objects, vtable VA `0x1b91500`.

Original color factory `0xd93594`, LR `0xd512d4`, receives mapped argument0 and returns one `10LogicColor`, vtable VA `0x1aa1b98`, initially owner/release−1, bypass0. Original `0xc66560` stores that same pointer into both arcs+0xb0. This is distinct from the later shared `13LogicArcGroup`, vtable VA `0x1b85570`.

Representative runtime identities:

| Object | Observed pointer |
|---|---|
| GameScene / GameModel / LogicChart | `0x4327c40` / `0x43579c0` / `0x4332080` |
| GameTimeline / ScoreState / gauge | `0x4357b40` / `0x4357b80` / `0x4357d00` |
| First / successor arc | `0x4332a00` / `0x4332c40` |
| Shared LogicColor / LogicArcGroup | `0x4332980` / `0x4332e00` |
| Native primary camera | `0x436a780` |

Scene/model/chart/timing/color/group relationships are asserted relationally. No prepared gameplay heap is imported.

## 3. Native linking and field correction

Original `0x173bd5c → 0x125e474` runs once with LR `0x173bd60`. Executed pair predicates show:

| Original branch | Operands/result in this fixture |
|---|---|
| `0x125e610` | Absolute end/start-time difference0; branch permits differences≤9 |
| `0x125e630` | X difference double0.0, threshold double0.1; this pair passes |
| `0x125e640` | Successor start Y0.5 equals predecessor end Y0.5 |
| `0x125e658` | Both native modes0 |

Original allocation block `0x125e674..0x125e69c` creates the group, then setter `0x165286c`/store `0x16528b4` assigns it to both arcs+0xe0. `0x1205bf4` links the first arc's successor vector to the second. Native store **`0x125e5c8` writes the first arc pointer directly to second+0x150**.

Thus **+0x138 is a successor pointer vector; +0x150 is a single predecessor pointer in this path**, not a predecessor vector. Both directions and shared group are original products. Shared color alone is not used as proof of linking. No fixture adjustment is needed.

## 4. Generation argument production — the missing producer is closed

Both original arc factories explicitly store byte0 at+0xa0 at **`0x178f8fc`**, in addition to allocation zeroing. Linking's same-direction constant-geometry branch writes successor+0xa0 from0 to1 at **`0x125e784`**. The root arc stays0. This distinguishes deliberate native defaults from host-chosen values and links the successor flag to an executed original producer.

After linking, original whole-chart initialization does:

```text
0x173bdec: call original sampled-geometry producer1925084
0x173bdf0: load arc byte+a0
0x173bdf4/df8: compare and CSET W8 = (byte != 0)
0x173bd98: move W8 into W1
0x173bd9c: call native virtual+50, targetba81e8
0xba81f4: mask W1 to bit0
0xba81fc: call originald92558, LRba8200
```

All observed register values agree: **first argument0, successor argument1**. There is no direct host generation call. Original `0xd925a0/0xd925a4` transforms the flag into the first interval index, `(~flag)&1`;0 skips the start-time record and1 includes it. Its fallback/other-duration branches are not claimed generally verified.

Base generation at `0xd925fc`, before arc-specific folding:

| Arc | Flag | Native base records (time,weight) |
|---|---:|---|
| First | 0 | (1250,1), (1500,1), (1750,1) |
| Successor | 1 | (2001,1), (2251,1), (2501,1), (2751,1) |

Native arc virtual `0xba81e8` then inspects its successor vector and ordinary successor mode. For the first arc, `0xba8248` observes `trunc(duration/interval)-1 = 3` and `trunc((duration-2)/interval) = 3`. With sufficient records, **`0xba8274` shortens vector end by12**, removing the final1750 record from the logical range; **`0xba8278` writes weight2 into the previous1500 record**. A memory hook observes weight1→2 at that original PC. It is not a Python vector edit.

Final native records:

```text
first:     (1250,1,unresolved0), (1500,2,unresolved0)  -> 3 units
successor: (2001,1,0), (2251,1,0), (2501,1,0), (2751,1,0) -> 4 units
```

Original `0x173bf28 → 0x11ea120(chart,0,INT_MAX)`, LR `0x173bf2c`, counts these final native ranges and returns **N7**, stored at chart+0xb8. There are two main objects before bars,506 afterward; chart end is3501. Native N equals the sum of final record weights, not the number of records or auxiliary objects.

**Difference from009:** that prepared experiment explicitly passed1 to the first arc too, adding its1000 start record and producing four first-arc units/N8. The natural ordinary producer gives three/N7. Its native weight2 observation remains valid; universal selection of flag1 was never established. No historical report is rewritten.

## 5. Geometry, original index and admission

Original `0x1925084` executes twice; native append observations retain nine geometry samples per arc. Local X is0/Y50 throughout; depth follows original sampling, including first final Z−8097 and successor final Z−8089. The inherited CPU geometry-height environment remains the028 boundary; this is not visual fidelity or GPU evidence.

Original index insertion `0x1576aa4` executes506 times including bars. The first arc occupies group0 buckets0/1, the successor buckets1/2. Both reference the original native timing record and input-enabled1. Native active-range processing admits both by E1000. The successor is indexed/active long before it is spatially eligible: its cache-valid byte remains0, with no successful successor activation before the junction.

Original Director/GameScene visitation produces23 guarded model/continuous updates over the full schedule. Effective time is derived from the native GameTimeline and supplied clock; no timeline fields or geometry caches are set by the driver.

## 6. One JNI contact and actual successor boundary

At native E1000, original camera projection `0xbdbb70` of the first arc's native-produced target(0,50,0) gives external JNI **(640,593.0632781982422)**. DOWN42 through `0xbe31a8 → EventDispatcher → 0x194ff80` creates native Touch `0x4ee9140`, engine slot0/generated gameplayID0. The same pointer/ID stays retained throughout. No MOVE is necessary for this constant X/Y fixture; no array service is added.

DOWN itself does not activate either ordinary arc or claim its color. On the first subsequent continuous frame E1001, native camera unprojection before clamping is(0,50.017578125,0). Original processing clamps the point to(0,100,0); `0xc98490 → 0x927384` accepts it against the original arc target(0,50). These are separate native projection, preprocessing and eligibility stages, not exact point equality imposed by Python.

Original `0x15dfe2c → 0x15a90c4` claims the shared color for generatedID0. Subsequent calls accept that same owner; bypass stays0. Each accepted spatial contact sets the corresponding arc's activity through original code. One initial Touch does not imply a synthetic owner transfer at the junction.

| Native E | First active member/activity/cache | Successor active member/activity/cache | PURE |
|---:|---|---|---:|
| 1000 after DOWN | yes /0,0 /1 | yes /0,0 /0 | 0 |
| 1001 | yes /1,1 /1 | yes /0,0 /0 | 0 |
| 1125 | yes /1,1 /1 | yes /0,0 /0 | 1 |
| 1375 | yes /1,1 /1 | yes /0,0 /0 | 3 |
| 1876 | yes /1,1 /1 | yes /0,0 /0 | 3 |
| 2000 | yes /1,1 /1 | yes /0,0 /0 | 3 |
| **2001** | yes /0,0 /0 | yes /1,1 /1 | 4 |
| **2002** | no /0,0 /0 | yes /1,1 /1 | 4 |
| 2126 /2376 /2626 | no /0,0 /0 | yes /1,1 /1 | 5 /6 /7 |

Native cache setter `0xad11b0/0xad11b4`, called with LR `0x19f41f8`, is observed separately from geometry/cache data. It can receive several0 calls while samples are searched, then1 for the selected segment; final frame state is authoritative. At E2001 the first arc has no valid segment/cache and original `0xc98570` rejects it; the successor's native cache and spatial predicate accept. The first is removed by the next active-range frame. **No simultaneous activity overlap occurs at this tested exact boundary.**009's prepared surroundings observed1/1 there; this does not establish that changing generation flag alone causes the difference.

Shared color owner0, release−1 and claimed IDs[0] persist from E1001 throughE2876. No release/reclaim or second contact occurs at the junction.

## 7. Linked consumers and group state — observed, not assumed necessary

Original `0x15dfe6c` reads the predecessor pointer and `0x15dff4c` the successor vector. At E2000 first-arc acceptance's scan yields predecessor/own record−1, successor record2001 at `0x15dffd4`. At E2001 successor acceptance reads its actual predecessor and current record2001. Those links are genuinely consumed, not merely present in memory.

The group timestamp vector+0x18 is empty in this fixture; float window+0x14 stays0 and extension store `0x15e015c` is **not entered**. Shared group state still evolves through original calls:

- `0x19f3e40/0x19f3e44` reset group+0x10/+0x12 during frame processing.
- Cache setter `0xad11c8` writes group+0x11=1 when a valid arc cache is selected.
- Accepted arc `0x15e01b8/0x15e01bc` writes group+0x10/+0x12=1.

At E2002, first-arc end cleanup `0x95d6f4` reads ordinary successor mode0 and returns before the shared-color reset at `0x95d700..0x95d710`. The executed successor-aware branch preserves color state rather than treating the first segment as an isolated terminal arc.

No counterfactual control is required to establish these producers/consumers. The optional control is **not run**. This does not prove that group machinery is unnecessary, or that every continuity effect is caused by the group window. This fixture demonstrates shared-owner persistence, native per-segment eligibility and actual link/group processing; necessity under other connections remains untested.

## 8. Native weighted recording and cleanup

Original `0xf80904` reads record guards, and `0xf80924` writes each of six final records resolved0→1 once. The removed1750 base record is outside the final vector and is not awarded. Recorder `0x1730290`, LR `0xf809a8`, executes **seven times**, all judgmentID0:

| Record | Weight | Native resolution E | Actual recorder calls | Cumulative PURE / live H |
|---|---:|---:|---:|---|
| First1250 | 1 | 1125 | 1 | 1 /11.628571510314941 |
| First1500 | 2 | 1375 | **2** | 3 /34.88571548461914 |
| Successor2001 | 1 | 2001 | 1 | 4 /46.514286041259766 |
| Successor2251 | 1 | 2126 | 1 | 5 /58.14285659790039 |
| Successor2501 | 1 | 2376 | 1 | 6 /69.77143096923828 |
| Successor2751 | 1 | 2626 | 1 | 7 /81.4000015258789 |

At E1375 the two native callback returns separately produce PURE2/H23.257143020629883 and PURE3/H34.88571548461914. No weighted Python callback substitutes for them. Repeated later guard reads skip resolved records. The successor's first record is already within lookahead atE1876 but cannot score until its original eligibility activates atE2001. Miss recorder `0x868e54` has0 entries.

Final native N7 agrees with sum(weights)7 and accepted units7; PURE7/FAR0/LOST0/shining7/combo7, score10000007. No host score/gauge equation or state write supplies those outputs.

UP42 atE2876 runs original `0xdda71c` and `0xf9a50c → 0x13db7a0`, release caller LR `0xf9a5cc`. Android map/slot0/mask/retained vector and claimed IDs empty; owner becomes−1 and release time2876. Score/gauge are unchanged. Activity is still1/1 on the successor immediately after UP, then E2877 resets it to0/0. Group bytes+0x10..+0x13 change `[1,1,1,0] → [0,1,0,0]`: the cache-related byte+0x11 remains1, not a falsely claimed full group reset. Color previously-claimed byte+0x24 remains1. No owner/activity cleanup is forced.

The chart is unfinished and result cache null; completion/snapshot counts0. Physical reclamation, chart completion, results scene and SQLite are not newly tested.

## 9. Reproducibility and regression evidence

New `src/linked_arc.py` and one synthetic fixture reuse the established native runtime. CLI/config changes are limited to registration; README appends documentation. The scenario retains partial evidence/incomplete gates on failure and uses relational identities.

```bash
python research_harness/run.py \
  --archive /path/to/arccopy.zip --scenario linked_arc \
  --output /path/outside/research_harness/linked-arc-result.json
```

Actual final invocation uses `/tmp/arconist038/bin/python`, archive `project_sources/01-arccopy.zip`, scenario `linked_arc`, output `audit/038/final.json`: exit0/statuspass, all five gates pass, no native failures. An initial successful diagnostic preceded the independent final run with additional read-only color-factory/unprojection/cache observations and assertions for observed producer/consumer relationships. No native repair or spliced trace is used. There is no requirement for the historical N8, although the actually observed record multiplicity and successful native continuity are preserved as assertions.

Assertions include native link/default/flag writers; register-chain consistency through virtual/base generation; base/final unit conservation; N/count ownership; index and admission; one stable JNI contact; native successor reads/eligibility and shared-owner state; per-record recorder multiplicity; unique resolved writes and cleanup. The original OBJ ABI helper is installed unchanged but receives0 calls. No MOVE array adapter is needed. Optional native comparison is not run; no extra fixture is published.

Fresh prior CLI commands use:

```bash
/tmp/arconist038/bin/python research_harness/run.py \
  --archive /workspace/scratch/90d77f091ffe/project_sources/01-arccopy.zip \
  --scenario NAME \
  --output /workspace/scratch/90d77f091ffe/audit/038/NAME.json
```

| NAME | Actual exit / JSON status | Seconds |
|---|---|---:|
| ordinary — full session/results/SQLite | 0 / pass | 17.615 |
| chord — both orders | 0 / pass | 34.630 |
| moving_arc — moving and crossing | 0 / pass | 37.889 |
| timing_group — grouped and reverse | 0 / pass | 37.004 |
| cpu_note — refresh/expiry | 0 / pass | 47.507 |
| late_input_expiry — both interleavings | 0 / pass | 39.120 |
| noinput_semantics — paired lifecycle | 0 / pass | 43.634 |
| mixed_hold_tap — all three cases | 0 / pass | 69.814 |

With ARCHIVE referring to that same external ZIP:

```bash
ARCONIST_TEST_ARCHIVE="$ARCHIVE" \
ARCONIST_ARC_TAP_TEST_ARCHIVE="$ARCHIVE" \
ARCONIST_HOLD_TEST_ARCHIVE="$ARCHIVE" \
/tmp/arconist038/bin/python -m unittest discover -s research_harness/tests -v
```

All five tests actually pass in56.563s, exit0, **no skips**: native arc-tap CLI, native hold dual-case CLI, missing archive, native unavailable-song negative and wrong hash. Together these exercise all ten prior successful gameplay scenarios. Existing Blocked camera/track/flick/gauge/Designant diagnostics remain intact and are not rerun or counted as green gameplay. No previous fixture, scenario assertion, test or dependency pin changes. All generated JSON/logs stay outside publication.

## 10. Scientific and publication boundaries

**Native-integrated:** ordinary entry, original parser/arcs/color/group/link stores, original generation arguments/folding/count, native geometry/index/admission, Director/JNI/continuous spatial/owner/group processing, weighted recording and cleanup. **Native-isolated:** only historical009's separately prepared comparison, not represented as this run. **Instruction-backed:** decoded untaken alternative link/generator/group-window branches and comparator limits outside the exact operands. **Externally supplied:** synthetic AFF, offline catalog/profile/settings/platform/ABI/resources, clock and JNI inputs. **Hypothesis/unknown:** counterfactual necessity of group-window behavior for other chains, arbitrary branching/curves/colors/modes, Android physical scheduling and GPU/audio-device behavior.

Exact inherited PC skips, unchanged:

```text
0xf72110  -> 0xf72158
0x16a4238 -> 0x16a48d8
0x121581c -> 0x121584c
0xa507c4  -> 0xa519ec
0xa51adc  -> 0xa5213c
0x196fdac -> 0x196ffac
0x891190 -> 0x89164c
0x891688 -> 0x89219c
0x8921dc -> 0x8928e0
```

These remain platform/loading/presentation boundaries; the last three results-only ranges are unentered here. Existing inert base Node traversal/render/flush, resource/font/CSB/audio/GPU, libc/C++/math/locale, allocator/autorelease and ordinary catalog/account services retain their documented scope. Native TrackLayer initialization/CPU processing remains enabled. No new service, privileged selection, feature permission or gameplay PC skip is introduced.

Publication is a non-forced child of the verified parent, limited to eight paths: report/context/backlog, harness README/CLI/config, new source and synthetic fixture. Every changed committed file is read back exactly; parent/child blob trees and exact historical context prefix are checked. G-001–G-013 rows/statuses/history, prior reports/fixtures/scenarios/tests/assertions/pins/blocked diagnostics/root instructions and unrelated blobs remain preserved. G-014 is Verified only for this scoped linked pair. No original binary/archive/assets, generated JSON/traces/dumps, databases/environments/account data or secrets are committed. The exact child SHA and immutable links are returned to headquarters separately.

## Pseudocode — observed native chain

```text
Supply external synthetic AFF and unchanged ordinary platform services
Original solo entry -> GameScene loading/initialization
Original parser -> two ordinary LogicArcNotes, shared LogicColor
Original whole-chart linker:
    verify native time/X/Y/mode predicates
    create shared LogicArcGroup
    append first.successor = second; second.predecessor = first
    original successor+a0 store0->1; root remains native default0

Original chart initializer loads+a0 -> boolean W1
Original virtualba81e8 -> d92558 with flags0/1
    native base records
    original successor/duration fold removes last root record
    native previous weight1->2
Original count -> N7, original geometry/index/admission
Director activates native GameScene

Original camera projects native constant target -> supplied JNI DOWN42
Original native Touch retained
Director frames -> native spatial eligibility/color claim/group writes
    first active throughE2000
    atE2001 first cache/activityoff; successor cache/activityon
    same Touch/color owner persists, links consulted
    atE2002 first removed; ordinary-successor cleanup preserves color state

Original checkpoint guards/resolved writes -> seven real recorder calls
    weight2 record -> two original callbacks atE1375
Original score/combo/gauge updates; no miss or duplicate
JNI UP -> native mapping/slot/retention/claim/owner cleanup
Next Director frame clears activity; cache-related group byte remains
StopE2877, before completion/results/SQLite
```

## Final research boundary

This closes the missing original argument producer and joins a genuine linked ordinary arc chain to retained-contact successor gameplay. Native flag selection gives N7, not the prepared N8; native weight2 and two callbacks are nevertheless real. One constant-geometry pair neither establishes every connection policy nor proves group machinery unnecessary. No further experiment is required for the bounded objective. Stop after038, without039/S2-C05 or reopening deferred work.
