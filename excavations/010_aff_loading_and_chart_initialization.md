# Expedition 010 — Full AFF Loading, Chart Initialization & Metadata Integration

Date: 2026-10-24. Project Arconist; repository `thgillwtnorizoh/arconist`, existing `main`.

## Result

**The essential objectives are met in bounded original-ARM64 execution.** Complete synthetic AFF text passes through original whole-file separation, body lexer/parser, header parser, LogicChart allocation, and the **entire ordinary LogicChart initializer `0x173b358`**, including runtime assembly, sorting/linking, checkpoint generation, count, auxiliary-object generation, depth preprocessing and group lifetimes. No manual assignments supply the resulting header fields, effective speed, note depths, checkpoints, judgment count or chart end.

A stronger resource-caller test executes `0x16e67a4`, original filename selection, original provider string-return wrapper, whole-file parsing, **original MD5 calculation**, metadata selection, speed selection/normalization and the native chart factory/initializer together. The resource bytes, metadata objects, settings backend and selected application environment remain supplied. This is not real Android file/account startup.

The optional small regression also succeeds: the fully initialized two-tap chart feeds the original spatial-index construction and native frame/projected input/score/gauge/result routines. It ends with PURE2, LOST0, score **10,000,002**, live H **80.4000015258789**, category3. Full gameplay or all special initialization branches are not claimed.

## What I Found

### 1. Preparation, identity and evidence scope

Read the project instructions, current cumulative context, complete009 report, and relevant002/005/008 parsing, offset and initialization evidence. Inspected the supplied archive and its songlist/packlist/unlocks metadata. Starting main is **`42e63ca6eb8da68896ded92e2aacb61fe8448341`**; no010 report existed at the initial check. The earlier recovery's scratch loader was actually present and inspected; new loading fixtures and runtime-service support were written for010. No inaccessible previous Work state or unrecovered script is claimed.

| Source | SHA-256 |
|---|---|
| `arccopy.zip` | `5dc2f3d1f5387d0c5da06ad72694105cdd7fa4b7ff80f981f77998e89eb2b4cb` |
| Project instruction text | `8a9bea2e002d6ce282dc7b92592379927088a2ecbab2e451b585aea4c921f1e8` |
| `lib/arm64-v8a/libcocos2dcpp.so` | `3eaca4e6dabb3395f276f8915698d57675757d0df0970e716b23a3dc201c79be` |

Main-library Build ID remains `17d660edbf37ca78beefc32e07672c97419ddce6`. All addresses in this report are **library-relative ELF virtual addresses before relocation**, in that main library. PT_LOAD mapping and RELATIVE relocations are applied; data VAs are not assumed equal to file offsets.

**Native-executed** means original instructions on the identified scoped path. **Instruction-backed** means decoded original code/relocations without a newly executed complete surrounding path. **Synthetic** means a supplied service, object/configuration or event schedule. **Interpretation** names inferred roles. **Unknown** means the path or provenance is not established. Descriptive function/field names are researcher labels; identified RTTI names are original metadata.

## Native loading and initialization call chains

### 2. Resource acquisition, filename selection and string ownership

The joined source-caller chain is:

```text
0x16e67a4(resource context, song, difficulty index, mirror flag, speed override, ..., inclusion)
  -> 0x1371744(song,index)                 filename/resource selection
  -> 0xb99da4()                           resource-provider singleton boundary
  -> provider.virtual+0x28 = 0x10f45e8     original std::string-return wrapper
       -> provider.virtual+0x38 = 0xd7845c byte/file loading boundary in these tests
  -> if returned string empty: return null
  -> 0x1870de0(text,inclusion)             complete AFF parser
  -> 0x16147c8(text)                       original CryptoPP MD5 / hex formatting
  -> 0x19833fc(song,index)                 selected difficulty object
  -> 0x8f2618(song)                        song-side integer
  -> choose requested speed
  -> 0xc052f4(...)                         allocate LogicChart and dispatch initializer
       -> chart.virtual+0x10 = 0x173b358
```

`0x16e6804` receives the loaded **24-byte libc++ string through X8 aggregate-return storage**. Short strings store size<<1 in byte0 and characters at+1; long strings have bit0 set, size at+8 and buffer at+16. `0x10f45e8` initializes that aggregate and supplies a callback shell to the lower file reader. The caller checks string length, copies it for parsing, calculates MD5 from the loaded text, and frees its temporary long-string buffers through the standard delete import. No raw borrowed Android buffer is passed directly to the lexer in this path.

