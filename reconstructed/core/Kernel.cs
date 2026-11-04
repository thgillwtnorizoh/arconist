namespace Arconist.Core;

public sealed class Timeline
{
    private readonly long origin;
    private readonly int offset;
    private long lastWall;
    public int RawTime { get; private set; }
    public int Compensation { get; private set; }
    public int EffectiveTime => unchecked(RawTime - Compensation);
    public bool MusicStarted { get; private set; }
    public Timeline(long originMs, int chartOffset, int userOffset)
    {
        origin = lastWall = originMs; offset = checked(chartOffset + userOffset);
        RawTime = -3000;
    }
    public void Update(long wallMs)
    {
        if (wallMs < lastWall) throw new ArgumentException("Wall time must be monotonic; array order resolves equal times.");
        lastWall = wallMs;
        RawTime = unchecked((int)(wallMs - origin) - 3000);
        // 005/040: strict crossing, followed by compensation anchoring back to -O.
        if (!MusicStarted && (long)EffectiveTime > -(long)offset)
        {
            MusicStarted = true; Compensation = unchecked(RawTime + offset);
        }
    }
}

public sealed class NoteState
{
    public Tap Data { get; }
    public bool Active { get; internal set; }
    public bool Missed { get; internal set; }
    public bool Consumed { get; internal set; }
    public int Contact { get; internal set; } = -1;
    public int Depth { get; internal set; }
    public int Bucket { get; internal set; }
    internal NoteState(Tap data) { Data = data; }
}

public sealed class Classification
{
    public string Note { get; }
    public string Outcome { get; }
    public int Error { get; }
    public bool ConsumesInput { get; }
    internal Classification(string note, string outcome, int error, bool consumes)
    { Note = note; Outcome = outcome; Error = error; ConsumesInput = consumes; }
}

public sealed class GameResult
{
    public int Pure { get; }
    public int Far { get; }
    public int Lost { get; }
    public int RecordedLost { get; }
    public int Shining { get; }
    public int Score { get; }
    public int Health { get; }
    public int Category { get; }
    public int MaxCombo { get; }
    public int Early { get; }
    public int Late { get; }
    internal GameResult(Kernel k)
    {
        Pure = k.Pure; Far = k.Far; Lost = k.Chart.JudgmentUnits - Pure - Far;
        RecordedLost = k.Lost; Shining = k.Shining; MaxCombo = k.MaxCombo;
        Health = (int)Math.Floor(k.Health); Early = k.Early; Late = k.Late;
        Score = Kernel.CalculateScore(Pure, Far, Shining, Pure + Far + Lost);
        Category = Health < 70 ? 0 : Lost != 0 ? 1 : Far != 0 ? 2 : 3;
    }
}

public sealed class Kernel
{
    public Chart Chart { get; }
    public Timeline Timeline { get; }
    public IReadOnlyList<NoteState> Notes { get; }
    private readonly List<NoteState> active = new List<NoteState>();
    private readonly Dictionary<int, List<NoteState>> buckets = new Dictionary<int, List<NoteState>>();
    private readonly Dictionary<int, int> contacts = new Dictionary<int, int>();
    private readonly float[] scales;
    private int nextContact;
    public float EffectiveSpeed { get; }
    public float BaseGain { get; }
    public int LastFrameTime { get; private set; } = -3000;
    public int Pure { get; private set; }
    public int Far { get; private set; }
    public int Lost { get; private set; }
    public int Shining { get; private set; }
    public int Score { get; private set; }
    public int Combo { get; private set; }
    public int MaxCombo { get; private set; }
    public int Early { get; private set; }
    public int Late { get; private set; }
    public float Health { get; private set; }
    public bool Finished { get; private set; }
    public GameResult? Result { get; private set; }
    public int ContactCount => contacts.Count;
    public List<string> Candidates { get; } = new List<string>();
    public List<Classification> Classifications { get; } = new List<Classification>();
    public List<string> Expired { get; } = new List<string>();

    public Kernel(Chart chart, long originMs = 0, int userOffset = 0, float requestedSpeed = 4, int baseBpm = 178)
    {
        if (!float.IsFinite(requestedSpeed) || requestedSpeed <= 0 || baseBpm <= 0)
            throw new ArgumentException("Positive finite speed and metadata BPM required.");
        Chart = chart; Timeline = new Timeline(originMs, chart.AudioOffset, userOffset);
        EffectiveSpeed = (requestedSpeed * 180f) / baseBpm;
        scales = chart.Timings.Select(t => (1f / (t.Bpm * EffectiveSpeed)) * 60f).ToArray();
        if (scales.Any(s => !float.IsFinite(s) || s <= 0)) throw new ArgumentException("Unsupported timing scale.");
        var notes = chart.Taps.Select(t => new NoteState(t)).ToList(); Notes = notes.AsReadOnly();
        foreach (var note in notes)
        {
            note.Bucket = (int)(DepthAt(note.Data.Time) / -10000f);
            note.Depth = (int)DepthAt(note.Data.Time);
            if (!buckets.TryGetValue(note.Bucket, out var list)) buckets[note.Bucket] = list = new List<NoteState>();
            list.Add(note);
        }
        int n = chart.JudgmentUnits;
        float total = n < 400 ? 200f + n * 0.5f : n < 600 ? 280f + (n - 400) * 0.5f : 360f + (n - 600) / 5f;
        BaseGain = (total / 2.5f) / n;
    }

