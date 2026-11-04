using System.Globalization;
using System.Text.RegularExpressions;

namespace Arconist.Core;

public sealed class Tap
{
    public int Ordinal { get; }
    public int Time { get; }
    public int RawLane { get; }
    public int Lane => RawLane + 1;
    public string Id => $"tap:{Ordinal}:{Time}:{Lane}";
    public float NormalizedX => 0.5f * (Lane - 2);
    internal Tap(int ordinal, int time, int rawLane) { Ordinal = ordinal; Time = time; RawLane = rawLane; }
}

public sealed class Timing
{
    public int Time { get; }
    public float Bpm { get; }
    public float Beats { get; }
    internal Timing(int time, float bpm, float beats) { Time = time; Bpm = bpm; Beats = beats; }
}

public sealed class Chart
{
    public IReadOnlyList<Tap> Taps { get; }
    public IReadOnlyList<Timing> Timings { get; }
    public int AudioOffset { get; }
    public float Density { get; }
    public int JudgmentUnits => Taps.Count;
    public int EndTime { get; }
    private Chart(List<Tap> taps, List<Timing> timings, int offset, float density)
    {
        Taps = taps.AsReadOnly(); Timings = timings.AsReadOnly(); AudioOffset = offset;
        Density = density; EndTime = checked(taps.Max(t => t.Time) + 120);
    }

    // Deliberately bounded grammar: no silent omission of unsupported AFF constructs.
    public static Chart Parse(string text)
    {
        text = text.Replace("\r\n", "\n");
        int separator = text.IndexOf("\n-\n", StringComparison.Ordinal);
        if (separator < 0) throw new FormatException("AFF requires a newline-hyphen-newline separator.");
        int offset = 0; float density = 1;
        foreach (var line in text.Substring(0, separator).Split('\n'))
        {
            if (string.IsNullOrWhiteSpace(line)) continue;
            var pair = line.Split(new[] { ':' }, 2);
            if (pair.Length != 2) throw new FormatException("Malformed AFF header.");
            switch (pair[0].Trim())
            {
                case "AudioOffset": offset = pair[1].Trim().Length == 0 ? 0 : int.Parse(pair[1], CultureInfo.InvariantCulture); break;
                case "TimingPointDensityFactor": density = pair[1].Trim().Length == 0 ? 1 : float.Parse(pair[1], CultureInfo.InvariantCulture); break;
                default: throw new NotSupportedException($"Unsupported AFF header: {pair[0]}");
            }
        }
        if (!float.IsFinite(density) || density <= 0) throw new FormatException("Density must be positive and finite.");
        var taps = new List<Tap>(); var timings = new List<Timing>();
        string body = text.Substring(separator + 3);
        const string number = @"[0-9]+\.[0-9]+";
        var tapPattern = new Regex(@"^\(\s*([0-9]+)\s*,\s*([0-9]+)\s*\)$", RegexOptions.CultureInvariant);
        var timingPattern = new Regex(@"^timing\(\s*([0-9]+)\s*,\s*(" + number + @")\s*,\s*(" + number + @")\s*\)$", RegexOptions.CultureInvariant);
        var statements = body.Split(';');
        if (!string.IsNullOrWhiteSpace(statements[statements.Length - 1])) throw new FormatException("AFF statement requires semicolon.");
        for (int i = 0; i < statements.Length - 1; i++)
        {
            string s = statements[i].Trim();
            var tap = tapPattern.Match(s);
            if (tap.Success)
            {
                int time = int.Parse(tap.Groups[1].Value, CultureInfo.InvariantCulture);
                int raw = int.Parse(tap.Groups[2].Value, CultureInfo.InvariantCulture);
                if (raw > 5) throw new NotSupportedException("Supported raw integer lanes are 0..5.");
                if (time > int.MaxValue - 1000000) throw new NotSupportedException("Timestamp outside supported arithmetic domain.");
                taps.Add(new Tap(taps.Count, time, raw)); continue;
            }
            var timing = timingPattern.Match(s);
            if (!timing.Success) throw new NotSupportedException($"Unsupported AFF statement: {s}");
            int at = int.Parse(timing.Groups[1].Value, CultureInfo.InvariantCulture);
            float bpm = float.Parse(timing.Groups[2].Value, CultureInfo.InvariantCulture);
            float beats = float.Parse(timing.Groups[3].Value, CultureInfo.InvariantCulture);
            if (!float.IsFinite(bpm) || !float.IsFinite(beats) || bpm <= 0 || beats <= 0)
                throw new NotSupportedException("Only finite positive ordinary timing is supported.");
            timings.Add(new Timing(at, bpm, beats));
        }
        if (taps.Count == 0 || timings.Count == 0) throw new FormatException("At least one timing and one tap required.");
        timings.Sort((a, b) => a.Time.CompareTo(b.Time));
        if (timings[0].Time != 0 || timings.Select(t => t.Time).Distinct().Count() != timings.Count)
            throw new NotSupportedException("Timing must start at zero, with distinct timing times.");
        taps.Sort((a, b) => { int c = a.Time.CompareTo(b.Time); return c != 0 ? c : a.Ordinal.CompareTo(b.Ordinal); });
        return new Chart(taps, timings, offset, density);
    }
}
