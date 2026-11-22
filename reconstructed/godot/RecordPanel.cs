using Godot;
using Arconist.Records;
using System.Globalization;
namespace Arconist.GodotApp;

public partial class RecordPanel:Control
{
    private readonly Label summary=new(){Size=new Vector2(336,48),MouseFilter=MouseFilterEnum.Ignore};
    public string DisplayText=>summary.Text;
    public int? DisplayedBestScore {get;private set;}
    public int DisplayedClear {get;private set;}=-1;
    public bool ShowsError {get;private set;}
    public RecordPanel()
    {
        Size=new Vector2(336,48);MouseFilter=MouseFilterEnum.Pass;
        summary.AddThemeFontSizeOverride("font_size",16);AddChild(summary);
    }
    public void ShowError(string detail)
    {ShowsError=true;DisplayedBestScore=null;DisplayedClear=-1;summary.Text="RECORD ERROR — gameplay continues\nHover here for recovery details";summary.Modulate=new Color("ff6985");TooltipText=detail;}
    public void Refresh(LocalRecordStore store,ChartIdentity identity,RecordOutcome? outcome=null)
    {
        if(store.HasError){ShowError(store.Detail);return;}
        if(outcome is {Success:false}&&outcome.Key==identity.Key){ShowError(outcome.Detail);return;}
        ShowsError=false;summary.Modulate=new Color("b9f56c");var record=store.Get(identity);
        DisplayedBestScore=record?.BestScore.Score;DisplayedClear=record?.NormalizedClear??-1;
        if(record==null){summary.Text="Selected best: No record\nComplete this chart to save";TooltipText="No completed local result for this exact chart/profile/content.\n"+identity.Key+"\n"+store.FilePath;return;}
        string clear=DisplayedClear<0?"No clear record":DisplayedClear.ToString(CultureInfo.InvariantCulture);
        string notice=outcome?.Key==identity.Key?outcome.Detail:store.LoadedFromDisk?"Loaded from local records":"Local record";
        summary.Text=$"Selected best: {record.BestScore.Score.ToString("N0",CultureInfo.InvariantCulture)}  |  Clear: {clear}\n{notice}";
        var r=record.BestScore;
        TooltipText=$"Best-score snapshot: PURE{r.Pure}, shining{r.Shining}, FAR{r.Far}, final LOST{r.Lost}, recorded LOST{r.RecordedLost}, health{r.Health}, category{r.Category}.\nUTC {DateTimeOffset.FromUnixTimeSeconds(r.UtcUnixSeconds):u}; native low32 date {r.NativeDate32}.\nClear progression is separate: 0 < 4 < 1 < 5 < 2 < 3.\n"+identity.Key+"\n"+store.FilePath;
    }
}
