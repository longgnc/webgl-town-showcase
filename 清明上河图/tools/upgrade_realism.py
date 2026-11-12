from pathlib import Path
root=Path(__file__).resolve().parents[1]
p=root/'scene.js';s=p.read_text(encoding='utf-8')
v=root/'vendor/jimao-engine.js';vs=v.read_text(encoding='utf-8')
vs=vs.replace('window.TOWN_ENGINE={THREE:lt,createInput:v_,events:Dy};','window.TOWN_ENGINE={THREE:lt,createInput:v_,events:Dy,createPost:jy,createNoise:Oy,createSky:Hy,captureEnvironment:Vy,installSoftShadows:qy,lightSettings:Mn,skySettings:en,quality:zy};')
v.write_text(vs,encoding='utf-8')
s=s.replace('new T.PerspectiveCamera(68,innerWidth/innerHeight,.12,1600)','new T.PerspectiveCamera(74,innerWidth/innerHeight,.08,1600)')
s=s.replace('antialias:true','antialias:false').replace('renderer.toneMapping=T.ACESFilmicToneMapping','renderer.toneMapping=T.NoToneMapping').replace('renderer.shadowMap.type=T.PCFSoftShadowMap','renderer.shadowMap.type=T.PCFShadowMap')
s=s.replace('scene.fog=new T.FogExp2(0xb9c2b0,.0018);','scene.fog=null;')
s=s.replace('0x968568,2.1','0x968568,0')
s=s.replace('const sun=new T.DirectionalLight(0xffe2ba,3.2);','const sun=new T.DirectionalLight(TOWN_ENGINE.lightSettings.color,9);')
s=s.replace('sun.shadow.mapSize.set(2048,2048)','sun.shadow.mapSize.set(4096,4096)').replace('sun.shadow.bias=-.0003;sun.shadow.normalBias=.06','sun.shadow.bias=-.00012;sun.shadow.normalBias=.02')
s=s.replace('const U={time:',"TOWN_ENGINE.installSoftShadows({width:130,height:130,depth:799},{taps:16,searchTaps:8});\nconst U={time:")
a=s.index('const M={');b=s.index('\nM.roof.side',a)
s=s[:a]+'''const M={wall:REALISM.material('white_plaster_02',{color:0xd8d2c1,scale:.36,normal:.7,wetness:.3}),stone:REALISM.material('pavement_01',{color:0xc6c9c4,scale:.36,rough:.95,normal:1.05,wetness:.9}),darkStone:REALISM.material('stone_brick_wall_001',{color:0xa8aaa1,scale:.48,normal:1,wetness:.65}),wood:REALISM.material('weathered_brown_planks',{color:0xc4b8a3,scale:.34,rough:.98,normal:.75,timber:true,wetness:.32}),darkWood:REALISM.material('weathered_brown_planks',{color:0x8e8574,scale:.34,rough:.98,normal:.85,timber:true,wetness:.35}),roof:REALISM.material('grey_roof_tiles',{color:0xa6aba9,scale:.45,normal:.8,wetness:.7}),trim:REALISM.material('white_plaster_02',{color:0x565b57,scale:1.2,normal:.4,wetness:.5}),white:REALISM.material('white_plaster_02',{color:0xcfc9ba,scale:.8}),black:mat(0x151712),gold:mat(0x867453,.65,{metalness:.45}),red:REALISM.material('weathered_brown_planks',{color:0x8b5440,scale:.4,timber:true}),cloth:REALISM.material('white_plaster_02',{color:0xa19478,scale:1.1,normal:.2,wetness:.2}),leaf:mat(0x526b3e,.92,{side:T.DoubleSide}),pine:mat(0x344e39),pot:REALISM.material('white_plaster_02',{color:0x735441,scale:2.4,normal:.4,wetness:.25}),glass:REALISM.material('white_plaster_02',{color:0x918c78,scale:1,normal:.15,wetness:.1})};
M.cloth.side=T.DoubleSide;M.glass.emissive=new T.Color(0xc38c42);M.glass.emissiveIntensity=.01;
const tileMat=REALISM.material('white_plaster_02',{color:0x555d5b,scale:2,normal:.38,rough:.88,vertexColors:true,wetness:.65});tileMat.side=T.DoubleSide;
const roofDetails=[],placementBoxes=[],placementRejected=[];
''' +s[b:]
s=s.replace('M.lantern=mat(0xb34a28,.7,{emissive:0xd75b22,emissiveIntensity:.4})',"M.lantern=REALISM.material('white_plaster_02',{color:0xa68b62,scale:1,normal:.25,wetness:.1});M.lantern.emissive=new T.Color(0xc27628);M.lantern.emissiveIntensity=.03")
s=s.replace('const gableMat=M.wall.clone();gableMat.side=T.DoubleSide;', 'const gableMat=M.wall.clone();gableMat.onBeforeCompile=M.wall.onBeforeCompile;gableMat.customProgramCacheKey=M.wall.customProgramCacheKey;gableMat.side=T.DoubleSide;')
s=s.replace('+.28*Math.pow(t,7)','+.08*Math.pow(t,7)')
# Match ridge trims to the real roof surface instead of the exaggerated old hooks.
s=s.replace("function roof(x,y,z,w,d,h,rot=0){batch", "function roof(x,y,z,w,d,h,rot=0){if(w>4&&d>4)roofDetails.push({x,y,z,w,d,h,rot,mesh:null});batch")
s=s.replace('y+h+.12),P(w/2,0,y+h+.12),.13','y+h+.055),P(w/2,0,y+h+.055),.09')
s=s.replace('y+.28),P(w/2,side*d/2,y+.28),.12','y+h*.08),P(w/2,side*d/2,y+h*.08),.055')
s=s.replace('Math.pow(t,5)*.4','Math.pow(t,5)*.06').replace('y+h*(1-t)**1.65+.08*Math.pow(t,7)','y+h*(1-t)**1.65+h*.08*Math.pow(t,7)').replace('beam(M.trim,prev,pt,.11)','beam(M.trim,prev,pt,.055)')
# Remove decorative cartoon flowers and fabric repeated on every storefront.
s=s.replace('if(built%2===0){','if(false){').replace("const f=P(w*.32,d/2+.32),cloth=mesh", "const f=P(w*.32,d/2+.32),cloth=mesh")
s=s.replace('cloth.rotation.y=rot;cloth.castShadow=false;streetBusiness','cloth.rotation.y=rot;cloth.visible=false;cloth.userData.disabled=true;cloth.castShadow=false;streetBusiness')
# Wall construction: hollow perimeter plus recessed façade bays, rather than a solid cuboid facade.
s=s.replace('B(M.wall,0,h/2+.55,0,w,h,d);', '''B(M.wall,-w/2+.11,h/2+.55,0,.22,h,d);B(M.wall,w/2-.11,h/2+.55,0,.22,h,d);B(M.wall,0,h/2+.55,-d/2+.11,w,h,.22);B(M.darkWood,0,.54,0,w,.09,d);
 for(let fl=0;fl<levels;fl++){const base=fl*3.1;B(M.wall,0,base+.84,d/2-.11,w,.58,.22);B(M.wall,0,base+3.2,d/2-.11,w,.86,.22);}const facadeBays=Math.max(2,Math.round(w/2.3));for(let k=0;k<=facadeBays;k++)B(M.wall,-w/2+k*w/facadeBays,h/2+.55,d/2-.11,.3,h,.22);
 B(M.black,0,h/2+.55,0,w-.5,h-.15,.08);''')
