namespace Arconist.Core;

// Immutable logical playback request; no engine, asset, audio playhead or input timestamp.
public sealed class MusicStartRequest
{
    public long WallMilliseconds { get; }
    public int RawTime { get; }
    public int CompensationBefore { get; }
    public int EffectiveTimeBefore { get; }
    public int CombinedOffset { get; }
    public int CompensationAfter => unchecked(RawTime + CombinedOffset);
    public int EffectiveTimeAfter => unchecked(-CombinedOffset);
    internal MusicStartRequest(long wall, int raw, int compensation, int offset)
    { WallMilliseconds=wall; RawTime=raw; CompensationBefore=compensation; EffectiveTimeBefore=unchecked(raw-compensation); CombinedOffset=offset; }
}

public sealed class Timeline
{
    private readonly long origin;
    private readonly int offset;
    private long lastWall;
    public int RawTime { get; private set; }
    public int Compensation { get; private set; }
    public int EffectiveTime => unchecked(RawTime - Compensation);
    public bool MusicStarted { get; private set; }
    public int CombinedOffset => offset;
    public bool Paused { get; private set; }
    public int PauseReference { get; private set; }
    public int MusicAnchor { get; private set; }
    public int StartRequestCount { get; private set; }
    public MusicStartRequest? LastStartRequest { get; private set; }
    private readonly List<string> notificationErrors = new List<string>();
    public IReadOnlyList<string> NotificationErrors => notificationErrors.AsReadOnly();
    public event Action<MusicStartRequest>? MusicStartRequested;
    public event Action<MusicStartRequest>? MusicStartAnchored;
    private bool updating;
    private void Notify(Action<MusicStartRequest>? handlers, MusicStartRequest request)
    {
        if (handlers == null) return;
        foreach (Action<MusicStartRequest> callback in handlers.GetInvocationList())
            try { callback(request); } catch (Exception e) { notificationErrors.Add(e.GetType().Name + ": " + e.Message); }
    }
    public Timeline(long originMs, int chartOffset, int userOffset)
    {
        origin = lastWall = originMs; offset = checked(chartOffset + userOffset);
        RawTime = -3000;
    }
    public void Update(long wallMs)
    {
        if (updating) throw new InvalidOperationException("Timeline notifications cannot reenter Update.");
        if (wallMs < lastWall) throw new ArgumentException("Wall time must be monotonic; array order resolves equal times.");
        lastWall = wallMs;
        RawTime = unchecked((int)(wallMs - origin) - 3000);
        if (Paused) { Compensation = unchecked(RawTime - PauseReference); return; }
        // 005/040: strict crossing, followed by compensation anchoring back to -O.
        if (!MusicStarted && (long)EffectiveTime > -(long)offset)
        {
            MusicStarted = true;
            var request = new MusicStartRequest(wallMs, RawTime, Compensation, offset);
            LastStartRequest = request; StartRequestCount++;
            updating = true;
            try
            {
                // E040: native latch -> request entry BEFORE compensation stores.
                Notify(MusicStartRequested, request);
                Compensation = request.CompensationAfter; MusicAnchor = request.EffectiveTimeAfter;
                Notify(MusicStartAnchored, request);
            }
            finally { updating = false; }
        }
    }
    // E005/012/041 ordinary A=0. Audio callbacks cannot own the clock.
    public bool Pause(long wallMs, Action? requestPause=null)
    {
        if(updating) throw new InvalidOperationException("Reentrant pause transition.");
        if(Paused) return false;
        Update(wallMs); PauseReference=EffectiveTime; updating=true;
        try { try { requestPause?.Invoke(); } catch(Exception e) {notificationErrors.Add(e.Message);} Paused=true; }
        finally {updating=false;}
        return true;
    }
    public bool Resume(long wallMs, Func<int,bool>? seekAndUnpause=null)
    {
        if(updating) throw new InvalidOperationException("Reentrant resume transition.");
        if(!Paused) return false;
        Update(wallMs); // MUST absorb elapsed time while still paused.
        updating=true;
        try
        {
            if(MusicStarted && seekAndUnpause!=null && !seekAndUnpause(unchecked(EffectiveTime-MusicAnchor))) return false;
            Paused=false; return true;
        }
        catch(Exception e) {notificationErrors.Add(e.Message);return false;}
        finally {updating=false;}
    }

}

