using Godot;
using Arconist.Bridge;
using System.Buffers.Binary;
using System.Security.Cryptography;

namespace Arconist.GodotApp;

// Godot output substitution; this class never receives or writes Kernel time.
public partial class GodotBgmBackend : Node, IBgmBackend
{
    private AudioStreamPlayer player = null!;
    private AudioStreamWav? stream;
    private string resourceSha = "";
    public event Action? Ended;
    public bool Muted { get; set; }
    public AudioStreamPlayer Player => player;
    public override void _Ready()
    {
        player=new AudioStreamPlayer { Name="SessionBgm", Autoplay=false, MaxPolyphony=1, VolumeDb=-3 };
        AddChild(player);player.Finished+=()=>Ended?.Invoke();
    }
    public void Load(string resource)
    {
        StopAndUnload();
        if(!resource.StartsWith("res://",StringComparison.Ordinal) || !Godot.FileAccess.FileExists(resource))
            throw new FileNotFoundException("Bundled BGM resource unavailable: "+resource);
        byte[] data=Godot.FileAccess.GetFileAsBytes(resource);
        // Deliberately bounded asset contract: generated uncompressed PCM16 mono.
        // Reject invalid resources before a decoder call so expected negatives are
        // visible application diagnostics, not silent success or engine errors.
        if(data.Length<44 || System.Text.Encoding.ASCII.GetString(data,0,4)!="RIFF" ||
           System.Text.Encoding.ASCII.GetString(data,8,8)!="WAVEfmt " ||
           BinaryPrimitives.ReadInt32LittleEndian(data.AsSpan(16))!=16 ||
           BinaryPrimitives.ReadInt16LittleEndian(data.AsSpan(20))!=1 ||
           BinaryPrimitives.ReadInt16LittleEndian(data.AsSpan(22))!=1 ||
           BinaryPrimitives.ReadInt32LittleEndian(data.AsSpan(24))!=22050 ||
           BinaryPrimitives.ReadInt16LittleEndian(data.AsSpan(34))!=16 ||
           System.Text.Encoding.ASCII.GetString(data,36,4)!="data" ||
           BinaryPrimitives.ReadInt32LittleEndian(data.AsSpan(40))!=data.Length-44)
            throw new InvalidDataException("BGM must be the bundled valid PCM16 mono22050 WAV.");
        stream=AudioStreamWav.LoadFromBuffer(data,new Godot.Collections.Dictionary {
            ["compress/mode"]=0,["edit/normalize"]=false,["edit/trim"]=false,["edit/loop_mode"]=0 });
        if(stream==null || stream.GetLength()<=0 || stream.LoopMode!=AudioStreamWav.LoopModeEnum.Disabled)
            throw new InvalidDataException("Godot could not decode the bundled non-looping soundtrack.");
        resourceSha=Convert.ToHexString(SHA256.HashData(data)).ToLowerInvariant();
        player.Stream=stream;player.StreamPaused=false;
    }
    public void PlayFromStart()
    {
        if(stream==null)throw new InvalidOperationException("BGM was not prepared.");
        player.Stop();player.StreamPaused=false;player.VolumeDb=Muted?-80:-3;player.Play(0);
    }
    public void StopAndUnload()
    {
        if(player!=null && GodotObject.IsInstanceValid(player)) {player.Stop();player.Stream=null;player.StreamPaused=false;}
        stream?.Dispose();stream=null;resourceSha="";
    }
    public BgmStatus Inspect()
    {
        string identity=$"Godot AudioStreamPlayer; driver={AudioServer.GetDriverName()}; device={AudioServer.OutputDevice}; mixHz={AudioServer.GetMixRate()}";
        bool masterMuted=AudioServer.IsBusMute(AudioServer.GetBusIndex("Master"));
        return new BgmStatus(player?.Playing??false,player?.GetPlaybackPosition()??0,
            stream?.GetLength()??0,identity,Muted||masterMuted,resourceSha);
    }
    public override void _ExitTree() => StopAndUnload();
}
