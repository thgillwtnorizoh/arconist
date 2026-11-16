using Godot;
using Arconist.Bridge;
using Arconist.Core;
namespace Arconist.GodotApp;

// ENGINEERING desktop/touch transport. Every press originates a distinct delivered
// button/touch event; no fabricated DOWN, aim-assist or ownership assignment.
public sealed class SpatialContactAdapter
{
    private readonly GameplaySession session;
    private readonly SpatialTrack track;
    private readonly HashSet<int> retained=new();
    public int Count=>retained.Count;
    public SpatialContactAdapter(GameplaySession session,SpatialTrack track){this.session=session;this.track=track;}
    public bool Press(int pointer,Vector2 local,bool skyOnly=false)
    {
        if(retained.Contains(pointer))return false;
        int lane=skyOnly?0:track.Pick(local,out _);
        SkyContact? sky=track.PickSky(local,out var point)?point:null;
        bool hasArcs=session.Core?.Arcs.Count>0;
        bool accepted=hasArcs?((lane!=0||sky.HasValue)&&session.Pointer(pointer,lane,sky,true)):(lane!=0&&session.Contact(pointer,lane,true));
        if(accepted)retained.Add(pointer);return accepted;
    }
    public bool Release(int pointer,bool cancel=false)
    {
        if(!retained.Remove(pointer))return false;
        if(cancel)return session.Cancel(pointer,"platform pointer cancellation");
        return session.Core?.Arcs.Count>0?session.Pointer(pointer,0,null,false):session.Contact(pointer,2,false);
    }
    public void Move(int pointer,Vector2 local)
    {
        if(!retained.Contains(pointer))return;
        int lane=track.Pick(local,out _);SkyContact? sky=track.PickSky(local,out var point)?point:null;
        if(session.Core?.Arcs.Count>0)session.MovePointer(pointer,lane,sky);else session.MoveContact(pointer,lane);
    }
    public void MoveMouse(Vector2 local)
    {
        // L/R are separate physical button contacts sharing the actual cursor.
        Prune();foreach(int id in retained.Where(i=>i==100||i==101).ToArray())Move(id,local);
    }
    public void Prune(){foreach(int id in retained.ToArray())if(session.Core==null||!session.Core.Contacts.Any(c=>c.Pointer==id))retained.Remove(id);}
    public void Forget()=>retained.Clear(); // session owns cancellation/terminal cleanup
}
