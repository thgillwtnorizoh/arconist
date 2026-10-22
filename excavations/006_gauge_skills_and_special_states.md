# Expedition 006 — Gauge, Character Skills & Special Gameplay States

Date: 2026-10-22. Repository: `thgillwtnorizoh/arconist`, existing branch `main`. This investigation is limited to Expedition 006.

## Result

Recovered and executed the principal chain **accepted/missed judgment → LifeBarState update → frame failure or final GameResult classification**. Recovered the note-count-dependent gain equation, mode-dependent damage, native clamping and failure sentinels, staged gauges, representative character-skill construction and effects, score-based clear classification, expanded scoring-cap writers, final snapshot fields, and concrete local persistence routines.

The core chain is substantially reconstructed. The complete skill catalog, continuous Tempest/Insight behavior, every special-scene transition, and every result-saving eligibility gate remain incomplete. This is disassembly and isolated ARM64 execution of the supplied binary, not real-device validation or a recreation of the full game.

## What I Found

### 1. Sources, conventions, and preservation

The authoritative `Introduction-and-the-scheme-of-this-project.txt`, ZIP inventory, current `context.md`, and Expedition 001–005 reports were consulted before the new investigation. Relevant preliminary findings were checked against the supplied archive. No external Arcaea gameplay description was used as implementation evidence.

- Primary evidence: `arccopy.zip` → `lib/arm64-v8a/libcocos2dcpp.so`.
- SHA-256: `3eaca4e6dabb3395f276f8915698d57675757d0df0970e716b23a3dc201c79be`.
- ELF Build ID: `17d660edbf37ca78beefc32e07672c97419ddce6`.
- Extracted primary-library bytes were compared with the ZIP member. The ZIP contains 9,658 entries and no `.aff` chart samples.
- **Every native address in this report belongs to that main library and is a library-relative ELF virtual address before relocation.** Cited code/rodata VAs equal file offsets. In the cited `.data.rel.ro`, file offset is VA minus `0x4000`; vtables and GOT pointers require relocation interpretation.
- **Confirmed:** original instructions, archive metadata, relocation-backed RTTI/vtables, or explicitly scoped native execution. **Interpretation:** explanatory meaning supported by that evidence. **Unknown:** insufficiently established provenance, lifecycle, or product meaning.
- C++ class names below are recovered RTTI names. Routine and field labels such as `baseGain`, `hardPhase`, and `expandedCap` are researcher-assigned descriptions, not recovered source symbols. Vtable offsets are bytes from the address point.

Earlier documentation is preserved. The previously authorized curve-ID and depth-cutoff corrections were reviewed and are not reopened. This report extends Expedition 002's intentionally omitted gauge callbacks and previously unnamed special score flag; it does not change its ordinary score formula. No new contradiction requiring an earlier-file correction was established.

### 2. The instruction-backed chain and ordering

| Mechanism | Entry / decisive instructions | Observed behavior |
|---|---|---|
| Accepted recorder | `0x1730290`; note guard `0x17302e8`; gauge call `0x1730350` | Note virtual `+0x20` must accept. ID 0 increments shining PURE and PURE; ID 1 PURE; ID 2 FAR. Then every LifeBarState receives the judgment. |
| Miss recorder | `0x868e54` | Note virtual `+0x38` must accept. Increments LOST, visits every gauge through `0x1869e90`, then resets combo. |
| Accepted gauge handler | `0x16e4ab0` | Computes gain/damage, invokes ability hooks, tail-calls `0x133fac8`. |
| Miss gauge handler | `0x1869e90`; damage call `0x1869efc` | Computes weighted damage through `0x120dd34`, invokes ability hooks, applies it through `0x133fac8`. |
| Core application | `0x133fac8` | Stores live health, handles caps and special postprocessing; does not terminate gameplay itself. |
| Per-frame update | `0xa126f4` → `0x83dd70` | Updates continuous gauge behavior, pending changes, and score consistency. |
| Failure decision | Frame `0x10a7550`, block `0x10a7d74–0x10a8018` | Mode-dependent threshold test; immediate finish or grace continuation. |
| Final snapshot | `0x1600bb0` → factory `0x180e994` → initializer `0xcab7fc` | Creates and caches a GameResult; health is floored to signed integer. |
| Final classification | `0x12a5574` | Produces result codes 0–5 from health/mode/counters or a score-clear ability. |

**Confirmed ordering:** accepted counters change before gauge/ability callbacks; score helper `0xe43b80` is called later at `0x1730504`; combo increment/max-combo bookkeeping follows. A skill's gauge hook can therefore see the new PURE/FAR counts and the previous combo. The miss handler increments LOST before its gauge callbacks and resets combo afterward. A rejected note guard leaves the tested counters and health unchanged.

Long-note checkpoint processing in `0xf8056c` sums pending record weights and calls the recorders **once per judgment unit** (`0xf809a4`, `0xf80bd8`), rather than applying one large gauge delta. A weight-2 checkpoint consequently produces two callbacks and two clamp operations. `0xc6e938` supplies overdue-unit counts. This extends the Expedition 002 checkpoint findings without changing them.

### 3. Relevant object layouts and authoritative state

`ScoreState`: RTTI typeinfo `0x1b10180`, vtable `0x1b35178`; factory `0x14f0a94`, initializer `0x13e00b4`, allocation size `0xf8`.

| Offset | Type / recovered use |
|---|---|
| `+0x0c` | signed i32 total judgment units, N |
| `+0x10/+0x14` | i32 maximum combo / recorded score |
| `+0x18/+0x1c` | score consistency cache / current combo |
| `+0x20/+0x24/+0x28/+0x2c` | i32 shining PURE / PURE / FAR / LOST |
| `+0x60/+0x68` | LogicChart pointer / cached GameResult pointer |
| `+0x94/+0x98` | selected gauge mode / active gauge-vector index |
| `+0xa0/+0xa8/+0xb0` | vector begin / end / capacity of LifeBarState pointers |
| `+0xc8` | CharacterAbility pointer |
| `+0xd0` | expanded score-cap flag |
| `+0xd1` | selects recorded LOST rather than N−PURE−FAR at finalization; producer unresolved |
| `+0xd2` | copied as a nonzero-health requirement flag into GameResult `+0xb3`; producer unresolved |

`LifeBarState`: RTTI typeinfo `0x1b7d788`, vtable `0x1ad3848`; factory `0x12c5070`, initializer `0x160a3b8`, allocation size `0xd8`.

