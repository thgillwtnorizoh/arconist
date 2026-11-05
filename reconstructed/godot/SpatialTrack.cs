using Godot;
using Arconist.Core;

namespace Arconist.GodotApp;

// Native axes retained, uniformly scaled. No scoring or timeline mutations here.
public partial class SpatialTrack : Node3D
{
    public const float Unit = 1f / 425f;
    public Camera3D Camera { get; private set; } = null!;
    private readonly Dictionary<string, MeshInstance3D> notes = new();
    public bool AlternateView { get; private set; }
    public static Vector3 World(float x, float y, float z) => new(x * Unit, y * Unit, z * Unit);
    public static int NativeX(int lane) => 425 * (lane - 1) - 1063;
    public static Vector3 NotePosition(Kernel core, NoteState note) => World(NativeX(note.Data.Lane), 4, CurrentDepth(core,note));
    // Same pre-depth truncation and float-add/truncation as 010/035. Read-only,
    // including notes not currently admitted to the gameplay active vector.
    public static int CurrentDepth(Kernel core, NoteState note) => (int)((int)core.DepthAt(note.Data.Time) - core.DepthAt(core.Timeline.EffectiveTime));
    public static bool Present(Kernel core, NoteState note) => !core.Finished && !note.Consumed && !note.Missed && CurrentDepth(core,note) >= -9500 && CurrentDepth(core,note) <= 1000;
    public static int LaneAt(Vector3 world)
    {
        if (!world.IsFinite()) return 0;
        var native = world / Unit;
        // Ordinary E004 strict depth window; bounded four-lane outer clipping is
        // intentional (native G=1/E<=0 otherwise has unbounded outer lanes).
        if (native.Z <= -500 || native.Z >= 500 || native.X < -850 || native.X > 850) return 0;
        int x = (int)native.X;
        return x < -425 ? 2 : x < 0 ? 3 : x < 425 ? 4 : x == 425 ? 0 : 5;
    }
    public static bool GroundIntersection(Vector3 origin, Vector3 direction, out Vector3 hit)
    {
        hit = default;
        if (!origin.IsFinite() || !direction.IsFinite() || Math.Abs(direction.Y) < 1e-6f) return false;
        float t = -origin.Y / direction.Y;
        if (!float.IsFinite(t) || t < 0) return false;
        hit = origin + direction * t;
        return hit.IsFinite();
    }
    public int Pick(Vector2 screen, out Vector3 hit)
    {
        hit = default;
        if (!screen.IsFinite() || !GetViewport().GetVisibleRect().HasPoint(screen)) return 0;
        return GroundIntersection(Camera.ProjectRayOrigin(screen),Camera.ProjectRayNormal(screen),out hit) ? LaneAt(hit) : 0;
    }
    public override void _Ready()
    {
        Camera = new Camera3D { Projection = Camera3D.ProjectionType.Perspective, Fov = 65, Near = Unit, Far = 10000 * Unit, Current = true };
        AddChild(Camera); SetView(false);
        var environment = new WorldEnvironment { Environment = new Godot.Environment { BackgroundMode = Godot.Environment.BGMode.Color, BackgroundColor = new Color("10182b"), AmbientLightSource = Godot.Environment.AmbientSource.Color, AmbientLightColor = new Color("b5c9ed"), AmbientLightEnergy = 0.65f } };
        AddChild(environment);
        AddChild(new DirectionalLight3D { RotationDegrees = new Vector3(-55,-25,0), LightEnergy = 1.1f });
        for (int lane=2;lane<=5;lane++)
            Box(World(NativeX(lane),-15,-4450),World(418,24,9900),new Color(lane%2==0 ? "253b59" : "304869"));
        for (int i=0;i<=4;i++) Box(World(-850+i*425,1,-4450),World(5,3,9900),new Color("6386a5"),true);
        for (int z=-9000;z<0;z+=1000) Box(World(0,1,z),World(1700,3,5),new Color("47617c"),true);
        Box(World(-0.5f,4,0),World(1700,5,20),new Color("c3fa7d"),true);
        for (int i=0;i<4;i++)
        {
            var label = new Label3D { Text = new[]{"D","F","J","K"}[i], Position = World(NativeX(i+2),65,240), FontSize = 64, PixelSize = 0.003f, Modulate = new Color("d6e8f8"), Billboard = BaseMaterial3D.BillboardModeEnum.Enabled };
            AddChild(label);
        }
    }
    private MeshInstance3D Box(Vector3 position, Vector3 size, Color color, bool unshaded=false)
    {
        var m = new StandardMaterial3D { AlbedoColor = color, Roughness=0.8f };
        if (unshaded) m.ShadingMode = BaseMaterial3D.ShadingModeEnum.Unshaded;
        var mesh = new MeshInstance3D { Mesh = new BoxMesh { Size=size }, MaterialOverride=m, Position=position };
        AddChild(mesh); return mesh;
    }
    public void SetView(bool alternate)
    {
        AlternateView=alternate;
        Camera.Position = alternate ? World(220,1100,1050) : World(0,900,900);
        Camera.LookAt(World(0,-550,-2000),Vector3.Up);
    }
    public void Refresh(Kernel? core)
    {
        var ids=core?.Notes.Select(n=>n.Data.Id).ToHashSet() ?? new HashSet<string>();
        foreach (string id in notes.Keys.Where(id=>!ids.Contains(id)).ToArray()) { notes[id].QueueFree(); notes.Remove(id); }
        if (core == null) return;
        foreach (var note in core.Notes)
        {
            if (!notes.TryGetValue(note.Data.Id,out var mesh))
            { mesh=Box(Vector3.Zero,World(382,8,95),new Color("69e1f7")); notes.Add(note.Data.Id,mesh); }
            mesh.Position=NotePosition(core,note); mesh.Visible=Present(core,note);
        }
    }
}
