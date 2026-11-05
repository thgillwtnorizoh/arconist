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
    public GameplaySession(IMonotonicClock clock) { this.clock = clock; }
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
    public void Start(string aff)
    {
        ReleaseAll();
        Core = new Kernel(Chart.Parse(aff), clock.Milliseconds);
        held.Clear(); Feedback = "READY"; Run++;
        Core.Frame(clock.Milliseconds); Changed?.Invoke("START");
    }
    public void Frame()
    {
        if (Core == null || Core.Finished) return;
        Core.Frame(clock.Milliseconds);
        if (Core.Expired.Count > 0) Feedback = "LOST";
        if (Core.Finished) { ReleaseAll(); Changed?.Invoke("RESULT"); }
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
    public void ReleaseAll()
    {
        if (Core != null)
            foreach (int pointer in held.ToArray()) { Core.Up(pointer); held.Remove(pointer); Changed?.Invoke("CLEANUP_UP"); }
    }
    public void Home() { ReleaseAll(); Core = null; Feedback = "READY"; Changed?.Invoke("HOME"); }
}
