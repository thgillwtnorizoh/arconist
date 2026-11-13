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
    public virtual int TimingGroupId => 0;
    public virtual bool InputEnabled => true;
    public int PreDepth { get; internal set; }
    public int PreEndDepth { get; internal set; }
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
    public override int TimingGroupId => Data.Group.Id;
    public override bool InputEnabled => Data.InputEnabled;
    public bool Missed { get; internal set; }
    public bool Consumed { get; internal set; }
    public int Contact { get; internal set; } = -1;
    internal NoteState(Tap data) { Data = data; }
}

public sealed class CheckpointState
{
    public int Time { get; }
    public int Weight { get; } // E038 arc weights; ordinary holds remain1.
    public bool Resolved { get; internal set; }
    public string? Outcome { get; internal set; }
    public int? ResolvedAt { get; internal set; }
    internal CheckpointState(int time,int weight=1) { Time = time; Weight=weight; }
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
    public SkyContact? Sky {get;internal set;}
    public SkyContact? PreviousSky {get;internal set;}
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
    public IReadOnlyList<ArcState> Arcs {get;}
    public IReadOnlyList<ArcTapState> ArcTaps {get;}
    public IReadOnlyList<ArcGroupState> ArcGroups {get;}
    public List<RecorderObservation> RecorderTrace {get;}=new List<RecorderObservation>();
    public int RecorderCalls {get;private set;}
    private readonly Dictionary<int,ArcColorState> colors=new Dictionary<int,ArcColorState>();
    private readonly HashSet<int> claimed=new HashSet<int>();
    public IReadOnlyDictionary<int,ArcColorState> Colors=>colors;
    public IReadOnlyList<int> ClaimedIds=>claimed.OrderBy(i=>i).ToArray();
    private readonly List<RuntimeNote> active = new List<RuntimeNote>();
    public IReadOnlyList<TimingGroupState> TimingGroups { get; }
    private readonly Dictionary<int, RetainedContact> contacts = new Dictionary<int, RetainedContact>();
    public IReadOnlyList<RetainedContact> Contacts => contacts.Values.OrderBy(c => c.Id).ToList().AsReadOnly();
    public List<JudgmentEvent> Judgments { get; } = new List<JudgmentEvent>();
    private readonly float[] scales;
    private int nextContact;
    public float RequestedSpeed { get; }
    public int MetadataBpm { get; }
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

    public Kernel(Chart chart, long originMs = 0, int userOffset = 0, float requestedSpeed = 4, int baseBpm = 178, int arcHeight=500)
    {
        if (!float.IsFinite(requestedSpeed) || requestedSpeed <= 0 || baseBpm <= 0)
            throw new ArgumentException("Positive finite speed and metadata BPM required.");
        RequestedSpeed=requestedSpeed;MetadataBpm=baseBpm;
        Chart = chart; Timeline = new Timeline(originMs, chart.AudioOffset, userOffset);
        EffectiveSpeed = (requestedSpeed * 180f) / baseBpm;
        TimingGroups=chart.TimingGroups.Select(g=>new TimingGroupState(g,EffectiveSpeed,chart.EndTime,chart.TimingGroups.Count>1)).ToArray();
        scales = TimingGroups[0].Records.Select(t=>t.Scale).ToArray();
        if (scales.Any(s => !float.IsFinite(s) || s <= 0)) throw new ArgumentException("Unsupported timing scale.");
        var notes = chart.Taps.Select(t => new NoteState(t)).ToList(); Notes = notes.AsReadOnly();
        var holds = chart.Holds.Select(h => new HoldState(h)).ToList(); Holds = holds.AsReadOnly();
        var arcs=chart.Arcs.Select(a=>{
            if(!colors.TryGetValue(a.Color,out var color))colors[a.Color]=color=new ArcColorState(a.Color);
            int ti=chart.Timings.ToList().FindLastIndex(t=>t.Time<=a.Start);
            return new ArcState(a,new ArcGeometry(a,scales[ti],arcHeight),color);
        }).ToList();Arcs=arcs.AsReadOnly();ArcTaps=arcs.SelectMany(a=>a.Children).ToList().AsReadOnly();
        var byDefinition=arcs.ToDictionary(a=>a.Data);var groups=new List<ArcGroupState>();
        foreach(var arc in arcs)
        {
            if(arc.Data.Predecessor!=null)arc.Predecessor=byDefinition[arc.Data.Predecessor];
            foreach(var next in arc.Data.Successors)arc.successors.Add(byDefinition[next]);
            if(arc.Data.Group!=null&&arc.Data.Predecessor==null)
            {var group=new ArcGroupState(arc.Data.Group,arc,byDefinition[arc.Data.Group.Successor]);foreach(var member in group.Members)member.Group=group;groups.Add(group);}
        }
        ArcGroups=groups.AsReadOnly();
        var objects = notes.Cast<RuntimeNote>().Concat(holds).Concat(arcs).OrderBy(n => n.Start).ThenBy(n => n.SourceOrder);
        foreach (var note in objects) TimingGroups[note.TimingGroupId].Insert(note);
        int n = chart.JudgmentUnits;
        float total = n < 400 ? 200f + n * 0.5f : n < 600 ? 280f + (n - 400) * 0.5f : 360f + (n - 600) / 5f;
        BaseGain = (total / 2.5f) / n;
    }

