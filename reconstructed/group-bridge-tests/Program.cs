using Arconist.Core;
using Arconist.Bridge;
using System.Text.Json;
class Clock:IMonotonicClock{public long Milliseconds{get;set;}}
class Audio:IPausableBgmBackend
{
 public bool Playing,Paused,FailSeek,FailLoad;public int Starts;public double Position;public readonly List<string> Calls=new();
 public void Load(string r){if(FailLoad)throw new Exception("missing resource");Calls.Add("load");}
 public void PlayFromStart(){Starts++;Playing=true;Paused=false;Calls.Add("start");}
 public void StopAndUnload(){Playing=false;Paused=false;Calls.Add("stop");}
 public BgmStatus Inspect()=>new(Playing,Position,32,"engineering fake (not audibility)",paused:Paused);
 public void PausePlayback(){Paused=true;Calls.Add("pause");}
 public void SeekMilliseconds(int p){Calls.Add("seek:"+p);if(FailSeek)throw new Exception("seek failure");Position=p/1000.0;}
 public void UnpausePlayback(){Paused=false;Calls.Add("resume");}
}
class Program
{
 static int Main(string[] args)
 {
 string root=args.Length>0?args[0]:".",output=args.Length>1?args[1]:"group-bridge-evidence";Directory.CreateDirectory(output);int passed=0,failed=0;var outcomes=new List<object>();
 void Check(bool ok,string why){if(!ok)throw new Exception(why);}
 void Test(string name,Action body){try{body();passed++;outcomes.Add(new{name,status="PASS"});Console.WriteLine("PASS "+name);}catch(Exception e){failed++;outcomes.Add(new{name,status="FAIL",error=e.ToString()});Console.WriteLine("FAIL "+name+": "+e.Message);}}
 string Load(string n)=>File.ReadAllText(Path.Combine(root,"reconstructed/godot/content",n));
 (Clock,GameplaySession,Audio) New(string n="native_reverse_scroll.aff",int offset=0,Audio? backend=null){var c=new Clock();var a=backend??new Audio();var s=new GameplaySession(c,a);s.Start(Load(n),offset,n,"res://test");return(c,s,a);}
 void F(Clock c,GameplaySession s,int e,int delay=0){c.Milliseconds=e+3002+delay;s.Frame();}
 Test("actual keyboard mapping and separate mouse contact judge proper groups",()=>{var(c,s,a)=New();F(c,s,0);F(c,s,1500);Check(s.Key('K',true)&&s.Core!.Notes[0].Consumed&&!s.Core.Notes[1].Consumed,"default K");s.Key('K',false);Check(s.Contact(100,2,true)&&s.Core!.Notes[1].Consumed&&s.Core.Pure==2&&s.Core.Contacts.Single().Id==1,"mouse grouped D");s.Contact(100,2,false);Check(s.HeldCount==0&&s.Core!.ContactCount==0,"cleanup");s.Home();});
 Test("E036 disabled DOWN retains contact but yields no candidate",()=>{var(c,s,a)=New("native_noinput_group.aff");F(c,s,0);F(c,s,1500);s.Key('D',true);Check(s.HeldCount==1&&s.Core!.ContactCount==1&&s.Core.Candidates.Count==0&&s.Core.Score==0,"input transport versus eligibility");s.Key('D',false);s.Key('K',true);s.Key('K',false);F(c,s,1621);Check(s.Core!.Result!.Score==10000001&&s.Core.Result.Lost==0&&!s.Core.Notes[1].Missed&&s.Core.Notes[1].Active,"native result");});
 Test("repeat held key cannot manufacture duplicate DOWN",()=>{var(c,s,a)=New();F(c,s,0);F(c,s,1500);s.Key('D',true);Check(!s.Key('D',true)&&!s.Key('D',true,true)&&s.Core!.RecorderCalls==1,"echo guard");s.Key('D',false);s.Key('D',true);Check(s.Core!.Classifications.Single().Outcome=="guard_consumed"&&s.Core.Contacts.Single().Id==1,"consumption not input-repeat cooldown");s.Home();});
 Test("group MOVE does not judge or advance frame time",()=>{var(c,s,a)=New();F(c,s,0);F(c,s,1400);s.Contact(100,3,true);int frame=s.Core!.LastFrameTime;c.Milliseconds=4502;s.MoveContact(100,2);Check(s.Core.Pure==0&&s.Core.LastFrameTime==frame&&s.Core.Timeline.EffectiveTime==1400,"MOVE boundary");s.Home();});
 Test("positive and negative offsets keep one clock and forward BGM",()=>{foreach(int offset in new[]{-120,0,120}){var(c,s,a)=New(offset:offset);c.Milliseconds=3000-offset;s.Frame();Check(!s.Core!.Timeline.MusicStarted,"strict equality");c.Milliseconds=3002-offset;s.Frame();Check(s.Core.Timeline.EffectiveTime==-offset&&a.Starts==1,"anchor");F(c,s,1200);Check(s.Core.Timeline.EffectiveTime==1200&&s.Core.Notes[1].Depth==1213&&a.Starts==1,"shared forward clock");s.Home();}});
 Test("60second pause freezes both groups and dismiss restores DOWN",()=>{var(c,s,a)=New();F(c,s,0);F(c,s,1200);var before=s.Core!.Notes.Select(n=>n.Depth).ToArray();s.Pause();F(c,s,1200,60000);s.FocusReturned();Check(s.PauseModalActive&&s.Core.Paused&&s.Core.Notes.Select(n=>n.Depth).SequenceEqual(before)&&!s.Key('D',true),"frozen modal");Check(s.Resume()&&!s.PauseModalActive&&s.Core.Pure==0,"dismiss without DOWN");Check(a.Calls.TakeLast(3).SequenceEqual(new[]{"pause","seek:1200","resume"}),"audio order");F(c,s,1500,60000);s.Key('K',true);s.Key('K',false);s.Key('D',true);Check(s.Core.Pure==2,"input restored");s.Home();});
 Test("failed seek preserves paused group caches and supports retry",()=>{var(c,s,a)=New();F(c,s,0);F(c,s,1200);s.Pause();c.Milliseconds+=60000;a.FailSeek=true;Check(!s.Resume()&&s.PauseModalActive&&s.Core!.Timeline.EffectiveTime==1200&&s.Core.Notes[1].Depth==1213,"error state");a.FailSeek=false;Check(s.Resume()&&s.Core!.Pure==0,"retry");s.Home();});
 Test("preroll interruption does not start music early",()=>{var(c,s,a)=New();c.Milliseconds=1000;s.Frame();s.Pause();c.Milliseconds=61000;s.Frame();s.Resume();Check(!s.Core!.Timeline.MusicStarted&&a.Starts==0&&!a.Calls.Any(x=>x.StartsWith("seek")),"preroll");c.Milliseconds=63000;s.Frame();Check(a.Starts==0,"equality");c.Milliseconds++;s.Frame();Check(a.Starts==1&&s.Core.Timeline.EffectiveTime==0,"strict boundary");s.Home();});
 Test("focus cancels contacts but never resumes grouped chart",()=>{var(c,s,a)=New();F(c,s,0);F(c,s,1100);s.Key('D',true);s.FocusLost();c.Milliseconds+=60000;s.FocusReturned();s.Frame();Check(s.PauseModalActive&&s.Core!.Paused&&s.HeldCount==0&&s.Core.ContactCount==0&&s.Core.Timeline.EffectiveTime==1100,"focus");s.Resume();Check(s.Core!.Pure==0,"no invented input");s.Home();});
 Test("audio unavailable does not change grouped judgments and results",()=>{var(c,s,a)=New(backend:new Audio{FailLoad=true});F(c,s,0);F(c,s,1500);s.Key('K',true);s.Key('K',false);s.Key('D',true);s.Key('D',false);F(c,s,1621);Check(s.Core!.Result!.Score==10000002&&(double)s.Core.Health==80.4000015258789&&a.Starts==0,"independent gameplay");});
 Test("result menu replay and different chart discard old groups and audio",()=>{var(c,s,a)=New();F(c,s,0);F(c,s,1500);s.Key('K',true);s.Key('K',false);s.Key('D',true);F(c,s,1621);var old=s.Core!.TimingGroups[1];Check(s.HeldCount==0&&!a.Playing&&s.Core.Result!.Pure==2,"completion");s.Home();s.Start(Load("native_noinput_group.aff"),0,"new","res://test");Check(!ReferenceEquals(old,s.Core!.TimingGroups[1])&&!s.Core.Timeline.MusicStarted&&s.Core.Pure==0&&!s.Core.Notes[1].Consumed&&s.HeldCount==0,"fresh groups");s.Home();s.Start(Load("native_linked_arc_successors.aff"));Check(s.Core!.TimingGroups.Count==1&&s.Core.ArcGroups.Count==1,"old linked choice");s.Home();});
 File.WriteAllText(Path.Combine(output,"group-bridge-tests.json"),JsonSerializer.Serialize(new{passed,failed,skipped=0,outcomes},new JsonSerializerOptions{WriteIndented=true}));Console.WriteLine($"R010 bridge: {passed+failed}; passed:{passed}; failed:{failed}; skipped:0");return failed==0?0:1;
 }
}
