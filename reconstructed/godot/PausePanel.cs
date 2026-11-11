using Godot;
using Arconist.Bridge;
namespace Arconist.GodotApp;

// Scene/modal presentation is separate from model and timeline pause states.
public partial class PausePanel : ColorRect
{
    private GameplaySession session=null!;
    private Label message=null!;
    public Button ResumeButton {get;private set;}=null!;
    public Button MenuButton {get;private set;}=null!;
    public void Bind(GameplaySession value) {session=value;Sync();}
    public override void _Ready()
    {
        Name="PauseModal";Position=Vector2.Zero;Size=new Vector2(1100,740);ZIndex=100;
        Color=new Color(0.025f,0.035f,0.065f,0.96f);MouseFilter=MouseFilterEnum.Stop;Visible=false;
        var title=new Label{Text="PAUSED",Position=new Vector2(330,180),Size=new Vector2(440,60)};
        title.AddThemeFontSizeOverride("font_size",40);AddChild(title);
        message=new Label{Position=new Vector2(330,250),Size=new Vector2(440,160),AutowrapMode=TextServer.AutowrapMode.WordSmart};
        message.AddThemeFontSizeOverride("font_size",20);AddChild(message);
        ResumeButton=new Button{Text="Resume (R)",Position=new Vector2(330,430),Size=new Vector2(440,55),FocusMode=FocusModeEnum.None};
        MenuButton=new Button{Text="Return to start",Position=new Vector2(330,505),Size=new Vector2(440,55),FocusMode=FocusModeEnum.None};
        ResumeButton.Pressed+=()=>Resume();MenuButton.Pressed+=()=>Menu();AddChild(ResumeButton);AddChild(MenuButton);
    }
    public bool Resume(){bool ok=session.Resume();Sync();return ok;}
    public void Menu(){session.Home();Sync();}
    public void Sync()
    {
        if(session==null)return;
        Visible=session.PauseModalActive;
        if(message!=null)message.Text=$"Chart frozen at {(session.Core?.Timeline.EffectiveTime??0)/1000.0:F3}s.\n{session.PauseReason}\nResume explicitly; focus return does not resume.\n"+
            (session.Audio?.State=="ERROR"?session.Audio.Detail+"\nRetry Resume, or return to start.":"Retained contacts survive manual pause.\nUP releases them; focus loss cancels them.");
    }
}
