from pathlib import Path
p=Path(__file__).with_name('scene.js');s=p.read_text(encoding='utf-8')
a="check('人物时间推进产生位移',Math.abs(p.z-z)>.1,Math.abs(p.z-z));"
b=a+"for(const route of ['bank','cross','field']){const actor=people.find(p=>p.route===route&&p.role!=='onlooker'),saved={...actor};actor.direction=1;if(route==='cross')actor.x=actor.hi+.1;else actor.z=(route==='bank'?305:actor.zmax)+.1;updatePeople(.1,t);check('人物边界折返 '+route,actor.direction===-1&&(route==='cross'?actor.x<=actor.hi:actor.z<=(route==='bank'?305:actor.zmax)));Object.assign(actor,saved);}"
assert a in s
s=s.replace(a,b);p.write_text(s,encoding='utf-8')
