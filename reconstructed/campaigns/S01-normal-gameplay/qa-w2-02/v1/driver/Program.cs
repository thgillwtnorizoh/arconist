using System.Text.Json;
using System.Text.Json.Nodes;
using Arconist.Core;
using Arconist.Bridge;
sealed class Clock:IMonotonicClock {public long Milliseconds{get;set;}}
static class Program {
 static List<object> checks=new();static string context="";static string? first;
 static void Eq<T>(string field,T expected,T actual){bool ok=JsonSerializer.Serialize(expected)==JsonSerializer.Serialize(actual);checks.Add(new{context,field,expected,actual,status=ok?"PASS":"FAIL"});if(!ok){first=context+"."+field;throw new Exception(first);}}
 static int Bits(float x)=>BitConverter.SingleToInt32Bits(x);
 static void Reject(string aff,ChartProfile profile){try{Chart.Parse(aff,profile);Eq("reject",true,false);}catch(NotSupportedException){Eq("reject",true,true);}}
 public static int Main(string[] args){var dir=args[0];var e=JsonNode.Parse(File.ReadAllText(Path.Combine(dir,"expectations.json")))!;string[] names={"control","camera","lanes"};
 try{
 for(int n=0;n<3;n++){
 context=names[n]+" parse";var aff=File.ReadAllText(Path.Combine(dir,names[n]+".aff"));var chart=Chart.Parse(aff,ChartProfile.S01Mixed);Eq("N",2,chart.JudgmentUnits);Eq("end",1620,chart.EndTime);Eq("lanes",new[]{3,6},chart.Taps.Select(t=>t.Lane).ToArray());Eq("raw",new[]{2,5},chart.Taps.Select(t=>t.RawLane).ToArray());Eq("controls",n==0?0:1,chart.SceneControls.Count);
 if(n>0){var c=chart.SceneControls[0];Eq("kind",n==1?5:6,(int)c.Kind);Eq("time",500,c.Time);Eq("duration",500f,c.Duration);Eq("direction",1,c.Direction);Reject(aff,ChartProfile.R010);}
 var clock=new Clock();var session=new GameplaySession(clock);session.Start(aff,profile:ChartProfile.S01Mixed);clock.Milliseconds=3002;session.Frame();var k=session.Core!;Eq("anchor",0,k.Timeline.EffectiveTime);float previous=1;
 for(int j=0;j<6;j++){int time=e["times"]![j]!.GetValue<int>();context=names[n]+" E"+time;clock.Milliseconds=3002+time;session.Frame();float g=e["g"]![n]![j]!.GetValue<float>(),w=e["w"]![n]![j]!.GetValue<float>();Eq("Gbits",Bits(g),Bits(k.Widening.G));Eq("Wbits",Bits(w),Bits(k.Widening.W));Eq("previousG",Bits(previous),Bits(k.Widening.PreviousG));previous=g;
 if(n>0){var c=k.Widening.Controls[0];Eq("processed",time>500,c.Processed);Eq("dispatch",time>500?(int?)501:null,c.DispatchedAt);if(time>=501)Eq("originalStart",500,n==1?k.Widening.Camera.Start:k.Widening.Lanes.Start);}
 }
 context=names[n]+" original probes";
 for(int i=0;i<2;i++){float x=i==0?40:950;var pair=GroundSpatial.Select(new SkyPoint(x,0,0),k.Widening.G,k.Widening.W);Eq("pair"+i,new[]{e["pairs"]![n]![i]![0]!.GetValue<int>(),e["pairs"]![n]![i]![1]!.GetValue<int>()},new[]{pair.Primary,pair.Secondary});int last=k.LastFrameTime;int pointer=42+i;session.GroundPointer(pointer,new SkyPoint(x,0,0),null,true);Eq("DOWN no FRAME",last,k.LastFrameTime);Eq("generated contact",i,k.Contacts.Single().Id);session.GroundPointer(pointer,new SkyPoint(x,0,0),null,false);Eq("UP contacts",0,k.ContactCount);}
 int hits=n==0?0:1;Eq("pure",hits,k.Pure);Eq("shining",hits,k.Shining);Eq("far",0,k.Far);Eq("lost",0,k.Lost);Eq("combo",hits,k.Combo);Eq("score",hits*5000001,k.Score);Eq("health",hits==0?0:1109445837,Bits(k.Health));
 if(n>0){var note=k.Notes.Single(t=>t.Lane==(n==1?3:6));Eq("consumed",true,note.Consumed);Eq("accepted contact",n==1?0:1,note.Contact);session.GroundPointer(44,new SkyPoint(n==1?40:950,0,0),null,true);Eq("duplicate pure",1,k.Pure);Eq("duplicate recorder",0,k.RecorderTrace.Count);session.Cancel(44);}
 clock.Milliseconds=4503;session.Frame();Eq("E1501 pure",hits,k.Pure);Eq("cleanup",0,k.ContactCount);Eq("held cleanup",0,session.HeldCount);Eq("no result",false,k.Finished);
 }
 context="E004 boundaries";
 foreach(var row in e["boundaries"]!.AsArray()){float x=row![0]!.GetValue<float>(),w=row[1]!.GetValue<float>();Eq("X"+x+" W"+w,row[2]!.GetValue<int>(),GroundSpatial.Select(new SkyPoint(x,0,0),1,w).Primary);}
 foreach(float z in new[]{-500f,500f,-501f,501f})Eq("strict depth"+z,0,GroundSpatial.Select(new SkyPoint(40,0,z),1,0).Primary);
 foreach(float z in new[]{-499.99f,499.99f})Eq("inside depth"+z,4,GroundSpatial.Select(new SkyPoint(40,0,z),1,0).Primary);
 context="ENGINEERING invalid inputs";foreach(float x in new[]{float.NaN,float.PositiveInfinity,float.NegativeInfinity})Eq("invalid",0,GroundSpatial.Select(new SkyPoint(x,0,0),1,0).Primary);
 Eq("invalid G",0,GroundSpatial.Select(new SkyPoint(0,0,0),0,0).Primary);Eq("invalid W",0,GroundSpatial.Select(new SkyPoint(0,0,0),1,2).Primary);
 context="RECONSTRUCTED lifecycle";var a=File.ReadAllText(Path.Combine(dir,"camera.aff"));var cl=new Clock();var se=new GameplaySession(cl);se.Start(a,profile:ChartProfile.S01Mixed);cl.Milliseconds=3002;se.Frame();cl.Milliseconds=3752;se.Frame();var core=se.Core!;se.GroundPointer(80,new SkyPoint(40,0,0),null,true);Eq("retained id",0,core.Contacts.Single().Id);se.Pause();cl.Milliseconds+=60000;se.Frame();Eq("paused E",750,core.Timeline.EffectiveTime);Eq("paused G",Bits(1.25f),Bits(core.Widening.G));Eq("retained",1,core.ContactCount);se.Resume();cl.Milliseconds++;se.Frame();Eq("resume E",751,core.Timeline.EffectiveTime);float u=251f*.5f;u/=500f;float expected=1f+u;Eq("resume f32 G",Bits(expected),Bits(core.Widening.G));se.Cancel(80);Eq("cancel",0,core.ContactCount);cl.Milliseconds=3002+60000+1500;se.Frame();se.GroundPointer(81,new SkyPoint(950,0,0),null,true);se.MoveGroundPointer(81,new SkyPoint(40,0,0),null);Eq("MOVE no judgment",0,core.Pure);se.Cancel(81);se.GroundPointer(82,new SkyPoint(40,0,0),null,true);Eq("fresh after MOVE",1,core.Pure);se.ReleaseAll();se.Start(a,profile:ChartProfile.S01Mixed);Eq("replay G",Bits(1f),Bits(se.Core!.Widening.G));Eq("replay score",0,se.Core.Score);Eq("replay contacts",0,se.Core.ContactCount);Eq("replay unprocessed",false,se.Core.Widening.Controls[0].Processed);se.Home();Eq("home core",true,se.Core==null);
 context="ENGINEERING grammar rejection";foreach(string control in new[]{"scenecontrol(500,enwidencamera,500,1);","scenecontrol(500,enwidencamera,500.00,0);","scenecontrol(500,trackhide,500.00,1);","scenecontrol(500,enwidenlanes,0.00,1);"})Reject(File.ReadAllText(Path.Combine(dir,"control.aff"))+control,ChartProfile.S01Mixed);
 }catch(Exception ex){first??="Harness exception: "+ex;}
 File.WriteAllText(args[1],JsonSerializer.Serialize(new{productionSha=e["productionSha"]!.GetValue<string>(),status=first==null?"PASS":"FAIL",firstDifference=first,assertions=checks.Count,checks},new JsonSerializerOptions{WriteIndented=true}));return first==null?0:1;
 }
}
