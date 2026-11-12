from pathlib import Path
import importlib.util,sys
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('editor',HERE/'剪辑宣传片.py');e=importlib.util.module_from_spec(spec);spec.loader.exec_module(e);e.D=70

def render(key,title):
 parts=[e.TMP/f'{key}-{i}.mp4' for i in [0,1,3]]
 for i in range(6):
  p=e.TMP/f'{key}-feature-{i}.mp4'
  # 日夜变化使用场景原始光照，剪辑仅统一尺寸与帧率。
  e.run(['-ss',i*8+.5,'-i',e.BASE/'原始素材'/f'{key}.webm','-t','7','-an','-vf','scale=1920:1080,setsar=1,fps=30,fade=t=in:d=0.25,fade=t=out:st=6.75:d=0.25','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-threads','4',p]);parts.append(p)
 parts.append(e.TMP/f'{key}-5.mp4')
 listing=e.TMP/f'{key}-full.txt';listing.write_text('\n'.join("file '"+p.as_posix()+"'" for p in parts),encoding='utf-8')
 joined=e.TMP/f'{key}-full.mp4';e.run(['-f','concat','-safe','0','-i',listing,'-c','copy',joined])
 old=(e.TMP/f'{key}.ass').read_text(encoding='utf-8-sig');header=old.split('[Events]')[0]+'[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n'
 events=[f'Dialogue: 0,0:00:01.00,0:00:05.00,Title,,0,0,0,,{{\\fad(700,700)}}{title}', 'Dialogue: 0,0:00:00.00,0:01:10.00,Small,,0,0,0,,WEBGL REALTIME  /  浏览器实机画面']
 captions=['风过白墙，水映青瓦','循着河水，走近古镇','换个角度，看见旧时光'] if key=='yunxi' else ['从一幅画，到一座可探索的城','汴河穿城，舟楫相衔','穿过城门，走入画中街巷']
 for i,c in enumerate(captions):events.append(f'Dialogue: 0,{e.stamp(i*7+1)},{e.stamp(i*7+6)},Text,,0,0,0,,{{\\fad(350,350)}}{c}')
 events.extend(['Dialogue: 0,0:01:04.00,0:01:09.50,Title,,0,0,0,,{\\fad(500,600)}打开浏览器，亲自探索','Dialogue: 0,0:01:04.00,0:01:10.00,Text,,0,0,0,,参照 Saltline / 几猫传播版开发 · 来源与致谢见 README'])
 ass=e.TMP/f'{key}-full.ass';ass.write_text(header+'\n'.join(events),encoding='utf-8-sig');esc=ass.as_posix().replace(':','\\:')
 target=e.OUT/f'{title}_宣传片_含功能与三时段.mp4'
 # 功能部分保留原录制状态字幕，底栏不遮挡。
 filt=f"drawbox=x=0:y=0:w=iw:h=80:color=black:t=fill,ass='{esc}'"
 e.run(['-i',joined,'-i',e.music(key),'-vf',filt,'-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-t','70','-movflags','+faststart','-threads','4',target]);print('DONE',target,flush=True)
if __name__=='__main__':
 key=sys.argv[1];render(key,'云溪古镇' if key=='yunxi' else '清明上河图')
