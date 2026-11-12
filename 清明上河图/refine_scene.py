from pathlib import Path
import base64

root=Path(__file__).parent
p=root/'scene.js'
s=p.read_text(encoding='utf-8')
# A closer opening composition makes the scene's principal bridge readable.
s=s.replace("bird={target:new V(0,0,35),azimuth:.78,elevation:.65,radius:220}","bird={target:new V(-9,0,35),azimuth:.83,elevation:.51,radius:135}")
s=s.replace("int:3.3,hemi:2.4","int:3.15,hemi:1.35").replace("density:.0016,ex:1.12","density:.00115,ex:1.04")
s=s.replace("v==='night'?.12:.6","v==='night'?.12:.4")
s=s.replace("openingTimer=setTimeout(finishOpening,10500)","openingTimer=setTimeout(finishOpening,matchMedia('(prefers-reduced-motion: reduce)').matches?250:10500)")
# Material sharing removes repeated sign textures without sacrificing lettering.
s=s.replace("function label(text,", "const labelMaterials=new Map(),signGeo=new T.PlaneGeometry(1,1);\nfunction label(text,")
start=s.index('function label(text,'); end=s.index('\nfunction lantern',start)
s=s[:start]+'''function label(text,x,y,z,w=2,h=.65,rot=0,bg='#273933',ink='#d7c59e'){const key=text+bg+ink;let material=labelMaterials.get(key);if(!material){const c=document.createElement('canvas');c.width=512;c.height=128;const g=c.getContext('2d');g.fillStyle=bg;g.fillRect(0,0,512,128);g.strokeStyle='#aa9168';g.lineWidth=4;g.strokeRect(7,7,498,114);g.fillStyle=ink;g.textAlign='center';g.textBaseline='middle';g.font='64px KaiTi, STKaiti, serif';g.fillText(text,256,68,460);const t=new T.CanvasTexture(c);t.colorSpace=T.SRGBColorSpace;material=mat(0xffffff,.85,{map:t});labelMaterials.set(key,material);}batch(signGeo,material,x,y,z,w,h,1,rot);}
'''+s[end:]
# Bridge stalls stand at its edges, keeping a four-metre central crossing clear.
needle="bridges.push({z,center,half,hw,top});registry.push"
s=s.replace(needle,"""if(z===35)for(let k of [-2,-1,1,2])for(let side of [-1,1]){const x=center+k*8,y=top(x),zz=z+side*(hw-.45);for(let dx of [-1.3,1.3])box(M.darkWood,x+dx,y+1.2,zz,.065,2.4,.065);const awning=mesh(new T.PlaneGeometry(3,1.25,6,3),M.cloth,x,y+2.3,zz);awning.rotation.x=-Math.PI/2;animated.push({o:awning,base:y+2.3});}
 bridges.push({z,center,half,hw,top});registry.push""")
# Varied masses and street-facing shops instead of uniform warehouse blocks.
s=s.replace("register('', '补全街区',x+range(-1,1),z,range(15,19),range(15,19),rnd()<.32?2:1,iz%2?0:Math.PI,ix===0,1);", "register('', '补全街区',x+range(-2,2),z+range(-2,2),range(13,19),range(12,20),rnd()<.25?2:1,iz%2?0:Math.PI,ix<2,iz%3);")
old="if(Math.abs(z+92)<22||Math.abs(z-35)<15||Math.abs(z+190)<18)continue;register('', '城内街坊',x,z,range(18,23),range(24,29),rnd()<.4?2:1,Math.PI/2,ix===0,1);"
new="""if(Math.abs(z+92)<22||Math.abs(z-35)<15||Math.abs(z+190)<18)continue;if(Math.abs(x+194)<31&&Math.abs(z+65)<25||Math.abs(x+231)<37&&Math.abs(z+216)<33||Math.abs(x+219)<20&&Math.abs(z+113)<19)continue;
 if(ix>0&&(iz+ix)%3===0){register('', '城内院落',x,z-8,18,7,1,0,false,1);register('', '城内院落',x-7,z+3,7,13,1,0,false,0);register('', '城内院落',x+7,z+3,7,13,1,0,false,0);box(M.wall,x,.9,z+11,19,1.8,.3);tree(x,z+3,.65);}
 else register('', '城内街坊',x+range(-1,1),z+range(-2,2),range(16,22),range(19,27),rnd()<.3?2:1,Math.PI/2,ix===0,iz%3);"""
