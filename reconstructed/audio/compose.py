#!/usr/bin/env python3
"""Clockwork Steps: original Project Arconist composition/recording, CC0-1.0.
Integer-only synthesis: same PCM on every host; no samples, codecs or network.
"""
from array import array
from pathlib import Path
import argparse
import hashlib
import json
import math
import struct
import wave

RATE = 22050
SECONDS = 32
BEAT = RATE // 2  # 120BPM: every beat is an exact sample index.
# Integer millihertz; fixed pitches, no platform libm oscillator/table dependency.
HZ = {'D2':73416,'F2':87307,'Bb2':116541,'C3':130813,'D3':146832,'F3':174614,
      'A3':220000,'C4':261626,'D4':293665,'E4':329628,'F4':349228,'G4':391995,
      'A4':440000,'C5':523251,'D5':587330}
CHORDS = [('D2',['D3','F3','A3']),('Bb2',['F3','A3','D4']),
          ('F2',['F3','A3','C4']),('C3',['G4','C4','E4'])]
MELODY = ['D4','F4','A4','F4','D5','A4','F4','E4',
          'F4','A4','C5','A4','G4','E4','C4','E4']


def render():
    mix = [0] * (RATE * SECONDS)
    def tone(at, length, frequency, amplitude, attack=110, decay=True):
        phase = 0
        step = frequency * (1 << 32) // (RATE * 1000)
        filtered = 0
        for n in range(min(length, len(mix)-at)):
            q = phase >> 16
            raw = 4*q-65536 if q < 32768 else 196608-4*q
            phase = (phase+step) & 0xffffffff
            filtered = (filtered*3+raw)//4
            env = min(4096, n*4096//max(1,attack), (length-n)*4096//max(1,length//5))
            if decay:
                env = env * (length-n)//length
                env = env * (length-n)//length
            mix[at+n] += filtered*amplitude*env//(65536*4096)
    def drum(at, accent):
        # A deterministic downward chirp plus short noise tick; no imported sample.
        phase=0;seed=0x13579b;length=RATE//9
        for n in range(min(length,len(mix)-at)):
            hz=155000-110000*n//length
            phase=(phase+hz*(1<<32)//(RATE*1000))&0xffffffff
            q=phase>>16;tri=4*q-65536 if q<32768 else 196608-4*q
            env=(length-n)*4096//length
            tick=0
            if n<RATE//100:
                seed=(1664525*seed+1013904223)&0xffffffff
                tick=((seed>>16)-32768)*(RATE//100-n)*1300//((RATE//100)*32768)
            mix[at+n] += tri*env*env*(7200 if accent else 4800)//(65536*4096*4096)+tick
    for beat in range(64):
        at=beat*BEAT
        drum(at,beat%4==0)
        if beat<4:
            tone(at,RATE//10,1200000,2600,attack=12)
            continue  # One bar of clear count-in before first playable tap at2s.
        bar=beat//4
        bass,chord=CHORDS[(bar-1)%4]
        if beat%2==0:tone(at,BEAT*2,HZ[bass],2800,attack=180)
        if beat%4==0:
            for pitch in chord:tone(at,BEAT*4,HZ[pitch],850,attack=900,decay=False)
        tone(at,BEAT,HZ[MELODY[(beat-4)%len(MELODY)]],1800)
        tone(at+BEAT//2,BEAT//2,HZ[chord[beat%3]],900,attack=70)
    # Deterministic headroom/fade. The generator never clips an intermediate sum.
    peak=max(abs(v) for v in mix)
    gain=24000*32768//max(1,peak)
    result=array('h')
    for i,v in enumerate(mix):
        v=v*gain//32768
        if i>=len(mix)-RATE//4:v=v*(len(mix)-i)//(RATE//4)
        result.append(max(-32768,min(32767,v)))
    if struct.pack('=H',1)!=struct.pack('<H',1):result.byteswap()
    return result.tobytes()


def generate(path, report):
    pcm=render();path.parent.mkdir(parents=True,exist_ok=True)
    with wave.open(str(path),'wb') as w:
        w.setnchannels(1);w.setsampwidth(2);w.setframerate(RATE);w.writeframes(pcm)
    # Offline signal evidence; never an assertion that a speaker was heard.
    samples=struct.unpack('<'+'h'*(len(pcm)//2),pcm)
    windows=[]
    for beat in range(64):
        segment=samples[beat*BEAT:beat*BEAT+RATE//20]
        rms=math.sqrt(sum(v*v for v in segment)/len(segment))
        assert rms>300, f'silent beat {beat}'
        windows.append({'beat':beat,'sample':beat*BEAT,'seconds':beat/2,'rms_first_50ms':rms})
    peak=max(abs(v) for v in samples)
    assert 3000<peak<=24001 and len(samples)==RATE*SECONDS
    result={'title':'Clockwork Steps','origin':'Original score/synthesis composed for Project Arconist R005; no third-party samples',
            'license':'CC0-1.0','rate':RATE,'channels':1,'bits':16,'duration_seconds':SECONDS,'bpm':120,
            'count_in_beats':4,'first_chart_note_ms':2000,'frames':len(samples),'peak':peak,
            'rms':math.sqrt(sum(v*v for v in samples)/len(samples)),
            'wav_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'pcm_sha256':hashlib.sha256(pcm).hexdigest(),
            'beats':windows,'physical_audibility':'NOT RUN','hardware_latency':'UNVERIFIED'}
    report.parent.mkdir(parents=True,exist_ok=True);report.write_text(json.dumps(result,indent=2)+'\n')
    return result


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',type=Path,required=True);p.add_argument('--report',type=Path,required=True)
    a=p.parse_args();r=generate(a.output,a.report);print(json.dumps({k:v for k,v in r.items() if k!='beats'},indent=2))
