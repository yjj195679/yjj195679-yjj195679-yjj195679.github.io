const fs=require('fs'),vm=require('vm'),assert=require('node:assert/strict');
const {parseHTML}=require('linkedom');
const root=require('node:path').resolve(__dirname,'..')+'/';const core=require(root+'js/408.js');
const all=JSON.parse(fs.readFileSync(root+'data/408-knowledge.json','utf8'));
assert.equal(all.items.length,211); assert.equal(all.calculations.length,8);
const values=all.items.map(x=>({...x,search:Object.values(x).join(' ')}));
assert.equal(values.filter(x=>core.matches(x,{},{}   )).length,211);
assert.equal(values.filter(x=>core.matches(x,{subject:'操作系统'},{} )).length,52);
assert.equal(values.filter(x=>core.matches(x,{tag:'个人错题'},{})).length,21);
assert.equal(values.filter(x=>core.matches(x,{tag:'近年考查'},{})).length,46);
assert.equal(values.filter(x=>core.matches(x,{query:'不存在的关键词'},{})).length,0);
assert(values.some(x=>core.matches(x,{query:'cache 组号'},{})));
assert(core.matches(values.find(x=>x.title.startsWith('Cache：')),{query:'ＣＡＣＨＥ'},{}));
assert.equal(Object.keys(core.parseMarks('{bad')).length,0);
assert.equal(Object.keys(core.parseMarks('[]')).length,0);
const loaded=core.parseMarks('{"k001":"review","c001":"mastered","k080":"review","k212":"review","__proto__":"review","k002":"broken"}');
assert.deepEqual(Object.keys(loaded),['k001','c001','k080']);
core.toggleMark(loaded,'k001','mastered');assert.equal(loaded.k001,'mastered');
core.toggleMark(loaded,'k001','mastered');assert(!loaded.k001);
const store=new Map(); const storage={getItem:k=>store.get(k)||null,setItem:(k,v)=>store.set(k,v)};
function persisted() {
 const result=core.parseMarks(store.get('true-path-408-marks-v1')||null);
 for (const [key,value] of store.entries()) {
  if(!key.startsWith('true-path-408-mark-v2-')) continue;
  const id=key.slice('true-path-408-mark-v2-'.length);
  if(value==='review'||value==='mastered')result[id]=value;else delete result[id];
 }
 return result;
}
const code=fs.readFileSync(root+'js/408.js','utf8');
function runPage(name,blocked=false,hash='') {
 const {window,document}=parseHTML(fs.readFileSync(root+name,'utf8'));
 const selectValues=new WeakMap();
 // LinkeDOM's select.value is read-only; emulate browser setter for application integration tests.
 Object.defineProperty(window.HTMLSelectElement.prototype,'value',{configurable:true,get(){return selectValues.get(this)??this.querySelector('option')?.value??'';},set(v){selectValues.set(this,String(v));}});
 window.HTMLElement.prototype.scrollIntoView=function(){this.scrolled=true;};
 window.HTMLElement.prototype.focus=function(){document.lastFocused=this;};
 const local=blocked?{getItem(){throw Error('blocked')},setItem(){throw Error('blocked')}}:storage;
 const loc={hash,origin:'https://1956799.xyz',pathname:'/'+name,href:'https://1956799.xyz/'+name+hash};
 window.location=loc;window.localStorage=local;window.sessionStorage=local;window.innerWidth=375;window.innerHeight=800;window.scrollY=0;
 window.matchMedia=()=>({matches:false,addEventListener(){}});window.requestAnimationFrame=f=>f();window.setInterval=()=>1;window.setTimeout=()=>1;window.clearTimeout=()=>{};window.scrollTo=()=>{};
 Object.defineProperties(window.HTMLAnchorElement.prototype,{hash:{configurable:true,get(){return new URL(this.getAttribute('href')||'',loc.href).hash;}},origin:{configurable:true,get(){return new URL(this.getAttribute('href')||'',loc.href).origin;}},pathname:{configurable:true,get(){return new URL(this.getAttribute('href')||'',loc.href).pathname;}}});
 const sandbox={document,window,URL,CustomEvent:window.CustomEvent,navigator:{platform:'iPad'},location:loc,localStorage:local,requestAnimationFrame:f=>f(),Option:function(text,value){const el=document.createElement('option');el.textContent=text;el.value=value;return el;}};
 vm.runInNewContext(fs.readFileSync(root+'js/main.js','utf8'),sandbox,{filename:'main.js'});
 vm.runInNewContext(code,sandbox,{filename:'408.js'});
 const get=id=>document.getElementById(id),visible=()=>[...document.querySelectorAll('.study-card')].filter(e=>!e.hidden);
 const set=(id,value)=>{get(id).value=value;get(id).dispatchEvent(new window.Event(id==='study-search'?'input':'change'));};
 const click=(sel)=>document.querySelector(sel).dispatchEvent(new window.Event('click',{bubbles:true}));
 return {window,document,get,visible,set,click};
}
let p=runPage('408.html'); assert(!p.get('study-filters').hidden);assert.equal(p.visible().length,211);
p.set('study-subject','计算机组成原理');assert.equal(p.visible().length,52);
assert(![...p.get('study-chapter').children].some(x=>x.value==='文件系统'));
p.set('study-chapter','存储系统');assert(p.visible().length>0);assert(p.visible().every(x=>x.dataset.chapter==='存储系统'));
p.set('study-tag','个人错题');assert.equal(p.visible().length,1);assert.equal(p.visible()[0].id,'k027');
p.set('study-search','Cache 组号');assert.equal(p.visible().length,1);
p.click('#k027 [data-mark="review"]');assert.equal(persisted().k027,'review');
p.set('study-state','review');assert.equal(p.visible().length,1);
p.click('#k027 [data-mark="mastered"]');assert.equal(p.visible().length,0);assert.equal(p.document.lastFocused.id,'study-state');
p.click('#study-reset');assert.equal(p.visible().length,211);assert.equal(persisted().k027,'mastered');
p.set('study-subject','数据结构');p.set('study-chapter','存储系统'); // An impossible selection is harmless and produces no cards.
assert.equal(p.visible().length,0);p.click('#study-reset');
p.set('study-search','zzzzzz');assert(!p.get('study-empty').hidden);
p.click('#study-reset');p.set('study-subject','操作系统');p.click('#study-expand');assert(p.visible().every(x=>x.open));
assert(!p.get('k001').open);p.click('#study-collapse');assert(p.visible().every(x=>!x.open));
p.window.dispatchEvent(new p.window.Event('beforeprint'));assert(p.visible().every(x=>x.open));
p.window.dispatchEvent(new p.window.Event('afterprint'));assert(p.visible().every(x=>!x.open));
let calc=runPage('408-calculations.html');assert.equal(calc.visible().length,8);
calc.click('#c001 [data-mark="review"]');assert.equal(persisted().k027,'mastered');
let reload=runPage('408.html');assert.equal(reload.get('k027').querySelector('[data-mark="mastered"]').getAttribute('aria-pressed'),'true');
assert.equal(persisted().c001,'review');
let blocked=runPage('408.html',true);blocked.click('#k001 [data-mark="review"]');assert(blocked.get('study-storage').textContent.includes('本次打开'));
let deep=runPage('408.html',false,'#k080');assert(deep.get('k080').open);assert(deep.get('k080').scrolled);
const evt=new reload.window.Event('storage');evt.key='true-path-408-marks-v1';evt.newValue='{"k002":"review"}';store.set('true-path-408-marks-v1',evt.newValue);reload.window.dispatchEvent(evt);
assert.equal(reload.get('k002').querySelector('[data-mark="review"]').getAttribute('aria-pressed'),'true');
console.log('PASS shared main.js + 408.js integration: content counts, combined filters, search, empty state, marking, persistence, blocked/corrupt storage, cross-page preservation, focus, expand/collapse, print restore, deep links, cross-tab sync.');

