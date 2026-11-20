# W1-02 — original graph, child and conflict reference pack

**Source closure: PARTIAL / BLOCKED for generalized integration.** Evidence pack
validation passes; no native or production runtime comparison was executed here.
Starting source16d17765e6fe50251162a45ffd5d1a64f243acf5; accepted production49e7c26;
prior independent QAde13645 remains unchanged.

Files:

- `requirements.json`:19 bounded requirements mapped to existing S01 IDs/D06/D07,
  confidence, original addresses, implementation readiness and exact unknowns.
- `fixtures.json`:45raw AFF identities/hashes, lexical normalized objects,
  historical or conditional prepared structures, event schedules, expected
  observations, controls, missing facts and future tests.
- `fixtures/`:five unchanged original controls and40proposed charts. **None rerun.**
- `fixture-index.md`:readable fixture crosswalk.
- `instruction-anchors.json`:109curated decoded instruction excerpts, one binary64
  constant and two relocation-backed child virtual targets. These are static source
  anchors, not a trace or a copy of the library.
- `sources.json`:38historical authority/source hashes and exact commit identities.
- `proposed-experiments.json`:four bounded proposals, **NOT AUTHORIZED/NOT RUN**.
  P01is the first recommended request; P02/P03/P04 do not automatically follow it.
- `validate.py`:standard-library structural/provenance/byte validator, never imports
  the native harness, Unicorn or a native library.
- `results/`:actual validation, environment and preservation evidence.

Run from repo root (the archive remains external):

```bash
python reconstructed/campaigns/S01-normal-gameplay/w1-02/validate.py \
  --archive /path/to/arccopy.zip --output /tmp/w1-02-validation.json
```

Without --archive the source/fixture checks run, but archive instruction checks
are explicitly NOT RUN. Validation proves schema, checksums, source identities,
selected instruction bytes/relocation targets and declared f32 arithmetic. It does
**not** execute proposed AFF through the native parser or prove semantic conclusions
by itself. No C# parser is used to determine original support or expected results.

## Original source contracts that can be reused now

1. **Two different sorts.** Main-vector initialization calls0x7b6a08 before
   linkage:decoded paths compare start then end. Initial-input candidates call
   0xf6b514:only signed start is the comparator key. E004's isolated31-element
   case already disproved stable equal-key ordering. Equal-time outcomes are
   deterministic for an exact native vector/algorithm, not randomly selected;
   no universal source/type/nearest priority exists. A stable managed time sort
   would itself introduce a policy. Exact mixed permutations remain NOT VERIFIED.
2. **Link predicate and graph writes.** For finite bounded times/coordinates,
   later vector entry j>i can link if abs(endA-startB)<=9, float32 abs(XB-XA)
   promoted to double is <double0.1, and Y matches by float comparison. Both modes
   must be zero, or both nonzero. Inspected loop does not compare color, curve or
   timing-group ID. Absence of that guard is not integrated gameplay proof.
   It scans all later entries; successor append has no dedup/one-edge break.
   Single predecessor+150 can be overwritten by another matching predecessor.
   Existing successor group is not unioned/reassigned in this branch. Thus the
   native data structure is not an arbitrary symmetric adjacency graph.
3. **No native cycle claim.** With unique arc-pointer entries, this pass creates only forward-index edges,
   proving no self-edge/cycle in that bounded representation. Native pointer
   uniqueness must be observed before applying the proof to a proposed chart. It does not prove all possible writers or
   manually prepared heaps are acyclic. The zero-duration repeated-time probe is
   a proposed rejection of a requested cyclic interpretation, not a fake cycle.
4. **Precision matters.** Predecessor endpoint0.5f versus successor0.4f yields
   float32delta0.09999999403953552 and passes;0.6f yields0.10000002384185791 and
   fails. This is independent arithmetic from decoded FABD/FCVT/FCMP ordering,
   not an original edge observation. Y differs by one float ULP -> unequal.
5. **Flags/folding are different contracts.** Factory flag+a0=0, matched successor
   becomes1. Direction-change branch also writes+6c=1; broad gameplay effect is
   not newly established. Generation follows linking and sampled geometry. Arc
   folding scans for an ordinary successor and folds at most once per generation,
   not once per outgoing edge. E038's natural0/1/N7 and E009's prepared1/1/N8
   remain separate. Each weight unit reaches a recorder/clamp call.
6. **A group history producer is identified.** Second linker pass selects a
   linked zero-duration arc and appends its start time to group+18/end+20. Native
   acceptance scans actual predecessor, own and **first-successor-chain** records;
   conditional0x15e015c stores selected recordTime+f32min(2*interval,500) at+14.
   E038 empty history/window0 never reached that store. Nonempty production and
   consumer behavior are still NOT VERIFIED; do not replace it with an arbitrary
   fixed grace period or assume all successors are scanned by this consumer.
7. **Children are not trace-only in the inspected constructor path.** Parser
   grammar contains a timestamp vector. Builder copies/loops it and calls child
   factory per time before parent-mode selection; ordinary parent path receives
   that vector and writes each backlink. Ordinary0/trace1 child acceptance and
   miss methods set their own flags and return true; parent mode2 returns false
   after flag writes, suppressing recorder accounting through caller gates. This
   does not authorize special-mode inclusion/account/content work.
8. **Count and child normalization must agree.** Native count traverses children,
   then adds record weights only for ordinary mode0 (with input/special guards).
   Its child loop can stop at an upper-time bound, so child ordering is functional.
   Exact unsorted/outside-parent/endpoints/simultaneous multiplicity outcomes are
   not established by seeing a vector loop. No sorting/default/clamping rule is
   invented for those fixtures.
9. **Discrete versus continuous.** Initial DOWN collects child pointers through
   enabled active parents using spatial flag1/width212; body arcs are not discrete
   tap candidates. Hold latch stops unconditionally; a tap/child false guard
   continues, while true includes consuming LOST. MOVE/retained processing is
   separate. E037 proves a contact that originally hit a tap can sustain a later
   latched hold. Color claims/generated IDs and crossing bypass are separate.

## Bounded facts versus integration unknowns

Historical original controls are E025one trace child, E038one natural constant pair,
E035two tap interleavings and E037hold-first/tap-first. Their actual observations
are copied only into those unchanged control fixtures. Predictions such as triple
N11 or ordinary-two-child N5 are explicitly conditional RECONSTRUCTED values from
instructions, not new native results or Work2 outputs. Proposed fixtures have no
originalObserved result and no runtime PASS classification.

First prerequisite B01:original-owned two-child construction/count/geometry and
per-child judgment for trace/ordinary parents. P01proposes exactly that positive/
mode-contrast/duplicate/negative-spatial experiment. B02is actual small graph
links/groups/flags/records plus triple continuity (P02). B03is actual mixed collected
order/native tie permutation/stopping ledger (P03). B04is nonempty group history/
window production and effect (P04only if demanded). There is no need to repeat
solved generic tap/hold/crossing research or the completed W2-01 QA.

Until separately authorized observation closes the needed integration gates,
Headquarters can authorize faithful primitive ports with the stated confidence,
but cannot call arbitrary graphs/multi-child conflicts native-integrated. Current
production's source-order tie key, exact-pair restrictions and240ms ground/child
rejection remain explicit engineering limits. S01 remains OPEN.
