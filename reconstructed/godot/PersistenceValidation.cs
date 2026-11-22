using Godot;
using Arconist.Core;
using Arconist.Bridge;
using Arconist.Records;
using System.Text.Json;
using System.Security.Cryptography;
namespace Arconist.GodotApp;
public static class PersistenceValidation
{
 sealed class Clock:IMonotonicClock{public long Milliseconds{get;set;}}
 static string Aff()=>Godot.FileAccess.GetFileAsString("res://content/ordinary_two_tap.aff");
 static ChartIdentity Id()=>BundledCatalog.Find("ordinary_two_tap.aff").Identity(Aff());
 static SavedResult Prepared(int score,int cat,long date)=>new(score,10,10,cat==3?0:1,cat is 2 or 3?0:1,99,80,cat,10,0,0,date,unchecked((int)date),1,0);
 static void Complete(GameplaySession s,Clock c,bool hit=true){foreach(var p in new[]{(1000,'J'),(2000,'F')}){c.Milliseconds=p.Item1+3002;s.Frame();if(hit){s.Key(p.Item2,true);s.Key(p.Item2,false);}}c.Milliseconds=5123;s.Frame();}
 public static void Run(Main app,string evidenceDir)
 {
  int passed=0,failed=0,index=0;var outcomes=new List<object>();
  void C(bool ok,string why){if(!ok)throw new Exception(why);}
  void T(string name,Action body){try{body();passed++;outcomes.Add(new{name,status="PASS"});GD.Print("PASS W2-03 "+name);}catch(Exception e){failed++;outcomes.Add(new{name,status="FAIL",error=e.ToString()});GD.Print("FAIL W2-03 "+name+": "+e.Message);}}
  string PathFor()=>RecordPaths.ForUserData(Path.Combine(evidenceDir,"case"+(++index)));
  RecordPanel Panel(){var p=new RecordPanel();app.AddChild(p);return p;}
  void Remove(RecordPanel p){app.RemoveChild(p);p.QueueFree();}
  (GameplaySession,SessionRecords,Clock) Session(LocalRecordStore store)
  {var c=new Clock();var s=new GameplaySession(c);var rec=new SessionRecords(s,store);rec.Start("ordinary_two_tap.aff",Aff());c.Milliseconds=3002;s.Frame();return(s,rec,c);}
  T("production startup and all26 compiled resource identities",()=>{C(app.RecordStore.FilePath==RecordPaths.ForUserData(ProjectSettings.GlobalizePath("user://")),"owner user-data path");foreach(var r in BundledCatalog.Entries){string aff=Godot.FileAccess.GetFileAsString("res://content/"+r.File);C(r.Identity(aff).ContentSha256==r.PackagedSha256,"packaged bytes "+r.File);app.SelectRecordProbeChart(r.File,false);C(app.RecordDisplay.IsInsideTree()&&!string.IsNullOrWhiteSpace(app.RecordDisplay.DisplayText),"actual UI binding");}});
  T("real panel shows No record without writing a score file",()=>{using var store=new LocalRecordStore(PathFor());var p=Panel();p.Refresh(store,Id());C(p.DisplayText.Contains("No record")&&p.DisplayedBestScore==null&&!p.ShowsError&&!File.Exists(store.FilePath),"missing record is explicit");Remove(p);});
  T("UI displays independently improving clear beside retained best score",()=>{using var store=new LocalRecordStore(PathFor());var p=Panel();store.Record(Id(),Prepared(9100000,1,101));var result=store.Record(Id(),Prepared(8900000,3,102));p.Refresh(store,Id(),result);C(p.DisplayedBestScore==9100000&&p.DisplayedClear==3&&p.DisplayText.Contains("9,100,000")&&p.DisplayText.Contains("stronger clear")&&store.Get(Id())!.BestScore.UtcUnixSeconds==101,"two independent decisions visible");Remove(p);});
  T("new production store and panel reload real persisted snapshot",()=>{string path=PathFor();using(var store=new LocalRecordStore(path))store.Record(Id(),Prepared(9200000,3,100));using var fresh=new LocalRecordStore(path);var p=Panel();p.Refresh(fresh,Id());C(fresh.LoadedFromDisk&&p.DisplayedBestScore==9200000&&p.DisplayedClear==3&&p.DisplayText.Contains("Loaded")&&p.TooltipText.Contains("final LOST0"),"readback not memory stub");Remove(p);});
  T("natural GameResult reaches actual panel via completion observer",()=>{using var store=new LocalRecordStore(PathFor());var(s,rec,c)=Session(store);using(rec){Complete(s,c);var p=Panel();p.Refresh(store,Id(),rec.LastOutcome);C(s.Core!.Result!.Score==10000002&&p.DisplayedBestScore==10000002&&p.DisplayedClear==3&&rec.CompletionAttempts==1&&store.SuccessfulWrites==1,"natural completion");Remove(p);s.Home();}});
  T("repeated UI refresh and chart selection never writes or leaks records",()=>{using var store=new LocalRecordStore(PathFor());store.Record(Id(),Prepared(9100000,3,100));var p=Panel();for(int i=0;i<100;i++)p.Refresh(store,Id());var other=BundledCatalog.Find("native_widen_lanes.aff").Identity(Godot.FileAccess.GetFileAsString("res://content/native_widen_lanes.aff"));p.Refresh(store,other);C(p.DisplayedBestScore==null&&p.DisplayText.Contains("No record"),"separate selected identity");p.Refresh(store,Id());C(p.DisplayedBestScore==9100000&&store.SuccessfulWrites==1&&store.WriteAttempts==1,"no UI writes");Remove(p);});
  T("corrupt storage stays untouched and visible while gameplay completes",()=>{string path=PathFor();Directory.CreateDirectory(Path.GetDirectoryName(path)!);File.WriteAllText(path,"truncated{");using var store=new LocalRecordStore(path);var(s,rec,c)=Session(store);using(rec){Complete(s,c);var p=Panel();p.Refresh(store,Id(),rec.LastOutcome);C(p.ShowsError&&p.DisplayText.Contains("RECORD ERROR")&&!p.DisplayText.Contains("No record")&&p.TooltipText.Contains(path),"visible error/recovery path");C(s.Core!.Result!.Score==10000002&&File.ReadAllText(path)=="truncated{"&&rec.LastOutcome?.Success==false,"judgments unaffected");Remove(p);s.Home();}});
  T("actual write failure cannot show a saved-success message",()=>{using var store=new LocalRecordStore(PathFor());store.Record(Id(),Prepared(9000000,1,100));Directory.CreateDirectory(store.BackupPath);var result=store.Record(Id(),Prepared(9200000,3,101));var p=Panel();p.Refresh(store,Id(),result);C(p.ShowsError&&!result.Success&&store.Get(Id())!.BestScore.Score==9000000&&store.SuccessfulWrites==1,"failure remains failure");Remove(p);});
  T("pause early menu focus and uncompleted retry never create record",()=>{using var store=new LocalRecordStore(PathFor());var(s,rec,c)=Session(store);using(rec){c.Milliseconds=4002;s.Frame();s.Pause();c.Milliseconds+=60000;s.Frame();s.FocusLost();s.FocusReturned();s.Home();rec.Start("ordinary_two_tap.aff",Aff());s.Home();C(store.WriteAttempts==0&&rec.CompletionAttempts==0&&!File.Exists(store.FilePath),"lifecycle eligibility");}});
  T("ordinary category0 completion saved without changing result layout",()=>{using var store=new LocalRecordStore(PathFor());var(s,rec,c)=Session(store);using(rec){Complete(s,c,false);var p=Panel();p.Refresh(store,Id(),rec.LastOutcome);C(p.DisplayedBestScore==0&&p.DisplayedClear==0&&s.Core!.Result!.Lost==2,"failure completion is eligible");C(p.Size==new Vector2(336,48)&&p.GetChildren().OfType<Label>().Single().Text.Split('\n').Length==2,"two-line best panel; current result stays separate");Remove(p);s.Home();}});
  app.SelectRecordProbeChart("widen_lanes_practice.aff",false);
  File.WriteAllText(Path.Combine(evidenceDir,"record-headless.json"),JsonSerializer.Serialize(new{passed,failed,skipped=0,outcomes,human="PENDING",newIndependent="NOT RUN"},new JsonSerializerOptions{WriteIndented=true}));GD.Print($"W2-03 headless records: {passed+failed}; passed:{passed}; failed:{failed}; skipped:0");app.GetTree().Quit(failed==0?0:1);
 }
 public static void RunProcess(Main app,string evidenceDir,bool write)
 {
  int failed=0;string? error=null;
  try
  {
   if(app.RecordStore.HasError)throw new Exception(app.RecordStore.Detail);
   if(write)
   {
    if(File.Exists(app.RecordStore.FilePath))throw new Exception("Probe writer requires a fresh isolated data directory");
    app.SelectRecordProbeChart("ordinary_two_tap.aff",true);app.AdvanceRecordProbe(3002);
    app.AdvanceRecordProbe(4002);app.RecordProbeSession.Key('J',true);app.RecordProbeSession.Key('J',false);
    app.AdvanceRecordProbe(5002);app.RecordProbeSession.Key('F',true);app.RecordProbeSession.Key('F',false);
    app.AdvanceRecordProbe(5123);
    if(app.RecordSessions.LastOutcome?.Written!=true||app.RecordProbeSession.Core?.Result?.Score!=10000002||app.RecordStore.SuccessfulWrites!=1)throw new Exception("Normal Main/session result did not persist once");
   }
   else
   {
    app.SelectRecordProbeChart("ordinary_two_tap.aff",false);
    if(!app.RecordStore.LoadedFromDisk||app.RecordProbeSession.Core!=null||app.RecordStore.SuccessfulWrites!=0)throw new Exception("Fresh Main must reload before gameplay without writing");
   }
   if(app.RecordDisplay.DisplayedBestScore!=10000002||app.RecordDisplay.DisplayedClear!=3||!app.RecordDisplay.DisplayText.Contains("10,000,002"))throw new Exception("Real Main UI did not display the loaded best");
  }
  catch(Exception e){failed=1;error=e.ToString();}
  string file=app.RecordStore.FilePath;string? hash=File.Exists(file)?Convert.ToHexString(SHA256.HashData(File.ReadAllBytes(file))):null;
  string kind=write?"write":"read";
  File.WriteAllText(Path.Combine(evidenceDir,"record-process-"+kind+".json"),JsonSerializer.Serialize(new{passed=failed==0?1:0,failed,skipped=0,error,file,sha256=hash,display=app.RecordDisplay.DisplayText,loaded=app.RecordStore.LoadedFromDisk,writes=app.RecordStore.SuccessfulWrites,record=app.RecordStore.Get(Id()),boundary="Real headless Main + production user-data path builder; deterministic input callbacks, not physical GUI qualification"},new JsonSerializerOptions{WriteIndented=true}));
  GD.Print($"W2-03 process {kind}: 1; passed:{(failed==0?1:0)}; failed:{failed}; skipped:0");app.GetTree().Quit(failed==0?0:1);
 }
}