// Two tabs can act before either receives the other tab's storage event.
store.clear();let tabA=runPage('408.html'),tabB=runPage('408.html');
tabA.click('#k001 [data-mark="review"]');tabB.click('#k002 [data-mark="mastered"]');
const concurrent=persisted();
assert.equal(concurrent.k001,'review','An independent mark from the first tab must survive.');
assert.equal(concurrent.k002,'mastered');
console.log('PASS: concurrent independent marks survive.');

store.clear();store.set('true-path-408-marks-v1','{"k003":"review","c003":"mastered"}');
let migrated=runPage('408.html');
assert.equal(migrated.get('k003').querySelector('[data-mark="review"]').getAttribute('aria-pressed'),'true');
migrated.click('#k003 [data-mark="review"]');assert.equal(store.get('true-path-408-mark-v2-k003'),'unmarked');
let migratedReload=runPage('408.html');
assert.equal(migratedReload.get('k003').querySelector('[data-mark="review"]').getAttribute('aria-pressed'),'false');
let migratedCalc=runPage('408-calculations.html');
assert.equal(migratedCalc.get('c003').querySelector('[data-mark="mastered"]').getAttribute('aria-pressed'),'true');
store.set('true-path-408-mark-v2-k001','review');
let fresh=runPage('408.html');store.set('true-path-408-mark-v2-k001','mastered');
let staleEvent=new fresh.window.Event('storage');staleEvent.key='true-path-408-mark-v2-k001';staleEvent.newValue='review';fresh.window.dispatchEvent(staleEvent);
assert.equal(fresh.get('k001').querySelector('[data-mark="mastered"]').getAttribute('aria-pressed'),'true');
console.log('PASS: legacy migration, clearing legacy marks without resurrection, preserved calculation marks, and stale storage events use current data.');

// New content must be searchable and its new IDs must persist.
store.clear();const added=runPage('408.html');added.set('study-tag','图解');assert.equal(added.visible().length,6);
added.click('#study-reset');added.set('study-search','B 树高度公式');assert.equal(added.visible().length,1);
added.click('#study-reset');added.click('#k208 [data-mark="review"]');const addedReload=runPage('408.html');assert.equal(addedReload.get('k208').querySelector('[data-mark="review"]').getAttribute('aria-pressed'),'true');
console.log('PASS: six diagram cards, memory-topic search and persistence for new knowledge IDs.');
