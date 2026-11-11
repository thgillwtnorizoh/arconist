using Godot;
using Arconist.Bridge;
using System.Buffers.Binary;
using System.Security.Cryptography;

namespace Arconist.GodotApp;

// Godot output substitution; this class never receives or writes Kernel time.
public partial class GodotBgmBackend : Node, IPausableBgmBackend
{
    private AudioStreamPlayer player = null!;
    private AudioStreamWav? stream;
    private AudioStreamPlayback? playback;
    private double? seekReadback;
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
        playback=player.GetStreamPlayback();
    }
    public void PausePlayback() {player.StreamPaused=true;}
    public void SeekMilliseconds(int position)
    {
        if(stream==null || !player.StreamPaused || position<0 || position/1000.0>=stream.GetLength())
            throw new InvalidOperationException("Seek requires a paused prepared stream and a valid logical position.");
        if(playback==null) throw new InvalidOperationException("No retained PCM playback to seek.");
        // Godot4.7.2 player-level Seek ignores paused playbacks (is_playing guard).
        // Seek the same PCM playback under the audio-server lock; never Play(0).
        AudioServer.Lock();
        try
        {
            playback.Seek(position/1000.0);
            seekReadback=playback.GetPlaybackPosition();
            if(Math.Abs(seekReadback.Value-position/1000.0)>1.0/22050)
                throw new InvalidOperationException("PCM playback did not acknowledge logical seek.");
            // Discard samples/interpolation history from before the interruption.
            if(playback is AudioStreamPlaybackResampled resampled)resampled.BeginResample();
        }
        finally {AudioServer.Unlock();}
    }
    public void UnpausePlayback()
    {
        if(stream==null) throw new InvalidOperationException("No paused BGM stream.");
        player.StreamPaused=false;
    }
    public void StopAndUnload()
    {
        if(player!=null && GodotObject.IsInstanceValid(player)) {player.Stop();player.Stream=null;player.StreamPaused=false;}
        playback?.Dispose();playback=null;seekReadback=null;stream?.Dispose();stream=null;resourceSha="";
    }
    public BgmStatus Inspect()
    {
        string identity=$"Godot AudioStreamPlayer; driver={AudioServer.GetDriverName()}; device={AudioServer.OutputDevice}; mixHz={AudioServer.GetMixRate()}";
        bool masterMuted=AudioServer.IsBusMute(AudioServer.GetBusIndex("Master"));
        return new BgmStatus(player?.Playing??false,playback?.GetPlaybackPosition()??0,
            stream?.GetLength()??0,identity,Muted||masterMuted,resourceSha,player?.StreamPaused??false,seekReadback);
    }
    public override void _ExitTree() => StopAndUnload();
}
