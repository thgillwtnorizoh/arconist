using Arconist.Core;
using Arconist.Bridge;
using Arconist.Headless;
using System.Text.Json;
using System.Text.Json.Nodes;

sealed class Clock : IMonotonicClock { public long Milliseconds { get; set; } }
static class Tests
{
    static int count, failed;
    static string root = "", output = "";
    static readonly List<object> traces = new();
    const string HoldAff = "AudioOffset:0\nTimingPointDensityFactor:1.0\n-\ntiming(0,120.00,4.00);hold(1000,2000,3);";
    static void Check(bool ok, string message) { if (!ok) throw new Exception(message); }
    static void Test(string name, Action test)
    { count++; try { test(); Console.WriteLine("PASS R004 " + name); } catch (Exception e) { failed++; Console.WriteLine("FAIL R004 " + name + ": " + e.Message); } }
    static void Throws(Action a) { bool threw = false; try { a(); } catch { threw = true; } Check(threw,"expected explicit rejection"); }
    static string Read(string path) => File.ReadAllText(Path.Combine(root, path));
    static Kernel Begin(string aff = HoldAff) { var k = new Kernel(Chart.Parse(aff)); k.Frame(0); k.Frame(3002); return k; }
    static void Frame(Kernel k, int e) => k.Frame(e + 3002L);
    static void Down(Kernel k, int e, int p = 42, int lane = 4) => k.Down(e + 3002L, p, lane);
    static JsonNode Snapshot(Kernel k) => JsonSerializer.SerializeToNode(new {
        e = k.Timeline.EffectiveTime, lastFrameTime=k.LastFrameTime, pure=k.Pure, far=k.Far, lost=k.Lost,
        shining=k.Shining, score=k.Score, combo=k.Combo, maxCombo=k.MaxCombo, health=(double)k.Health,
        healthBits=BitConverter.SingleToInt32Bits(k.Health), contactCount=k.ContactCount, contacts=k.Contacts,
        hold=k.Holds.Count == 0 ? null : new { latched=k.Holds[0].Latched, holding=k.Holds[0].Holding,
            active=k.Holds[0].Active, resolved=k.Holds[0].Records.Select(r=>r.Resolved?1:0),
            activatingContacts=k.Holds[0].ActivatingContacts, records=k.Holds[0].Records },
        tap=k.Notes.Count == 0 ? null : new { consumed=k.Notes[0].Consumed, missed=k.Notes[0].Missed, contact=k.Notes[0].Contact },
        candidates=k.Candidates, outcomes=k.Classifications.Select(c=>c.Outcome), judgments=k.Judgments,
        finished=k.Finished,result=k.Result
    },Replay.JsonOptions)!;
    static void NativeCase(JsonNode c)
    {
        var k=Begin(Read("research_harness/fixtures/"+c["fixture"]!.GetValue<string>()));
        Check(k.Chart.JudgmentUnits==c["judgmentUnits"]!.GetValue<int>() && k.Chart.EndTime==c["endTime"]!.GetValue<int>(),"native N/end");
        var h=k.Holds.Single(); Check(h.Data.Lane==4 && h.Data.RawLane==3 && h.Data.Interval==250 && h.Data.Start==1000 && h.Data.End==2000,"native hold identity");
        Check(h.Records.Select(r=>r.Time).SequenceEqual(new[]{1250,1500,1750}) && h.Records.All(r=>r.Weight==1),"native records");
        var states=new List<JsonNode>(); string? difference=null;
        foreach(var ev in c["steps"]!.AsArray())
        {
            int e=ev!["e"]!.GetValue<int>(); string kind=ev["kind"]!.GetValue<string>();
            if(kind=="FRAME") Frame(k,e);
            else if(kind=="DOWN") Down(k,e,ev["pointer"]!.GetValue<int>(),ev["lane"]!.GetValue<int>());
            else k.Up(ev["pointer"]!.GetValue<int>());
            var actual=Snapshot(k);states.Add(actual);
            difference ??= Replay.FirstDifference(ev["expect"],actual,$"{c["name"]}:event[{states.Count-1}]E{e}/{kind}");
        }
        traces.Add(new{name=c["name"]!.GetValue<string>(),states,firstDifference=difference});
        Check(difference==null,difference??"");
        Check(h.Records.All(r=>r.Resolved) && k.ContactCount==0,"complete native record/cleanup path");
    }
    static (GameplaySession s,Clock clock) Session(string aff=HoldAff)
    {var clock=new Clock();var s=new GameplaySession(clock);s.Start(aff);clock.Milliseconds=3002;s.Frame();return(s,clock);}
    public static int Main(string[] args)
    {
        if(args.Length!=2) {Console.Error.WriteLine("Usage: Arconist.Hold.Tests REPO_ROOT OUTPUT_DIR");return 1;}
        root=Path.GetFullPath(args[0]);output=Path.GetFullPath(args[1]);Directory.CreateDirectory(output);
        var references=JsonNode.Parse(Read("reference_traces/r004/native-cases.json"))!;
        foreach(var c in references["cases"]!.AsArray()) Test("native "+c!["name"]!.GetValue<string>(),()=>NativeCase(c));
        Test("typed integer hold, pure hold chart and no invented head/tail",()=> {
            var c=Chart.Parse(HoldAff);Check(c.Taps.Count==0 && c.Holds.Count==1 && c.JudgmentUnits==3 && c.EndTime==2500,"typed initialization");
            Check(c.Holds[0].Checkpoints.SequenceEqual(new[]{1250,1500,1750}),"interior only");
        });
        Test("E010 density2 interval125 seven units end2500",()=> {
            var c=Chart.Parse(HoldAff.Replace("Factor:1.0","Factor:2.0"));Check(c.Holds[0].Interval==125 && c.JudgmentUnits==7 && c.EndTime==2500 && c.Holds[0].Checkpoints.SequenceEqual(new[]{1125,1250,1375,1500,1625,1750,1875}),"native density propagation");
        });
        Test("E001 tempo255 divisor boundary and midpoint fallback",()=> {
            Check(Chart.Parse(HoldAff.Replace("120.00","300.00")).Holds[0].Interval==200,"high tempo divisor");
            Check(Chart.Parse(HoldAff.Replace("2000","1100")).Holds[0].Checkpoints.SequenceEqual(new[]{1050}),"midpoint single unit");
        });
        Test("interval selected at hold start; later timing changes depth",()=> {
            var c=Chart.Parse(HoldAff.Replace("hold(","timing(1200,60.00,4.00);hold("));
            Check(c.Holds[0].Interval==250,"start timing");var k=new Kernel(c);Check(k.DepthAt(2000)!=new Kernel(Chart.Parse(HoldAff)).DepthAt(2000),"piecewise depth");
        });
        Test("unsupported hold domain and grammar fail explicitly",()=> {
            foreach(string h in new[]{"hold(1000,1000,3);","hold(2000,1000,3);","hold(1,2,3);","hold(1000,2000,3.0);","hold(1000,2000,0);","hold(1000,2000,5);","hold(-1,2000,3);"})
                Throws(()=>Chart.Parse("AudioOffset:0\n-\ntiming(0,120.00,4.00);"+h));
            Throws(()=>Chart.Parse(HoldAff.Replace("Factor:1.0","Factor:100000000.0")));
        });
        Test("hold endpoint buckets and min endpoint admission",()=> {
            var k=Begin();Check(k.Holds[0].Bucket==0 && k.Holds[0].EndBucket==1 && k.Holds[0].Active,"E026 index");
            var late=new Kernel(Chart.Parse(HoldAff));late.Timeline.Update(3002);Frame(late,1500);Check(late.Holds[0].Active,"end endpoint admits despite passed start");
            Frame(late,2600);Check(late.Holds[0].Records.All(r=>r.Resolved),"admitted overdue recording");
        });
        Test("initial strict100ms and continuous strict start/end boundaries",()=> {
            foreach(int e in new[]{900,901,1000,1001,1999,2000}) {
                var k=Begin();Frame(k,e);Down(k,e);Check(k.Holds[0].Latched==(e>900&&e<2000),"latch E"+e);
                Frame(k,e);Check(k.Holds[0].Holding==(e>1000&&e<2000),"activity E"+e);
            }
        });
        Test("release preserves latch until next frame clears activity",()=> {
            var k=Begin();Frame(k,1000);Down(k,1000);Frame(k,1001);k.Up(42);
            Check(k.Holds[0].Holding&&k.Holds[0].Latched,"UP must not insert frame");Frame(k,1002);
            Check(!k.Holds[0].Holding&&k.Holds[0].Latched&&k.Lost==0,"no immediate penalty");
        });
        Test("all contacts release and reused pointer gets fresh generated identity",()=> {
            var k=Begin();Down(k,1000);Down(k,1000,43);Frame(k,1001);Check(k.Holds[0].ActivatingContacts.SequenceEqual(new[]{0,1}),"both contacts");
            k.Up(42);k.Up(43);Frame(k,1002);Check(!k.Holds[0].Holding,"clear");Down(k,1100);Check(k.Contacts[0].Id==2,"new logical contact");Frame(k,1101);Check(k.Holds[0].Holding,"reacquire");
        });
        Test("wrong lane cannot latch or sustain",()=> {
            var k=Begin();Down(k,1000,42,3);Frame(k,1001);Check(!k.Holds[0].Latched&&!k.Holds[0].Holding,"wrong lane");
        });
        Test("unlatched hold cannot activate from retained earlier contact",()=> {
            var k=Begin();Down(k,900);Frame(k,1125);Check(!k.Holds[0].Holding&&k.Pure==0,"latch required");
        });
        Test("temporary release around due time allows later successful catchup",()=> {
            var k=Begin();Down(k,1000);Frame(k,1001);k.Up(42);Frame(k,1125);Check(k.Lost==0,"no instant due miss");
            Down(k,1300,43);Frame(k,1301);Check(k.Pure==1&&k.Lost==0,"catchup before overdue");
        });
        Test("due cutoff uses truncating float addition for fractional interval",()=> {
            var k=Begin(HoldAff.Replace("120.00","180.00"));Down(k,1000);
            int record=k.Holds[0].Records[0].Time;float interval=k.Holds[0].Data.Interval;
            int e=record-(int)(interval*0.5f)-1;Frame(k,e);Check(k.Pure==0,"before cutoff");Frame(k,e+1);Check(k.Pure==1,"inclusive cutoff");
        });
        Test("inactive overdue boundary inclusive and repeated frames never duplicate",()=> {
            var k=Begin();Frame(k,1749);Check(k.Lost==0,"first record not overdue");Frame(k,1750);Check(k.Lost==1&&k.Health==0,"first overdue");
            Frame(k,1750);Check(k.Lost==1,"duplicate miss");Frame(k,2000);Frame(k,2250);Check(k.Lost==3,"three missed units");
            Frame(k,2501);Check(k.Result!.Lost==3&&k.Result.RecordedLost==3,"result denominator");
        });
        Test("missed checkpoints cannot later be awarded on reacquisition",()=> {
            var k=Begin();Frame(k,1750);Down(k,1750);Frame(k,1751);
            Check(k.Lost==1&&k.Pure==2&&k.Holds[0].Records[0].Outcome=="LOST","unique outcomes");
        });
        Test("hold completion equality and cached result",()=> {
            var k=Begin();Down(k,1000);foreach(int e in new[]{1001,1125,1375,1625,2500})Frame(k,e);
            Check(!k.Finished,"strict chart end");Frame(k,2501);var r=k.Result;Check(r!.Pure==3&&r.Score==10000003&&r.Health==80&&r.MaxCombo==3,"composed result");
            Frame(k,2502);Check(ReferenceEquals(r,k.Result)&&k.Pure==3,"cached");
        });
        foreach(bool reverse in new[]{false,true}) Test("E027 independent chord contacts "+reverse,()=> {
            var k=Begin(Read("research_harness/fixtures/native_chord.aff"));Frame(k,1500);int[] lanes=reverse?new[]{5,2}:new[]{2,5};
            Down(k,1500,42,lanes[0]);Down(k,1500,43,lanes[1]);Check(k.Pure==2&&k.Score==10000002&&(double)k.Health==80.4000015258789,"native chord totals");
            Check(k.Notes.Single(n=>n.Data.Lane==lanes[0]).Contact==0&&k.Notes.Single(n=>n.Data.Lane==lanes[1]).Contact==1,"contact identity");k.Up(42);k.Up(43);
        });
        Test("bridge held key and echoes do not create duplicate DOWN",()=> {
            var(s,c)=Session();c.Milliseconds=4002;s.Frame();s.Key('J',true);for(int i=0;i<20;i++)Check(!s.Key('J',true,i%2==0),"duplicate accepted");
            c.Milliseconds=4003;s.Frame();Check(s.Core!.Holds[0].Holding&&s.Core.ContactCount==1,"retained key");
        });
        Test("bridge keyboard plus mouse same lane survives keyboard release",()=> {
            var(s,c)=Session();c.Milliseconds=4002;s.Frame();s.Key('J',true);s.Contact(100,4,true);c.Milliseconds=4003;s.Frame();
            Check(s.Core!.Holds[0].ActivatingContacts.Count==2,"distinct human adapter contacts");s.Key('J',false);c.Milliseconds=4127;s.Frame();
            Check(s.Core.Holds[0].Holding&&s.Core.Pure==1&&s.HeldCount==1,"mouse sustains");s.Contact(100,4,false);c.Milliseconds++;s.Frame();Check(!s.Core.Holds[0].Holding,"all released");
        });
        Test("bridge key reacquisition has new identity and checkpoint feedback",()=> {
            var(s,c)=Session();c.Milliseconds=4002;s.Key('J',true);c.Milliseconds=4003;s.Frame();s.Key('J',false);c.Milliseconds=4102;s.Frame();s.Key('J',true);c.Milliseconds=4127;s.Frame();
            Check(s.Core!.Contacts.Single().Id==1&&s.Core.Pure==1&&s.Feedback.Contains("CHECKPOINT"),"reacquire/feedback");
        });
        Test("bridge cleanup resets activity next frame and restart makes fresh records",()=> {
            var(s,c)=Session();c.Milliseconds=4002;s.Key('J',true);c.Milliseconds=4127;s.Frame();var old=s.Core;s.ReleaseAll();c.Milliseconds++;s.Frame();Check(!old!.Holds[0].Holding,"focus cleanup");
            c.Milliseconds=20000;s.Start(HoldAff);Check(!ReferenceEquals(old,s.Core)&&s.Core!.Holds[0].Records.All(r=>!r.Resolved)&&!s.Core.Holds[0].Latched&&s.HeldCount==0,"restart clear");
        });
        Test("bridge mouse MOVE changes retained lane without input or frame judgment",()=> {
            var(s,c)=Session();c.Milliseconds=4002;s.Contact(100,4,true);c.Milliseconds=4003;s.Frame();int id=s.Core!.Contacts[0].Id;
            s.MoveContact(100,3);Check(s.Core.Timeline.EffectiveTime==1001&&s.Core.LastFrameTime==1001,"MOVE clock");
            c.Milliseconds=4004;s.Frame();Check(!s.Core.Holds[0].Holding&&s.Core.Lost==0,"departure");
            s.MoveContact(100,0);s.MoveContact(100,4);c.Milliseconds=4127;s.Frame();Check(s.Core.Holds[0].Holding&&s.Core.Pure==1&&s.Core.Contacts[0].Id==id,"same retained contact reentry");
        });
        Test("mouse MOVE never creates a fresh tap or contact",()=> {
            var(s,c)=Session("AudioOffset:0\n-\ntiming(0,120.00,4.00);(1000,3);");
            c.Milliseconds=4002;s.Contact(100,2,true);s.MoveContact(100,4);Check(s.Core!.Pure==0&&s.Core.ContactCount==1,"movement is not DOWN");s.ReleaseAll();Check(!s.MoveContact(100,4),"released pointer");
        });
        Test("bridge completed hold results release contacts and replay/home",()=> {
            var(s,c)=Session();c.Milliseconds=4002;s.Key('J',true);foreach(int e in new[]{1001,1125,1375,1625,2501}){c.Milliseconds=e+3002;s.Frame();}
            Check(s.Core!.Result!.Pure==3&&s.HeldCount==0&&s.Core.ContactCount==0,"results cleanup");s.Start(HoldAff);Check(s.Core!.Result==null,"replay");s.Home();Check(s.Core==null,"home");
        });
        Test("R004 bundled mixed chart completes with held/released/reacquired contacts",()=> {
            var k=Begin(Read("reconstructed/godot/content/mixed_practice.aff"));
            for(int e=1;e<=k.Chart.EndTime+1;e++) {
                foreach(var t in k.Chart.Taps.Where(t=>t.Time==e)){Down(k,e,100+t.Ordinal,t.Lane);k.Up(100+t.Ordinal);}
                foreach(var h in k.Chart.Holds) {
                    int p=200+h.Ordinal;
                    if(e==h.Start)Down(k,e,p,h.Lane);
                    if(e==h.Start+600)k.Up(p);
                    if(e==h.Start+700)Down(k,e,p,h.Lane);
                    if(e==h.End)k.Up(p);
                }
                Frame(k,e);
            }
            Check(k.Result!=null&&k.Lost==0&&k.Pure==k.Chart.JudgmentUnits&&k.ContactCount==0,"mixed completion");
        });
        Test("native oracle detects first intermediate divergence",()=> {
            var actual=Snapshot(Begin());actual["health"]=99;
            Check(Replay.FirstDifference(JsonNode.Parse("{\"health\":0}"),actual,"E1000")!.StartsWith("E1000.health:"),"first field diagnostic");
        });
        File.WriteAllText(Path.Combine(output,"native-comparisons.json"),JsonSerializer.Serialize(new{count,passed=count-failed,failed,skipped=0,traces},Replay.JsonOptions));
        Console.WriteLine($"R004 core/bridge tests: {count}; passed: {count-failed}; failed: {failed}; skipped: 0");return failed==0?0:1;
    }
}
