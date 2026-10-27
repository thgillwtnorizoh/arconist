# Expedition 034 — Native Continuous-Gauge State Producers, Temporal Updates & Failure Boundaries

Date: 2026-10-28 (Asia/Ho_Chi_Minh). Backlog G-010. Verified starting main: `626ef94e6652070762b0795e19d87067e8a33fd0`; no034 was present. G-006/G-007/G-009 remain Blocked; G-001–G-005/G-008 remain Verified. No Expedition035 is initiated.

## Result

**Blocked for both requested special modes; minimum scientific success through a precise producer dependency. G-010 is Blocked — Expedition 034.** The existing ordinary no-ability fixture produces native mode0 ScoreState/LifeBarState and handles original frames/JNI scoring. It does not provide an initialized, owned Character35 or98. Each target producer phase inspects a fresh unchanged environment, identifies the missing account/character input contract and stops **before attempting target selection or constructing an ability**.

Neither special activation, selector, ScoreState/LifeBarState initialization, temporal branch, `expf`, failure nor completion is executed. No unavailable character is unlocked and no gauge number, H/F/p/accumulator/cap or ability pointer is assigned. A successful ordinary subcase does not turn the overall research gate into a passing special-gauge regression. The new CLI returns exit1/`status: fail`/`NativeContinuousGaugeProducerBlocked`.

New evidence includes the native ordinary selection-to-gauge write chain; deliberate native zero producers distinct from supplied allocator zeroing; the enriched character-stat/account join required upstream of the skill factory; conditional Insight profile/session dependencies; and correction of a misidentified selector address. Earlier006 isolated gauge/failure arithmetic retains its stated scope.

## Preparation and evidence identity

Read the standing introduction, latest context/backlog, complete006 and relevant008/010/013–015/018–024 plus current025–033 execution/producer-boundary evidence and source. Existing local repository files matched parent Git blob hashes before editing. Original ZIP and resources remain read-only.

Original member `lib/arm64-v8a/libcocos2dcpp.so` SHA-256:

`3eaca4e6dabb3395f276f8915698d57675757d0df0970e716b23a3dc201c79be`.

All code/data addresses below are original ELF VAs. Object pointers in JSON are emulated allocations, checked relationally. Python3.12/Unicorn2.1.4/pyelftools0.33 pins are unchanged. Capstone5.0.7 was used only for unpublished targeted disassembly, not added as a package dependency.

## Archived catalog versus selected account state

Unmodified `assets/char/characters.json` contains100 records:97 have `is_available:false`, three true (IDs2/3/4). Selected factual records:

| ID | Name | Skill | char_type | Unlock level | Bundled is_available |
|---:|---|---|---:|---:|---|
|35|tairitsu_tempest|gauge_tempest|2|0|false|
|98|insight_konzetsu|skill_insight_konzetsu|4|0|false|
|49|lily|skill_lily|0|0|false|

**External supplied input:** existing `prepare_app` allocates a character49 shell, writes its ID, links it at account+58 and leaves vtable/ability0. This is not original Character/Lily-ability initialization or proof of a real account entitlement. Ordinary mode0 execution remains valid within that declared no-ability boundary.

**Observed bounded input state in each fresh environment:** account+18 owned-character vector is empty, account+68 fallback pointer is0, selected character+0c is49 and +d0 is0. Merely changing that ID to35/98 would not produce a Character or its skill and is not attempted.

`is_available:false` is preserved but **not equated to an executed activation/entitlement rejection**. Character49's archived record is also false. No executed character-availability consumer establishes that catalog boolean as the deciding gate here. Its complete character-selection meaning remains Unknown. Original base activation instead has explicit level/unlock/awakening/session checks. The precise current blocker is missing initialized account-owned character state, not a demonstrated false-bit rejection.

## Native character/ability producer contract

**Instruction-backed, not executed for targets:** `96b358` first reads a record's `character_id`, gets the account through`b688e0`, searches account+18 objects by character+0c (`96b46c–96b4a8`) and otherwise uses account+68 (`96b4ac`). If that pointer is null, `96b58c→96b424` skips the record. This function updates an existing owner; the catalog record alone is not that owner.