s=s.replace("B(floor===0&&j===1?M.darkWood:M.glass,a,yy,side*(d/2+.045),w/bays*.67,1.65,.06)","B(floor===0&&shop?M.black:M.glass,a,yy,side*(d/2-.10),w/bays*.86,1.65,.055)")
s=s.replace('h+.94,e[1],.07,.4,.07','h+.65+(1.9+variant*.25)*.08-.10,e[1],.055,.38,.055')
s=s.replace('const swap=Math.abs(Math.sin(rot))>.7;collision', '''for(let a=-w/2+.3;a<w/2;a+=w/3){B(M.darkWood,a,h+.37,d/2+.32,.42,.12,.62);B(M.wood,a,h+.46,d/2+.47,.65,.10,.55);const q=P(a,d/2-.05),r=P(a,d/2+.7);beam(M.darkWood,new V(q[0],h-.18,q[1]),new V(r[0],h+.46,r[1]),.06);}
 const swap=Math.abs(Math.sin(rot))>.7;collision''')
a=s.index('const skyMat=');b=s.index('\nfunction unusedMountains',a)
s=s[:a]+'''const originalNoise=TOWN_ENGINE.createNoise(),originalSky=TOWN_ENGINE.createSky(originalNoise),sky=originalSky.mesh,skyMat=originalSky.material;scene.add(sky);skyMat.uniforms.uTime=U.time;
let skyEnvironment=TOWN_ENGINE.captureEnvironment(renderer,originalSky);scene.environment=skyEnvironment.texture;scene.environmentIntensity=2;
''' +s[b:]
s=s.replace("const earthMat=worldMat(0xd7d3bc,earthTex,.08,.98)","const earthMat=REALISM.material('brown_mud_dry',{color:0xa9a68f,scale:.24,normal:.8,wetness:.4})")
s=s.replace('async function buildTown(){const start=performance.now();','async function buildTown(){await REALISM.ready;const start=performance.now();')
# No human, farmer, vendor or animal meshes in this architecture-focused build.
s=s.replace('setupPeople();setupAnimals();setupMap();',"window.__town.population={total:0,active:0,moving:0,motionSample:[]};setupMap();")
boatman="part(cylGeo,M.darkWood,-.5,1.12,4.4,.2,.65,.22);part(sphereGeo,mat(0xb79576,.9),-.5,1.64,4.4,.13,.17,.13);part(new T.ConeGeometry(.3,.15,12),marketMats.bamboo,-.5,1.86,4.4);part(boxGeo,M.darkWood,-.7,1.2,4.6,.08,.1,.5,0,.65);"
assert boatman in s;s=s.replace(boatman,'')
s=s.replace("carts.push({g,x,z,wheels,moving});", "carts.push({g,x,z,wheels,moving:false});collision(x,z,1.5,4.8,0,1.6);")
s=s.replace("check('有动态行人、商贩及搬运者',people.some(p=>p.role==='vendor')&&people.some(p=>p.role==='porter'));", "check('人物和牲畜渲染已关闭',people.length===0&&animals.length===0&&Object.keys(peopleMeshes).length===0);")
a=s.index("const p=people.find(p=>p.route==='bank'&&p.role==='walker'),z=p.z;");b=s.index('}finally{',a)
s=s[:a]+"check('六组真实 PBR 材质已加载',Object.keys(REALISM.sets).length===6);check('原版后处理已启用',!!originalPost&&originalPost.materials.length>10);check('建筑屋顶无相互穿插',auditPlacement().length===0,auditPlacement().length);"+s[b:]
# Original HDR, AO, volumetric lighting, exposure, bloom, AgX/filmic grading and FXAA chain.
a=s.index('const postRT=');b=s.index('\nlet audioCtx',a)
s=s[:a]+'''const postContext={quality:TOWN_ENGINE.quality('high'),params:{},level:{interiorBoxes:[]}},originalPost=TOWN_ENGINE.createPost(renderer,postContext,{noiseTex:originalNoise});
const originalTuning={...originalPost.TUNE};const postRT=new T.WebGLRenderTarget(innerWidth,innerHeight,{type:T.HalfFloatType,samples:4});postRT.depthTexture=new T.DepthTexture(innerWidth,innerHeight);postRT.depthTexture.type=T.UnsignedIntType;postRT.depthTexture.minFilter=postRT.depthTexture.magFilter=T.NearestFilter;
const postState={damage:0,lowHealth:0,ads:0,flash:0,fade:0,saturation:1,wet:.38};let sceneCalls=0,sceneTriangles=0;
function resizePost(){const size=renderer.getDrawingBufferSize(new T.Vector2());postRT.setSize(size.x,size.y);originalPost.resize(size.x,size.y);}resizePost();
function renderFinal(){renderer.toneMapping=T.NoToneMapping;renderer.setRenderTarget(postRT);renderer.clear();renderer.render(scene,camera);sceneCalls=renderer.info.render.calls;sceneTriangles=renderer.info.render.triangles;originalPost.run({hdr:postRT,camera,sun,dt:1/Math.max(15,fps),post:postState,exposure:renderer.toneMappingExposure,time:t,fast:false,thunder:0});renderer.setRenderTarget(null);}
''' +s[b:]
s=s.replace('sky.position.copy(camera.position);','')
s=s.replace('if(worldDt>0&&frame%12===0&&quality!==\'low\')renderer.shadowMap.needsUpdate=true;',"if(frame%10===0)updateRoofDetails();")
s=s.replace('far:550','far:800').replace('sun.position.set(focus.x-120,210,focus.z+90);',"sun.position.copy(new V(focus.x,0,focus.z).addScaledVector(TOWN_ENGINE.lightSettings.dir,400));")
a=s.index('function setMood(v)');b=s.index('\nfunction showMap',a)
s=s[:a]+'''function setMood(v){mood=v;const u=skyMat.uniforms,base=TOWN_ENGINE.skySettings,light=TOWN_ENGINE.lightSettings;sun.color.copy(light.color);sun.intensity=v==='night'?.12:v==='dusk'?6:9;hemi.intensity=0;renderer.toneMappingExposure=1;scene.environmentIntensity=v==='night'?.16:2;
 u.uZen.value.copy(base.zenith);u.uHor.value.copy(base.horizon);u.uHorAway.value.copy(base.horizonAway);u.uSunCol.value.copy(light.color);
 if(v==='night'){u.uZen.value.setRGB(.008,.014,.026);u.uHor.value.setRGB(.026,.038,.055);u.uHorAway.value.setRGB(.012,.023,.04);u.uSunCol.value.setRGB(.04,.06,.09);originalPost.TUNE.volAmbient=.035;originalPost.TUNE.flare=0;}else{originalPost.TUNE.volAmbient=originalTuning.volAmbient;originalPost.TUNE.flare=originalTuning.flare;}
 for(const m of originalPost.materials){for(const k of ['uZen','uHor','uHorAway','uSunCol'])if(m.uniforms[k])m.uniforms[k].value.copy(u[k].value);}
 skyEnvironment.dispose();skyEnvironment=TOWN_ENGINE.captureEnvironment(renderer,originalSky);scene.environment=skyEnvironment.texture;
 M.glass.emissiveIntensity=v==='night'?.55:.015;M.lantern.emissiveIntensity=v==='night'?1.1:.025;if(waterMat)waterMat.uniforms.uLight.value=v==='night'?.18:1;
 $('weather-label').textContent={morning:'雨霁 · 原版光影',dusk:'斜阳 · 暮景',night:'灯火 · 夜景'}[v];shadowUpdate();}
''' +s[b:]
s=s.replace("quality=e.target.value;renderer.setPixelRatio", "quality=e.target.value;postContext.quality=TOWN_ENGINE.quality(quality);originalPost.applyQuality();postRT.samples=postContext.quality.msaa;postRT.dispose();sun.shadow.mapSize.set(postContext.quality.shadow,postContext.quality.shadow);if(sun.shadow.map){sun.shadow.map.dispose();sun.shadow.map=null;}renderer.setPixelRatio")
s=s.replace("renderer.shadowMap.enabled=quality!=='low'","renderer.shadowMap.enabled=true")
s=s.replace("for(const o of lodObjects)o.visible=", "for(const o of lodObjects)o.visible=!o.userData.disabled&&")
s=s.replace("${built} 栋建筑 · ${people.length} 人 · ${boats.length} 船 · ${animals.length} 牲畜", "${built} 栋建筑 · 人物已关闭 · ${boats.length} 船\\nPBR 6 组 · 近景瓦面 ${roofDetails.filter(r=>r.mesh?.visible).length} · 原版 HDR / AO / 体积光")
p.write_text(s,encoding='utf-8')
h=root/'index.html';html=h.read_text(encoding='utf-8');html=html.replace('<script src="scene.js">','<script src="assets/pbr-data.js"></script><script src="real-materials.js"></script><script src="scene.js">');html=html.replace('春和日景','原版光影 · 雨霁').replace('精致</option>','写实 · 原版高画质</option>');h.write_text(html,encoding='utf-8')
print('Original lighting pipeline and photographic materials installed. Geometry integration follows.')
