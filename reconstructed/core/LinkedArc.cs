namespace Arconist.Core;

public sealed class ArcRecordDefinition
{
    public int Time {get;}public int Weight {get;}
    internal ArcRecordDefinition(int time,int weight){Time=time;Weight=weight;}
}
public sealed class ArcGroupDefinition
{
    public string Id=>"group:"+Root.Id;
    public Arc Root {get;}public Arc Successor {get;}
    internal ArcGroupDefinition(Arc root,Arc successor){Root=root;Successor=successor;}
}
internal static class OrdinaryPairLinker
{
    internal static void LinkAndGenerate(IReadOnlyList<Arc> arcs)
    {
        int pairs=0;
        for(int i=1;i<arcs.Count;i++)
        {
            var a=arcs[i-1];var b=arcs[i];
            if((long)b.Start>=a.End+1000L)continue; // Preserve old isolated/trace spacing.
            bool constant=a.X0==a.X1&&a.Y0==a.Y1&&b.X0==b.X1&&b.Y0==b.Y1;
            bool strict=!a.Trace&&!b.Trace&&a.Children.Count==0&&b.Children.Count==0&&
                a.SourceOrder<b.SourceOrder&&a.End==b.Start&&constant&&a.X1==b.X0&&a.Y1==b.Y0&&a.Color==0&&b.Color==0&&
                a.Bpm==120&&b.Bpm==120&&a.Density==1&&b.Density==1&&a.TimingTime==b.TimingTime&&
                a.End-a.Start>=1000&&b.End-b.Start>=1000&&(a.End-a.Start)%250==1&&(b.End-b.Start)%250==0;
            // Declared R009 subset: exact adjacency, one constant pair, same timing.
            // No approximation of native9ms/.1 tolerances or graph selection.
            if(!strict||pairs!=0||a.Predecessor!=null||a.Successors.Count!=0||b.Predecessor!=null)
                throw new NotSupportedException("Only one unambiguous exact constant ordinary color0 pair is supported near another arc; branches/cycles/tolerances/trace links deferred.");
            var group=new ArcGroupDefinition(a,b);a.Group=b.Group=group;
            a.successors.Add(b);b.Predecessor=a;b.GenerationFlag=1;pairs++;
        }
        foreach(var arc in arcs)arc.GenerateRecords(); // Only after all links/flags.
    }
}
public sealed class ArcLinkScan
{
    public string Arc {get;}public string? Predecessor {get;}public int? PredecessorRecord {get;}
    public int? OwnRecord {get;}public string? Successor {get;}public int? SuccessorRecord {get;}
    internal ArcLinkScan(ArcState arc)
    {
        Arc=arc.Id;Predecessor=arc.Predecessor?.Id;
        PredecessorRecord=arc.Predecessor?.Records.LastOrDefault(r=>!r.Resolved)?.Time;
        OwnRecord=arc.Records.FirstOrDefault(r=>!r.Resolved)?.Time;
        var next=arc.Successors.SingleOrDefault();Successor=next?.Id;
        SuccessorRecord=next?.Records.FirstOrDefault(r=>!r.Resolved)?.Time;
    }
}
public sealed class ArcGroupState
{
    public string Id {get;}
    public IReadOnlyList<ArcState> Members {get;}
    public bool Active {get;internal set;}
    public bool CacheRelated {get;internal set;}
    public bool Accepted {get;internal set;}
    public float Window=>0;
    public IReadOnlyList<int> TimestampHistory=>Array.Empty<int>();
    public string WindowBehavior=>"UNSUPPORTED_NONEMPTY_TIMESTAMP_HISTORY";
    internal ArcGroupState(ArcGroupDefinition definition,ArcState root,ArcState next)
    {Id=definition.Id;Members=Array.AsReadOnly(new[]{root,next});}
    internal void Accept(ArcState arc)
    {
        // E038 consumes real links, but timestamp history is empty and extension
        // store15e015c is never entered. Do not fabricate a group window.
        if(TimestampHistory.Count!=0)throw new NotSupportedException("Nonempty group timestamp/window behavior is unsupported.");
        arc.LastLinkScan=new ArcLinkScan(arc);Active=Accepted=true;
    }
}
// Observations taken AFTER each genuine recorder operation, never multiplied gains.
public sealed class RecorderObservation
{
    public int Sequence {get;}public string Note {get;}public int? Checkpoint {get;}
    public string Outcome {get;}public int EffectiveTime {get;}
    public int Pure {get;}public int Shining {get;}public int Far {get;}public int Lost {get;}
    public int Score {get;}public int Combo {get;}public float Health {get;}
    internal RecorderObservation(int sequence,string note,int? checkpoint,string outcome,int now,Kernel k)
    {Sequence=sequence;Note=note;Checkpoint=checkpoint;Outcome=outcome;EffectiveTime=now;Pure=k.Pure;Shining=k.Shining;Far=k.Far;Lost=k.Lost;Score=k.Score;Combo=k.Combo;Health=k.Health;}
}