| Offset | Type / recovered use |
|---|---|
| `+0x0c` | disabled/dormant byte; direct judgment/application routines return when set |
| `+0x10` | **f32 live health H** |
| `+0x14/+0x18/+0x1c` | f32 lower bound L / upper cap U / cap-enabled byte |
| `+0x1d` | continuous-update enabled byte |
| `+0x20` | f32 Tempest parameter p; production not fully recovered |
| `+0x24/+0x28/+0x2c/+0x30` | Tempest floor / override / baseline / accumulator fields |
| `+0x34/+0x38` | pending positive / negative mode-6 terms |
| `+0x40` | f32 failure threshold F, distinct from H |
| `+0x44` | pending recovery processed per frame |
| `+0x48/+0x4c` | f32 peak / trough health |
| `+0x88` | caller-supplied damage/weight-control flag; full product meaning unknown |
| `+0x8c` | f32 per-unit base gain g |
| `+0x98` | signed i32 damage percentage, normally 100 |
| `+0xa0/+0xa8` | numeric gauge ID / owning ScoreState pointer |
| `+0xb0/+0xb4` | configuration argument / last update chart time |
| `+0xb8/+0xb9` | hard-phase flag / deferred-hard or grace flag |
| `+0xc8` | CharacterAbility pointer |

H and F are used directly by native failure decisions. They are not merely HUD percentages. The HUD routine `0x1713a64` reads the active gauge's H/F/cap at `0x1713f5c–0x1713fc0` and passes them to `0x178d4fc`; its own presentation caches are downstream. Score-clear skills can overwrite H with a score-derived visualization, while their final clear rule independently uses score.

### 4. Initialization and exact gain equation

Factory defaults include L=0, U=100, cap-disabled, continuous-update enabled, damage percentage 100, and zeroed special accumulators. `0x160a3b8` accepts an explicit signed initial-health argument: **−1 is the default-selection sentinel**; other values are converted to f32, rather than silently clamped at initialization.

With the sentinel, IDs `{2,6,7,8,9,11,12,13,14}` start at 100 unless ability virtual `+0x48` returns a positive replacement. Other IDs start at the ability's returned value, or 0 without an ability. Thus the traced ordinary/easy/overflow defaults are 0 and hard is 100. Mode 11 then performs additional account/world-state-dependent configuration (`0x160a474–0x160a678`), not dynamically validated here.

`0x160a67c–0x160a76c` derives g from signed chart count `LogicChart+0xb8`. For positive N, preserving each f32 operation:

```text
T = f32(200 + f32(f32(N) * 0.5))                    if 1 <= N <= 399
T = f32(280 + f32(f32(N-400) * 0.5))                if 400 <= N <= 599
T = f32(360 + f32(f32(N-600) / 5))                  if N >= 600
Q = f32(T / 2.5)
if byte[chart.song(+0x18) + 0x54] != 0:
    Q = f32(f64(Q) * 0.8)                          # double constant at 0x418b98
if gaugeID == 6:
    baseline = f32(Q * f32(1-p))
    if baseline < 100: accumulator = f32(100-baseline)
    Q = f32(Q * f32(2-p))
g = f32(Q / f32(N))
```

The song byte's scaling effect is confirmed; its product meaning is **unknown**. Do not silently rename it as difficulty, World mode, or a character statistic. The native routine selects T=0 for N<1 but still divides by N; valid positive-count charts were the test scope.

Selected native results, song flag zero and mode 0:

| N | g |
|---:|---:|
| 100 | 1.0 |
| 399 | 0.4005012512 |
| 400 | 0.2800000012 |
| 599 | 0.2534223795 |
| 600 | 0.2399999946 |
| 1,000 | 0.1759999990 |
| 2,000 | 0.1280000061 |

The discontinuities at 400 and 600 are instruction-backed; this report does not replace them with a smoother remembered formula.

### 5. Judgment gain, damage, and type identity

Without an ability, accepted handler `0x16e4ab0` uses gain g for IDs 0 and 1, and g/2 for ID 2. With the ordinary default `+0x88=0`, ordinary accepted judgments have no damage. IDs 0 and 1 therefore differ in score/shining count, not ordinary gauge gain.

Exceptions directly decoded and executed:

- Gauge 8 forces all accepted gain to zero after ability callbacks.
- Gauge 12, ID 1: zero gain and damage 2, with lethal-damage protection.
- Gauge 12, ID 2: retains half-gain and computes damage with base weight 1.
- Gauge 13, ID 2: retains half-gain and computes damage with base weight 0.5.
- Without an ability, a nonzero `+0x88` adds 0.5 to the FAR weight above and enables a weight-0.5 damage call in other IDs. This flag's full caller-side meaning remains unresolved.
- In the last two cases, flag `+0x88==0` enables protection; when protected damage is at least current H, it becomes `f32(max(0, f64(H)-0.5))`. This protects against that accepted judgment's damage, not every possible failure source.
- Miss weight is 2 for IDs 12/13, otherwise 1.

**Important type boundary:** `0x1869ecc–0x1869ef4` and `0x16e4d0c–0x16e4d30` compare the runtime RTTI **name pointer for equality** with `LogicLongNoteBase` typeinfo `0x1af6c48` via GOT `0x1b964e0`. This is not a `dynamic_cast` accepting every subclass. The name pointers for `LogicHoldNote` (`0x1b44168`) and `LogicArcNote` (`0x1b123e0`) differ. Native tests using their actual vtables `0x1b2eda8` and `0x1b91500` take the nonmatching path. Consequently, do not automatically call the reduced-damage branch “all holds/arcs.” Below, **E** means this literal exact-name match; **non-E** includes the tested derived-class identities. Checkpoint counts and this damage predicate are separate mechanisms.

#### Damage helper `0x120dd34`

The following default **base D** table applies with no ability override, no hard/grace promotion, and ordinary finite state:

| Gauge ID | D before weight/type scaling |
|---:|---|
| 0, 3, 4, 10 | 1 |
| 1 | f32(0.6) |
| 2, 9, 11, 13, 14 | H>30 ? 4.5 : 2.5 |
| 5 | f32(0.6) before hard phase; H>30 ? 4.5 : 2.5 after it |
| 6 | f32(9 + f32(p * −6.5)) |
| 7 | H>30 ? 5 : 2.5 |
| 8 | fixed 10, suppressing ordinary weight/type scaling |
| 12 | **4.5, including below 30** |

Evidence includes jump-table bytes at `0x42ed5a` / `0x42ed63` and branches `0x120dde0–0x120df9c`. The shared hard-phase flag can promote default damage paths; mode 10's `+0xb9` also selects hard-style D. Avoid treating this table as all skill overrides.

