# Expedition 032 — Native CPU Note Refresh, Disappearance & Culling

Date: 2026-10-27 (Asia/Bangkok). Backlog: G-008. Starting main: `66d3e36a4716b0dea332f141aeb38d14e1fd7d94` (031). No existing032 was present. Scope: one original-created tap renderer, one judged execution and one fresh no-input expiry execution. G-006/G-007 remain Blocked; neither investigation is resumed. No Expedition033 is initiated.

## Result and evidence classification

**Strong success, Native-integrated within the declared controlled environment.** Original traversal refreshes the native-created RenderTapNote, writes its position/quad, and exposes two distinct lifecycle outcomes. The judged renderer stops receiving refreshes because its logic leaves the active vector; the missed renderer is hidden by the original processed/depth predicate before active removal. Both remain retained, and neither is shown to be destroyed. G-008 is Verified for this bounded CPU lifecycle.

Original ARM64 instructions execute in each connected ordinary solo scene. No host invocation of the updater, model frame, acceptance, recorder or renderer visibility setter substitutes a native handoff. External AFF, catalog/profile/settings, clock and JNI coordinates remain controlled inputs. GPU pixels, physical-device timing, arbitrary renderer types and complete memory reclamation remain Unknown. Previous007 isolated updater findings are reused as instruction-backed leads, not mislabeled as earlier integrated execution.

## Preparation and reproducibility

Read the standing project introduction, cumulative context/backlog and relevant004/007–009/018–020/024–031 environment and rendering evidence. Inspected the published source and original ELF in the external read-only archive. Library member `lib/arm64-v8a/libcocos2dcpp.so` has SHA-256:

`3eaca4e6dabb3395f276f8915698d57675757d0df0970e716b23a3dc201c79be`.

All code addresses below are original ELF VAs. Object pointers in generated JSON are emulated allocations, compared by relationship rather than fixed values. Existing harness files matched their parent Git blob hashes before editing. Preparation diagnostics corrected two host observer assumptions: TrackLayer+3b8 is an embedded vector, and Node parent/children are+148/+140; no native dependency was repaired. A second observer correction records W1 at the forwarding stub rather than interpreting the overwritten X1 inside the updater as time.

The archive remains external; source package includes only the new synthetic fixture and Python observations/assertions. Python3.12, Unicorn2.1.4 and pyelftools0.33 are unchanged; Capstone5.0.7 was used only in an unpublished static inspection environment and is not a runtime dependency.

```bash
python3.12 -m venv /path/to/venv
/path/to/venv/bin/pip install -r research_harness/requirements.txt
/path/to/venv/bin/python research_harness/run.py \
  --archive /path/to/arccopy.zip --scenario cpu_note \
  --output /path/outside/research_harness/cpu-note-result.json
```

The CLI runs `judged_tap`, then `unjudged_expiry` in independent Uc/ELF/global/heap environments. The first run proves the refresh gate before JNI; only after its assertions pass does the fresh no-input run start. Generated output, private databases, binaries and inspection traces are not publication files.

## Native construction and legitimate refresh caller

The synthetic fixture contains timing0/120.00/4.00 and `(1500,3);`, with the standard header and no camera/scene-control events. Native whole-chart construction produces one LogicTapNote, raw3→internal lane4, N1/end1620, original spatial-index membership and enabled/registered gameplay listener. Original ordinary `ee197c→ee29a8→ee29e8`, loading callback and GameScene initializer return1 lead to Director activation of that same scene.

Original TrackLayer factory/initialization (`12970c4→ae6740`, initializer`12967e4`) creates an embedded renderer vector at+3b8/+3c0/+3c8: **503 RenderBars plus one RenderTapNote**, not the historical two-tap fixture's506 products. The tap renderer initializer `d7e290` returns1 to`ae69e0`; its vtable is`1acde18`. Logic+40 points to that renderer; renderer+2a8 points to the same logic. Renderer+2b8 identifies its original quad child, also present in the native Node child collection; child.parent points back to the renderer. The renderer itself has parent0. It does not need manual attachment: TrackLayer explicitly refreshes/visits renderers reached through active logic links.

The original visual-control owner at scene+300 references this TrackLayer at owner+2b8. TrackLayer's actual Node parent chain passes through a native Sprite3D to GameScene. Complete original base traversal reaches it after the original model/TrackLayer CPU graphical update:

