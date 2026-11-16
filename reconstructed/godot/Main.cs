using Godot;
using Arconist.Bridge;
using Arconist.Core;
using System.Text.Json;

namespace Arconist.GodotApp;

public partial class Main : Control
{
    private sealed class GodotClock : IMonotonicClock { public long Milliseconds => (long)Time.GetTicksMsec(); }
    private GameplaySession session = null!;
    private GodotBgmBackend bgm = null!;
    private PausePanel pausePanel = null!;
    private Button pauseButton = null!;
    private SpinBox userOffset = null!;
    private Label audioStatus = null!;
    private Font font = null!;
    private SpatialTrack track = null!;
    private SubViewport viewport3D = null!;
    private readonly Vector2 trackOrigin = new(40,130);
    private readonly Vector2 trackSize = new(610,550);
    private Button start = null!, home = null!;
    private OptionButton charts = null!;
    private Label hud = null!, status = null!, holdStatus = null!, chartInfo = null!;
    private readonly List<string> chartData = new();
    private static readonly (string file, string title, string description, string? audio, bool mixed)[] ChartChoices = {
        ("s01_mixed.aff", "S01 · Mixed ordinary gameplay / N38", "F hold + curved mouse4–6.5s.\nGold click9s; linked mouse12–14s.\nCrossing L+R16s; reverse20.3s.", "res://content/audio/clockwork_steps.wav.bytes", true),
        ("s01_crossing.aff", "S01 · E028 two-contact crossing", "L+R mouse: two actual contacts.\nFollow sky targets1–2s. Native N6.\nSeparate diagnostic; silent.", null, true),
        ("s01_grouped.aff", "S01 · Grouped long-note diagnostic", "Group1 F hold + mouse curve4–6s.\nSingle judgment clock; separate depth.\nRelease both after6s.", null, true),
        ("grouped_practice.aff", "R010 · Independent reverse practice", "K + D at HUD5.5s. Pink D reverses5.2s.\nCyan K: default group. Pink D: group1.\nSilent N2; release after each input.", null, false),
        ("native_timing_group.aff", "E029 · Independent +120/+60 control", "K then D at HUD1.5s. N2.\nIndependent timing, shared judgment E.\nCyan K / pink D reach line together.", null, false),
        ("native_reverse_scroll.aff", "E029 · Reverse +60/-60 comparison", "K then D at HUD1.5s. N2.\nPink D reverses direction at1.2s.\nExisting admission survives depth>300.", null, false),
        ("native_noinput_group.aff", "E036 · noinput comparison / N1", "Grey D is visible but cannot judge/miss.\nTry D then K at HUD1.5s. Only K scores.\nTwo runtime taps; one judgment unit.", null, false),
        ("linked_practice.aff", "R009 · Connected ordinary arc practice", "Hold left mouse4–12s, same target.\nJunction8.001s: keep it held.\nGold x2 record resolves7.375s. N31.", null, false),
        ("native_linked_arc_successors.aff", "E038 · Natural linked pair / N7", "Hold mouse1–3s. Junction2.001s.\nNo second DOWN. Weight2 at1.375s.\nNative N7; Godot referenceH500.", null, false),
        ("arctap_practice.aff", "R008 · Trace parent + arc-tap practice", "D2s, K2.5s. Click gold sky child6s.\nGrey trace is not a hold. Release.\nF10s, J10.5s. Silent chart.", null, false),
        ("native_arc_tap.aff", "E025 · One arc-tap / H500 diagnostic", "Click gold child at1.5s.\nTwo fresh clicks: only one award.\nOriginal fixture; Godot height500.", null, false),
        ("sky_practice.aff", "R007 · Ordinary sky arc practice", "D2s, K2.5s. Hold left mouse,\nfollow white sky target4–12s.\nF14s, J14.5s. Silent chart.", null, false),
        ("native_moving_arc.aff", "E028 · Moving arc diagnostic / H500", "Native E028 chart bytes.\nGodot reference uses height500.\nHold mouse / follow target1–2s.", null, false),
        ("audible_practice.aff", "R005 · Clockwork Steps / 120 BPM", "One bar of audible count-in, then D.\nPositive offset: notes occur later.\nHold/repress J at8–11s.", "res://content/audio/clockwork_steps.wav.bytes", false),
        ("audible_aff120.aff", "R005 · AFF +120 offset diagnostic", "Same music/chart, AFF offset +120.\nUser -120 cancels it (combined0).\nUser -40 gives combined +80.", "res://content/audio/clockwork_steps.wav.bytes", false),
        ("mixed_practice.aff", "R004 mixed taps + holds", "F 4–6.5s: release / press again.\nJ 8–11s: key + mouse, release J.\nKeep mouse pressed near the line.", null, false),
        ("practice.aff", "Original practice · 16 taps", "Original R002/R003 chart.\nD / F / J / K: tap and release.\nMouse: click lane near green line.", null, false),
        ("ordinary_two_tap.aff", "Native reference · two taps", "Two taps: J at1s, F at2s.\nRelease between inputs.\nOriginal reference bytes preserved.", null, false),
        ("native_hold.aff", "E026 · J hold 1–2 seconds", "Hold J, briefly release, press again.\nFor two contacts: J + left mouse.\nRelease one; keep the other held.", null, false),
        ("hold_first.aff", "E037 · hold first / tap blocked", "Earlier J hold blocks the1.25s tap.\nTry J + mouse, then release one.\nNative target: PURE3 / LOST1.", null, false),
        ("tap_first.aff", "E037 · tap first / two contacts", "Near1s: press J, then mouse on J.\nRelease mouse; keep J held.\nNative target: PURE4 / shining3.", null, false)
    };
    private string evidenceDir = "";
    private StreamWriter? log;
    private long sequence;
    private SpatialContactAdapter pointers=null!;
    private readonly Color ink = new("e9eef8"), muted = new("8794b0"), accent = new("b9f56c"), cyan = new("65d9f0");

