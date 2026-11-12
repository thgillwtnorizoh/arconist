using Arconist.Core;
using Arconist.Bridge;
using System.Text.Json;
class Clock:IMonotonicClock{public long Milliseconds{get;set;}}
class Program
{
 static int Main(string[] args)
 {
  string root=args.Length>0?args[0]:".",output=args.Length>1?args[1]:"linked-bridge-evidence";Directory.CreateDirectory(output);int passed=0,failed=0;var outcomes=new List<object>();
  void Check(bool ok,string why){if(!ok)throw new Exception(why);}
  void Test(string name,Action body){try{body();passed++;outcomes.Add(new{name,status="PASS"});Console.WriteLine("PASS "+name);}catch(Exception e){failed++;outcomes.Add(new{name,status="FAIL",error=e.ToString()});Console.WriteLine("FAIL "+name+": "+e.Message);}}
  string Load(string n)=>File.ReadAllText(Path.Combine(root,"reconstructed/godot/content",n));
  (Clock,GameplaySession) New(){var c=new Clock();var s=new GameplaySession(c);s.Start(Load("native_linked_arc_successors.aff"));c.Milliseconds=3002;s.Frame();c.Milliseconds=4002;s.Frame();s.Pointer(100,0,new SkyContact(new SkyPoint(0,300,0)),true);return(c,s);}
  SkyContact At()=>new(new SkyPoint(0,300,0));
  Test("one bridge DOWN retains ID through exact junction",()=>{var(c,s)=New();foreach(int e in new[]{1001,1125,1375,2000,2001,2002,2126,2376,2626}){c.Milliseconds=e+3002;s.Frame();Check(s.Core!.Contacts.Single().Id==0&&s.HeldCount==1,"same contact");}Check(s.Core!.Pure==7&&s.Core.Arcs[1].Holding,"successor without DOWN");});
  Test("weighted bridge events are seven units from six record identities",()=>{var(c,s)=New();var events=new List<JudgmentEvent>();s.JudgmentsProduced+=e=>events.AddRange(e);foreach(int e in new[]{1001,1125,1375,2001,2126,2376,2626}){c.Milliseconds=e+3002;s.Frame();}Check(events.Count==7&&events.Count(e=>e.CheckpointTime==1500)==2&&events.Select(e=>(e.Note,e.CheckpointTime)).Distinct().Count()==6&&s.Core!.RecorderCalls==7,"unit events versus record guards");});
  Test("release before junction prevents stale successor contact",()=>{var(c,s)=New();c.Milliseconds=4377;s.Frame();c.Milliseconds=5002;s.Frame();s.Pointer(100,0,null,false);c.Milliseconds=5003;s.Frame();Check(s.Core!.ContactCount==0&&!s.Core.Arcs[1].Holding&&s.Core.Arcs[1].Color.Owner==-1,"UP");});
  Test("foreign pointer cannot steal shared ownership",()=>{var(c,s)=New();c.Milliseconds=4003;s.Frame();s.Pointer(101,0,At(),true);s.MovePointer(100,0,new SkyContact(new SkyPoint(9000,300,0)));c.Milliseconds=5003;s.Frame();Check(s.Core!.ArcGroups[0].Active==false&&s.Core.Arcs[1].Color.Owner==0,"foreign rejected");});
  Test("manual junction pause60seconds retains actual contact",()=>{var(c,s)=New();c.Milliseconds=5002;s.Frame();s.Pause();c.Milliseconds=65002;s.Frame();Check(s.Core!.Timeline.EffectiveTime==2000&&s.Core.ContactCount==1&&s.Core.Pure==3,"freeze");s.Resume();Check(!s.PauseModalActive,"dismissed");c.Milliseconds=65003;s.Frame();Check(s.Core.Arcs[1].Holding&&s.Core.Pure==4&&s.Core.Contacts.Single().Id==0,"same contact junction");});
  Test("paused UP and CANCEL deliver cleanup and no phantom resume",()=>{foreach(bool cancel in new[]{false,true}){var(c,s)=New();c.Milliseconds=5002;s.Frame();s.Pause();if(cancel)s.Cancel(100);else s.Pointer(100,0,null,false);c.Milliseconds=65002;s.Resume();c.Milliseconds++;s.Frame();Check(s.Core!.ContactCount==0&&!s.Core.Arcs[1].Holding&&s.HeldCount==0,"cleanup");}});
  Test("focus loss cancels shared contact and never automatically resumes",()=>{var(c,s)=New();c.Milliseconds=5002;s.Frame();s.FocusLost();c.Milliseconds=65002;s.Frame();s.FocusReturned();Check(s.PauseModalActive&&s.Core!.Paused&&s.Core.ContactCount==0&&s.Core.Arcs[1].Color.Owner==-1,"focus policy");});
  Test("native terminal UP leaves activity until next frame and cache group byte",()=>{var(c,s)=New();foreach(int e in new[]{1001,1125,1375,2001,2126,2376,2626,2876}){c.Milliseconds=e+3002;s.Frame();}s.Pointer(100,0,null,false);Check(s.Core!.Score==10000007&&s.Core.Arcs[1].Holding&&s.Core.Arcs[1].Color.ReleaseTime==2876,"immediate UP");c.Milliseconds++;s.Frame();Check(!s.Core.Arcs[1].Holding&&!s.Core.ArcGroups[0].Active&&s.Core.ArcGroups[0].CacheRelated,"next frame group state");});
  Test("complete result menu and replay reset group owner and records",()=>{var(c,s)=New();foreach(int e in new[]{1125,1375,2001,2126,2376,2626,3502}){c.Milliseconds=e+3002;s.Frame();}Check(s.Core!.Result!.Score==10000007&&s.Core.Result.MaxCombo==7&&s.HeldCount==0,"result");var old=s.Core.ArcGroups[0];s.Home();s.Start(Load("native_linked_arc_successors.aff"));Check(!ReferenceEquals(old,s.Core!.ArcGroups[0])&&s.Core.Arcs[0].Color.Owner==-1&&s.Core.Pure==0&&!s.PauseModalActive,"fresh replay");});
  Test("extended practice production bridge completes N31",()=>{var c=new Clock();var s=new GameplaySession(c);s.Start(Load("linked_practice.aff"));c.Milliseconds=3002;s.Frame();for(int e=1;e<=12502;e++){c.Milliseconds=e+3002;if(e==4000)s.Pointer(100,0,At(),true);s.Frame();}Check(s.Core!.Result!.Score==10000031&&s.Core.Pure==31&&s.HeldCount==0,"complete practice");});
  File.WriteAllText(Path.Combine(output,"linked-bridge-tests.json"),JsonSerializer.Serialize(new{passed,failed,skipped=0,outcomes},new JsonSerializerOptions{WriteIndented=true}));Console.WriteLine($"R009 bridge: {passed+failed}; passed:{passed}; failed:{failed}; skipped:0");return failed==0?0:1;
 }
}
