#!/usr/bin/env python3
"""Work1 exact-source QA; reads frozen expectations, never regenerates them."""
import argparse, hashlib, json, os, subprocess, sys
from pathlib import Path
SHA='49e7c263a36aebcc0316e010a629c6bfdf205f6d'
BASE=Path(__file__).resolve().parent

def command(args, cwd):
    r=subprocess.run(args,cwd=cwd,capture_output=True,text=True)
    return dict(command=args,exit=r.returncode,stdout=r.stdout,stderr=r.stderr)

def project(expected,actual):
    if isinstance(expected,dict):
        if 'approx' in expected:return actual
        return {k:project(v,actual[k]) for k,v in expected.items()}
    if isinstance(expected,list):return [project(v,actual[i]) for i,v in enumerate(expected)]
    return actual

def main():
    p=argparse.ArgumentParser();p.add_argument('--production-root',required=True);p.add_argument('--output',required=True);p.add_argument('--raw-output',default='/tmp/qa-w2-01-full-runtime.json');a=p.parse_args()
    root=Path(a.production_root).resolve();dst=Path(a.output).resolve();dst.parent.mkdir(parents=True,exist_ok=True)
    def git(*s):return subprocess.check_output(['git',*s],cwd=root)
    source={}
    paths=git('ls-tree','-r','--name-only',SHA,'reconstructed/core','reconstructed/godot/bridge').decode().splitlines()
    for path in paths:
        expected=git('show',SHA+':'+path);actual=(root/path).read_bytes()
        if expected!=actual:raise SystemExit('BLOCKED: source mismatch '+path)
        source[path]=hashlib.sha256(actual).hexdigest()
    allowed=set(paths)
    for sub in ['reconstructed/core','reconstructed/godot/bridge']:
        for path in (root/sub).rglob('*.cs'):
            if not {'bin','obj'}.intersection(path.relative_to(root).parts) and path.relative_to(root).as_posix() not in allowed:raise SystemExit('BLOCKED: extra compile source '+str(path))
    manifest=json.loads((BASE/'manifest.json').read_text());assert manifest['productionSha']==SHA
    cases=[json.loads((BASE/path).read_text()) for path in manifest['cases']]
    for c in cases:
        assert hashlib.sha256((BASE/c['aff']).read_bytes()).hexdigest()==c['affSha256'],c['id']+' fixture mismatch'
    commands=[command(['dotnet','build',str(BASE/'driver/Driver.csproj'),'-c','Release','-p:ProductionRoot='+str(root),'-m:1','-nr:false'],root)]
    if commands[-1]['exit']:raise SystemExit(json.dumps(commands[-1]))
    commands.append(command(['dotnet',str(BASE/'driver/bin/Release/net10.0/Driver.dll'),str(BASE),str(Path(a.raw_output).resolve())],root))
    raw=Path(a.raw_output).read_bytes();data=json.loads(raw);results=[];assertions=0
    for c,r in zip(cases,data['results'],strict=True):
        assert c['id']==r['id'];rows=[]
        for t in r.get('trace',[]):
            expectation=t.get('sample',{}).get('expect') if 'sample' in t else c['events'][t['index']].get('expect')
            if not expectation:continue
            def leaves(v):return sum(leaves(x) for x in v.values()) if isinstance(v,dict) and 'approx' not in v else sum(leaves(x) for x in v) if isinstance(v,list) else 1
            assertions+=leaves(expectation)
            try:observed=project(expectation,t['actual'])
            except (KeyError,IndexError,TypeError):observed=t['actual']
            rows.append(dict(event=t.get('index',t.get('sample')),expected=expectation,actual=observed,difference=t['difference']))
        results.append(dict(id=r['id'],classification=c['classification'],status=r['status'],firstDifference=r['firstDifference'],comparisons=rows))
    receipt=dict(assignment='QA-W2-01',exactProductionSha=SHA,checkoutHead=git('rev-parse','HEAD').decode().strip(),sourceSha256=source,manifestSha256=hashlib.sha256((BASE/'manifest.json').read_bytes()).hexdigest(),rawOutputSha256=hashlib.sha256(raw).hexdigest(),commands=commands,counts=dict(passed=sum(r['status']=='PASS' for r in results),failed=sum(r['status']!='PASS' for r in results),skipped=0,assertedLeaves=assertions),results=results,firstDivergences=[dict(id=r['id'],firstDifference=r['firstDifference']) for r in results if r['status']!='PASS'],notVerified=['G-006','G-007','G-009','G-010'])
    dst.write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt['counts']));return int(receipt['counts']['failed']!=0)
if __name__=='__main__':sys.exit(main())
