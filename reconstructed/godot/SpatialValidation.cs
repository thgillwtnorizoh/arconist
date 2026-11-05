using Godot;
using Arconist.Core;
using Arconist.Bridge;
using System.Text.Json;

namespace Arconist.GodotApp;

// Executed by the real Godot .NET runtime with actual Camera3D APIs. This mode
// tests production geometry/bridge; it never participates in graphical play.
public static class SpatialValidation
{
    private sealed class Clock : IMonotonicClock { public long Milliseconds { get; set; } }
    public static void Run(Node owner, SpatialTrack track, string evidenceDir)
    {
        var outcomes=new List<object>(); int passed=0,failed=0;
        void Check(bool value,string name) { if (!value) throw new Exception(name); }
        void Test(string name,Action action) { try { action();passed++;outcomes.Add(new{name,status="PASS"});GD.Print("PASS R003 "+name); } catch(Exception e) { failed++;outcomes.Add(new{name,status="FAIL",error=e.Message});GD.Print("FAIL R003 "+name+": "+e.Message); } }
        const string aff="AudioOffset:0\n-\ntiming(0,120.00,4.00);(1000,3);(2000,2);";
        Kernel Core(string chart=aff) { var k=new Kernel(Chart.Parse(chart));k.Frame(0);k.Frame(3002);return k; }
        Vector2 Project(Vector3 p) => track.Camera.UnprojectPosition(p);
        Test("real perspective camera and mesh tree",()=>Check(track.Camera.Projection==Camera3D.ProjectionType.Perspective && track.GetChildren().OfType<MeshInstance3D>().Count()>=19,"3D nodes"));
        for(int lane=2;lane<=5;lane++) { int l=lane;
            Test($"lane {l} native integer placement",()=>Check(SpatialTrack.NativeX(l)==new[]{-638,-213,212,637}[l-2],"native X"));
            Test($"lane {l} actual Camera3D ray roundtrip",()=> {
                var p=SpatialTrack.World(SpatialTrack.NativeX(l),0,0);int picked=track.Pick(Project(p),out var hit);
                Check(picked==l && hit.DistanceTo(p)<0.0001f,"roundtrip");
            });
        }
        Test("uniform reversible native axes",()=>Check((SpatialTrack.World(-638,4,-4044)/SpatialTrack.Unit-new Vector3(-638,4,-4044)).Length()<0.001f,"scale"));
        Test("near/far projected dimensions",()=> {
            float Width(int z)=>Math.Abs(Project(SpatialTrack.World(191,4,z)).X-Project(SpatialTrack.World(-191,4,z)).X);
            Check(Width(0)>Width(-4000)*2,"perspective size");
            Check(Project(SpatialTrack.World(212,4,0)).Y>Project(SpatialTrack.World(212,4,-4000)).Y,"depth screen position");
        });
        Test("judgment Z alignment at E1500",()=> {var k=Core("AudioOffset:0\n-\ntiming(0,120.00,4.00);(1500,3);");k.Frame(4502);Check(SpatialTrack.NotePosition(k,k.Notes[0]).Z==0 && SpatialTrack.NotePosition(k,k.Notes[0]).Y==4*SpatialTrack.Unit,"line alignment");});
        Test("E032 native depth samples",()=> {
            var k=Core("AudioOffset:0\n-\ntiming(0,120.00,4.00);(1500,3);");
            int[] times={1000,1300,1499,1500,1501,1537,1538,1600,1601,1602}; int[] depths={-4044,-1617,-7,0,8,300,308,809,817,826};
            for(int i=0;i<times.Length;i++){k.Frame(times[i]+3002);Check(SpatialTrack.CurrentDepth(k,k.Notes[0])==depths[i],$"E{times[i]}");}
        });
        Test("E035 integer predepth order",()=> {var k=Core("AudioOffset:0\n-\ntiming(0,120.00,4.00);(1000,3);(1109,3);");k.Frame(4002);Check(k.Notes.Select(n=>SpatialTrack.CurrentDepth(k,n)).SequenceEqual(new[]{0,-881}),"E1000");k.Frame(4112);Check(k.Notes.Select(n=>SpatialTrack.CurrentDepth(k,n)).SequenceEqual(new[]{890,8}),"E1110");});
        Test("timing changes alter depth slope",()=> {var k=Core("AudioOffset:0\n-\ntiming(0,120.00,4.00);timing(1000,60.00,4.00);(2000,3);");float first=k.DepthAt(1000)-k.DepthAt(500),second=k.DepthAt(1500)-k.DepthAt(1000);Check(Math.Abs(first/second-2)<0.0001f,"piecewise integration");});
        Test("presentation reads effective clock without gameplay mutation",()=> {var k=Core();k.Frame(4002);var before=JsonSerializer.Serialize(new{k.LastFrameTime,k.Score,k.Health,k.Combo,k.ContactCount});for(int i=0;i<100;i++)track.Refresh(k);Check(before==JsonSerializer.Serialize(new{k.LastFrameTime,k.Score,k.Health,k.Combo,k.ContactCount}),"render mutated core");});
        Test("resolved versus expired presentation",()=> {var k=Core();k.Frame(4002);k.Down(4002,1,4);Check(k.Notes[0].Consumed && !SpatialTrack.Present(k,k.Notes[0]),"consumed");k.Up(1);k.Frame(5103);Check(k.Notes[1].Missed&&!SpatialTrack.Present(k,k.Notes[1]),"expired");});
        Test("presentation and active membership remain distinct",()=> {var k=Core("AudioOffset:0\n-\ntiming(0,120.00,4.00);(20000,3);");Check(!k.Notes[0].Active&&!SpatialTrack.Present(k,k.Notes[0]),"far inactive");Check(SpatialTrack.CurrentDepth(k,k.Notes[0])==(int)k.DepthAt(20000),"inactive predepth");});
        Test("strict native depth region rejection",()=> {foreach(int z in new[]{-501,-500,500,501})Check(SpatialTrack.LaneAt(SpatialTrack.World(212,0,z))==0,"depth");Check(SpatialTrack.LaneAt(SpatialTrack.World(212,0,499))==4,"inner depth");});
        Test("bounded outside-track rejection",()=> {foreach(int x in new[]{-10000,-851,851,10000})Check(SpatialTrack.LaneAt(SpatialTrack.World(x,0,0))==0,"outer X");});
        Test("native signed X asymmetry",()=> {foreach(var pair in new[]{(-426,2),(-425,3),(-1,3),(0,4),(424,4),(425,0),(426,5)})Check(SpatialTrack.LaneAt(SpatialTrack.World(pair.Item1,0,0))==pair.Item2,$"X{pair.Item1}");});
        Test("invalid parallel and backwards ray rejection",()=> {Check(!SpatialTrack.GroundIntersection(Vector3.Up,Vector3.Right,out _),"parallel");Check(!SpatialTrack.GroundIntersection(Vector3.Up,Vector3.Up,out _),"backwards");Check(!SpatialTrack.GroundIntersection(new(float.NaN,1,0),Vector3.Down,out _),"NaN origin");Check(!SpatialTrack.GroundIntersection(Vector3.Up,new(0,float.PositiveInfinity,0),out _),"infinite ray");Check(SpatialTrack.LaneAt(new(float.NaN,0,0))==0,"NaN hit");});
        Test("invalid viewport coordinates rejected",()=> {Check(track.Pick(new(float.NaN,0),out _)==0 && track.Pick(new(-1,100),out _)==0 && track.Pick(new(99999,100),out _)==0,"viewport bounds");});
        Test("controlled camera changes projection and roundtrip",()=> {var p=SpatialTrack.World(212,0,0);var before=Project(p);track.SetView(true);Check(before.DistanceTo(Project(p))>5 && track.Pick(Project(p),out _)==4,"camera move");track.SetView(false);});
        foreach(var size in new[]{new Vector2I(610,550),new Vector2I(800,600),new Vector2I(1280,720),new Vector2I(960,540)}) {var v=size;
            Test($"viewport {v.X}x{v.Y} finite aligned lanes",()=> { var vp=(SubViewport)track.GetViewport();var container=(SubViewportContainer)vp.GetParent();var old=container.Size;container.Size=v;Check(vp.Size==v,"requested size actually applied");foreach(int l in Enumerable.Range(2,4)){var p=Project(SpatialTrack.World(SpatialTrack.NativeX(l),0,0));Check(p.IsFinite()&&track.Pick(p,out _)==l,"resize alignment");}container.Size=old; });
        }
        Test("projected wrong/correct clicks reach same core and clean pointer100",()=> {var clock=new Clock();var s=new GameplaySession(clock);s.Start(aff);clock.Milliseconds=3002;s.Frame();clock.Milliseconds=4002;s.Frame();int PickLane(int l)=>track.Pick(Project(SpatialTrack.World(SpatialTrack.NativeX(l),0,0)),out _);s.Contact(100,PickLane(2),true);s.Contact(100,2,false);Check(s.Core!.Pure==0,"wrong click scored");s.Contact(100,PickLane(4),true);Check(s.Core.Pure==1&&s.Core.ContactCount==1,"correct click");s.Contact(100,4,false);Check(s.Core.ContactCount==0&&s.HeldCount==0,"cleanup");});
        Test("camera movement preserves clock and judgment",()=> {var k=Core();k.Frame(4002);int e=k.Timeline.EffectiveTime;track.SetView(true);track.Refresh(k);Check(k.Timeline.EffectiveTime==e&&k.Score==0,"camera mutation");track.SetView(false);});
        File.WriteAllText(Path.Combine(evidenceDir,"spatial-tests.json"),JsonSerializer.Serialize(new{passed,failed,skipped=0,outcomes},new JsonSerializerOptions{WriteIndented=true}));
        GD.Print($"R003 spatial tests: {passed+failed}; passed: {passed}; failed: {failed}; skipped: 0");owner.GetTree().Quit(failed==0?0:1);
    }
}
