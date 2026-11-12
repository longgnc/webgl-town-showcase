function setupWater(){reflRT=new T.WebGLRenderTarget(1024,576,{type:T.HalfFloatType});reflCam=camera.clone();waterMat=new T.ShaderMaterial({uniforms:{uTime:U.time,uWind:U.wind,tReflection:{value:reflRT.texture},textureMatrix:{value:textureMatrix},uColor:{value:new T.Color(0x34483d)},uEye:{value:camera.position},uLight:{value:1},uSun:{value:TOWN_ENGINE.lightSettings.dir.clone()}},vertexShader:`uniform mat4 textureMatrix;varying vec4 vMirror;varying vec3 vWorld;void main(){vec4 w=modelMatrix*vec4(position,1.);vWorld=w.xyz;vMirror=textureMatrix*w;gl_Position=projectionMatrix*viewMatrix*w;}`,fragmentShader:`uniform sampler2D tReflection;uniform float uTime,uWind,uLight;uniform vec3 uColor,uEye,uSun;varying vec4 vMirror;varying vec3 vWorld;
void main(){vec2 p=vWorld.xz,flow=p+vec2(uTime*.06,-uTime*.14);vec2 slope=vec2(0.);
for(int i=0;i<6;i++){float k=float(i),angle=k*2.399+.42;vec2 dir=vec2(cos(angle),sin(angle));float f=1.2+pow(1.58,k);float phase=dot(flow,dir)*f+uTime*(.7+k*.19);slope+=dir*cos(phase)*(.019/(1.+k*.38));}slope*=.6+uWind*.8;
vec3 normal=normalize(vec3(-slope.x,1.,-slope.y)),view=normalize(uEye-vWorld);float ndv=max(.0,dot(normal,view));float fresnel=.0204+.9796*pow(1.-ndv,5.);
vec2 uv=vMirror.xy/vMirror.w+slope*.035;vec2 texel=vec2(1./1024.,1./576.);vec3 reflection=texture2D(tReflection,clamp(uv,.002,.998)).rgb*.5;reflection+=(texture2D(tReflection,clamp(uv+texel,.002,.998)).rgb+texture2D(tReflection,clamp(uv-texel,.002,.998)).rgb)*.25;
float center=24.*sin(p.y/83.)+7.*sin(p.y/28.);float bank=1.-smoothstep(13.5,18.,abs(p.x-center));vec3 depthColor=mix(uColor*1.3,uColor*.65,bank)*uLight;vec3 color=mix(depthColor,reflection,clamp(fresnel+.10,.10,.94));
vec3 halfVector=normalize(view+uSun);float sunSpec=pow(max(0.,dot(normal,halfVector)),220.);color+=vec3(1.,.72,.42)*sunSpec*.8*uLight;
gl_FragColor=vec4(color,1.);
#include <tonemapping_fragment>
#include <colorspace_fragment>
}`});water=mesh(riverSurface(-18,18),waterMat,0,-.9,0);water.castShadow=water.receiveShadow=false;}
