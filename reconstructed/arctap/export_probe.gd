extends SceneTree
# Non-graphical actual-PCK resource verification. No scene/input/visual qualification.
func _initialize():
    var args = OS.get_cmdline_user_args()
    if args.size() != 2:
        quit(2)
        return
    var expected = JSON.parse_string(FileAccess.get_file_as_string(args[0]))
    var report = {"status":"PASS", "resources":[], "human_qualification":"PENDING"}
    for name in expected:
        var path = "res://content/" + name
        var data = FileAccess.get_file_as_bytes(path)
        var hash = HashingContext.new()
        hash.start(HashingContext.HASH_SHA256)
        hash.update(data)
        var digest = hash.finish().hex_encode()
        var ok = data.size() > 0 and digest == expected[name]
        report.resources.append({"resource":path, "bytes":data.size(), "sha256":digest, "matches":ok})
        if not ok:
            report.status = "FAIL"
    var output = FileAccess.open(args[1],FileAccess.WRITE)
    output.store_string(JSON.stringify(report,"  ")+"\n")
    output.close()
    print("R008_EXPORTED_RESOURCES "+report.status)
    quit(0 if report.status == "PASS" else 1)
