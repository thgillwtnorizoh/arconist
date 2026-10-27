# Expedition 030 — Native Camera-Action Overlap, Reset Cancellation & JNI Projection

Date: 2026-10-27. Parent: `ffce27f95649d581715a51deb295e13aad5d3d01`. Selected backlog item: Scout001 **G-006**.

## Result

**Blocked before Gate A; the expedition's minimum action-integration criterion is not met.** Original AFF parsing accepts both proposed camera controls, but the original chart builder excludes them in the unchanged ordinary `sayonarahatsukoi` fixture. No LogicCameraControl is produced, no AFF-driven camera action enters the ActionManager, no camera reset executes and no post-action JNI projection/judgment is attempted. Gate B is not started. G-006 becomes **Blocked — Expedition030**, with the exact predicate preserved below. No Expedition031 is initiated.

The useful new result is the missing **runtime camera-construction eligibility contract**, observed inside original solo-created GameScene initialization. It prevents confusing parser support with a reachable ordinary chart event. This is not evidence that reset cancels child actions or that child actions survive: both remain **Unknown** in the requested native-owned integration.

## Preparation and evidence provenance

The introduction, current context/backlog, relevant004/007–009/011 camera/input/scheduling sections,022–024 entry/runtime evidence and025–029 published source/fixtures/scenario conventions were reviewed. Current main matched the expected parent and no030 existed before changes. Every locally present parent file matched its GitHub Git-blob hash. The actual reusable source was available; no emulator, camera rig, Scheduler or ActionManager was rebuilt.

The external read-only archive member `lib/arm64-v8a/libcocos2dcpp.so` was inspected and verified:

`SHA-256 3eaca4e6dabb3395f276f8915698d57675757d0df0970e716b23a3dc201c79be`.

Original code addresses below are ELF VAs. The object pointers are observations in an emulated address space, never required constants. Validated environment remains Python3.12.14/Unicorn2.1.4/pyelftools0.33 with unchanged dependency pins. Existing external Capstone5.0.7 diagnostic tooling inspected only the relevant builder/property/reset/ActionManager routines; it is not a published dependency.

**Native-integrated:** connected execution in the new ordinary scene and its frames. **Instruction-backed:** targeted original code not executed on the new camera-action path. **Interpretation:** a consequence beyond the direct trace. **Unknown:** unexecuted overlap/reset/camera-JNI behavior. Earlier007–011 prepared-environment action/matrix/input tests retain their original classifications and are not substituted for a new successful gate.

## Supplied fixture and original entry

The original ordinary fixture is retained: Song`sayonarahatsukoi`, difficulty0, set`base`, no purchase descriptor, ordinary mode0, speed40 tenths, no modifier/map,40 zero PlayParameters bytes, existing controlled catalog/profile/settings/platform/resource services. Complete original static initializer`1930604` and song registry initializer`1054f24` are reused.

`fixtures/native_camera_overlap.aff`:

```aff
AudioOffset:0
TimingPointDensityFactor:1.0
-
timing(0,120.00,4.00);
camera(600,600.00,0.00,0.00,0.00,0.00,0.00,l,2000);
camera(900,0.00,0.00,0.00,0.00,0.00,15.00,qi,2000);
(1500,3);
```

External chart bytes enter the existing resource-provider boundary. The original whole-file parser and MD5 execute; native chart+f8 retains `95451b38656c8e41b8ac12acf524897b`, matching an independent host comparison of these exact synthetic bytes. The host comparison is not a replacement digest. The initializer's temporary property-comparison string changes the final digest character to0, as previously recovered in010.

`fixtures/native_camera_reset.aff` adds only `camera(1200,0.00,0.00,0.00,0.00,0.00,0.00,reset,0);`. It is preserved as an **unexecuted candidate**, not claimed validated by this experiment. No fresh reset-variant runtime is created after the control fails.

Connected execution succeeds through original menu construction/selection setter, `ee197c` eligibility1, native request latch1, allocation`ee29a8`, constructor call`ee29e8`, original loading actions, `e2ea48` initializer return1 and Director activation of that same GameScene. No direct driver GameScene construction/initialization or model frame supplies those handoffs.