```text
Director scene visitation → GameScene::visit18be2f8
  → original GameModel frame10a7550
  → 18be420 calls TrackLayer graphical update19069a0
  → 18be438 calls original Node::visit129c924
  → native child hierarchy/Sprite3D → TrackLayer::visit960288
  → 960308 calls b1638c
  → active logic+40 → renderer virtual+518 at b16468
  → cf2640 tail-forwards virtual+510 → f20c28
```

**The only changed runtime boundary is removal of the existing inert129c924 hook after native loading/activation, scoped to this scenario.** Full original traversal succeeds using existing services. There is no selective renderer call, new renderer/platform service, added PC skip or synthetic target. Older scenarios keep their existing traversal boundary.

`19069a0` receives model+a0, the original active-vector header, and stores it in TrackLayer+2c8. In `b1638c`, the original TrackLayer+3dc/Director+134 frame comparison limits each active renderer's refresh to once per Director frame, despite repeated camera visits. `cf2640` receives native E in W1; its `ldr x1,[vtable,#510]; br x1` overwrites that register with`f20c28`. The updater reads native logic depth; its raw X1 is not a usable E argument. Native LR remains`b1646c` through the tail branch.

## Position, geometry and lifecycle comparison

At E1000/1300/1499/1500, each run records one model frame, one TrackLayer graphical update and one tap CPU refresh per frame. Native placement is renderer X212/Y4/Z=current start depth, consistent with `425*(lane−1)−1063`. Cache writes and original Node position setters execute; the quad's four native vertices change from their initialized values to the native geometry. Representative quad at E1000: X±191, Y0/366, Z0. Geometry updates continue through the genuine caller, without host position or vertex writes.

Position write PCs include`d3d150/125441c`; quad writes include`9f2c90` and`f20fc8–f20ff8`. The JSON records exact write addresses, offsets, previous values and phases. Renderer Node opacity remains255/255 in these samples; visibility is a distinct byte. Initial renderer refresh count is0 before restoring traversal.

| Effective E | Native logic end depth, both runs | Judged run | No-input run |
|---:|---:|---|---|
|1000|−4044|Active, visible, refreshed|Same|
|1300|−1617|Active, visible, refreshed|Same|
|1499|−7|Active, visible, refreshed|Same|
|1500|0|JNI consumes once after frame|Unresolved, active, visible|
|1501|8|Removed from active vector; no further refresh|Active, visible, refreshed|
|1537|300|Retained renderer at last placement|Unresolved, active, visible|
|1538|308|Retained/visible; not offered for refresh|Processed predicate0, visible|
|1600|809|No extra judgment or refresh|No premature miss; processed0/visible1|
|1601|817|No extra judgment or refresh|Native miss once, processed1, visibility0|
|1602|826|Still retained, no refresh|Removed from active vector; no second miss/refresh|

**Judged case.** The original camera projects the input-plane lane4 center `(212.5,0,0)` to supplied JNI coordinates approximately`(775.8657837,617.3407059)` in the controlled1280×720 environment. These are derived anew, distinct from renderer's integer-quantized X212. Original JNI DOWN42→listener→candidate collector→classifier→acceptance`965e28`→recorder`1730290` selects the same native tap. Original consumed/contact-ID writes occur at`965e68/965e6c`. Result: PURE1/shining1/FAR0/LOST0, score10000001, health80.19999694824219. UP42 clears retained contacts, mapping and mask without another judgment.

The active updater's original condition near`10fd5f4–10fd608` combines processed state with strict E>end. E1501 removes the consumed tap. The renderer remains allocated, collection-retained, visible1/opacity255, and linked, but receives no subsequent updater/Node visit. Its position stays at the E1500 placement. **Native logic depth nevertheless continues advancing** through other original depth processing; removal from active processing is not frozen chart depth. Thus the isolated processed/depth hide rule is not exercised for this judged scheduling path.

**No-input case.** No JNI begin/end, acceptance or accepted recorder occurs. Native depth308 at E1538 passes the renderer's depth≥301 test, but the original logic processed virtual returns0 at`f20c9c`; the renderer stays visible. E1600 likewise stays unresolved. At E1601, original miss recorder`868e54` runs once under strict end+100 expiry; logic missed byte is written at`7e9968`. The same Director frame then refreshes the still-active renderer: depth817, processed virtual returns1, and`f20cb0` invokes native visible=false. Exactly one visibility0 write is observed at`18e18a4`. Native Node::visit subsequently tests visible0 at`129c954`. E1602 removes active membership, with no repeated miss, hide transition or per-tap refresh.

