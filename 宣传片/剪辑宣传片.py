"""剪辑本地实机录制；需要 FFmpeg、Python 和 NumPy。"""
from pathlib import Path
import subprocess, wave, numpy as np
BASE=Path(__file__).resolve().parent
OUT=BASE/'成片';OUT.mkdir(exist_ok=True)
TMP=BASE.parent/'.local/edit';TMP.mkdir(exist_ok=True)
SR=48000; D=42

def music(key):
 rng=np.random.default_rng(12 if key=='yunxi' else 26);track=np.zeros((SR*D,2),dtype=np.float64)
 notes=[62,65,69,72,74,77] if key=='yunxi' else [60,62,65,67,69,72]
 for j,start in enumerate(np.arange(0,D,.875)):
  note=notes[([0,2,3,1,4,2,5,3][j%8]+j//16)%6];freq=440*2**((note-69)/12);n=min(int(SR*3),len(track)-int(start*SR));t=np.arange(n)/SR
  sig=(np.sin(2*np.pi*freq*t)*np.exp(-t*1.5)+.28*np.sin(2*np.pi*freq*2.003*t)*np.exp(-t*3)+.1*np.sin(2*np.pi*freq*3*t)*np.exp(-t*5))*(1-np.exp(-t*80))*.14
  at=int(start*SR);pan=.3+.4*rng.random();track[at:at+n,0]+=sig*pan;track[at:at+n,1]+=sig*(1-pan)
  delay=int(.28*SR);nd=min(n,len(track)-at-delay)
  if nd>0:track[at+delay:at+delay+nd]+=sig[:nd,None]*.1
 for j,start in enumerate(np.arange(0,D,7)):
  n=min(SR*7,len(track)-int(start*SR));t=np.arange(n)/SR;f=440*2**((notes[j%6]-24-69)/12)
  sig=np.sin(np.pi*np.minimum(t/7,1))**2*(np.sin(2*np.pi*f*t)+.25*np.sin(2*np.pi*f*1.5*t))*.09
  track[int(start*SR):int(start*SR)+n]+=sig[:,None]
 fade=np.minimum(np.arange(len(track))/SR/2,1)*np.minimum((len(track)-np.arange(len(track)))/SR/3,1);track*=fade[:,None]
 path=TMP/f'{key}.wav'
 with wave.open(str(path),'wb') as w:w.setnchannels(2);w.setsampwidth(2);w.setframerate(SR);w.writeframes((np.clip(track,-.95,.95)*32767).astype('<i2').tobytes())
 return path

def run(args):subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y',*map(str,args)],check=True)
def stamp(sec):return f'0:{sec//60:02d}:{sec%60:02d}.00'

def edit(key,title,captions):
 audio=music(key);parts=[]
 for i in range(6):
  p=TMP/f'{key}-{i}.mp4';parts.append(p)
  run(['-ss',i*8+.6,'-i',BASE/'原始素材/风景'/f'{key}.webm','-t',7,'-an','-vf','scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,setsar=1,fps=30,fade=t=in:d=0.3,fade=t=out:st=6.7:d=0.3','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-threads','4',p])
 listing=TMP/f'{key}.txt';listing.write_text('\n'.join("file '"+p.as_posix()+"'" for p in parts),encoding='utf-8')
 joined=TMP/f'{key}-joined.mp4';run(['-f','concat','-safe','0','-i',listing,'-c','copy',joined])
 header='''[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Title,Microsoft YaHei,92,&H00E9E1CE,&H00FFFFFF,&H90000000,&H80000000,0,0,0,0,100,100,12,0,1,1,2,5,80,80,0,1
Style: Text,Microsoft YaHei,38,&H00E9E1CE,&H00FFFFFF,&H60000000,&H80000000,0,0,0,0,100,100,3,0,1,1,1,2,70,70,44,1
Style: Small,Microsoft YaHei,25,&H00D4CEBD,&H00FFFFFF,&H60000000,&H80000000,0,0,0,0,100,100,1,0,1,1,1,8,60,60,24,1
[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
'''
 events=[f'Dialogue: 0,0:00:01.00,0:00:05.00,Title,,0,0,0,,{{\\fad(700,700)}}{title}',f'Dialogue: 0,0:00:00.00,0:00:42.00,Small,,0,0,0,,WEBGL REALTIME  /  浏览器实机画面']
 for i,cap in enumerate(captions):events.append(f'Dialogue: 0,{stamp(i*7+1)},{stamp(i*7+6)},Text,,0,0,0,,{{\\fad(350,350)}}{cap}')
 events.append('Dialogue: 0,0:00:37.00,0:00:42.00,Text,,0,0,120,,{\\fad(500,700)}参照 Saltline / 几猫传播版开发 · 来源与致谢见项目 README')
 ass=TMP/f'{key}.ass';ass.write_text(header+'\n'.join(events),encoding='utf-8-sig')
 escaped=ass.as_posix().replace(':','\\:')
 target=OUT/f'{title}_宣传片.mp4'
 run(['-i',joined,'-i',audio,'-vf',f"drawbox=x=0:y=0:w=iw:h=90:color=black:t=fill,drawbox=x=0:y=ih-112:w=iw:h=112:color=black:t=fill,ass='{escaped}'",'-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-ar','48000','-t','42','-movflags','+faststart','-threads','4',target])
 run(['-ss','3','-i',target,'-frames:v','1','-update','1',OUT/f'{title}_封面.jpg'])
 print('DONE',target,flush=True)
if __name__=='__main__':
 import sys
 which=sys.argv[1:]
 if not which or 'yunxi' in which:edit('yunxi','云溪古镇',['风过滇西 · 水映旧时光','六桥两岸，沿溪而行','把脚步，留在石板路上','白墙灰瓦之间，自有山风','暮色落下，灯火初上','打开浏览器，亲自走进云溪'])
 if not which or 'qingming' in which:edit('qingming','清明上河图',['一卷繁华 · 步入汴京','舟楫相衔，一河连城','穿过城门，走近画中街巷','檐下光影，留下市井的轮廓','白昼将尽，汴京灯火未眠','从观看画卷，到走进画卷'])