The concrete lower reader `0xd7845c` contains path resolution and file/asset branches; `0xd71794` includes an absolute/file path and open/read path. Their real filesystem, Android assets and failure/retry policies were not executed. **The successful I/O hook supplies AFF bytes at `0xd7845c`; the original `0x10f45e8` wrapper still executes.** Provider lookup `0xb99da4` returns a prepared provider with its original vtable. This is an explicit resource-provider boundary, not a reconstructed storage backend.

For ordinary filename selection, `0x1371744` combines the supplied directory string at global `0x1bef230`, song ID, and `0xa58154(selectedDifficulty)`. `0x14ac910` keeps indices0..4 and maps other unsigned inputs to1. `0x19833fc` accesses song+228 plus8*normalizedIndex; `0xa58154` uses selected metadata `+124` to produce0.aff..4.aff, default1.aff. Thus filename selection is based on the selected difficulty object's class, not simply concatenating the original argument.

Executed with directory=`songs`, song ID=`expedition010`, and distinct metadata classes0..4:

| Requested index | Native selected resource |
|---:|---|
| 0 | `songs/expedition010/0.aff` |
| 1 | `songs/expedition010/1.aff` |
| 2 | `songs/expedition010/2.aff` |
| 3 | `expedition010_3`, with the special resource-prefix getter supplied empty |
| 4 | `songs/expedition010/4.aff` |
| 5 | `songs/expedition010/1.aff` |

Index3 and song byte+1c0 take a separate branch using the `_` form, integer-to-string conversion and `0xa382d4`/`0x107a824` resource-prefix machinery. The +1c0 branch prepends `dl_` before that transformation. Only the index3 form above was executed, with an explicitly empty prefix service; a universal on-disk location for these special resources is not claimed. The production initialization of the root-directory global remains outside coverage.

### 3. Whole-file parser and exact separators

**Entire `0x1870de0` executes** for the valid fixtures. It first searches for `\r\n-\r\n`, then, if absent, searches for `\n-\n`. The source code's control flow gives the CRLF search priority; this is not a generic line-reader replacement.

If `p` is the index of the newline sequence preceding `-`:

```text
header = text.substr(0,p)
body = text.substr(p+3)  # CRLF form: leaves trailing CRLF before first statement
body = text.substr(p+2)  # LF form: leaves trailing LF before first statement
```

Native substring calls are at `0x1870f18/0x1870f30`. The trailing newline is harmless native lexer whitespace; the body is not supplied separately by the driver.

The parser then runs **body first**, header second:

```text
0x137678c                         lexer state initialization
0xdf4a58 -> 0x814384               body token collection/lexer
0xb01d6c -> 0x139b96c -> 0x923240  parsed event objects
0x10dbff8                         native header-map construction
0x132525c                         attach/copy native header map to parsed chart
```

The driver never supplies native token classifications, parsed note objects or a prebuilt header map. Imported character/string/number services are listed below. The original grammar still distinguishes integer and float tokens.

### 4. Header-map behavior and bounded malformed input

Original `0x10dbff8` calls original splitter `0x95ef80` for newlines and colons. It requires at least two colon-separated components, a nonempty key and a nonempty second component **before CR removal**. It copies that second component, removes carriage-return characters, and assigns it into the native tree. Additional colon-separated components are not joined back into the value. It does not implement a generic whitespace-trimming configuration parser.

Executed examples:

| Input variation | Native map / initialized outcome |
|---|---|
| Ordinary LF | AudioOffset=`0`, density=`1.0`; two runtime taps |
| Same file with CRLF | Same header values, playable fields, count and depths |
| AudioOffset120, density2.0 | Native chart+c4=120, chart+c8=2 |
| Density header omitted | Native density defaults1 |
| Both LF header values empty | Entries absent; offset0, density1 |
| Add `Custom:a:b` | Native map stores `Custom`=`a`; gameplay header outputs unchanged |

Missing or malformed separators are **not** reported as cleanly rejected files. In the inspected missing-separator branch, not-found is −1 and body substring position wraps to1; the native lexer is given the original text starting at byte1. For the two tested files (separator removed, or replaced with ` - `), whole-file parsing did not return within the **5,000,000-instruction per-call limit**. The native lexer reached its invalid-character/token path repeatedly; no parsed chart or successful initializer is claimed. This is bounded noncompletion in the supplied runtime, not a proof of every malformed file's outcome, an in-device hang, or a completed exception-unwind test.

An empty returned resource string is different: original `0x16e681c -> 0x16e6968` returns null before whole-file parsing, MD5 or chart allocation. This path was executed with an empty I/O result.

## Original LogicChart initialization

### 5. Allocation and input contract

