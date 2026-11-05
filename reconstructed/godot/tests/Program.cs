using Arconist.Bridge;
using Arconist.Core;

sealed class Clock : IMonotonicClock { public long Milliseconds { get; set; } }
static class Tests
{
    static int count,failed;
    const string Ordinary="AudioOffset:0\n-\ntiming(0,120.00,4.00);(1000,3);(2000,2);";
    static void Assert(bool condition,string detail) { if (!condition) throw new Exception(detail); }
    static void Test(string name,Action action)
    { count++; try { action();Console.WriteLine("PASS "+name); } catch(Exception e) { failed++;Console.WriteLine("FAIL "+name+": "+e.Message); } }
    static (GameplaySession s,Clock c) Begin(string chart=Ordinary)
    { var c=new Clock(); var s=new GameplaySession(c);s.Start(chart);c.Milliseconds=3002;s.Frame();return(s,c); }
    static int Main()
    {
        Test("physical D/F/J/K map to internal 2/3/4/5",()=> {
            Assert(new[]{'D','F','J','K'}.Select(GameplaySession.LaneForKey).SequenceEqual(new[]{2,3,4,5}),"mapping");
            Assert(GameplaySession.LaneForKey('d')==2 && GameplaySession.LaneForKey('X')==0,"case/unmapped");
        });
        Test("Godot physical/logical/Unicode key fallback",()=> {
            Assert(GameplaySession.ResolveKey(74,70,102)=='J',"physical preference");
            Assert(GameplaySession.ResolveKey(4194313,74,106)=='J',"observed Windows injected key");
            Assert(GameplaySession.ResolveKey(0,0,107)=='K',"Unicode fallback");
            Assert(GameplaySession.ResolveKey(4194305,4194305,0)=='\0',"unmapped input");
        });
        Test("Godot callbacks keep input-first035 order",()=> {
            var(s,c)=Begin("AudioOffset:0\n-\ntiming(0,120.00,4.00);(1000,3);(1109,3);");
            c.Milliseconds=4002;s.Frame();c.Milliseconds=4112;s.Key('J',true);
            Assert(s.Core!.LastFrameTime==1000 && s.Core.Lost==1 && s.Core.Pure==0,"Input must not call Frame");
            s.Key('J',false);s.Frame();Assert(s.Core.ContactCount==0 && !s.Core.Notes[1].Consumed,"cleanup/later note");
        });
        Test("Godot callbacks keep frame-first035 order",()=> {
            var(s,c)=Begin("AudioOffset:0\n-\ntiming(0,120.00,4.00);(1000,3);(1109,3);");
            c.Milliseconds=4002;s.Frame();c.Milliseconds=4112;s.Frame();s.Key('J',true);s.Key('J',false);
            Assert(s.Core!.Lost==1 && s.Core.Pure==1 && s.Core.Score==5000001,"expiry-before-input");
        });
        Test("correct versus incorrect key changes actual judgment",()=> {
            var(s,c)=Begin();c.Milliseconds=4002;s.Frame();s.Key('D',true);s.Key('D',false);
            Assert(s.Core!.Pure==0 && s.Core.Score==0,"wrong lane should not score");
            s.Key('J',true);s.Key('J',false);Assert(s.Core.Pure==1 && s.Core.Score==5000001,"correct lane must score");
        });
        Test("echo and repeated DOWN do not manufacture input",()=> {
            var(s,c)=Begin();c.Milliseconds=4002;s.Frame();Assert(!s.Key('J',true,true),"echo accepted");
            s.Key('J',true);Assert(!s.Key('J',true) && s.Core!.ContactCount==1 && s.Core.Pure==1,"duplicate DOWN");
            s.Key('J',false);Assert(!s.Key('J',false) && s.HeldCount==0,"duplicate UP");
        });
        Test("UP does not advance E or frame",()=> {
            var(s,c)=Begin();c.Milliseconds=4002;s.Frame();s.Key('J',true);c.Milliseconds=4052;s.Key('J',false);
            Assert(s.Core!.Timeline.EffectiveTime==1000 && s.Core.LastFrameTime==1000 && s.Core.ContactCount==0,"UP clock/order");
        });
        Test("focus-loss release cleans multiple contacts",()=> {
            var(s,c)=Begin();s.Key('D',true);s.Key('F',true);s.ReleaseAll();Assert(s.Core!.ContactCount==0 && s.HeldCount==0,"focus cleanup");
        });
        Test("mouse contacts use separate identity and same lane core",()=> {
            var(s,c)=Begin();c.Milliseconds=4002;s.Frame();s.Contact(100,4,true);s.Key('J',true);
            Assert(s.Core!.Pure==1 && s.Core.ContactCount==2,"mouse/keyboard duplicate guard");s.ReleaseAll();
        });
        Test("complete two-tap result propagates same core instance",()=> {
            var(s,c)=Begin();c.Milliseconds=4002;s.Frame();s.Key('J',true);s.Key('J',false);
            c.Milliseconds=5002;s.Frame();s.Key('F',true);s.Key('F',false);c.Milliseconds=5123;s.Frame();
            var r=s.Core!.Result;Assert(r!=null && r.Pure==2 && r.Score==10000002 && r.Health==80 && r.Category==3 && r.MaxCombo==2,"result propagation");
            Assert(BitConverter.SingleToInt32Bits(s.Core.Health)==1117834445,"native health bits");
        });
        Test("frame miss feedback is core-produced once",()=> {
            var(s,c)=Begin();c.Milliseconds=4102;s.Frame();Assert(s.Core!.Lost==0,"strict boundary");
            c.Milliseconds=4103;s.Frame();Assert(s.Feedback=="LOST" && s.Core.Lost==1,"miss feedback");s.Frame();Assert(s.Core.Lost==1,"duplicate miss");
        });
        Test("results release held contacts without mutating cached result",()=> {
            var(s,c)=Begin();c.Milliseconds=4002;s.Frame();s.Key('J',true);c.Milliseconds=5123;s.Frame();
            Assert(s.Core!.Finished && s.Core.ContactCount==0 && s.HeldCount==0,"end cleanup");
            Assert(!s.Key('K',true),"finished input accepted");
        });
        Test("restart has fresh counters/notes/contacts/result/epoch",()=> {
            var(s,c)=Begin();c.Milliseconds=4002;s.Frame();s.Key('J',true);c.Milliseconds=5123;s.Frame();var old=s.Core;
            c.Milliseconds=20000;s.Start(Ordinary);
            Assert(!ReferenceEquals(old,s.Core) && s.Core!.Result==null && !s.Core.Finished && s.Core.Score==0 && s.Core.Pure==0 && s.Core.Far==0 && s.Core.Lost==0 && s.Core.Combo==0 && s.Core.MaxCombo==0 && s.Core.Health==0 && s.Core.ContactCount==0 && s.HeldCount==0 && s.Core.Notes.All(n=>!n.Consumed&&!n.Missed&&n.Contact==-1),"stale restart");
            Assert(s.Core!.Timeline.EffectiveTime==-3000 && s.Run==2,"restart epoch");
        });
        Test("callback ledger preserves DOWN/UP before subsequent frame",()=> {
            var(s,c)=Begin();var ledger=new List<string>();s.Changed+=ledger.Add;c.Milliseconds=4002;s.Key('J',true);s.Key('J',false);s.Frame();
            Assert(ledger.SequenceEqual(new[]{"DOWN","UP","FRAME"}),"event reorder");
        });
        Test("home cleans contacts and removes result",()=> { var(s,c)=Begin();s.Key('D',true);s.Home();Assert(s.Core==null&&s.HeldCount==0,"home state"); });
        Console.WriteLine($"Bridge tests: {count}; passed: {count-failed}; failed: {failed}; skipped: 0");return failed==0?0:1;
    }
}