The two cases therefore prove different CPU culling mechanisms rather than requiring a common hide outcome. TrackLayer's render collection, chart ownership and reciprocal links persist in both; no renderer remove-from-parent/destructor is observed during the bounded interval. Hidden does not mean destroyed; active removal does not mean collection deletion. The original RenderTapNote base draw virtual is a no-op; native traversal/visibility filtering and quad CPU state do not establish GPU output.

An authoritative run observed emulated scene`0x4327c40`, model`0x4355c40`, chart`0x4331740`, TrackLayer`0x4368100`, logic`0x4332000`, renderer`0x4376400` and quad`0x4376740`. The two fresh allocators happen to reproduce these values; they are not shared objects or required constants. Tap-specific updater entries are5 in the judged case and10 in the expiry case. Native Node visibility tests see1 before expiry and0 in all four camera passes at E1601; no tap draw virtual is reached after that hide. No tap renderer visit occurs after its active removal.

## Boundaries, automated validation and preservation

Retained external services are the published libc/C++ABI, Android/JNI, catalog/profile/settings, clock/audio, original archive resource-provider and GL/platform interfaces. Allocator/autorelease and swap/framebuffer suppression remain. Original resources are loaded from the external ZIP; no proprietary resources are copied into source. No new timing, active-list, visibility, geometry, depth, group, consumption or score repair is supplied. G-006/G-007 diagnostic source, fixtures and Blocked statuses remain unchanged.

Exact inherited presentation PC ranges:

```text
f72110→f72158        16a4238→16a48d8    121581c→121584c
a507c4→a519ec        a51adc→a5213c      196fdac→196ffac
891190→89164c        891688→89219c      8921dc→8928e0
```

The final three are results-only and are not reached by this scenario. Original129c924 is restored only here; platform swap`1017a84` and framebuffer-registry-clear`13edf0c` remain controlled. GL imports remain supplied; no new GPU or hardware claim follows from reaching more original CPU code.

The new CLI automatically asserts original construction, graph links, chart count/index/listener/activation, authentic refresh caller and frame cadence, native position/quad writes, JNI candidate/acceptance/score/cleanup, absence of premature miss, processed/visibility divergence, single miss/hide, retained ownership and no direct host calls replacing native handoffs. Exceptions return exit1 with partial native observations. Two fresh runs stop at E1602 below chart end1620; ending/results/SQLite are not replayed for this fixture.

Validation uses a fresh Python3.12 environment and unchanged pinned dependencies. Fresh executions pass: new CPU-note two-case CLI; unchanged ordinary full-session/SQLite CLI; chord forward/reverse; moving/crossing arcs; timing-group/reverse-scroll. Existing unittest discovery passes all5 tests without skips: arc-tap, hold dual-case, unavailable-song native negative, missing archive and wrong binary hash. The blocked camera/fade diagnostics are preserved, not counted as successful regressions or reopened.

Publication changes only the new fixture/scenario, minimal config/CLI/own README additions, this report, append-only context and G-008/backlog history. Earlier fixtures/scenario assertions/dependencies/reports/root README and unrelated instructions remain unchanged. Historical context is an exact prefix. Commit/readback verification uses exact committed bytes, parent tree comparison and main ref verification; the final conversation returns the immutable SHA and pinned links. No generated outputs, traces, databases, assets, binaries, environments or secrets are committed.

## Runnable pseudocode

```text
for judged_tap, then fresh unjudged_expiry:
    verify external ELF hash; supply minimal AFF and existing services
    original ordinary solo entry → original scene/loading/chart/TrackLayer
    verify native tap ↔ RenderTapNote ↔ original quad
    restore original Node traversal after Director activation
    Director frames → model + TrackLayer graphical update
      → native hierarchy → TrackLayer visit → active logic renderer link
      → frame-stamped virtual forwarding → original CPU refresh/writes
    prove refresh/placement/geometry gate before input

    if judged:
        original camera projection → supplied JNI DOWN/UP
        original candidate/classifier/acceptance/recorder consumes once
        E1501 original active removal stops refresh/visit; renderer retained
    else:
        no input; depth≥301 alone leaves unresolved renderer visible
        E1600 no miss
        E1601 original miss → processed predicate1 → native hide once
        E1602 original active removal stops refresh; renderer retained

compare independent logic, refresh, visibility and ownership lifetimes
validate prior successful scenarios and negative tests
preserve G-006/G-007 blockers; update G-008; publish; STOP
```