    public override void _Ready()
    {
        font = ThemeDB.FallbackFont;
        bgm = new GodotBgmBackend(); AddChild(bgm);
        session = new GameplaySession(new GodotClock(), bgm);
        bgm.Ended += () => session.Audio?.Finished();
        var container = new SubViewportContainer { Position=trackOrigin, Size=trackSize, Stretch=true, MouseFilter=MouseFilterEnum.Ignore };
        viewport3D = new SubViewport { Size=(Vector2I)trackSize, OwnWorld3D=true, RenderTargetUpdateMode=SubViewport.UpdateMode.Always, HandleInputLocally=false };
        container.AddChild(viewport3D); AddChild(container);
        track = new SpatialTrack(); viewport3D.AddChild(track);
        pointers=new SpatialContactAdapter(session,track);
        foreach (var choice in ChartChoices)
            chartData.Add(Godot.FileAccess.GetFileAsString("res://content/" + choice.file));
        foreach (string arg in OS.GetCmdlineUserArgs())
            if (arg.StartsWith("--evidence-dir=", StringComparison.Ordinal)) evidenceDir = arg.Substring(15);
        if (evidenceDir.Length == 0) evidenceDir = ProjectSettings.GlobalizePath("user://evidence");
        Directory.CreateDirectory(evidenceDir);
        log = new StreamWriter(Path.Combine(evidenceDir, "session-" + DateTime.UtcNow.ToString("yyyyMMdd-HHmmss") + ".jsonl")) { AutoFlush = true };
        session.Changed += Log;
        pausePanel=new PausePanel();AddChild(pausePanel);pausePanel.Bind(session);
        session.Changed += kind => {
            pausePanel.Sync();
            if(kind=="RESUME_ACCEPTED" && pointers.Count!=0)
            {
                // Reproject the genuinely retained mouse at its current position;
                // a modal move must not leave stale pre-pause lane support.
                Vector2 local=(GetViewport().GetMousePosition()-trackOrigin)*(Vector2)viewport3D.Size/trackSize;
                ReprojectMouse(GetViewport().GetMousePosition());
            }
        };
        session.JudgmentsProduced += events => log?.WriteLine(JsonSerializer.Serialize(new {
            kind="JUDGMENTS",run=session.Run,chart=session.Audio?.Session?.Chart,
            wall=(long)Time.GetTicksMsec(),clockDomain="Godot monotonic wall ms; authoritative judgment E ms",events }));
        session.Audio!.Diagnostic += d => log?.WriteLine(JsonSerializer.Serialize(d, new JsonSerializerOptions { PropertyNamingPolicy=JsonNamingPolicy.CamelCase }));
        MakeLabel(692, 82, 210, 26, 16).Text="User offset (ms):";
        userOffset = new SpinBox { Position=new Vector2(900,77),Size=new Vector2(112,32),MinValue=-500,MaxValue=500,Step=1,Value=0 };
        userOffset.TooltipText="Applied to the next run. Positive values delay chart-effective time relative to music. AFF offset is added.";
        AddChild(userOffset);
        audioStatus=MakeLabel(692,162,336,23,15);
        charts = new OptionButton { Position = new Vector2(692, 440), Size = new Vector2(320, 44) };
        foreach (var choice in ChartChoices) charts.AddItem(choice.title);
        AddChild(charts);
        chartInfo = MakeLabel(692, 620, 330, 64, 16);
        chartInfo.Text = ChartChoices[0].description; chartInfo.AutowrapMode=TextServer.AutowrapMode.WordSmart;
        charts.ItemSelected += index => chartInfo.Text = ChartChoices[(int)index].description;
        holdStatus = MakeLabel(692, 402, 336, 32, 18);
        start = MakeButton("Start practice", 692, 502, () => Begin());
        home = MakeButton("Back to start", 692, 564, () => session.Home());
        hud = MakeLabel(692, 186, 336, 245, 25);
        status = MakeLabel(692, 115, 340, 44, 24);
        pauseButton=new Button {Text="Pause (Esc/P)",Position=new Vector2(500,75),Size=new Vector2(150,36),FocusMode=FocusModeEnum.None};
        pauseButton.Pressed+=()=>session.Pause();AddChild(pauseButton);
        GetWindow().FocusExited += () => {session.FocusLost();pointers.Forget();};
        GetWindow().FocusEntered += () => session.FocusReturned();
        if (OS.GetCmdlineUserArgs().Contains("--mixed-tests")) CallDeferred(nameof(RunMixedTests));
        if (OS.GetCmdlineUserArgs().Contains("--group-tests")) CallDeferred(nameof(RunGroupTests));
        if (OS.GetCmdlineUserArgs().Contains("--linked-tests")) CallDeferred(nameof(RunLinkedTests));
        if (OS.GetCmdlineUserArgs().Contains("--arctap-tests")) CallDeferred(nameof(RunArcTapTests));
        if (OS.GetCmdlineUserArgs().Contains("--arc-tests")) CallDeferred(nameof(RunArcTests));
        if (OS.GetCmdlineUserArgs().Contains("--spatial-tests")) CallDeferred(nameof(RunSpatialTests));
        if (OS.GetCmdlineUserArgs().Contains("--hold-tests")) CallDeferred(nameof(RunHoldTests));
        if (OS.GetCmdlineUserArgs().Contains("--pause-tests")) CallDeferred(nameof(RunPauseTests));
        if (OS.GetCmdlineUserArgs().Contains("--audio-tests")) CallDeferred(nameof(RunAudioTests));
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
    private void Begin()
    {
        pointers.Forget();chartInfo.Text=ChartChoices[charts.Selected].description;
        try { session.Start(chartData[charts.Selected],(int)userOffset.Value,ChartChoices[charts.Selected].file,ChartChoices[charts.Selected].audio,profile:ChartChoices[charts.Selected].mixed?ChartProfile.S01Mixed:ChartProfile.R010); }
        catch(Exception e) { chartInfo.Text="Start error: "+e.Message; GD.Print("SESSION_CONFIGURATION_ERROR "+e.Message); }
        UpdateHud(); QueueRedraw();
    }
    private Vector2 Local(Vector2 screen)=>(screen-trackOrigin)*(Vector2)viewport3D.Size/trackSize;
    private void ReprojectMouse(Vector2 screen)=>pointers.MoveMouse(Local(screen));
    public override void _Process(double delta)
    { if(!session.PauseModalActive)pointers.MoveMouse(Local(GetViewport().GetMousePosition()));session.Frame();pointers.Prune();track.Refresh(session.Core);UpdateHud();QueueRedraw(); }
    public override void _Input(InputEvent ev)
    {
        if (ev is InputEventKey key)
        {
            GD.Print($"KEY_EVENT logical={(long)key.Keycode} physical={(long)key.PhysicalKeycode} unicode={key.Unicode} pressed={key.Pressed} echo={key.Echo}");
            if (key.Pressed && !key.Echo && key.Keycode == Key.F6) { track.SetView(!track.AlternateView); LogSpatial("CAMERA"); return; }
            if (key.Pressed && !key.Echo && key.Keycode == Key.F7) { GetWindow().Size = GetWindow().Size.X == 1100 ? new Vector2I(1320,888) : new Vector2I(1100,740); LogSpatial("RESIZE"); return; }
            if (key.Pressed && !key.Echo && key.Keycode == Key.F8) { Capture(); return; }
            if(key.Pressed && !key.Echo && (key.Keycode==Key.Escape || key.Keycode==Key.P))
            {session.Pause();GetViewport().SetInputAsHandled();return;}
            if(key.Pressed && !key.Echo && key.Keycode==Key.R && session.PauseModalActive)
            {pausePanel.Resume();GetViewport().SetInputAsHandled();return;}
            char letter = GameplaySession.ResolveKey((long)key.PhysicalKeycode,(long)key.Keycode,key.Unicode);
            if (letter != '\0')
            {
                GD.Print($"GODOT_KEY {letter} {(key.Pressed ? "DOWN" : "UP")} echo={key.Echo}");
                session.Key(letter,key.Pressed,key.Echo);
                GetViewport().SetInputAsHandled();
            }
        }
        // Real UP/CANCEL always cleans contacts, including under the modal.
        if(ev is InputEventMouseButton button&&(button.ButtonIndex==MouseButton.Left||button.ButtonIndex==MouseButton.Right))
        {
            int id=button.ButtonIndex==MouseButton.Left?100:101;
            if(!button.Pressed)pointers.Release(id);
            else if(!session.PauseModalActive)pointers.Press(id,Local(button.Position),button.ButtonIndex==MouseButton.Right);
            return;
        }
        if(ev is InputEventScreenTouch touch)
        {
            int id=1000+touch.Index;
            if(touch.Canceled)pointers.Release(id,true);
            else if(!touch.Pressed)pointers.Release(id);
            else if(!session.PauseModalActive)pointers.Press(id,Local(touch.Position));
            return;
        }
        if(session.PauseModalActive)return;
        if(ev is InputEventMouseMotion motion)pointers.MoveMouse(Local(motion.Position));
        if(ev is InputEventScreenDrag drag)pointers.Move(1000+drag.Index,Local(drag.Position));
    }
    private void UpdateHud()
    {
        var k = session.Core;
        pauseButton.Visible=k!=null&&!k.Finished&&!session.PauseModalActive;
        pausePanel.Sync();
        var audio=session.Audio!;
        audioStatus.Text=audio.State switch {"API_PLAYING"=>"Music playing", "READY"=>"Music ready — waiting for start", "ERROR"=>"MUSIC ERROR — see guide", "STOPPED"=>"Music stopped", "PAUSED"=>"Music paused", _=>"Silent chart"};
        audioStatus.TooltipText=audio.Detail+"\n"+audio.LastBackendStatus?.Backend;
        audioStatus.Modulate=new Color(audio.State=="ERROR"?"ff6985":"b9f56c");
        if(audio.State=="ERROR") {chartInfo.Text=audio.Detail;chartInfo.TooltipText=audio.Detail;}
        userOffset.Editable=k==null||k.Finished;
        holdStatus.Visible = k != null && !k.Finished && (k.Holds.Count > 0||k.Arcs.Count>0);
        if (holdStatus.Visible)
        {
            var hold = k!.Holds.FirstOrDefault(h => h.Holding) ?? k.Holds.FirstOrDefault(h => h.End > k.Timeline.EffectiveTime);
            if(k.Chart.Profile==ChartProfile.S01Mixed){double e=k.Timeline.EffectiveTime/1000.0;holdStatus.Text=e<4?"D/F/J/K · then F + mouse4s":e<6.5?"Hold F + follow curved target":e<10?"Click gold sky child at9s":e<14.1?"Hold mouse12–14s · junction13.001":e<18?"Crossing16–17s · hold L+R mouse":e<21?"Reverse D + K at20.3s":"F21.5s (grey D disabled) · J24s";}
            else if(k.Chart.TimingGroups.Count>1){var n=k.Notes.First(t=>t.TimingGroupId==1);holdStatus.Text=$"G0 K / G1 D · {(n.InputEnabled?"INPUT ON":"NOINPUT")} · Z {n.Depth}";}
            else if(k.ArcGroups.Count>0){var group=k.ArcGroups[0];int junction=group.Members[1].Start;holdStatus.Text=$"CHAIN {(group.Active?"ON":"OFF")} · SEG {(k.Timeline.EffectiveTime<junction?1:2)} · JUNCTION {junction/1000.0:F3}s";}
            else if(k.ArcTaps.Count>0){var child=k.ArcTaps.First();holdStatus.Text=$"ARC-TAP {(child.Consumed?"HIT":child.Missed?"MISS":"READY")}   at {child.Data.Time/1000.0:F2}s";}
            else if(k.Arcs.Count>0){var arc=k.Arcs.FirstOrDefault(a=>a.Holding)??k.Arcs.First();holdStatus.Text=$"ARC {(arc.Holding?"ON":"OFF")} owner {arc.Color.Owner} units {arc.Records.Count(r=>r.Resolved)}/{arc.Records.Count}";}
            else holdStatus.Text = hold == null ? "HOLDS COMPLETE" : $"HOLD {(hold.Holding ? "ON" : "OFF")}   contacts {hold.ActivatingContacts.Count}   units {hold.Records.Count(r=>r.Resolved)}/{hold.Records.Count}";
        }
        charts.Visible = k == null || k.Finished; start.Visible = charts.Visible;
        home.Visible = k != null && k.Finished;
        start.Text = k == null ? "Start chart" : "Play again";
        if (k == null)
        {
            status.Text = "FIND YOUR RHYTHM";
            hud.Text = "D     F     J     K\n\nCyan: tap and release.\nAmber: hold the key.\nGreen: hold contact active.\n\nKey + mouse = two contacts.\nChoose audible or silent practice.";
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
            status.Text = k.Paused ? "PAUSED" : k.Timeline.EffectiveTime < 0 ? $"READY  {Math.Ceiling(-k.Timeline.EffectiveTime/1000.0)}" : session.Feedback;
            hud.Text = $"COMBO   {k.Combo}\nSCORE   {k.Score:N0}\nHEALTH   {k.Health:F1}\n\nPURE {k.Pure}  FAR {k.Far}  LOST {k.Lost}\nTime   {k.Timeline.EffectiveTime/1000.0:F2} s\nContacts   {k.ContactCount}";
        }
    }
    private void Text(string value, float x, float y, int size, Color color) => DrawString(font,new Vector2(x,y),value,HorizontalAlignment.Left,-1,size,color);
    public override void _Draw()
    {
        if (font == null) return;
        DrawRect(new Rect2(665,0,435,740),new Color("0b1020"));
        Text("ARCONIST",72,64,32,ink); Text("S01   /   MIXED GAMEPLAY",692,60,17,muted);
        Text("D  ·  F  ·  J  ·  K",72,102,19,muted);
        Text("Native coordinates / 425   |   perspective Camera3D",52,713,15,muted);
        Text("F6 view   F7 resize   F8 capture",692,686,15,muted);
    }
    private void RunMixedTests()=>MixedValidation.Run(this,track,evidenceDir);
    private void RunGroupTests()=>GroupValidation.Run(this,track,evidenceDir);
    private void RunLinkedTests()=>LinkedValidation.Run(this,track,evidenceDir);
    private void RunArcTapTests()=>ArcTapValidation.Run(this,track,evidenceDir);
    private void RunArcTests()=>ArcValidation.Run(this,track,evidenceDir);
    private void RunPauseTests() => PauseValidation.Run(this,evidenceDir);
    private void RunAudioTests() => AudioValidation.Run(this, evidenceDir);
    private void RunHoldTests() => HoldValidation.Run(this, track, evidenceDir);
    private void RunSpatialTests() => SpatialValidation.Run(this,track,evidenceDir);
    private void LogSpatial(string kind)
    {
        var centers=Enumerable.Range(2,4).Select(lane => {
            var p=track.Camera.UnprojectPosition(SpatialTrack.World(SpatialTrack.NativeX(lane),0,0));
            return new { lane, x=p.X+trackOrigin.X,y=p.Y+trackOrigin.Y };
        }).ToArray();
        log?.WriteLine(JsonSerializer.Serialize(new { kind, view=track.AlternateView, viewport=new[]{viewport3D.Size.X,viewport3D.Size.Y}, centers }));
    }    private void Log(string kind)
    {
        var k=session.Core;
        log?.WriteLine(JsonSerializer.Serialize(new { sequence=++sequence, run=session.Run, kind,
            wall=(long)Time.GetTicksMsec(), clockDomain="Godot monotonic ticks ms / kernel E ms", e=k?.Timeline.EffectiveTime, lastFrame=k?.LastFrameTime,
            r=k?.Timeline.RawTime,p=k?.Timeline.PauseReference,c=k?.Timeline.Compensation,effective=k?.Timeline.EffectiveTime,o=k?.Timeline.CombinedOffset,b=k?.Timeline.MusicAnchor,
            modelPaused=k?.ModelPaused,timelinePaused=k?.Timeline.Paused,modal=session.PauseModalActive,pauseReason=session.PauseReason,requests=k?.Timeline.StartRequestCount,
            audioState=session.Audio?.State, audioDetail=session.Audio?.Detail, audioSession=session.Audio?.Session,
            pure=k?.Pure,far=k?.Far,lost=k?.Lost,shining=k?.Shining,score=k?.Score,combo=k?.Combo,maxCombo=k?.MaxCombo,
            health=k?.Health,contacts=k?.ContactCount,held=session.HeldCount,finished=k?.Finished,
            holds=k?.Holds.Select(h=>new { id=h.Data.Id, h.Active, h.Latched, h.Holding, h.ActivatingContacts, h.Records }).ToArray(),
            arcs=k?.Arcs.Select(a=>new{a.Id,a.Active,a.Depth,a.Cache,a.CacheEnabled,a.TargetX,a.TargetY,a.Holding,a.Records,a.ResolutionWrites,generationFlag=a.Data.GenerationFlag,predecessor=a.Predecessor?.Id,successors=a.Successors.Select(next=>next.Id),group=a.Group?.Id,a.SuccessorCleanupPreserved,a.LastLinkScan,trace=a.Data.Trace,children=a.Children.Select(c=>new{c.Id,c.ParentId,time=c.Data.Time,c.Local,c.InputTarget,c.WorldPosition,c.Consumed,c.Missed,c.Contact,c.Outcome,c.ResolvedAt})}),colors=k?.Colors,claimed=k?.ClaimedIds,
            profile=k?.Chart.Profile.ToString(),proximity=k?.ProximityTrace,
            groups=k?.ArcGroups.Select(g=>new{g.Id,g.Active,g.CacheRelated,g.Accepted,g.Window,g.TimestampHistory,g.WindowBehavior,members=g.Members.Select(a=>a.Id)}),recorder=k?.RecorderTrace,recorderCalls=k?.RecorderCalls,
            timingGroups=k?.TimingGroups.Select(g=>new{g.Id,g.Definition.SourceOrder,g.Definition.Attribute,g.Definition.InputEnabled,g.Definition.LifetimeEnd,g.Active,g.QueryLow,g.QueryHigh,g.FrameOffset,g.Records,g.Index}),requestedSpeed=k?.RequestedSpeed,metadataBpm=k?.MetadataBpm,effectiveSpeed=k?.EffectiveSpeed,
            retained=k?.Contacts, judgments=k?.Judgments.ToArray(),
            candidates=k?.Candidates.ToArray(),classifications=k?.Classifications.ToArray(),expired=k?.Expired.ToArray(),
            notes=k?.Notes.Select(n=>new { id=n.Data.Id,group=n.TimingGroupId,n.InputEnabled,timing=n.Data.Timing.SourceOrder,n.PreDepth,n.Bucket, consumed=n.Consumed,missed=n.Missed,active=n.Active,contact=n.Contact,depth=SpatialTrack.CurrentDepth(k!,n),visible=SpatialTrack.Present(k!,n) }).ToArray(),result=k?.Result }));
    }
    private async void Capture()
    {
        await ToSignal(RenderingServer.Singleton,RenderingServer.SignalName.FramePostDraw);
        string path=Path.Combine(evidenceDir,$"run{session.Run}-{DateTime.UtcNow:HHmmssfff}.png");
        LogSpatial("CAPTURE_GEOMETRY");
        Error error=GetViewport().GetTexture().GetImage().SavePng(path); GD.Print($"VIEWPORT_CAPTURE {error} {path}");
    }
    public override void _ExitTree() { session?.Home(); log?.Dispose(); }
}
