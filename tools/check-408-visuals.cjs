const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const {parseHTML}=require('linkedom');const root=require('node:path').resolve(__dirname,'..')+'/';
const {window,document}=parseHTML(fs.readFileSync(root+'408-handbook.html','utf8'));
const selects=new WeakMap();Object.defineProperty(window.HTMLSelectElement.prototype,'value',{configurable:true,get(){return selects.get(this)||this.querySelector('option')?.value||''},set(v){selects.set(this,String(v))}});
const timers=new Map();let token=0;const context={document,window,CustomEvent:window.CustomEvent,setTimeout:fn=>{timers.set(++token,fn);return token;},clearTimeout:id=>timers.delete(id)};
vm.runInNewContext(fs.readFileSync(root+'js/408-visuals.js','utf8'),context);
vm.runInNewContext(fs.readFileSync(root+'js/408-simulations.js','utf8'),context);
const expected=JSON.parse(fs.readFileSync(root+'data/408-handbook.json','utf8')).flatMap(c=>c.sections.filter(s=>s.simulation).map(s=>s.simulation));
const roots=[...document.querySelectorAll('.study-sim')];assert.equal(roots.length,expected.length);
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
  const wires=data.steps.at(-1).wires||[];
  for(const wire of wires){assert([...r.querySelectorAll('.board-wire')].some(p=>p.style.opacity==='1' && p.getAttribute('d')===wire.points.map(([x,y],i)=>(i?'L':'M')+x+','+y).join(' ')),data.title+': missing waveform');}
  if(data.steps.at(-1).edges.length && data.steps.at(-1).edges.every(e=>e.directed===false))assert([...r.querySelectorAll('.board-edge')].filter(p=>p.style.opacity==='1').every(p=>!p.getAttribute('marker-end')),data.title+': undirected edges must have no arrowheads');
  for(const n of data.steps.at(-1).nodes)if(n.w>4)assert(r.querySelector('svg').textContent.includes(n.label.split('\n')[0]),data.title+': '+n.label);
  const range=r.querySelector('input[type=range]');range.value='1';range.dispatchEvent(new window.Event('input'));assert.equal(r.querySelector('.sim-heading').textContent,data.steps[1].title);
 }
 click(reset);assert(prev.disabled);click(play);
 while(timers.size){const [id,fn]=timers.entries().next().value;timers.delete(id);fn();}
 assert(next.disabled);assert.equal(play.textContent,'自动演示');click(reset);click(play);assert.equal(play.textContent,'暂停演示');
 card.open=false;card.dispatchEvent(new window.Event('toggle'));assert.equal(play.textContent,'自动演示');assert.equal(timers.size,0,'closing card must cancel timer');
}
assert.equal(boards,expected.filter(s=>s.scene==='board').length);
// Starting another player must pause the first, including across old/new engines.
const a=roots.find(r=>JSON.parse(r.querySelector('.sim-data').textContent).scene==='board'),b=roots.find(r=>JSON.parse(r.querySelector('.sim-data').textContent).scene!=='board');
for(const r of [a,b]){const c=r.closest('.handbook408-card');c.open=true;c.dispatchEvent(new window.Event('toggle'));r.querySelectorAll('.sim-buttons button')[2].dispatchEvent(new window.Event('click'));}
assert.equal(a.querySelectorAll('.sim-buttons button')[2].textContent,'自动演示');
document.getElementById('handbook408-search').dispatchEvent(new window.Event('input',{bubbles:true}));assert.equal(timers.size,0,'filtering must stop hidden scenes');
console.log(`PASS: ${roots.length} animations forward/back/reset, last frames, ${boards} seek sliders, pause on close/filter, one player across both engines.`);