public abstract class RuntimeNote
{
    public abstract string Id { get; }
    public abstract int Start { get; }
    public abstract int End { get; }
    public abstract int Lane { get; }
    public abstract int SourceOrder { get; }
    public abstract bool Terminal { get; }
    public bool Active { get; internal set; }
    public int Depth { get; internal set; }
    public int EndDepth { get; internal set; }
    public int Bucket { get; internal set; }
    public int EndBucket { get; internal set; }
}

public sealed class NoteState : RuntimeNote
{
    public Tap Data { get; }
    public override string Id => Data.Id;
    public override int Start => Data.Time;
    public override int End => Data.Time;
    public override int Lane => Data.Lane;
    public override int SourceOrder => Data.SourceOrder;
    public override bool Terminal => Missed || Consumed;
    public bool Missed { get; internal set; }
    public bool Consumed { get; internal set; }
    public int Contact { get; internal set; } = -1;
    internal NoteState(Tap data) { Data = data; }
}

public sealed class CheckpointState
{
    public int Time { get; }
    public int Weight => 1; // Ordinary hold flag0 records, E001/026.
    public bool Resolved { get; internal set; }
    public string? Outcome { get; internal set; }
    public int? ResolvedAt { get; internal set; }
    internal CheckpointState(int time) { Time = time; }
}

public sealed class HoldState : RuntimeNote
{
    public Hold Data { get; }
    public override string Id => Data.Id;
    public override int Start => Data.Start;
    public override int End => Data.End;
    public override int Lane => Data.Lane;
    public override int SourceOrder => Data.SourceOrder;
    public override bool Terminal => Records.All(r => r.Resolved);
    public bool Latched { get; internal set; }
    public bool Holding { get; internal set; }
    // Factory0x144650c initializes +6c to0 for this ordinary hold domain.
    public bool FirstRecordEarlyExpiry => false;
    public IReadOnlyList<CheckpointState> Records { get; }
    public IReadOnlyList<int> ActivatingContacts => activating.AsReadOnly();
    internal readonly List<int> activating = new List<int>();
    internal HoldState(Hold data) { Data = data; Records = data.Checkpoints.Select(t => new CheckpointState(t)).ToList().AsReadOnly(); }
}

public sealed class RetainedContact
{
    public int Pointer { get; }
    public int Id { get; }
    public int Lane { get; internal set; }
    internal RetainedContact(int pointer, int id, int lane) { Pointer = pointer; Id = id; Lane = lane; }
}

