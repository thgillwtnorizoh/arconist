namespace Arconist.Core;

// A descriptor is not a clock. Every group uses the one Kernel.Timeline.
public sealed class TimingGroup
{
    public int Id { get; }
    public int SourceOrder { get; }
    public string Attribute { get; }
    public bool InputEnabled => Attribute != "noinput";
    public IReadOnlyList<Timing> Timings { get; }
    public int LifetimeEnd { get; internal set; } = int.MaxValue;
    internal TimingGroup(int id, int sourceOrder, string attribute, List<Timing> timings)
    { Id=id; SourceOrder=sourceOrder; Attribute=attribute; Timings=timings.AsReadOnly(); }
}

public sealed class GroupTimingRecord
{
    public Timing Source { get; }
    public int StartBound { get; }
    public int EndBound { get; }
    public float ScaledBpm { get; }
    public float Scale { get; }
    internal GroupTimingRecord(Timing source, int start, int end, float speed)
    {
        Source=source; StartBound=start; EndBound=end;
        ScaledBpm=source.Bpm*speed;
        float reciprocal=1f/ScaledBpm;
        Scale=reciprocal*60f;
        if(!float.IsFinite(Scale)||Scale==0)throw new NotSupportedException("Nonfinite/zero group scale.");
    }
}

public sealed class TimingGroupState
{
    public TimingGroup Definition { get; }
    public int Id => Definition.Id;
    public bool Active { get; private set; } = true;
    public IReadOnlyList<GroupTimingRecord> Records { get; }
    public int QueryLow { get; private set; }
    public int QueryHigh { get; private set; }
    public float FrameOffset { get; private set; }
    // The model owns managed maps; no claim about native header reclamation.
    private readonly SortedDictionary<int,List<RuntimeNote>> index=new SortedDictionary<int,List<RuntimeNote>>();
    public IReadOnlyDictionary<int,IReadOnlyList<string>> Index => index.ToDictionary(p=>p.Key,p=>(IReadOnlyList<string>)p.Value.Select(n=>n.Id).ToArray());
    internal IEnumerable<KeyValuePair<int,List<RuntimeNote>>> Buckets => index;
    private readonly bool signedPreroll;
    internal TimingGroupState(TimingGroup definition,float speed,int chartEnd,bool signedPreroll)
    {
        Definition=definition;this.signedPreroll=signedPreroll;
        Records=definition.Timings.Select((t,i)=>new GroupTimingRecord(t,i==0?int.MinValue:t.Time,
            i+1<definition.Timings.Count?definition.Timings[i+1].Time:checked(chartEnd+1000000),speed)).ToArray();
    }
    public float DepthAt(int time)
    {
        // E009/E029: native f32 divide then subtract for EACH timing contribution.
        // R001 default-only negative-time behavior remains a compatibility boundary.
        if(time<0&&!signedPreroll)return 0;
        float depth=0;
        foreach(var record in Records)
        {
            if(record.StartBound>=time)break;
            int bound=Math.Min(record.EndBound,time);
            float duration=bound-Math.Max(record.StartBound,0);
            float contribution=duration/record.Scale;
            depth=depth-contribution;
        }
        return depth;
    }
    internal static int SignedKey(float quotient)
    {
        // Explicit engineering bound; never saturate/wrap unsupported FCVTZS input.
        if(!float.IsFinite(quotient)||quotient < -100000 || quotient > 100000)
            throw new NotSupportedException("Spatial arithmetic exceeds bounded signed key domain.");
        return (int)quotient; // toward zero, including negative fractional keys
    }
    internal void Insert(RuntimeNote note)
    {
        int k0=SignedKey(DepthAt(Math.Min(note.Start,note.End))/-10000f);
        int k1=SignedKey(DepthAt(Math.Max(note.Start,note.End))/-10000f);
        note.Bucket=Math.Min(k0,k1);note.EndBucket=Math.Max(k0,k1);
        note.PreDepth=(int)DepthAt(note.Start);note.PreEndDepth=(int)DepthAt(note.End);
        note.Depth=note.PreDepth;note.EndDepth=note.PreEndDepth;
        if((long)note.EndBucket-note.Bucket>100000)throw new NotSupportedException("Spatial bucket span exceeds100000.");
        for(int key=note.Bucket;key<=note.EndBucket;key++)
        {
            if(!index.TryGetValue(key,out var list))index[key]=list=new List<RuntimeNote>();
            list.Add(note);
        }
    }
    internal void Update(int time)
    {
        Active=time<=Definition.LifetimeEnd;
        float a=-DepthAt(time),b=-DepthAt(checked(time+120));FrameOffset=a;
        QueryLow=Math.Min(SignedKey((a-700f)/10000f),SignedKey((b-700f)/10000f));
        QueryHigh=Math.Max(SignedKey((a+10000f)/10000f),SignedKey((b-700f)/10000f));
    }
    internal void UpdateDepth(RuntimeNote note)
    { note.Depth=(int)(note.PreDepth+FrameOffset);note.EndDepth=(int)(note.PreEndDepth+FrameOffset); }
}

internal readonly struct AffStatement
{
    public string Text { get; }
    public int Group { get; }
    public int TokenOrder { get; }
    public AffStatement(string text,int group,int order){Text=text;Group=group;TokenOrder=order;}
}

internal static class GroupBodyParser
{
    // Bounded structural scanner: semicolons terminate records, braces delimit ONE
    // independent group. Parentheses/arc child brackets remain inside each record.
    internal static List<AffStatement> Read(string body,List<TimingGroup> groups,List<List<Timing>> lists)
    {
        var result=new List<AffStatement>();int at=0,group=0,order=0;bool opened=false;
        void Space(){while(at<body.Length&&char.IsWhiteSpace(body[at]))at++;}
        while(true)
        {
            Space();if(at==body.Length)break;
            if(body[at]=='}')
            {
                if(group==0)throw new FormatException("Unmatched group close.");
                at++;Space();if(at==body.Length||body[at++]!=';')throw new FormatException("Group close requires semicolon.");
                group=0;continue;
            }
            if(body.Substring(at).StartsWith("timinggroup",StringComparison.Ordinal))
            {
                if(group!=0||opened)throw new NotSupportedException("One nonnested independent timing group supported.");
                int brace=body.IndexOf('{',at);if(brace<0)throw new FormatException("Timing group requires braces.");
                string head=body.Substring(at,brace-at).Trim();
                var match=System.Text.RegularExpressions.Regex.Match(head,@"^timinggroup\(\s*(noinput)?\s*\)$");
                if(!match.Success)throw new NotSupportedException("Unsupported timing-group descriptor.");
                group=1;opened=true;at=brace+1;
                var list=new List<Timing>();lists.Add(list);groups.Add(new TimingGroup(1,order++,match.Groups[1].Value,list));continue;
            }
            int end=body.IndexOf(';',at);if(end<0)throw new FormatException("AFF record requires semicolon.");
            string text=body.Substring(at,end-at).Trim();
            if(text.Length==0||text.IndexOfAny(new[]{'{','}'})>=0)throw new FormatException("Malformed group/record boundary.");
            result.Add(new AffStatement(text,group,order++));at=end+1;
        }
        if(group!=0)throw new FormatException("Unclosed timing group.");
        return result;
    }
}