After the ability base-D override and loss multiplier, normal damage is D×weight, optionally scaled by signed percentage/100. It is doubled for non-E notes, except the fixed-condition/mode-8 branch. Mode 7 doubles even for E. **A non-1 base-D override alone does not suppress weight or doubling**: `0x120ddd8` skips the mode table, but the fixed-condition flag used at `0x120de64–0x120deac` is separate.

For modes 2/7/9 and mode 10 with `+0xb9`, when old H>30 and the tentative new value is <30, and the fixed-condition flag is false:

```text
tentative = f32(H - scaledDamage)
tentative = f32(f64(tentative) + f64(f32(H-30)) * 0.5)
returnedDamage = f32(H - tentative)
```

Equality at 30 does not enter that correction. The helper returns H−tentative, so cancellation rounding is retained. At old H=31, mode-2 non-E LOST leaves 22.5 before core clamping; at H=30 it leaves 25. E counterparts leave 27 and 27.5. This unusual boundary was executed, not normalized into a conventional hard-gauge model.

At H=50, no ability, g=0.1, percentage=100:

| Mode | PURE H | FAR H | LOST H non-E | LOST H E |
|---:|---:|---:|---:|---:|
| 0 | 50.0999985 | 50.0499992 | 48 | 49 |
| 1 | 50.0999985 | 50.0499992 | 48.7999992 | 49.4000015 |
| 2 | 50.0999985 | 50.0499992 | 41 | 45.5 |
| 6, p=0 | 50.0999985 | 50.0499992 | 32 | 41 |
| 7 | 50.0999985 | 50.0499992 | 40 | 40 |
| 8 | 50 | 50 | 40 | 40 |
| 12 | 50.0999985 | 41.0499992 | 32 | 41 |
| 13 | 50.0999985 | 45.5499992 | 32 | 41 |

Here g was explicitly set for dispatch tests; mode-6 initialization normally changes g as described earlier.

### 6. Core clamping and continuous state

`0x133fac8` first computes `x=f32(f32(H+gain)-damage)`. For tested finite bounds with L≤100:

- If cap-enabled and U>100, H=`max(L,min(U,x))`.
- Otherwise H=`max(L,min(100,x))`.
- After ability postprocessing, cap-enabled performs another `H=min(U,H)`, including when U<100.

Thus U is not necessarily a visual-only ceiling. Failure writes H=−1 elsewhere, deliberately bypassing this lower clamp. Disabled `+0x0c` objects ignore the core application. Peak/trough values are updated after postprocessing.

For mode 6, the routine also accumulates gain at `+0x34` and subtracts damage into `+0x38`. `0x83dd70` later applies continuous/accumulated behavior, including `expf` and fields `+0x20–+0x38`; the complete differential behavior and all state producers were not reconstructed or executed. Mode 11 additionally changes a cap using account/world-dependent initialization and per-frame state. These are genuine gameplay variables, not evidence for a fully recovered skill algorithm.

Pending recovery `+0x44` is processed separately per frame, bounded by 60×dt (mixed double/f32 arithmetic), with an ability callback before applying the recovered amount. It is not proof that all ordinary judgment gain is delayed.

For mode 9, the post-update routine stores a moving failure threshold:

```text
r = f32(f32(PURE) / f32(N))
F = f32(f32(r * f32(r*70)) + 0.0)
```

This is checked against live H in the frame loop; it must not be confused with a universal fixed zero threshold.

### 7. Supported IDs, staged gauges, and immediate failure

Score initialization uses global mode→gauge-vector map `0x1bf9648`, populated by `0x1905bc8`. Executing its initializer with map insertion captured gives:

```text
0..11 -> [same ID]
12    -> [12,13,14]
13    -> [13,14]
```

There is no outer map entry 14; 14 is an internal fallback stage in these configurations. Recorders update every non-disabled gauge, not just the active one. After judgment processing, selected modes 12/13 disable an exhausted active gauge and advance the index by at most one if a successor exists (`0x173035c–0x17303b0` and the miss counterpart).

Synthetic native example: mode 12 with gauge IDs `[12,13,14]`, H=`[1,100,100]`, one non-E LOST gives H=`[0,82,91]`, disables the first state, and selects index 1. The successor was already taking damage before becoming active.

| ID | Verified association | Default H | HP-threshold finish branch |
|---:|---|---:|---|
| 0 | Base/ordinary selector | 0 | No |
| 1 | `gauge_easy` | 0 | No |
| 2 | `gauge_hard` | 100 | Yes |
| 3, 4 | Numeric modes; product semantics unresolved | 0 | No in this branch |
| 5 | `gauge_overflow` | 0 | Only after model `+0x13b` |
| 6 | `CharacterAbilityTempestGauge` | 100 | Yes |
| 7, 8 | Special numeric modes; product names unresolved | 100 | Yes |
| 9 | `CharacterAbilityFatalis` | 100 | Yes, moving F |
| 10 | `CharacterAbilityInsight` | 0 | Only after model `+0x13c` |
| 11 | `CharacterAbilityInsightKonzetsu` | 100 before extra configuration | Yes |
| 12, 13 | `CharacterAbilitySayaKonzetsu`, conditional selector | 100 | Yes, active stage |
| 14 | Internal stage | 100 | No outer-ID-14 branch |

Associations 6/9/10/11 are backed by overridden gauge-selector functions `0x179727c`, `0x889a18`, `0x1581ccc`, `0x1003b90`; Saya selector `0x9f3cc4` returns 12 or 13 after an external condition. Those associations do not establish every effect named by each class.

Frame failure conditions (`0x10a7d74`):

1. Select the applicable mode branch above; inspect active H and F.
2. If H>F, continue. If already finished (`model+0x139`), do not finish again.
3. At **H≤F**, when scene `+0x34d` is clear: write H=−1 to **all** gauges, disable their continuous updates, call delegate virtual `+0x10(true)`, set finished.
4. When scene `+0x34d` is set and the grace latch `model+0x140` is clear: set grace and `model+0x13c`, set every gauge's `+0xb9`, set every U to the **same failed active H** and enable caps; do not call the finish delegate in this branch. Repeated entry with the grace latch set also does not immediately repeat a finish callback.

Ordinary/easy H=0 therefore does not cause this mid-song failure. Native hard H=0 without grace does. A direct final classifier call with survival H=0 can still pass unless `GameResult+0xb3` requires nonzero H: normal runtime failure usually converts H to −1 first. These are different observations, not contradictory rules.

**Overflow:** `0x10a78f8–0x10a79a4` checks active H≥100 in mode 5 and, once only, sets model `+0x13b` and every gauge `+0xb8`; then issues an audio event. This changes damage to hard-style processing and enables threshold failure. Before activation, it uses easy-style loss and has no HP-finish branch. Equality at 100 activates; 99.999 does not.

