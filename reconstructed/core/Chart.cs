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
    public int SourceOrder { get; }
    internal Tap(int ordinal, int time, int rawLane, int sourceOrder) { Ordinal = ordinal; Time = time; RawLane = rawLane; SourceOrder = sourceOrder; }
}

public sealed class Hold
{
    public int Ordinal { get; }
    public int SourceOrder { get; }
    public int Start { get; }
    public int End { get; }
    public int RawLane { get; }
    public int Lane => RawLane + 1;
    public float Interval { get; }
    public IReadOnlyList<int> Checkpoints { get; }
    public string Id => $"hold:{Ordinal}:{Start}:{End}:{Lane}";
    internal Hold(int ordinal, int sourceOrder, int start, int end, int rawLane, float bpm, float density)
    {
        Ordinal = ordinal; SourceOrder = sourceOrder; Start = start; End = end; RawLane = rawLane;
        // E001/010: literal f32 stages; ordinary generation flag0, no head/tail.
        float beat = 60000f / bpm;
        float divided = beat / (bpm >= 255f ? 1f : 2f);
        Interval = divided / density;
        if (!float.IsFinite(Interval) || Interval < 1 || Interval > int.MaxValue / 4f)
            throw new NotSupportedException("Hold interval outside supported finite >=1ms domain.");
        float quotient = (float)(end - start) / Interval;
        if (quotient > 100000) throw new NotSupportedException("Hold exceeds 100000 checkpoint generation steps.");
        int limit = (int)quotient;
        var records = new List<int>();
        for (int i = 1; i < limit; i++)
        {
            float step = Interval * (float)i;
            int time = (int)((float)start + step);
            if (time < end) records.Add(time);
        }
        if (records.Count == 0) records.Add((int)((float)start + (float)(end - start) * 0.5f));
        if (records.Any(t => t <= start || t >= end) || records.Distinct().Count() != records.Count)
            throw new NotSupportedException("Hold checkpoints must remain distinct interior integer timestamps.");
        Checkpoints = records.AsReadOnly();
    }
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
    public IReadOnlyList<Hold> Holds { get; }
    public IReadOnlyList<Arc> Arcs { get; }
    public int AudioOffset { get; }
    public float Density { get; }
    public int JudgmentUnits { get; }
    public int EndTime { get; }
    private Chart(List<Tap> taps, List<Hold> holds, List<Arc> arcs, List<Timing> timings, int offset, float density)
    {
        Taps = taps.AsReadOnly(); Timings = timings.AsReadOnly(); AudioOffset = offset;
        Density = density; Holds = holds.AsReadOnly(); Arcs=arcs.AsReadOnly();
        JudgmentUnits = checked(taps.Count + holds.Sum(h => h.Checkpoints.Count)+arcs.Sum(a=>a.Checkpoints.Count));
        EndTime = Math.Max(taps.Count == 0 ? 0 : checked(taps.Max(t => t.Time) + 120),
                           holds.Count == 0 ? 0 : checked(holds.Max(h => h.End) + 500));
        EndTime=Math.Max(EndTime,arcs.Count==0?0:checked(arcs.Max(a=>a.End)+500));
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
        var parsedHolds = new List<(int start, int end, int raw, int order)>();
        var parsedArcs=new List<(string[] fields,int order)>();
        int sourceOrder = 0;
        string body = text.Substring(separator + 3);
        const string number = @"[0-9]+\.[0-9]+";
        var tapPattern = new Regex(@"^\(\s*([0-9]+)\s*,\s*([0-9]+)\s*\)$", RegexOptions.CultureInvariant);
        var holdPattern = new Regex(@"^hold\(\s*([0-9]+)\s*,\s*([0-9]+)\s*,\s*([0-9]+)\s*\)$", RegexOptions.CultureInvariant);
        var timingPattern = new Regex(@"^timing\(\s*([0-9]+)\s*,\s*(" + number + @")\s*,\s*(" + number + @")\s*\)$", RegexOptions.CultureInvariant);
        var statements = body.Split(';');
        if (!string.IsNullOrWhiteSpace(statements[statements.Length - 1])) throw new FormatException("AFF statement requires semicolon.");
        for (int i = 0; i < statements.Length - 1; i++)
        {
            string s = statements[i].Trim();
            if(s.StartsWith("arc(",StringComparison.Ordinal))
            {
                if(!s.EndsWith(")",StringComparison.Ordinal))throw new NotSupportedException("Attached arc-taps unsupported.");
                var fields=s.Substring(4,s.Length-5).Split(',').Select(f=>f.Trim()).ToArray();
                if(fields.Length!=10&&fields.Length!=11)throw new NotSupportedException("Unsupported arc field count.");
                if(fields[4]!="s"||fields[8]!="none"||fields[9]!="false")throw new NotSupportedException("Only ordinary linear none-effect arcs supported.");
                foreach(int f in new[]{0,1,7})if(!Regex.IsMatch(fields[f],@"^[0-9]+$"))throw new NotSupportedException("Arc integer syntax required.");
                foreach(int f in new[]{2,3,5,6}.Concat(fields.Length==11?new[]{10}:Array.Empty<int>()))if(!Regex.IsMatch(fields[f],@"^[0-9]+\.[0-9]+$"))throw new NotSupportedException("Arc decimal syntax required.");
                parsedArcs.Add((fields,sourceOrder++));continue;
            }
            var tap = tapPattern.Match(s);
            if (tap.Success)
            {
                int time = int.Parse(tap.Groups[1].Value, CultureInfo.InvariantCulture);
                int raw = int.Parse(tap.Groups[2].Value, CultureInfo.InvariantCulture);
                if (raw > 5) throw new NotSupportedException("Supported raw integer lanes are 0..5.");
                if (time > int.MaxValue - 1000000) throw new NotSupportedException("Timestamp outside supported arithmetic domain.");
                taps.Add(new Tap(taps.Count, time, raw, sourceOrder++)); continue;
            }
            var hold = holdPattern.Match(s);
            if (hold.Success)
            {
                int start = int.Parse(hold.Groups[1].Value, CultureInfo.InvariantCulture);
                int end = int.Parse(hold.Groups[2].Value, CultureInfo.InvariantCulture);
                int raw = int.Parse(hold.Groups[3].Value, CultureInfo.InvariantCulture);
                // Preserve R001's rejection of its 1ms unsupported hold specimen.
                // R004 supports >=2ms, with finite distinct interior checkpoint times.
                if (end <= start || (long)end - start < 2 || end > int.MaxValue - 1000000 || raw < 1 || raw > 4)
                    throw new NotSupportedException("Holds require duration >=2ms and raw integer lanes 1..4 within the timestamp domain.");
                parsedHolds.Add((start, end, raw, sourceOrder++)); continue;
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
        if ((taps.Count == 0 && parsedHolds.Count == 0 && parsedArcs.Count==0) || timings.Count == 0) throw new FormatException("At least one timing and one supported note required.");
        timings.Sort((a, b) => a.Time.CompareTo(b.Time));
        if (timings[0].Time != 0 || timings.Select(t => t.Time).Distinct().Count() != timings.Count)
            throw new NotSupportedException("Timing must start at zero, with distinct timing times.");
        taps.Sort((a, b) => { int c = a.Time.CompareTo(b.Time); return c != 0 ? c : a.Ordinal.CompareTo(b.Ordinal); });
        var holds = parsedHolds.Select((h, i) => new Hold(i, h.order, h.start, h.end, h.raw,
            timings.Last(t => t.Time <= h.start).Bpm, density)).OrderBy(h => h.Start).ThenBy(h => h.SourceOrder).ToList();
        var arcs=parsedArcs.Select((a,i)=>{
            var f=a.fields;int start=int.Parse(f[0],CultureInfo.InvariantCulture),end=int.Parse(f[1],CultureInfo.InvariantCulture),color=int.Parse(f[7],CultureInfo.InvariantCulture);
            float V(int k)=>float.Parse(f[k],CultureInfo.InvariantCulture);
            float x0=V(2),x1=V(3),y0=V(5),y1=V(6),extra=f.Length==11?V(10):1;
            if(start<0||(long)end-start<2||(long)end-start>600000||end>int.MaxValue-1000000||color>1||!float.IsFinite(extra)||extra<0||extra>4||new[]{x0,x1,y0,y1}.Any(v=>!float.IsFinite(v)||v<0||v>1))throw new NotSupportedException("Arc outside bounded R007 domain.");
            if(timings.Any(t=>t.Time>start&&t.Time<end))throw new NotSupportedException("Timing changes inside an arc deferred.");
            return new Arc(i,a.order,start,end,x0,x1,y0,y1,color,extra,timings.Last(t=>t.Time<=start),density);
        }).OrderBy(a=>a.Start).ThenBy(a=>a.SourceOrder).ToList();
        for(int i=1;i<arcs.Count;i++)if((long)arcs[i].Start<arcs[i-1].End+1000L)throw new NotSupportedException("Overlapping/crossing/linked or closely adjacent arcs deferred.");
        return new Chart(taps, holds, arcs, timings, offset, density);
    }
}
