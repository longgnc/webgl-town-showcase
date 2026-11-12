from pathlib import Path
root=Path(__file__).resolve().parents[1];p=root/'scene.js';s=p.read_text(encoding='utf-8')
a=s.index('function register(');b=s.index('\nfunction rainbowBridge',a)
s=s[:a]+'''function register(name,zone,x,z,w,d,h=1,rot=0,shop=true,variant=1){const bounds=orientedBox(x,z,w,d,rot,shop);const reserved=!name&&zone!=='寺观院落'&&reservedLandmarks.some(b=>boxOverlaps(bounds,b));if(reserved||placementBoxes.some(b=>boxOverlaps(bounds,b))){placementRejected.push({name,zone,x,z,reason:reserved?'地标预留区':'屋檐或店前净距不足'});return false;}placementBoxes.push({...bounds,top:h*3.1+3});house(x,z,w,d,h,rot,shop,variant);registry.push({id:registry.length+1,name,zone,x,z,w,d,levels:h,evidence:zone==='补全街区'?'补全设计':'原画场景类型，尺寸与背面为设计补全'});if(name){const dx=Math.sin(rot)*(d/2+.2),dz=Math.cos(rot)*(d/2+.2);label(name,x+dx,3.02,z+dz,Math.min(w*.72,4.6),.65,rot);}return true;}
''' +s[b:]
s=s.replace('function road(x,z,w,d){box(M.stone,x,.015,z,w,.03,d);roads.push({x,z,w,d});}', 'function road(x,z,w,d){roads.push({x,z,w,d});}')
s=s.replace('collision(x,z,swap?d:w,swap?w:d,0,h+3)', 'collision(x,z,Math.abs(Math.cos(rot))*w+Math.abs(Math.sin(rot))*d,Math.abs(Math.sin(rot))*w+Math.abs(Math.cos(rot))*d,0,h+3)')
s=s.replace('box(M.wood,x,top(x)+.75,z+side*(hw-.5),2.6,.09,.8);','box(M.wood,x,top(x)+.75,z+side*(hw-.5),2.6,.09,.8);collision(x,z+side*(hw-.5),2.6,.8,top(x),1.15);')
s=s.replace('y+1.2,zz,.065,2.4,.065','y+1.45,zz,.065,2.9,.065').replace('x,y+2.3,zz','x,y+2.9,zz').replace('base:y+2.3','base:y+2.9')
s=s.replace('for(let dx of [-w/2,w/2])for(let dz of [-d/2,d/2])box(M.darkWood,x+dx,1.45,z+dz,.09,2.9,.09);','for(let dx of [-w/2,w/2])for(let dz of [-d/2,d/2]){box(M.darkWood,x+dx,1.45,z+dz,.09,2.9,.09);collision(x+dx,z+dz,.09,.09,0,2.9);}')
s=s.replace('function umbrella(x,z){batch','function umbrella(x,z){collision(x,z,.09,.09,0,2.8);batch')
s=s.replace('const q=P(w*.28,d/2+1.4);for(let k=0;k<3;k++)','const q=P(w*.28,d/2+1.4);collision(q[0],q[1],.85,.85,0,1.5);for(let k=0;k<3;k++)')
s=s.replace('for(let i=0;i<10;i++)handCart(-103-i*11,42,false)','for(let i=0;i<10;i++)handCart(-103-i*11,44,false)')
s=s.replace('for(const b of batches.values()){','renderPaving();resolveLandmarks();window.__town.placement={accepted:placementBoxes.length,rejected:placementRejected.length,overlaps:auditPlacement()};for(const b of batches.values()){',1)
idx=s.index('async function buildTown()');s=s[:idx]+(root/'geometry-realism.part.js').read_text(encoding='utf-8')+'\n'+s[idx:]
a=s.index('function setupWater()');b=s.index('\nlet particles',a);s=s[:a]+(root/'water-realism.part.js').read_text(encoding='utf-8')+s[b:]
s=s.replace('camera.lookAt(bird.target);','avoidBirdClipping();camera.lookAt(bird.target);')
s=s.replace('function canMove(x,z){if(Math.abs(x)>276','function canMove(x,z){for(const b of bridges)if(Math.abs(x-b.center)<b.half&&Math.abs(z-b.z)>b.hw-.33&&Math.abs(z-b.z)<b.hw+.25&&player.pos.y<b.top(x)+1.18)return false;if(Math.abs(x)>276')
s=s.replace("const dyeTex=new T.CanvasTexture(dyeCanvas);dyeTex.colorSpace=T.SRGBColorSpace;const dyeMat=mat(0xffffff,.92,{map:dyeTex,side:T.DoubleSide});dyeMat.onBeforeCompile=s=>{", "const dyeTex=new T.CanvasTexture(dyeCanvas);dyeTex.colorSpace=T.SRGBColorSpace;const dyeMat=REALISM.material('white_plaster_02',{color:0x888574,scale:1.5,normal:.2,wetness:.15});dyeMat.side=T.DoubleSide;const dyeCompile=dyeMat.onBeforeCompile;dyeMat.onBeforeCompile=s=>{dyeCompile(s);")
p.write_text(s,encoding='utf-8');print('Geometry, clearance checks and river shading integrated.')