**Insight mode 10:** `0x10a79d0–0x10a7b2c` includes a strict elapsed-time > quarter-chart-duration transition, sets `+0x13c`, propagates `+0xb9`, and caps gauges to active H. This static transition was traced, but its complete skill lifecycle was not tested.

### 8. Character metadata, selection, and hooks

Archive path **`assets/char/characters.json`** contains 100 records and 88 distinct base `skill_id` values including the empty value. Examples checked directly:

| character_id / name | char_type | skill_id | skill_unlock_level |
|---|---:|---|---:|
| 0 / hikari | 1 | `gauge_easy` | 0 |
| 7 / tairitsu_grievous_lady | 2 | `gauge_hard` | 0 |
| 14 / hikari_zero | 2 | `challenge_fullcombo_0gauge` | 8 |
| 15 / hikari_fracture | 3 | `gauge_overflow` | 0 |
| 20 / eto_luna_winter | 1 | `gaugestart_30\|gaugegain_70` | 0 |
| 34 / doroc | 0 | `scoreclear_aa\|visual_scoregauge` | 0 |
| 35 / tairitsu_tempest | 2 | `gauge_tempest` | 0 |

The displayed backslashes escape Markdown table separators; they are not in the asset strings.

JSON loader `0x96b358` reads `skill_unlock_level` (`0x96b8a4`), `char_type` (`0x96b8d8`), `skill_id` (`0x96c398`), and optional `skill_id_uncap` (`0x96c3f0/0x96c478`). It selects an alternate skill under awakening/nonempty-string conditions; all account-dependent alternatives are not reconstructed. Character initializer `0x100ec3c` stores type at `+0xb8`, level/unlock at `+0xc0/+0xc4`, awakening requirements/state at `+0xc8/+0xc9`, statistics at `+0xac/+0xb0/+0xb4`, and an ability pointer at `+0xd0` via `0xa44128` → whole-key factory `0x7ac3cc`.

Factory comparisons match **complete strings**, including compound keys containing `|`. This investigation did not establish a general grammar that splits arbitrary skill strings into composable effects.

Selection chain:

```text
selected account character (+0x58 from 0xb688e0)
 -> scene +0x330 selected character (0xe2ea48)
 -> character +0xd0 ability -> scene +0x338
 -> gate 0x9e979c -> ability virtual +0x18, accepted only when return == 1
 -> ability virtual +0x58 selects numeric gauge mode (0x13b5c2c)
 -> scene +0x324, model +0x144; ability model +0x80
 -> ScoreState +0xc8 and each LifeBarState +0xc8
```

Scene initializer/factory `0xe4e4dc`, model initializer `0xfbfd04`, and score/gauge factories substantiate the transfer. Metadata `char_type` is not by itself proof of the actual runtime selector result.

Base activation gate `0x118e220` rejects numeric argument w3 values 3/4, w4 value 2, level below unlock, and an unmet awakening requirement. w2 is a separate difficulty argument; these exclusions must not be conflated with difficulty 3/4. Additional character-45/song-unlock, pack/song-filter, and session-condition branches remain partly bounded. Prefix tests stop before those later checks and do not claim universal skill activation.

Base `CharacterAbility` constructor `0x189c9f4`, initializer `0x192bf34`, vtable `0x1a95bf0` store hard/easy/overflow flags at `+0x0c/+0x0d/+0x0e`, initial H at `+0x10`, key string at `+0x20`, and mirror at `+0x3b`. Selector `0xdce310` tests easy first →1, hard →2, overflow →5, otherwise 0.

| Virtual offset | Observed role in the recovered paths |
|---|---|
| `+0x18` | activation eligibility |
| `+0x48/+0x58/+0x68` | initial-health override / gauge ID / optional result category |
| `+0x88` | accepted-judgment additive gain callback, receives ScoreState and kind |
| `+0x90` | miss additive-damage callback |
| `+0x98` | judgment-change notification |
| `+0xa0` | gain multiplier, default 1 |
| `+0xa8` | FAR gain multiplier, default 1 |
| `+0xb0/+0xb8` | loss multiplier / base-loss override, default 1 |
| `+0xc0` | FAR weight parameter, default 1; conditional damage path |
| `+0xc8` | post-gauge callback |
| `+0xf0/+0x108` | result-related callback / scene completion callback |

The order is accepted gain delta → notification → gain multiplier → core application → post-hook. Miss damage adds its callback delta before notification/application. Some abilities also override update/end/result hooks; this is not an exhaustive interface naming exercise. There is no single unconditional “deactivate all effects” routine established here: suppression at selection, per-instance disabled flags, and final continuous-update disabling are separately observed.

#### Representative effects traced beyond their names

1. **Easy, hard, mirror, overflow.** Factory branches `0x7ac67c/0x7ac6c0/0x7ac754/0x7ac7dc` construct base abilities through `0xd777ec`. Native construction confirms the respective flags. Mirror byte `+0x3b` is passed into chart loading at `0xe2f0c0` → `0x16e67a4`; this is a concrete chart-loading modifier, not evidence for changed touch timing. The entire coordinate mirror transform was not re-executed in this expedition.

2. **`gaugestart_30|gaugegain_70`.** Factory `0x7ad044–0x7ad09c` → `0x13cf328` → initializer `0x16eebd4` creates RTTI `CharacterAbilityGaugeRateModify`, vtable `0x1b5e0a0`: initial H=30, easy flag, gain multiplier f32(0.7), loss base/multiplier=1. Getter `0xf45e28` returns `+0xac`; the actual accepted path applies it. N=1,000 gives g≈0.176; a PURE from H=50 gains g×0.7, with native f32 rounding.

3. **`challenge_fullcombo_0gauge`.** Factory `0x7acc10–0x7acc6c` creates the same rate-modify class with initial H=0, base-loss override 100, gain multiplier 1, and FAR parameter 0.01. Its ordinary selector is 0. Native helper tests return damage **200 for non-E, 100 for E**, before clamping. A miss from H=50 therefore clamps to 0. The metadata name is not proof of immediate song termination: the traced selector and frame rule do not give mode 0 an immediate H=0 failure.

4. **`scoreclear_aa|visual_scoregauge`.** Factory branch `0x7ad634` → constructor `0x16acf24` creates RTTI `CharacterAbilityClearBasedOnScore`, vtable `0x1aa4720`, threshold `+0xa0=9,500,000`, result code `+0xa4=4`, initial H=100. Its gain multiplier, FAR gain multiplier, and base-loss override return zero (`0x870ce4`, `0x13d100c`, `0xd475a4`). Core application dynamically recognizes the class and computes a score-derived H through `0x171a230` → `0xac61b8`:

