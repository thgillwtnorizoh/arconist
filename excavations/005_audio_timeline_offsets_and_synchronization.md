# Expedition 005 — Audio Timeline, Offsets & Synchronization

Date: 2026-10-22. Primary evidence: supplied `arccopy.zip`. Authoritative project instructions and current cumulative GitHub record, including the relevant Expedition 002–004 subject records, were read before investigation.

## Result

Recovered the normal judgment-clock lifecycle, concrete AFF/user offset combination and sign, pause compensation and resume-time music seek, timeline adjustment modes, FMOD playback/SFX scheduling arithmetic, and a timestamp-age correction in offset calibration. No periodic audio-position feedback was found in the recovered running gameplay clock or the inspected frame/input path. Explicit pause/resume/seek alignment exists and must be distinguished from continuous drift correction.

This is native reverse engineering with isolated execution and synthetic objects, not measured Android audio/touch latency or a live gameplay reproduction. Negative findings below are bounded to the inspected chains, not a proof about every game mode, backend or indirect caller.

## What I Found

### Evidence and address conventions

Archive paths and SHA-256:

| Evidence | SHA-256 |
|---|---|
| `lib/arm64-v8a/libcocos2dcpp.so` | `3eaca4e6dabb3395f276f8915698d57675757d0df0970e716b23a3dc201c79be` |
| `lib/arm64-v8a/libfmodProvider.so` | `db07590708c1e2b7ed3a17800a8839392d5a7a8322cd102d5b35bda05b251bfb` |

Extracted files were compared with ZIP bytes. Main-library Build ID remains `17d660edbf37ca78beefc32e07672c97419ddce6`. Main addresses below are library-relative ELF VAs; code/rodata addresses equal file offsets. Provider addresses belong to a separate ELF and are explicitly labeled. RTTI/virtual targets are resolved through ELF relocations, including symbol relocations in the provider. Recovered symbol names are distinguished from researcher field labels.

**Confirmed:** decoded instructions, smali, relocation-backed identity, or the explicitly described isolated tests. **Inference:** interpretation of those operations, especially logical audio/chart alignment. **Unknown:** provenance/lifecycle not fully followed. Arithmetic descriptions assume ordinary valid integer/finite inputs without overflow; float32 order is material.

### 1. Authoritative judgment clock

The recovered normal judgment source is **effective GameTimeline time**, not a direct FMOD playback-position read and not the stored Android touch timestamp.

`GameTimeline` RTTI name is at main VA `0x4d6216`, typeinfo `0x1b09aa0`, vtable address point `0x1af5e60` (GOT entry `0x1b96478` points to vtable prefix `0x1af5e50`). Its small virtual initializer `0x1636640` returns true; substantive setup is in model initializer `0xfbfd04`.

| Timeline offset | Instruction-backed role / explanatory label |
|---|---|
| `+0x10` | 64-bit steady-clock origin Osteady |
| `+0x18` | 64-bit system-clock origin Osystem; not the running judge source |
| `+0x20` | Signed 32-bit computed raw time R |
| `+0x24` | Signed pause reference P |
| `+0x28` | Signed time compensation C |
| `+0x2c` | Pause flag |
| `+0x2d` | Started/steady-clock mode flag |
| `+0x2e` | Music-started latch |
| `+0x2f` | Flag set by adjustment mode 2; enables startup fade branch |
| `+0x30` | Combined chart/player offset O |
| `+0x34` | Signed cursor/adjustment A; **not established as frame delta** |
| `+0x38` | Effective-time anchor B recorded when music starts |

Factory fragment `0xfbfed0–0xfbff7c` allocates/zeroes the 0x40-byte timeline, initializes cursor/anchor to zero and flags at `+0x2c` to zero, sets the combined offset, and stores timeline at model `+0x30`.

Repeated judge/frame readers use:

```text
E = R - C                         if steadyMode != 0
E = A - C - (3000 if A<=0 else 0) otherwise
```

Representative readers: tap classifier `0x160ce28`, initial touch `0xeec024`, continuous input `0x14858d4`, frame `0x10a7550`, and pause/adjustment routines. In the ordinary running state, A=0. Before steady mode is enabled, the getter is cursor-based; repeated writes to raw R do not themselves advance that alternate getter.

`0x1271200` calls imported `std::chrono::steady_clock::now()` at PLT `0x1a6dc60` and divides its nanosecond count by 1,000,000. It returns milliseconds. Updater `0x16c90bc` loads the low 32 bits of the stored origin and uses 32-bit time arithmetic. Within ordinary durations this represents the elapsed difference; full wrap/overflow behavior was not tested.

