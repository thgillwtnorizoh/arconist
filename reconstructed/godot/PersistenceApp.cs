using Godot;
using Arconist.Bridge;
using Arconist.Records;
namespace Arconist.GodotApp;

public partial class Main
{
    private sealed class RecordProbeClock:IMonotonicClock{public long Milliseconds{get;set;}}
    private RecordProbeClock? recordProbeClock;
    private int recordSelection=-1;
    private ChartIdentity? selectedRecordIdentity;
    internal LocalRecordStore RecordStore {get;private set;}=null!;
    internal SessionRecords RecordSessions {get;private set;}=null!;
    internal RecordPanel RecordDisplay {get;private set;}=null!;
    internal GameplaySession RecordProbeSession=>session;
    private bool IsRecordProcessProbe=>DisplayServer.GetName()=="headless"&&OS.GetCmdlineUserArgs().Any(a=>a=="--records-process-write"||a=="--records-process-read");
    private IMonotonicClock MakeGameplayClock()
    {if(IsRecordProcessProbe){recordProbeClock=new RecordProbeClock();return recordProbeClock;}return new GodotClock();}
    private void InitializeRecords()
    {
        string root=ProjectSettings.GlobalizePath("user://");
        // Deterministic process tests are headless only, isolated from owner data.
        // Exported owner flow always defaults to the application-owned user://.
        if(IsRecordProcessProbe)
        {
            string arg=OS.GetCmdlineUserArgs().Single(a=>a.StartsWith("--records-probe-root=",StringComparison.Ordinal));root=Path.GetFullPath(arg.Substring("--records-probe-root=".Length));
        }
        RecordStore=new LocalRecordStore(RecordPaths.ForUserData(root));
        RecordSessions=new SessionRecords(session,RecordStore);
        RecordDisplay=new RecordPanel{Position=new Vector2(692,350)};AddChild(RecordDisplay);
    }
    private void RefreshRecords()
    {
        if(RecordDisplay==null||charts==null||charts.Selected<0||chartData.Count==0)return;
        try
        {
            var selected=ChartChoices[charts.Selected];var registration=BundledCatalog.Find(selected.file);
            if(recordSelection!=charts.Selected){selectedRecordIdentity=registration.Identity(chartData[charts.Selected]);recordSelection=charts.Selected;}
            RecordDisplay.Refresh(RecordStore,selectedRecordIdentity!,RecordSessions.LastOutcome);
        }
        catch(Exception e){RecordDisplay.ShowError("Record identity/display unavailable: "+e.Message);}
    }
    internal void SelectRecordProbeChart(string file,bool begin)
    {
        int index=Array.FindIndex(ChartChoices,c=>c.file==file);if(index<0)throw new ArgumentException("Unknown bundled chart");
        charts.Select(index);if(begin)Begin();else{UpdateHud();QueueRedraw();}
    }
    internal void AdvanceRecordProbe(long wall)
    {if(recordProbeClock==null)throw new InvalidOperationException("Headless process clock only");recordProbeClock.Milliseconds=wall;session.Frame();track.Refresh(session.Core);UpdateHud();}
    private void RunRecordTests()=>PersistenceValidation.Run(this,evidenceDir);
    private void RunRecordProcess()=>PersistenceValidation.RunProcess(this,evidenceDir,OS.GetCmdlineUserArgs().Contains("--records-process-write"));
    private void CloseRecords(){RecordSessions?.Dispose();RecordStore?.Dispose();}
}