    // 009: float timing integration before truncation; auxiliary bars are omitted.
    public float DepthAt(int time)
    {
        float depth = 0;
        for (int i = 0; i < Chart.Timings.Count; i++)
        {
            int start = Chart.Timings[i].Time;
            if (start >= time) break;
            int end = i + 1 < scales.Length ? Chart.Timings[i + 1].Time : int.MaxValue;
            int bound = Math.Min(end, time);
            depth -= (bound - Math.Max(start, 0)) / scales[i];
        }
        return depth;
    }

    private void BeginEvent() { Candidates.Clear(); Classifications.Clear(); Expired.Clear(); }

    public void Frame(long wallMs)
    {
        BeginEvent(); Timeline.Update(wallMs); int now = Timeline.EffectiveTime;
        LastFrameTime = now;
        float a = -DepthAt(now), b = -DepthAt(checked(now + 120));
        foreach (var note in active.ToArray())
        {
            // 010 preprocessing stores integer pre-depth; the frame adds current float depth to that stored value.
            note.Depth = (int)((int)DepthAt(note.Data.Time) + a);
            if ((note.Missed || note.Consumed || Finished) && now > note.Data.Time)
            { note.Active = false; active.Remove(note); }
        }
        int low = Math.Min((int)((a - 700f) / 10000f), (int)((b - 700f) / 10000f));
        int high = Math.Max((int)((a + 10000f) / 10000f), (int)((b - 700f) / 10000f));
        // Enumerate only existing keys; native insertion of empty buckets has no gameplay effect.
        foreach (var pair in buckets.OrderBy(p => p.Key))
        {
            if (pair.Key < low || pair.Key > high) continue;
            foreach (var note in pair.Value)
            {
                if (note.Active) continue;
                note.Depth = (int)((int)DepthAt(note.Data.Time) + a);
                if (note.Depth >= 300 || note.Missed || note.Consumed || Finished) continue;
                note.Active = true; active.Add(note);
            }
        }
        if (Finished) return;
        foreach (var note in active)
            if (!note.Missed && !note.Consumed && now > note.Data.Time + 100)
            { Miss(note); Expired.Add(note.Data.Id); }
        if (now > Chart.EndTime)
        { Finished = true; Result = new GameResult(this); }
    }

    public void Down(long wallMs, int pointer, int lane)
    {
        BeginEvent();
        if (lane < 2 || lane > 5) throw new NotSupportedException("Ordinary input accepts internal lanes 2..5; widening is deferred.");
        if (contacts.ContainsKey(pointer)) throw new ArgumentException("DOWN pointer already retained.");
        int contact = nextContact++; contacts.Add(pointer, contact);
        if (Finished) return;
        Timeline.Update(wallMs); int now = Timeline.EffectiveTime;
        // Range maintenance belongs to FRAME, never to DOWN. Guards are evaluated after collection.
        var ordered = active.Where(n => n.Data.Lane == lane).OrderBy(n => n.Data.Time).ThenBy(n => n.Data.Ordinal).ToArray();
        Candidates.AddRange(ordered.Select(n => n.Data.Id));
        foreach (var note in ordered)
        {
            int error = (int)Math.Abs((long)now - note.Data.Time);
            string outcome; bool consumes = false;
            if (note.Missed) outcome = "guard_missed";
            else if (note.Consumed) outcome = "guard_consumed";
            else if (error > 120) outcome = "outside_window";
            else if (error > 100) { outcome = "LOST"; Miss(note); consumes = true; }
            else
            {
                int id = error <= 25 ? 0 : error <= 50 ? 1 : 2;
                outcome = id == 0 ? "SHINING_PURE" : id == 1 ? "PURE" : "FAR";
                note.Consumed = true; note.Contact = contact;
                if (id == 0) Shining++;
                if (id < 2) Pure++; else Far++;
                if (id != 0) { if (now < note.Data.Time) Early++; else Late++; }
                ApplyHealth(id < 2 ? BaseGain : BaseGain * 0.5f, 0);
                Score = CalculateScore(Pure, Far, Shining, Chart.JudgmentUnits);
                Combo++; MaxCombo = Math.Max(MaxCombo, Combo); consumes = true;
            }
            Classifications.Add(new Classification(note.Data.Id, outcome, error, consumes));
            if (consumes) break;
        }
    }

    // Ordinary UP only cleans retained contacts; it does not refresh the judgment clock (035).
    public void Up(int pointer) { BeginEvent(); if (!contacts.Remove(pointer)) throw new ArgumentException("UP pointer is not retained."); }
    private void Miss(NoteState note)
    { note.Missed = true; Lost++; ApplyHealth(0, 2); Combo = 0; }
    private void ApplyHealth(float gain, float damage)
    { float sum = Health + gain; float value = sum - damage; Health = Math.Max(0f, Math.Min(100f, value)); }
    public static int CalculateScore(int pure, int far, int shining, int total)
    {
        if (total <= 0) throw new ArgumentException("Positive judgment count required.");
        if (pure == total) return 10000000 + shining;
        long weighted = 10L * pure + 5L * far;
        long quotient = weighted * 1000000000L / total;
        return checked((int)Math.Min(quotient / 1000L, 10000000L) + shining);
    }
}
