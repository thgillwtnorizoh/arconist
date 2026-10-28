# Expedition 030-R — Designant Material-Backed Camera Revisit

Date: 2026-10-28. Parent: `b2704dbcdaaf8aeae6d30df3b3d64c6d98399438`. Backlog: **G-006**. This is an addendum; original Expedition 030 is unchanged. No Expedition 035 or G-007 investigation is initiated.

## Result

**Blocked at Gate A, before native Designant selection.** The new files close a content-availability gap, but do not supply the missing purchased-Song/ownership/unlock provenance needed to justify this entry with the current adapter. No Designant Song is renamed from the base fixture, no eligibility return is forced, and no purchase or unlock record is invented. G-006 remains Blocked.

| Gate | Result |
|---|---|
| A — legitimate Designant selection/activated scene | Blocked before target selection; no executed target rejection is claimed |
| B — supplied-chart native parsing/runtime camera production | not_run |
| C — native overlapping actions | not_run |
| D — reset/cancellation and subsequent camera evolution | not_run |
| E — camera-dependent JNI judgment | not_run |

The unchanged ordinary control passes original solo eligibility, constructor/loading/initializer and Director activation. It is explicitly **not** the Designant experiment. Earlier camera-reset behavior remains Unknown in the requested connected environment. A precisely bounded input/producer blocker is preserved rather than replacing it with an isolated action/reset test.

## Preparation and provenance

Read project instructions and cumulative research relevant to chart construction, camera/input/scheduling, original scene entry and current producer-first restrictions; inspect the complete 030 report and current backlog/source. GitHub main matches the stated parent. Recursive parent tree contains no 030-R publication or camera_designant source. All 60 locally present parent files match their GitHub Git-blob hashes before changes; missing historical local files are retained through the unchanged parent tree. Relevant 007/010/022 original reports were also accessed at the parent. Historical camera/action experiments are reused as references, never relabeled as this run.

Original ZIP member `lib/arm64-v8a/libcocos2dcpp.so` is verified unchanged:

`SHA-256 3eaca4e6dabb3395f276f8915698d57675757d0df0970e716b23a3dc201c79be`.

Code addresses below are original ELF VAs. Runtime object pointers are observations in a fresh emulated address space. Runtime versions: Python 3.12.14, Unicorn 2.1.4, pyelftools 0.33; package pins unchanged. Capstone 5.0.7 is used only for bounded external instruction inspection, not added as a runtime dependency.

## Supplied materials and compatibility

| Original supplied filename | Bytes | SHA-256 |
|---|---:|---|
| `0.aff` | 38167 | `a9d55c137f69ff77edc0f6834f040877d80c97596299abcbb2fb78ec12400b41` |
| `1.aff` | 56948 | `7688e9177b1d4ee34ad026fad8741a18fea421d12c9c09e64974a84b1b2ee974` |
| `2.aff` | 99137 | `3a02e106e5772cc5039ec0db5221764c934428865cfafa0089ffe35637f0db13` |
| `3.aff` | 125802 | `bd7b198b28ebbeef694a446e3f22f8ba81bfe5541cdca4379f0a4730ff5974f7` |
| `base.ogg` | 4340249 | `6f3536d348750e30faff624530326ac4c88cc5049fbfa8497737227ef7d0d8ac` |

All four chart files decode as UTF-8 text AFF with `AudioOffset:0`, dash separator and timing0/200.00/4.00. They are not encrypted or binary containers in these supplied copies. The audio has an Ogg/Vorbis header. These are **direct file observations**, not original parser/audio execution, signed content authentication or proof of complete installed resources. Filenames/bytes remain unchanged. No chart/audio content is committed.

**Lexical inspection only:** each difficulty contains three camera records: opposing Z translations +0.01 and -0.01 at89669, easing `l`, duration1; reset at140270 with zero triples, duration1. The reset is nominally50601ms later, so these records alone do not establish reset during an unfinished long overlap. Native scheduling effects for these originals remain unexecuted. A later synthetic overlap/reset fixture would be separate research input; none is created after Gate A stops.

The user-supplied song record matches the original archive's `assets/songs/songlist` Designant record (idx433, id`designant`, BPM200, set/purchase`lephon`, side3, version6.0, remote_dl true, world_unlock false, byd_local_unlock true; difficulties0–3 hidden_until_unlocked true / hidden_until song). Songlist SHA-256 is `d0fa964e32d16ca486255d123880e200bb01504cdb26c78c729de9ae0120ba86`. The supplied data adds actual chart/audio bytes; it does not newly add the already archived metadata or an ownership assertion.

No Designant-named original ZIP paths exist. That is a scoped inventory, not proof about every installed file or alternative resource representation. The archive already includes `assets/songs/packlist` and a descriptive `lephon` record; no extra packlist is requested. Its catalog description is not a purchase receipt/unlock producer. No native requirement for additional pack metadata has been established.

## Gate A: exact producer boundary