## New native construction blocker

Original parser`138f560` executes twice inside whole parser`1870de0`. Builder`1862a14` recognizes both parsed camera objects through its original RTTI cast, reaching`1863e4c` with actual native products:

| Parsed object | Type/vtable | Time | Six numeric values | Easing | Duration |
|---|---|---:|---|---|---:|
| `0x432f080` | `13CameraControl` / `1b17318` | 600 | 600,0,0,0,0,0 | `l` | 2000 |
| `0x432f140` | `13CameraControl` / `1b17318` | 900 | 0,0,0,0,0,15 | `qi` | 2000 |

Thus original grammar, integer/float distinctions and `qi` parsing are accepted. The failure occurs **after parsing and recognition**, before runtime camera allocation.

Instruction-backed decision, now executed with both records:

```text
1863e4c: get chart
1863e54: load byte chart+110
1863e58: if nonzero → runtime camera construction at1864540
otherwise compare selected Song ID with exact9-byte literal "designant"
186453c: if comparison false → next parsed object at1863d60
1864540..1864590: prepare camera parameters → factory1651e88
```

Both actual decisions record chart`0x4332180`, chart+110=0, Song ID`sayonarahatsukoi`, native exception-result W19=0 at`186453c`, followed by the observed original edge **`186453c→1863d60`**. Runtime factory`1651e88` and initializer`81d3e4` have zero entries. Main chart contains zero`18LogicCameraControl` objects. No host-provided object, flag or skipped branch repairs this result.

The property byte is not merely assumed zero from allocation: an original one-byte store at **`173c3cc`** writes0 to emulated address`0x4332290` (chart+110) before the builder. Targeted original disassembly shows the preceding feature-property selection checks normalized digest strings and named Song IDs. Named true branches include `lfdyrmx`, `unknownrmx`, `cataclysmcry`, `deinosphainein`, `ember` and `sacrosanct`; the builder has its additional exact`designant` exception. These alternative property branches are **Instruction-backed, unexecuted here**; no universal semantic name is fabricated for byte+110.

Archive `assets/songs/songlist` contains Designant metadata with set/purchase`lephon`, BPM200, side3 and hidden/unlock-related fields; there are no `designant`-named archive paths. This does not prove all installed Designant resources are absent. It does show that simply renaming the base/no-purchase/BPM178 ordinary fixture to`designant` would misrepresent the supplied catalog. Other inspected named property examples belong to purchased catalog contexts or are absent from this supplied songlist. No entitlement/account reconstruction or alternate-song experiment is undertaken.

**Interpretation:** the proposed generic AFF controls cannot reach the native action/reset path in this particular ordinary fixture because the original builder restricts their construction. This does not prove that all ordinary solo charts reject camera events. A properly justified native camera-permitted catalog/chart/eligibility context could take a different original branch. That input is the minimum future remedy; manually setting chart+110, fabricating an approved digest, or calling the camera handler directly would bypass the connection under investigation.

## Native scene, rig, ActionManager and frame observations

The final diagnostic uses a fresh native runtime and records the construction rejection, successful ordinary scene and subsequent native frames together:

| Observed emulated object | Pointer |
|---|---|
| GameScene | `0x4327c40` |
| GameModel | `0x4356680` |
| LogicChart | `0x4332180` |
| CameraController (`16CameraController`) | `0x4368f80` |
| Primary Camera / mask4 | `0x43692c0` |
| Secondary Camera / mask16 | `0x43697c0` |
| Scheduler / ActionManager | `0x41081c0` / `0x4108840` |

Scene+3e0→model and scene+3e8→chart; model+20→rig; rig+2a8/+2b0→distinct original child Cameras. Factory`1393474`/initializer`851514` each execute once. Rig and both children have their original inherited+1b0 ActionManager relationship equal to the native manager. Gameplay listener is registered1/enabled1/paused0; final dispatcher enabled1, running scene unchanged and pending replacement0.

The ordinary native tap survives construction at1500/raw3→lane4; chart N1/end1620. Original index producer executes504 times including auxiliary objects, and the tap appears in the native index. It becomes active byE500. This is not evidence that a camera event has been admitted: no runtime camera-control object exists to index or dispatch.