```text
if projectedScore >= 8_600_000:
    H = min(100, 25 + 75*(projectedScore-8_600_000)/1_400_000)
else:
    H = max(0, 25*(projectedScore-5_000_000)/3_600_000)
```

The instructions use f32 operations; the compact equation is not a promise that reassociated arithmetic is bit-identical. `0x171a230` projects remaining units as future PURE/shining results unless active H is −1. **Final classification instead compares the stored final score at GameResult+0x10 with 9,500,000**, independent of the ordinary health≥70 test. With LOST=0 it takes the no-LOST/no-FAR category path first. Tests with LOST>0 and H=0 return fail at 9,499,999 and code 4 at 9,500,000/9,500,001.

Base unlock gating depends on character level/awakening. The ordinary g equation does not read character statistics; other skill-specific statistics/progress dependencies are not thereby excluded. Visibility-changing and judgment-changing skill classes exist in RTTI/factory material but were not sufficiently traced for behavioral claims here.

### 9. Expanded scoring and special-scene state

The Expedition 002 leaf helper `0xe43b80` uses the ordinary expression for valid nonnegative counts and positive N:

`floor(10,000,000 × (PURE + FAR/2) / N) + shiningPURE`.

Flag bit 0 changes the base cap from **10,000,000 to 99,999,999** and suppresses the all-PURE shortcut. It does not itself change PURE/FAR weighting. For valid counts below the ordinary cap, tested normal and expanded paths agree. Synthetic PURE=200, N=100 yields 10,000,000 normally and 20,000,000 expanded, without shining; this deliberately excessive input demonstrates the cap distinction, not a claim that an ordinary chart allows 200/100 judgments.

Concrete flag writers:

| Recovered special-scene RTTI / routine | Instruction / effect |
|---|---|
| `SpecialSceneKonzetsuArghenaChainChallenge`, `0x111b678`, vtable `0x1b18e78` virtual `+0x4d8` | `0x111b6cc` writes ScoreState `+0xd0=1` in its branch |
| `SpecialSceneKonzetsuChainChallenge`, `0x1244c30`, vtable `0x1acb328` virtual `+0x4d8` | `0x1244c60` writes ScoreState `+0xd0=1` |
| Track/scene-transfer helper `0x889b54` | `0x889b9c` marks the retained ScoreState expanded |

Transfer `0x178ce84` reuses the preceding model's timeline `+0x30` and ScoreState `+0x38` in the new model, then marks already elapsed notes/checkpoints resolved. This connects the flag to score continuity across special transitions. The full stage denominator policy and all scene-entry eligibility conditions remain unknown.

The flag is copied into GameResult `+0xb0`. Result score getter `0x1315038` normally recomputes from counters with N=PURE+FAR+LOST and that flag; if `+0xb1` is set, it instead returns stored `+0x10`. The producer of `+0xb1` remains unresolved. Thus saved/displayed points cannot universally be assumed to be the raw snapshot field.

No instruction-backed equivalence was established between these score-cap writers and Expedition 005's timing-adjustment modes. No claim is made that expandedCap alone changes a judgment window, input projection, or gauge formula.

### 10. Chart termination, snapshot, and final categories

Frame completion block `0x10a7b38–0x10a7d68` compares effective timeline time E against chart `+0xbc`, with **strict E>end**. Mode 6 adds **6,000 ms**. A successful dynamic recognition of `CharacterAbilityModifyFragmentOnResultOngeki` (typeinfo `0x1a86630` via GOT `0x1b964b0`) adds **2,000 ms** when ability byte `+0xf0` is set. Other ability update hooks are called in the surrounding frame path; not every specialized completion rule is reduced here.

The ordinary completion callback passes false to delegate virtual `+0x10`, sets model `+0x139`, and reaches thunk `0xe2c124` → scene handler `0xc27d34`. Failure uses the same delegate with true. The scene handler latches termination, calls ability virtual `+0x108`, builds the final snapshot via `0x1600bb0`, and enters presentation/queued-processing paths. Special scene virtual `+0x510` can handle termination instead of the common ending path. `0xe5c700` separately schedules `endingAnimation`: ordinary delay 4 seconds, mode 6 delay 0.5, and a failed immediate-ending branch delay 0, plus optional special-scene `+0x520` delay. Logical failure and presentation delay are separate decisions.

Snapshot `0x1600bb0` is idempotent when ScoreState `+0x68` already exists. It disables each gauge's continuous update, calls `0xa126f4` at chart end, and transfers active H. Unless ScoreState `+0xd1` is nonzero, final LOST is **N−PURE−FAR**, including units never recorded as misses. The actual recorded LOST count is preserved separately.

Selected `GameResult` layout (RTTI typeinfo `0x1ad8f80`, vtable `0x1b054c0`):

| Offset | Value |
|---|---|
| `+0x10` | stored score snapshot |
| `+0x14/+0x18/+0x1c` | shining PURE / PURE / FAR |
| `+0x20/+0x24` | final selected LOST / actual recorded LOST |
| `+0x28` | **floor(H)** as signed integer, `fcvtms` in `0xcab7fc` |
| `+0x30/+0x38/+0x50` | date / song ID string / difficulty |
| `+0x54/+0x58` | selected outer gauge mode / partition-like argument |
| `+0x60/+0x64` | maximum combo / early-late counter block |
| `+0x74/+0x78/+0x7c` | cap / floored peak / floored trough |
| `+0x80/+0x84` | timing aggregate / active hard-phase flag |
| `+0x88/+0xa8` | character ID / staged-result value |
| `+0xb0/+0xb1/+0xb3` | expanded cap / return-stored-score / zero-health-fails flags |
| `+0xc0/+0xe4` | ability pointer / timing sample count |

Stages 12/13 additionally compute a result value from active index, with −1 H forcing zero (`0x1600e1c–0x1600e74`); this is distinct from the primary clear code.

Classifier `0x12a5574` returns the following codes. Labels are **interpretations** supported by counter predicates and clear-type storage; numbers/branches are confirmed:

| Code | Interpreted category | Core condition |
|---:|---|---|
| 0 | Fail | Failed health/score predicate |
| 1 | Ordinary clear | Ordinary health pass, LOST>0, no overriding clear label |
| 2 | Full recall | Passed health predicate and LOST=0, FAR>0 |
| 3 | Pure memory | Passed health predicate and LOST=0, FAR=0 |
| 4 | Easy/skill clear | Mode 1 or 5, or relevant ability result category |
| 5 | Hard/survival clear | Survival-mode health pass and no higher counter/ability category |

