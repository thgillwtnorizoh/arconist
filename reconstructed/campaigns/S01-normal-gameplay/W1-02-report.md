# W1-02 — original graph, arc-child and candidate-conflict closure

2026-11-20, Asia/Bangkok. **BLOCKED for generalized native-integrated closure;
reference-pack structural/provenance validation PASS.** No new native experiment.

## UEP-001 checkpoint

| Field | Result |
|---|---|
|Project / Campaign / Actor / Assignment|Arconist / S01 Normal Gameplay / Work1 original research and independent verification / W1-02, issue #7|
|Status|**BLOCKED**:existing evidence closes instruction contracts, but broader owned graph/child/conflict runtime ledgers are absent. Published partial findings are preserved.|
|Starting SHA|`16d17765e6fe50251162a45ffd5d1a64f243acf5`, matched remote main; isolated detached worktree|
|Published SHA|Non-forced descendant containing this report; exact identity and completed remote readback supplied in handoff. A commit cannot embed its own SHA.|
|Exact tested SHA|**NONE for production/native runtime in W1-02**. Source assessed:accepted `49e7c263a36aebcc0316e010a629c6bfdf205f6d`; prior independent QA `de13645219e965ae6f519f5665dbcf2de8aa8a59` preserved, not repeated.|
|Objective / supported profile / changes|Bounded D06/D07 graph/child/conflict reference pack from original evidence and static ARM64 decoding. Added fixtures/matrix/validator/reports and appended campaign records. No gameplay implementation.|
|Evidence / confidence|Historical native-integrated E025/E035/E037/E038; native-isolated E004/E009; newly rechecked instruction-backed contracts; explicitly conditional RECONSTRUCTED arithmetic/structures. No new production behavior upgraded to INDEPENDENTLY VERIFIED.|
|Tests|553structural checks,38source checks,5exact historical-control copies,109instruction anchors/1constant/2relocations,4independent f32 boundary calculations,2negative validator controls PASS;0fail/skip. Native/production runtime, graphical, CI and owner tests NOT RUN.|
|Coverage gained / remaining|19bounded source requirements and45fixtures (5historical controls,40proposed). Predicates, graph writes, child loops/recorder guards, two distinct sort contracts and group-history producer identified. Owned multi-child, broader topology/group window and mixed tie outcomes remain NOT VERIFIED.|
|Discrepancies / limitations / blockers|B01multi-child original-owned ledger; B02small graph topology/continuity; B03mixed collected order/native tie permutation; B04nonempty group-window activation. D06/D07 remain OPEN.|
|Updated records / reproduction|w1-02/, this report, appended coverage/dependency/discrepancy/history. Standard-library validate.py command below.|
|Next bounded task / actor / dependencies|Headquarters may separately authorize Work1 W102-P01:reuse E025 owning entry/objects to observe two-child trace versus ordinary parents and per-unit judgment. No experiment or Work2 execution started.|
|Subsystem|**OPEN**|

## Source versions, preparation and method

Remote main matched the assigned start. Production49e7c26, handoff6b84bf3 and
independent QAde13645 are ancestors. The only change from QAde13645 to starting
main is47lines appended to reconstruction history, recording bounded W2-01
acceptance and this authorization. Previously read full standing/history and S01
records remain authoritative; the complete new history addition was reviewed.
Charter/A01/registers, W2 technical handoff, QA-W2-01, original research context/
backlog and relevant E002–004/E009/E010/E025/E028/E029/E035–038 were reused.
Actual Chart/LinkedArc/Arc/ArcTap/Kernel/MixedArcConstruction interfaces and
original arc_tap/linked_arc/mixed_hold_tap/late_input_expiry harnesses were inspected.
No completed W2-01 QA or owner six-group qualification was rerun or relabeled.

The original library was read from the supplied archive **without execution**:
lib/arm64-v8a/libcocos2dcpp.so,29217504bytes,SHA256
`3eaca4e6dabb3395f276f8915698d57675757d0df0970e716b23a3dc201c79be`,
ELF64 little-endian AArch64, GNU Build ID
`17d660edbf37ca78beefc32e07672c97419ddce6` rechecked. VAs are original ELF addresses;
PT_LOAD mapping is used rather than assuming every VA is a file offset.

Source hashes/commits:[sources.json](w1-02/sources.json).
Static excerpts:[instruction-anchors.json](w1-02/instruction-anchors.json).
Capstone5.0.7/pyelftools0.33 were installed nonprivileged solely to decode bytes and
inspect relocations. No original instruction was executed/emulated; no native
harness scenario/import, gameplay heap, fake producer or dynamic patch was used.
The reproducible validator needs only Python's standard library.