public sealed class JudgmentEvent
{
    public string Note { get; }
    public int? CheckpointTime { get; }
    public string Outcome { get; }
    public int EffectiveTime { get; }
    internal JudgmentEvent(string note, int? checkpointTime, string outcome, int effectiveTime)
    { Note = note; CheckpointTime = checkpointTime; Outcome = outcome; EffectiveTime = effectiveTime; }
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
    public IReadOnlyList<HoldState> Holds { get; }
    private readonly List<RuntimeNote> active = new List<RuntimeNote>();
    private readonly Dictionary<int, List<RuntimeNote>> buckets = new Dictionary<int, List<RuntimeNote>>();
    private readonly Dictionary<int, RetainedContact> contacts = new Dictionary<int, RetainedContact>();
    public IReadOnlyList<RetainedContact> Contacts => contacts.Values.OrderBy(c => c.Id).ToList().AsReadOnly();
    public List<JudgmentEvent> Judgments { get; } = new List<JudgmentEvent>();
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
    public bool ModelPaused { get; private set; }
    public bool Paused => ModelPaused || Timeline.Paused;
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
        var holds = chart.Holds.Select(h => new HoldState(h)).ToList(); Holds = holds.AsReadOnly();
        var objects = notes.Cast<RuntimeNote>().Concat(holds).OrderBy(n => n.Start).ThenBy(n => n.SourceOrder);
        foreach (var note in objects)
        {
            note.Bucket = (int)(DepthAt(note.Start) / -10000f);
            note.EndBucket = (int)(DepthAt(note.End) / -10000f);
            note.Depth = (int)DepthAt(note.Start); note.EndDepth = (int)DepthAt(note.End);
            // E009 endpoint-only index: one long note can occupy several buckets.
            if ((long)note.EndBucket - note.Bucket > 100000)
                throw new NotSupportedException("Hold index exceeds the supported bucket span.");
            for (int key = note.Bucket; key <= note.EndBucket; key++)
            {
                if (!buckets.TryGetValue(key, out var list)) buckets[key] = list = new List<RuntimeNote>();
                list.Add(note);
            }
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

    private void BeginEvent() { Candidates.Clear(); Classifications.Clear(); Expired.Clear(); Judgments.Clear(); }

    public void Frame(long wallMs)
    {
        BeginEvent(); Timeline.Update(wallMs); int now = Timeline.EffectiveTime;
        LastFrameTime = now;
        if(Paused)
        {
            // Native paused model resets activity, preserving latch/retained IDs.
            foreach(var hold in Holds) {hold.Holding=false;hold.activating.Clear();}
            return;
        }
        float a = -DepthAt(now), b = -DepthAt(checked(now + 120));
        foreach (var note in active.ToArray())
        {
            // 010 preprocessing stores integer pre-depth; the frame adds current float depth to that stored value.
            note.Depth = (int)((int)DepthAt(note.Start) + a);
            note.EndDepth = (int)((int)DepthAt(note.End) + a);
            if ((note.Terminal || Finished) && now > note.End)
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
                note.Depth = (int)((int)DepthAt(note.Start) + a);
                note.EndDepth = (int)((int)DepthAt(note.End) + a);
                if (Math.Min(note.Depth, note.EndDepth) >= 300 || note.Terminal || Finished) continue;
                note.Active = true; active.Add(note);
            }
        }
        if (Finished) return;
        // E026/E037: reset frame activity, then restore it through ALL retained
        // contacts. Initial DOWN never performs this frame pass or owns the hold.
        foreach (var hold in Holds) { hold.Holding = false; hold.activating.Clear(); }
        foreach (var contact in contacts.Values.OrderBy(c => c.Id))
            foreach (var hold in active.OfType<HoldState>())
                if (hold.Latched && hold.Start < now && now < hold.End && contact.Lane == hold.Lane)
                { hold.Holding = true; hold.activating.Add(contact.Id); }
        foreach (var item in active)
        {
            if (item is NoteState note && !note.Missed && !note.Consumed && now > note.Data.Time + 100)
            { Miss(note); Expired.Add(note.Data.Id); }
            else if (item is HoldState hold) ResolveHold(hold, now);
        }
        if (now > Chart.EndTime)
        { Finished = true; Result = new GameResult(this); }
    }

