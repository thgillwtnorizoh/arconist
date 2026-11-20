# W102-P03 — native mixed candidate investigation

2026-11-20. **BLOCKED at Scene A activation: missing host `asin` ABI service.**
No mixed input sorting/stopping result is established. One fresh scene attempted;
three later scenes NOT RUN. No retry or ABI repair/new experiment followed.

## UEP-001 checkpoint

|Field|Result|
|---|---|
|Project / Campaign / Actor / Assignment|Arconist / S01 Normal Gameplay / Work1 Original Research and Independent Verification / W102-P03, issue #10|
|Starting SHA|`69b2b272cff47211091da767840f16a9d56b943b`, matched remote main|
|Exact executed harness SHA|`f595c7e4bce057efa02d3d587900045e7680effe`, published before execution and fetched/selected before native run|
|Published SHA|Final non-forced evidence child; exact final SHA and verified remote readback in handoff / Git history|
|Status|BLOCKED, no native gameplay PASS|
|Objective / profile / changes|Observe four published W1-02 mixed candidate fixtures. External driver, read-only hooks and evidence only; production unchanged.|
|Evidence / confidence|CONFIRMED ORIGINAL for factory returns, child backlink/geometry writes, count helper result and activation exception. Instruction-backed caller/PLT role; mixed collection/order/stopping NOT VERIFIED.|
|Tests|One invocation exit1:0 completed,1blocked,3NOT RUN,0retries. Separate offline receipt audits captured structure/provenance; no native outcome inferred from static tests.|
|Coverage gained / remaining|Partial Scene A construction evidence and exact missing ABI prerequisite; B03 remains OPEN. Eligibility, input order, sort permutation, winners, recorder/health and cleanup unobserved.|
|Discrepancy / limitation|Host service gap, not original rejection or falsified candidate winner. two-retained fixture has no hold, so cannot alone establish hold-latch stopping.|
|Updated records / reproduction|This report; w102-p03/ source, frozen fixture manifest, ledger, failure, command/offline/preservation receipts; appended registers/history.|
|Next bounded task / Actor / dependencies|HQ-authorized Work1 asin ABI recovery and one fresh identical Scene A. Requires correct AArch64 double D0 input/output and numeric/domain controls before native use. No current retry.|
|Subsystem|OPEN|

## Preparation and frozen scope

Remote main matched69b2b27 and descends from f21af7b child recovery and accepted
49e7c26 reconstruction. Read Issue #10's complete execution contract (zero comments),
standing instructions/history and new HQ authorization, S01 registers/charter,
W1-02 proposals/requirements/fixture index and prior P01/C01 source/ledgers.
Reused E004, E025, E035 and E037 producer, projection and stop authorities; old
successful scenes were not rerun. No managed/Work2 output supplies expectations.

Original library SHA256 `3eaca4e6dabb3395f276f8915698d57675757d0df0970e716b23a3dc201c79be`,
Build ID `17d660edbf37ca78beefc32e07672c97419ddce6` checked without creating a VM.
[Preflight](w102-p03/preflight.json) verifies eight original entry/observer anchors.
Static disassembly of the failure caller finds `fcvt/scvtf` and double arithmetic,
`0x17d26c4 bl 0x1a6e300`, returning to17d26c8; the PLT stub loads GOT1b99030.
The runtime import resolver identifies `asin`. Attribution to a particular camera/
renderer product role is NOT VERIFIED and is not needed to preserve the ABI gap.

[Frozen fixture manifest](w102-p03/fixtures.json) preserves all four exact AFF
sources/checksums and typed expectations before execution. Static overlap is only
plausible: AFF lane3 maps to native4; a supplied projection buffer at world
(212.5,0,0) would be within E004's child half-width302 around X0/Y50, with clampY100.
This is not a native eligibility observation. No object geometry would be changed.
`two-retained` contains two simultaneous child times but **no tap/hold**; that fixture
can examine child guards/contact identity, not hold-latch behavior. Its original
bytes were not repaired to fit the proposed role.

## Actual Scene A and first blocker

Executed owning path: original setup/ABI services, ordinary entry ee197c, loading
and initialization/builder, then `activate -> lifecycle.py:34 -> n.tick(dt)`.
Original parsed/factory observations before failure:

|Product|Parsed / prepared observation|
|---|---|
|Tap|raw lane3, start1500; LogicTapNote start/end1500|
|Hold|raw lane3, start1500/end2500; LogicHoldNote same times|
|Arc/child|parsed trace mode1, parent1000–2000, child1500; genuine LogicArcTapNote factory return|
|Backlink / geometry|original stores1865514,1925888,192588c captured|
|Count helper11ea120|native return N5 for this mixed chart, **not** P01's refuted ordinary-parent N5 hypothesis|
|Main sort7b6a08|entry arguments observed, including first three-pointer range; no full permutation inferred|

