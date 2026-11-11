using Arconist.Core;

namespace Arconist.Bridge;

public interface IMonotonicClock { long Milliseconds { get; } }

// Godot calls this bridge in callback order. It never moves FRAME work into DOWN.
public sealed class GameplaySession
{
    private readonly IMonotonicClock clock;
    private readonly HashSet<int> held = new HashSet<int>();
    public Kernel? Core { get; private set; }
    public string Feedback { get; private set; } = "READY";
    public int Run { get; private set; }
    public int HeldCount => held.Count;
    public event Action<string>? Changed;
    public event Action<IReadOnlyList<JudgmentEvent>>? JudgmentsProduced;
    private void PublishJudgments()
    {
        if(Core==null || Core.Judgments.Count==0) return;
        IReadOnlyList<JudgmentEvent> events=Core.Judgments.ToArray();
        if(JudgmentsProduced!=null) foreach(Action<IReadOnlyList<JudgmentEvent>> observer in JudgmentsProduced.GetInvocationList())
            try { observer(events); } catch { /* Diagnostics cannot change gameplay. */ }
    }
    public BgmController? Audio { get; }
    private Action<MusicStartRequest>? requestHandler,anchorHandler;
    private void DetachAudio()
    {
        if(Core==null) return;
        Core.Timeline.MusicStartRequested-=requestHandler;
        Core.Timeline.MusicStartAnchored-=anchorHandler;
    }
    public GameplaySession(IMonotonicClock clock, IBgmBackend? backend=null) { this.clock = clock; if(backend!=null)Audio=new BgmController(backend); }
    public static int LaneForKey(char key) => char.ToUpperInvariant(key) switch
    { 'D' => 2, 'F' => 3, 'J' => 4, 'K' => 5, _ => 0 };
    public static char ResolveKey(long physical, long logical, long unicode)
    {
        // Prefer physical D/F/J/K. Some OS-injected keys have a non-letter
        // physical code but a valid logical key; retain that real event pathway.
        foreach (long code in new[] { physical, logical, (long)unicode })
            if (code <= char.MaxValue && code >= 0 && LaneForKey((char)code) != 0)
                return char.ToUpperInvariant((char)code);
        return '\0';
    }
    public void Start(string aff, int userOffset=0, string chartId="ordinary", string? audioResource=null)
    {
        var chart=Chart.Parse(aff);
        _ = checked(chart.AudioOffset+userOffset);
        ReleaseAll(); DetachAudio(); Audio?.End("restart");
        held.Clear(); Feedback = "READY"; Run++;
        Audio?.Begin(new BgmSession(Run,chartId,audioResource,chart.AudioOffset,userOffset,chart.EndTime));
        // Resource preparation precedes the fresh session's steady-clock origin.
        // Loading time is not hidden compensation or gameplay elapsed time.
        Core = new Kernel(chart, clock.Milliseconds, userOffset);
        var current=Core;int currentRun=Run;
        requestHandler=request => {if(ReferenceEquals(Core,current))Audio?.Request(currentRun,request,current.Timeline);};
        anchorHandler=request => {if(ReferenceEquals(Core,current))Audio?.Anchored(currentRun,request,current.Timeline);};
        Core.Timeline.MusicStartRequested+=requestHandler;
        Core.Timeline.MusicStartAnchored+=anchorHandler;
        Core.Frame(clock.Milliseconds); Changed?.Invoke("START");
    }
    public void Frame()
    {
        if (Core == null || Core.Finished) return;
        Core.Frame(clock.Milliseconds);
        PublishJudgments();
        if (Core.Judgments.Count > 0)
        {
            var last = Core.Judgments.Last();
            Feedback = (last.CheckpointTime.HasValue ? "CHECKPOINT " : "") + last.Outcome.Replace('_', ' ');
        }
        else if (Core.Expired.Count > 0) Feedback = "LOST";
        if (Core.Finished) { Audio?.End("completion"); ReleaseAll(); Changed?.Invoke("RESULT"); }
        else Changed?.Invoke("FRAME");
    }
    public bool Key(char key, bool pressed, bool echo = false)
    {
        int lane = LaneForKey(key); return lane != 0 && Contact(lane, lane, pressed, echo);
    }
    public bool Contact(int pointer, int lane, bool pressed, bool echo = false)
    {
        if (Core == null || lane < 2 || lane > 5 || echo) return false;
        if (pressed)
        {
            if (Core.Finished || !held.Add(pointer)) return false;
            Core.Down(clock.Milliseconds, pointer, lane);
            PublishJudgments();
            foreach (var classification in Core.Classifications)
                if (classification.ConsumesInput) Feedback = classification.Outcome.Replace('_', ' ');
            Changed?.Invoke("DOWN");
        }
        else
        {
            if (!held.Remove(pointer)) return false;
            Core.Up(pointer); Changed?.Invoke("UP");
        }
        return true;
    }
    public bool MoveContact(int pointer, int lane)
    {
        if (Core == null || Core.Finished || !held.Contains(pointer)) return false;
        Core.Move(pointer, lane); Changed?.Invoke("MOVE"); return true;
    }
    public void ReleaseAll()
    {
        if (Core != null)
            foreach (int pointer in held.ToArray()) { Core.Up(pointer); held.Remove(pointer); Changed?.Invoke("CLEANUP_UP"); }
    }
    public void Home() { ReleaseAll(); DetachAudio(); Audio?.End("menu"); Core = null; Feedback = "READY"; Changed?.Invoke("HOME"); }
}
