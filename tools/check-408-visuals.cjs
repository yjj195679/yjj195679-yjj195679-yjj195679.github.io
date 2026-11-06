const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const {parseHTML}=require('linkedom');const root=require('node:path').resolve(__dirname,'..')+'/';
const {window,document}=parseHTML(fs.readFileSync(root+'408-handbook.html','utf8'));
const selects=new WeakMap();Object.defineProperty(window.HTMLSelectElement.prototype,'value',{configurable:true,get(){return selects.get(this)||this.querySelector('option')?.value||''},set(v){selects.set(this,String(v))}});
const timers=new Map();let token=0;const context={document,window,CustomEvent:window.CustomEvent,setTimeout:fn=>{timers.set(++token,fn);return token;},clearTimeout:id=>timers.delete(id)};
vm.runInNewContext(fs.readFileSync(root+'js/408-visuals.js','utf8'),context);
vm.runInNewContext(fs.readFileSync(root+'js/408-simulations.js','utf8'),context);
const roots=[...document.querySelectorAll('.study-sim')];assert.equal(roots.length,52);
let boards=0;
for(const r of roots){
 const data=JSON.parse(r.querySelector('.sim-data').textContent),card=r.closest('.handbook408-card');card.open=true;card.dispatchEvent(new window.Event('toggle'));
 const buttons=[...r.querySelectorAll('.sim-buttons button')];assert.equal(buttons.length,4,data.title);
 const [prev,next,play,reset]=buttons;const click=b=>b.dispatchEvent(new window.Event('click'));
 assert(prev.disabled,data.title);assert(!next.disabled,data.title);
 for(let i=1;i<data.steps.length;i++)click(next);
 assert(next.disabled,data.title);assert(r.querySelector('.sim-count').textContent.includes(`${data.steps.length} / ${data.steps.length}`));
 assert.equal(r.querySelector('.sim-heading').textContent,data.steps.at(-1).title);
 click(prev);assert.equal(r.querySelector('.sim-heading').textContent,data.steps.at(-2).title);click(next);
 if(data.scene==='board'){
  boards++;
  for(const n of data.steps.at(-1).nodes)if(n.w>4)assert(r.querySelector('svg').textContent.includes(n.label.split('\n')[0]),data.title+': '+n.label);
  const range=r.querySelector('input[type=range]');range.value='1';range.dispatchEvent(new window.Event('input'));assert.equal(r.querySelector('.sim-heading').textContent,data.steps[1].title);
 }
 click(reset);assert(prev.disabled);click(play);
 while(timers.size){const [id,fn]=timers.entries().next().value;timers.delete(id);fn();}
 assert(next.disabled);assert.equal(play.textContent,'自动演示');click(reset);click(play);assert.equal(play.textContent,'暂停演示');
 card.open=false;card.dispatchEvent(new window.Event('toggle'));assert.equal(play.textContent,'自动演示');assert.equal(timers.size,0,'closing card must cancel timer');
}
assert.equal(boards,40);
// Starting another player must pause the first, including across old/new engines.
const a=roots.find(r=>JSON.parse(r.querySelector('.sim-data').textContent).scene==='board'),b=roots.find(r=>JSON.parse(r.querySelector('.sim-data').textContent).scene!=='board');
for(const r of [a,b]){const c=r.closest('.handbook408-card');c.open=true;c.dispatchEvent(new window.Event('toggle'));r.querySelectorAll('.sim-buttons button')[2].dispatchEvent(new window.Event('click'));}
assert.equal(a.querySelectorAll('.sim-buttons button')[2].textContent,'自动演示');
document.getElementById('handbook408-search').dispatchEvent(new window.Event('input',{bubbles:true}));assert.equal(timers.size,0,'filtering must stop hidden scenes');
console.log('PASS: 52 animations forward/back/reset, last frames, 40 seek sliders, pause on close/filter, one player across both engines.');
