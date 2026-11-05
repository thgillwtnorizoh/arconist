using Godot;
using Arconist.Bridge;
using System.Text.Json;

namespace Arconist.GodotApp;

public partial class Main : Control
{
    private sealed class GodotClock : IMonotonicClock { public long Milliseconds => (long)Time.GetTicksMsec(); }
    private readonly GameplaySession session = new(new GodotClock());
    private Font font = null!;
    private Button start = null!, home = null!;
    private OptionButton charts = null!;
    private Label hud = null!, status = null!;
    private string practice = "", reference = "";
    private string evidenceDir = "";
    private StreamWriter? log;
    private long sequence;
    private int mouseLane;
    private readonly Color ink = new("e9eef8"), muted = new("8794b0"), accent = new("b9f56c"), cyan = new("65d9f0");

    public override void _Ready()
    {
        font = ThemeDB.FallbackFont;
        practice = Godot.FileAccess.GetFileAsString("res://content/practice.aff");
        reference = Godot.FileAccess.GetFileAsString("res://content/ordinary_two_tap.aff");
        foreach (string arg in OS.GetCmdlineUserArgs())
            if (arg.StartsWith("--evidence-dir=", StringComparison.Ordinal)) evidenceDir = arg.Substring(15);
        if (evidenceDir.Length == 0) evidenceDir = ProjectSettings.GlobalizePath("user://evidence");
        Directory.CreateDirectory(evidenceDir);
        log = new StreamWriter(Path.Combine(evidenceDir, "session-" + DateTime.UtcNow.ToString("yyyyMMdd-HHmmss") + ".jsonl")) { AutoFlush = true };
        session.Changed += Log;
        charts = new OptionButton { Position = new Vector2(692, 440), Size = new Vector2(320, 44) };
        charts.AddItem("Practice · 16 taps / four lanes"); charts.AddItem("Native reference · two taps"); AddChild(charts);
        start = MakeButton("Start practice", 692, 502, () => Begin());
        home = MakeButton("Back to start", 692, 564, () => session.Home());
        hud = MakeLabel(692, 186, 336, 245, 25);
        status = MakeLabel(692, 115, 340, 65, 29);
        GetWindow().FocusExited += () => session.ReleaseAll();
        GD.Print("ARCONIST_READY Godot=" + Engine.GetVersionInfo()["string"] + " .NET=" + System.Environment.Version + " evidence=" + evidenceDir);
        UpdateHud();
    }
    private Button MakeButton(string text, float x, float y, Action action)
    {
        var button = new Button { Text = text, Position = new Vector2(x,y), Size = new Vector2(320,48), FocusMode = FocusModeEnum.None };
        button.AddThemeFontSizeOverride("font_size", 22); button.Pressed += action; AddChild(button); return button;
    }
    private Label MakeLabel(float x, float y, float w, float h, int size)
    {
        var label = new Label { Position = new Vector2(x,y), Size = new Vector2(w,h), MouseFilter = MouseFilterEnum.Ignore };
        label.AddThemeFontSizeOverride("font_size",size); AddChild(label); return label;
    }
    private void Begin() { session.Start(charts.Selected == 0 ? practice : reference); UpdateHud(); QueueRedraw(); }
    public override void _Process(double delta) { session.Frame(); UpdateHud(); QueueRedraw(); }
    public override void _Input(InputEvent ev)
    {
        if (ev is InputEventKey key)
        {
            GD.Print($"KEY_EVENT logical={(long)key.Keycode} physical={(long)key.PhysicalKeycode} unicode={key.Unicode} pressed={key.Pressed} echo={key.Echo}");
            if (key.Pressed && !key.Echo && key.Keycode == Key.F8) { Capture(); return; }
            char letter = GameplaySession.ResolveKey((long)key.PhysicalKeycode,(long)key.Keycode,key.Unicode);
            if (letter != '\0')
            {
                GD.Print($"GODOT_KEY {letter} {(key.Pressed ? "DOWN" : "UP")} echo={key.Echo}");
                session.Key(letter,key.Pressed,key.Echo);
                GetViewport().SetInputAsHandled();
            }
        }
        if (ev is InputEventMouseButton mouse && mouse.ButtonIndex == MouseButton.Left)
        {
            if (mouse.Pressed && mouse.Position.X >= 72 && mouse.Position.X < 592 && mouse.Position.Y >= 140 && mouse.Position.Y < 665)
            { mouseLane = 2 + (int)((mouse.Position.X-72)/130); session.Contact(100,mouseLane,true); }
            else if (!mouse.Pressed && mouseLane != 0) { session.Contact(100,mouseLane,false); mouseLane = 0; }
        }
    }
    private void UpdateHud()
    {
        var k = session.Core;
        charts.Visible = k == null || k.Finished; start.Visible = charts.Visible;
        home.Visible = k != null && k.Finished;
        start.Text = k == null ? "Start chart" : "Play again";
        if (k == null)
        {
            status.Text = "FIND YOUR RHYTHM";
            hud.Text = "Four lanes. One timing line.\n\nD     F     J     K\n\nPress as each note meets the line.\nA quiet, audio-free practice.";
            hud.AddThemeFontSizeOverride("font_size",21); return;
        }
        hud.AddThemeFontSizeOverride("font_size",25);
        if (k.Result is { } r)
        {
            status.Text = "SESSION COMPLETE";
            hud.Text = $"PURE {r.Pure}   FAR {r.Far}   LOST {r.Lost}\nShining PURE   {r.Shining}\nScore   {r.Score:N0}\nMax combo   {r.MaxCombo}\nFinal health   {r.Health}\nResult category   {r.Category}";
        }
        else
        {
            status.Text = k.Timeline.EffectiveTime < 0 ? $"READY  {Math.Ceiling(-k.Timeline.EffectiveTime/1000.0)}" : session.Feedback;
            hud.Text = $"COMBO   {k.Combo}\nSCORE   {k.Score:N0}\nHEALTH   {k.Health:F1}\n\nPURE {k.Pure}  FAR {k.Far}  LOST {k.Lost}\nTime   {k.Timeline.EffectiveTime/1000.0:F2} s\nContacts   {k.ContactCount}";
        }
    }
    private void Text(string value, float x, float y, int size, Color color) => DrawString(font,new Vector2(x,y),value,HorizontalAlignment.Left,-1,size,color);
    public override void _Draw()
    {
        if (font == null) return;
        DrawRect(new Rect2(0,0,1100,740),new Color("0b1020"));
        Text("ARCONIST",72,64,32,ink); Text("TAP PRACTICE   /   R002",692,60,17,muted);
        Text("D  ·  F  ·  J  ·  K",72,102,19,muted);
        DrawRect(new Rect2(72,140,520,525),new Color("141e32"));
        for (int lane=0;lane<4;lane++)
        {
            float x = 72+lane*130;
            DrawLine(new Vector2(x,140),new Vector2(x,665),new Color("2b3853"),1);
            Text(new[]{"D","F","J","K"}[lane],x+54,648,26,ink);
            Text((lane+2).ToString(),x+59,687,13,muted);
        }
        DrawLine(new Vector2(72,590),new Vector2(592,590),accent,4);
        Text("JUDGMENT LINE",72,721,13,muted);
        Text("Original shapes · shared gameplay core · no audio",692,686,14,muted);
        var k = session.Core;
        if (k != null)
        {
            int e = k.Timeline.EffectiveTime;
            foreach (var note in k.Notes)
            {
                if (note.Consumed || note.Missed) continue;
                float y = 590 - (note.Data.Time-e)*0.18f;
                if (y<140 || y>610) continue;
                float x = 72+(note.Data.Lane-2)*130+10;
                DrawRect(new Rect2(x,y-10,110,20),cyan);
                DrawLine(new Vector2(x+5,y-7),new Vector2(x+105,y-7),ink,2);
            }
            float progress = Math.Clamp((float)e/k.Chart.EndTime,0,1);
            DrawRect(new Rect2(72,120,520,4),new Color("2b3853")); DrawRect(new Rect2(72,120,520*progress,4),accent);
            if (k.Result != null)
            { Text("CHART FINISHED",178,350,29,accent); Text("Your next run starts fresh.",162,393,20,muted); }
        }
        else
        {
            Text("READY WHEN YOU ARE",139,350,26,accent);
            Text("Choose a chart and press Start.",134,395,20,muted);
        }
    }
    private void Log(string kind)
    {
        var k=session.Core;
        log?.WriteLine(JsonSerializer.Serialize(new { sequence=++sequence, run=session.Run, kind,
            wall=(long)Time.GetTicksMsec(), e=k?.Timeline.EffectiveTime, lastFrame=k?.LastFrameTime,
            pure=k?.Pure,far=k?.Far,lost=k?.Lost,shining=k?.Shining,score=k?.Score,combo=k?.Combo,maxCombo=k?.MaxCombo,
            health=k?.Health,contacts=k?.ContactCount,held=session.HeldCount,finished=k?.Finished,
            candidates=k?.Candidates.ToArray(),classifications=k?.Classifications.ToArray(),expired=k?.Expired.ToArray(),
            notes=k?.Notes.Select(n=>new { id=n.Data.Id, consumed=n.Consumed,missed=n.Missed,active=n.Active,contact=n.Contact }).ToArray(),result=k?.Result }));
    }
    private async void Capture()
    {
        await ToSignal(RenderingServer.Singleton,RenderingServer.SignalName.FramePostDraw);
        string path=Path.Combine(evidenceDir,$"run{session.Run}-{DateTime.UtcNow:HHmmssfff}.png");
        Error error=GetViewport().GetTexture().GetImage().SavePng(path); GD.Print($"VIEWPORT_CAPTURE {error} {path}");
    }
    public override void _ExitTree() { session.ReleaseAll(); log?.Dispose(); }
}
