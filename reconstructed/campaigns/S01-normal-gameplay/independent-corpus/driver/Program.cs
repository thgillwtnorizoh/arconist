using System.Text.Json;
using System.Text.Json.Nodes;
using Arconist.Core;
using Arconist.Bridge;

// Work1 adapter and comparator. No Work2 tests/comparator loaded; expectations are read-only.
sealed class Clock : IMonotonicClock { public long Milliseconds {get;set;} }
sealed class Audio : IPausableBgmBackend {
 public readonly List<string> Calls=new();bool playing,paused;
 public void Load(string r){Calls.Add("load");} public void PlayFromStart(){Calls.Add("play");playing=true;}
 public void StopAndUnload(){Calls.Add("stop");playing=false;paused=false;}
 public void PausePlayback(){Calls.Add("pause");paused=true;}
 public void SeekMilliseconds(int n){Calls.Add("seek:"+n);}
 public void UnpausePlayback(){Calls.Add("unpause");paused=false;}
 public BgmStatus Inspect()=>new(playing,0,100000,"Work1 fake output boundary",paused:paused);
}
static class Program {
 static int I(JsonNode n,string k,int d=0)=>n[k]?.GetValue<int>()??d;
 static JsonNode Snap(Kernel k)=>JsonSerializer.SerializeToNode(new {
  e=k.Timeline.EffectiveTime,lastFrameTime=k.LastFrameTime,contactStates=k.Contacts.Select(c=>new{pointer=c.Pointer,id=c.Id,lane=c.Lane}).ToArray(),raw=k.Timeline.RawTime,c=k.Timeline.Compensation,p=k.Timeline.PauseReference,b=k.Timeline.MusicAnchor,paused=k.Paused,
  n=k.Chart.JudgmentUnits,end=k.Chart.EndTime,pure=k.Pure,far=k.Far,lost=k.Lost,shining=k.Shining,score=k.Score,combo=k.Combo,max=k.MaxCombo,
  healthBits=BitConverter.SingleToInt32Bits(k.Health),contacts=k.ContactCount,ids=k.Contacts.Select(c=>c.Id).ToArray(),lanes=k.Contacts.Select(c=>c.Lane).ToArray(),
  candidates=k.Candidates.ToArray(),outcomes=k.Classifications.Select(c=>c.Outcome).ToArray(),finished=k.Finished,
  notes=k.Notes.Select(t=>new{time=t.Start,group=t.TimingGroupId,input=t.InputEnabled,active=t.Active,depth=t.Depth,bucket=t.Bucket,consumed=t.Consumed,missed=t.Missed,contact=t.Contact}).ToArray(),
  holds=k.Holds.Select(h=>new{latched=h.Latched,holding=h.Holding,resolved=h.Records.Select(r=>r.Resolved?1:0).ToArray(),activators=h.ActivatingContacts.ToArray()}).ToArray(),
  arcs=k.Arcs.Select(a=>new{holding=a.Holding,cache=a.CacheEnabled,owner=a.Color.Owner,predecessor=a.Predecessor?.Id,successors=a.Successors.Select(s=>s.Id).ToArray(),flag=a.Data.GenerationFlag,weights=a.Records.Select(r=>r.Weight).ToArray(),times=a.Records.Select(r=>r.Time).ToArray(),resolved=a.Records.Select(r=>r.Resolved?1:0).ToArray(),x=a.TargetX,y=a.TargetY}).ToArray(),
  children=k.ArcTaps.Select(c=>new{time=c.Start,consumed=c.Consumed,missed=c.Missed,contact=c.Contact,x=c.Local.X,y=c.Local.Y,z=c.Local.Z}).ToArray(),
  groups=k.TimingGroups.Select(g=>new{id=g.Id,active=g.Active,low=g.QueryLow,high=g.QueryHigh,scales=g.Records.Select(r=>r.Scale).ToArray()}).ToArray(),
  records=k.RecorderTrace.Select(r=>new{time=r.Checkpoint,pure=r.Pure,score=r.Score,healthBits=BitConverter.SingleToInt32Bits(r.Health)}).ToArray(),
  result=k.Result==null?null:new{pure=k.Result.Pure,far=k.Result.Far,lost=k.Result.Lost,recordedLost=k.Result.RecordedLost,score=k.Result.Score,health=k.Result.Health,category=k.Result.Category,max=k.Result.MaxCombo}
 })!;
 static string? Diff(JsonNode? e,JsonNode? a,string path) {
  if(e is JsonObject o){if(a is not JsonObject z)return path+": expected object";foreach(var kv in o){if(!z.ContainsKey(kv.Key))return path+"."+kv.Key+": missing";var d=Diff(kv.Value,z[kv.Key],path+"."+kv.Key);if(d!=null)return d;}return null;}
  if(e is JsonArray ar){if(a is not JsonArray br||ar.Count!=br.Count)return path+": array length";for(int i=0;i<ar.Count;i++){var d=Diff(ar[i],br[i],path+"["+i+"]");if(d!=null)return d;}return null;}
  return JsonNode.DeepEquals(e,a)?null:path+": expected "+e+", actual "+a;
 }
 static object Run(JsonNode c,string dir) {
  string id=c["id"]!.GetValue<string>();var trace=new List<object>();string? first=null;
  try {
   string aff=File.ReadAllText(Path.Combine(dir,c["aff"]!.GetValue<string>()));
   if(c["classification"]!.GetValue<string>()=="EXPECTED REJECTION"){
    try{Chart.Parse(aff);return new{id,status="FAIL",firstDifference="parse: expected NotSupportedException"};}
    catch(NotSupportedException){return new{id,status="PASS",firstDifference=(string?)null};}
   }
   var clock=new Clock();var audio=new Audio();var session=new GameplaySession(clock,audio);session.Start(aff,I(c,"userOffset"),id,"res://work1-fake",I(c,"height",0));
   var k=session.Core!;
   foreach(var (ev,index) in c["events"]!.AsArray().Select((v,i)=>(v!,i))){
    clock.Milliseconds=ev["wall"]?.GetValue<long>()??(3002L+I(ev,"e"));string op=ev["op"]!.GetValue<string>();int pointer=I(ev,"pointer",42),lane=I(ev,"lane",4);
    SkyContact? sky=ev["sky"] is JsonArray p?new SkyContact(new SkyPoint(p[0]!.GetValue<float>(),p[1]!.GetValue<float>(),p[2]!.GetValue<float>())):null;
    switch(op){case "FRAME":session.Frame();break;case "DOWN":session.Contact(pointer,lane,true);break;case "UP":session.Contact(pointer,lane,false);break;case "CANCEL":session.Cancel(pointer);break;
     case "SPATIAL":session.Pointer(pointer,lane,sky,true);break;case "MOVE":k.MoveSpatial(pointer,lane,sky);break;case "PAUSE":session.Pause();break;case "RESUME":session.Resume();break;
     case "RESTART":session.Start(aff,0,id,null,I(c,"height",0));k=session.Core!;break;case "HOME":session.Home();break;default:throw new Exception("Unknown op "+op);}
    var actual=Snap(k);actual["audio"]=JsonSerializer.SerializeToNode(audio.Calls.ToArray());actual["sessionHeld"]=session.HeldCount;actual["sessionHome"]=session.Core==null;
    var diff=ev["expect"]==null?null:Diff(ev["expect"],actual,"$.events["+index+"]");first??=diff;trace.Add(new{index,op,actual,difference=diff});
   }
  }catch(Exception e){first??="exception: "+e.GetType().Name+": "+e.Message;}
  return new{id,status=first==null?"PASS":"FAIL",firstDifference=first,trace};
 }
 public static int Main(string[] args){
  if(args.Length!=2)return 2;var root=Path.GetFullPath(args[0]);var manifest=JsonNode.Parse(File.ReadAllText(Path.Combine(root,"manifest.json")))!;var results=new List<object>();
  foreach(var entry in manifest["cases"]!.AsArray()){var c=JsonNode.Parse(File.ReadAllText(Path.Combine(root,entry!.GetValue<string>())))!;if(c["classification"]!.GetValue<string>()=="RESEARCH BLOCKED")continue;results.Add(Run(c,root));}
  var output=new{productionSha=manifest["productionSha"]!.GetValue<string>(),results};File.WriteAllText(args[1],JsonSerializer.Serialize(output,new JsonSerializerOptions{WriteIndented=true}));
  var parsed=JsonSerializer.SerializeToNode(output)!;return parsed["results"]!.AsArray().Any(r=>r!["status"]!.GetValue<string>()=="FAIL")?1:0;
 }
}
