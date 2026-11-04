using System.Text.Json;
using System.Text.Json.Nodes;
using System.Globalization;
using Arconist.Core;

namespace Arconist.Headless;

public static class Replay
{
    public static readonly JsonSerializerOptions JsonOptions = new() { WriteIndented = true, PropertyNamingPolicy = JsonNamingPolicy.CamelCase };
    public static JsonObject Run(string aff, JsonObject schedule)
    {
        var chart = Chart.Parse(aff);
        var kernel = new Kernel(chart, schedule["epochMs"]?.GetValue<long>() ?? 0,
            schedule["userOffset"]?.GetValue<int>() ?? 0,
            schedule["requestedSpeed"]?.GetValue<float>() ?? 4,
            schedule["baseBpm"]?.GetValue<int>() ?? 178);
        var events = schedule["events"]?.AsArray() ?? throw new FormatException("Missing events array.");
        if (events.Count == 0) throw new FormatException("Empty event schedule.");
        var trace = new JsonArray(); long lastWall = schedule["epochMs"]?.GetValue<long>() ?? 0;
        foreach (var item in events)
        {
            var ev = item?.AsObject() ?? throw new FormatException("Event must be object.");
            long wall = ev["wallMs"]?.GetValue<long>() ?? throw new FormatException("Event requires wallMs.");
            if (wall < lastWall) throw new FormatException($"Event {trace.Count}: wall time went backwards.");
            lastWall = wall;
            string kind = ev["kind"]?.GetValue<string>() ?? throw new FormatException("Event requires kind.");
            switch (kind)
            {
                case "FRAME": kernel.Frame(wall); break;
                case "DOWN": kernel.Down(wall, RequiredInt(ev, "pointer"), RequiredInt(ev, "lane")); break;
                case "UP": kernel.Up(RequiredInt(ev, "pointer")); break;
                default: throw new FormatException($"Unknown event kind {kind}.");
            }
            // Materialize each snapshot; later mutations never alter earlier events.
            trace.Add(JsonSerializer.SerializeToNode(new
            {
                index = trace.Count, kind, wallMs = wall, effectiveTime = kernel.Timeline.EffectiveTime,
                lastFrameTime = kernel.LastFrameTime, musicStarted = kernel.Timeline.MusicStarted,
                rawTime = kernel.Timeline.RawTime, compensation = kernel.Timeline.Compensation,
                candidates = kernel.Candidates, classifications = kernel.Classifications, expired = kernel.Expired,
                notes = kernel.Notes.Select(n => new { id = n.Data.Id, active = n.Active, missed = n.Missed,
                    consumed = n.Consumed, contact = n.Contact, depth = n.Depth }),
                pure = kernel.Pure, far = kernel.Far, lost = kernel.Lost, shining = kernel.Shining,
                combo = kernel.Combo, maxCombo = kernel.MaxCombo, score = kernel.Score,
                health = (double)kernel.Health, healthBits = BitConverter.SingleToInt32Bits(kernel.Health),
                early = kernel.Early, late = kernel.Late, contacts = kernel.ContactCount,
                finished = kernel.Finished, result = kernel.Result
            }, JsonOptions));
        }
        return JsonSerializer.SerializeToNode(new
        {
            schema = "arconist-r001-v1", status = "computed",
            chart = new { judgmentUnits = chart.JudgmentUnits, endTime = chart.EndTime,
                audioOffset = chart.AudioOffset, density = chart.Density,
                taps = chart.Taps.Select(t => new { id = t.Id, time = t.Time, endTime = t.Time,
                    rawLane = t.RawLane, lane = t.Lane, normalizedX = t.NormalizedX }),
                effectiveSpeed = kernel.EffectiveSpeed, baseGain = (double)kernel.BaseGain },
            trace, result = kernel.Result
        }, JsonOptions)!.AsObject();
    }
    private static int RequiredInt(JsonObject o, string key) => o[key]?.GetValue<int>() ?? throw new FormatException($"Missing {key}.");

