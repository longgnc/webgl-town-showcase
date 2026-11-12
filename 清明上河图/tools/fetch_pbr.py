"""Download identified CC0 PBR maps from the official Poly Haven API, keeping provenance."""
from pathlib import Path
import urllib.request,json,concurrent.futures

root=Path(__file__).resolve().parents[1]/'assets'/'pbr'
ids=['pavement_01','weathered_brown_planks','white_plaster_02','grey_roof_tiles','stone_brick_wall_001','brown_mud_dry']
def get(url):
    req=urllib.request.Request(url,headers={'User-Agent':'Qingming-local-scene/1.0'})
    with urllib.request.urlopen(req,timeout=90) as r:return r.read()
def work(asset):
    dest=root/asset;dest.mkdir(parents=True,exist_ok=True)
    meta=json.loads((dest/'files.json').read_text(encoding='utf-8')) if (dest/'files.json').exists() else json.loads(get('https://api.polyhaven.com/files/'+asset))
    (dest/'files.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding='utf-8')
    records=[]
    for channel in ['diff','nor_gl','rough','disp','ao']:
        variants=meta.get({'diff':'Diffuse','rough':'Rough','disp':'Displacement','ao':'AO'}.get(channel,channel),{})
        resolution='2k' if channel in ['diff','nor_gl'] else '1k'
        options=variants.get(resolution,{})
        choice=options.get('jpg') or options.get('png')
        if not choice:continue
        url=choice['url'];ext=url.rsplit('.',1)[-1];file=dest/(channel+'.'+ext)
        if not file.exists():file.write_bytes(get(url))
        records.append({'channel':channel,'resolution':resolution,'file':str(file.relative_to(root)),'url':url,'bytes':file.stat().st_size})
    print(asset,[(r['channel'],r['bytes']) for r in records],flush=True)
    return {'asset':asset,'source':'https://polyhaven.com/a/'+asset,'license':'CC0','maps':records}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:records=list(pool.map(work,ids))
(root/'manifest.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
