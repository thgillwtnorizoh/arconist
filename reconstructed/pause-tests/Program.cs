using Arconist.Core;
using Arconist.Bridge;
using Arconist.Headless;
using System.Text.Json;
using System.Text.Json.Nodes;
using System.Security.Cryptography;
using System.Text;
sealed class Clock : IMonotonicClock {public long Milliseconds{get;set;}}
sealed class Audio : IPausableBgmBackend
{
    public bool Playing,Paused,FailPause,FailSeek,FailUnpause;
    public int Starts;public double Position;public readonly List<string> Calls=new();
    public void Load(string r){Calls.Add("load");}
    public void PlayFromStart(){Starts++;Playing=true;Paused=false;Calls.Add("start");}
    public void StopAndUnload(){Playing=false;Paused=false;Calls.Add("stop");}
    public BgmStatus Inspect()=>new(Playing,Position,32,"fake engineering output",paused:Paused);
    public void PausePlayback(){Calls.Add("pause:true");if(FailPause)throw new Exception("injected pause failure");Paused=true;}
    public void SeekMilliseconds(int p){Calls.Add("seek:"+p);if(FailSeek)throw new Exception("injected seek failure");Position=p/1000.0;}
    public void UnpausePlayback(){Calls.Add("pause:false");Paused=false;if(FailUnpause)throw new Exception("injected unpause failure");}
}
static class Tests
{
    static string root="",output="";static int count,failed;static JsonNode native=null!;static readonly List<object> traces=new();
    const string Resource="res://content/audio/clockwork_steps.wav.bytes";
    const string Hold="AudioOffset:0\nTimingPointDensityFactor:1.0\n-\ntiming(0,120.00,4.00);hold(1000,2000,3);";
    static void Check(bool b,string s){if(!b)throw new Exception(s);}
    static void Test(string name,Action action){count++;try{action();Console.WriteLine("PASS R006 "+name);}catch(Exception e){failed++;Console.WriteLine("FAIL R006 "+name+": "+e.Message);}}
    static (GameplaySession s,Clock c,Audio a) Session(string aff=Hold,int user=0,string? resource=Resource)
    {var c=new Clock{Milliseconds=6450};var a=new Audio();var s=new GameplaySession(c,a);s.Start(aff,user,"test",resource);return(s,c,a);}
    static object Snapshot(Kernel k)=>new{e=k.Timeline.EffectiveTime,k.Pure,k.Far,k.Lost,k.Shining,k.Score,k.Combo,k.MaxCombo,health=(double)k.Health,contacts=k.Contacts,holds=k.Holds.Select(h=>new{h.Latched,h.Holding,h.ActivatingContacts,h.Records}),k.Finished,k.Result};
    static void NativeClock(Kernel k,string key)
    {var x=native[key]!;Check(k.Timeline.RawTime==x["r"]!.GetValue<int>()&&k.Timeline.PauseReference==x["p"]!.GetValue<int>()&&k.Timeline.Compensation==x["c"]!.GetValue<int>()&&k.Timeline.EffectiveTime==x["e"]!.GetValue<int>(),"native R/P/C/E "+key);}
    static string RunNative(string history)
    {
        var(s,c,a)=Session();var ledger=new List<JudgmentEvent>();var events=new List<object>();s.JudgmentsProduced+=x=>ledger.AddRange(x);
        void Frame(int e,int delay=0){c.Milliseconds=9452L+e+delay;s.Frame();events.Add(new{kind="FRAME",wall=c.Milliseconds,r=s.Core!.Timeline.RawTime,p=s.Core.Timeline.PauseReference,c=s.Core.Timeline.Compensation,state=Snapshot(s.Core)});}
        Frame(0);Frame(1000);s.Contact(42,4,true);Check(s.Core!.Contacts.Single().Id==0&&!s.Core.Holds[0].Holding,"initial identity/latch only");Frame(1001);Frame(1125);
        int delay=history=="control"?0:60000;
        Frame(1200);
        if(delay!=0){Check(s.Pause(),"pause accepted");NativeClock(s.Core,"pause");if(history=="up")s.Contact(42,4,false);if(history=="cancel")s.Cancel(42);
            c.Milliseconds+=60000;s.FocusReturned();Check(s.Core.Paused&&s.PauseModalActive,"foreground remains paused");Frame(1200,delay);NativeClock(s.Core,"compensated");
            Check(!s.Core.Holds[0].Holding&&s.Core.Holds[0].Latched&&s.Core.Pure==1,"paused activity/latch/record");
            Check(s.Resume(),"explicit resume");NativeClock(s.Core,"compensated");Check(!s.PauseModalActive&&a.Calls.TakeLast(3).SequenceEqual(new[]{"pause:true","seek:1200","pause:false"}),"request ledger/dismissal");
        }
        Frame(1201,delay);if(delay!=0)NativeClock(s.Core,"next");
        Check(s.Core.Holds[0].Holding==(history=="control"||history=="retained"),"retained versus actually released");
        c.Milliseconds=9452+1300+delay;
        if(history=="up"||history=="cancel"){Check(s.Contact(43,4,true),"new DOWN reaches after modal dismissal");Check(s.Core.Contacts.Single().Id==1&&!s.Core.Holds[0].Holding,"fresh ID/reacquire no frame");}
        Frame(1301,delay);Frame(1375,delay);Frame(1625,delay);
        foreach(var row in native["checkpoints"]!.AsArray()){
            int e=row!["e"]!.GetValue<int>();var ev=events.Select(x=>JsonSerializer.SerializeToNode(x,Replay.JsonOptions)!).Last(x=>x["state"]!["e"]!.GetValue<int>()==e)["state"]!;
            foreach(string key in new[]{"pure","shining","combo","score","health"})Check(Replay.FirstDifference(row[key],ev[key],key)==null,$"native {e}/{key}");
            Check(ledger.Count(x=>x.CheckpointTime==row["record"]!.GetValue<int>()&&x.EffectiveTime==e)==1,"unique record identity/time");
        }
        Check(s.Core.Far==0&&s.Core.Lost==0&&ledger.Count==3,"native no misses/duplicates");
        c.Milliseconds=9452+1626+delay;s.Contact(history is "up" or "cancel"?43:42,4,false);Frame(1627,delay);
        Check(s.Core.Holds[0].Latched&&!s.Core.Holds[0].Holding&&s.Core.ContactCount==0&&s.Core.Result==null,"native terminal scope");
        string? firstDifference=null;traces.Add(new{history,events,ledger,audio=a.Calls,firstDifference});
        Frame(2501,delay);Check(s.Core.Finished&&s.HeldCount==0,"engineering completion extension");return JsonSerializer.Serialize(s.Core.Result,Replay.JsonOptions);
    }
    static string Mixed(bool interrupted)
    {
        string aff=File.ReadAllText(Path.Combine(root,"reconstructed/godot/content/audible_practice.aff"));var(s,c,a)=Session(aff);c.Milliseconds=9452;s.Frame();int delay=0;
        using var trace=IncrementalHash.CreateHash(HashAlgorithmName.SHA256);
        for(int e=1;e<=s.Core!.Chart.EndTime+1;e++){
            c.Milliseconds=9452+e+delay;
            if(interrupted&&(e==8500||e==16000)){s.Pause();c.Milliseconds+=60000;delay+=60000;s.Frame();Check(s.Resume(),"mixed resume");}
            foreach(var t in s.Core.Chart.Taps.Where(t=>t.Time==e)){s.Contact(100+t.Ordinal,t.Lane,true);s.Contact(100+t.Ordinal,t.Lane,false);}
            foreach(var h in s.Core.Chart.Holds){int p=200+h.Ordinal;if(e==h.Start)s.Contact(p,h.Lane,true);if(e==h.Start+600)s.Contact(p,h.Lane,false);if(e==h.Start+700)s.Contact(p,h.Lane,true);if(e==h.Start+800)s.Contact(p+1000,h.Lane,true);if(e==h.Start+900)s.Contact(p,h.Lane,false);if(e==h.End)s.Contact(p+1000,h.Lane,false);}
            s.Frame();trace.AppendData(Encoding.UTF8.GetBytes(JsonSerializer.Serialize(Snapshot(s.Core),Replay.JsonOptions)));
        }
        Check(s.Core.Result!.Pure==86&&s.Core.Lost==0&&a.Starts==1&&!a.Playing&&s.HeldCount==0,"mixed units/results/audio");return Convert.ToHexString(trace.GetHashAndReset());
    }
    public static int Main(string[] args)
    {
        if(args.Length!=2)return 1;root=Path.GetFullPath(args[0]);output=Path.GetFullPath(args[1]);Directory.CreateDirectory(output);native=JsonNode.Parse(File.ReadAllText(Path.Combine(root,"reference_traces/r006/native-interruption.json")))!;
        string? control=null;
        Test("A E041 uninterrupted control",()=>control=RunNative("control"));
        foreach(string h in new[]{"retained","up","cancel"})Test("E041 "+h+" sixty-second interruption",()=>Check(RunNative(h)==control,"cross-run cached result"));
        Test("fixture identity remains the original native hold",()=>Check(Convert.ToHexString(SHA256.HashData(File.ReadAllBytes(Path.Combine(root,"research_harness/fixtures/native_hold.aff")))).ToLowerInvariant()==native["fixtureSha256"]!.GetValue<string>(),"fixture SHA"));
        Test("paused frame prevents expiry checkpoint result and counters",()=>{var(s,c,a)=Session();c.Milliseconds=9452;s.Frame();c.Milliseconds=10652;s.Frame();s.Pause();var k=s.Core!;string records=JsonSerializer.Serialize(new{k.Score,k.Combo,k.Health,k.Lost,k.Pure,k.Holds[0].Records});c.Milliseconds+=86400000;s.Frame();Check(k.Timeline.EffectiveTime==1200&&!k.Finished&&records==JsonSerializer.Serialize(new{k.Score,k.Combo,k.Health,k.Lost,k.Pure,k.Holds[0].Records}),"frozen for a day");});
        Test("paused core DOWN rejects before identity and timeline refresh",()=>{var k=new Kernel(Chart.Parse(Hold));k.Frame(3002);k.Pause(4202);int r=k.Timeline.RawTime;k.Down(90000,42,4);Check(k.ContactCount==0&&k.Timeline.RawTime==r&&k.Judgments.Count==0,"core gate");k.Resume(90000);k.Down(90100,42,4);Check(k.Contacts.Single().Id==0,"blocked DOWN did not allocate ID");});
        Test("paused adapter rejects echo new keyboard mouse and movement",()=>{var(s,c,a)=Session();s.Pause();Check(!s.Key('J',true)&&!s.Contact(100,4,true)&&!s.MoveContact(100,3)&&s.HeldCount==0,"modal gate");});
        Test("UP during pause reuses pointer with fresh logical identity",()=>{var(s,c,a)=Session();c.Milliseconds=9452;s.Frame();c.Milliseconds=10452;s.Frame();s.Key('J',true);s.Pause();s.Key('J',false);Check(s.HeldCount==0&&s.Core!.Holds[0].Latched,"UP/latch");c.Milliseconds+=60000;s.Resume();c.Milliseconds+=100;s.Key('J',true);Check(s.Core!.Contacts.Single().Id==1,"same pointer fresh ID");});
        Test("CANCEL is distinct idempotent cleanup without judgment",()=>{var(s,c,a)=Session();c.Milliseconds=9452;s.Frame();c.Milliseconds=10452;s.Frame();s.Key('J',true);s.Pause();Check(s.Cancel(4)&&!s.Cancel(4)&&s.Core!.ContactCount==0&&s.Core.Judgments.Count==0&&s.Core.Holds[0].Latched,"cancel");});
        Test("two contacts partial release during pause retains other identity",()=>{var(s,c,a)=Session();c.Milliseconds=9452;s.Frame();c.Milliseconds=10452;s.Frame();s.Key('J',true);s.Contact(100,4,true);c.Milliseconds++;s.Frame();s.Pause();s.Cancel(100);c.Milliseconds+=60000;s.Frame();s.Resume();c.Milliseconds++;s.Frame();Check(s.Core!.Holds[0].ActivatingContacts.SequenceEqual(new[]{0}),"remaining key");});
        Test("both released contacts never resurrect on resume",()=>{var(s,c,a)=Session();c.Milliseconds=9452;s.Frame();c.Milliseconds=10452;s.Frame();s.Key('J',true);s.Contact(100,4,true);s.Pause();s.CancelAll("test");c.Milliseconds+=60000;s.Resume();c.Milliseconds++;s.Frame();Check(s.HeldCount==0&&s.Core!.ContactCount==0&&!s.Core.Holds[0].Holding,"no fabricated physical input");});
        foreach(int o in new[]{-120,0,120,200})Test("offset-aware seek O"+o,()=>{var(s,c,a)=Session(user:o);c.Milliseconds=9452-o;s.Frame();c.Milliseconds=10452;s.Frame();s.Pause();c.Milliseconds+=60000;s.Resume();Check(a.Calls.Contains("seek:"+(1000+o))&&s.Core!.Timeline.EffectiveTime==1000,"E-B");});
        Test("E preroll pause no seek unpause or premature start",()=>{var(s,c,a)=Session();c.Milliseconds=7450;s.Frame();s.Pause();c.Milliseconds+=60000;s.Frame();Check(s.Core!.Timeline.EffectiveTime==-2000&&a.Starts==0,"frozen preroll");s.Resume();Check(!a.Calls.Any(x=>x.StartsWith("seek")||x=="pause:false"),"no started branch");c.Milliseconds+=2000;s.Frame();Check(a.Starts==0,"strict equality");c.Milliseconds++;s.Frame();Check(a.Starts==1&&s.Core.Timeline.EffectiveTime==0,"strict crossing");});
        Test("pause itself may cross ordinary startup before audio pause",()=>{var(s,c,a)=Session();c.Milliseconds=9460;s.Pause();Check(a.Calls.TakeLast(2).SequenceEqual(new[]{"start","pause:true"})&&s.Core!.Timeline.EffectiveTime==0,"old-state update then pause");});
        Test("duplicate transitions add no operations or chart advance",()=>{var(s,c,a)=Session();c.Milliseconds=9452;s.Frame();c.Milliseconds=10652;s.Pause();int n=a.Calls.Count;for(int i=0;i<5;i++){c.Milliseconds+=1000;Check(!s.Pause(),"duplicate pause");}Check(a.Calls.Count==n,"no duplicated pause");s.Resume();n=a.Calls.Count;int e=s.Core!.Timeline.EffectiveTime;for(int i=0;i<5;i++){c.Milliseconds++;Check(!s.Resume(),"duplicate resume");}Check(n==a.Calls.Count&&e==s.Core.Timeline.EffectiveTime,"no duplicate seek/unpause/update");});
        Test("negative modal control remains blocked after model-only resume",()=>{var(s,c,a)=Session(resource:null);s.Pause();s.Core!.Resume(c.Milliseconds);Check(s.PauseModalActive&&!s.Key('J',true),"modal must be dismissed too");});
        Test("positive explicit dismissal restores fresh DOWN",()=>{var(s,c,a)=Session();s.Pause();Check(s.Resume()&&!s.PauseModalActive&&s.Key('J',true),"input restored");});
        Test("focus loss cancels contacts and foreground never resumes",()=>{var(s,c,a)=Session();s.Key('J',true);s.FocusLost();c.Milliseconds+=60000;s.FocusReturned();s.Frame();Check(s.Core!.Paused&&s.HeldCount==0&&s.Core.ContactCount==0&&s.PauseModalActive,"Windows policy");});
        Test("seek failure preserves frozen clock modal and supports retry",()=>{var(s,c,a)=Session();c.Milliseconds=9452;s.Frame();c.Milliseconds=10652;s.Pause();a.FailSeek=true;c.Milliseconds+=60000;Check(!s.Resume()&&s.Core!.Paused&&s.PauseModalActive&&s.Audio!.State=="ERROR"&&a.Paused,"safe seek failure");Check(s.Core!.Timeline.EffectiveTime==1200,"clock intact");a.FailSeek=false;c.Milliseconds+=1000;Check(s.Resume()&&s.Core.Timeline.EffectiveTime==1200,"retry");});
        Test("unpause failure re-pauses backend and leaves gameplay frozen",()=>{var(s,c,a)=Session();c.Milliseconds=9452;s.Frame();s.Pause();a.FailUnpause=true;c.Milliseconds+=60000;Check(!s.Resume()&&s.Core!.Paused&&a.Paused&&s.PauseModalActive,"safe unpause failure");a.FailUnpause=false;Check(s.Resume(),"retry");});
        Test("pause backend failure stops sound and freezes gameplay",()=>{var(s,c,a)=Session();c.Milliseconds=9452;s.Frame();a.FailPause=true;s.Pause();Check(s.Core!.Paused&&!a.Playing&&s.Audio!.State=="ERROR"&&!s.Resume(),"restart-required state");s.Home();Check(s.Core==null,"menu recovery");
            var(pre,pc,pa)=Session();pa.FailPause=true;pre.Pause();pc.Milliseconds+=60000;
            Check(!pre.Resume()&&pre.Core!.Paused&&pre.PauseModalActive,"failed preroll pause requires fresh run");});
        Test("missing music cannot masquerade as synchronized resume",()=>{var(s,c,a)=Session(resource:"bad");c.Milliseconds=9452;s.Frame();s.Pause();Check(!s.Resume()&&s.Core!.Paused,"explicit missing output failure");});
        Test("full mixed chart two pauses matches every effective frame",()=>Check(Mixed(false)==Mixed(true),"full trace comparison"));
        Test("menu restart after paused run clears every pause state",()=>{var(s,c,a)=Session();s.Pause();s.Home();s.Start(Hold,0,"fresh",Resource);Check(!s.PauseModalActive&&!s.Core!.Paused&&!s.Core.Timeline.Paused&&s.HeldCount==0&&!s.Core.Timeline.MusicStarted,"fresh state");});
        Test("finished cached result cannot be paused or resumed",()=>{var(s,c,a)=Session();c.Milliseconds=9452;s.Frame();c.Milliseconds=12000;s.Frame();var r=s.Core!.Result;Check(!s.Pause()&&!s.Resume()&&ReferenceEquals(r,s.Core.Result),"result cache");});
        File.WriteAllText(Path.Combine(output,"pause-tests.json"),JsonSerializer.Serialize(new{count,passed=count-failed,failed,skipped=0,traces},Replay.JsonOptions));Console.WriteLine($"R006 pause tests: {count}; passed: {count-failed}; failed: {failed}; skipped: 0");return failed==0?0:1;
    }
}
