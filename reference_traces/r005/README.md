# R005 timing/audio reference boundary

E005 in full establishes the ordinary steady clock, strict request threshold,
offset sign, no observed ordinary audio-playhead feedback, and backend boundaries.
E040 in full independently joins four native Settings-produced combined offsets
0/80/80/200 to request-entry/pre-compensation and post-anchor states, later E and
aligned judgments. native-offsets.json transcribes those published observations,
not reconstruction outputs. Original research remains unchanged and is not rerun.

R005 consumes an explicit selected user value. The separate regular/alternate80
rows preserve the two native upstream sources; no profile loader, legacy migration,
Bluetooth route detection or preferences persistence is implemented here. Additional
negative offsets and larger overshoots use E005's isolated evidence and declared
integer engineering cases, not a fresh native-owned negative-offset experiment.

Godot is an output substitution: load bundled original PCM, Play(0) at the logical
request and stop/unload on lifecycle boundaries. API Playing, decoded PCM, resource
hashes and headless Dummy-driver output do not prove audibility, latency or physical
synchronization. Playback position is logged in seconds but never fed into E/R/C.