The existing `solo_entry.setup`/`chart_services.metadata` adapter supplies a bounded base-song representation, not a complete original catalog/account startup. It allocates an external Song/difficulty, uses base/no-purchase metadata, prepares zero-initialized local/profile storage and an external no-ability character shell. It has no implemented coherent purchased-Song descriptor/ownership import. Keeping those null/default fields while changing only the ID to`designant` would omit the supplied record's purchase and hidden/unlock contract. This revisit does not do that.

**Native-executed ordinary control:** original `ee197c →17c45f4` returns1 at`ee2214`; original latch, `ee29a8 →ee29e8 →e4e4dc`, loading callback and `e2ea48` return1 execute. Native Director activates that same ordinary GameScene. Example observed scene`0x4327c40`, model`0x4356040`, chart`0x4331980`; scene+3e0/+3e8 and model+28 agree. Listener registered/enabled1, paused0; running scene same, pending0, dispatcher1. Two original visitation/model entries occur, with a final preroll frameE−2999. Heap values are not required constants.

For this **ordinary** Song, original `18c898c` returns null from Song+190. Two `10a1b04` calls execute the null-purchase path `10a1c8c →10a1cb8`, yielding the permissive branch within the original eligibility chain. That is exactly why this baseline cannot prove paid-song eligibility. Read-only observations also show supplied local+288=0 and local+298=0; no purchase entries exist in that bounded storage. These are host-prepared source-state defaults, not an original native account import or real account ownership verdict.

**Instruction-backed, unexecuted for Designant:**

| Consumer / edge | Contract and limit |
|---|---|
| `18c898c` | Loads Song+190, an object pointer; JSON purchase text is not that object |
| `10a1b04`, fallback `10a1c84–10a1c98` | Loads the purchase reference; null can return true, nonnull follows local-state membership |
| `10a1c9c–10a1ca0 →10a1ccc` | Reads local+288; zero count returns false for this nonnull-reference branch |
| `17c46a0–17c46a4` | Consumes that predicate; a false result enters later original alternate checks, not an unconditional final rejection |
| `17c46f8/17c470c/17c4714` | Purchase-object bytes+bb/+bc and local-state query `f2bed8` can affect alternate routes |
| `f2bee0–f2bf08` | Nonnull purchase object and zero local+288 count return false |
| `169eb68 →16c1270` | Separate string-key lookup at local+2b8; not populated as an invented unlock |
| `17c478c →fc2f64 →17857fc` | Further purchase-object status logic; full target outcome not executed |

The **first missing interface** is coherent native/catalog purchase-object mapping plus justified ownership/unlock source data (or an evidence-backed legitimate alternative route). The exact conditional false edge above characterizes one prerequisite consumer, **not a claimed observed native rejection of Designant**. No final eligibility return for Designant is reported. `remote_dl`, hidden flags and local chart presence are not silently reinterpreted as proof of permission. The complete meaning/production of the relevant descriptor flags for this song remains Unknown.

Recovering that original catalog/ownership lifecycle would be a substantial new producer dependency. No supplied account/save/unlock evidence or established paid-song adapter closes it. The hard stop is applied here, before attempting native Designant chart loading. This is a bounded source-availability conclusion, not proof that the original application cannot play Designant offline or that all paid content requires network access.

## Camera construction, reset and JNI status

Historical 030's observed generic-song exclusion remains valid: original property writer`173c3cc` wrote chart+110=0; `186453c →1863d60` omitted parsed camera events for sayonarahatsukoi. The exact`designant` exception at that builder remains **Instruction-backed**. Its existence cannot supply upstream selection state. No supplied original chart reaches this comparison in030-R.

Target chart pointer/native digest/property, runtime factory`1651e88`, initializer`81d3e4`, handler`192b5c8`, action clones/targets, reset`b0bd74 →15beb20 →f14f9c`, immediate/later child transforms/matrices and projected JNI results are all **Unknown/not_run for Designant**. No direct handler/action/reset/judgment invocation substitutes for them. The old rig-target versus child-target cancellation hypothesis is neither proved nor disproved.

## Reproducible diagnostic and regression validation

```bash
python research_harness/run.py \
  --archive /path/to/arccopy.zip --scenario camera_designant \
  --designant-materials /path/to/designant-materials \
  --output /path/outside/research_harness/camera-designant-result.json
```

The external directory contains original0.aff/1.aff/2.aff/3.aff/base.ogg. No old session state is needed. The new scenario uses unchanged ordinary_two_tap AFF only for its explicitly named ordinary control. External originals are inspected read-only and are never silently substituted into that base Song. Missing/incompatible external inputs fail clearly. Native exceptions retain available partial evidence.

Authoritative diagnostic: **exit1**, `status: fail`, `NativeDesignantSelectionProvenanceUnavailable`; ordinary_control pass; designant_native_selection_attempted false; Gate A blocked_before_native_selection and B–E not_run. Structured output contains material hashes/formats/lexical events/catalog source, native ordinary calls/ownership/control state, original instruction words, exact conditional consumer edge, declared services/skips and null target outputs. A characterized blocker is not relabeled a passing camera regression.

