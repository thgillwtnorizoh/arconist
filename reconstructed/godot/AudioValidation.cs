using Godot;
using Arconist.Core;
using Arconist.Bridge;
using System.Text.Json;
using System.Text.Json.Nodes;

namespace Arconist.GodotApp;

// Production audio nodes/decoder under headless Godot. Never an audible test.
public static class AudioValidation
{
    private sealed class Clock : IMonotonicClock {public long Milliseconds{get;set;}}
    const string Resource="res://content/audio/clockwork_steps.wav.bytes";
    public static void Run(Node owner,string evidenceDir)
    {
        int passed=0,failed=0;var outcomes=new List<object>();var diagnostics=new List<BgmDiagnostic>();
        var nodes=new List<GodotBgmBackend>();
        void Check(bool v,string text){if(!v)throw new Exception(text);}
        void Test(string name,Action action){try{action();passed++;outcomes.Add(new{name,status="PASS"});GD.Print("PASS R005 "+name);}catch(Exception e){failed++;outcomes.Add(new{name,status="FAIL",error=e.Message});GD.Print("FAIL R005 "+name+": "+e.Message);}}
        GodotBgmBackend Backend(){var b=new GodotBgmBackend();owner.AddChild(b);nodes.Add(b);return b;}
        string Aff(string name="audible_practice.aff")=>Godot.FileAccess.GetFileAsString("res://content/"+name);
        (GameplaySession s,Clock c,GodotBgmBackend b) Session(string name="audible_practice.aff",int user=0,string? resource=Resource)
        {var b=Backend();var c=new Clock();var s=new GameplaySession(c,b);s.Audio!.Diagnostic+=diagnostics.Add;b.Ended+=s.Audio.Finished;s.Start(Aff(name),user,name,resource);return(s,c,b);}
        Test("raw bundled PCM and composition manifest accessible via Godot FileAccess",()=>{
            Check(Godot.FileAccess.FileExists(Resource),"WAV present");var m=JsonNode.Parse(Godot.FileAccess.GetFileAsString("res://content/audio/manifest.json"))!;
            var b=Backend();b.Load(Resource);Check(b.Inspect().ResourceSha256==m["wav_sha256"]!.GetValue<string>()&&b.Inspect().DurationSeconds==32,"hash/length");b.StopAndUnload();
        });
        Test("actual nonlooping AudioStreamWav decoder and player configuration",()=>{
            var b=Backend();b.Load(Resource);var w=(AudioStreamWav)b.Player.Stream;
            Check(w.Format==AudioStreamWav.FormatEnum.Format16Bits&&w.MixRate==22050&&!w.Stereo&&w.LoopMode==AudioStreamWav.LoopModeEnum.Disabled,"decoded PCM");
            Check(!b.Player.Autoplay&&b.Player.MaxPolyphony==1&&!b.Player.Playing&&b.GetChildren().OfType<AudioStreamPlayer>().Count()==1,"no autoplay/single voice");b.StopAndUnload();
        });
        Test("actual Godot player Play reports active and Stop unloads stream",()=>{
            var b=Backend();b.Load(Resource);b.PlayFromStart();Check(b.Player.Playing&&b.Inspect().Playing,"API playback active");b.StopAndUnload();Check(!b.Player.Playing&&b.Player.Stream==null,"stopped/unloaded");
        });
        Test("strict boundary prepares without premature playback",()=>{
            var(s,c,b)=Session();c.Milliseconds=2999;s.Frame();c.Milliseconds=3000;s.Frame();Check(!b.Player.Playing&&s.Audio!.Starts==0,"before/equal");c.Milliseconds=3001;s.Frame();Check(b.Player.Playing&&s.Audio!.Starts==1&&s.Core!.Timeline.EffectiveTime==0,"after");s.Home();
        });
        Test("request precedes compensation with actual Godot backend",()=>{
            var(s,c,b)=Session(user:80);int first=diagnostics.Count;c.Milliseconds=2921;s.Frame();var rows=diagnostics.Skip(first).ToArray();
            var request=rows.Single(d=>d.Kind=="BGM_REQUEST");var anchor=rows.Single(d=>d.Kind=="BGM_ANCHORED");
            Check(request.EffectiveTime==-79&&request.Compensation==0&&anchor.EffectiveTime==-80&&anchor.Compensation==1&&s.Audio!.Starts==1,"native ordering");s.Home();
        });
        Test("AFF120 explicit user-40 and-120 apply through real session",()=>{
            foreach(var pair in new[]{(-40,80),(-120,0)}){var(s,c,b)=Session("audible_aff120.aff",pair.Item1);c.Milliseconds=3001-pair.Item2;s.Frame();Check(s.Core!.Timeline.CombinedOffset==pair.Item2&&s.Core.Timeline.EffectiveTime==-pair.Item2&&b.Player.Playing,"combined offset");s.Home();}
        });
        Test("DOWN startup never substitutes a FRAME",()=>{
            var(s,c,b)=Session();c.Milliseconds=3000;s.Frame();int frame=s.Core!.LastFrameTime;c.Milliseconds=3001;s.Key('D',true);Check(b.Player.Playing&&s.Core.LastFrameTime==frame,"callback order");s.Home();
        });
        Test("repeated frames preserve one Godot start",()=>{
            var(s,c,b)=Session();c.Milliseconds=3001;s.Frame();for(int i=0;i<30;i++)s.Frame();Check(s.Audio!.Requests==1&&s.Audio.Starts==1&&s.Core!.Timeline.StartRequestCount==1,"once");s.Home();
        });
        Test("missing resource is visible and does not claim backend playback",()=>{
            var(s,c,b)=Session(resource:"res://content/audio/not-there.wav");c.Milliseconds=3001;s.Frame();Check(s.Audio!.State=="ERROR"&&s.Audio.Starts==0&&!b.Player.Playing&&s.Core!.Timeline.EffectiveTime==0,"resource error");s.Home();
        });
        Test("invalid existing resource rejected before WAV decoder",()=>{
            var(s,c,b)=Session(resource:"res://content/practice.aff");Check(s.Audio!.State=="ERROR"&&s.Audio.Detail.Contains("PCM16")&&!b.Player.Playing,"invalid resource diagnostic");s.Home();
        });
        Test("restart before request cancels old audio subscription",()=>{
            var(s,c,b)=Session();var old=s.Core!;c.Milliseconds=100;s.Start(Aff(),0,"new",Resource);old.Frame(4000);Check(!b.Player.Playing&&s.Audio!.Starts==0,"old kernel detached");s.Home();
        });
        Test("restart while playing stops old stream and resets start latch",()=>{
            var(s,c,b)=Session();c.Milliseconds=3001;s.Frame();var old=b.Player.Stream;c.Milliseconds=3500;s.Start(Aff(),0,"new",Resource);Check(!b.Player.Playing&&!ReferenceEquals(old,b.Player.Stream)&&!s.Core!.Timeline.MusicStarted,"fresh stream/preroll");c.Milliseconds=6501;s.Frame();Check(b.Player.Playing&&s.Audio!.Starts==1&&s.Run==2,"second session starts once");s.Home();
        });
        Test("menu stops and unloads current BGM",()=>{
            var(s,c,b)=Session();c.Milliseconds=3001;s.Frame();s.Home();Check(!b.Player.Playing&&b.Player.Stream==null&&s.Core==null,"menu cleanup");
        });
        Test("legacy R004 chart choices remain explicitly silent",()=>{
            foreach(var file in new[]{"practice.aff","ordinary_two_tap.aff","mixed_practice.aff","native_hold.aff","hold_first.aff","tap_first.aff"}){var(s,c,b)=Session(file,resource:null);c.Milliseconds=3001;s.Frame();Check(s.Audio!.State=="SILENT"&&!b.Player.Playing,"silent "+file);s.Home();}
        });
        Test("muted real backend preserves chart time and accepted tap",()=>{
            var(s,c,b)=Session();b.Muted=true;c.Milliseconds=3001;s.Frame();c.Milliseconds=5001;s.Frame();s.Key('D',true);Check(s.Core!.Pure==1&&s.Core.Timeline.EffectiveTime==2000&&b.Inspect().Muted,"muted output independent");s.Home();
        });
        Test("full audible chart held/reacquired two-contact session reaches results",()=>{
            var(s,c,b)=Session();c.Milliseconds=3002;s.Frame();var chart=s.Core!.Chart;
            for(int e=1;e<=chart.EndTime+1;e++){
                c.Milliseconds=e+3002;
                foreach(var tap in chart.Taps.Where(t=>t.Time==e)){s.Contact(100+tap.Ordinal,tap.Lane,true);s.Contact(100+tap.Ordinal,tap.Lane,false);}
                foreach(var h in chart.Holds){int p=200+h.Ordinal;
                    if(e==h.Start)s.Contact(p,h.Lane,true);if(e==h.Start+600)s.Contact(p,h.Lane,false);if(e==h.Start+700)s.Contact(p,h.Lane,true);
                    if(e==h.Start+800)s.Contact(p+1000,h.Lane,true);if(e==h.Start+900)s.Contact(p,h.Lane,false);if(e==h.End)s.Contact(p+1000,h.Lane,false);
                }
                s.Frame();
            }
            Check(s.Core.Result!.Pure==chart.JudgmentUnits&&s.Core.Lost==0&&s.HeldCount==0&&s.Audio!.Starts==1&&!b.Player.Playing&&b.Player.Stream==null,"complete result and cleanup");s.Home();
        });
        Test("backend identity and playhead domain are diagnostic only",()=>{
            var(s,c,b)=Session();c.Milliseconds=3002;s.Frame();Check(s.Audio!.LastBackendStatus!.Backend.Contains("driver=")&&s.Audio.LastBackendStatus.ResourceSha256.Length==64,"backend/resource identity");c.Milliseconds=4002;s.Frame();Check(s.Core!.Timeline.EffectiveTime==1000&&s.Core.Timeline.Compensation==2,"steady clock");s.Home();
        });
        foreach(var b in nodes){b.StopAndUnload();owner.RemoveChild(b);b.QueueFree();}
        File.WriteAllText(Path.Combine(evidenceDir,"audio-tests.json"),JsonSerializer.Serialize(new{passed,failed,skipped=0,outcomes,diagnostics,audibility="NOT RUN",hardwareLatency="UNVERIFIED"},new JsonSerializerOptions{WriteIndented=true,PropertyNamingPolicy=JsonNamingPolicy.CamelCase}));
        GD.Print($"R005 headless audio tests: {passed+failed}; passed: {passed}; failed: {failed}; skipped: 0");owner.GetTree().Quit(failed==0?0:1);
    }
}
