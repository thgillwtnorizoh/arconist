using Arconist.Core;
using Arconist.Bridge;
using Arconist.Headless;
using System.Text.Json;
using System.Security.Cryptography;
using System.Text;
using System.Text.Json.Nodes;

sealed class Clock : IMonotonicClock { public long Milliseconds {get;set;} }
sealed class FakeBgm : IBgmBackend
{
    public int Loads,Plays,Stops,Active,PeakActive;
    public Action? OnLoad;
    public bool FailLoad,FailPlay,RejectPlay,FailStop,Muted;
    public double Position,Duration=32;
    public void Load(string r){Loads++;OnLoad?.Invoke();if(FailLoad)throw new Exception("missing resource");}
    public void PlayFromStart(){Plays++;if(FailPlay)throw new Exception("playback failed");if(!RejectPlay){Active++;PeakActive=Math.Max(PeakActive,Active);}}
    public void StopAndUnload(){Stops++;if(FailStop)throw new Exception("cleanup failed");Active=0;}
    public BgmStatus Inspect()=>new(Active>0,Position,Duration,"deterministic test backend (not sound output)",Muted);
}
static class Tests
{
    static int count,failed;static string root="",output="";static readonly List<object> traces=new();
    const string Resource="res://content/audio/clockwork_steps.wav.bytes";
    const string Single="AudioOffset:0\n-\ntiming(0,120.00,4.00);(1500,3);";
    static void Check(bool b,string s){if(!b)throw new Exception(s);}
    static void Test(string n,Action a){count++;try{a();Console.WriteLine("PASS R005 "+n);}catch(Exception e){failed++;Console.WriteLine("FAIL R005 "+n+": "+e.Message);}}
    static string Read(string p)=>File.ReadAllText(Path.Combine(root,p));
    static (GameplaySession s,Clock c,FakeBgm b) Session(string? aff=null,int user=0,FakeBgm? b=null,string? resource=Resource)
    {var c=new Clock();b??=new();var s=new GameplaySession(c,b);s.Start(aff??Single,user,"test-chart",resource);return(s,c,b);}
    static object State(Kernel k)=>new{k.Timeline.RawTime,k.Timeline.Compensation,k.Timeline.EffectiveTime,k.LastFrameTime,k.Pure,k.Far,k.Lost,k.Shining,k.Score,k.Combo,k.MaxCombo,k.Health,k.ContactCount,k.Result,holds=k.Holds.Select(h=>new{h.Latched,h.Holding,h.Records})};
    static string Complete(string aff,FakeBgm b)
    {
        var(s,c,_)=Session(aff,b:b);using var trace=IncrementalHash.CreateHash(HashAlgorithmName.SHA256);c.Milliseconds=3002;s.Frame();
        for(int e=1;e<=s.Core!.Chart.EndTime+1;e++)
        {
            c.Milliseconds=e+3002;
            foreach(var t in s.Core.Chart.Taps.Where(t=>t.Time==e)){s.Contact(100+t.Ordinal,t.Lane,true);s.Contact(100+t.Ordinal,t.Lane,false);}
            foreach(var h in s.Core.Chart.Holds){int p=200+h.Ordinal;
                if(e==h.Start)s.Contact(p,h.Lane,true);
                if(e==h.Start+600)s.Contact(p,h.Lane,false);
                if(e==h.Start+700)s.Contact(p,h.Lane,true);
                if(e==h.Start+800)s.Contact(p+1000,h.Lane,true);
                if(e==h.Start+900)s.Contact(p,h.Lane,false);
                if(e==h.End)s.Contact(p+1000,h.Lane,false);
            }
            s.Frame();trace.AppendData(Encoding.UTF8.GetBytes(JsonSerializer.Serialize(State(s.Core),Replay.JsonOptions)));
        }
        Check(s.Core.Result!.Pure==s.Core.Chart.JudgmentUnits&&s.Core.Lost==0&&s.HeldCount==0,"all tap/hold units and contacts");
        Check(b.Active==0&&b.PeakActive<=1&&s.Audio!.Requests==1,"cleanup/no overlap/request");
        return JsonSerializer.Serialize(State(s.Core),Replay.JsonOptions)+Convert.ToHexString(trace.GetHashAndReset());
    }
    public static int Main(string[] args)
    {
        if(args.Length!=2)return 1;root=Path.GetFullPath(args[0]);output=Path.GetFullPath(args[1]);Directory.CreateDirectory(output);
        var refs=JsonNode.Parse(Read("reference_traces/r005/native-offsets.json"))!;
        foreach(var row in refs["cases"]!.AsArray())Test("native E040 "+row!["name"]!.GetValue<string>(),()=>{
            int aff=row["aff"]!.GetValue<int>(),user=row["selectedUser"]!.GetValue<int>(),o=row["o"]!.GetValue<int>();
            long origin=6450;var k=new Kernel(Chart.Parse(Single.Replace("AudioOffset:0","AudioOffset:"+aff)),origin,user);
            var seen=new List<object>();k.Timeline.MusicStartRequested+=r=>{
                Check(k.Timeline.MusicStarted&&k.Timeline.Compensation==0,"latch before request/C after");
                Check(r.RawTime==row["requestR"]!.GetValue<int>()&&r.EffectiveTimeBefore==row["requestE"]!.GetValue<int>(),"native request entry");seen.Add(r);
            };
            k.Frame(origin+3000-o-1);Check(!k.Timeline.MusicStarted,"before");k.Frame(origin+3000-o);Check(!k.Timeline.MusicStarted,"equality");
            long requestWall=origin+3001-o;k.Frame(requestWall);
            Check(k.Timeline.Compensation==row["postC"]!.GetValue<int>()&&k.Timeline.EffectiveTime==row["postE"]!.GetValue<int>(),"anchor");
            k.Frame(requestWall+1500);Check(k.Timeline.EffectiveTime==row["at1500E"]!.GetValue<int>(),"equal elapsed");
            long aligned=requestWall+row["alignedElapsed"]!.GetValue<int>();k.Frame(aligned);k.Down(aligned,42,4);
            var actual=JsonSerializer.SerializeToNode(new{k.Pure,k.Far,k.Lost,k.Shining,k.Combo,k.Score,health=(double)k.Health},Replay.JsonOptions);
            string? diff=Replay.FirstDifference(refs["alignedJudgment"],actual,row["name"]!.GetValue<string>());
            Check(diff==null,diff??"");k.Up(42);k.Frame(aligned+1);Check(k.Timeline.StartRequestCount==1&&seen.Count==1&&k.ContactCount==0,"once/cleanup");
            traces.Add(new{name=row["name"]!.GetValue<string>(),source=row["source"]!.GetValue<string>(),requests=seen,actual,firstDifference=diff});
        });
        foreach(int o in new[]{-500,-100,0,100,500})Test("E005 strict threshold offset "+o,()=>{
            var t=new Timeline(0,0,o);int calls=0;t.MusicStartRequested+=r=>calls++;
            t.Update(2999-o);Check(!t.MusicStarted,"before");t.Update(3000-o);Check(!t.MusicStarted,"equal");t.Update(3001-o);
            Check(calls==1&&t.EffectiveTime==-o&&t.Compensation==1&&t.MusicAnchor==-o,"after");t.Update(4501-o);Check(t.EffectiveTime==1500-o,"progress");
        });
        Test("large startup jump discards overshoot once",()=>{
            var t=new Timeline(0,120,80);int n=0;t.MusicStartRequested+=r=>{n++;Check(r.RawTime==97000&&r.EffectiveTimeBefore==97000,"request raw");};
            t.Update(100000);Check(t.EffectiveTime==-200&&t.Compensation==97200,"overshoot");t.Update(100500);t.Update(100500);Check(t.EffectiveTime==300&&n==1,"once/progression");
        });
        Test("request and anchor observer order preserves native moments",()=>{
            var t=new Timeline(0,0,80);var order=new List<string>();t.MusicStartRequested+=r=>{order.Add("request");Check(t.EffectiveTime==-79&&t.Compensation==0&&t.MusicStarted,"pre compensation");};
            t.MusicStartAnchored+=r=>{order.Add("anchor");Check(t.EffectiveTime==-80&&t.Compensation==1,"post compensation");};t.Update(2921);Check(order.SequenceEqual(new[]{"request","anchor"}),"order");
        });
        Test("throwing callback cannot change clock or suppress other observers",()=>{
            var t=new Timeline(0,0,0);int n=0;t.MusicStartRequested+=r=>throw new Exception("audio unavailable");t.MusicStartRequested+=r=>n++;t.Update(3010);
            Check(t.EffectiveTime==0&&t.Compensation==10&&n==1&&t.NotificationErrors.Count==1,"error isolation");t.Update(3020);Check(t.EffectiveTime==10&&t.StartRequestCount==1,"no retry");
        });
        Test("callback timeline reentry is rejected without moving anchor",()=>{
            var t=new Timeline(0,0,0);t.MusicStartRequested+=r=>t.Update(9999);t.Update(3001);Check(t.RawTime==1&&t.EffectiveTime==0&&t.NotificationErrors.Count==1,"reentry guard");
        });
        Test("DOWN can trigger BGM start without running FRAME",()=>{
            var(s,c,b)=Session();c.Milliseconds=3000;s.Frame();int frame=s.Core!.LastFrameTime;c.Milliseconds=3001;s.Key('J',true);
            Check(b.Plays==1&&s.Core.LastFrameTime==frame&&s.Core.Timeline.EffectiveTime==0,"DOWN contract");s.Key('J',false);
        });
        Test("UP and MOVE never refresh music-start clock",()=>{
            var(s,c,b)=Session();c.Milliseconds=100;s.Contact(100,4,true);int e=s.Core!.Timeline.EffectiveTime;c.Milliseconds=4000;s.MoveContact(100,3);s.Contact(100,3,false);
            Check(b.Plays==0&&s.Core.Timeline.EffectiveTime==e,"cleanup does not update");
        });
        Test("resource loading occurs before the fresh clock origin",()=>{
            var c=new Clock();var b=new FakeBgm{OnLoad=()=>c.Milliseconds+=600};var s=new GameplaySession(c,b);s.Start(Single,0,"prepared",Resource);
            Check(s.Core!.Timeline.EffectiveTime==-3000,"load delay is not gameplay time");c.Milliseconds=3600;s.Frame();Check(b.Plays==0,"equality after full preroll");c.Milliseconds=3601;s.Frame();Check(b.Plays==1&&s.Core.Timeline.EffectiveTime==0,"strict start");
        });
        Test("invalid combined offset rejects before altering current run",()=>{
            var(s,c,b)=Session();var old=s.Core;bool threw=false;try{s.Start(Single.Replace("AudioOffset:0","AudioOffset:120"),int.MaxValue,"invalid",Resource);}catch(OverflowException){threw=true;}
            Check(threw&&ReferenceEquals(old,s.Core)&&s.Run==1,"explicit invalid configuration");
        });
        Test("load before preroll has no premature play",()=>{
            var(s,c,b)=Session();Check(b.Loads==1&&b.Plays==0&&s.Audio!.State=="READY","prepare");c.Milliseconds=2999;s.Frame();c.Milliseconds=3000;s.Frame();Check(b.Plays==0,"preroll/equality");
        });
        Test("repeated frames and contacts never double-start audio",()=>{
            var(s,c,b)=Session();c.Milliseconds=3002;s.Frame();for(int i=0;i<20;i++){s.Frame();s.Key('J',true);s.Key('J',false);}
            Check(b.Plays==1&&s.Audio!.Requests==1&&s.Audio.Starts==1,"exact once");
        });
        Test("explicit AFF120 user-40 yields80; user-120 cancels",()=>{
            foreach(var p in new[]{(-40,80),(-120,0)}){var(s,c,b)=Session(Single.Replace("AudioOffset:0","AudioOffset:120"),p.Item1);c.Milliseconds=3001-p.Item2;s.Frame();Check(s.Core!.Timeline.EffectiveTime==-p.Item2,"sum/sign");}
        });
        Test("missing resource reports error while gameplay still judges",()=>{
            var(s,c,b)=Session(b:new FakeBgm{FailLoad=true});Check(s.Audio!.State=="ERROR","visible error");c.Milliseconds=3002;s.Frame();c.Milliseconds=4502;s.Frame();s.Key('J',true);
            Check(s.Core!.Pure==1&&s.Core.Score==10000001&&s.Audio.Requests==1&&b.Plays==0,"unavailable output cannot change judgment");
        });
        Test("invalid nonbundled resource rejected",()=>{
            var(s,c,b)=Session(resource:"https://example.invalid/audio.wav");Check(s.Audio!.State=="ERROR"&&b.Loads==0,"no network resource");
        });
        Test("short soundtrack is rejected without changing timeline",()=>{
            var(s,c,b)=Session(b:new FakeBgm{Duration=0.1});c.Milliseconds=3002;s.Frame();Check(s.Audio!.State=="ERROR"&&b.Plays==0&&s.Core!.Timeline.EffectiveTime==0,"duration/config");
        });
        Test("backend Play rejection does not claim acceptance",()=>{
            var(s,c,b)=Session(b:new FakeBgm{RejectPlay=true});c.Milliseconds=3002;s.Frame();Check(s.Audio!.State=="ERROR"&&s.Audio.Starts==0&&s.Audio.PlayAttempts==1&&s.Core!.Timeline.EffectiveTime==0,"backend rejected");
        });
        Test("backend Play exception is stopped and clock still anchored",()=>{
            var(s,c,b)=Session(b:new FakeBgm{FailPlay=true});c.Milliseconds=3010;s.Frame();Check(s.Audio!.State=="ERROR"&&b.Stops>0&&s.Core!.Timeline.Compensation==10,"failed start cleanup");
        });
        Test("consecutive runs have fresh latch and no audio overlap",()=>{
            var(s,c,b)=Session();c.Milliseconds=3002;s.Frame();c.Milliseconds=4000;s.Start(Single,0,"second",Resource);Check(b.Active==0&&!s.Core!.Timeline.MusicStarted,"fresh prereoll");
            c.Milliseconds=7002;s.Frame();Check(b.Plays==2&&b.PeakActive==1&&s.Audio!.Requests==1&&s.Run==2,"new run");
        });
        Test("menu detaches old timeline and stops audio",()=>{
            var(s,c,b)=Session();var old=s.Core!;s.Home();old.Frame(3002);Check(b.Plays==0&&s.Core==null,"stale start notification");
        });
        Test("replay detaches prior session even if old kernel advanced",()=>{
            var(s,c,b)=Session();var old=s.Core!;c.Milliseconds=100;s.Start(Single,0,"new",Resource);old.Frame(4000);Check(b.Plays==0&&!s.Core!.Timeline.MusicStarted,"old request ignored");
        });
        Test("cleanup failure blocks new playback and remains visible",()=>{
            var b=new FakeBgm();var(s,c,_)=Session(b:b);c.Milliseconds=3002;s.Frame();b.FailStop=true;c.Milliseconds=4000;s.Start(Single,0,"blocked",Resource);c.Milliseconds=7002;s.Frame();Check(s.Audio!.State=="ERROR"&&b.Plays==1,"new start blocked");
        });
        Test("diagnostic observer failures cannot corrupt lifecycle",()=>{
            var(s,c,b)=Session();s.Audio!.Diagnostic+=d=>throw new Exception("log sink");c.Milliseconds=3002;s.Frame();s.Home();Check(b.Active==0,"cleanup survives logging");
        });
        Test("silent legacy chart has request but no backend playback",()=>{
            var(s,c,b)=Session(resource:null);c.Milliseconds=3002;s.Frame();Check(s.Audio!.State=="SILENT"&&s.Audio.Requests==1&&b.Plays==0&&b.Loads==0,"preserved silent chart");
        });
        Test("backend playhead is diagnostic and never feedback",()=>{
            var b=new FakeBgm{Position=99999};var(s,c,_)=Session(b:b);c.Milliseconds=3002;s.Frame();b.Position=-10000;c.Milliseconds=4002;s.Frame();Check(s.Core!.Timeline.EffectiveTime==1000&&s.Core.Timeline.Compensation==2,"authoritative E");
        });
        Test("BGM end reports error without replacing chart results",()=>{
            var(s,c,b)=Session();c.Milliseconds=3002;s.Frame();s.Audio!.Finished();Check(s.Audio.State=="ERROR"&&!s.Core!.Finished,"early finish diagnostic");
            c.Milliseconds=4502;s.Frame();s.Key('J',true);c.Milliseconds=4623;s.Frame();Check(s.Core!.Result!.Pure==1&&b.Active==0,"gameplay/result unaffected");
        });
        Test("completion stops before replay and result identity remains stable",()=>{
            var(s,c,b)=Session();c.Milliseconds=3002;s.Frame();c.Milliseconds=4502;s.Frame();s.Key('J',true);c.Milliseconds=4623;s.Frame();var r=s.Core!.Result;Check(r!=null&&b.Active==0&&s.Audio!.State=="STOPPED","result cleanup");
            s.Frame();Check(ReferenceEquals(r,s.Core.Result)&&b.Plays==1,"no repeated start");
        });
        Test("audible chart full trace independent of unavailable muted and hostile playhead output",()=>{
            string aff=Read("reconstructed/godot/content/audible_practice.aff");string a=Complete(aff,new FakeBgm());
            foreach(var backend in new[]{new FakeBgm{Muted=true,Position=10000},new FakeBgm{Position=-10000},new FakeBgm{FailLoad=true},new FakeBgm{RejectPlay=true},new FakeBgm{FailPlay=true}})
                Check(a==Complete(aff,backend),"identical every-frame clock/contacts/units/counters/result despite output state");
        });
        Test("judgment diagnostics survive result contact cleanup without duplicates",()=>{
            const string hold="AudioOffset:0\n-\ntiming(0,120.00,4.00);hold(1000,2000,3);";
            var(s,c,b)=Session(hold);var ledger=new List<JudgmentEvent>();s.JudgmentsProduced+=events=>ledger.AddRange(events);
            c.Milliseconds=3002;s.Frame();c.Milliseconds=4002;s.Key('J',true);c.Milliseconds=6002;s.Frame();
            Check(s.Core!.Finished&&s.HeldCount==0&&ledger.Count==3&&ledger.All(e=>e.CheckpointTime.HasValue&&e.Outcome=="LOST"&&e.EffectiveTime==3000),"record before cleanup");
            s.Frame();Check(ledger.Count==3,"no duplicate diagnostics");
        });
        Test("audio diagnostics capture session offset and pre/post clock domains",()=>{
            var(s,c,b)=Session(user:80);var d=new List<BgmDiagnostic>();s.Audio!.Diagnostic+=d.Add;c.Milliseconds=2921;s.Frame();
            var before=d.Single(x=>x.Kind=="BGM_REQUEST");var after=d.Single(x=>x.Kind=="BGM_ANCHORED");
            Check(before.EffectiveTime==-79&&before.Compensation==0&&after.EffectiveTime==-80&&after.Compensation==1&&after.Session.CombinedOffset==80&&after.RequestCount==1,"observable order");
        });
        File.WriteAllText(Path.Combine(output,"audio-contract-tests.json"),JsonSerializer.Serialize(new{count,passed=count-failed,failed,skipped=0,traces},Replay.JsonOptions));
        Console.WriteLine($"R005 core/audio tests: {count}; passed: {count-failed}; failed: {failed}; skipped: 0");return failed==0?0:1;
    }
}
