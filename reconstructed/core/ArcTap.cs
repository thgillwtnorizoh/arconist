namespace Arconist.Core;

// Parsed child identity stays attached to the exact parsed parent, never a lane tap.
public sealed class ArcTap
{
    public Arc Parent {get;}
    public string ParentId=>Parent.Id;
    public int Ordinal {get;}
    public int Time {get;}
    public string Id=>$"{ParentId}:arctap:{Ordinal}:{Time}";
    internal ArcTap(Arc parent,int ordinal,int time){Parent=parent;Ordinal=ordinal;Time=time;}
}
public sealed class ArcTapState:RuntimeNote
{
    public ArcTap Data {get;}
    public ArcState Parent {get;}
    public string ParentId=>Parent.Id;
    public SkyPoint Local {get;}
    // Sampled local Z scrolls with the parent; initial input independently uses Z0.
    public SkyPoint WorldPosition=>new SkyPoint(Parent.Geometry.X0+Local.X,Local.Y,Parent.Depth+Local.Z);
    public SkyPoint InputTarget=>new SkyPoint(Parent.Geometry.X0+Local.X,Local.Y,0);
    public override string Id=>Data.Id;
    public override int Start=>Data.Time;
    public override int End=>Data.Time;
    public override int Lane=>0;
    public override int SourceOrder=>Parent.SourceOrder;
    public override bool Terminal=>Consumed||Missed;
    public bool Consumed {get;internal set;}
    public bool Missed {get;internal set;}
    public int Contact {get;internal set;}=-1;
    public string? Outcome {get;internal set;}
    public int? ResolvedAt {get;internal set;}
    internal ArcTapState(ArcTap data,ArcState parent,SkyPoint local){Data=data;Parent=parent;Local=local;}
}
public static class ArcTapSpatial
{
    // E004 flag1, ordinary chart+110==0. Unlike ordinary arcs, width contribution212.
    public static bool Matches(float targetX,float targetY,SkyContact contact)
    {
        if(!contact.Valid||!float.IsFinite(targetX)||!float.IsFinite(targetY))return false;
        float scale=ArcSpatial.Scale(contact.CameraZ,contact.FrameHeight);
        float half=scale*90f,bx=scale*212f,by=scale*250f;
        int y=(int)Math.Max(100f,Math.Min(550f,contact.Point.Y));
        return targetX-half-bx<contact.Point.X&&contact.Point.X<targetX+half+bx&&targetY-by-60f*scale<y&&y<targetY+by&&contact.Point.Z> -1000;
    }
}