`0xc052f4` allocates **0x118 bytes**, zeroes the chart with original stores, installs the original LogicChart vtable **`0x1b31408`**, initializes native container headers, and calls its initializer virtual+10. Success returns the chart through the autorelease boundary; the explicit false-result branch deletes it and returns null. Ordinary tested initializations return1. That false-result branch was inspected, not forced as a newly recovered reachable chart-validation failure.

Recovered argument roles at the initializer entry:

| Argument | Role in the tested path |
|---|---|
| X0 | allocated LogicChart |
| X1 / X2 | song object / selected difficulty object |
| X3 | original parsed whole-file chart |
| W4 | caller flag stored bit0 at chart+cc; ordinary resource caller supplies0 |
| W5 | song-side integer; passed to runtime builder and bar-generation path |
| X6 | original complete-text MD5 string in the resource-caller chain |
| W7 | mirror flag; stored bit0 at chart+cd |
| S0 | requested speed in ordinary units, stored chart+f0 |
| entry stack+0 | inclusion/configuration integer, stored chart+d0 |

The resource caller passes its inclusion argument both to whole-file parsing and the factory. Its full product/scene selection remains caller-specific. Do not rename the song-side W5 as an AFF header or equate all of these flags with a single mode.

### 6. Executed initializer order

The successful tests enter `0x173b358` normally and execute its complete ordinary return path, rather than jumping among postprocessing blocks:

1. Store metadata pointers, requested speed, flags and MD5 string; copy/read the parsed native header map.
2. Retrieve AudioOffset and TimingPointDensityFactor values. Missing lookups use empty string values in temporary map copies.
3. Run MD5/song-ID special-property checks and derive chart+110/+111 where applicable. Ordinary fixtures retain0.
4. Call native metadata BPM selector `0xe17528` and compute chart+f4 speed normalization.
5. Convert AudioOffset via **`0x173bcfc -> atoi`**; store+c4 and default+c8=1. Nonempty density uses **`0x173bd34 -> atof`**, converts double to f32 and replaces+c8.
6. Call runtime builder **`0x173bd4c -> 0x1862a14`**.
7. Sort **`0x173bd54 -> 0x7b6a08`**, link/group arcs **`0x173bd5c -> 0x125e474`**; dispatch long-note record generation, with arc geometry/flag-specific handling on arc branches.
8. Count judgment units **`0x173bf28 -> 0x11ea120(chart,0,INT_MAX)`**, store chart+b8.
9. Generate auxiliary bars **`0x173bf38 -> 0xec2a5c`**, then sort again. Call `0x8e04ec` three times, `0x100ae64`, and `0xc34008`. Whole helper calls execute; arc-specific interiors are not covered by the tap/hold fixtures.
10. Original loop **`0x173bfb0..0x173c1d8`** computes both endpoint depths and writes current+30/+34 and precomputed+38/+3c, including arc-child handling on applicable branches.
11. Set nondefault group lifetime from member end+1200, and default group end INT_MAX **`0x173c1dc..0x173c24c`**.
12. **`0x173c250 -> 0x18e8aa4`**, then delete the parsed chart; clean up temporary header strings and return1.

The count occurs **before auxiliary bars are appended**. Sorting helper observations include recursive calls; an entry-observer total is not the number of top-level sort phases.

The successfully initialized AFF tap/hold objects and depths match the corresponding prior fixtures. The full chart additionally contains original RTTI **LogicBar**, vtable `0x1a82298`, generated by `0xec2a5c`. FixtureA has **506 main runtime objects = two taps plus504 bars**, yet native N=2 and chart end2120. FixtureC has505 objects, N3 and end2500. In this tempo120/beats4 fixture bars run from−4000 through1002000 in2000 ms increments. Their existence must not inflate judgment N or replace chart completion with the last auxiliary object's time.

The original builder's final timing bounds in these full initializations are first start **INT_MIN**, last end **chartEnd+1,000,000**. ForA: `[-2147483648,1002120]`, tempo120, scale0.0833333358168602. ForC: end1002500. The bounded fixtures establish these values; they do not establish an audio-duration policy for every special chart.

### 7. Fields and their actual producers

