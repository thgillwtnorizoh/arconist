using Arconist.Bridge;
using Arconist.Core;
namespace Arconist.Records;

// Completion observer is downstream of immutable GameResult; no kernel edits.
public sealed class SessionRecords:IDisposable
{
    private readonly GameplaySession session;
    private readonly LocalRecordStore store;
    private readonly Func<DateTimeOffset> utcNow;
    private ChartIdentity? pending;
    private Kernel? boundCore,attemptedCore;
    public ChartIdentity? CurrentIdentity {get;private set;}
    public RecordOutcome? LastOutcome {get;private set;}
    public int CompletionAttempts {get;private set;}
    public SessionRecords(GameplaySession session,LocalRecordStore store,Func<DateTimeOffset>? utcNow=null)
    {this.session=session;this.store=store;this.utcNow=utcNow??(()=>DateTimeOffset.UtcNow);session.Changed+=Observe;}
    public void Start(string file,string aff,int userOffset=0,string? audioResource=null,int arcHeight=500)
    {
        var registration=BundledCatalog.Find(file);pending=registration.Identity(aff);
        try{session.Start(aff,userOffset,file,audioResource,arcHeight,registration.Profile);}
        finally{pending=null;}
    }
    private void Observe(string kind)
    {
        if(kind=="START"){CurrentIdentity=pending;boundCore=session.Core;attemptedCore=null;LastOutcome=null;return;}
        if(kind=="HOME"){CurrentIdentity=null;boundCore=null;attemptedCore=null;return;}
        var core=session.Core;
        if(kind!="RESULT"||core==null||!ReferenceEquals(core,boundCore)||ReferenceEquals(core,attemptedCore)||!core.Finished||core.Result==null||CurrentIdentity==null)return;
        attemptedCore=core;CompletionAttempts++;
        try{LastOutcome=store.Record(CurrentIdentity,SavedResult.Capture(core.Result,utcNow()));}
        catch(Exception e){LastOutcome=new(CurrentIdentity.Key,false,false,false,false,"ERROR","Record save failed: "+e.Message);}
    }
    public void Dispose()=>session.Changed-=Observe;
}
