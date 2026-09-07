import fs from 'node:fs';
import vm from 'node:vm';
import assert from 'node:assert/strict';
const source = fs.readFileSync('game.js','utf8');
const levels = JSON.parse(fs.readFileSync('NotTrollGDX/assets/levels.json','utf8')).levels;
function fn(name) {
  const start=source.indexOf(`function ${name}(`);
  const end=source.indexOf('\nfunction ',start+1);
  return source.slice(start,end);
}
const ctx=vm.createContext({Math, keys:{}, H:540, W:960, GRAVITY:1800,CUT_GRAVITY_MULT:2.4,FALL_GRAVITY_MULT:1.35,MOVE_ACCEL:2600,AIR_ACCEL_MULT:.85,FRICTION:2200,MAX_SPEED:220,JUMP_VELOCITY:620,MAX_FALL:900,COYOTE_TIME:.09,GROUND_LIFT:90,spawnDust(){},addShake(){},Sound:{jump(){},land(){}},player:null,level:null,platformState:[]});
for(const name of ['updatePlayer','solidPlatforms','resolveCollisions','overlap','rect','updateMovingPlatforms','cameraTargetY','levelProgress','trapReached']) vm.runInContext(fn(name),ctx);
function reset(level,x,y){
 ctx.level=level;ctx.platformState=structuredClone(level.platforms).map(p=>({...p,dir:1}));
 ctx.player={x,y,w:26,h:36,vx:0,vy:0,onGround:false,facing:1,coyote:0,jumpBuffer:0,squashX:1,squashY:1,animTime:0,rotation:0};ctx.keys={};
}
function tick(direction=0,jump=false){ctx.keys={ArrowLeft:direction<0,ArrowRight:direction>0,Space:jump};if(jump&&ctx.player.onGround)ctx.player.jumpBuffer=.12;ctx.updatePlayer(1/120);ctx.updateMovingPlatforms(1/120);}
let connections=0;
for(let n=71;n<=76;n++){
 const lv=levels[n-1],floors=lv.routeFloors;assert(lv.verticalCamera);assert(floors.length>=5);
 for(let i=0;i<floors.length-1;i++){
  const right=i%2===0,dir=right?1:-1,y=floors[i],target=floors[i+1];
  if(lv.teleporters?.some(tp=>tp.y===y-40)){connections++;continue;}
  const lift=lv.platforms.find(p=>p.type==='moving'&&p.maxY===y);
  const bounce=lv.platforms.find(p=>p.type==='bounce'&&p.y===y);
  reset(lv,right?1420:150,(lift?target:y)-36);
  if(lift) {
    const instance=ctx.platformState.find(p=>p.type==='moving'&&p.maxY===y);
    instance.y=target;instance.dir=1;
    ctx.player.onGround=true;ctx.player.groundPlatform=instance;ctx.player.groundType='moving';
  }
  let landed=false;
  for(let frame=0;frame<1200;frame++){
   const p=ctx.player;
   let move=0,jump=false;
   if(lift){move=-dir;jump=frame===0;}
   else if(bounce){move=p.y+p.h<=target-12?-dir:0;}
   tick(move,jump);
   if(p.onGround&&Math.abs(p.y+p.h-target)<3&&p.groundType!=='moving'){landed=true;break;}
   if(p.y>lv.height+200)break;
  }
  assert(landed,`Level ${n} connection ${i}: ${JSON.stringify(ctx.player)}`);connections++;
 }
 reset(lv,260,floors[0]-36);
 assert(ctx.cameraTargetY()>=0&&ctx.cameraTargetY()<=lv.height-ctx.H);
 for(const trap of [...lv.bombs,...lv.fallingBlocks]){
  ctx.player.x=trap.triggerX-1;ctx.player.y=trap.triggerY+40;assert(ctx.trapReached(trap));
  ctx.player.y=trap.triggerY-300;assert(!ctx.trapReached(trap));
 }
}
reset(levels[0],60,300);assert.equal(ctx.cameraTargetY(),0);
console.log(`PASS: ${connections} floor connections, floor-specific triggers and camera bounds. Route physics tested without hazards.`);

