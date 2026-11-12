"""Extract the exact reference's bundled engine and input without starting the FPS game."""
from pathlib import Path
import argparse, hashlib

if __name__ == '__main__':
    p=argparse.ArgumentParser();p.add_argument('reference',type=Path);p.add_argument('output',type=Path)
    a=p.parse_args();raw=a.reference.read_bytes();text=raw.decode('utf-8-sig')
    start=text.index('<script>')+len('<script>');end=text.index('</script>',start);script=text[start:end]
    expected=['M2="180"','function v_(i)','function Dy()','var lt={}', 'async function Gg(i)', 'function Hy(i)', 'function Oy()', 'function Vy(i,e)', 'QC().catch(i=>bM(i&&i.stack||i));']
    for marker in expected:
        if script.count(marker)!=1: raise SystemExit('Different reference version. Inspect before extracting: '+marker)
    script=script.replace(expected[-1],'window.TOWN_ENGINE={THREE:lt,createInput:v_,events:Dy,createMaterials:Gg,createSky:Hy,createNoise:Oy,captureEnvironment:Vy};')
    a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(script,encoding='utf-8')
    print('Reference SHA256: '+hashlib.sha256(raw).hexdigest());print('Saved '+str(a.output))