    // Native references are partial observations, not invented full emulator traces.
    // Object keys project only fields actually established by the cited source.
    // Arrays always compare exact length/order, numbers compare exact value.
    public static string? FirstDifference(JsonNode? expected, JsonNode? actual, string path = "$")
    {
        if (expected is JsonObject obj)
        {
            if (actual is not JsonObject observed) return $"{path}: expected object, got {actual}";
            foreach (var pair in obj)
            {
                if (!observed.ContainsKey(pair.Key)) return $"{path}.{pair.Key}: missing field";
                var diff = FirstDifference(pair.Value, observed[pair.Key], path + "." + pair.Key);
                if (diff != null) return diff;
            }
            return null;
        }
        if (expected is JsonArray arr)
        {
            if (actual is not JsonArray observed) return $"{path}: expected array";
            if (arr.Count != observed.Count) return $"{path}.length: expected {arr.Count}, actual {observed.Count}";
            for (int i = 0; i < arr.Count; i++)
            { var diff = FirstDifference(arr[i], observed[i], $"{path}[{i}]"); if (diff != null) return diff; }
            return null;
        }
        if (expected is JsonValue e && actual is JsonValue a &&
            e.GetValueKind() == JsonValueKind.Number && a.GetValueKind() == JsonValueKind.Number)
        {
            if (double.Parse(e.ToJsonString(), CultureInfo.InvariantCulture) ==
                double.Parse(a.ToJsonString(), CultureInfo.InvariantCulture)) return null;
        }
        else if (JsonNode.DeepEquals(expected, actual)) return null;
        return $"{path}: expected {expected?.ToJsonString() ?? "null"}, actual {actual?.ToJsonString() ?? "null"}";
    }

    public static string? Validate(JsonObject reference, JsonObject actual)
    {
        var diff = FirstDifference(reference["chart"], actual["chart"], "$.chart");
        if (diff != null) return diff;
        // Checkpoints must be declared in chronological event order.
        foreach (var item in reference["checkpoints"]!.AsArray())
        {
            int index = item!["event"]!.GetValue<int>();
            var trace = actual["trace"]!.AsArray();
            if (index < 0 || index >= trace.Count) return $"$.trace[{index}]: missing event";
            diff = FirstDifference(item["state"], trace[index], $"$.trace[{index}]");
            if (diff != null) return diff;
        }
        return FirstDifference(reference["result"], actual["result"], "$.result");
    }
}

public static class Program
{
    public static int Main(string[] args)
    {
        try
        {
            if (args.Length != 3 && args.Length != 5)
                throw new ArgumentException("Usage: Arconist.Headless CHART.aff SCHEDULE.json OUTPUT.json [--reference REFERENCE.json]");
            if (args.Length == 5 && args[3] != "--reference") throw new ArgumentException("Expected --reference.");
            var report = Replay.Run(File.ReadAllText(args[0]), JsonNode.Parse(File.ReadAllText(args[1]))!.AsObject());
            string? difference = args.Length == 5 ? Replay.Validate(JsonNode.Parse(File.ReadAllText(args[4]))!.AsObject(), report) : null;
            if (args.Length == 5) report["validation"] = new JsonObject { ["status"] = difference == null ? "pass" : "fail", ["firstDifference"] = difference };
            File.WriteAllText(args[2], report.ToJsonString(Replay.JsonOptions) + Environment.NewLine);
            if (difference != null) { Console.Error.WriteLine(difference); return 1; }
            Console.WriteLine($"Computed {report["trace"]!.AsArray().Count} events; validation {(args.Length == 5 ? "pass" : "not requested")}; output {Path.GetFullPath(args[2])}");
            return 0;
        }
        catch (Exception ex) { Console.Error.WriteLine($"{ex.GetType().Name}: {ex.Message}"); return 1; }
    }
}