Separate helper `0x11a7ae0` calls `std::chrono::system_clock::now()` at PLT `0x1a6dbe0` and divides its native count by 1000 to produce milliseconds. It must not be conflated with the monotonic source or Android elapsed-realtime epoch.

### 2. Initialization, start and normal updates

Model start wrapper `0x8db04c` receives two epochs, stores them at timeline `+0x10/+0x18`, then sets `+0x2d=1`. It does not itself recalculate R/C. Start callers include:

- `0x192d8a0`: samples `0x1271200` and `0x11a7ae0`, then calls the wrapper.
- `0x14b2910`: obtains a target/deferred system-time value through `0xf0ca18`, computes an ahead-of-current delay, and adds a corresponding delay to both clock epochs before calling at `0x14b29e4`.
- `0x9605f8`: at `0x960aa8–0x960ae0`, adds a nonnegative supplied delay to both clock samples, or uses current samples for a negative branch.

These show immediate and deferred start origins. The full multiplayer/network target-time policy behind those call sites is outside this reconstruction; it is not audio-position feedback.

Literal normal update sequence in `0x16c90bc`:

```text
if steadyMode:
    base = steadyNowMs - low32(Osteady) - (3000 if A<=0 else 0)
    R = base
    if paused: C = base - P
    if music not started:
        compare effective time, before final R+=A, against -O
        if strictly greater and not paused:
            request main BGM start
            musicStarted = true
            C = base + O        # ordinary steady-mode path
            B = -O
            optional fade calls if flag_2f
R += A
```

The repeated fallback getter branches in the native function are retained in the detailed pseudocode below. The common 3000 ms term is an explicit pre-roll/count-in term, not a measured audio-output latency estimate.

With steady mode on, A=0, unpaused and music not yet started, E advances from approximately -3000 after the first update. Startup uses **E > -O**, not >=. When the first update crosses that boundary, it sets C so the effective chart time becomes **exactly -O**; update overshoot is discarded at that anchor. Subsequent ordinary E advances by elapsed steady time while C remains fixed.

This resolves the startup behavior left open in Expeditions 002–003. The clock remains a steady-time computation; the start latch aligns its origin with a playback request rather than making FMOD the authoritative judge clock.

### 3. Timing offsets: sources, order and signs

AFF `AudioOffset` parsing remains as documented: main `0x173b358`, `atoi` conversion at `0x173bcfc`, chart signed integer `+0xc4`.

Model initialization at `0xfbfed0–0xfbff54` reads settings from application context `+0x70`:

```text
selectedUserOffset = settings.i32_04 if settings.i32_00 == 0
                     else settings.i32_08
O = signed32(chart.i32_c4 + selectedUserOffset)
timeline.i32_30 = O
```

Both operands are added; no sign reversal or sample-rate conversion occurs here. Native settings loader `0x1a02b48` and setter `0x169e288` identify the persisted keys:

| Field | Key / observed loading rule |
|---|---|
| Settings `+0x00` | `audio_preset`, default 0; zero selects regular offset, nonzero alternate |
| Settings `+0x04` | Prefer `offset_int_2`; if missing, load legacy `offset_int` and subtract **20**; if both absent, zero |
| Settings `+0x08` | `bt_offset`; missing value defaults to **200** |

Missing is detected with INT_MIN sentinel. If `offset_int_2` exists, legacy `offset_int` does not also contribute. The -20 term is a persisted-setting migration, **not a second runtime subtraction applied to every chart**. `0x169e288` writes regular selection to `offset_int_2`, alternate selection to `bt_offset`.

Names support interpreting the alternate profile as Bluetooth-related; the arithmetic and persisted names are confirmed, while automatically equating the setting selector with the currently active Android route is not established by these accesses alone.

**Sign interpretation for the ordinary anchored path:** with A=0 and no pause/seek, chart time E starts at -O when the music start is requested. Ignoring backend/call/output latency and differences between requested and actual start, logical playback position M and chart time satisfy:

```text
E ≈ M - (AFF AudioOffset + selectedUserOffset)
nominal logical music position for chart note n ≈ n + AFF AudioOffset + selectedUserOffset
```

Thus increasing the selected user offset by +Δ holds chart time Δ earlier at the same logical music position; the nominal matching input occurs Δ later on that music timeline. This is a mathematical inference from the startup anchor, not a measurement of when sound reaches the speaker or when a physical tap occurred.

