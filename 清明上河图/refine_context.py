from pathlib import Path
p=Path(__file__).with_name('scene.js');s=p.read_text(encoding='utf-8')
s=s.replace("const registry=[],roads=[],carts=[],waterwheels=[];", """const registry=[],roads=[],carts=[],waterwheels=[];
const earthCanvas=document.createElement('canvas');earthCanvas.width=earthCanvas.height=512;{const g=earthCanvas.getContext('2d');g.fillStyle='#aaa38c';g.fillRect(0,0,512,512);for(let i=0;i<500;i++){const x=rnd()*512,y=rnd()*512,r=range(3,44),a=g.createRadialGradient(x,y,0,x,y,r);a.addColorStop(0,rnd()<.5?'#626c4a32':'#ded4b634');a.addColorStop(1,'#aaa38c00');g.fillStyle=a;g.fillRect(x-r,y-r,r*2,r*2);}for(let i=0;i<22000;i++){g.fillStyle=rnd()<.5?'#343c3022':'#e2d9bd44';g.fillRect(rnd()*512,rnd()*512,range(1,3),range(1,3));}}const earthTex=new T.CanvasTexture(earthCanvas);earthTex.wrapS=earthTex.wrapT=T.RepeatWrapping;earthTex.colorSpace=T.SRGBColorSpace;earthTex.anisotropy=8;const earthMat=worldMat(0xd7d3bc,earthTex,.08,.98);
""")
s=s.replace("segments=180;for(let i=0;i<=segments;i++){const z=-350+i*700/segments", "segments=480;for(let i=0;i<=segments;i++){const z=-1200+i*2400/segments")
start=s.index('function terrain(side)');end=s.index('\nfunction road',start)
s=s[:start]+"""function terrain(side){const p=[],uv=[],ix=[];for(let i=0;i<=480;i++){const z=-1200+i*5,c=riverX(z),inner=c+side*18,outer=side*1400;p.push(inner,0,z,outer,0,z);uv.push(inner*.1,z*.1,outer*.1,z*.1);if(i<480){const n=i*2;side>0?ix.push(n,n+2,n+1,n+1,n+2,n+3):ix.push(n,n+1,n+2,n+1,n+3,n+2);}}const g=new T.BufferGeometry();g.setAttribute('position',new T.Float32BufferAttribute(p,3));g.setAttribute('uv',new T.Float32BufferAttribute(uv,2));g.setIndex(ix);g.computeVertexNormals();const o=mesh(g,earthMat,0,-.08,0);o.castShadow=false;}
"""+s[end:]
needle="landmarks.push({name:'虹桥闹市'"
pos=s.index(needle)
s=s[:pos]+"""// The town sits in a continuous plain, with an agricultural fringe instead of an exposed diorama edge.
 for(let side of [-1,1])for(let i=0;i<70;i++){const z=-370+i*11+range(-4,4),x=side*range(287,350);tree(x,z,range(.9,1.7),false);}for(let i=0;i<55;i++){const x=range(-310,310),z=i%2?range(355,410):range(-410,-355);if(Math.abs(x-riverX(z))>35)tree(x,z,range(.9,1.8));}
 for(let side of [-1,1])for(let i=0;i<6;i++)field(side*(170+(i%3)*42),side*(335+Math.floor(i/3)*44),34,35,i%3);
 // Store rear yards have low walls and lean-tos, breaking repeated roof silhouettes.
 for(const b of buildings.slice()){if(Math.abs(b.x-riverX(b.z))>46||Math.abs(b.z-35)<20||Math.abs(b.z+210)<20)continue;const side=b.x>riverX(b.z)?1:-1,x=b.x+side*(b.d/2+2.6);box(M.wall,x,.7,b.z,4.4,1.4,.24);for(let dz of [-b.w/2,b.w/2])box(M.wall,x,.7,b.z+dz,4.4,1.4,.24);box(M.wall,x+side*2.2,.7,b.z,.24,1.4,b.w);for(let k=0;k<3;k++)batch(jarGeo,M.pot,x,.1,b.z-2+k,1,1,1);}
 """+s[pos:]
# A boatman is grouped with each boat, so his body follows the hull and oar.
s=s.replace("g.position.set(x,-.55,z);scene.add(g);boats.push", """part(cylGeo,M.darkWood,-.5,1.12,4.4,.2,.65,.22);part(sphereGeo,mat(0xb79576,.9),-.5,1.64,4.4,.13,.17,.13);part(new T.ConeGeometry(.3,.15,12),marketMats.bamboo,-.5,1.86,4.4);part(boxGeo,M.darkWood,-.7,1.2,4.6,.08,.1,.5,0,.65);g.position.set(x,-.55,z);scene.add(g);boats.push""")
p.write_text(s,encoding='utf-8');print('Continuous terrain, rear yards, boatmen added.')
