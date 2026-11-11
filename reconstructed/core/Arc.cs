namespace Arconist.Core;

public readonly struct SkyPoint
{
    public float X {get;} public float Y {get;} public float Z {get;}
    public SkyPoint(float x,float y,float z){X=x;Y=y;Z=z;}
    public bool Finite=>float.IsFinite(X)&&float.IsFinite(Y)&&float.IsFinite(Z);
}
public readonly struct SkyContact
{
    public SkyPoint Point {get;} public float CameraZ {get;} public float FrameHeight {get;}
    public SkyContact(SkyPoint point,float cameraZ=900,float frameHeight=720){Point=point;CameraZ=cameraZ;FrameHeight=frameHeight;}
    public bool Valid=>Point.Finite&&float.IsFinite(CameraZ)&&float.IsFinite(FrameHeight)&&FrameHeight>0;
}
public static class ArcSpatial
{
    public static float Scale(float cameraZ,float height)
    {
        float delta=height<=720?0:height<=960?height-720:240;
        float basis=900f+(delta/-240f)*100f;
        return cameraZ<0?2f:Math.Max(1f,cameraZ/basis);
    }
    public static bool Matches(float targetX,float targetY,SkyContact contact)
    {
        if(!contact.Valid||!float.IsFinite(targetX)||!float.IsFinite(targetY))return false;
        float scale=Scale(contact.CameraZ,contact.FrameHeight), half=scale*90f, width=scale*100f, vertical=scale*250f;
        // Continuous caller clamps Y before helper's integer truncation (E004).
        int y=(int)Math.Max(100f,Math.Min(550f,contact.Point.Y));
        return targetX-half-width<contact.Point.X&&contact.Point.X<targetX+half+width&&targetY-vertical<y&&y<targetY+vertical&&contact.Point.Z> -1000;
    }
}
public sealed class Arc
{
    public int Ordinal {get;} public int Start {get;} public int End {get;} public int SourceOrder {get;}
    public float X0 {get;} public float X1 {get;} public float Y0 {get;} public float Y1 {get;} public int Color {get;} public float Extra {get;}
    public string Curve=>"s";public string Effect=>"none";public bool Trace {get;}public int Mode=>Trace?1:0;
    public IReadOnlyList<ArcTap> Children {get;}
    public int TimingTime {get;} public float Bpm {get;} public float Density {get;}
    public float Interval {get;} public IReadOnlyList<int> Checkpoints {get;}
    public string Id=>$"arc:{Ordinal}:{Start}:{End}:{Color}";
    internal Arc(int ordinal,int order,int start,int end,float x0,float x1,float y0,float y1,int color,float extra,Timing timing,float density,bool trace=false,int? childTime=null)
    {
        Trace=trace;
        if(trace!=childTime.HasValue)throw new NotSupportedException("Trace parents require exactly one child; ordinary arcs cannot have children in R008.");
        Children=Array.AsReadOnly(childTime.HasValue?new[]{new ArcTap(this,0,childTime.Value)}:Array.Empty<ArcTap>());
        Ordinal=ordinal;SourceOrder=order;Start=start;End=end;X0=x0;X1=x1;Y0=y0;Y1=y1;Color=color;Extra=extra;TimingTime=timing.Time;Bpm=timing.Bpm;Density=density;
        // E009 ordinary flag0 generation, same literal f32 stages as E001/010.
        Interval=((60000f/Bpm)/(Bpm>=255f?1f:2f))/density;
        if(!float.IsFinite(Interval)||Interval<1||Interval>int.MaxValue/4f)throw new NotSupportedException("Arc interval outside supported domain.");
        if(Trace){Checkpoints=Array.Empty<int>();return;}
        float quotient=(float)(end-start)/Interval;
        if(quotient>100000)throw new NotSupportedException("Excessive arc records.");
        var records=new List<int>();
        for(int i=1;i<(int)quotient;i++){float step=Interval*(float)i;int t=(int)((float)start+step);if(t<end)records.Add(t);}
        if(records.Count==0)records.Add((int)((float)start+(float)(end-start)*0.5f));
        if(records.Any(t=>t<=start||t>=end)||records.Distinct().Count()!=records.Count)throw new NotSupportedException("Arc records must be distinct interior times.");
        Checkpoints=records.AsReadOnly();
    }
}
public sealed class ArcGeometry
{
    private readonly Arc data;
    public int Height {get;} public int X0 {get;} public int X1 {get;} public int Y0 {get;} public int Y1 {get;} public int Z {get;} public int Rate {get;}
    public IReadOnlyList<SkyPoint> Samples {get;} public IReadOnlyList<SkyPoint> DetailSamples {get;}
    public ArcGeometry(Arc arc,float timingScale,int height)
    {
        if(height<0||height>1000||!float.IsFinite(timingScale)||timingScale<=0)throw new NotSupportedException("Arc geometry environment outside supported domain.");
        data=arc;Height=height;X0=(int)(arc.X0*850f-425f);X1=(int)(arc.X1*850f-425f);Y0=(int)(arc.Y0*(height-100)+100f);Y1=(int)(arc.Y1*(height-100)+100f);
        Z=(int)(-(float)(arc.End-arc.Start)/timingScale);if(Z>=0)throw new NotSupportedException("Arc needs nonzero forward geometry depth.");
        Rate=arc.End-arc.Start<1000?14:7;
        Samples=Generate(arc,1);DetailSamples=Generate(arc,Math.Max(1f,arc.Extra));
    }
    private IReadOnlyList<SkyPoint> Generate(Arc arc,float extra)
    {
        double seconds=(arc.End-arc.Start)/1000.0,step=1.0/(seconds*Rate*extra);
        if(1/step>20000)throw new NotSupportedException("Excessive geometry sample count.");
        var points=new List<SkyPoint>{Point(0)};
        for(double u=step;u<1;u+=step)points.Add(Point((float)u));
        points.Add(Point(1));return points.AsReadOnly();
    }
    public SkyPoint ChildPoint(ArcTap child)
    {
        if(!ReferenceEquals(child.Parent,data))throw new ArgumentException("Child belongs to another parent.");
        return Point((float)(child.Time-data.Start)/(data.End-data.Start));
    }
    private SkyPoint Point(float u)=>new SkyPoint((X1-X0)*u,Y0+(Y1-Y0)*u,Z*u);
}
public sealed class ArcColorState
{
    public int Color {get;} public int Owner {get;internal set;}=-1;public int ReleaseTime {get;internal set;}=-1;
    public int IntervalInteger {get;internal set;}public bool PreviouslyClaimed {get;internal set;}public bool Accepted {get;internal set;}public bool Conflict {get;internal set;}
    internal ArcColorState(int color){Color=color;}
}
public sealed class ArcState:RuntimeNote
{
    public Arc Data {get;}public ArcGeometry Geometry {get;}public ArcColorState Color {get;}
    public override string Id=>Data.Id;public override int Start=>Data.Start;public override int End=>Data.End;public override int Lane=>0;public override int SourceOrder=>Data.SourceOrder;
    public override bool Terminal=>Data.Trace?Children.All(c=>c.Terminal):Records.All(r=>r.Resolved);
    public SkyPoint Cache {get;private set;}public bool CacheEnabled {get;private set;}public float TargetX=>Geometry.X0+Cache.X;public float TargetY=>Cache.Y;
    public bool Holding {get;internal set;}public bool EndReset {get;internal set;}
    public bool FirstRecordEarlyExpiry=>false;public bool InactiveExpiryAllowed=>true;
    public IReadOnlyList<CheckpointState> Records {get;}
    public IReadOnlyList<ArcTapState> Children {get;}
    internal ArcState(Arc data,ArcGeometry geometry,ArcColorState color){Data=data;Geometry=geometry;Color=color;Children=data.Children.Select(c=>new ArcTapState(c,this,geometry.ChildPoint(c))).ToList().AsReadOnly();Records=data.Checkpoints.Select(t=>new CheckpointState(t)).ToList().AsReadOnly();Cache=geometry.Samples[0];}
    internal void UpdateCache(int now)
    {
        CacheEnabled=false;
        var samples=Geometry.Samples;
        for(int i=0;i+1<samples.Count;i++)
        {
            var a=samples[i];var b=samples[i+1];float az=a.Z+Depth,bz=b.Z+Depth;
            if(bz>az){az=-az;bz=-bz;}
            float bx=b.X,by=b.Y;if(az<0){bx=a.X;by=a.Y;}
            float denominator=bz-az;
            if(denominator==0)continue;
            float u=1f-bz/denominator;float v=Math.Max(0f,Math.Min(1f,u));
            float x=a.X+(bx-a.X)*v,y=a.Y+(by-a.Y)*v;
            if(now<=End)Cache=new SkyPoint(x,y,0);
            CacheEnabled=u>=0&&u<=1&&Start<=now&&now<=End;
            if(CacheEnabled||az<=0)break;
        }
    }
}