At scheduler wall2450, the original call into unimplemented import
`0x1a6e300 asin`, LR=`0x17d26c8`, raised RuntimeError. [Original curated ledger and
traceback](w102-p03/native-ledger.json) preserve the failing call chain. No chart,
mode, count, candidate vector, classifier or return value was repaired.

The failure precedes post-activation ownership/index/listener assertions, admission,
input projection and any JNI DOWN. Therefore genuine factory returns do not prove
successful scene activation, simultaneous spatial eligibility or a native winner.
All input candidate/classifier/spatial/recorder/event vectors are empty. No full
cleanup could be qualified. Stop on this original-owning ABI prerequisite; the
remaining budget does not authorize substitutes or a silent repaired rerun.

|Scene|Disposition|
|---|---|
|A all3|1 fresh VM, BLOCKED during activation before input|
|B distinct|NOT RUN|
|C size31|NOT RUN; no31-candidate collection observed|
|D two-retained|NOT RUN|

[Budget](w102-p03/budget.json) reserved1/4 before setup. Repeated scheduler
instruction budgets inside this VM do not represent extra fresh scenes. No old
P01 scene or isolated E004 vector was executed. [Partial normalized evidence](w102-p03/normalized-reference.json)
separates raw/parsed/factory/count from absent active/input observations.
[Sorting disposition](w102-p03/sorting-permutations.json) explicitly contains no
claimed input permutation. [First blocker](w102-p03/first-blocker.json).

## Commands and evidence validation

Linux/Python3.12.14. Isolated setup succeeded:

```bash
python -m pip install --target /tmp/p03-libs -r research_harness/requirements.txt capstone==5.0.7
```

One native invocation from f595c7e:

```bash
PYTHONPATH=/tmp/p03-libs python reconstructed/campaigns/S01-normal-gameplay/w102-p03/run.py --archive ../project_sources/01-arccopy.zip --budget /tmp/p03-budget.json --output /tmp/p03-ledger.json > /tmp/p03-host.log 2>&1
```

Exit1, budget1/4; stop, **do not rerun under this completed assignment**. Remaining
three scenarios were not attempted. [Command receipt](w102-p03/command.json) gives
ledger and external host-log hashes; raw scheduler logs remain outside source.
Unicorn2.1.4/pyelftools0.33 used for native execution; Capstone5.0.7 static only.

The first offline audit failed its own report-link existence check before its receipt
was written. Preparing that receipt path resolved the publication check; no native
expectation, source driver or scene was changed.

Safe independent offline check (no VM/native imports):

```bash
python reconstructed/campaigns/S01-normal-gameplay/w102-p03/audit.py
```

[Offline receipt](w102-p03/audit-receipt.json) reports45 checks PASS,0fail/skip of frozen fixture
identity, Git source, ledger hashes, factory relations/count structure, reserved
budget and absent input phases. PASS here validates the **blocked evidence**, not
gameplay equivalence or a missing scene. Original E004/E035/E037 ledgers remain
independent authority, never replacement goldens for unobserved mixed outcomes.
Production, historical regression, Godot/Windows/GUI/audio, results, P02/P04 and
additional P01 experiments NOT RUN. Static preflight/compilation is not native PASS.

## Preservation, next task and stop

[Preservation verifier/receipt](w102-p03/preservation.json) inventories every changed
path; all protected original/reconstruction/tests/QA/old P01 bytes unchanged and
four record prefixes exact. Source driver/fixture manifest stay frozen at f595c7e.
Non-forced main publication, ancestry and remote exact-byte readback verified in
handoff. No source gameplay change, scope waiver or S01 acceptance.

Recommend **one bounded corrective Work1 task**: implement/validate an isolated
AArch64 `asin(double)` host ABI adapter (D0 in/out, finite positive/negative/zero/
endpoints and out-of-domain behavior, no gameplay semantic replacement), inspect
the saved failure/caller and source composition, then only under fresh HQ budget
run **one identical all3 Scene A** with the same inputs and hooks. Record runtime
argument/return and continue only with valid ownership. Stop after candidate/stop/
cleanup or the next genuine prerequisite. Do not automatically spend B–D budgets.
P03 collection/tie/stop contracts remain blocked until actual native input executes;
no Work2 conflict integration is authorized by partial construction. Other graph,
widening and G006/007/009/010 dependencies remain separate OPEN work. Stop here.