## What the original evidence now establishes

### D06 — connections, flags, records and ownership

| Question | Established source contract | Confidence / remaining boundary |
|---|---|---|
|Traversal/adjacency|0x125e514starts j=i+1;0x125e5cccontinues through later main entries after a match. It can append multiple successors.|Instruction-backed general loop; E038 executes one natural pair. No arbitrary graph runtime proof.|
|Time|abs(endA-startB)<=9 at0x125e60c/610, for bounded finite signed-time domain.|Native-integrated delta0; ±9/±10probes are instruction-derived, NOT RUN.|
|X|Float32 FABD0x125e624, promote-to-double0x125e628, compare to double0.1 at0x4184b0;0x125e630rejects >=threshold.|Exact pair observed; boundary arithmetic independently calculated. Decimal0.4/0.6 around0.5f is asymmetric after rounding.|
|Y/modes|Float Y equality; zero-zero or nonzero-nonzero mode class at0x125e634..658.|Instruction-backed. Nonzero does not mean trace1 and special2 have identical gameplay.|
|Curve/color/group|No equality test for these fields in the inspected link-pair loop.|Source absence, not native-integrated proof that all cross-color/group/curve layouts play correctly. Current reconstruction adds same-group/color/curve restrictions.|
|Graph storage|0x1205bf4appends successor;0x125e5c8stores one predecessor pointer at+150. Multiple incoming matches can overwrite it.|Native-integrated one pair; branch/merge prediction instruction-backed. No synthesized predecessor vector.|
|Groups|Predecessor group created/reused; successor receives it only if successor lacks a group. Existing successor group is not unioned by this branch.|Instruction-backed. A merged graph need not have a single symmetric group under this procedure; actual merge identities NOT VERIFIED.|
|Cycles|For unique arc-pointer entries, only forward-index edges are created, so that representation has no self-links/cycles, including equal-time zero-duration members. Pointer uniqueness remains a prerequisite.|Instruction-backed directed-index proof. Not a universal claim about all writers or prepared heaps. No cycle injection experiment proposed.|
|Flags|Factory+a0=0; linked successor+a0=1. Direction mismatch additionally writes+6c=1 at0x125e798.|E038 natural0/1 integrated; changed-direction branch instruction-backed. Broader +6c gameplay effects remain unverified.|
|Generation/folding|Linking then geometry then native flag argument; a qualifying ordinary successor causes at most one tail fold in one generation call, not one fold per outgoing edge.|E038 integrated six records/seven calls; general topology predictions remain conditional.|
|Group history|Second linker pass0x125e860..91cappends linked zero-duration start time into group vector+18/end+20. Acceptance scans predecessor/current/first-successor-chain records and may store recordTime+f32min(2*interval,500) at+14.|Instruction-backed producer/consumer. E038 has empty history/window0 and never enters0x15e015c. Nonempty behavior NOT VERIFIED.|
|Ownership|Group links, shared LogicColor and generated Touch identity are distinct. E038 one contact persists through the junction; UP and later activity reset are separate.|Native-integrated exact pair. E009 prepared overlap/release and E028 two-contact crossing retain their own scope; no universal one-contact-per-note/color rule.|

E038 exact native records remain root[(1250,1),(1500,2)] and
successor[(2001,1),(2251,1),(2501,1),(2751,1)],N7. E009 supplied flag1to both
arcs and obtained N8; it is not overwritten or generalized as natural production.
E038's exclusive activity at2001 also does not erase E009 prepared1/1 observation.
Neither experiment establishes that group machinery is unnecessary.

### D07 — child producer and parent-dependent judgment

The only fully original-owned child profile established here by historical E025
is linear `s`, color0, trace mode1, one interior child1500in parent1000..2000.
E003's six sine equations are native-isolated geometry evidence, not proof of
curved-child construction/gameplay. Other colors, endpoint/outside/unsorted or
simultaneous children and connected-parent combinations remain NOT VERIFIED,
with explicit proposed fixtures. E002's mode2 token/filter is not normal-scope
permission or a reason to silently exclude the applicability question.