Detailed comparison: survival modes are 2, 6–13, and mode 5 with result `+0x84`. They fail on integer H<0, or H==0 with `+0xb3` set. Others require integer H≥70. Only after passing does the ordinary path upgrade LOST=0 to codes 2/3. Mode 14, if artificially supplied as the outer result mode, uses the ordinary threshold; normal staged configurations retain outer 12/13.

For mode 5, the hard-phase flag changes the health eligibility test, but the subsequent `(mode|4)==5` branch still returns code 4 when LOST>0. It must not be rewritten to code 5 merely because damage/failure processing has become hard-style. Native tests with hard-phase mode 5 give code4 at integer H0 with the zero-health flag clear, and fail0 when that flag is set or H is −1.

The score-clear ability is recognized before ordinary health checks. LOST=0 immediately selects 2/3; otherwise stored score must be ≥ability threshold and the ability supplies the category. A generic ability virtual `+0x68` returning 4 can also change an otherwise passed result to 4. Score, combo, and clear category are therefore related but not interchangeable; max combo itself is not the recovered no-LOST classifier input.

### 11. Concrete local persistence and bounded eligibility

`0x13552d4` is an actual SQLite score writer. It queries `scores` by song ID, difficulty, and a `ct` partition; it inserts/replaces only when no record exists or getter `0x1315038(result)` is **strictly greater** than the stored best score (`0x1355610` onward). SQL assembly/binding stores version, getter score, shining/PURE/FAR/LOST, date, song, difficulty, normalized modifier, integer health, and `ct`. Equal scores do not replace the best-score row in this branch.

Modifier normalization is a separate decision: `0x10d50b0` maps input modes 5–13 through table `0x47a684` to `[1,2,0,0,2,2,2,2,2]`; other inputs pass through. `0xdc2dd0` then maps 1–5 to `[1,2,0,0,5]`, otherwise 0. Runtime gauge ID must not be assumed identical to persisted modifier.

Independently of whether the score row improved, when writer argument w2==0, `0x1355a7c` calls classifier `0x12a5574` and clear-type writer `0x12a5e60`. That routine queries/upserts **`clearTypes(songId,songDifficulty,clearType,ct)`** and uses `0x196b22c` → comparator `0xe3c054`, not numerical max. Executing that comparator gives these allowed replacements:

| Old type | New types that replace it |
|---:|---|
| −1 / missing | 0,1,2,3,4,5 |
| 0 | 1,2,3,4,5 |
| 4 | 1,2,3,5 |
| 1 | 2,3,5 |
| 5 | 2,3 |
| 2 | 3 |
| 3 | none |

Concrete caller `0xe44c5c` invokes this writer with w2=0 at `0xe44cac` **before** testing whether the clear code is zero. Thus failure alone is not a universal prohibition on local score writing. Caller `0xc0c7a8` has additional song/object gates and supplies w2 based on classification; other special callers differ. The full ownership of every normal/special results-screen save path was not closed.

Scene completion also reaches `0x1246c98` → `0xe26e44`, which serializes/enqueues pending result work. This is not itself the SQLite score write, nor proof that remote submission succeeds. Eligibility for all special charts, leaderboard/rating submission, network persistence, and all queued-worker conditions remains **unknown**. No database or network effects were executed in validation.

## Pseudocode

Only recovered mechanisms are implemented below. `f32` rounds to IEEE binary32 after the indicated operation; integer counters are signed 32-bit as in the native fields. Ordinary finite values and valid object pointers are assumed. Unknown special branches are explicitly left unresolved.

### Initialization and ordinary judgment dispatch

```text
make_score(chart, selectedMode, ability):             # 0x13e00b4
    score.N = chart.i32_b8
    score.mode = selectedMode
    score.active = 0
    score.ability = ability
    for id in native_mode_map[selectedMode]:
        score.gauges.push(make_lifebar(score,id,ability))

initialize_lifebar(g, explicitInitial=-1):           # 0x160a3b8
    override = ability.v48() if ability else 0.0
    if explicitInitial != -1: g.H = f32(explicitInitial)
    elif g.id in {2,6,7,8,9,11,12,13,14}:
        g.H = override if override > 0 else 100.0
    else: g.H = override
    g.peak = g.trough = g.H
    if g.id == 11: configure_from_external_world_state_UNKNOWN(g)
    g.baseGain = gain_equation_given_above(chart.N, song.byte_54, g.id, g.p)

record_accepted(s,note,id,side,now,contact):           # 0x1730290
    if not note.v20(now,contact): return
    if id == 0: s.shiningPURE = i32(s.shiningPURE+1)
    if id in {0,1}: s.PURE = i32(s.PURE+1)
    if id == 2: s.FAR = i32(s.FAR+1)
    for g in s.gauges: accepted_gauge(g,note,id,side,now,contact)
    advance_staged_index_if_needed(s)
    # native early/late/analytics bookkeeping
    s.score = native_score_helper(s.LOST,s.FAR,s.PURE,s.shiningPURE,s.N,s.expanded)
    s.combo = i32(s.combo+1)
    s.maxCombo = max(s.maxCombo,s.combo)

record_miss(s,note,now):                             # 0x868e54
    if not note.v38(true): return
    s.LOST = i32(s.LOST+1)
    for g in s.gauges:
        if g.disabled: continue
        E = RTTI_name_pointer(note) == RTTI_name_pointer(LogicLongNoteBase)
        weight = 2.0 if g.id in {12,13} else 1.0
        damage = native_damage(g,E,kind=3,weight)
        if g.ability:
            damage = f32(damage + g.ability.v90(s,damage))
            g.ability.v98(s)
        apply_gauge(g,0.0,damage)
    advance_staged_index_if_needed(s)
    # native analytics/cache bookkeeping
    s.combo = 0

accepted_gauge(g,note,id,...):                       # 0x16e4ab0
    if g.disabled: return
    gain = g.baseGain if id in {0,1} else f32(g.baseGain*0.5) if id==2 else 0
    damage = 0.0
    protected = false
    if id==1 and g.id==12:
        gain,damage,protected = 0.0,2.0,true
    if id==2:
        if g.ability:
            # FAR gain multiplier, fixed-FAR subclass, FAR-weight and flag hooks
            # 0x16e4be0..0x16e4d54; not a generic ordinary FAR-damage formula
            gain,damage,protected = native_ability_FAR_branch(g,note,gain)
        else:
            weight = 0.5 if g.byte_88 else 0.0
            if g.id==12: weight=f32(weight+1.0)
            if g.id==13: weight=f32(weight+0.5)
            if g.id in {12,13} or g.byte_88:
                damage = native_damage(g,exact_name_test(note),2,weight)
            protected = g.id in {12,13} and not g.byte_88
    if g.ability:
        gain = f32(gain + g.ability.v88(g.score,gain,damage,id))
        g.ability.v98(g.score)
        gain = f32(gain * g.ability.va0())
    if g.id==8: gain=0.0
    if protected and damage>=g.H:
        damage = f32(max(0.0,f64(g.H)-0.5))
    apply_gauge(g,gain,damage)
```

