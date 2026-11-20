"""Lexical fixture inventory only. No production/native parser or runtime output."""
import re

def normalize_aff(raw):
    body=raw.decode().split('\n-\n',1)[1];group=0;next_group=1;objects=[];timings=[]
    for line in body.splitlines():
        s=line.strip()
        if not s:continue
        if s.startswith('timinggroup('):
            assert group==0;group=next_group;next_group+=1;continue
        if s=='};':assert group!=0;group=0;continue
        if s.startswith('timing('):
            values=s[7:].split(')')[0].split(',');assert len(values)==3
            timings.append(dict(group=group,time=int(values[0]),bpmToken=values[1],beatsToken=values[2]));continue
        item=dict(sourceNoteOrdinal=len(objects),group=group)
        if s.startswith('arc('):
            v=s[4:].split(')',1)[0].split(',');assert len(v)==10
            item.update(kind='arc',start=int(v[0]),end=int(v[1]),xTokens=v[2:4],curve=v[4],yTokens=v[5:7],color=int(v[7]),effect=v[8],modeToken=v[9],children=[dict(sourceChildOrdinal=i,time=int(t)) for i,t in enumerate(re.findall(r'arctap\((\d+)\)',s))])
        elif s.startswith('hold('):
            a,b,l=s[5:].split(')')[0].split(',');item.update(kind='hold',start=int(a),end=int(b),rawLane=int(l))
        else:
            m=re.fullmatch(r'\((\d+),(\d+)\);',s);assert m,s;item.update(kind='tap',start=int(m[1]),end=int(m[1]),rawLane=int(m[2]))
        objects.append(item)
    assert group==0
    return dict(status='LEXICAL SOURCE INVENTORY; not native parsed/prepared output',groupCount=next_group,timings=timings,objects=objects)
