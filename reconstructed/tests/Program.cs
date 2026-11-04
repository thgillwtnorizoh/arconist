using System.Text.Json.Nodes;
using Arconist.Core;
using Arconist.Headless;

static class Tests
{
    static int count, failures;
    static string root = "";
    static void Check(bool ok, string message) { if (!ok) throw new Exception(message); }
    static void Test(string name, Action test)
    {
        count++;
        try { test(); Console.WriteLine($"PASS {name}"); }
        catch (Exception e) { failures++; Console.WriteLine($"FAIL {name}: {e.Message}"); }
    }
    static void Throws(Action action)
    { bool threw = false; try { action(); } catch { threw = true; } Check(threw, "Expected exception"); }
    static JsonObject Read(string path) => JsonNode.Parse(File.ReadAllText(Path.Combine(root, path)))!.AsObject();
    static string Aff => File.ReadAllText(Path.Combine(root, "research_harness/fixtures/ordinary_two_tap.aff"));
    static string Single => "AudioOffset:0\n-\ntiming(0,120.00,4.00);(1000,3);";
    static JsonObject Schedule(string name) => Read($"reference_traces/r001/{name}.schedule.json");
    static JsonObject Run(string name) => Replay.Run(name == "ordinary" ? Aff : File.ReadAllText(Path.Combine(root, "research_harness/fixtures/native_late_input_expiry.aff")), Schedule(name));
    static Kernel Started(string? aff = null)
    { var k = new Kernel(Chart.Parse(aff ?? Single)); k.Frame(1); k.Frame(3002); return k; }
    public static int Main(string[] args)
    {
        if (args.Length != 1) { Console.Error.WriteLine("Usage: Arconist.Tests REPOSITORY_ROOT"); return 1; }
        root = Path.GetFullPath(args[0]);
        foreach (string name in new[] { "ordinary", "input-first", "frame-first" })
        {
            Test($"native reference {name}", () => {
                var diff = Replay.Validate(Read($"reference_traces/r001/{name}.reference.json"), Run(name));
                Check(diff == null, diff ?? "");
            });
            Test($"deterministic replay {name} x100", () => {
                string first = Run(name).ToJsonString();
                for (int i = 0; i < 100; i++) Check(first == Run(name).ToJsonString(), $"Replay {i} diverged");
            });
        }
        Test("parser LF/CRLF, whitespace, typed lanes and dynamic end", () => {
            var c = Chart.Parse("AudioOffset:120\r\nTimingPointDensityFactor:2.0\r\n-\r\n timing(0,120.00,4.00); (700,1);\n(1800,4);\n");
            Check(c.AudioOffset == 120 && c.Density == 2 && c.JudgmentUnits == 2 && c.EndTime == 1920, "Header/count/end");
            Check(c.Taps[0].Lane == 2 && c.Taps[1].Lane == 5, "Raw lane conversion");
        });
        Test("parser rejects unsupported types and malformed AFF", () => {
            foreach (string bad in new[] { "hold(1,2,3);", "(1000,3.0);", "(1000,6);", "timinggroup(){(1000,3);};", "(1000,3)", "timing(0,120,4);" })
                Throws(() => Chart.Parse("AudioOffset:0\n-\ntiming(0,120.00,4.00);" + bad));
            Throws(() => Chart.Parse("(1000,3);"));
        });
        // 002: both signs at each recovered comparison boundary, with no intervening expiry frame.
        foreach (int delta in new[] { -121,-120,-101,-100,-51,-50,-26,-25,0,25,26,50,51,100,101,120,121 })
        {
            int d = delta;
            Test($"classifier delta {d}", () => {
                var k = Started(); k.Down(4002 + d, 42, 4);
                int abs = Math.Abs(d);
                string expected = abs > 120 ? "outside_window" : abs > 100 ? "LOST" : abs > 50 ? "FAR" : abs > 25 ? "PURE" : "SHINING_PURE";
                Check(k.Classifications.Single().Outcome == expected, $"Expected {expected}");
                Check(k.Lost == (abs is > 100 and <= 120 ? 1 : 0), "Recorded miss");
                Check(k.Notes[0].Consumed == (abs <= 100), "Successful-hit guard");
                Check(k.Notes[0].Missed == (abs is > 100 and <= 120), "Missed guard");
                Check(k.Combo == (abs <= 100 ? 1 : 0), "Combo");
            });
        }
        Test("strict expiry equality and one miss only", () => {
            var k = Started(); k.Frame(4102); Check(k.Lost == 0, "E1100 must not expire");
            k.Frame(4103); Check(k.Lost == 1 && k.Notes[0].Active, "E1101 miss occurs after range pass");
            k.Frame(4103); Check(k.Lost == 1 && !k.Notes[0].Active, "Next frame cleanup, no duplicate");
        });
        Test("strict completion equality and cached result", () => {
            var k = Started(); k.Down(4002, 1, 4); k.Up(1);
            k.Frame(4122); Check(!k.Finished && k.Result == null, "E1120 unfinished");
            k.Frame(4123); var result = k.Result; Check(k.Finished && result != null, "E1121 finished");
            k.Frame(4124); Check(ReferenceEquals(result, k.Result) && k.Pure == 1, "Result cache/duplicate guard");
        });
        Test("consumed candidate guard and UP do not score", () => {
            var k = Started(); k.Frame(4002); k.Down(4002, 1, 4); int score = k.Score;
            k.Down(4002, 2, 4); Check(k.Classifications.Single().Outcome == "guard_consumed", "Duplicate guard");
            Check(k.Pure == 1 && k.Score == score && k.ContactCount == 2, "Duplicate scored");
            k.Up(1); k.Up(2); Check(k.ContactCount == 0 && k.Score == score, "UP cleanup");
        });
        Test("chronological candidates beat nearest timing error", () => {
            var k = Started("AudioOffset:0\n-\ntiming(0,120.00,4.00);(1109,3);(1000,3);");
            k.Frame(4002); k.Down(4053, 1, 4);
            Check(k.Candidates[0] == "tap:1:1000:4" && k.Far == 1 && k.Notes[0].Consumed, "Earlier FAR must consume");
        });
        Test("outside-window candidate continues to later note", () => {
            var k = Started("AudioOffset:0\n-\ntiming(0,120.00,4.00);(1000,3);(1121,3);");
            k.Down(4123, 1, 4); Check(k.Classifications.Count == 2 && k.Pure == 1 && k.Lost == 0, "Outside120 skip");
        });
        Test("lane eligibility", () => {
            var k = Started(); k.Down(4002, 1, 3); Check(k.Candidates.Count == 0 && k.Pure == 0, "Wrong lane judged");
        });
        Test("timeline startup equality, offsets and independent touch timestamp", () => {
            var k = new Kernel(Chart.Parse(Single.Replace("AudioOffset:0", "AudioOffset:120")), userOffset:30);
            k.Frame(2849); Check(!k.Timeline.MusicStarted && k.Timeline.EffectiveTime == -151, "Before startup");
            k.Frame(2850); Check(!k.Timeline.MusicStarted && k.Timeline.EffectiveTime == -150, "Equality startup");
            k.Frame(2851); Check(k.Timeline.MusicStarted && k.Timeline.EffectiveTime == -150, "Crossing anchor");
            k.Down(4001, 1, 4); Check(k.Pure == 1, "Offset alignment");
            var s = Schedule("ordinary"); s["events"]![3]!["timestampMs"] = long.MaxValue;
            Check(JsonNode.DeepEquals(Replay.Run(Aff, s), Run("ordinary")), "Touch timestamp changed judgment");
        });
        Test("never-admitted old tap versus retained expiry", () => {
            var warm = Started(); warm.Frame(5002); Check(warm.Lost == 1, "Retained old note must expire");
            // 009 prepared speed6 threshold: at E1025 current depth300 rejects new admission.
            var k = new Kernel(Chart.Parse(Single), requestedSpeed:4, baseBpm:120);
            k.Timeline.Update(3002); k.Frame(4027);
            Check(!k.Notes[0].Active && k.Lost == 0, "New admission threshold must be strict <300");
            k.Frame(5002); Check(k.Lost == 0 && k.Result!.RecordedLost == 0 && k.Result.Lost == 1, "Reconciliation is not retroactive gauge damage");
        });
        Test("negative schedules and invalid contact lifecycle fail", () => {
            var s = Schedule("ordinary"); s["events"]![2]!["wallMs"] = 0; Throws(() => Replay.Run(Aff, s));
            var k = Started(); k.Down(4002, 1, 4); Throws(() => k.Down(4002, 1, 4)); k.Up(1); Throws(() => k.Up(1));
        });
        Test("comparator catches first divergent intermediate despite correct final", () => {
            var actual = Run("ordinary"); actual["trace"]![3]!["combo"] = 99;
            string? diff = Replay.Validate(Read("reference_traces/r001/ordinary.reference.json"), actual);
            Check(diff != null && diff.StartsWith("$.trace[3].combo:"), "First event/field diagnostic: " + diff);
            actual = Run("frame-first"); actual["trace"]![4]!["candidates"]!.AsArray().RemoveAt(0);
            diff = Replay.Validate(Read("reference_traces/r001/frame-first.reference.json"), actual);
            Check(diff != null && diff.Contains("$.trace[4].candidates.length"), "Candidate length diagnostic");
        });
        Test("integer score arithmetic matches published mixed-count examples", () => {
            Check(Kernel.CalculateScore(2,1,2,6) == 4166668, "042 prefix score");
            Check(Kernel.CalculateScore(4,1,4,6) == 7500004, "042 recovery score");
        });
        Console.WriteLine($"Tests: {count}; passed: {count-failures}; failed: {failures}; skipped: 0");
        return failures == 0 ? 0 : 1;
    }
}
