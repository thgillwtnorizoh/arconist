using Arconist.Core;

namespace Arconist.Bridge;

public sealed class BgmStatus
{
    public bool Playing { get; }
    public double PositionSeconds { get; }
    public double DurationSeconds { get; }
    public string Backend { get; }
    public bool Muted { get; }
    public string ResourceSha256 { get; }
    public BgmStatus(bool playing, double position, double duration, string backend, bool muted=false, string resourceSha256="")
    { Playing=playing; PositionSeconds=position; DurationSeconds=duration; Backend=backend; Muted=muted; ResourceSha256=resourceSha256; }
}

// Engineering output port. Its diagnostic playhead is never an input to Timeline.
public interface IBgmBackend
{
    void Load(string resource);
    void PlayFromStart();
    void StopAndUnload();
    BgmStatus Inspect();
}

public sealed class BgmSession
{
    public int Id { get; }
    public string Chart { get; }
    public string? Resource { get; }
    public int AffOffset { get; }
    public int UserOffset { get; }
    public int CombinedOffset => checked(AffOffset+UserOffset);
    public int ChartEnd { get; }
    public BgmSession(int id,string chart,string? resource,int aff,int user,int chartEnd)
    { Id=id;Chart=chart;Resource=resource;AffOffset=aff;UserOffset=user;ChartEnd=chartEnd; }
}

public sealed class BgmDiagnostic
{
    public string Kind { get; }
    public BgmSession Session { get; }
    public string State { get; }
    public string Detail { get; }
    public MusicStartRequest? Request { get; }
    public int? RawTime { get; }
    public int? Compensation { get; }
    public int? EffectiveTime { get; }
    public int RequestCount { get; }
    public int PlayAttempts { get; }
    public int AcceptedStarts { get; }
    public string ClockDomain => "request wall: supplied monotonic session clock ms; R/C/E: kernel ms; backend position: audio seconds (diagnostic only)";
    public BgmStatus? BackendStatus { get; }
    public BgmDiagnostic(string kind,BgmSession session,string state,string detail,MusicStartRequest? request,Timeline? t,BgmStatus? backend,int requests,int attempts,int starts)
    {Kind=kind;Session=session;State=state;Detail=detail;Request=request;RawTime=t?.RawTime;Compensation=t?.Compensation;EffectiveTime=t?.EffectiveTime;BackendStatus=backend;RequestCount=requests;PlayAttempts=attempts;AcceptedStarts=starts;}
}

public sealed class BgmController
{
    private readonly IBgmBackend backend;
    public BgmSession? Session { get; private set; }
    public string State { get; private set; } = "IDLE";
    public string Detail { get; private set; } = "";
    public int Requests { get; private set; }
    public int PlayAttempts { get; private set; }
    public int Starts { get; private set; }
    public BgmStatus? LastBackendStatus { get; private set; }
    public event Action<BgmDiagnostic>? Diagnostic;
    private bool prepared, stopped=true;
    public BgmController(IBgmBackend backend) { this.backend=backend; }
    private void Emit(string kind,MusicStartRequest? request=null,Timeline? timeline=null)
    {
        try { LastBackendStatus=backend.Inspect(); } catch(Exception e) { Detail="Backend status unavailable: "+e.Message; }
        if(Session==null) return;
        // Observational logging cannot interrupt playback cleanup or gameplay.
        var d=new BgmDiagnostic(kind,Session,State,Detail,request,timeline,LastBackendStatus,Requests,PlayAttempts,Starts);
        if(Diagnostic!=null) foreach(Action<BgmDiagnostic> observer in Diagnostic.GetInvocationList())
            try { observer(d); } catch { /* A diagnostic sink cannot own game time. */ }
    }
    public void Begin(BgmSession session)
    {
        bool safe=End("replace");Session=session;Requests=0;Starts=0;PlayAttempts=0;prepared=false;
        if(!safe) {State="ERROR";Detail="Previous playback cleanup failed; new playback blocked.";Emit("BGM_ERROR");return;}
        State="SILENT";Detail="No soundtrack assigned to this preserved chart.";
        if(string.IsNullOrEmpty(session.Resource)) {Emit("BGM_PREPARE");return;}
        try
        {
            if(!session.Resource.StartsWith("res://",StringComparison.Ordinal)) throw new ArgumentException("Audio must use an explicit bundled res:// resource.");
            stopped=false; backend.Load(session.Resource);
            var status=backend.Inspect();
            if(!double.IsFinite(status.DurationSeconds) || status.DurationSeconds <= 0 ||
               status.DurationSeconds*1000 < (long)session.ChartEnd+session.CombinedOffset)
                throw new ArgumentException("Soundtrack is invalid or ends before the chart's logical music position.");
            prepared=true;State="READY";Detail="Bundled stream loaded; waiting for strict kernel request.";Emit("BGM_PREPARE");
        }
        catch(Exception e) { State="ERROR";Detail=e.Message;Emit("BGM_ERROR"); }
    }
    public void Request(int sessionId,MusicStartRequest request,Timeline timeline)
    {
        if(Session?.Id!=sessionId || stopped && State!="SILENT" && State!="ERROR") return;
        Requests++;
        if(Requests!=1) {State="ERROR";Detail="Duplicate start request rejected.";Emit("BGM_ERROR",request,timeline);return;}
        Emit("BGM_REQUEST",request,timeline);
        if(State=="SILENT" || !prepared) return;
        try
        {
            PlayAttempts++;backend.PlayFromStart();
            var status=backend.Inspect();
            if(!status.Playing) throw new InvalidOperationException("Backend did not report an active playback after Play.");
            Starts++;State="API_PLAYING";Detail="Godot API reports playback; audible output/latency unverified.";Emit("BGM_BACKEND_ACCEPTED",request,timeline);
        }
        catch(Exception e) {State="ERROR";Detail=e.Message;Emit("BGM_ERROR",request,timeline);End("failed start", preserveError:true);}
    }
    public void Anchored(int sessionId,MusicStartRequest request,Timeline timeline)
    {if(Session?.Id==sessionId)Emit("BGM_ANCHORED",request,timeline);}
    public void Finished()
    {
        if(Session==null || stopped) return;
        State="ERROR";Detail="Audio backend ended before session completion; gameplay clock unchanged.";Emit("BGM_EARLY_FINISH");
    }
    public bool End(string reason,bool preserveError=false)
    {
        if(stopped) return true;
        try {backend.StopAndUnload();stopped=true;prepared=false;if(!preserveError){State="STOPPED";Detail=reason;}Emit("BGM_STOP");return true;}
        catch(Exception e) {State="ERROR";Detail="Audio cleanup failed: "+e.Message;Emit("BGM_ERROR");return false;}
    }
}