Example: AFF=+120, regular user=+30 -> O=+150; chart time is -150 at the music-start request. A note at chart time1000 nominally aligns with logical music position1150. No extra fixed 20 ms subtraction is applied if the current regular key supplied +30.

### 4. Pause, resume and seeking

Model pause wrapper `0xe31764` stores its pause argument in model byte `+0x138` (initial-input gate), then calls timeline pause routine `0x9e74f4`. Scene callers include `0xd44fac` (pause true at `0xd450d8`) and `0x165211c` (state-dependent true/false at `0x1652198`).

`0x9e74f4` first updates the clock with the old pause state:

- **Pause true:** stores P=E-A, requests provider pause through audio manager `0x18c9ba4`, then sets timeline paused flag.
- **While paused:** each steady-mode update makes C=base-P. After the final R+=A, E=P+A remains fixed even though the underlying steady clock continues advancing. Pause duration is absorbed into C rather than stopping the OS clock.
- **Resume false, music already started:** update while still paused, compute seek position **E-B**, call audio manager `0xfbf24c`, then unpause through `0x18c9ba4`; finally clear timeline pause flag. With ordinary B=-O, that seek is **E+O**.
- **Resume before music started:** clears the pause flag without the started-music seek/unpause branch; a subsequent normal update can cross the startup gate. Pause true can still request the provider pause before music startup.

This is explicit resume-time realignment. It does not compare E with the actual playback position to estimate drift before deciding the seek.

Timeline adjustment routine `0xa19088`, reached from model wrapper `0x15a0238`, has separate modes:

| Mode argument | Actual operation |
|---|---|
| Other than 1 or 2, including 0 | Subtract supplied delta from both 64-bit epochs `+0x10/+0x18`; no immediate audio seek in this branch |
| 1 | Add delta to A at `+0x34`, update timeline, then call audio seek with E |
| 2 | Same cursor/update/seek path, also set byte `+0x2f`; model wrapper performs additional note/checkpoint-state handling |

The mode1/2 seek argument is E, whereas resume uses E-B. They must not be silently rewritten as one identical seek formula. A also selects whether the -3000 term applies, so changing its sign/zero status is not generally equivalent to a plain delta addition to E.

Observed callers include special-song RTTI for `SpecialSceneGrievousLadyTrigger::performSpecialSongUpdate` and `SpecialSceneFractureRayTrigger::performSpecialSongFinish` in mode0 callbacks; one callback `0x1088034` supplies5000. Scene initialization `0xe2ea48` uses mode1 or mode2 at `0xe2f818`, including a multiplayer-related branch with a start-time-minus3000 calculation. These are concrete adjustment/skip paths, not evidence for periodic music-drift measurement.

### 5. GameTimeline-to-FMOD alignment

Main-library startup manager `0x1735d7c` clears several queued/fade settings, restores volume and dispatches provider virtual `+0x28` with loop=false, BGM index0, delay0. Relevant separate-provider vtable targets, resolved from `_ZTV24AudioProviderFMODAndroid`:

| Virtual byte offset | Provider VA | Exported operation |
|---|---:|---|
| `+0x28` | `0x270a8` | `playBGM(bool,int,int)` |
| `+0x30` | `0x22124` | `setBGMPaused(bool,int)` |
| `+0x38` | `0x32da0` | `getBGMPosition(int)` |
| `+0x40` | `0x35b38` | `setBGMPosition(int,int)` |
| `+0x58` | `0x26e04` | `loadAndScheduleSfxOnMainBGM(...)` |
| `+0x70` | `0x39b8c` | `playSFX(...)` |
| `+0xa8` | `0x39ea0` | `update()` |
| `+0xb8/+0xc0` | `0x3f708/0x49118` | `suspend()/resume()` |

Provider `playBGM` calls `Channel::setLoopCount` (false->0, true->-1), applies volume, obtains sample rate Fs via `System::getSoftwareFormat`, and obtains own/parent DSP clocks via `ChannelControl::getDSPClock`. It uses the **parent** clock for scheduling:

```text
d = float32(delayMilliseconds)
d = float32(d / 1000)
d = float32(d * float32(Fs))
startDSP = uint64(float32(d + float32(parentDSPClock)))
channel.setDelay(startDSP, 0, true)
```

Then it unpauses the selected channel, or the shared main channel group for index0. The actual gameplay startup request supplies delay0; the API's nonzero delay handling is capability, not proof that normal GameTimeline startup uses a future nonzero DSP delay.

