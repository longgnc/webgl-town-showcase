from pathlib import Path
import json,base64
root=Path(__file__).resolve().parents[1]
manifest=json.loads((root/'assets/pbr/manifest.json').read_text(encoding='utf-8'))
data={}
for asset in manifest:
    data[asset['asset']]={}
    for item in asset['maps']:
        p=root/'assets/pbr'/item['file']
        data[asset['asset']][item['channel']]='data:image/jpeg;base64,'+base64.b64encode(p.read_bytes()).decode()
(root/'assets/pbr-data.js').write_text('/* Poly Haven CC0 maps; see assets/pbr/manifest.json. */\nwindow.PBR_DATA='+json.dumps(data,separators=(',',':'))+';\n',encoding='utf-8')
print('Embedded PBR bytes:',(root/'assets/pbr-data.js').stat().st_size)
