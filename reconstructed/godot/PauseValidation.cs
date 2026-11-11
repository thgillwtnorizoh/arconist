using Godot;
using Arconist.Core;
using Arconist.Bridge;
using System.Text.Json;
namespace Arconist.GodotApp;

// Headless production nodes and modal binding only; no OS/UI input or listening.
public static class PauseValidation
{
    sealed class Clock:IMonotonicClock{public long Milliseconds{get;set;}}
    const string Resource="res://content/audio/clockwork_steps.wav.bytes";
    public static async void Run(Node owner,string evidenceDir)
    {
        int passed=0,failed=0;var outcomes=new List<object>();var diagnostics=new List<BgmDiagnostic>();var nodes=new List<Node>();
        void Check(bool b,string text){if(!b)throw new Exception(text);}
        void Test(string name,Action action){try{action();passed++;outcomes.Add(new{name,status="PASS"});GD.Print("PASS R006 "+name);}catch(Exception e){failed++;outcomes.Add(new{name,status="FAIL",error=e.Message});GD.Print("FAIL R006 "+name+": "+e.Message);}}
        (GameplaySession s,Clock c,GodotBgmBackend b,PausePanel panel) Session(int offset=0,string file="native_hold.aff")
        {
            var b=new GodotBgmBackend();owner.AddChild(b);nodes.Add(b);var c=new Clock();var s=new GameplaySession(c,b);b.Ended+=s.Audio!.Finished;s.Audio.Diagnostic+=diagnostics.Add;
            var panel=new PausePanel();owner.AddChild(panel);nodes.Add(panel);panel.Bind(s);s.Changed+=_=>panel.Sync();
            s.Start(Godot.FileAccess.GetFileAsString("res://content/"+file),offset,file,Resource);return(s,c,b,panel);
        }
        Test("production stream pause keeps loaded stream without restarting",()=>{var(s,c,b,p)=Session();c.Milliseconds=3002;s.Frame();var stream=b.Player.Stream;c.Milliseconds=4202;s.Pause();Check(b.Player.StreamPaused&&ReferenceEquals(stream,b.Player.Stream)&&s.Audio!.Starts==1&&s.Core!.Paused,"pause state");s.Home();});
        Test("modal and model timeline states are distinct observable gates",()=>{var(s,c,b,p)=Session();s.Pause();Check(p.Visible&&p.MouseFilter==Control.MouseFilterEnum.Stop&&p.ResumeButton.Visible&&p.MenuButton.Visible&&s.Core!.ModelPaused&&s.Core.Timeline.Paused,"actual node/gates");Check(!s.Contact(100,4,true),"modal blocks pointer");p.Menu();});
        Test("preroll explicit resume avoids seek and preserves strict startup",()=>{var(s,c,b,p)=Session();c.Milliseconds=1000;s.Frame();s.Pause();c.Milliseconds+=60000;s.Frame();int before=diagnostics.Count;p.Resume();Check(!p.Visible&&!s.Core!.Timeline.MusicStarted&&!b.Player.Playing,"preroll");Check(!diagnostics.Skip(before).Any(d=>d.Kind=="BGM_SEEK_REQUEST"||d.Kind=="BGM_UNPAUSE_REQUEST"),"no music branch");c.Milliseconds+=2000;s.Frame();Check(!b.Player.Playing,"equality");c.Milliseconds++;s.Frame();Check(b.Player.Playing&&s.Audio!.Starts==1,"strict start");s.Home();});
        Test("sixty-second retained contact activates after explicit resume",()=>{var(s,c,b,p)=Session();c.Milliseconds=3002;s.Frame();c.Milliseconds=4002;s.Frame();s.Key('J',true);c.Milliseconds=4127;s.Frame();c.Milliseconds=4202;s.Frame();s.Pause();int id=s.Core!.Contacts.Single().Id;c.Milliseconds+=60000;s.Frame();s.FocusReturned();Check(s.Core.Paused&&s.Core.Timeline.EffectiveTime==1200&&!s.Core.Holds[0].Holding&&s.Core.Contacts.Single().Id==id&&b.Player.StreamPaused,"frozen");p.Resume();c.Milliseconds++;s.Frame();Check(s.Core.Timeline.EffectiveTime==1201&&s.Core.Holds[0].ActivatingContacts.Contains(id)&&!p.Visible,"recovery");c.Milliseconds=3002+60000+1375;s.Frame();c.Milliseconds=3002+60000+1625;s.Frame();Check(s.Core.Pure==3&&s.Core.Score==10000003&&(double)s.Core.Health==80.5999984741211,"native checkpoints");s.Home();});
        foreach(bool cancel in new[]{false,true})Test((cancel?"CANCEL":"UP")+" during modal allows fresh replacement after dismissal",()=>{var(s,c,b,p)=Session();c.Milliseconds=3002;s.Frame();c.Milliseconds=4002;s.Frame();s.Key('J',true);s.Pause();if(cancel)s.Cancel(4);else s.Key('J',false);c.Milliseconds+=60000;s.Frame();Check(!s.Contact(100,4,true),"blocked while modal");p.Resume();c.Milliseconds+=300;s.Contact(100,4,true);Check(s.Core!.Contacts.Single().Id==1&&s.Core.Holds[0].Latched&&!p.Visible,"fresh input restored");s.Home();});
        Test("remaining keyboard contact survives mouse cancellation during pause",()=>{var(s,c,b,p)=Session();c.Milliseconds=3002;s.Frame();c.Milliseconds=4002;s.Frame();s.Key('J',true);s.Contact(100,4,true);s.Pause();s.Cancel(100);c.Milliseconds+=60000;s.Frame();p.Resume();c.Milliseconds++;s.Frame();Check(s.Core!.Holds[0].ActivatingContacts.SequenceEqual(new[]{0}),"partial release");s.Home();});
        Test("negative control model-only resume leaves modal blocking input",()=>{var(s,c,b,p)=Session();s.Pause();s.Core!.Resume(c.Milliseconds);Check(p.Visible&&s.PauseModalActive&&!s.Key('J',true),"modal omission reproduced as negative control");s.Home();});
        Test("actual Resume button binding dismisses and restores new input",()=>{var(s,c,b,p)=Session();s.Pause();p.ResumeButton.EmitSignal(BaseButton.SignalName.Pressed);Check(!s.Core!.Paused&&!p.Visible&&s.Key('J',true),"button binding restores routing");s.Home();});
        Test("actual menu binding stops unloads and clears paused state",()=>{var(s,c,b,p)=Session();c.Milliseconds=3002;s.Frame();s.Pause();p.MenuButton.EmitSignal(BaseButton.SignalName.Pressed);Check(s.Core==null&&!p.Visible&&!b.Player.Playing&&b.Player.Stream==null,"menu binding");});
        Test("focus loss cancellation and gain preserve explicit-resume policy",()=>{var(s,c,b,p)=Session();s.Key('J',true);s.FocusLost();c.Milliseconds+=60000;s.FocusReturned();s.Frame();Check(s.Core!.Paused&&p.Visible&&s.Core.ContactCount==0,"focus policy");p.Resume();Check(!p.Visible,"explicit dismissal");s.Home();});
        Test("duplicate actions produce one pause seek and unpause",()=>{var(s,c,b,p)=Session();c.Milliseconds=3002;s.Frame();int n=diagnostics.Count;s.Pause();s.Pause();c.Milliseconds+=60000;p.Resume();p.Resume();var rows=diagnostics.Skip(n).ToArray();Check(rows.Count(d=>d.Kind=="BGM_PAUSE_REQUEST")==1&&rows.Count(d=>d.Kind=="BGM_SEEK_REQUEST")==1&&rows.Count(d=>d.Kind=="BGM_UNPAUSE_REQUEST")==1,"idempotent ledger");s.Home();});
        Test("mixed audible completion pause replay and chart switch",()=>{var(s,c,b,p)=Session(file:"audible_practice.aff");c.Milliseconds=3002;s.Frame();int delay=0;for(int e=1;e<=s.Core!.Chart.EndTime+1;e++){c.Milliseconds=3002+e+delay;if(e==8500){s.Pause();c.Milliseconds+=60000;delay+=60000;s.Frame();Check(p.Resume(),"resume");}foreach(var t in s.Core.Chart.Taps.Where(t=>t.Time==e)){s.Contact(100+t.Ordinal,t.Lane,true);s.Contact(100+t.Ordinal,t.Lane,false);}foreach(var h in s.Core.Chart.Holds){int pointer=200+h.Ordinal;if(e==h.Start)s.Contact(pointer,h.Lane,true);if(e==h.End)s.Contact(pointer,h.Lane,false);}s.Frame();}Check(s.Core.Result!.Pure==86&&s.Core.Lost==0&&!b.Player.Playing&&b.Player.Stream==null,"mixed completion");s.Home();s.Start(Godot.FileAccess.GetFileAsString("res://content/audible_aff120.aff"),-120,"replay",Resource);Check(!s.Core!.Paused&&!s.PauseModalActive&&!b.Player.Playing&&s.HeldCount==0&&s.Audio!.Starts==0,"fresh replay");s.Home();});
        // Audio thread needs real time to acknowledge a queued seek. This is an
        // API position probe under Dummy, not a hardware/perceptual assertion.
        foreach(int offset in new[]{-120,0,120})
        {
            var(s,c,b,p)=Session(offset);c.Milliseconds=3002-offset;s.Frame();
            await owner.ToSignal(owner.GetTree().CreateTimer(0.05),SceneTreeTimer.SignalName.Timeout);
            c.Milliseconds=4002;s.Frame();s.Pause();c.Milliseconds+=60000;s.Frame();
            bool resumed=p.Resume();b.PausePlayback();
            await owner.ToSignal(owner.GetTree().CreateTimer(0.05),SceneTreeTimer.SignalName.Timeout);
            Test("actual queued seek readback O"+offset,()=>{Check(resumed&&b.Inspect().SeekReadbackSeconds.HasValue&&Math.Abs(b.Inspect().SeekReadbackSeconds!.Value-(1000+offset)/1000.0)<=1.0/22050&&Math.Abs(b.Inspect().PositionSeconds-(1000+offset)/1000.0)<0.02,"Godot PCM seek position "+b.Inspect().PositionSeconds);Check(diagnostics.Any(d=>d.Session.Id==s.Run&&d.Kind=="BGM_SEEK_REQUEST"&&d.SeekMilliseconds==1000+offset),"logical requested ms");});
            s.Home();
        }
        {
            var(s,c,b,p)=Session();c.Milliseconds=3002;s.Frame();
            await owner.ToSignal(owner.GetTree().CreateTimer(0.05),SceneTreeTimer.SignalName.Timeout);
            s.Pause();
            await owner.ToSignal(owner.GetTree().CreateTimer(0.05),SceneTreeTimer.SignalName.Timeout);
            Test("seek flushes old PCM resampler history against fresh target decode",()=>{
                b.SeekMilliseconds(1120);AudioServer.Lock();
                try
                {
                    using var fresh=b.Player.Stream.InstantiatePlayback();fresh.Start(1.120);
                    var expected=fresh.MixAudio(1,128);var actual=b.Player.GetStreamPlayback().MixAudio(1,128);
                    Check(actual.Length==128&&actual.SequenceEqual(expected),"target PCM frames must match independently positioned decoder");
                }
                finally {AudioServer.Unlock();}
            });s.Home();
        }
        foreach(var n in nodes){if(n is GodotBgmBackend b)b.StopAndUnload();owner.RemoveChild(n);n.QueueFree();}
        await owner.ToSignal(owner.GetTree().CreateTimer(0.1),SceneTreeTimer.SignalName.Timeout);
        File.WriteAllText(Path.Combine(evidenceDir,"pause-tests.json"),JsonSerializer.Serialize(new{passed,failed,skipped=0,outcomes,diagnostics,physicalAudio="NOT RUN",hardwareLatency="UNVERIFIED"},new JsonSerializerOptions{WriteIndented=true,PropertyNamingPolicy=JsonNamingPolicy.CamelCase}));
        GD.Print($"R006 headless pause tests: {passed+failed}; passed: {passed}; failed: {failed}; skipped: 0");owner.GetTree().Quit(failed==0?0:1);
    }
}
