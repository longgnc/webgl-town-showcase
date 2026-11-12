from pathlib import Path
root=Path(__file__).resolve().parents[1];p=root/'scene.js';s=p.read_text(encoding='utf-8')
s=s.replace('0,1.3);\n const vendor=', '0,.9);\n const vendor=')
s=s.replace('collision(q[0],q[1],.85,.85,0,1.5)','collision(q[0],q[1],.85,.85,0,1.29)')
# Hanging banners, tilted cloth and tea furniture become explicit physical obstacles.
s=s.replace("function verticalSign(text,x,y,z,rot){", "function verticalSign(text,x,y,z,rot){collision(x,z,Math.abs(Math.cos(rot))*.62+.04,Math.abs(Math.sin(rot))*.62+.04,y-1.05,2.1);")
s=s.replace("cloth.rotation.x=-.45;cloth.rotation.y=rot;", "cloth.rotation.x=-.45;cloth.rotation.y=rot;collision(p[0],p[1],Math.abs(Math.cos(rot))*2.3+Math.abs(Math.sin(rot))*.83,Math.abs(Math.sin(rot))*2.3+Math.abs(Math.cos(rot))*.83,2.04,1.72);")
s=s.replace('batch(cylGeo,M.darkWood,q[0],.37,q[1],.08,.75,.08);for(let a', 'batch(cylGeo,M.darkWood,q[0],.37,q[1],.08,.75,.08);collision(q[0],q[1],1.2,1.2,0,.8);for(let a')
s=s.replace('box(M.darkWood,p[0],.3,p[1],.45,.6,.45,rot);}', 'box(M.darkWood,p[0],.3,p[1],.45,.6,.45,rot);collision(p[0],p[1],.45,.45,0,.6);}')
s=s.replace('collision(x,z,2.6,1.3);}', 'collision(x,z,2.6,1.3,0,.96);collision(x,z,3.3,2,2.68,.05);for(let a of [-1,1])for(let b of [-1,1])collision(x+a*1.15,z+b*.55,.08,.08,0,2.7);}')
s=s.replace('stall(x,27);canopy(x,27,3.5,2.5,[0xa08a63,0x7f8c7b,0x9a6b50][i%3]);', 'stall(x,27);')
s=s.replace('box(M.wood,x,.0,z,8,.25,10);', 'box(M.wood,x,.0,z,8,.25,10);collision(x,z,8,10,-.125,.25);')
# Top contact is evaluated independently of lateral blocking; small curbs are stepable.
s=s.replace('player.pos.y<b.y+b.h&&player.pos.y+1.7>b.y', 'player.pos.y+.18<b.y+b.h&&player.pos.y+(input.crouch?1.15:1.8)>b.y')
old="const y=floorAt(player.pos.x,player.pos.z);if(input.pressed('jump')&&player.grounded){player.vy=6.4;player.grounded=false;}player.vy-=21*dt;player.pos.y+=player.vy*dt;if(player.pos.y<=y+.16&&player.vy<=0)"
new="""let y=floorAt(player.pos.x,player.pos.z);if(input.pressed('jump')&&player.grounded){player.vy=6.4;player.grounded=false;}const beforeY=player.pos.y,height=input.crouch?1.15:1.8;player.vy-=21*dt;let nextY=beforeY+player.vy*dt;for(const b of colliders){if(Math.abs(player.pos.x-b.x)>b.w+.12||Math.abs(player.pos.z-b.z)>b.d+.12)continue;const top=b.y+b.h;if(player.vy<=0&&beforeY>=top-.18&&nextY<=top)y=Math.max(y,top);if(player.vy>0&&beforeY+height<=b.y+.015&&nextY+height>=b.y){nextY=b.y-height-.008;player.vy=0;}}player.pos.y=nextY;if(player.pos.y<=y+.04&&player.vy<=0)"""
assert old in s;s=s.replace(old,new)
needle="check('货车实体阻挡',!canMove(cart.x,cart.z));"
extra="""const fixtureCount=colliders.length;try{collision(260,-330,3,3,0,.9);player.pos.set(260,1.7,-330);player.vy=0;input.move.x=input.move.y=0;for(let i=0;i<90;i++)walk(1/60);check('落在货台表面而非穿透',Math.abs(player.pos.y-.9)<.015,player.pos.y);colliders.length=fixtureCount;collision(260,-330,3,3,2.35,.1);player.pos.set(260,0,-330);player.vy=6.4;player.grounded=false;let maxY=0;for(let i=0;i<90;i++){walk(1/60);maxY=Math.max(maxY,player.pos.y);}check('起跳时头部不穿透棚布',maxY+1.8<=2.35+.01,maxY+1.8);}finally{colliders.length=fixtureCount;}"""
assert needle in s;s=s.replace(needle,needle+extra)
p.write_text(s,encoding='utf-8');print('Vertical contacts, low clearance and prop collision implemented.')
