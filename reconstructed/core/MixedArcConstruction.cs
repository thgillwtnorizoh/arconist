namespace Arconist.Core;

// S01 integration subset. Full graph/tolerance/child conflicts remain OPEN.
internal static class MixedArcConstruction
{
    internal static void Link(IReadOnlyList<Arc> arcs)
    {
        foreach(var group in arcs.GroupBy(a=>a.TimingGroup.Id))
        {
            var members=group.ToArray();var crossing=new HashSet<Arc>();
            foreach(var pair in members.GroupBy(a=>(a.Start,a.End)).Where(g=>g.Count()>1))
            {
                var p=pair.ToArray();
                bool Supported(Arc a)=>!a.Trace&&a.Curve=="s"&&a.End-a.Start==1000&&a.Y0==.5f&&a.Y1==.5f&&a.Bpm==120&&a.Density==1;
                if(p.Length!=2||!p.All(Supported)||p[0].Color==p[1].Color||p[0].X0!=p[1].X1||p[0].X1!=p[1].X0||p[0].X0!=.2f||p[0].X1!=.8f)
                    throw new NotSupportedException("Only the E028 translated two-color linear crossing pair is integrated.");
                p[0].CrossingPartner=p[1];p[1].CrossingPartner=p[0];crossing.Add(p[0]);crossing.Add(p[1]);
            }
            foreach(var a in crossing)if(members.Any(b=>b!=a&&b!=a.CrossingPartner&&b.Start<a.End+1000L&&a.Start<b.End+1000L))
                throw new NotSupportedException("Additional sky conflicts around a crossing remain unverified.");
            OrdinaryPairLinker.LinkAndGenerate(members.Where(a=>!crossing.Contains(a)).ToArray());
            foreach(var a in crossing)a.GenerateRecords();
        }
        // Shared colors across groups remain real shared identities. Ambiguous
        // simultaneous sky interactions across groups need separate native closure.
        foreach(var a in arcs)foreach(var b in arcs)
            if(a.TimingGroup.Id!=b.TimingGroup.Id&&a.Start<b.End&&b.Start<a.End)
                throw new NotSupportedException("Simultaneous sky arcs across timing groups remain unverified.");
    }
}
public sealed class ProximityObservation
{
    public int EffectiveTime {get;}public string Arc {get;}public string Neighbor {get;}public float Distance {get;}
    internal ProximityObservation(int e,string arc,string neighbor,float distance){EffectiveTime=e;Arc=arc;Neighbor=neighbor;Distance=distance;}
}
