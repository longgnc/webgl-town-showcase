/* Runtime PBR atlas generation. No image downloads. Texture channels are independent. */
window.TownSurface = function(T, renderer) {
  const size=1024;
  const hash=(x,y)=>{let a=Math.imul(x,374761393)^Math.imul(y,668265263);a=Math.imul(a^(a>>>13),1274126177);return ((a^(a>>>16))>>>0)/4294967295;};
  const smooth=t=>t*t*(3-2*t),mix=(a,b,t)=>a+(b-a)*t;
  function noise(x,y,period=256){let a=Math.floor(x),b=Math.floor(y),u=smooth(x-a),v=smooth(y-b);const h=(i,j)=>hash((i%period+period)%period,(j%period+period)%period);return mix(mix(h(a,b),h(a+1,b),u),mix(h(a,b+1),h(a+1,b+1),u),v);}
  function make(kind){
    const count=size*size,alb=new Uint8Array(count*4),orm=new Uint8Array(count*4),heights=new Float32Array(count),norm=new Uint8Array(count*4);
    for(let y=0;y<size;y++)for(let x=0;x<size;x++){
      const i=y*size+x,k=i*4,u=x/size,v=y/size;
      const n=noise(u*16,v*16,16),mid=noise(u*64,v*64,64),fine=hash(x,y),micro=noise(u*256,v*256,256);
      let base,h,r,ao,tint;
      if(kind==='stone'){
        const row=Math.floor(v*12),fy=(v*12)%1,cols=[5,6,7,5,7,6,6,5,7,6,5,6][row],offset=hash(row,71)*.8,gx=u*cols+offset,col=Math.floor(gx),fx=gx-col;
        const id=hash(col%cols,row),chip=(noise(u*180,v*180,180)-.5)*.012;
        const edge=Math.min(fx,1-fx,fy*.5,(1-fy)*.5)+chip;
        const bevel=smooth(Math.max(0,Math.min(1,(edge-.0035)/.014)));
        const vein=Math.pow(Math.max(0,1-Math.abs(Math.sin(u*88+v*60+n*12))*8),3);
        const dry=113+(id-.5)*26+(n-.5)*26+(mid-.5)*15+(fine-.5)*13;
        base=mix(48+mid*13,dry,bevel);h=bevel*(.68+(id-.5)*.12+(n-.5)*.1+(mid-.5)*.055)+(micro-.5)*.028-vein*.025*bevel;
        r=mix(.94,.69+mid*.17,bevel);ao=mix(.52,1,bevel);tint=[1.025,1.015,.99];
      }else{
        base=77+(n-.5)*24+(mid-.5)*17+(fine-.5)*18;h=.5+(mid-.5)*.15+(micro-.5)*.05;r=.78+mid*.15;ao=.94;tint=[.96,1.015,1.035];
      }
      heights[i]=h;for(let c=0;c<3;c++)alb[k+c]=Math.max(0,Math.min(255,base*tint[c]));alb[k+3]=255;
      orm[k]=ao*255;orm[k+1]=r*255;orm[k+2]=0;orm[k+3]=255;
    }
    const strength=kind==='stone'?size/4.8*.016:size/1.2*.004;
    for(let y=0;y<size;y++)for(let x=0;x<size;x++){
      const i=(y*size+x)*4,dx=(heights[y*size+(x+1)%size]-heights[y*size+(x+size-1)%size])*strength,dy=(heights[((y+1)%size)*size+x]-heights[((y+size-1)%size)*size+x])*strength,l=Math.hypot(dx,dy,1);
      norm[i]=(-dx/l*.5+.5)*255;norm[i+1]=(-dy/l*.5+.5)*255;norm[i+2]=(1/l*.5+.5)*255;norm[i+3]=255;
    }
    function tex(data,color){const t=new T.DataTexture(data,size,size,T.RGBAFormat);t.wrapS=t.wrapT=T.RepeatWrapping;t.magFilter=T.LinearFilter;t.minFilter=T.LinearMipmapLinearFilter;t.generateMipmaps=true;t.anisotropy=Math.min(12,renderer.capabilities.getMaxAnisotropy());t.colorSpace=color?T.SRGBColorSpace:T.NoColorSpace;t.needsUpdate=true;return t;}
    const map=tex(alb,true),normalMap=tex(norm,false),roughnessMap=tex(orm,false);return {map,normalMap,roughnessMap,aoMap:roughnessMap,metalnessMap:roughnessMap};
  }
  return {make};
};