The uint64 clock is converted to float32 before addition; this is not an exact integer sample-count calculation. Isolated example: parent536870929, delay0 -> scheduled536870912. That is arithmetic behavior of this implementation, not a measured audio glitch.

`getBGMPosition` calls `FMOD::Channel::getPosition(..., unit=1)`. `setBGMPosition` first reads current **main/index0** position through its getter, sets the requested indexed channel's position with unit1, and for index0 processes scheduled SFX. Unit literal1 and the surrounding /1000 conversions support the millisecond interpretation; no external FMOD manual was substituted for binary evidence.

Audio manager wrappers: `0x1947af4` reads main playback position, `0xfbf24c` dispatches seek through provider+40 (normally index0, optionally another track), and `0x18c9ba4` dispatches pause through provider+30 at index0.

### 6. SFX scheduling and seek alignment

Main-library `0xc81b18` copies `(string, integerTime)` records, prefixes/transforms the resource name through `0x8d4fe8`, and dispatches provider+58. Its inspected integer copy path does not add the user/chart offset. Upstream authorship of every scheduled timestamp is not reconstructed, so these records are not generalized to all tap sounds.

Provider `0x26e04`:

1. Pauses the main group at provider `+0x18`.
2. Preloads/obtains each sound and creates its channel.
3. Reads software sample rate and the main BGM channel's parent DSP clock.
4. Schedules each supplied time with the same float32 `parent + time/1000*Fs` conversion and `setDelay(...,0,true)`.
5. Places the SFX channel in the main group and retains scheduled sound/channel records.

Group anchoring and later group unpause explicitly connect scheduled SFX and main BGM. This is distinct from ordinary interactive `playSFX` at provider `0x39b8c`, which creates/sets volume/loop parameters and unpauses immediately; no `getDSPClock/setDelay` call occurs in that inspected routine.

On main BGM seek, provider `0x35b38` obtains old main position, sample rate and parent clock. For each retained scheduled channel:

```text
deltaSeconds = float32((newPosition-oldMainPosition)/1000)
newStartDSP = float32(float32(oldScheduledStartDSP)
                      - float32(deltaSeconds*float32(Fs)))
if newStartDSP < float32(currentParentDSP): stop channel
else: channel.setDelay(uint64(newStartDSP),0,true)
```

Equality reschedules rather than stops. Nonzero BGM index skips this main-SFX adjustment branch. This is direct rescheduling after a seek; it does not periodically estimate audio drift.

### 7. Device/audio compensation versus output configuration

`smali/low/moe/AppActivity.smali` reads Android properties `OUTPUT_SAMPLE_RATE` and `OUTPUT_FRAMES_PER_BUFFER`, and computes a Bluetooth-related boolean through adapter/profile queries, with exception/permission branches. It passes `(sampleRate,bufferSize,bool)` to native `setAndroidAudioProperties(IIZ)`.

In the provider ELF, exported JNI `Java_low_moe_AppActivity_setAndroidAudioProperties` at `0x3cc90` stores buffer size at global `0x58510`, stores the boolean at `0x584e4`, and retains Java VM/JNI-related state. This inspected body does not store/use its sampleRate argument as a timeline offset.

Provider init `0x30af0` conditionally calls `System::setOutput(enum11)` when that boolean is set, then `setDSPBufferSize(bufferSize,4)`, then system init with512 channels. Playback scheduling queries the actual software sample rate separately. These are output/backend/buffering decisions. No `bufferSize/Fs` or reported output-latency quantity was traced into GameTimeline offset O or tap timing error.

Therefore the confirmed configurable timing compensation is the selected persisted offset (including the alternate `bt_offset` profile) plus AFF offset. Dynamic end-to-end device/DAC latency measurement and a separately added automatic compensation term are **not established** by these paths. Internal FMOD/OS output behavior is not a substitute for evidence of application-level judgment compensation.

### 8. Input latency: gameplay path and calibration differ

Expedition 004 established Java's pre-queue timestamp and native Touch `+0x40` storage. This investigation follows a concrete consumer outside the ordinary judge:

- GLViewImpl virtual `+0x100` resolves to main `0x12e0d48`, which calls Java `Cocos2dxGLSurfaceView.getTouchTimestampNow()` through JNI.
- Offset-calibration touch callback `0x192410c` has RTTI identifying `SettingsLayerV2Offset::showSync`'s dialog touch lambda (function-object vtable `0x1b32250`).
- It obtains current Android touch-clock time N, reads contact timestamp T from Touch+40, reads actual main playback position M through `0x1947af4`, and computes **M + T - N - expectedBeatTime**.
- Visible beat selection uses expected times1000,3000,5000,7000, with playback thresholds1999,3999,5999. It stores samples and updates display labels. Thus stored timestamp age is explicitly subtracted in calibration; it estimates playback phase at the recorded touch time rather than at callback handling time.

This is positive evidence for queue/touch-age-aware **calibration**. It does not prove calibration captures the earlier physical sensor timestamp, since the original timestamp is sampled in Java `onTouchEvent`, nor does it remove all audio-output latency.

For ordinary gameplay, recovered begin callback `0x194ff80` assigns ID/last-frame time, then calls `0xeec024`; that routine updates GameTimeline and calls tap classifier `0x160ce28` with note and generated ID, not the Touch object. The classifier reads E and compares it with note time. Continuous path `0x14858d4` likewise uses effective timeline time. No `AndroidNow - TouchTimestamp` subtraction or substitution of Touch+40 into the effective clock was found in these inspected judge/input routines.

Bounded conclusion: gameplay queue-age correction remains **unestablished**, while static calibration offsets and timestamp-aware calibration are confirmed. The calibration correction must not be silently imported into the gameplay algorithm.

### 9. Drift correction: what was and was not found

The inspected running updater `0x16c90bc` calls the steady clock and startup/fade dispatch, not `getBGMPosition`. After the ordinary startup anchor, C changes for pause handling, and explicit adjustment routines modify epochs/cursor; there is no feedback error term derived from periodically sampled audio position in that updater. The previously traced frame/input chain calls this updater rather than refreshing it from FMOD playback position.

Main playback-position wrapper `0x1947af4` has observed direct callers:

- `0x192410c`: offset calibration, described above.
- `0x1591420`: RTTI identifies a `StartScene::init` touch lambda; one branch compares position against static15930 and seeks forward to15930 when lower. This is a start-scene audio action, not a recurring gameplay clock correction.

Other inspected provider-position access includes main seek logic, a queued system-BGM routine `0xd64d80`, and a TopBar login-status function object `0x1020784`. Those accesses do not establish normal-gameplay drift tracking. Static scanning for provider-pointer `+0x2c0` followed by virtual+38 also did not identify such a loop; this search cannot prove absence of arbitrary indirect routes.

Provider `update` at `0x39ea0` calls `FMOD::System::update`, then result/error handling `0x48240` (returns immediately for successful zero result). It does not query current playback position or mutate the application timeline. Provider app/mixer `suspend/resume` at `0x3f708/0x49118` call `mixerSuspend/mixerResume` and set provider state, distinct from timeline pause/resume seek. All platform lifecycle ordering is not reconstructed.

**Supported model:** steady-derived gameplay clock, a startup anchor, configured offsets, pause-duration compensation, and explicit seek/resume realignment; DSP-clock scheduling coordinates audio channels. **Not established:** continuous application-level measurement/correction of steady-clock versus actual audio-playhead drift during ordinary uninterrupted gameplay. Synthetic long-duration checks confirm arithmetic behavior, not actual hardware oscillator drift.

### Validation

Executed original ARM64 instructions in Unicorn:

- Four settings-loading cases through the relevant prefix of `0x1a02b48`, including legacy migration/defaults; nine native offset-selection/sum basic-block cases. Surrounding settings backend/allocation is isolated.
- Five startup-offset scenarios (-500,-100,0,100,500), each checking before/equal/after the strict startup threshold and later progression.
- Pause freeze across four elapsed jumps, resume seek/unpause order, post-resume progression, five long-duration intervals (through day-scale synthetic elapsed time), three adjustment modes and manual/cursor branch.
- Twenty-one original calibration-callback cases across beat-selection boundaries and synthetic touch ages0/5/100 ms; actual age subtraction and sample stores execute, with spatial gate/clock/music getter/UI formatting hooked.
- Separate provider:45 BGM scheduling combinations across44100/48000/96000 sample rates, multiple parent clocks and delays; two main-group pause cases; four main-seek cases checking SFX reschedule versus stop.

Clock source, application audio dispatch, settings backend, FMOD APIs and one map-entry helper are hooked to synthetic values/call logs. Native timeline/start/pause/adjustment and provider scheduling/seek arithmetic execute. Provider scheduling tests include the float32 rounding example above. Full scheduled-SFX loading, real mixer output, Android input queues, device latency, actual oscillator drift, and every scene-specific lifecycle branch were not executed. No AFF samples exist in the supplied archive. Intermediate harnesses/results are not added to GitHub; the two authorized documentation files are the deliverables.