| Object | Offset | Producer / meaning |
|---|---|---|
| Parsed chart | +0/+8/+10 | native header tree: leftmost/root/count |
| Header tree node | +20 / +38 | 24-byte key string / value string; native node size0x50 |
| Parsed chart | +18/+20/+28 | main parsed-object pointer vector |
| Parsed chart | +30/+38/+40 | parsed timing-group-related pointer vector |
| LogicChart | +10 / +18 | initializer's song / selected difficulty pointers |
| LogicChart | +20/+28/+30 | runtime main-object vector, later includes auxiliary bars |
| LogicChart | +38/+40/+48 | per-group timing-list pointer vector |
| LogicChart | +50/+58/+60 | group-descriptor pointer vector |
| LogicChart | +b8 | native judgment-unit count at173bf2c |
| LogicChart | +bc | runtime builder's chart end; A2120/C2500 |
| LogicChart | +c4 / +c8 | native header-derived AudioOffset i32 / density f32 |
| LogicChart | +cc / +cd / +d0 | caller flag / mirror / inclusion-config integer |
| LogicChart | +f0 / +f4 | requested speed / BPM-normalized speed |
| LogicChart | +f8 | copied complete-text MD5 string |
| LogicChart | +110 / +111 | native digest/song-ID/difficulty property branches; not ordinary supplied defaults |
| Song metadata | +0 / +188 / +1b0 / +1c0 | ID string / base BPM f32 / side integer / special-resource flag |
| Song metadata | +228 +8*index | selected difficulty pointer array |
| Difficulty | +50 / +124 | optional base-BPM override f32 / rating-class integer |
| Timing | +10/+14; +18/+20/+28 | interval bounds; scaled tempo/original tempo/scale |
| Runtime position | +c/+10/+14 | integer discriminator/internal lane/normalized X |
| Long note | +70; +78/+80/+88 | native interval; checkpoint vector (12-byte records) |

## Configuration provenance

### 8. Requested speed is not the runtime timing multiplier

Resource caller `0x16e6874..0x16e68c4` uses a nonzero explicit W4 speed-in-tenths override as supplied. If it is zero, it reads application+70 settings+0c and clamps the selected stored integer to **10..65** in the tested ordinary branch. It then computes `requested=f32(scvtf(tenths)/10.0)`.

Settings prefix **`0x1a02b48..0x1a02cec`** reads `highspeed_int` with INT_MIN sentinel. If absent, it reads legacy `highspeed` float, default1.0, and stores `trunc(f32(legacy*10))` at settings+c. This prefix was executed with a supplied key/value backend and connected through the same settings object to native resource loading. Later account/settings initialization is deliberately not executed.

Metadata selector **`0xe17528`** normalizes difficulty index, chooses nonzero difficulty+50 or otherwise song+188, then **FCVTZS converts the chosen BPM to i32**. Initializer **`0x173bc6c..0x173bc80`** computes:

```text
baseBpmInt = native_metadata_BPM_selector(song, difficulty.ratingClass)
chart.requested_f0 = requested
chart.effective_f4 = f32(f32(requested * 180.0) / f32(baseBpmInt))
```

`0x1862a14` passes+f4 to timing initializer **`0xbe2b98`**; native timing arithmetic is:

```text
m = f32(affTempo * chart.effective_f4)
scale = f32(f32(1.0 / m) * 60.0)
```

Executed complete initialization, all with AFF tempo120:

| Requested | Song base BPM | Difficulty override | Native+f4 | Tap1000 pre-depth |
|---:|---:|---:|---:|---:|
| 4 | 120 | 0 | 6 | −12000 |
| 4 | 178 | 0 | 4.044943809509277 | −8089 |
| 4 | 120 | 240 | 3 | −6000 |
| 4 | 120 | 100.9 | 7.199999809265137 | **−14399** |

The last row preserves integer BPM selection and float32 operation order; replacing the recovered expression with a decimal-real calculation can change truncated depth.

Executed settings→source-caller→full initialization cases (base BPM120):

| Explicit tenths override | Supplied settings backend | Native requested / effective speed |
|---:|---|---|
| 0 | highspeed_int40 | 4 /6 |
| 0 | only legacy highspeed3.7 | 3.700000047683716 /5.550000190734863 |
| 0 | neither key | 1 /1.5 |
| 0 | highspeed_int0 | 1 /1.5, caller clamp |
| 0 | highspeed_int66 | 6.5 /9.75, caller clamp |
| 80 | neither key | 8 /12, explicit override bypasses that stored-setting clamp |

No universal fallback for invalid/zero/nonfinite BPM or density is invented.

### 9. Metadata and flag provenance table

