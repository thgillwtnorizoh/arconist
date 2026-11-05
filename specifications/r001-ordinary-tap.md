# R001 ordinary tap behavior and reconstruction boundary

Authority: immutable research parent0c174c6e481158ae73e4d7c18afabaa670794d2d.
References: excavations002/005/006/008/009/010/024/035/042 and unchanged
research_harness fixtures/source. Native-executed observations outrank engineering
choices within their verified scope. This document does not authorize a new expedition.

## Chart and clock

Supported syntax is explicitly bounded by reconstructed/README.md. Integer raw
position0..5 becomes lane1..6, normalized X=0.5*(lane-2), tap start=end=AFF time.
Each ordinary tap contributes one judgment unit. Chart end=max(tap time+120).
Default ordinary metadata uses requested speed4 and base BPM178, matching the
024/035 native fixtures; these values are configurable inputs, not chart outputs.
Timing effectiveSpeed=f32(f32(requested*180)/baseBpm),
scale=f32(f32(1/f32(tempo*effectiveSpeed))*60).

For supported uninterrupted steady mode, origin is supplied at start, A=0:

```text
on clock refresh(wall):
    R = signed32(wall-origin-3000)
    E = signed32(R-C)
    if music not started and E > -(AFFoffset+userOffset):
        musicStarted = true
        C = signed32(R+AFFoffset+userOffset)
    E = signed32(R-C)
```

Epoch translation is an engineering adapter. Physical audio playback, startup
scene construction, pause/manual-clock/seek and Android transport are not modeled.
DOWN refreshes E; UP only removes the retained contact. The stored external event
timestamp does not replace current Timeline E (005/008). Every event is executed
in the schedule's array order, including equal wall times; time cannot go backwards.

## Native-derived depth, index and frame order

For positive default-group timing, integrate each record up to min(record end,t):
`D -= f32(f32(bound-max(start,0))/scale)`. Insertion key truncates
`f32(D(noteTime)/-10000)` before indexing; keys are not computed from truncated
pre-depth. Precomputed note depth separately truncates D(noteTime) to signed integer.
Current depth truncates `f32(storedIntegerPreDepth + f32(-D(E)))`.

```text
FRAME:
    refresh Timeline; publish lastFrameE
    A=f32(-D(E)); B=f32(-D(E+120))
    update retained note depths
    remove terminal (missed or consumed or finished) notes when E>note.end
    lo=min(trunc(f32((A-700)/10000)),trunc(f32((B-700)/10000)))
    hi=max(trunc(f32((A+10000)/10000)),trunc(f32((B-700)/10000)))
    query indexed notes in signed keys[lo..hi]
    admit previously inactive unresolved taps only if current depth<300
    for active unresolved taps: if E>note.end+100, record LOST
    if E>chart.end: mark finished and cache ordinary GameResult
```

Range processing precedes expiry: a newly missed tap remains active until a later
frame, and can still be collected before its missed guard rejects it. Retention
does not reapply the new-admission depth threshold. No catch-up sweep fabricates
recorded misses for never-admitted notes. Snapshot reconciliation remains separate.

Engineering substitutions: managed collections replace C++ pointers/trees; empty
native buckets need not be allocated. Auxiliary bars, engine scene stamps, rendering
and reference counting are omitted. One ordinary group and positive timing only.
Exact depth equivalence is asserted at the published035 sampled endpoints; arbitrary
tempo-change/long-gap native equivalence is not claimed from these limited fixtures.

## Initial input, guards and judgment

```text
DOWN(pointer,lane):
    retain contact with a generated monotonically increasing ID
    if finished: stop
    refresh Timeline (without range maintenance or expiry)
    candidates = active notes matching internal lane
    sort by signed start time (equal-time source ordinal is an engineering choice)
    for note in candidates:
        if missed or successfullyConsumed: continue
        error=abs(E-note.start)
        if error>120: continue
        if error>100: record LOST; stop input iteration
        id=0 if error<=25 else 1 if error<=50 else 2
        record accepted; stop input iteration
UP(pointer): release retained contact; do not score
```

Missed and successful-consumption bytes are distinct. A LOST classifier return
consumes initial input without setting successful-consumption or accepted contact.
Frame-first035 sets older missed, then initial input visits both candidates and
accepts newer error1. Input-first035 consumes older error110 as LOST and never
classifies newer. Candidate sorting is chronological, not minimum absolute error.

## Score, gauge and completion

Accepted ID0 increments shining and PURE; ID1 PURE; ID2 FAR. Nonshining accepted
judgments count early when E<noteTime, otherwise late. Acceptance sets successful
consumption/contact, then updates counters, gauge, score and combo/max. LOST sets
missed, increments recorded LOST, applies ordinary damage2 and resets combo; max
persists. A miss does not recompute the stored accepted-count score.

For positive count N and song scaling byte0/no ability/mode0:

```text
T=f32(200+f32(N*0.5))                     for N<400
T=f32(280+f32((N-400)*0.5))               for 400<=N<600
T=f32(360+f32((N-600)/5))                 for N>=600
gain=f32(f32(T/2.5)/N)
acceptedGain = gain for ID0/1, f32(gain*0.5) for ID2
H=clamp(f32(f32(H+acceptedGain)-damage),0,100)
score=10000000+shining if PURE==N
otherwise:
    weighted=10*PURE+5*FAR
    q=integer_divide(weighted*1000000000,N)
    score=min(integer_divide(q,1000),10000000)+shining
```

At completion, final LOST=N-PURE-FAR; recorded LOST is preserved separately and
unrecorded final LOST does not cause retroactive damage. Result score uses the
ordinary accepted counts and final total. Result health=floor(live H). Ordinary
category=0 when integer H<70, otherwise1 if LOST>0,2 if FAR>0,3 otherwise.
Result also carries shining/PURE/FAR, recorded/final LOST, max combo and early/late.
The managed result is cached; no presentation, persistence or GameSession is claimed.

## Verification scope

R001 asserts024 ordinary transitions/final result and035 both exact orderings,
with chart IDs, E/last-frame E, candidates/classifier returns, guards, counters,
score, combo/max, health bits, cleanup/completion and available result fields.
The reference README labels native-executed and instruction-backed sources.
Additional boundary tests exercise both signs at25/50/100/120, strict expiry,
completion, admission hysteresis, duplicate guards, offsets and negative inputs.
No Godot/Unity/device/audio/visual validation or042 six-note integration milestone
is implied by reusing the verified ordinary numerical algorithms.