    public void Down(long wallMs, int pointer, int lane)
    {
        BeginEvent();
        if (Paused) return; // Reject new contacts before allocation/time refresh.
        if (lane < 2 || lane > 5) throw new NotSupportedException("Ordinary input accepts internal lanes 2..5; widening is deferred.");
        if (contacts.ContainsKey(pointer)) throw new ArgumentException("DOWN pointer already retained.");
        int contact = nextContact++; contacts.Add(pointer, new RetainedContact(pointer, contact, lane));
        if (Finished) return;
        Timeline.Update(wallMs); int now = Timeline.EffectiveTime;
        // Range maintenance belongs to FRAME, never to DOWN. Guards are evaluated after collection.
        var ordered = active.Where(n => n.Lane == lane &&
            (n is NoteState || (n.Start < (long)now + 100 && now < n.End)))
            .OrderBy(n => n.Start).ThenBy(n => n.SourceOrder).ToArray();
        Candidates.AddRange(ordered.Select(n => n.Id));
        foreach (var item in ordered)
        {
            if (item is HoldState hold)
            {
                // E037: even a prior latch1->1 stops initial iteration.
                hold.Latched = true;
                Classifications.Add(new Classification(hold.Id, "HOLD_LATCH", 0, true));
                break;
            }
            var note = (NoteState)item;
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
                RecordAccepted(note.Id, null, id, now);
                if (id != 0) { if (now < note.Data.Time) Early++; else Late++; }
                consumes = true;
            }
            Classifications.Add(new Classification(note.Data.Id, outcome, error, consumes));
            if (consumes) break;
        }
    }

    // Desktop retained mouse movement changes lane membership, not initial
    // arbitration, timeline or FRAME. Lane0 means outside the supported track.
    public void Move(int pointer, int lane)
    {
        BeginEvent();
        if (lane != 0 && (lane < 2 || lane > 5)) throw new NotSupportedException("Unsupported contact lane.");
        if (!contacts.TryGetValue(pointer, out var contact)) throw new ArgumentException("MOVE pointer is not retained.");
        contact.Lane = lane;
    }

    // Ordinary UP only cleans retained contacts; it does not refresh the judgment clock (035).
    public void Up(int pointer) { BeginEvent(); if (!contacts.Remove(pointer)) throw new ArgumentException("UP pointer is not retained."); }
    public void Cancel(int pointer) { BeginEvent(); if(!contacts.Remove(pointer)) throw new ArgumentException("CANCEL pointer is not retained."); }
    public bool Pause(long wallMs,Action? requestPause=null)
    {
        if(Finished || Paused) return false;
        BeginEvent();ModelPaused=true;
        return Timeline.Pause(wallMs,requestPause);
    }
    public bool Resume(long wallMs,Func<int,bool>? seekAndUnpause=null)
    {
        if(Finished || !Paused) return false;
        BeginEvent();
        if(!Timeline.Resume(wallMs,seekAndUnpause)) return false;
        ModelPaused=false;return true;
    }
    private void Miss(NoteState note)
    { note.Missed = true; RecordMiss(note.Id, null, Timeline.EffectiveTime); }

    private void RecordAccepted(string note, int? checkpoint, int id, int now)
    {
        if (id == 0) Shining++;
        if (id < 2) Pure++; else Far++;
        ApplyHealth(id < 2 ? BaseGain : BaseGain * 0.5f, 0);
        Score = CalculateScore(Pure, Far, Shining, Chart.JudgmentUnits);
        Combo++; MaxCombo = Math.Max(MaxCombo, Combo);
        Judgments.Add(new JudgmentEvent(note, checkpoint, id == 0 ? "SHINING_PURE" : id == 1 ? "PURE" : "FAR", now));
    }
    private void RecordMiss(string note, int? checkpoint, int now)
    {
        Lost++; ApplyHealth(0, 2); Combo = 0;
        // E008/009: derived ordinary LogicHoldNote takes the 2HP branch.
        Judgments.Add(new JudgmentEvent(note, checkpoint, "LOST", now));
    }
    private void ResolveHold(HoldState hold, int now)
    {
        int last = -1;
        if (hold.Holding)
        {
            int cutoff = (int)((float)now + hold.Data.Interval * 0.5f);
            while (last + 1 < hold.Records.Count && hold.Records[last + 1].Time <= cutoff) last++;
        }
        else
        {
            // E002 c6e938: double half-cutoff, then f32 overdue cutoff. Ordinary
            // factory flag+6c is0; preserve its separate first-record condition.
            int halfCutoff = (int)((double)now - Math.Min((double)hold.Data.Interval * 0.5, 500.0));
            int count = hold.Records.Count(r => r.Time <= halfCutoff);
            if (count == 1 && hold.FirstRecordEarlyExpiry) last = 0;
            else
            {
                int cutoff = (int)((float)now - Math.Min(hold.Data.Interval * 2f, 500f));
                while (last + 1 < hold.Records.Count && hold.Records[last + 1].Time <= cutoff) last++;
            }
        }
        // Native resolves an unresolved prefix backwards, stopping at a resolved
        // record, then makes one genuine recorder/clamp call per unit.
        var resolved = new List<CheckpointState>();
        for (int i = last; i >= 0 && !hold.Records[i].Resolved; i--)
        {
            var r = hold.Records[i]; r.Resolved = true; r.ResolvedAt = now;
            r.Outcome = hold.Holding ? "SHINING_PURE" : "LOST"; resolved.Add(r);
        }
        foreach (var r in resolved)
            for (int unit = 0; unit < r.Weight; unit++)
            {
                if (hold.Holding) RecordAccepted(hold.Id, r.Time, 0, now);
                else { RecordMiss(hold.Id, r.Time, now); Expired.Add(hold.Id + ":checkpoint:" + r.Time); }
            }
    }
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