assert old in s
s=s.replace(old,new)
# Real street life includes seated tea customers, port workers, a boatman and rural workers.
s=s.replace("for(let i=0;i<vendorSpots.length;i++){", """for(let i=0;i<30;i++){const z=-270+i*18,side=i%2?1:-1,x=riverX(z)+side*24.9;if(Math.abs(z-35)<20||Math.abs(z+210)<15)continue;people.push({role:'customer',route:'fixed',x,z,y:0,yaw:side>0?-Math.PI/2:Math.PI/2,phase:rnd()*6,scale:range(.9,1.02),color:colors[i%8],hat:i%4===0,walk:0});}
 for(let i=0;i<12;i++){people.push({role:'farmer',route:'field',x:134+(i%3)*35,z:150+Math.floor(i/3)*35,zmin:140,zmax:285,direction:i%2?1:-1,speed:.35,phase:rnd()*6,scale:range(.9,1.02),color:colors[i%8],hat:true,walk:0});}
 for(let i=0;i<vendorSpots.length;i++){""")
s=s.replace("p.z>230||p.z<-280","p.z>(p.zmax??230)||p.z<(p.zmin??-280)")
s=s.replace("belt:[boxGeo,mat(0x524c3d,.95),1]", "belt:[boxGeo,mat(0x524c3d,.95),1],collar:[boxGeo,mat(0xc4b699,.98),2],bun:[sphereGeo,M.black,1],cuffs:[cylGeo,mat(0x94866c,.98),2]")
s=s.replace("personPart('coat',i,0,0,1.0,0,1,1,1,0,0,0,p.color);", """personPart('coat',i,0,0,1.0,0,1,1,1,0,0,0,p.color);personPart('collar',i,0,-.05,1.28,.155,.035,.22,.022,0,0,.52);personPart('collar',i,1,.055,1.27,.16,.035,.25,.022,0,0,-.52);personPart('bun',i,0,0,1.74,-.04,.065,.06,.06);""")
s=s.replace("personPart('feet',i,k,side*.1", "personPart('cuffs',i,k,side*.25,.82+gesture*.14,gesture*.4,.089,.08,.084,arm);personPart('feet',i,k,side*.1")
# Retain an inspectable, downloadable inventory in the DOM.
s=s.replace("window.__town.ready=true", "$('building-inventory').textContent=JSON.stringify(registry,null,2);window.__town.ready=true")
p.write_text(s,encoding='utf-8')

html=root/'index.html'
h=html.read_text(encoding='utf-8').replace('<div class="scroll-paper"></div>','<div class="scroll-paper"></div><div class="scroll-painting"></div>')
h=h.replace('<div id="fatal"','<script id="building-inventory" type="application/json">[]</script><div id="fatal"')
html.write_text(h,encoding='utf-8')
css=root/'style.css'
c=css.read_text(encoding='utf-8')
jpg=base64.b64encode((root/'assets/故宫藏本参考.jpg').read_bytes()).decode()
c+='\n.scroll-painting{position:absolute;inset:7% 0;background:#b9a17b url(data:image/jpeg;base64,'+jpg+') center/cover no-repeat;opacity:0;filter:sepia(.2);}.unfold .scroll-painting{animation:paintingReveal 10.5s ease-in-out forwards}@keyframes paintingReveal{0%,14%{clip-path:inset(0 50%);opacity:1}52%{clip-path:inset(0 3%);opacity:1}67%{clip-path:inset(0 1%);opacity:.65}88%,100%{clip-path:inset(0);opacity:0}}@media(prefers-reduced-motion:reduce){.unfold .scroll-painting{animation-duration:.1s}}\n'
css.write_text(c,encoding='utf-8')
print('Scene and scroll refined.')