The original music anchor is wall9452/E0. The final diagnostic visits E500/600/601/900/901, explicitly crossing both strict event boundaries without a camera handler call. Each frame observes the original chain:

`Director1793f8c → Scheduler13d3f44 → registered callbackd630b8 → ActionManager9effe0 → scene visitation/model`.

| E | Wall | Actual float32 Scheduler/ActionManager dt |
|---:|---:|---:|
| 500 | 9952 | 0.5 |
| 600 | 10052 | 0.10000002384185791 |
| 601 | 10053 | 0.0010000000474974513 |
| 900 | 10352 | 0.29899999499320984 |
| 901 | 10353 | 0.0010000000474974513 |

The driver supplies only wall-clock values; effective GameTimeline E and native dt are read, not assigned. It does not call individual action updates or the camera handler. Existing native ActionManager inspection matches original`9effe0` layout: manager+10 entry list, entry+8 target, entry+21 paused byte, entry+38 next; entry+0 action array with count at+0 and pointer data at+10. Original insertion`b3dc38` takes manager/action/target/paused arguments. These are **Instruction-backed layout checks**, corroborated by actual target snapshots.

At every observed state, the manager contains three unrelated loading/UI target entries (`0x47b3340`, `0x4948380`, `0x4482900`), each unpaused with one action. **None targets the rig or either child camera.** No new Node runAction occurs in the selected camera frames. Existing ambient action stepping is not relabeled AFF camera-action advancement.

Both cameras remain position(0,900,900), Euler(−26.565061569213867,0,−0), quaternion(−0.22975297272205353,0,0,0.973249077796936), Node flags34. Rig home is(0,900,900), look-at(0,−550,−2000), latch1. Cached view/PV data are recorded as read; no additional getter forces matrix refresh, and no changed-matrix or post-reset projection claim is made.

Counts over the final connected run include whole parser1, camera parser2, runtime builder1, native camera rig factory/initializer1, Scheduler/callback/ActionManager31 each including loading, event-processing dispatcher`f8056c`8, and ActionInterval step98 across existing loading/UI actions. Runtime camera factory/initializer, camera handler`192b5c8`, translation/rotation builders, MoveBy/RotateBy factories, cubic wrapper, rig reset`b0bd74`, JNI DOWN/UP, tap classifier/acceptance/recorder and miss recorder are all0. Global Node runAction/insertion9 and generic stop-target`f14f9c`35 occur during startup/loading; those counts are **not camera-action construction or a camera reset**. Global`15beb20`30 similarly does not establish the unexecuted reset chain.

## Reset/cancellation question and unexecuted portions

Targeted original instructions still support007's relationship:

```text
b0bd74(rig)
  →15beb20: X1=rig, X0=rig[+1b0]
  →f14f9c(manager,rig)
  →original look-at/home stores, then rig latch1
```

Native stop-target code searches the requested target identity. That static relationship cannot establish cancellation/survival of child actions in a complete reset experiment when no such actions were constructed here. No child queue is manually populated to finish the experiment. No isolated MoveBy or reset call is substituted. The reset fixture, action/clone creation, overlapping elapsed/progress, immediate reset state, later action survival, changed matrices, camera projection, JNI candidate/judgment/score and contact cleanup for these new fixtures remain **unexecuted/Unknown**. Zero judgment entries are not a successful miss/eligibility test; no input was delivered.

This single construction-eligibility blocker consumes the bounded dependency investigation. The last successful pathway is original solo loading/scene activation and Director-driven model frames; the first target-path exclusion is the native builder edge above. No new renderer/audio/Android investigation follows. Cancellation policy remains an open research question with a now-precise prerequisite.

## Reproducible blocked diagnostic

```bash
python research_harness/run.py \
  --archive /path/to/arccopy.zip --scenario camera_reset \
  --output /path/to/camera-reset-result.json
```

