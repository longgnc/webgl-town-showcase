from pathlib import Path
root=Path(__file__).resolve().parents[1];p=root/'scene.js';s=p.read_text(encoding='utf-8')
s=s.replace('B(M.darkWood,0,h+.73,0,w+.1,.5,d+.1);','B(M.darkWood,0,h+.59,0,w-.15,.12,d-.15);')
# Gables follow the underside of the curved roof; triangular gables protruded through it.
idx=s.index('function batch(')
s=s[:idx]+'''const gableCache=new Map();function gableGeometry(d){const key=d.toFixed(2);if(gableCache.has(key))return gableCache.get(key);const pos=[0,0,0],uv=[.5,0],ix=[];for(let j=0;j<=32;j++){const z=-.5+j/32,t=Math.abs(z)*2*d/(d+2),y=Math.max(0,(1-t)**1.65+.08*t**7-.012);pos.push(0,y,z);uv.push(z+.5,y);}for(let j=0;j<32;j++)ix.push(0,j+1,j+2);const g=new T.BufferGeometry();g.setAttribute('position',new T.Float32BufferAttribute(pos,3));g.setAttribute('uv',new T.Float32BufferAttribute(uv,2));g.setIndex(ix);g.computeVertexNormals();gableCache.set(key,g);return g;}
''' +s[idx:]
s=s.replace('batch(gableGeo,gableMat','batch(gableGeometry(d),gableMat')
s=s.replace('const sign=P(-w*.26,d/2+1.1);B(M.darkWood,-w*.26,4.6,d/2+.6,.11,.11,1.4);verticalSign', 'const sign=P(-w*.26,d/2+2.2);B(M.darkWood,-w*.26,3.18,d/2+1.12,.075,.075,2.24);verticalSign')
s=s.replace('sign[0],3.55,sign[1]','sign[0],2.05,sign[1]')
a=s.index(' // Store rear yards have low walls');b=s.index("landmarks.push({name:'虹桥闹市'",a);s=s[:a]+s[b:]
s=s.replace('side*(335+Math.floor(i/3)*44)','side*(385+Math.floor(i/3)*44)')
s=s.replace('function tree(x,z,scale=1,willow=false){','const pendingTrees=[];function tree(...args){pendingTrees.push(args);}function constructTree(x,z,scale=1,willow=false){if(placementBoxes.some(b=>boxOverlaps({x,z,w:5.4*scale,d:5.4*scale,rot:0},b)))return;')
s=s.replace('renderPaving();resolveLandmarks();','renderPaving();for(const args of pendingTrees)constructTree(...args);resolveLandmarks();')
p.write_text(s,encoding='utf-8');print('Roof cap, gables, signs and vegetation clearances corrected.')