### Damage and clamping

```text
native_damage(g,E,kind,weight):                     # 0x120dd34
    override = g.ability.vb8(g.hardPhase) if g.ability else 1.0
    fixed = is_native_FixedValueCondition_class(g.ability) or g.id==8
    D = 10.0 if g.id==8 else override
    if D==1.0 and not fixed:
        D = default_mode_table_and_hard_flags(g)     # exact table in section 5
    if g.ability: D=f32(D*g.ability.vb0())
    amount = D if fixed else f32(D*weight)
    if g.damagePercentage != 100:
        amount=f32(amount*f32(f32(g.damagePercentage)/100.0))
    if g.id==7 or (not E and not fixed): amount=f32(amount+amount)
    new=f32(g.H-amount)
    crossingRule = g.id in {2,7,9} or (g.id==10 and g.byte_b9)
    if crossingRule and g.H>30 and new<30 and not fixed:
        new=f32(f64(new)+f64(f32(g.H-30.0))*0.5)
    return f32(g.H-new)

apply_gauge(g,gain,damage):                         # 0x133fac8
    if g.disabled: return
    x=f32(f32(g.H+gain)-damage)
    ceiling=g.U if g.capEnabled and g.U>100 else 100.0
    g.H=max(g.L,min(ceiling,x))                      # tested finite normal bounds
    if g.id==6:
        g.pendingPositive=f32(g.pendingPositive+gain)
        g.pendingNegative=f32(g.pendingNegative-damage)
    if g.ability:
        g.ability.vc8(g.score)
        if is_native_ScoreClear(g.ability):
            g.H=score_to_visual_health(projected_score(g.score))
        elif is_native_ClearBasedOnBestGrade(g.ability):
            g.H=native_best_grade_conversion_UNRESOLVED(...)
    if g.id==9:
        r=f32(f32(g.score.PURE)/f32(g.score.N))
        g.F=f32(f32(r*f32(r*70.0))+0.0)
    if g.capEnabled: g.H=min(g.U,g.H)
    g.peak=max(g.peak,g.H); g.trough=min(g.trough,g.H)
```

### Frame transitions and failure

```text
frame_gauge_fragment(model,scene):                  # 0x10a7550, excerpts
    native_continuous_and_score_update(model.score) # 0xa126f4 -> 0x83dd70
    active=model.score.gauges[model.score.active]
    if model.mode==5 and active.H>=100 and not model.hardPhase:
        model.hardPhase=true
        for g in model.score.gauges: g.hardPhase=true
        native_audio_event(...)
    # mode-10 quarter-duration transition exists; other update hooks omitted
    checkable = model.mode in {2,6,7,8,9,11,12,13}
    checkable |= model.mode==5 and model.hardPhase
    checkable |= model.mode==10 and model.byte_13c
    if not checkable or active.H>active.F or model.finished: return
    if scene.byte_34d:
        if not model.grace:
            model.grace=true; model.byte_13c=true
            failedH=active.H
            for g in model.score.gauges:
                g.byte_b9=true; g.U=failedH; g.capEnabled=true
        return
    for g in model.score.gauges:
        g.H=-1.0; g.continuousUpdate=false
    model.delegate.v10(true)
    model.finished=true

advance_staged_index_if_needed(s):
    if s.mode not in {12,13}: return
    g=s.gauges[s.active]
    if g.H<=0:
        g.disabled=true
        if s.active < len(s.gauges)-1: s.active+=1
```

### Character selection, special scoring, and final classification

```text
base_skill_gauge_id(a):                            # 0xdce310
    if a.easy: return 1
    if a.hard: return 2
    if a.overflow: return 5
    return 0

base_activation_prefix(a,song,difficulty,arg3,arg4,flag): # 0x118e220
    if u32(arg3-3)<2 or arg4==2: return false
    c=selected_character()
    if c.level<c.unlockLevel: return false
    if c.requiresAwakening and not c.awakened: return false
    # awakening/special-character/song/pack/session checks continue here
    return native_remaining_restrictions_UNKNOWN(...)

score_helper(lost,far,pure,shining,N,expanded):       # 0xe43b80
    if pure==N and not (expanded&1): return i32(10_000_000+shining)
    weighted=i32(10*pure+5*far)
    q=signed_divide(i64(weighted)*1_000_000_000,N)
    base=signed_divide(q,1000)
    cap=99_999_999 if expanded&1 else 10_000_000
    return i32(min(base,cap)+shining)

finalize(s):                                       # 0x1600bb0
    if s.cachedResult: return s.cachedResult
    lost=s.LOST if s.byte_d1 else i32(s.N-s.PURE-s.FAR)
    for g in s.gauges: g.continuousUpdate=false
    native_update(s,s.chart.endTime)
    active=s.gauges[s.active]
    r=GameResult(score=s.score,shining=s.shiningPURE,PURE=s.PURE,FAR=s.FAR,
                 LOST=lost,recordedLOST=s.LOST,health=floor_i32(active.H),
                 mode=s.mode,ability=s.ability,expanded=s.expanded,...)
    r.hardPhase=active.hardPhase
    r.zeroHealthFails=bool(s.byte_d2)
    # copies max combo, early/late, health range, song, character, analytics
    # stage values and ability result callback also run
    s.cachedResult=r
    return r

classify(r):                                       # 0x12a5574
    a=as_native_ClearBasedOnScore(r.ability)
    if a:
        if r.LOST==0: return 3 if r.FAR==0 else 2
        if r.storedScore<a.threshold: return 0
        return a.v68()
    survival = r.mode==2 or 6<=r.mode<=13 or (r.mode==5 and r.hardPhase)
    if survival:
        if r.health<0 or (r.health==0 and r.zeroHealthFails): return 0
        base=5
    else:
        if r.health<70: return 0
        base=1
    if r.LOST==0: return 3 if r.FAR==0 else 2
    if (r.mode|4)==5: return 4
    if r.ability and r.ability.v68()==4: return 4
    return base

persist_local_fragment(db,r,skipClearType):           # 0x13552d4
    score=native_result_score_getter(r)             # 0x1315038
    old=select_scores_row(song,difficulty,ct)
    if missing(old) or score>old.score:
        insert_or_replace_score_and_counters(db,r,score,normalized_modifier(r))
    if not skipClearType:
        newType=classify(r)
        oldType=select_clearTypes_row(song,difficulty,ct)
        if native_replacement_comparator(newType,oldType):
            insert_or_replace_clearType(db,newType)
    # Caller eligibility and remote/queued result work are separate.
```