    // 009: float timing integration before truncation; auxiliary bars are omitted.
    public float DepthAt(int time) => DepthAt(time,0);
    public float DepthAt(int time,int group) => TimingGroups[group].DepthAt(time);
    public int CurrentDepth(RuntimeNote note) => (int)(note.PreDepth-DepthAt(Timeline.EffectiveTime,note.TimingGroupId));

    private void BeginEvent() { Candidates.Clear(); Classifications.Clear(); Expired.Clear(); Judgments.Clear(); RecorderTrace.Clear(); }

    public void Frame(long wallMs)
    {
        BeginEvent(); Timeline.Update(wallMs); int now = Timeline.EffectiveTime;
        LastFrameTime = now;
        if(Paused)
        {
            // Native paused model resets activity, preserving latch/retained IDs.
            foreach(var hold in Holds) {hold.Holding=false;hold.activating.Clear();}
            foreach(var arc in Arcs)arc.Holding=false;
            foreach(var group in ArcGroups){group.Active=false;group.Accepted=false;}
            return;
        }
        foreach(var group in TimingGroups)group.Update(now);
        foreach (var note in active.ToArray())
        {
            // 010 preprocessing stores integer pre-depth; the frame adds current float depth to that stored value.
            var group=TimingGroups[note.TimingGroupId];group.UpdateDepth(note);
            if(note is ArcState arc && !arc.Data.Trace && now>arc.End&&!arc.EndReset)
            {
                arc.EndReset=true;
                if(arc.Successors.Any(next=>!next.Data.Trace))arc.SuccessorCleanupPreserved=true;
                else {arc.Color.PreviouslyClaimed=false;arc.Color.ReleaseTime=-1;arc.Color.Conflict=false;}
            }
            if (!group.Active || ((note.Terminal || Finished) && now > note.End))
            { note.Active = false; active.Remove(note); }
        }
        // One spatial map/query per timing group. Retention above never reapplies
        // fresh-admission depth limits (E029 reverse excursion hysteresis).
        foreach(var group in TimingGroups)
        {
            if(!group.Active)continue;
            foreach(var pair in group.Buckets)
            {
                if(pair.Key<group.QueryLow||pair.Key>group.QueryHigh)continue;
                foreach(var note in pair.Value)
                {
                    if(note.Active)continue;
                    group.UpdateDepth(note);
                    if(Math.Min(note.Depth,note.EndDepth)>=(note is ArcState?700:300)||note.Terminal||Finished)continue;
                    note.Active=true;active.Add(note);
                }
            }
        }
        foreach(var child in ArcTaps)
        {child.Active=child.Parent.Active;child.Depth=(int)child.WorldPosition.Z;child.EndDepth=child.Depth;}
        if (Finished) return;
        // E026/E037: reset frame activity, then restore it through ALL retained
        // contacts. Initial DOWN never performs this frame pass or owns the hold.
        foreach (var hold in Holds) { hold.Holding = false; hold.activating.Clear(); }
        foreach (var contact in contacts.Values.OrderBy(c => c.Id))
            foreach (var hold in active.OfType<HoldState>())
                if (hold.Latched && hold.Start < now && now < hold.End && contact.Lane == hold.Lane)
                { hold.Holding = true; hold.activating.Add(contact.Id); }
        foreach(var color in colors.Values){color.Accepted=false;color.Conflict=false;}
        foreach(var group in ArcGroups){group.Active=false;group.Accepted=false;}
        foreach(var arc in Arcs)
        {arc.Holding=false;if(arc.Active)arc.UpdateCache(now);else if(arc.Group!=null)arc.ClearEligibility();if(arc.CacheEnabled&&arc.Group!=null)arc.Group.CacheRelated=true;}
        foreach(var contact in contacts.Values.OrderBy(c=>c.Id))
            if(contact.Sky.HasValue)foreach(var arc in active.OfType<ArcState>())
                if(!arc.Data.Trace&&arc.CacheEnabled&&ArcSpatial.Matches(arc.TargetX,arc.TargetY,contact.Sky.Value)&&Claim(arc.Color,contact.Id,now,(int)arc.Data.Interval)){arc.Holding=true;arc.Group?.Accept(arc);}
        foreach (var item in active)
        {
            if (item is NoteState note && note.InputEnabled && !note.Missed && !note.Consumed && now > note.Data.Time + 100)
            { Miss(note); Expired.Add(note.Data.Id); }
            else if (item is HoldState hold) ResolveHold(hold, now);
            else if(item is ArcState arc)ResolveArc(arc,now);
        }
        if (now > Chart.EndTime)
        { Finished = true; Result = new GameResult(this); }
    }