## Pseudocode

Field labels here are explanatory. Preserve signed32 arithmetic, conversion order and the distinct mode branches in a faithful implementation.

```text
load_offsets(settings):
    preset = getInt("audio_preset",0)
    regular = getInt("offset_int_2",INT_MIN)
    if regular == INT_MIN:
        legacy = getInt("offset_int",INT_MIN)
        regular = 0 if legacy==INT_MIN else signed32(legacy-20)
    alternate = getInt("bt_offset",INT_MIN)
    if alternate == INT_MIN: alternate=200
    return preset,regular,alternate

initialize_timeline(chart,settings):
    T = zeroed GameTimeline
    user = settings.regular if settings.preset==0 else settings.alternate
    T.offset = signed32(chart.AudioOffset+user)
    return T

start_model(model,steadyEpoch,systemEpoch):    # 0x8db04c
    optional model delegate notification
    model.timeline.Osteady=steadyEpoch
    model.timeline.Osystem=systemEpoch
    model.timeline.steadyMode=true

get_effective(T):
    if T.steadyMode: return signed32(T.R-T.C)
    return signed32(T.A-T.C-(3000 if T.A<=0 else 0))

update(T):                                  # 0x16c90bc
    if T.steadyMode:
        T.R=signed32(steady_ms()-low32(T.Osteady)-(3000 if T.A<=0 else 0))
        if T.paused: T.C=signed32(T.R-T.P)
        if not T.musicStarted:
            if get_effective(T)>-T.offset and not T.paused:
                T.musicStarted=true
                request_main_BGM_start(loop=false,index=0,delay=0)
                if T.steadyMode:
                    T.C=signed32(T.R+T.offset)
                    T.B=-T.offset
                else:
                    # Literal native fallback if mode changed during calls.
                    v=signed32(T.A-(3000 if T.A<=0 else 0))
                    T.C=signed32(v+T.offset)
                    T.B=signed32(v-T.C)
                if T.flag_2f: dispatch_startup_fade_calls()
    T.R=signed32(T.R+T.A)

set_paused(T,pause):                         # 0x9e74f4
    update(T)                               # with previous pause flag
    if pause:
        T.P=signed32(get_effective(T)-T.A)
        audio_pause(true)
    else if T.musicStarted:
        audio_seek(signed32(get_effective(T)-T.B))
        audio_pause(false)
    T.paused=pause

adjust(T,delta,mode):                        # 0xa19088
    if mode not in {1,2}:
        T.Osteady-=delta
        T.Osystem-=delta
        return
    if mode==2: T.flag_2f=true
    T.A=signed32(T.A+delta)
    update(T)
    audio_seek(get_effective(T))             # differs from resume's E-B

provider_play_BGM(loop,index,delayMs):
    channel=bgm[index]
    channel.setLoopCount(-1 if loop else 0)
    Fs=getSoftwareSampleRate()
    own,parent=channel.getDSPClock()
    samples=float32(float32(float32(delayMs)/1000)*float32(Fs))
    start=uint64(float32(samples+float32(parent)))
    channel.setDelay(start,0,true)
    unpause(mainGroup if index==0 else channel)

calibration_sample(touch,expectedBeat):      # 0x192410c
    androidNow=GLView.getTouchTimestampNow()
    M=audio_get_main_position()
    return M+touch.timestamp_40-androidNow-expectedBeat

ordinary_tap_error(note):
    return abs(note.startTime-get_effective(model.timeline))
    # No observed Touch.timestamp_40 age subtraction in this judge path.
```

## Unresolved Mysteries

Complete multiplayer/deferred-start policy and special-song adjustment semantics; every upstream scheduled-SFX timestamp producer; automatic audio-preset/route-selection policy; all indirect timestamp/audio-position consumers; physical output latency and native clock drift on devices; nonordinary integer overflow/mode transitions; complete foreground/background ordering between timeline pause and mixer suspend/resume.

These are bounded unknowns, not scheduled future directions or authorization for another expedition. Earlier documentation remains historical and is not rewritten.

## GitHub Status

Authorized outputs are this subject document and an appended Expedition 005 entry in `context.md`. No earlier subject file is modified. Exact commits and read-back verification are supplied in the Expedition Return Report after writing.