Its input is an **enriched current-character stat record**. Native key reads include `frag`, `prog`, `overdrive`, `level`, `exp`, `skill_unlock_level`, `char_type` and `skill_id`. The archive instead supplies base/max statistics and has no current `frag/prog/overdrive/level/exp` for either target. Original callers include `value.character` at`ff9664` and `value.characters` at`c451f4`. This is a materially different contract from passing the bundled base-stat array directly to the updater.

After ownership/stat resolution, `96c0d8→100ec3c` stores statistics at character+ac/+b0/+b4 and level/unlock/awakening-related fields. The inspected alternate callsite`16f79e0` also updates an existing character using existing metadata and session state; it is not a recovered account ownership producer. Skill assignment at`96c5fc` (and alternate string-selection branch`96c680`) calls`a44128→7ac3cc`; `a4415c` stores the returned ability at character+d0.

| Target | Original skill branch / factory | Concrete ability vtable/type | Selector |
|---|---|---|---|
|Tempest35|`7ad6dc–7ad700 → ca5ec8`|`1ac18f0`, CharacterAbilityTempestGauge|`179727c`: return6|
|Insight98|`7aed34–7aed58 → af8734`|`1b5a168`, CharacterAbilityInsightKonzetsu|`1003b90`: return11|

Both inspected factories allocate0xa0, construct the base ability, install their original vtable and call their native initializer. This is **Instruction-backed**, not new factory execution. Both activation virtual+18 entries resolve to`118e220`; acceptance wrapper`9e979c` requires return exactly1. Base checks include w3=3/4 rejection, w4=2 rejection, character level<unlock rejection, and unmet awakening requirements; later filters remain original. No missing account level or awakening state is invented to pass them.

Actual solo selection uses character+d0 at`ee25e4`; if non-null, `ee2638` calls acceptance and `ee2644/ee264c` dispatches ability virtual+58. **Address-role clarification:** in this exact ELF, `13b5c2c` is a factory for `SpecialSceneArcahvChallenge` (vtable`1b022d8`), not the ability gauge selector. That unrelated special scene is not invoked or investigated. Historical reports are not edited.

The single substantial missing producer prerequisite for each target is a justified account-owned Character/stat input and original materialization/update chain. No authentic target account rows or current stats are supplied. Reconstructing ownership/unlock/account startup to manufacture them would exceed the bounded task. Target selection is therefore NOT RUN; the missing-owner edge is an instruction-backed consequence of the observed source state, not a fabricated executed rejection of35/98.

## Ordinary native control: selection, ownership and original writes

**Native-executed:** unchanged `sayonarahatsukoi`/difficulty0/set base, ordinary synthetic two-tap AFF and speed40 pass original solo eligibility and reach `ee29a8→ee29e8`. Original loading invokes GameScene initialization, returning1; Director activates that same scene. The account/character getter itself remains supplied.

At`ee25e8`, original code observes the supplied character49 ability pointer0, takes`ee25ac` and produces W27=0. No acceptance/selector executes. Original writes then preserve the mode and null ability:

| Original writer | Produced state |
|---|---|
|`e4e598`|GameScene+324 mode0|
|`e2eae4`|GameScene+330 selected supplied character|
|`e2ecd0`|GameScene+338 ability0|
|`fbfd5c` / `fbfe34`|GameModel+144 mode0 / +80 ability0|
|`13e0100` / `13e00f4`|ScoreState+94 mode0 / +c8 ability0|
|`160a3fc` / `160a3f8` / `160a400`|LifeBarState+a0 gauge0 / +a8 original ScoreState owner / +c8 ability0|

Original `1905bc8` mode-map initialization is reused; read-only inspection confirms0→[0],6→[6],11→[11]. This is native numerical support, not target selection. Native `14f0a94→13e00b4→12c5070→160a3b8` constructs the score/gauge, with initializer return1 and intact chart/owner/vector relationships.

