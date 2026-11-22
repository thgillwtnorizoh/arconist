#!/usr/bin/env python3
"""Validate static E013 expectations/provenance, never production code execution."""
import json,hashlib,re
from pathlib import Path
P=Path(__file__).resolve().parent;R=P.parents[4];checks=0
x=json.loads((P/'expectations.json').read_text());authority=R/x['authority']['path'];assert hashlib.sha256(authority.read_bytes()).hexdigest()==x['authority']['sha256'];checks+=1
text=authority.read_text().split('## Clear-type comparison and progression')[1].split('Actual native insert SQL')[0]
accepted={}
for line in text.splitlines():
 cells=[s.strip() for s in line.split('|')]
 if len(cells)!=4:continue
 old=cells[1]
 if old=='missing / −1':old=-1
 elif old in ['0','1','2','3','4','5']:old=int(old)
 else:continue
 accepted[old]=[] if cells[2]=='none' else [int(n.strip()) for n in cells[2].split(',')]
assert len(accepted)==7;checks+=1
assert len(x['clearTable'])==42;checks+=1
assert len({(r['old'],r['incoming']) for r in x['clearTable']})==42;checks+=1
for r in x['clearTable']:assert r['replace']==(r['incoming'] in accepted[r['old']]);checks+=1
best=None;clear=-1
for step in x['sequence']:
 if best is None or step['incomingScore']>best[0]:best=(step['incomingScore'],step['incomingDate'],step['incomingClear'])
 if step['incomingClear'] in accepted[clear]:clear=step['incomingClear']
 assert best==(step['expectedBestScore'],step['expectedSnapshotDate'],step['expectedSnapshotClear']);checks+=1
 assert clear==step['expectedStrongestClear'];checks+=1
pre=json.loads((P/'preflight.json').read_text());assert pre['status']=='BLOCKED' and pre['runtimeTested']==False;checks+=1
assert pre['buildAttempts']==pre['restoreAttempts']==pre['installAttempts']==0;checks+=1
assert pre['sourceFileCount']==len(pre['sourceFileSha256'])==18;checks+=1
for f in P.glob('*.json'):json.loads(f.read_text())
for link in re.findall(r'\[[^\]]*\]\(([^)]+)\)',(P.parents[1]/'QA-W2-03-report.md').read_text()):assert (P.parents[1]/link).exists();checks+=1
out=dict(status='PASS static evidence only; production QA BLOCKED/NOT RUN',checks=checks,fail=0,skip=0,productionExecutions=0,nativeExecutions=0,clearRows=42,sequenceSteps=6)
(P/'static-validation.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
