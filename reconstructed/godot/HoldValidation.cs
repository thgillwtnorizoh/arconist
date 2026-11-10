using Godot;
using Arconist.Core;
using Arconist.Bridge;
using System.Text.Json;

namespace Arconist.GodotApp;

// Headless production-node/resource tests. No OS input or image inspection.
public static class HoldValidation
{
    private sealed class Clock : IMonotonicClock { public long Milliseconds { get; set; } }
    public static void Run(Node owner, SpatialTrack track, string evidenceDir)
    {
        int passed=0, failed=0;var outcomes=new List<object>();
        void Check(bool ok,string message){if(!ok)throw new Exception(message);}
        void Test(string name,Action test){try{test();passed++;outcomes.Add(new{name,status="PASS"});GD.Print("PASS R004 "+name);}catch(Exception e){failed++;outcomes.Add(new{name,status="FAIL",error=e.Message});GD.Print("FAIL R004 "+name+": "+e.Message);}}
        string Load(string name)=>Godot.FileAccess.GetFileAsString("res://content/"+name);
        Kernel Core(string name="native_hold.aff"){var k=new Kernel(Chart.Parse(Load(name)));k.Frame(0);k.Frame(3002);return k;}
        MeshInstance3D Body(Kernel k)=>track.HoldVisual(k.Holds[0].Id)!.GetNode<MeshInstance3D>("Body");
        Test("all six selectable AFF resources parse from real Godot filesystem",()=> {
            foreach(var name in new[]{"practice.aff","ordinary_two_tap.aff","mixed_practice.aff","native_hold.aff","hold_first.aff","tap_first.aff"})Check(Chart.Parse(Load(name)).JudgmentUnits>0,name);
        });
        Test("production 3D hold body head and generated checkpoint meshes",()=> {
            var k=Core();track.Refresh(k);var view=track.HoldVisual(k.Holds[0].Id)!;
            Check(track.HoldVisualCount==1&&view.GetChildren().OfType<MeshInstance3D>().Count()==5,"one body/head/three ticks");
            Check(Body(k).Mesh is BoxMesh,"real 3D geometry");
        });
        Test("hold starts at recovered integer lane and native Y plane",()=> {
            var k=Core();k.Frame(4002);track.Refresh(k);var b=Body(k);
            Check(b.Position.X==212*SpatialTrack.Unit&&b.Position.Y==7*SpatialTrack.Unit,"lane/placeholder height");
            Check(track.HoldVisual(k.Holds[0].Id)!.GetNode<MeshInstance3D>("Head").Position.Z==0,"start at line");
        });
        Test("longitudinal body endpoints follow integer predepth model",()=> {
            var k=Core();k.Frame(4002);track.Refresh(k);var b=Body(k);float length=((BoxMesh)b.Mesh).Size.Z;
            Check(Math.Abs(length-8089*SpatialTrack.Unit)<0.0001f,"E1000 native end depth");
            Check(Math.Abs(b.Position.Z+length*0.5f)<0.0001f,"front at Z0");
        });
        Test("body approaches then shrinks from judgment line",()=> {
            var k=Core();track.Refresh(k);float first=Body(k).Position.Z;k.Frame(4002);track.Refresh(k);float full=((BoxMesh)Body(k).Mesh).Size.Z;
            Check(Body(k).Position.Z>first,"approach");k.Down(4002,42,4);k.Frame(4502);track.Refresh(k);Check(((BoxMesh)Body(k).Mesh).Size.Z<full,"shrink");
        });
        Test("active body indication reads authoritative latch/frame state",()=> {
            var k=Core();k.Frame(4002);k.Down(4002,42,4);track.Refresh(k);var off=((StandardMaterial3D)Body(k).MaterialOverride).AlbedoColor;
            k.Frame(4003);track.Refresh(k);var on=((StandardMaterial3D)Body(k).MaterialOverride).AlbedoColor;
            Check(off!=on&&k.Holds[0].Holding,"active color");k.Up(42);k.Frame(4004);track.Refresh(k);Check(((StandardMaterial3D)Body(k).MaterialOverride).AlbedoColor==off,"release color");
        });
        Test("checkpoint marker and feedback follow core resolution",()=> {
            var k=Core();k.Down(4002,42,4);k.Frame(4126);track.Refresh(k);var marker=track.HoldVisual(k.Holds[0].Id)!.GetNode<MeshInstance3D>("Checkpoint1250");
            var before=((StandardMaterial3D)marker.MaterialOverride).AlbedoColor;k.Frame(4127);track.Refresh(k);
            Check(k.Pure==1&&k.Judgments.Single().CheckpointTime==1250&&((StandardMaterial3D)marker.MaterialOverride).AlbedoColor!=before,"authoritative checkpoint");
        });
        Test("overdue miss feedback is red and not immediate release damage",()=> {
            var k=Core();k.Frame(4751);track.Refresh(k);Check(k.Lost==0,"E1749");k.Frame(4752);track.Refresh(k);
            var marker=track.HoldVisual(k.Holds[0].Id)!.GetNode<MeshInstance3D>("Checkpoint1250");Check(k.Lost==1&&((StandardMaterial3D)marker.MaterialOverride).AlbedoColor==new Color("ff6985"),"miss marker");
        });
        Test("hold renderer cannot mutate gameplay or records",()=> {
            var k=Core();k.Down(4002,42,4);k.Frame(4127);string State()=>JsonSerializer.Serialize(new{k.Score,k.Health,k.Combo,k.ContactCount,k.LastFrameTime,hold=k.Holds[0].Records});
            string before=State();for(int i=0;i<30;i++)track.Refresh(k);Check(before==State(),"read-only renderer");
        });
        Test("release and reacquisition preserve hold geometry identity",()=> {
            var k=Core();k.Down(4002,42,4);k.Frame(4003);track.Refresh(k);var node=Body(k);k.Up(42);k.Frame(4202);k.Down(4302,43,4);k.Frame(4303);track.Refresh(k);
            Check(ReferenceEquals(node,Body(k))&&k.Holds[0].Holding,"reacquired same hold");
        });
        Test("headless actual camera ray mouse plus key two-contact continuity",()=> {
            var c=new Clock();var s=new GameplaySession(c);s.Start(Load("native_hold.aff"));c.Milliseconds=3002;s.Frame();c.Milliseconds=4002;s.Frame();s.Key('J',true);
            var p=track.Camera.UnprojectPosition(SpatialTrack.World(212,0,0));int lane=track.Pick(p,out _);s.Contact(100,lane,true);c.Milliseconds=4003;s.Frame();Check(s.Core!.Holds[0].ActivatingContacts.Count==2,"both");
            s.Key('J',false);c.Milliseconds=4127;s.Frame();track.Refresh(s.Core);Check(s.Core.Pure==1&&s.Core.Holds[0].Holding,"mouse remains");s.ReleaseAll();
        });
        Test("restart replaces all old hold meshes and unresolved states",()=> {
            var first=Core();track.Refresh(first);var old=track.HoldVisual(first.Holds[0].Id)!;first.Down(4002,42,4);first.Frame(4127);
            var second=Core();track.Refresh(second);Check(!ReferenceEquals(old,track.HoldVisual(second.Holds[0].Id))&&!old.IsInsideTree()&&second.Holds[0].Records.All(r=>!r.Resolved),"fresh tree/state");
        });
        Test("switching to taps or home removes stale hold nodes",()=> {
            track.Refresh(Core());track.Refresh(Core("practice.aff"));Check(track.HoldVisualCount==0,"tap chart");track.Refresh(Core());track.Refresh(null);Check(track.HoldVisualCount==0,"home");
        });
        Test("completion hides hold geometry without authoring results",()=> {
            var k=Core();k.Down(4002,42,4);foreach(int e in new[]{1001,1125,1375,1625,2501})k.Frame(e+3002);track.Refresh(k);
            Check(!track.HoldVisual(k.Holds[0].Id)!.Visible&&k.Result!.Score==10000003,"results/hide");
        });
        Test("mixed chart production bridge headless full frame lifecycle",()=> {
            var c=new Clock();var s=new GameplaySession(c);s.Start(Load("mixed_practice.aff"));c.Milliseconds=3002;s.Frame();var chart=s.Core!.Chart;
            for(int e=1;e<=chart.EndTime+1;e++){
                c.Milliseconds=e+3002;
                foreach(var t in chart.Taps.Where(t=>t.Time==e)){s.Contact(100+t.Ordinal,t.Lane,true);s.Contact(100+t.Ordinal,t.Lane,false);}
                foreach(var h in chart.Holds){int id=200+h.Ordinal;if(e==h.Start)s.Contact(id,h.Lane,true);if(e==h.Start+600)s.Contact(id,h.Lane,false);if(e==h.Start+700)s.Contact(id,h.Lane,true);if(e==h.End)s.Contact(id,h.Lane,false);}
                s.Frame();if(e%100==0)track.Refresh(s.Core);
            }
            track.Refresh(s.Core);Check(s.Core!.Result!.Pure==chart.JudgmentUnits&&s.Core.Lost==0&&s.HeldCount==0,"completed mixed fixture");
        });
        File.WriteAllText(Path.Combine(evidenceDir,"hold-tests.json"),JsonSerializer.Serialize(new{passed,failed,skipped=0,outcomes},new JsonSerializerOptions{WriteIndented=true}));
        GD.Print($"R004 headless tests: {passed+failed}; passed: {passed}; failed: {failed}; skipped: 0");owner.GetTree().Quit(failed==0?0:1);
    }
}