| Value | Native producer | Source | Consumer | Verification status |
|---|---|---|---|---|
| AudioOffset |1870de0→10dbff8 map;173bcfc atoi/store+c4|AFF header|chart;005 model timeline offset sum|**Native-integrated parsing/initialization**; no new hardware-audio measurement |
| Density factor |173bd04 default1;173bd34 atof/narrow/store+c8|AFF header|1862a14→hold/arc shared interval initialization|**Native-integrated hold checkpoints**, density1/2 |
| Requested speed |1a02cb8/1a02ce8 settings+c;16e6874..68c4|persisted highspeed_int, legacy highspeed/default, or caller override|chart+f0; normalization|**Native-integrated scoped settings prefix and source caller**; backend supplied |
| Effective speed |e17528;173bc6c..bc80|requested speed and selected integer metadata BPM|chart+f4→be2b98|**Native-integrated**, four metadata cases |
| Song base BPM |d98aa8 JSON bpm_base; d9db88/d9dc24→1a19f58;store1a1a288|songlist bpm_base|song+188; e17528|**Instruction-backed JSON/constructor provenance**, synthetic metadata supplied during execution |
| Difficulty BPM override |d9acdc/d9ad0c default0;d9c7c4/d9c808→1a22aec;store1a22b78|optional difficulty bpm_base|difficulty+50; e17528|**Instruction-backed producer**, scoped native consumer execution |
| Difficulty/index |d9a280 ratingClass read, normalization near d9a434, constructor1a22c24;19833fc|songlist difficulties; caller index|metadata selection; a58154 filename; speed selector|**Instruction-backed JSON**, native selection/path tests |
| Mirror |16e68c8 from caller bit;173b3a0 store+cd|scene/gameplay configuration|runtime position conversion|**Native-integrated consumer**, raw3/2 become IDs4/3 or mirrored3/4; upstream selection incomplete |
| Song side |d98c40 side read;d9923c spill;d9dc1c/24→1a19f58;1a1a2b0 store|songlist side, bounded below5 in that parser path|8f2618→runtime builder/bar construction|**Instruction-backed JSON-to-field chain**, native caller transfer; no new full gauge-side matrix |
| Chart caller flag+cc |16e68dc supplies0 in ordinary resource path;173b39c|caller context, not either recovered AFF header|chart/special consumers|**Native-executed ordinary0**, broader meaning/reachability unknown |
| MD5 and properties |16147c8;173b698 onward digest comparisons and song-ID branches|complete loaded bytes; selected song metadata|chart+f8, special+110/+111, speed exception|**MD5 native-executed**, ordinary properties0; special branches instruction-backed |
| Filename/root |1371744,14ac910,19833fc,a58154|directory global, song ID, difficulty metadata; special-resource state|resource provider|**Native-executed selection**, directory/prefix/storage environment supplied |

The ordinary scene callsite **`0xe2f0b0..0xe2f0dc`** passes song, selected difficulty, speed and inclusion state. If its optional context pointer X5 is nonnull, byte+3b is converted into the mirror argument. Alternate caller `0x12d5280..0x12d52ac` reuses existing chart+cd and requested+f0*10. Neither trace establishes every writer/equipment/unlock rule for that context byte. That account/selection boundary is a stopping point.

Archive inspection confirms `assets/songs/songlist` contains `bpm_base`, `side` and per-difficulty `ratingClass`; the first song has ID`sayonarahatsukoi`, bpm_base178 and side0. Native songlist loader/parser **`0xd97d60`** references `songs/songlist`, reads those JSON keys, and calls the constructors listed above. The JSON loader and constructors as a whole were **not** executed for the real archive in010. Metadata association is instruction-backed, not merely inferred from similarly named JSON keys.

`packlist` describes packs; `unlocks` describes conditions keyed by song/difficulty. Their presence does not establish a direct LogicChart field producer. No new direct feed from those two resources to this initializer was established; entitlement/account/database/network paths are not reconstructed here.

Original `0x16147c8` uses CryptoPP Weak1::MD5 RTTI and native filtering/hex formatting. For exact FixtureA bytes below it returns **`7fad5130f9c122e20bb21234d772e927`**, independently matched to host MD5 as an assertion, not substituted by it. Initializer+f8 retains that actual string. Its temporary property-check string replaces the final character with `0` before comparing fixed32-character identifiers. Song-ID checks include `dropdead` (difficulty2 has a minimum effective speed2.5), `yourbestnightmare` for a difficulty-dependent+111 property, and other named special cases. These branch instructions are preserved; the ordinary fixtures do not establish all special properties or their product reachability.

## Recovered pseudocode

### 10. Instruction-backed loading/reference interfaces

