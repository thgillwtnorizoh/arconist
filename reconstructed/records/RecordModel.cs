using Arconist.Core;
using System.Security.Cryptography;
using System.Text;
using System.Text.Json.Serialization;
using System.Text.RegularExpressions;

namespace Arconist.Records;

// E013 0x196b22c and0xe3c054. No category names or numeric-max assumption.
public static class RecordRules
{
    public static int NormalizeClear(int stored)=>stored>=0&&stored<=5?stored:-1;
    private static int Rank(int type)=>type switch {0=>0,4=>1,1=>2,5=>3,2=>4,3=>5,_=>-1};
    public static bool ImprovesClear(int incoming,int stored)=>incoming>=0&&incoming<=5&&Rank(incoming)>Rank(NormalizeClear(stored));
    public static bool ImprovesScore(int incoming,int? stored)=>!stored.HasValue||incoming>stored.Value;
}

// ENGINEERING namespace: no recovered native song/difficulty/ct producer asserted.
public sealed record ChartIdentity(string Namespace,string ChartId,int ChartVersion,string Profile,string ContentSha256,int Difficulty,bool Ct)
{
    [JsonIgnore] public string Key=>$"{Namespace}/{ChartId}/v{ChartVersion}/{Profile}/{ContentSha256}/difficulty{Difficulty}/ct{(Ct?1:0)}";
    public const string SyntheticNamespace="arconist.synthetic";
    public static ChartIdentity FromAff(string id,ChartProfile profile,string aff)=>new(SyntheticNamespace,id,1,profile.ToString(),Convert.ToHexString(SHA256.HashData(Encoding.UTF8.GetBytes(aff))).ToLowerInvariant(),0,false);
    internal void Validate()
    {
        if(Namespace!=SyntheticNamespace||!Regex.IsMatch(ChartId??"",@"^[a-z0-9_-]{1,80}$")||ChartVersion!=1||Profile is not("R010" or "S01Mixed")||!Regex.IsMatch(ContentSha256??"",@"^[a-f0-9]{64}$")||Difficulty!=0||Ct)
            throw new InvalidDataException("Unsupported synthetic chart identity; native catalog/difficulty/ct are not implemented.");
    }
}

public sealed record SavedResult(int Score,int Pure,int Shining,int Far,int Lost,int RecordedLost,int Health,int Category,int MaxCombo,int Early,int Late,long UtcUnixSeconds,int NativeDate32,int SnapshotVersion,int Modifier)
{
    public static SavedResult Capture(GameResult r,DateTimeOffset utc)=>new(r.Score,r.Pure,r.Shining,r.Far,r.Lost,r.RecordedLost,r.Health,r.Category,r.MaxCombo,r.Early,r.Late,utc.ToUnixTimeSeconds(),unchecked((int)utc.ToUnixTimeSeconds()),1,0);
    internal void Validate()
    {
        if(Score<0||Pure<0||Shining<0||Shining>Pure||Far<0||Lost<0||RecordedLost<0||Health< -1||Health>100||Category<0||Category>5||MaxCombo<0||Early<0||Late<0||SnapshotVersion!=1||Modifier!=0||NativeDate32!=unchecked((int)UtcUnixSeconds)||UtcUnixSeconds< -62135596800L||UtcUnixSeconds>253402300799L)
            throw new InvalidDataException("Invalid stored result snapshot.");
    }
}
public sealed record ChartRecord(ChartIdentity Identity,SavedResult BestScore,int ClearType)
{
    [JsonIgnore] public int NormalizedClear=>RecordRules.NormalizeClear(ClearType);
}
public sealed record RecordOutcome(string Key,bool Success,bool Written,bool ScoreChanged,bool ClearChanged,string Code,string Detail);
public static class RecordPaths
{
    // Same production path builder is used in the real app and disk/restart tests.
    public static string ForUserData(string userDataRoot)=>Path.Combine(Path.GetFullPath(userDataRoot),"records","best-records.v1.json");
}
