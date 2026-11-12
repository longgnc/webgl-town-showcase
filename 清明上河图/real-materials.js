/* Photographic PBR maps with physical UV scale, grain direction, dampness and microdetail. */
(() => {
'use strict';
const T=TOWN_ENGINE.THREE,sets={},loading=[],loader=new T.TextureLoader();
for(const [id,maps] of Object.entries(PBR_DATA)){sets[id]={};for(const [channel,uri] of Object.entries(maps)){let resolve,reject;const promise=new Promise((r,j)=>{resolve=r;reject=j;});const tex=loader.load(uri,()=>resolve(),undefined,reject);tex.wrapS=tex.wrapT=T.RepeatWrapping;tex.anisotropy=16;tex.colorSpace=channel==='diff'?T.SRGBColorSpace:T.NoColorSpace;sets[id][channel]=tex;loading.push(promise);}}
const wet={value:.38};
const header=`varying vec3 vRealP,vRealN,vMetricP,vRealSize,vLocalN;varying vec2 vRealUV;uniform float uRealScale,uDamp;vec2 realUV;float realWet;
float rHash(vec2 p){return fract(sin(dot(p,vec2(127.1,311.7)))*43758.5453);}
float rNoise(vec2 p){vec2 i=floor(p),f=fract(p);f=f*f*(3.-2.*f);return mix(mix(rHash(i),rHash(i+vec2(1,0)),f.x),mix(rHash(i+vec2(0,1)),rHash(i+1.),f.x),f.y);}`;
function material(id,{color=0xffffff,scale=.4,rough=1,normal=.8,timber=false,wetness=.3,vertexColors=false,riverCut=false,standardUV=false}={}){
 const maps=sets[id];if(!maps)throw Error('Missing PBR set '+id);
 const m=new T.MeshStandardMaterial({color,map:maps.diff,normalMap:maps.nor_gl,roughnessMap:maps.rough,aoMap:maps.ao,aoMapIntensity:.6,roughness:rough,metalness:0,vertexColors});m.normalScale.set(normal,normal);m.name='PBR '+id;
 m.onBeforeCompile=s=>{s.uniforms.uRealScale={value:scale};s.uniforms.uDamp=wet;
 s.vertexShader=s.vertexShader.replace('#include <common>','#include <common>\nvarying vec3 vRealP,vRealN,vMetricP,vRealSize,vLocalN;varying vec2 vRealUV;').replace('#include <begin_vertex>',`#include <begin_vertex>
 vec4 rw=vec4(position,1.);vec3 rn=normal;vec3 sz=vec3(1.);
 #ifdef USE_INSTANCING
 sz=vec3(length(instanceMatrix[0].xyz),length(instanceMatrix[1].xyz),length(instanceMatrix[2].xyz));rw=instanceMatrix*rw;rn=mat3(instanceMatrix)*rn;
 #endif
 vRealP=(modelMatrix*rw).xyz;vRealN=normalize(mat3(modelMatrix)*rn);vMetricP=position*sz;vRealSize=sz;vLocalN=normal;vRealUV=uv;`);
 s.fragmentShader=s.fragmentShader.replace('#include <common>','#include <common>\n'+header);
 let uv=standardUV?'realUV=vRealUV*uRealScale;':`vec3 bn=abs(vRealN);realUV=(bn.y>.5?vRealP.xz:(bn.x>.5?vRealP.zy:vRealP.xy))*uRealScale;`;
 if(timber)uv+=`vec3 ms=vRealSize,ln=abs(vLocalN);float along,across;bool endgrain=false;
 if(ms.y>=ms.x&&ms.y>=ms.z){along=vMetricP.y;across=ln.x>.5?vMetricP.z:vMetricP.x;endgrain=ln.y>.8;if(endgrain){along=vMetricP.x;across=vMetricP.z;}}
 else if(ms.x>=ms.z){along=vMetricP.x;across=ln.y>.5?vMetricP.z:vMetricP.y;endgrain=ln.x>.8;if(endgrain){along=vMetricP.y;across=vMetricP.z;}}
 else{along=vMetricP.z;across=ln.x>.5?vMetricP.y:vMetricP.x;endgrain=ln.z>.8;if(endgrain){along=vMetricP.x;across=vMetricP.y;}}
 realUV=vec2(along*uRealScale,across*.22+.19);if(endgrain)realUV=vec2(along,across)*.8;`;
 s.fragmentShader=s.fragmentShader.replace('#include <map_fragment>',uv+`
 ${riverCut?'if(abs(vRealP.x-(24.*sin(vRealP.z/83.)+7.*sin(vRealP.z/28.)))<18.4)discard;':''}
 vec4 texelColor=texture2D(map,realUV);diffuseColor*=texelColor;
 float macro=rNoise(vRealP.xz*.17)*.65+rNoise(vRealP.xz*.63)*.35;
 float lower=1.-smoothstep(.12,1.15,vRealP.y);float upward=smoothstep(.3,.85,abs(vRealN.y));
 realWet=clamp(uDamp*${wetness.toFixed(3)}*(.25+macro+lower*.5),0.,.85);
 diffuseColor.rgb*=mix(.84,1.08,macro)*(1.-realWet*.25);
 diffuseColor.rgb=mix(diffuseColor.rgb,diffuseColor.rgb*vec3(.71,.77,.65),lower*(1.-upward)*.3);
 `);
 s.fragmentShader=s.fragmentShader.replace('#include <normal_fragment_begin>',T.ShaderChunk.normal_fragment_begin.replaceAll('vNormalMapUv','realUV'));
 s.fragmentShader=s.fragmentShader.replace('#include <normal_fragment_maps>',T.ShaderChunk.normal_fragment_maps.replaceAll('vNormalMapUv','realUV'));
 s.fragmentShader=s.fragmentShader.replace('#include <roughnessmap_fragment>',T.ShaderChunk.roughnessmap_fragment.replaceAll('vRoughnessMapUv','realUV')+'\nroughnessFactor=clamp(roughnessFactor*(1.-realWet*.52),.23,.98);');
 s.fragmentShader=s.fragmentShader.replace('#include <aomap_fragment>',T.ShaderChunk.aomap_fragment.replaceAll('vAoMapUv','realUV'));
 };m.customProgramCacheKey=()=>`photo-v5-${id}-${scale}-${timber}-${riverCut}-${wetness}-${standardUV}`;return m;
}
const heightCache=new Map();function height(id,x,z,scale){let q=heightCache.get(id);if(!q){const tex=sets[id].disp;if(!tex?.image)return .5;const c=document.createElement('canvas');c.width=c.height=256;const g=c.getContext('2d');g.drawImage(tex.image,0,0,256,256);q=g.getImageData(0,0,256,256).data;heightCache.set(id,q);}const u=((x*scale%1)+1)%1,v=((z*scale%1)+1)%1;return q[(Math.floor((1-v)*255)*256+Math.floor(u*255))*4]/255;}
function tileGeometry(w,d,h){const pos=[],uv=[],colors=[],indices=[],cols=Math.max(1,Math.ceil(w/.265)),rows=Math.max(1,Math.ceil(d*.5/.38)),cw=w/cols,step=d*.5/rows;
 const roofY=t=>h*Math.pow(1-t,1.65)+h*.08*Math.pow(t,7),hash=(a,b)=>{const n=Math.sin(a*73.31+b*19.7)*23121.77;return n-Math.floor(n);};
 for(let side of [-1,1])for(let j=0;j<rows;j++)for(let i=0;i<cols;i++){const base=pos.length/3,shade=.77+hash(i,j)*.27;
  for(let end=0;end<2;end++){const zz=Math.min(d*.5,j*step+end*(step+.045)),t=zz/(d*.5),y=roofY(t)+.037+(end?0:.018);for(let k=0;k<=4;k++){const f=k/4,xx=-w/2+(i+f)*cw;pos.push(xx,y+Math.sin(f*Math.PI)*.047,side*zz);uv.push(xx*.45,zz*.45);colors.push(shade,shade,shade);}}
  for(let k=0;k<4;k++){let a=base+k,b=a+5;if(side>0)indices.push(a,b,a+1,a+1,b,b+1);else indices.push(a,a+1,b,a+1,b+1,b);}
  for(let k=0;k<=4;k++){const a=(base+5+k)*3;pos.push(pos[a],pos[a+1]-.018,pos[a+2]);uv.push(uv[(base+5+k)*2],uv[(base+5+k)*2+1]);colors.push(shade*.88,shade*.88,shade*.88);}
  for(let k=0;k<4;k++){const a=base+5+k,b=base+10+k;indices.push(a,a+1,b,a+1,b+1,b);}
 }
 const g=new T.BufferGeometry();g.setAttribute('position',new T.Float32BufferAttribute(pos,3));g.setAttribute('uv',new T.Float32BufferAttribute(uv,2));g.setAttribute('color',new T.Float32BufferAttribute(colors,3));g.setIndex(indices);g.computeVertexNormals();g.computeBoundingSphere();return g;
}
window.REALISM={sets,wet,material,height,tileGeometry,ready:Promise.all(loading)};
})();