    public void Down(long wallMs, int pointer, int lane)=>DownContact(wallMs,pointer,lane,null,false);
    public void DownSpatial(long wallMs,int pointer,int lane,SkyContact? sky)=>DownContact(wallMs,pointer,lane,sky,true);
    private void DownContact(long wallMs,int pointer,int lane,SkyContact? sky,bool spatial)
    {
        BeginEvent();
        if (Paused) return; // Reject new contacts before allocation/time refresh.
        if ((!spatial||lane!=0)&&(lane < 2 || lane > 5)) throw new NotSupportedException("Ordinary input accepts internal lanes 2..5; widening is deferred.");
        if (contacts.ContainsKey(pointer)) throw new ArgumentException("DOWN pointer already retained.");
        int contact = nextContact++; contacts.Add(pointer, new RetainedContact(pointer, contact, lane){Sky=sky.HasValue&&sky.Value.Valid?sky:null});
        if (Finished) return;
        Timeline.Update(wallMs); int now = Timeline.EffectiveTime;
        // FRAME owns ranges/cache. Initial children are collected by traversing their
        // active parent, including already-consumed children for the native guard.
        var collected=new List<RuntimeNote>();
        foreach(var item in active)
        {
            if(item.InputEnabled&&lane!=0&&item.Lane==lane&&(item is NoteState||(item is HoldState&&item.Start<(long)now+100&&now<item.End)))collected.Add(item);
            if(item is ArcState parent&&spatial&&sky.HasValue)
                foreach(var child in parent.Children)
                    if(ArcTapSpatial.Matches(child.InputTarget.X,child.InputTarget.Y,sky.Value))collected.Add(child);
        }
        // R008 rejects ground/child conflicts; this is not a universal mixed-note policy.
        var ordered=collected.OrderBy(n=>n.Start).ThenBy(n=>n.SourceOrder).ToArray();
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
            if(JudgeTap(item,contact,now))break;
        }
    }

    private bool JudgeTap(RuntimeNote item,int contact,int now)
    {
        var ground=item as NoteState;var child=item as ArcTapState;
        if(ground==null&&child==null)throw new InvalidOperationException("Not a tap-tier candidate.");
        int error=(int)Math.Abs((long)now-item.Start);string outcome;bool consumes=false;
        bool missed=ground?.Missed??child!.Missed,consumed=ground?.Consumed??child!.Consumed;
        if(missed)outcome="guard_missed";
        else if(consumed)outcome="guard_consumed";
        else if(error>120)outcome="outside_window";
        else if(error>100){outcome="LOST";Miss(item);consumes=true;}
        else
        {
            int id=error<=25?0:error<=50?1:2;outcome=id==0?"SHINING_PURE":id==1?"PURE":"FAR";
            if(ground!=null){ground.Consumed=true;ground.Contact=contact;}
            else {child!.Consumed=true;child.Contact=contact;child.Outcome=outcome;child.ResolvedAt=now;}
            RecordAccepted(item.Id,null,id,now);
            if(id!=0){if(now<item.Start)Early++;else Late++;}consumes=true;
        }
        Classifications.Add(new Classification(item.Id,outcome,error,consumes));return consumes;
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

    public void MoveSpatial(int pointer,int lane,SkyContact? sky)
    {Move(pointer,lane);var contact=contacts[pointer];contact.PreviousSky=contact.Sky;contact.Sky=sky.HasValue&&sky.Value.Valid?sky:null;}
    private bool Claim(ArcColorState color,int id,int now,int interval)
    {
        color.IntervalInteger=interval;
        if(color.ReleaseTime!=-1){if((long)now-color.ReleaseTime<(int)Math.Min(4L*interval,1000)){if(!color.Accepted)color.Conflict=true;return false;}color.ReleaseTime=-1;}
        if(color.Owner==id){color.Accepted=true;return true;}
        if(color.Owner!=-1||claimed.Contains(id)){if(!color.Accepted)color.Conflict=true;return false;}
        color.Owner=id;color.Accepted=color.PreviouslyClaimed=true;claimed.Add(id);return true;
    }
    private void ReleaseArcContact(int pointer)
    {
        if(!contacts.TryGetValue(pointer,out var contact))return;
        foreach(var color in colors.Values)if(color.Owner==contact.Id){color.Owner=-1;if(claimed.Remove(contact.Id)&&color.PreviouslyClaimed)color.ReleaseTime=Timeline.EffectiveTime;}
    }
    // Ordinary UP only cleans retained contacts; it does not refresh the judgment clock (035).
    public void Up(int pointer) { BeginEvent(); ReleaseArcContact(pointer); if (!contacts.Remove(pointer)) throw new ArgumentException("UP pointer is not retained."); }
    public void Cancel(int pointer) { BeginEvent(); ReleaseArcContact(pointer); if(!contacts.Remove(pointer)) throw new ArgumentException("CANCEL pointer is not retained."); }
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
    private void Miss(RuntimeNote note)
    {
        if(note is NoteState ground)ground.Missed=true;
        else if(note is ArcTapState child)
        {
            // E002 parent-dependent miss guard: supported parent is trace mode1.
            if(!child.Parent.Data.Trace)throw new InvalidOperationException("Unsupported parent miss state.");
            child.Missed=true;child.Outcome="LOST";child.ResolvedAt=Timeline.EffectiveTime;
        }
        else throw new InvalidOperationException("Not a tap-tier miss.");
        RecordMiss(note.Id,null,Timeline.EffectiveTime);
    }

    private void RecordAccepted(string note, int? checkpoint, int id, int now)
    {
        if (id == 0) Shining++;
        if (id < 2) Pure++; else Far++;
        ApplyHealth(id < 2 ? BaseGain : BaseGain * 0.5f, 0);
        Score = CalculateScore(Pure, Far, Shining, Chart.JudgmentUnits);
        Combo++; MaxCombo = Math.Max(MaxCombo, Combo);
        Judgments.Add(new JudgmentEvent(note, checkpoint, id == 0 ? "SHINING_PURE" : id == 1 ? "PURE" : "FAR", now));
        RecorderTrace.Add(new RecorderObservation(++RecorderCalls,note,checkpoint,id==0?"SHINING_PURE":id==1?"PURE":"FAR",now,this));
    }
    private void RecordMiss(string note, int? checkpoint, int now)
    {
        Lost++; ApplyHealth(0, 2); Combo = 0;
        // E008/009: derived ordinary LogicHoldNote takes the 2HP branch.
        Judgments.Add(new JudgmentEvent(note, checkpoint, "LOST", now));
        RecorderTrace.Add(new RecorderObservation(++RecorderCalls,note,checkpoint,"LOST",now,this));
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
    private void ResolveArc(ArcState arc,int now)
    {
        if(arc.Data.Trace)
        {
            foreach(var child in arc.Children)
                if(!child.Terminal&&now>child.End+100){Miss(child);Expired.Add(child.Id);}
            return;
        }
        int last=-1;
        if(arc.Holding){int cutoff=(int)((float)now+arc.Data.Interval*0.5f);while(last+1<arc.Records.Count&&arc.Records[last+1].Time<=cutoff)last++;}
        else if(arc.InactiveExpiryAllowed)
        {
            int halfCutoff=(int)((double)now-Math.Min((double)arc.Data.Interval*0.5,500.0));
            int count=arc.Records.Count(r=>r.Time<=halfCutoff);
            if(count==1&&arc.FirstRecordEarlyExpiry)last=0;
            else {int cutoff=(int)((float)now-Math.Min(arc.Data.Interval*2f,500f));while(last+1<arc.Records.Count&&arc.Records[last+1].Time<=cutoff)last++;}
        }
        for(int i=last;i>=0&&!arc.Records[i].Resolved;i--)
        {
            var r=arc.Records[i];arc.ResolutionWrites++;r.Resolved=true;r.ResolvedAt=now;r.Outcome=arc.Holding?"SHINING_PURE":"LOST";
            for(int unit=0;unit<r.Weight;unit++)if(arc.Holding)RecordAccepted(arc.Id,r.Time,0,now);else{RecordMiss(arc.Id,r.Time,now);Expired.Add(arc.Id+":checkpoint:"+r.Time);}
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
