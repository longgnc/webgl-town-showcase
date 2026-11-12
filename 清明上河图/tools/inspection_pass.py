from pathlib import Path
root=Path(__file__).resolve().parents[1];p=root/'scene.js';s=p.read_text(encoding='utf-8')
s=s.replace('strip(-24,-18,M.stone);strip(18,24,M.stone);','strip(-28.3,-18,M.stone);strip(18,28.3,M.stone);')
s=s.replace('renderPaving();resolveLandmarks();', 'road(-148,-20,6,620);for(let z=-256.5;z<235;z+=27){if(Math.abs(z-35)>16&&Math.abs(z+92)>15)road(-72,z,82,4.2);}renderPaving();resolveLandmarks();')
idx=s.index('function setMood(v)')
s=s[:idx]+'''function inspectMaterial(kind){pause();$('settings').classList.add('hidden');mode='inspect';input.exitLock();const l=landmarks[7],r=roofDetails.filter(r=>r.d>5).sort((a,b)=>Math.hypot(a.x-l.x,a.z-l.z)-Math.hypot(b.x-l.x,b.z-l.z))[0],c=Math.cos(r.rot),sn=Math.sin(r.rot);let target;
 if(kind==='roof'){camera.position.set(r.x+sn*(r.d/2+4),r.y+1.9,r.z+c*(r.d/2+4));target=new V(r.x,r.y+r.h*.55,r.z);}
 else if(kind==='wood'){camera.position.set(r.x+sn*(r.d/2+1.9)+c*r.w*.32,1.65,r.z+c*(r.d/2+1.9)-sn*r.w*.32);target=new V(r.x+sn*(r.d/2-.9)+c*r.w*.32,1.65,r.z+c*(r.d/2-.9)-sn*r.w*.32);}
 else if(kind==='stone'){camera.position.set(riverX(-56)-24.7,1.1,-56);target=new V(riverX(-53)-25,.05,-53);}
 else{camera.position.set(riverX(105)+19.2,1.4,105);target=new V(riverX(130),-.85,130);}
 camera.lookAt(target);bird.target.copy(target);shadowUpdate();updateLod();updateRoofDetails();$('hint').textContent='材质近景 · B 返回鸟瞰 · Esc 菜单';$('location').textContent={roof:'青瓦与屋檐',wood:'木构与灰泥',stone:'石板铺地',water:'汴河水面'}[kind];}
''' +s[idx:]
s=s.replace("mode==='walk'?(quality==='low'?100:155):1000", "(mode==='walk'||mode==='inspect')?(quality==='low'?100:155):1000")
s=s.replace("const focus=mode==='walk'?player.pos:bird.target;const size=mode==='walk'?65:", "const focus=mode==='walk'?player.pos:mode==='inspect'?camera.position:bird.target;const size=(mode==='walk'||mode==='inspect')?65:")
s=s.replace("e.code==='Escape'&&mode==='bird'", "e.code==='Escape'&&(mode==='bird'||mode==='inspect')")
s=s.replace("$('enter').onclick=", "document.querySelectorAll('[data-inspect]').forEach(b=>b.onclick=()=>inspectMaterial(b.dataset.inspect));\n$('enter').onclick=")
s=s.replace("window.__town={ready:false", "window.__town={lightingReference:{source:'几猫国产3A大作_V1.html',post:{...originalTuning},sun:{direction:TOWN_ENGINE.lightSettings.dir.toArray(),color:TOWN_ENGINE.lightSettings.color.toArray(),intensity:9},environmentIntensity:2,shadow:4096,msaa:4,volSteps:24},ready:false")
s=s.replace("$('building-inventory').textContent=JSON.stringify(registry,null,2);", "$('building-inventory').textContent=JSON.stringify(registry,null,2);$('render-audit').textContent=JSON.stringify({lighting:window.__town.lightingReference,placement:window.__town.placement,rejected:placementRejected},null,2);")
p.write_text(s,encoding='utf-8')
h=root/'index.html';html=h.read_text(encoding='utf-8');html=html.replace('<details><summary>运行状态与检查</summary>', '<details><summary>查看材质近景</summary><div class="inspect-grid"><button data-inspect="roof">青瓦屋檐</button><button data-inspect="wood">木构灰泥</button><button data-inspect="stone">石板铺地</button><button data-inspect="water">汴河水面</button></div></details><details id="runtime-details"><summary>运行状态与检查</summary>');html=html.replace('<script id="building-inventory"', '<script id="render-audit" type="application/json">{}</script><script id="building-inventory"');h.write_text(html,encoding='utf-8')
s=p.read_text(encoding='utf-8').replace("document.querySelector('details').open=true", "$('runtime-details').open=true");p.write_text(s,encoding='utf-8')
css=root/'style.css';c=css.read_text(encoding='utf-8');c+='\n.inspect-grid{display:grid;grid-template-columns:1fr 1fr;gap:6px;margin:12px 0}.inspect-grid button{border:1px solid #c2b79555;padding:10px;font-size:11px}\n';css.write_text(c,encoding='utf-8')
# WebGL 2 explicitly samples the non-mipmapped shadow atlas, avoiding implicit derivatives in PCSS loops on D3D drivers.
v=root/'vendor/jimao-engine.js';vs=v.read_text(encoding='utf-8');vs=vs.replace('texture2D( shadowMap, sc.xy + o )','textureLod( shadowMap, sc.xy + o, 0.0 )');v.write_text(vs,encoding='utf-8')
print('Material UVs, paved forecourts and inspection cameras corrected.')
