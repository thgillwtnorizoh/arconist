using Godot;
using Arconist.Core;
namespace Arconist.GodotApp;

public partial class SpatialTrack
{
    // ENGINEERING display: finite, one-native-unit cells sampled from the SAME
    // authoritative selector. E039 does not establish original FOV/track meshes.
    public readonly record struct InputRegion(int Lane,bool Secondary,float MinX,float MaxX);
    public IReadOnlyList<InputRegion> WideningRegions=>wideningRegions;
    private readonly List<InputRegion> wideningRegions=new();
    private readonly List<MeshInstance3D> wideningMeshes=new();
    private Node3D? wideningRoot;
    private readonly List<MeshInstance3D> outerPanels=new();
    private readonly List<Label3D> outerLabels=new();
    private Label3D? secondaryLabel;
    private float shownG=float.NaN,shownW=float.NaN;
    public bool WideningVisible=>wideningRoot?.Visible??false;
    public void RefreshWidening(Kernel? core)
    {
        bool show=core?.Chart.SceneControls.Count>0&&!core.Finished;
        if(wideningRoot!=null)wideningRoot.Visible=show;
        if(!show){wideningRegions.Clear();shownG=shownW=float.NaN;return;}
        if(wideningRoot==null)
        {
            wideningRoot=new Node3D{Name="EngineeringInputRegions"};AddChild(wideningRoot);
            foreach(int lane in new[]{1,6})
            {
                outerPanels.Add(Box(World(NativeX(lane),-15,-4450),World(420,24,9900),new Color("294c49"),false,wideningRoot));
                var label=new Label3D{Text=$"{(lane==1?"LEFT":"RIGHT")} MOUSE",Position=World(NativeX(lane),65,240),FontSize=48,PixelSize=.003f,Modulate=new Color("a5f56d"),Billboard=BaseMaterial3D.BillboardModeEnum.Enabled};wideningRoot.AddChild(label);outerLabels.Add(label);
            }
            secondaryLabel=new Label3D{Text="GOLD: ALSO F",Position=World(40,70,260),FontSize=42,PixelSize=.003f,Modulate=new Color("ffd36f"),Billboard=BaseMaterial3D.BillboardModeEnum.Enabled};wideningRoot.AddChild(secondaryLabel);
        }
        wideningRoot.Visible=true;
        if(shownG==core!.Widening.G&&shownW==core.Widening.W)return;
        shownG=core.Widening.G;shownW=core.Widening.W;wideningRegions.Clear();
        foreach(var panel in outerPanels)panel.Visible=shownW>0;
        foreach(var label in outerLabels)label.Visible=shownW>0;
        secondaryLabel!.Visible=shownG>1;
        for(int lane=1;lane<=6;lane++)foreach(bool secondary in new[]{false,true})
        {
            int begin=int.MinValue;
            for(int x=-1275;x<=1275;x++)
            {
                var pair=GroundSpatial.Select(new SkyPoint(x+.5f,0,0),shownG,shownW);
                bool match=x<1275&&(secondary?pair.Secondary:pair.Primary)==lane;
                if(match&&begin==int.MinValue)begin=x;
                if(!match&&begin!=int.MinValue){wideningRegions.Add(new InputRegion(lane,secondary,begin,x));begin=int.MinValue;}
            }
        }
        while(wideningMeshes.Count<wideningRegions.Count)wideningMeshes.Add(Box(Vector3.Zero,Vector3.One,new Color("6580bf"),true,wideningRoot));
        for(int i=0;i<wideningMeshes.Count;i++)
        {
            var mesh=wideningMeshes[i];mesh.Visible=i<wideningRegions.Count;if(!mesh.Visible)continue;
            var r=wideningRegions[i];mesh.Name=$"Lane{r.Lane}{(r.Secondary?"Secondary":"Primary")}{i}";
            float depth=r.Secondary?110:140;
            mesh.Position=World((r.MinX+r.MaxX)*.5f,r.Secondary?13:5,r.Secondary?130:0);
            ((BoxMesh)mesh.Mesh).Size=World(r.MaxX-r.MinX,4,depth);
            var color=r.Secondary?new Color("ffd36f"):new Color(r.Lane is 1 or 6?"a5f56d":"6386a5");
            ((StandardMaterial3D)mesh.MaterialOverride).AlbedoColor=color;
        }
    }
}