// Check spike clusters in the intended travel direction with the real jump physics.
let clusterCount=0;
for(let n=72;n<=76;n++){
 const lv=levels[n-1];
 for(const hazard of lv.hazards.filter(h=>h.type==='spike')){
  assert([40,60].includes(hazard.w),`Level ${n}: expected two or three spikes`);
  const floor=lv.routeFloors.indexOf(hazard.y+hazard.h),dir=floor%2?-1:1;
  let possible=false;
  for(const distance of [45,55,65,75,85,95]){
   reset(lv,dir===1?hazard.x-130:hazard.x+hazard.w+105,hazard.y+hazard.h-36);
   let launched=false,hit=false;
   for(let f=0;f<240;f++){
    const p=ctx.player;
    const approach=dir===1?hazard.x-(p.x+p.w):p.x-(hazard.x+hazard.w);
    const jump=!launched&&p.onGround&&approach<=distance;
    if(jump)launched=true;
    tick(dir,jump||launched);
    if(ctx.overlap(p,hazard)){hit=true;break;}
    if(launched&&p.onGround&&(dir===1?p.x>hazard.x+hazard.w:p.x+p.w<hazard.x)){possible=true;break;}
   }
   if(possible)break;
  }
  assert(possible,`Level ${n}: spike cluster at ${hazard.x},${hazard.y} cannot be cleared`);
  clusterCount++;
 }
}
console.log(`PASS: ${clusterCount} groups of two or three spikes can be jumped in the route direction (other traps excluded).`);
const portalTower=levels[74];
for(const gap of portalTower.platforms.filter(p=>p.type==='fake_floor')){
 const i=portalTower.routeFloors.indexOf(gap.y),dir=i%2?-1:1;
 reset(portalTower,dir===1?gap.x-90:gap.x+gap.w+65,gap.y-36);
 let launched=false,landed=false;
 for(let f=0;f<240;f++){
  const p=ctx.player,near=dir===1?gap.x-(p.x+p.w)<20:p.x-(gap.x+gap.w)<20;
  const jump=p.onGround&&!launched&&near;
  if(jump)launched=true;
  tick(dir,jump||launched);
  if(launched&&p.onGround&&Math.abs(p.y+p.h-gap.y)<2&&(dir===1?p.x>=gap.x+gap.w:p.x+p.w<=gap.x)){landed=true;break;}
 }
 assert(landed,`Portal tower gap at ${gap.x},${gap.y} cannot be crossed`);
}
console.log('PASS: all five fake-floor gaps can be crossed in the route direction.');
const extensionBoundaries = {49:2300,50:3200,51:2400,52:1900,53:2200,54:2500,55:3100,56:2400,57:2700,58:2600,59:2400,60:3300,61:2300,62:2200,63:2800,64:2500,65:2600,66:1400};
let extensionJumps=0;
for(const [number,boundary] of Object.entries(extensionBoundaries)){
 const lv=levels[Number(number)-1],extension=lv.platforms.filter(p=>p.x>=boundary+40);
 assert(extension.length>=4&&lv.width>boundary+1200);
 const approach=lv.platforms.find(p=>p.type!=='moving'&&p.x+p.w===boundary);
 const route=[approach,...extension];assert(approach);
 for(let i=0;i<route.length-1;i++){
  const from=route[i],to=route[i+1];let possible=false;
  for(const takeoff of [30,40,50,60]){
   reset(lv,from.x+from.w-90,from.y-36);let launched=false;
   for(let f=0;f<240;f++){
    const p=ctx.player,jump=p.onGround&&!launched&&p.x>=from.x+from.w-takeoff;
    if(jump)launched=true;
    tick(1,jump||launched);
    if(launched&&p.onGround&&p.groundPlatform.x===to.x){possible=true;break;}
   }
   if(possible)break;
  }
  assert(possible,`Level ${number} extension jump ${i} cannot be crossed`);extensionJumps++;
 }
 const last=extension.at(-1);assert(lv.goal.y+lv.goal.h===last.y&&lv.goal.x>=last.x&&lv.goal.x+lv.goal.w<=last.x+last.w);
}
console.log(`PASS: ${extensionJumps} extension jumps across levels 49–66 and supported final portals (without hazards).`);
// Late-game towers: actual transition physics and retreat into each bombardment refuge.
ctx.killPlayer=()=>{ctx.player.dead=true;};ctx.spawnBurst=()=>{};ctx.Sound.boom=()=>{};ctx.flash=0;
vm.runInContext(fn('updateBombs'),ctx);
let lateConnections=0,refuges=0;
for(let n=81;n<=100;n++){
 const lv=levels[n-1],floors=lv.routeFloors;assert(floors.length>=4);
 for(let i=0;i<floors.length-1;i++){
  const right=i%2===0,dir=right?1:-1,y=floors[i],target=floors[i+1];
  const tp=lv.teleporters?.find(t=>t.y===y-40);
  if(tp){assert(lv.platforms.some(p=>p.x<=tp.toX&&p.x+p.w>=tp.toX+26&&p.y===tp.toY+60));lateConnections++;continue;}
  const lift=lv.platforms.find(p=>p.type==='moving'&&p.maxY===y),bounce=lv.platforms.find(p=>p.type==='bounce'&&p.y===y);
  reset(lv,right?lv.width-180:150,(lift?target:y)-36);
  if(lift){const p=ctx.platformState.find(p=>p.type==='moving'&&p.maxY===y);p.y=target;p.dir=1;ctx.player.onGround=true;ctx.player.groundPlatform=p;ctx.player.groundType='moving';}
  let landed=false;
  for(let frame=0;frame<1200;frame++){
   const p=ctx.player;tick(lift?-dir:bounce&&p.y+p.h<=target-12?-dir:0,lift&&frame===0);
   if(p.onGround&&Math.abs(p.y+p.h-target)<3&&p.groundType!=='moving'){landed=true;break;}
   if(p.y>lv.height+200)break;
  }
  assert(landed,`Level ${n}: transition ${i} failed`);lateConnections++;
 }
 for(const shelter of lv.platforms.filter(p=>p.shelter)){
  const y=shelter.y+95,center=shelter.x+shelter.w/2;
  const barrage=lv.bombs.filter(b=>b.kind==='sky'&&b.groundY===y);
  assert(barrage.length>=8);const trigger=barrage[0],dir=trigger.triggerDir;
  for(const retreat of [true,false]){
   reset(lv,trigger.triggerX+(dir===1?-25:-1),y-36);ctx.player.vx=dir*220;
   ctx.bombs=barrage.map(b=>({...b,curY:b.y,vy:0,t:0,state:'idle',gone:false}));
   for(let f=0;f<720&&!ctx.player.dead&&ctx.bombs.some(b=>!b.gone);f++){
    ctx.updateBombs(1/120);
    if(retreat){const desired=Math.max(-220,Math.min(220,(center-13-ctx.player.x)*6));tick(Math.abs(desired-ctx.player.vx)>15?Math.sign(desired-ctx.player.vx):0);}
    else tick(dir);
   }
   assert(retreat?!ctx.player.dead:ctx.player.dead,`Level ${n} refuge ${y}: ${retreat?'retreat must survive':'running forward must be threatened'}`);
  }
  refuges++;
 }
}
console.log(`PASS: ${lateConnections} late-game floor connections and ${refuges} bombardments where retreat to shelter survives.`);
vm.runInContext(fn('updateFallingBlocks'),ctx);
const missileLevel=levels.slice(80).find(l=>l.bombs.some(b=>b.missile));
const missile=missileLevel.bombs.find(b=>b.missile);
reset(missileLevel,missile.fromX-13,missile.y-18);
ctx.bombs=[{...missile,state:'active',curX:missile.fromX,gone:false}];ctx.updateBombs(1/120);
assert(ctx.player.dead,'Missile body contact must kill');
reset(missileLevel,missile.fromX-13,missile.y-90);
ctx.bombs=[{...missile,state:'active',curX:missile.fromX,gone:false}];ctx.updateBombs(1/120);
assert(!ctx.player.dead,'A jump above a missile must be safe');
const spikeLevel=levels.slice(80).find(l=>l.fallingBlocks.some(b=>b.ceilingSpikes)),spike=spikeLevel.fallingBlocks.find(b=>b.ceilingSpikes);
reset(spikeLevel,spike.x+5,spike.groundY-36);
ctx.fallingBlocks=[{...spike,state:'landed',curY:spike.groundY-spike.h,t:0,gone:false}];ctx.updateFallingBlocks(1/120);
assert(ctx.player.dead,'Landed ceiling spikes must remain dangerous until disappearing');
console.log('PASS: missile contact, jumping over missiles and landed ceiling-spike contact.');
