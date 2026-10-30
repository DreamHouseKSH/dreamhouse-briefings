const fs=require('fs'),vm=require('vm'),assert=require('assert');
const source=fs.readFileSync(require('path').join(__dirname,'../assets/js/daily-audio.js'),'utf8');
const saved=new Map();
function setup(date,missing=false,reject=false){
 const events={},calls=[],cues=[{slide:0,step:1,start:0,end:1},{slide:1,step:1,start:1,end:2}];
 const audio={currentTime:0,duration:2,readyState:1,paused:true,muted:false,seeking:false,ended:false,
 addEventListener:(e,f)=>events[e]=f,pause(){this.paused=true;events.pause?.()},play(){if(reject)return Promise.reject({name:'NotAllowedError'});this.paused=false;events.playing?.();return Promise.resolve()}};
 const context={window:{},document:{hidden:false,querySelector:()=>({dataset:{date}}),getElementById:id=>id==='day-audio'?(missing?null:audio):{textContent:JSON.stringify(missing?[]:cues)}},location:{pathname:'/daily/'+date+'.html'},sessionStorage:{getItem:k=>saved.get(k),setItem:(k,v)=>saved.set(k,v)},setTimeout:f=>f()};
 vm.runInNewContext(source,context);const api=context.window.createDailyAudio({change(){},state:x=>calls.push(x),position:(s,p)=>calls.push([s,p]),complete:()=>calls.push('complete')});
 return{audio,api,events,calls};
}
(async()=>{let x=setup('2026-10-28');x.api.start(1);assert.equal(x.api.state,'playing');x.audio.currentTime=1.1;x.events.timeupdate();assert(x.calls.some(c=>Array.isArray(c)&&c[0]===1));x.api.pause();assert.equal(x.api.state,'paused');assert(saved.has('dh-day-audio-20261028'));let y=setup('2026-10-29');assert.equal(y.audio.currentTime,0);x.audio.ended=true;x.events.ended();assert.equal(x.api.state,'ended');assert(x.calls.includes('complete'));let z=setup('2026-10-30',true);assert(!z.api.available);z.api.start();assert.equal(z.api.state,'error');let denied=setup('2026-10-30',false,true);denied.api.start(1);await Promise.resolve();assert.equal(denied.api.state,'error');assert.equal(denied.calls.at(-1),false);console.log('PASS: media mocks, automatic cue boundary, pause/end, date isolation, missing/rejected audio');})();
