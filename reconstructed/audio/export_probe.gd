extends SceneTree
# Read/decode the ACTUAL exported PCK; no scene, GUI, .NET gameplay or OS input.
func _initialize():
    call_deferred("probe")

func probe():
    var args = OS.get_cmdline_user_args()
    var resource = "res://content/audio/clockwork_steps.wav.bytes"
    var bytes = FileAccess.get_file_as_bytes(resource)
    var hash = HashingContext.new()
    hash.start(HashingContext.HASH_SHA256)
    if not bytes.is_empty():
        hash.update(bytes)
    var digest = hash.finish().hex_encode()
    var manifest = JSON.parse_string(FileAccess.get_file_as_string("res://content/audio/manifest.json"))
    var valid = bytes.size() > 44 and manifest != null and digest == manifest.wav_sha256
    var stream = AudioStreamWAV.load_from_buffer(bytes, {"compress/mode": 0, "edit/normalize": false, "edit/trim": false, "edit/loop_mode": 0}) if valid else null
    valid = valid and stream != null and stream.get_length() == 32.0 and stream.loop_mode == AudioStreamWAV.LOOP_DISABLED
    var player = AudioStreamPlayer.new()
    root.add_child(player)
    player.stream = stream
    if valid:
        player.play(0.0)
        valid = valid and player.playing
    var report = {"status": "PASS" if valid else "FAIL", "source": "actual exported Arconist.pck", "resource": resource, "bytes": bytes.size(), "sha256": digest, "length_seconds": stream.get_length() if stream else 0.0, "backend": AudioServer.get_driver_name(), "api_playing": player.playing, "audibility": "NOT RUN", "hardware_latency": "UNVERIFIED"}
    player.stop()
    player.stream = null
    player.free()
    if args.size() == 1:
        var file = FileAccess.open(args[0], FileAccess.WRITE)
        file.store_string(JSON.stringify(report, "  "))
    print(JSON.stringify(report))
    quit(0 if valid else 1)