An observed ordinary run has emulated scene`0x4327c40`, model`0x4356040`, chart`0x4331980`, score`0x4356200` and gauge`0x4356380`; these are examples, not required allocation constants.

**Zero provenance:** the supplied allocator initially returns zeroed memory, recorded separately. Original factory bulk stores`12c50c4` then deliberate defaults`12c5144` zero the20..3f region; `12c5148` zeros threshold/recovery storage. `12c50f8` enables continuous updates while leaving caps disabled; initializer`160a468/160a76c` writes H/base gain. Original judgment writes include`133fb50` and peak/trough`133fc8c`; original time write`83ddb0` advances last-update E. These are native writes, not Python gauge assignments.

Director-driven samples and original camera-derived JNI DOWN42/UP42:

| Effective E | H | Last-update E | Observation |
|---:|---:|---:|---|
|−3000 activation|0|0|Native ordinary construction, no target ability|
|500|0|500|No-input ordinary frame|
|1000 before input|0|1000|First tap available|
|1001 after JNI|40.20000076293945|1001|PURE1/LOST0, score5000001; contact map/mask/retention empty|

Six original model frames call `a126f4→83dd70`, with LR`10a78f8`/`a12734`. Ordinary p/accumulators/F remain0, U100/caps-disabled and finish0. Neither mode11 branch`83ddd8`, mode6 branch`83df48`, `expf`, special selector/factory/activation, miss, completion nor snapshot runs. An ordinary gauge receiving a judgment and a common updater is **not** evidence of Tempest or Insight continuous behavior.

## Mode6 field producers and remaining gate

**Instruction-backed for mode6:** the common native factory deliberately initializes p and special accumulators to0 before calling the initializer. There is no p argument in the inspected factory/initializer interface. Mode6 gain initialization reads the stored p at`160a728`, writes baseline at`160a750`, conditional accumulator at`160a764`, then gain at`160a76c`. This narrows the initial producer beyond “zero because supplied memory happened to be zero.”

It does **not** establish a valid Tempest session or exclude later p writers/ranges. Current execution observes those defaults only on gauge0. Optional enriched-record `prog_tempest` is separately subtracted from `prog` at`96b780` before character-stat storage; no equivalence to LifeBarState p is established.

The original `83df48` temporal branch consumes baseline/pending positive/negative/override state, calls `expf` twice and updates H/accumulators. Its computation is not newly replayed here because the Character35 producer gate fails. Mode6 temporal trajectory, native failure and the historical completion+6000 boundary are **NOT RUN**. No p, baseline, health or time value is injected to reach them.

## Mode11 conditional external-state contract

**Instruction-backed, not executed:** additional initialization begins at`160a474`. Its first query`160a484→126dc1c` tests App+e0 context word+38. If false, the profile lookup is skipped and the local count starts at0. The observed ordinary context has word+38=0; this is a source-state observation, not execution of a mode11 branch.

When the context predicate is true:

- `bda064` supplies the **session/context mode**, a namespace distinct from gauge ID6/11.
- `1223ad4` reads settings key`insightChallengeDefaultDifficulty` and converts it through original code.
- `18e2d6c` forms decimal(context mode)+`deinosphaineinRelief` and reads an integer from App+28 via`9e59e4`, with the supplied default. If context mode0, that helper itself returns0.

The initializer derives a rate at gauge+74; `160a674/160a678` set U100/cap-enabled. Only **context mode6** additionally invokes`a3b33c(songId)` and transfers the returned timing-window vector at+48 into gauge+50 (`160a624`). The per-frame `83dd70` branch uses that vector and fields+68..+84 to evolve cap/health.

The profile key's authoritative value writer, exact product/World semantics and special-session vector producer are not reconstructed. They are not supplied as guessed World progress. The evidence establishes **conditional profile/session dependencies**, not an unconditional need to rebuild World state for an ordinary context. Mode11 is blocked earlier by the missing owned Character98 chain; its initializer/cap/health/failure behavior is NOT RUN. A second major subsystem is not reconstructed.