```text
load_chart(song, index, mirror, speedOverrideTenths, inclusion):  #16e67a4
    path = native_select_resource(song,index)                   #1371744
    text = native_provider_return_string(path)                  #10f45e8; byte I/O supplied
    if text.length == 0: return null
    parsed = native_parse_whole_AFF(text,inclusion)              #1870de0
    md5 = native_MD5_text(text)                                 #16147c8
    difficulty = native_select_difficulty(song,index)            #19833fc
    side = native_song_side(song)                               #8f2618
    tenths = speedOverrideTenths
    if tenths == 0:
        tenths = clamp_i32(settings.highspeedTenths,10,65)
    requested = f32(scvtf(tenths)/10.0)
    return native_chart_factory(song,difficulty,parsed,
                                callerFlag=0,side,md5,
                                mirror,inclusion,requested)    #c052f4

parse_whole_AFF(text,inclusion):                               #1870de0
    p = native_find_CRLF_dash_CRLF(text)
    if found(p): advance=3
    else: p=native_find_LF_dash_LF(text); advance=2
    header = native_substr(text,0,p)
    body = native_substr(text,unsigned64(p+advance),NPOS)
    tokens = native_body_lexer(body)                            #df4a58/814384
    chart = native_body_parser(tokens,inclusion)                 #b01d6c
    headerMap = native_parse_headers(header)                    #10dbff8
    native_attach_map(chart,headerMap)                          #132525c
    return chart
    # No invented missing-separator recovery or clean error return.

initialize_LogicChart(chart,song,difficulty,parsed,flags,side,md5,requested):
    store_native_metadata_flags_requested_speed_and_md5()
    offsetText = native_header_lookup_copy(parsed,"AudioOffset")
    densityText = native_header_lookup_copy(parsed,"TimingPointDensityFactor")
    native_digest_song_and_difficulty_properties()
    baseBpmInt = native_select_BPM(song,difficulty.ratingClass)
    chart.f4 = f32(f32(requested*180.0)/f32(baseBpmInt))
    apply_native_special_speed_branch_if_reached()
    chart.c4 = imported_atoi(offsetText)
    chart.c8 = f32(1.0)
    if densityText.length != 0:
        chart.c8 = f32(imported_atof_double(densityText))
    native_build_runtime(chart,parsed,side)                      #1862a14
    native_sort_main(); native_link_arc_groups()
    native_geometry_and_long_note_record_generation()
    chart.b8 = native_count(chart,0,INT_MAX)                     #11ea120
    native_generate_bars(chart,side); native_sort_main()
    native_three_8e04ec_passes(); native_100ae64(); native_c34008()
    for note and applicable arc child:
        # actual initializer loop integrates each note's timing group
        d0 = native_f32_integral_at_start()
        d1 = native_f32_integral_at_end()
        note.preDepthStart = note.currentDepthStart = fcvtzs_i32(d0)
        note.preDepthEnd = note.currentDepthEnd = fcvtzs_i32(d1)
    native_set_nondefault_group_end_from_members_plus1200()
    defaultGroup.end = INT_MAX
    native_destroy_and_delete(parsed)
    return true
```

## Native validation results

### 11. Exact AFF fixtures and initial state

FixtureA is the following ASCII text, **including a final LF**:

```aff
AudioOffset:0
TimingPointDensityFactor:1.0
-
timing(0,120.00,4.00);
(1000,3);
(2000,2);
```

FixtureB changes AudioOffset to120 and density to2.0. FixtureC replaces the two taps with `hold(1000,2000,3);`. A secondC uses density2.0 to expose propagation to record generation. LF/CRLF, omitted density, both empty LF values, unknown `Custom:a:b`, and two missing/malformed-separator cases form the bounded header matrix.

Direct parser→factory fixtures supply only **metadata/configuration inputs**, not derived chart fields: song ID`expedition010`; song BPM120; selected difficulty class2, override BPM0; requested speed4; mirror0 unless specified; side0; caller flag0; inclusion1. They pass the actual parsed pointer into `0xc052f4`; its complete initializer consumes/deletes it. These direct-stage fixtures supply MD5 argument`fixture0`, clearly distinct from the source-caller proof with actual native MD5. Their resulting+c4/+c8/+f4/+b8/+bc/depths are never patched by the driver.

The source-caller proof supplies complete AFF bytes at the I/O boundary, directory=`songs`, the same metadata, explicit speed40 tenths or the tested settings prefix output, and inclusion1. It executes the original MD5; no synthetic digest, parser/header objects, chart-end/count/pre-depth writes or initializer-control-flow skips are used there.

### 12. Expected versus observed native outputs

