#!/usr/bin/env python3
"""Validate source provenance and fixture structure; never loads/emulates native code."""
import argparse,copy,hashlib,json,re,struct,subprocess,sys,zipfile
from pathlib import Path
from normalize import normalize_aff
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
START='16d17765e6fe50251162a45ffd5d1a64f243acf5'

def sha(b):return hashlib.sha256(b).hexdigest()
def j(path):return json.loads(path.read_text())
def check_matrix(matrix,requirements,base):
    ids={r['id'] for r in requirements['requirements']};dependencies={r['id']:r['dependency'].split('/') for r in requirements['requirements']};fixtures=matrix['fixtures'];seen=set();checks=0
    for c in fixtures:
        assert c['id'] not in seen,c['id']+' duplicate';seen.add(c['id']);checks+=1
        raw=(base/c['aff']).read_bytes();assert sha(raw)==c['affSha256'],c['id']+' checksum';checks+=1
        assert raw.startswith(b'AudioOffset:0\nTimingPointDensityFactor:1.0\n-\n'),c['id']+' header';checks+=1
        assert normalize_aff(raw)==c['normalization'],c['id']+' lexical inventory';checks+=1
        assert all(q in ids for q in c['requirementIds']);checks+=1
        assert c['dependencyIds']==sorted({x for q in c['requirementIds'] for x in dependencies[q]});checks+=1
        assert c['normalization'] and c['preparedRuntime'] and c['inputSchedule'] and c['futureTests'];checks+=1
        assert c['readiness'] in ['EXISTING NATIVE CONTROL','SPECIFIED / NATIVE EXECUTION NOT AUTHORIZED'],c['id']+' unapproved runtime promotion';checks+=1
        if c['originalObserved'] is None:
            assert c['firstMissingOriginalFact'] and c['unknowns'];checks+=1
            assert c['confidence']=='instruction-backed predictions / NOT VERIFIED runtime';checks+=1
        assert c['evidence'] and c['campaignRequirementIds'];checks+=1
    for c in fixtures:
        assert all(x in seen for x in c['controlFixtureIds']);checks+=1
    return checks

def static_archive(path,anchors):
    with zipfile.ZipFile(path) as z:raw=z.read(anchors['libraryMember'])
    assert sha(raw)==anchors['librarySha256'],'original ELF SHA mismatch'
    assert raw[:6]==b'\x7fELF\x02\x01' and struct.unpack_from('<H',raw,18)[0]==183
    phoff=struct.unpack_from('<Q',raw,32)[0];phsize,phnum=struct.unpack_from('<HH',raw,54)
    segments=[struct.unpack_from('<IIQQQQQQ',raw,phoff+i*phsize) for i in range(phnum)]
    def readva(a,n):
        for typ,flags,off,va,pa,filesz,memsz,align in segments:
            if typ==1 and va<=a and a+n<=va+filesz:return raw[off+a-va:off+a-va+n]
        raise AssertionError('VA unmapped '+hex(a))
    for item in anchors['anchors']+anchors['constants']:
        expected=bytes.fromhex(item['bytes']);assert readva(int(item['va'],16),len(expected))==expected,item['va']
    shoff=struct.unpack_from('<Q',raw,40)[0];shsize,shnum=struct.unpack_from('<HH',raw,58)
    relocs={}
    wanted={int(r['va'],16) for r in anchors['relocations']}
    for i in range(shnum):
        _,typ,_,_,off,size,_,_,_,entry=struct.unpack_from('<IIQQQQIIQQ',raw,shoff+i*shsize)
        if typ==4:
            for at in range(off,off+size,entry):
                addr,info,addend=struct.unpack_from('<QQq',raw,at)
                if addr in wanted:relocs[addr]=addend
    for r in anchors['relocations']:assert relocs[int(r['va'],16)]==int(r['target'],16)
    return dict(sha256=sha(raw),bytes=len(raw),elf='ELF64 little-endian AArch64',instructionAnchors=len(anchors['anchors']),constants=len(anchors['constants']),relocations=len(wanted),execution='NOT RUN; byte reads only')

