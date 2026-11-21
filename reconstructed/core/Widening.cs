using System.Globalization;
namespace Arconist.Core;

public enum WideningKind { Camera = 5, Lanes = 6 }
public sealed class SceneControl
{
    public int Time {get;} public WideningKind Kind {get;} public float Duration {get;}
    public int Direction {get;} public int SourceOrder {get;} public int TimingGroupId=>0;
    public string Id=>$"scene:{SourceOrder}:{Time}:{(int)Kind}";
    internal SceneControl(int time,WideningKind kind,float duration,int direction,int order)
    {Time=time;Kind=kind;Duration=duration;Direction=direction;SourceOrder=order;}
}
public sealed class SceneControlState
{
    public SceneControl Data {get;}
    public bool Processed {get;internal set;}
    public bool Active {get;internal set;}=true;
    public int? DispatchedAt {get;internal set;}
    internal SceneControlState(SceneControl data){Data=data;}
}
public sealed class WideningTransition
{
    public int Start {get;internal set;}=-1073741824;
    public int Direction {get;internal set;}=-1;
    public float Duration {get;internal set;}=1;
    public string? Owner {get;internal set;}
    internal void Set(SceneControl c){Start=c.Time;Direction=c.Direction;Duration=c.Duration;Owner=c.Id;}
}
// E039 original frame: interpolate old parameters, THEN dispatch strict time<E.
// Does not claim native visible FOV/track-width behavior.
public sealed class WideningState
{
    public float G {get;private set;}=1;
    public float PreviousG {get;private set;}=1;
    public float W {get;private set;}
    public WideningTransition Camera {get;}=new WideningTransition();
    public WideningTransition Lanes {get;}=new WideningTransition();
    public IReadOnlyList<SceneControlState> Controls {get;}
    public IReadOnlyList<string> LastFrameOperations {get;private set;}=Array.Empty<string>();
    internal WideningState(IReadOnlyList<SceneControl> controls){Controls=controls.Select(c=>new SceneControlState(c)).ToArray();}
    internal void Frame(int e)
    {
        var operations=new List<string>();PreviousG=G;
        float u=(float)((long)e-Camera.Start)*0.5f;u=u/Camera.Duration;
        G=Math.Max(1f,Math.Min(1.5f,Camera.Direction>=1?1f+u:1.5f-u));
        float v=(float)((long)e-Lanes.Start)/Lanes.Duration;
        W=Math.Max(0f,Math.Min(1f,Lanes.Direction>=1?v:1f-v));
        operations.Add("INTERPOLATE");
        foreach(var state in Controls)
        {
            if(state.Processed){state.Active=false;continue;}
            if(e<=state.Data.Time)continue;
            state.Processed=true;state.DispatchedAt=e;
            (state.Data.Kind==WideningKind.Camera?Camera:Lanes).Set(state.Data);
            operations.Add("DISPATCH:"+state.Data.Id);
        }
        LastFrameOperations=operations.ToArray();
    }
}
public readonly struct LanePair
{
    public int Primary {get;} public int Secondary {get;}
    public bool Any=>Primary!=0||Secondary!=0;
    public LanePair(int primary,int secondary=0){Primary=primary;Secondary=secondary;}
    public bool Matches(int lane)=>lane!=0&&(lane==Primary||lane==Secondary);
}
public static class GroundSpatial
{
    // E004 normal Y=0 input plane; E039 chart feature0. Alternate special-song
    // depth branches are deliberately not exposed by this supported profile.
    public static LanePair Select(SkyPoint point,float g,float w)
    {
        if(!point.Finite||!float.IsFinite(g)||!float.IsFinite(w)||g<1||g>1.5f||w<0||w>1||point.X<=int.MinValue||point.X>=int.MaxValue||point.Z<=-500||point.Z>=500)return default;
        int x=(int)point.X,primary=Classify(x,w),secondary=0;
        if(g>1)
        {
            float a=(g-1f)*425f;a=a*0.5f;
            int left=Classify(x-a,w),right=Classify(x+a,w);
            if(left!=primary)secondary=left;else if(right!=primary)secondary=right;
        }
        return new LanePair(primary,secondary);
    }
    private static int Classify(float x,float w)
    {
        if(w>0&&x< -850)return 1;
        if(x< -425)return 2;
        if(x<0)return 3;
        if(x<425)return 4;
        if(x==425)return 0;
        return w>0&&x>850?6:5;
    }
}