| Test | Expected assertion | Observed |
|---|---|---|
| Whole FixtureA | native headers plus timing/two typed integer taps | exact map; parsed vtables Timing1b34b28, SimpleNote1ab62b8; times0/1000/2000 |
| A full initialization | N2/end2120, normalized6 | N2/end2120; lane IDs4/3; pre-depths−12000/−24000; 506 total objects |
| B | headers propagate without moving note timestamps | offset120/density2; N2/end2120, same tap timestamps/depths |
| C density1 | interval250, three records | records1250/1500/1750, weight1 unresolved0; N3/end2500 |
| C density2 | interval125, seven records |1125/1250/1375/1500/1625/1750/1875, each weight1; N7/end2500 |
| Mirror | preserve integer-position translation | raw3/2→IDs4/3 ordinary,3/4 mirrored |
| Grouped fixture | separate native timing/group and depths | add `timinggroup(){timing(0,60.00,4.00);(1500,1);};`: groups2/N3/end2120; group1 tap depth−9000, lane2; group ends INT_MAX/2700 |
| LF vs CRLF | same semantic playable output | same headers, N/end/lanes/depths; whole-byte MD5 equivalence is not asserted |
| Missing/empty optional values | recovered defaults | offset0/density1 |
| Unknown colon-containing header | retain only second split component | Custom=`a`, no change to observed gameplay header fields |
| Resource caller | select path, parse, MD5, initialize | songs/expedition010/2.aff; real MD5 above; N2/input4/effective6 |
| Empty resource | no parsed chart | null; no parser/MD5/factory entries |
| Missing/malformed separator | no fabricated clean-success fallback | neither returned within5M instructions; lexer-stage noncompletion |

The grouped test is native whole-file parsing and full initialization, not manually inserted group descriptors. Each timing list's first start is INT_MIN and last end1002120; group1 tempo60 gives scale0.1666666716337204. Default-group bar generation does not add a second group-wide judgment count.

### 13. Small gameplay regression

The successful source-loaded FixtureA chart is passed unchanged into original **`0xfc0184..0xfc02a4 -> 0x1576aa4`**. Original maps include the initializer's bars; active membership is not supplied. Native N2 is read by original score/gauge factory `0x14f0a94`; the driver does **not** overwrite chart+b8 or+bc.

Prepared model/scene/timeline/Director/orthographic Camera and external delegates are the009-style synthetic environment. Controlled timeline anchor−3000, flags+2d/+2e=1, offset0 and ordinary mode0/no ability are explicit. Design1280×720, projection diagonal(1/1280,1/720,1,1), Camera Z0; completed widening transitions give G1/W0. The scene delegate logs/returns; result finalization is driver-invoked after native completion.

Run whole model frame `0x10a7550`, then original begin input `0xeec024` at E1000/design(740,360) and E2000/design(540,360), with distinct supplied generated contact IDs. Run frame2121, native snapshot `0x1600bb0` and result queries `0x1315038/0x12a5574`.

Observed: native finished1, PURE2/shining2, recorded/final LOST0/0, score10,000,002, liveH80.4000015258789, final flooredH80/category3. This validates the reduced chart-initialization boundary, not full metadata/account/model startup, physical input, GPU or audio hardware.

### 14. Execution environment and explicit hooks

Unicorn2.1.4, Capstone5.0.9, pyelftools0.33. Main image0..0x2100000; supplied arena0x4000000..0x6000000; stack/TLS within0x6000000..0x6100000; SP0x60df000; TPIDR_EL0=0x60f0000; return sentinel0x4000100. Bump heap starts0x4100000 with64-byte alignment. Each native call has a5M-instruction limit; scoped settings/index blocks stop at the specified end address. No real-device execution is claimed.