Fresh modified-tree CLI runs: ordinary full-session/results/SQLite, chord forward/reverse, moving/crossing arc, timing-group/reverse-scroll and CPU note refresh/expiry all return exit0/status pass. Existing native arc-tap and hold dual-case tests pass through their CLI subprocesses. Missing archive and wrong ELF hash tests pass. The initial five-test discovery reports four passes and one skip because the native-negative switch was misnamed; the skipped unavailable-song test is then run explicitly with `ARCONIST_TEST_ARCHIVE` and passes (exit0). No skip is counted as native execution. All five existing test cases therefore have actual passing execution evidence across these invocations.

Actual command shapes (external output directory `audit/030R`, never published):

```bash
python research_harness/run.py --archive "$ARCHIVE" --scenario ordinary --output "$OUT/ordinary.json"
# Same command for chord, moving_arc, timing_group, cpu_note: each exit0.
ARCONIST_ARC_TAP_TEST_ARCHIVE="$ARCHIVE" ARCONIST_HOLD_TEST_ARCHIVE="$ARCHIVE" \
  python -m unittest discover -s research_harness/tests -v
# Four pass, one unavailable-song skip; process exit0.
ARCONIST_TEST_ARCHIVE="$ARCHIVE" PYTHONPATH=research_harness/tests \
  python -m unittest test_inputs.InputTests.test_unavailable_song -v
# The previously skipped native test passes; exit0.
```

Ordinary still records PURE2/FAR0/LOST0/score10000002 and native SQLite/result identity checks. Other scenarios retain their unchanged original assertions. No fresh clean-install reproducibility milestone is claimed; these are fresh processes using the pinned runtime and current source.

The original `camera_reset`, `track_fade`, `flick_producer` and `continuous_gauge` blocked diagnostics remain unchanged; they are not counted as passing gameplay scenarios or reopened. No existing fixture/assertion, dependency pin or historical source is weakened. No new renderer/platform service or gameplay PC skip is added.

## Scientific boundaries and publication

Inherited external catalog/account/profile/settings/platform/clock/JNI/ABI/resource/audio/GPU/allocator/autorelease interfaces remain supplied. Original chart/model/score/scheduling logic executes only for the declared ordinary controls/regressions. Base Node traversal/render/flush remain scoped boundaries except the existing cpu_note scenario's own previously authorized restoration. No real Android input latency, actual audio playback, GPU rendering, production account compatibility or copyrighted-content redistribution is claimed.

Exact inherited ELF PC skips:

```text
f72110→f72158
16a4238→16a48d8
121581c→121584c
a507c4→a519ec
a51adc→a5213c
196fdac→196ffac
891190→89164c
891688→89219c
8921dc→8928e0
```

The final three are results-only; the new short diagnostic does not enter them. No camera, eligibility, entitlement, index or judgment skip is added.

Authorized publication has exactly seven paths: this addendum, append-only context, G-006 status/history, harness README/run.py/config.py, new src/camera_designant.py. No synthetic fixture is needed. Historical030 and001–034, all prior source/tests/fixtures/assertions, root README/instructions and unrelated blobs remain intact. Original assets/charts/audio/archive, generated JSON/traces, databases, environments and secrets are excluded. Source/readback/prefix/tree verification and immutable commit links are returned to headquarters; no self-referential commit SHA is invented in this report.

## Pseudocode — observed path

```text
verify original ELF and published parent
read supplied chart/audio bytes without changing them
inventory hashes/formats/camera records; compare archived Designant catalog

fresh unchanged ordinary base-song control:
    original solo eligibility accepts null-purchase fixture
    original latch/allocation/constructor/loading/initializer
    Director activates same GameScene; original visit reaches model
    inspect bounded local purchase storage: empty

Designant Gate A preflight:
    catalog says purchase=lephon and hidden-until-song-unlocked
    current adapter provides no coherent purchase descriptor or ownership/unlock producer
    original instructions establish nonnull-descriptor membership/status consumers
    do NOT rename ordinary Song, fabricate a purchase/unlock, or claim target rejection
    stop before original Designant selection

NOT RUN for Designant:
    original chart loading/parser/digest/property/runtime camera builder
    camera dispatch/paired actions/overlap/reset/child-action survival
    camera matrices and JNI judgment

run unchanged successful regressions
emit failed diagnostic with explicit not_run stages
keep G-006 Blocked; append030-R evidence and publish narrow commit
STOP
```

## Final research boundary

Newly known: concrete supplied AFF/audio identities, matching archived metadata, lexical original camera sequence, and exact separation between this content and the current adapter's missing purchased-song selection provenance. The ordinary original-native entry remains working. Still unresolved: actual Designant eligibility, supplied-chart native compatibility/construction, integrated overlap/reset/cancellation and post-reset JNI projection. Minimum continuation input is the original purchase-object/catalog and ownership/unlock producer contract with legitimate source values, or a proven original alternative eligibility route. A new packlist, arbitrary account flag, forced feature byte or isolated camera routine is not an established remedy.