Actual result: exit1, `status: fail`, `NativeCameraConstructionExcluded`, Gate A`blocked_before_runtime_camera_construction`, Gate B`not_run`; final E901. JSON29664 bytes contains original binary hash, actual parsed objects/rejection operands/property write, scene/rig/children, native index/tap state, Scheduler dt/target snapshots, cached transforms/matrices, call counts and explicit unexecuted endpoints. Scientific characterization assertions pass, but the requested camera regression correctly remains failed. Unexpected exceptions also preserve available partial evidence and fail.

`src/camera_reset.py`, two candidate fixtures and minimal CLI/config/README additions preserve the diagnostic. Internal`camera_reset_variant` selects the unexecuted reset fixture; it is not a second tested CLI case. There is no passing-camera unittest wrapper or canned reset trace.

The first exploratory overlap run had already reachedE1500 with unchanged cameras/no controls. It is not spliced into the final diagnostic; the final fresh instrumented run independently captures actual parser products and native rejection, then stops atE901 after confirming non-dispatch. Neither run repairs state or calls a gameplay/camera/action routine directly. No third fixture or alternative-song runtime is tested.

## Regression protection and boundaries

Fresh current-source ordinary full-session, chord forward/reverse, moving/crossing arc and timing-group/reverse-scroll CLI regressions pass. Existing arc-tap and hold dual-case native unittests and missing-archive/wrong-hash/unavailable-song controls also pass. All5 discovered tests finish in64.957s with all3 archive switches enabled and zero skips. The new camera diagnostic's expected fail is reported separately and never included as a passing end-to-end regression.

No earlier fixture, scenario assertion, test, pinned dependency, report001–029, root README or standing instruction is changed. No new platform/ABI/catalog/resource/renderer service or gameplay PC skip is installed. Existing controlled catalog/settings/profile storage, standard libc/C++/math/JNI/platform services, archive resources, synthetic AFF, external clock, graphics/texture/presentation and audio services, allocation/autorelease and incomplete reclamation retain prior scope. Native TrackLayer CPU19069a0 remains enabled. No full Android/GPU/audio-device or production compatibility claim is made.

Exact inherited PC ranges (ELF VAs):

```text
f72110→f72158       platform GLView attachment
16a4238→16a48d8     shutter panel proxies
121581c→121584c     loading overlay
a507c4→a519ec       loading artwork prefix
a51adc→a5213c       information artwork/canary
196fdac→196ffac     closing information visuals
891190→89164c      results UI prefix
891688→89219c      middle results UI
8921dc→8928e0      post-save progression/UI
```

The last3 are not entered by the new diagnostic. Base traversal/render/flush129c924/1017a84/13edf0c remain inert. Inherited private DB preparation does not constitute a030 results/SQLite experiment. No proprietary archive/library/assets, full dumps, generated JSON/traces/databases, environments or secrets are published.

## Publication and backlog

Nine authorized paths contain the new report, append-only context, G-006/history change, harness README/config/CLI, blocked diagnostic source and two synthetic fixtures. G-001–G-005 remain Verified; G-007–G-010 statuses remain unchanged. Historical context is preserved as an exact prefix. Publication uses the verified parent and non-forced expected-head update; every changed committed file is fetched and compared against prepared content, and parent/child tree comparison verifies unrelated old blobs. The exact commit SHA and pinned links are returned in the final response.

## Pseudocode — observed path and stop

```text
verify external original ELF and published parent
supply established ordinary metadata/services plus overlap AFF bytes
original solo eligibility/latch/allocation/constructor
original loading → whole AFF parser → two parsed CameraControls and one tap
native chart property producer writes chart+110=0
original builder recognizes each parsed CameraControl:
    chart+110 is0 and exact designant Song exception is false
    original186453c→1863d60 skips it
native chart therefore contains no LogicCameraControls
original GameScene initializer returns1; Director activates original rig/cameras
Director frames execute Scheduler/callback/ActionManager/model past600 and900
observe no camera actions/handler, unchanged child transforms, other UI targets
emit failed camera regression with exact native construction blocker

NOT EXECUTED: overlap action creation, reset runtime, reset/cancellation,
              post-action camera projection, JNI judgment for new fixtures
run previous regressions; preserve them unchanged
mark G-006 Blocked; publish bounded evidence
STOP before Expedition031
```