| Hook / supplied boundary | Exact supplied role and limit |
|---|---|
| new1a6d9c0; malloc1a6df10; optional new-array/nothrow1a6dd40/1a6e090/calloc1a6ee10 | zeroed aligned bump allocations; no allocation-failure coverage |
| delete1a6d9e0, free1a6ded0, optional array-delete1a6e0a0 | no reclamation; original container/tree/destructor control flow still executes |
| Ref ctor121a0ec, retain147fe48, release d6dc98, autorelease10ac6e8 | no-op reference services; no real pool/reclamation proof |
| memcpy1a6d9d0, memmove1a6daf0, memset1a6db30, strlen1a6dad0, memchr1a6db40, memcmp1a6da80, strcmp1a6e100 | host byte operations/lexicographic comparisons |
| string copy1a6da50, assignment1a6db80, compare1a6da60, substring1a6dc20, append1a6db00/1a6db20, push1a6dda0, erase1a6e1a0, reserve1a6e8c0 | libc++ short/long strings with native inline layout; host storage/comparison primitives only; original separator/header splitting/tree logic executes |
| to_string1a6db60 | integer-to-string aggregate result; used by special filename test |
| lexer iswspace1a6e200; ctype pointer through GOT1b96168 | ASCII classification/whitespace, upper1/lower2/digit4 at table[c+1]; non-ASCII/locale unverified |
| numeric stringstream ctor1087f14 / dtor b06728; extraction1a6e210/1a6e230 | capture **native-scanned substring**, supply f32/int conversion; native token/grammar decisions retained |
| atoi1a6dd80 / atof1a6e150 | host ASCII numeric-prefix conversion; atof returns double then original FCVT narrows; malformed/locale/overflow compatibility not established |
| dynamic_cast1a6db90 | original relocated RTTI single-inheritance identity/base-chain resolver; general ABI not claimed |
| guard acquire1a6dd00/release1a6dd20, uncaught_exception1a6dd90 | single-threaded guard byte state; no active exception; needed by original native MD5 path; no threads/unwinding |
| bda064 configuration getter | return ordinary configuration0 when queried; rare mode reachability not established |
| b99da4 provider getter | return supplied provider carrying original vtable1aa8af0 |
| d7845c provider byte loading | set wrapper-owned output string to fixture bytes and return0; actual path access/Android assets unexecuted |
| 107a824 resource-prefix service | empty aggregate string **only for special index3 filename test**; not encountered by ordinary index2 resource proof |
| 18a6b8c + prepared backend virtuals | fixture settings values/defaults for original settings prefix; synthetic arena callback addresses0x4000300/0x4000310/0x4000320 implement bool/int/float getters, respectively (these three are not ELF VAs); no database/account initialization |
| optional regression clock1a6dc60; Director a4227c / size f09110 | controlled nanoseconds and design/frame dimensions1280×720 |
| optional regression audio107af5c, delegate methods, result e2388c / time1a6de50 | suppress external UI/audio; deterministic epoch and optional-null helper; no result arithmetic replaced |

Native allocation already zeroes the chart with original instructions; supplied allocator zeroing is not presented as the producer of fields the factory explicitly initializes. Original MD5 compression/filtering, native sorting/tree operations, whole-file/body/header parsing, chart construction/count/end/depth and successful checkpoint arithmetic are not replaced by Python formulas. Host MD5 is used only to compare the observed native digest.

Native `__cxa_allocate_exception` and `__cxa_throw` boundary observers were available during malformed-input exploration; successful fixtures do not require exception substitution. The two missing-separator tests hit the execution limit in the lexer rather than completing a throw/unwind. Full C++ exception handling remains unverified.

## Remaining synthetic dependencies

The following inputs remain intentionally supplied: resource bytes/storage, root/prefix environment, song/difficulty metadata object construction, settings key/value storage, caller mirror/inclusion/configuration state, reference-count pools/ownership, selected process globals and standard-runtime services. JSON metadata provenance is decoded, but the actual archived songlist-to-native-object creation pipeline is not newly executed as a whole.

The advancement over009 is concrete: the original source caller and entire chart initializer now obtain/derive the header map, AudioOffset, density/default, speed selection/normalization, positions, runtime notes, group/timing structures, long-note records, native count, chart end, auxiliary objects, pre-depths and group ends. These outputs no longer require the prior direct field assignments or selected initializer-block calls.

## Unresolved Mysteries

1. Actual resource-provider storage/encryption/cache/prefix selection and all I/O failure/retry branches on Android. The successful supplied byte boundary does not prove deployed paths or bundled AFF availability.
2. Complete archived metadata JSON loader execution, all constructors, downloaded-song flags, entitlement/unlock/account writers and every metadata default. Stop at the established metadata interfaces.
3. Every producer of caller mirror/+cc/inclusion state, and complete special digest/song-ID/difficulty property reachability. Their ordinary0/nonmatching paths are not broad mode proofs.
4. Invalid/nonfinite/overflow/locale numeric inputs, all separator combinations, full malformed-body failure/unwind behavior and non-ASCII lexer compatibility. The bounded missing-separator noncompletion must not be generalized to all errors.
5. Arc-specific helper transformations, all checkpoint weights/child-generation modes and every timing-group attribute in the full initializer; prior009 evidence remains separately scoped.
6. Full chart/model lifecycle reclamation, Android/GL queue execution, real clocks, audio output, GPU, persistence and networking. Optional gameplay here is a small synthetic-environment regression.
7. FlickNote gameplay remains unproven. This expedition neither requires nor fabricates a playable construction path and adds no new flick reachability claim.

These are limits of010, not authorization or a launch plan for011.

## GitHub Status

Authorized changes: this new report and an append-only010 entry in `context.md`, on existing main, based on `42e63ca6eb8da68896ded92e2aacb61fe8448341`. Reports001–009, README, earlier context, project instructions, binaries and archive assets are preserved. Harnesses/traces are scratch intermediates and are not authorized commit contents. Exact publication SHA, pinned read-back equality and final preservation comparison are reported in the headquarters return after committing; no self-referential future SHA is invented here.
