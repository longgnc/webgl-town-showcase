from pathlib import Path
root=Path(__file__).resolve().parents[1];p=root/'scene.js';s=p.read_text(encoding='utf-8')
s=s.replace('scale:2.4,normal:.4,wetness:.25','scale:1.6,normal:.22,wetness:.25,standardUV:true')
s=s.replace('color:0xa68b62,scale:1,normal:.25,wetness:.1','color:0xc1ae8e,scale:1,normal:.15,wetness:.1,standardUV:true')
s=s.replace('new T.Vector2(.27,.27),new T.Vector2(.23,.25),new T.Vector2(.15,.06)],12)','new T.Vector2(.27,.27),new T.Vector2(.23,.25),new T.Vector2(.15,.06)],24)')
s=s.replace('new T.Vector2(.15,.7),new T.Vector2(.19,.72)],12)','new T.Vector2(.15,.7),new T.Vector2(.19,.72)],24)')
s=s.replace('ceramic:mat(0x7d9b90,.35)',"ceramic:REALISM.material('white_plaster_02',{color:0x8d8978,scale:1.4,normal:.15,rough:.48,standardUV:true})")
s=s.replace('center-1.3+(i%3)*1.25,b=front-.4+Math.floor(i/3)*.75','center-1.15+(i%3)*1.05,b=front-.35+Math.floor(i/3)*.65')
s=s.replace("p[0],.92,p[1],.6,.65,.6,rot);batch(bowlGeo,marketMats.ceramic,p[0]+.22,.92,p[1]+.12,.7,.7,.7);", "p[0],.9,p[1],.6,.65,.6,rot);const bp=P(a+.4,b);batch(bowlGeo,marketMats.ceramic,bp[0],.9,bp[1],.7,.7,.7);")
s=s.replace('x-side*(i*.65),.15,z-3+j','x-side*(i*.65),.125,z-3+j')
s=s.replace('(i%3-1)*.8,.7,-3+Math.floor(i/3)*.9','(i%3-1)*.8,.665,-3+Math.floor(i/3)*.9')
s=s.replace('new T.CylinderGeometry(1.3,1.3,3.8,16,1,true,0,Math.PI)','new T.CylinderGeometry(1.3,1.3,3.8,24,1,true,Math.PI/2,Math.PI)')
a=s.index('function lantern(');b=s.index('\nconst names=',a)
s=s[:a]+'''const lanternSphere=new T.SphereGeometry(1,24,16);
function lantern(x,y,z){lanternSites.push(new V(x,y,z));batch(lanternSphere,M.lantern,x,y,z,.32,.46,.32);box(M.darkWood,x,y+.44,z,.27,.045,.27);box(M.darkWood,x,y-.43,z,.24,.045,.24);box(M.cloth,x,y-.65,z,.035,.38,.035);for(let k=0;k<8;k++){const a=k/8*Math.PI*2;let prev;for(let j=0;j<=8;j++){const yy=-.395+j*.79/8,r=.326*Math.sqrt(Math.max(0,1-(yy/.46)**2)),p=new V(x+Math.cos(a)*r,y+yy,z+Math.sin(a)*r);if(prev)beam(M.darkWood,prev,p,.006);prev=p;}}}
''' +s[b:]
s=s.replace('camera.position.set(riverX(105)+19.2,1.4,105);target=new V(riverX(130),-.85,130);','camera.position.set(riverX(148)+19.4,1.3,148);target=new V(riverX(170)-4,-.85,170);')
s=s.replace('async function buildTown(){await REALISM.ready;',"async function buildTown(){$('boot-msg').textContent='正在读取 2K 写实材质与法线';await REALISM.ready;")
s=s.replace("window.__town.ready=true;$('boot').classList.add('hidden');", "$('boot-msg').textContent='正在编译原版光照与写实表面';$('boot-fill').style.width='88%';await new Promise(requestAnimationFrame);await renderer.compileAsync(scene,camera);for(const m of originalPost.materials){originalPost.quad.material=m;await renderer.compileAsync(originalPost.quad,originalPost.fsCam);}$('boot-fill').style.width='100%';window.__town.ready=true;$('boot').classList.add('hidden');")
# Add direct collision regressions, beyond nominal bounding-box checks.
needle="check('建筑屋顶无相互穿插',auditPlacement().length===0,auditPlacement().length);"
extra="""for(const l of landmarks){const nearest=buildings.reduce((a,b)=>Math.hypot(b.x-l.x,b.z-l.z)<Math.hypot(a.x-l.x,a.z-l.z)?b:a,buildings[0]);player.pos.y=0;check('建筑实体阻挡 '+l.name,!canMove(nearest.x,nearest.z));}for(const b of bridges){player.pos.y=b.top(b.center);check('桥栏阻挡 z='+b.z,!canMove(b.center,b.z+b.hw-.15));}const cart=carts[0];player.pos.y=0;check('货车实体阻挡',!canMove(cart.x,cart.z));"""
assert needle in s;s=s.replace(needle,needle+extra)
p.write_text(s,encoding='utf-8');print('Props refined, extra collision tests and shader warm-up added.')