Original grammar0xc2cb1c accepts a vector `[arctap(time),...]`, not intrinsically
one child. Builder0x1864d78..0x1864f28loops that parsed vector, invokes
0x173a778per time and constructs the parent after this child loop. The ordinary
branch passes the child vector at0x18653d4..0x1865464 and loops parent backlink
stores at0x186550c/0x1865514. This identifies an ordinary/multiple-child source
path; it does not turn E025's single trace-child execution into multiplicity proof.

The count helper0x11ea120 visits children, has upper-time-bound breaks, and adds
ordinary-mode0record weights after the child count, with input/special guards.
For two interior child products, trace N2 and ordinary N5 are **conditional
RECONSTRUCTED predictions**, not native results. Children need normalization,
ordering, own identity/backlink, geometry and denominator reconciliation together.
No source-derived guarantee of clamping/sorting/outside-time rejection is invented.

Relocation-backed child virtual+20is0xc78814, +38is0x178f5fc. Acceptance writes
consumed+d/contact+10; miss writes missed+c. Both return true for ordinary0/trace1
or absent parent, but return false for parent mode2 after those writes. Recorders
0x17302ec/0x868e98gate their accounting on that return. This virtual return is
**not** the initial classifier return; do not infer that an uncounted special-mode
child allows initial iteration to continue. Special inclusion/normal applicability
remains outside this execution's authorization.

Initial DOWN traverses active enabled arc parents and tests each child with
spatial flag1/width212. Parent body is not appended as a discrete tap. E025 proves
same-child fresh-ID duplicate suppression through consumed guard, not pointer-ID
reuse or time cooldown. MOVE/continuous frames are a separate path. Ordinary
parent body ownership and child classification can therefore interact through the
same retained contact without being the same arbitration operation; that combined
owned runtime ledger remains absent. Linked parents carrying children are likewise
not proven by juxtaposing E025 and E038.

### Mixed candidates — a second sort contract must not be invented

E004 already recovered candidate sorter0xf6b514 with signed start-time key only,
including an isolated31-element equal-key reorder. This disproves a native stable
source-order guarantee. Main sort0x7b6a08 is different:decoded paths compare start,
then end at0x7b6ab8..0x7b6ad4 and helper0x150dbcc..0x150dbe8. Main sort feeds linking/
index insertion; candidate sort feeds initial selection. Their ties cannot be
collapsed into one stable `(time,sourceOrder)` abstraction.

E035/E037 native-integrated observations establish chronological selection and
stops:hold latch unconditionally stops, including1->1; tap/child missed/consumed
false guard continues; true classifier stops, including101–120ms LOST. E035 also
establishes input refresh without FRAME and distinct expiry/input interleavings.
E037 proves retained-contact participation is broader than the first latching
contact. E004/E009 ownership/bypass and E028 are not a universal exclusion across
all note types.

Production currently sorts `OrderBy(Start).ThenBy(SourceOrder)` and rejects
nearby ground/child conflicts within240ms; exact-pair/single-child restrictions
avoid many demanded combinations. These are source-confirmed engineering limits,
not newly observed production failures. A native counterexample to stable sorting
does not supply the exact winner of an unexecuted AFF mixed chart. Need the actual
main/index/active/collected vector, exact sort permutation and stopping pointer.
Porting only the start comparator into a stable managed sort would still add a
native-incompatible guarantee. Existing accepted W2-01 bounded QA remains valid.

## Fixture pack and readiness

[Readable index](w1-02/fixture-index.md), [complete machine matrix](w1-02/fixtures.json),
[19requirement records](w1-02/requirements.json), [source-contract guide](w1-02/README.md).
Every fixture has AFF checksum, requirement/dependency mapping, original evidence,
lexical normalized inventory, prepared-state status, event schedule, established
expectation or explicit NOT VERIFIED, controls, future QA and first missing fact.
Prepared runtime heaps are never fabricated. Conditional structures are separately
graded and never placed into originalObserved.

| Fixture family | Count | Existing native observations reused | New native executions |
|---|---:|---:|---:|
|E038/E025/E035/E037controls|5|5historical control fixtures|0|
|Time/X/Yboundary probes|10|0|0|
|Color/mode/triple/branch/merge/source/same-start/cycle-request/cross-group|9|0|0|
|Child multiplicity/mode/order/time/curve/color/linked parents|10|0|0|
|Equal-time/competing candidates,31size,distinct-time,three-way/retained contacts|11|0|0|
|Total|45|5reused, not rerun|0;40proposals NOT RUN|