## Validation

Original AArch64 instructions were executed in Unicorn, loading ELF PT_LOAD segments and applying `R_AARCH64_RELATIVE` relocations. Synthetic objects supplied fields/vtables. Infrastructure hooks covered allocation/free/refcount/autorelease, string/memory helpers, time, account lookup, optional-character lookup, logging, delegate notifications, and exact synthetic `dynamic_cast` cases. Map insertion was hooked to capture the original initializer's keys/vectors. Note acceptance virtuals were deliberately hooked true/false; they are the boundary to the judgment routines already investigated in earlier expeditions.

The actual gauge initializer, accepted/miss recorders, damage helper, core health arithmetic, skill key dispatch/constructors/getters, score helper, snapshot constructor, classifier, and selected frame blocks executed natively. These were not replaced by Python gauge formulas. Expected formulas were checked against results where stated.

| Coverage | Inputs / scope | Observations |
|---|---|---|
| Initialization | 14 IDs: 0–10,12–14 | Start values and gains; mode-11 external-state initialization not executed |
| Gain equation | 16 cases: N=1,100,399,400,599,600,1000,2000 × song flag 0/1 | Exact f32 outputs matched the recorded equation |
| Judgment dispatch | 120 combinations: 15 IDs × E/non-E × IDs 0/1/2/LOST | Outputs include the table in section 5; all calls completed |
| FAR caller flag | Six cases: modes0/12/13 × byte88=0/1 | At H50,g.1, non-E, H becomes50.05/49.05,41.05/36.55,45.55/41.05 respectively |
| Damage below 30 | Modes12/13/14 at H=20, unit weight, E | Returned 4.5/2.5/2.5 |
| Derived RTTI | Actual hold/arc vtables plus tap-like test, H=50, mode0 | Each non-E LOST damages 2; exact-base synthetic E damages 1 |
| Clamping | Five cases plus disabled no-op | 99.9+2→100; 1−9→0; lower bound10 retained; enabled cap150 permits 149+5→150 and 150−9→141 |
| Hard boundary | 12 cases: H=29.999,30,30.001,31,34.5,39 × E/non-E | Strict >30 crossing behavior and native rounding retained |
| Recorder ordering | Three mode chains, PURE0/PURE1/FAR/LOST | Counters `[shining,PURE,FAR,LOST]=[1,2,1,1]`; combo resets; native score/gauge dispatch executed |
| Rejection/repetition | Rejected note guards; eight accepted units | Rejection changes neither counters nor H; eight calls add eight PURE units and repeated f32 gain |
| Classifier | 228 cases: modes0–14, H=−1/0/69/70/100, LOST/FAR combinations, zero-health flag | Mode-specific health and no-LOST/no-FAR comparisons confirmed |
| Frame failure | 30 cases: modes0–14 × H=0/0.0001 | Delegate events and −1 sentinel observed; register w21 alone was not treated as a failure indicator |
| Promoted modes | Mode5 hard flag and mode10 promoted flag, H0; three mode5 final cases | Both enabled frame blocks call finish(true); mode5 health/category distinction confirmed |
| Grace | Mode2 H=0, scene grace enabled | No end event; H=0, cap0, deferred flags set, finished latch clear |
| Overflow boundary | H=99.999 /100, mode5 | Hard flags off/on; stopped before audio-event infrastructure |
| Completion boundary | End10000, E=9999/10000/10001 | Normal end callback only at10001 |
| Mode map | Original initializer, insertion capture | Fourteen outer keys and staged vectors exactly as recorded |
| Skill factory | Seven exact keys listed in section8 | Native flags, types, initial values, modifiers; rate skill PURE and challenge LOST executed |
| Activation prefix | Seven mode/session/level/awakening cases | Level7<unlock8 rejects, level8 reaches later checks; w3=3/4 and w4=2 reject; awakening gate tested |
| Scoring | Six normal/expanded cases | Valid counts agree; excess-count cap distinction confirmed |
| Snapshot rounding | H=69.999/70/99.999 after native judgments | Integer H=69/70/99 and ordinary classifications 0/1/1 |
| Score-clear threshold | Stored score9,499,999/9,500,000/9,500,001; LOST>0,H=0 | Codes0/4/4 |
| Clear-type comparator | 42 original comparisons: old−1..5 × new0..5 | Replacement table in section11 |
| Staged miss | IDs12/13/14, H1/100/100 | H0/82/91, first disabled, active index1 |

Two complete scoped chains deserve emphasis:

1. **Ordinary clear boundary:** original initialization with N=100 gives g=1,H=0. After **69** original accepted-recorder calls: H=69, final integer H=69, final LOST=31, classifier=0. After **70** calls: H=70, final LOST=30, classifier=1. No manual health write was made between judgments and finalization.
2. **Miss to immediate fail:** mode2,H=1 → original miss recorder → H=0 → original failure block → H=−1, finish delegate(true) → original final snapshot → integer H=−1 → original classifier=0.

Tests are synthetic native execution, not a real Android session. They do not exercise actual touches, audio, a full chart, renderer, every class-hierarchy cast, SQLite side effects, network submission, mode11 initialization, or complete Tempest/Insight continuous behavior. Sampled successful execution is not proof of every malformed/NaN/overflow edge case. No real-device claim is made.

## Unresolved Mysteries

- Full producers/ranges of Tempest p and accumulators; complete continuous-mode integration and mode11 world-state effects.
- Product identity and complete entry rules of numeric modes3/4/7/8; every class-specific eligibility/deactivation rule.
- Why the damage-category predicate uses exact RTTI-name identity rather than inheritance, and which additional runtime constructions instantiate the exact base category. Derived hold/arc test outcomes are established without inventing a rationale.
- Full FAR-damage hook combinations, fixed-value subclasses, statistics-based skills, visibility/input/judgment changes, and external-state activation conditions beyond the representative skills.
- All producers of ScoreState `+0xd1/+0xd2`, GameResult `+0xb1`, and song `+0x54`; their exact product meanings.
- Complete special-chain denominator/reset policy and all scene eligibility/results overrides.
- End-to-end ownership of every normal/special result-saving path and remote/rating/leaderboard eligibility. Concrete local writers are recovered, but not every caller or queued worker.

These are evidence limitations, not authorization or a plan for another expedition.

## GitHub Status

Authorized changes for this expedition are this new subject document and an append-only Expedition006 entry in `context.md`. Earlier expedition files, binaries, source assets, and README are preserved. Commit identities and final read-back verification are supplied in the headquarters return report after publication; this document does not invent its own future commit SHA.