def main():
    p=argparse.ArgumentParser();p.add_argument('--archive');p.add_argument('--output',required=True);a=p.parse_args();matrix=j(HERE/'fixtures.json');requirements=j(HERE/'requirements.json');sources=j(HERE/'sources.json')
    checks=check_matrix(matrix,requirements,HERE);source_checks=0
    for s in sources['sources']:
        original=subprocess.check_output(['git','show',START+':'+s['path']],cwd=ROOT)
        assert sha(original)==s['sha256'],s['path']+' historical source mismatch';source_checks+=1
    control_copies=0
    for c in matrix['fixtures']:
        if c['originalObserved'] is not None:
            source=c['evidence'][0]['fixture']
            original=subprocess.check_output(['git','show',START+':'+source],cwd=ROOT)
            assert original==(HERE/c['aff']).read_bytes(),c['id']+' historical control byte mismatch'
            control_copies+=1
    source_ids={r['id'] for r in requirements['requirements']}
    fixture_ids={c['id'] for c in matrix['fixtures']}
    for proposal in j(HERE/'proposed-experiments.json')['proposals']:
        assert all(f in fixture_ids for f in proposal['fixtures'])
        assert all(proposal.get(k) for k in ['owningEntry','objects','positiveCase','negativeControl','schedule','expectedObservations','passCriteria','failCriteria','stop','authorization']);checks+=1
    for r in requirements['requirements']:
        assert r['campaign'] and r['dependency'] and r['evidence'] and r['confidence'] and r['remaining'];checks+=1
    # Only numeric predicate expectations with fully specified operands are calculated.
    f=lambda x:struct.unpack('<f',struct.pack('<f',x))[0]
    arithmetic=[]
    for c in matrix['fixtures']:
        if c['id'].startswith('W102-GX-'):
            arcs=c['normalization']['objects'];x=float(arcs[1]['xTokens'][0]);delta=f(abs(f(f(x)-f(.5))))
            expected=c['instructionExpectations'];assert expected[0]['predicted']==delta and expected[1]['predicted']==(delta<.1)
            arithmetic.append(dict(id=c['id'],float32Delta=delta,predicate=delta<.1,classification='RECONSTRUCTED arithmetic, not native execution'))
    controls=[]
    for mode in ['badChecksum','falseRuntimePromotion']:
        bad=copy.deepcopy(matrix)
        if mode=='badChecksum':bad['fixtures'][0]['affSha256']='0'*64
        else:next(c for c in bad['fixtures'] if c['originalObserved'] is None)['readiness']='NATIVE PASS'
        try:check_matrix(bad,requirements,HERE)
        except AssertionError as e:controls.append(dict(id=mode,detected=True,diagnostic=str(e)))
        else:raise AssertionError(mode+' not detected')
    archive=static_archive(a.archive,j(HERE/'instruction-anchors.json')) if a.archive else dict(status='NOT RUN',reason='archive argument absent')
    result=dict(assignment='W1-02',sourceSha=START,productionAssessedSha=sources['acceptedProductionSha'],runtimeTestedSha=None,status='PASS evidence validation only',matrixFixtures=len(matrix['fixtures']),historicalNativeControls=sum(c['originalObserved'] is not None for c in matrix['fixtures']),proposedNotRun=sum(c['originalObserved'] is None for c in matrix['fixtures']),requirements=len(source_ids),matrixSha256=sha((HERE/'fixtures.json').read_bytes()),requirementsSha256=sha((HERE/'requirements.json').read_bytes()),historicalControlByteChecks=control_copies,structuralChecks=checks,sourceChecks=source_checks,arithmeticChecks=arithmetic,negativeControls=controls,archive=archive,productionRuntime='NOT RUN; prior QA not repeated',nativeRuntime='NOT RUN; no authorization',failures=0,skips=0)
    dest=Path(a.output);dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ['arithmeticChecks','archive']}));return 0
if __name__=='__main__':sys.exit(main())