READY in the machine matrix means the **named primitive contract** can be
reconstructed from cited evidence. PARTIAL/BLOCKED refers to its integration or
unobserved producer/consumer ledger; no full mechanic/S01row is declared closed.
No need for new experiments to rediscover signed-start comparisons, natural N7,
consumed guards or E037latch stops. Generalized topology/child/tie acceptance does
need the exact missing ledgers or explicit Headquarters disposition of confidence.

## Blockers and bounded proposals — none executed

[Machine proposals](w1-02/proposed-experiments.json) specify owning entry, native
objects, positive case, negative control, input/frame schedule, observations,
PASS/FAIL and stop condition for each.

- **B01/P01, first priority:**original-owned two-child construction/geometry/N and
  child judgment for trace versus ordinary parent. Reuse E025entry/child factory/
  sampler/Director/JNI with at most three scenes; displaced/duplicate/MOVE controls.
  Stop at first missing producer or cleanup before results. This is the precise
  next request; no fake child/vector/denominator is allowed.
- **B02/P02:**E038control plus three-node chain/branch/merge. Original sort/link/
  group/flags/records observed first; only triple continues through two junctions.
  No arbitrary graph/cycle expedition; construction-only branch/merge limits.
- **B03/P03:**native admitted/collected tie vectors and exact size-dependent
  permutation/stop ledger, with distinct-time and fresh/retained-contact controls.
  At most four scenes; input/frame ordering explicit; no Work2 oracle winner.
- **B04/P04:**if demanded, zero-duration linked timestamp producer and conditional
  group-window write/consumer; compare empty-history control. Stop at first missing
  prerequisite; no supplied group vector/window. Newly identified source path
  makes a bounded original experiment possible; it has not been run.

Candidate Work2 execution after P01/P03:coherent ordinary/trace multi-child and
mixed-candidate integration with faithful two-sort/data-order contracts, complete
unit/guard/contact accounting and mixed results/replay. Minimum chart must contain
multiple distinct/simultaneous children and eligible ground/hold conflicts with
independent ledgers; independent exact-production QA and owner qualification of
that new profile follow. Exclude unproven graph/mode2/general group extensions;
retain them in S01. P02/P04 separately gate broader graph integration. This is a
proposal, not authorization. E039widening remains separate and can be authorized
without waiting for unrelated camera/gauge/flick gates.

## Validation, failures, NOT RUN and preservation

Actual final command, from repo root:

```bash
python reconstructed/campaigns/S01-normal-gameplay/w1-02/validate.py \
  --archive ../project_sources/01-arccopy.zip \
  --output reconstructed/campaigns/S01-normal-gameplay/w1-02/results/validation.json
```

[Actual receipt](w1-02/results/validation.json), [environment](w1-02/results/environment.json).
Python3.12, Linux; static tool installation from PyPI HTTPS exited0. Standard-library
validator exits0,0fail/skip:553structural checks,38historical source hashes,5exact
control copies,109instruction byte anchors/1constant/2child relocation targets,
4binary32 boundary computations,2deliberate negative controls detected. These are
evidence-validation checks, not45native gameplay passes. All40proposed scenarios
are NOT RUN/NOT VERIFIED. No new runtime-tested production SHA, C# regression,
ARM64 scenario, graphical/OS input, Windows/audio/hardware, CI or owner test.
No instruction-byte validation claims to prove all semantic interpretations.

Authoring failures preserved:initial control writer duplicated its default timing
line, caught by exact-copy assertion before publication; repaired to copy the
original control exactly. A proposal-generation draft used reserved Python keyword
`pass` as a keyword argument and failed before execution; renamed passCriteria.
Some initial historical-path searches used descriptive rather than actual filenames
and returned missing-file errors; corrected with rg --files. Large reads were
truncated; critical source sections were read in bounded ranges. No native state,
production or historical expectation changed to repair these authoring/read issues.

Ancestry checks, complete changed-path inventory, relative links, fixture/reference
IDs, original source/test/report preservation and exact append-only history are
recorded in [preservation receipt](w1-02/results/preservation.json). Publication is
non-forced main with expected-head guard and immutable remote content readback;
exact published SHA/completed readback supplied in handoff. Original root context/
backlog, excavations/harness, production/tests and both old independent corpora stay
unchanged. The prior reconstruction history is an exact82655-byte prefix.

**Stop here.** No new original-native experiment, Work2 implementation, unrelated
G-series research, applicability exclusion or S01acceptance follows. G006/G007/
G009/G010 remain OPEN/BLOCKED. **Subsystem OPEN.**