## Reproduction, tests and scientific boundaries

```bash
python3.12 -m venv /path/to/venv
/path/to/venv/bin/pip install -r research_harness/requirements.txt
/path/to/venv/bin/python research_harness/run.py \
  --archive /path/to/arccopy.zip --scenario continuous_gauge \
  --output /path/outside/research_harness/continuous-gauge-result.json
# Expected exit1/status fail/NativeContinuousGaugeProducerBlocked.
```

New `src/continuous_gauge.py` records the ordinary native branch/creation/write/time/JNI evidence, mode-map and ownership observations, then two fresh **producer-input audits**. The target phases do not pretend to run special selection. Their metadata is read unchanged from the external ZIP; static ability contracts are labeled; actual selector/activation results and special objects/parameters are null, with temporal/failure/completion explicitly `not_run`. Partial evidence survives unexpected errors. No new fixture, ABI service, math implementation or skip is introduced.

Retained external services: controlled account/catalog/profile/settings/application storage; strings/RTTI/streams/math/libc/C++ABI; Android/JNI and clock; original resource-provider bytes/CSB/font support; graphics/audio; allocator/autorelease and swap/framebuffer boundaries. Native ordinary eligibility, construction, model frames, recorder/gauge arithmetic remain original. No production account, real Android scheduling, GPU, audio-device or complete reclamation claim follows.

Exact inherited PC skips, unchanged:

```text
f72110→f72158        16a4238→16a48d8    121581c→121584c
a507c4→a519ec        a51adc→a5213c      196fdac→196ffac
891190→89164c        891688→89219c      8921dc→8928e0
```

Results-only final three are not reached by this new short control.032 restores original Node traversal only in its own CPU-note scenario; that behavior is preserved.

Fresh validation: the new diagnostic reproduces the intended blocker, with its ordinary subcase passing. Unchanged ordinary full-session/results/SQLite, chord forward/reverse, moving/crossing arcs, timing-group/reverse-scroll and CPU-note refresh/expiry CLIs pass. Existing unittest discovery actually invokes arc-tap and hold dual-case CLIs plus unavailable-song, missing archive and wrong binary hash: all5 tests pass without skips. Camera-reset, track-fade and flick-producer expected-failure diagnostics remain unchanged, are not reopened/rerun and are not counted as green gameplay regressions.

## Publication and preservation

Only authorized changes: new gauge diagnostic source, minimal harness config/CLI/own README additions, this report, append-only context and G-010/backlog history. No previous fixture/test/assertion/dependency/report, historical context, root README/instruction or blocked diagnostic is modified. No archive/library/resource extract, character asset, generated JSON/trace, database, memory dump, environment, account data or secret is committed.

Main/034 absence are rechecked before publication. Parent/child tree allowlist, historical context prefix, prior-fixture/assertion blobs and exact committed-file readbacks are verified. The final headquarters return supplies the immutable commit SHA and pinned report/context/backlog links. Stop with both requested producer gates Blocked, without Expedition035.

## Pseudocode — observed and gated paths

```text
verify external ELF; read unchanged character catalog
ordinary_control in fresh native runtime:
    existing supplied character49 has no ability
    original solo code observes null ability → native mode0
    original loading → GameScene → model → ScoreState → LifeBarState0
    observe original owner/mode/default writes
    Director frames → original ordinary gauge updater
    camera-derived JNI DOWN/UP → native PURE and ordinary health gain
    verify cleanup; stop before completion

for target35/gauge6, target98/gauge11, each with fresh fixture:
    read actual archived record and unchanged account boundary
    owned-character rows absent; fallback null; selected shell49
    inspect original metadata/stat/ability/activation contracts
    do not invent missing owned character or current stats
    mark target selection/ability/gauge/temporal/failure NOT RUN

record native factory defaults separately from hypothetical special state
record conditional Insight profile/session interfaces as instruction-backed
run previous successful regressions and negative tests
preserve G-006/G-007/G-009; mark G-010 Blocked; publish; STOP
```
