const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const {parseHTML}=require('linkedom');
const root=require('node:path').resolve(__dirname,'..')+'/';
const items=JSON.parse(fs.readFileSync(root+'data/408-handbook.json','utf8'));
const code=fs.readFileSync(root+'js/408-handbook.js','utf8');
const store=new Map([['true-path-408-mark-v2-k001','review']]);
function page(blocked=false,hash=''){
 const {window,document}=parseHTML(fs.readFileSync(root+'408-handbook.html','utf8'));
 const selections=new WeakMap();
 Object.defineProperty(window.HTMLSelectElement.prototype,'value',{configurable:true,get(){return selections.get(this)??this.querySelector('option')?.value??''},set(v){selections.set(this,String(v))}});
 Object.defineProperty(window.HTMLSelectElement.prototype,'options',{configurable:true,get(){return [...this.querySelectorAll('option')]}});
 window.HTMLSelectElement.prototype.add=function(el){this.append(el)};
 window.HTMLElement.prototype.focus=function(){document.lastFocused=this};
 window.HTMLElement.prototype.getBoundingClientRect=function(){return {top:200}};
 const local=blocked?{getItem(){throw Error('blocked')},setItem(){throw Error('blocked')}}:{getItem:k=>store.get(k)??null,setItem:(k,v)=>store.set(k,String(v))};
 const location={hash};window.scrollY=0;window.scrollTo=()=>{};window.print=()=>{};
 vm.runInNewContext(code,{document,window,location,localStorage:local,Option:function(text,value){const e=document.createElement('option');e.textContent=text;e.value=value;return e;},Math});
 const get=id=>document.getElementById(id),visible=()=>[...document.querySelectorAll('.handbook408-card')].filter(x=>!x.hidden);
 const set=(name,v)=>{get('handbook408-'+name).value=v;get('handbook408-'+name).dispatchEvent(new window.Event(name==='search'?'input':'change'))};
 const click=selector=>document.querySelector(selector).dispatchEvent(new window.Event('click',{bubbles:true}));
 return {get,visible,set,click,window,document};
}
let p=page();assert.equal(p.visible().length,items.length);assert(!p.get('handbook408-controls').hidden);
const co=items.filter(x=>x.subject==='计算机组成原理');p.set('subject','计算机组成原理');assert.equal(p.visible().length,co.length);
assert([...p.get('handbook408-chapter').options].slice(1).every(o=>p.get(o.value).dataset.subject==='计算机组成原理'));
p.set('search','zzzz-不存在');assert.equal(p.visible().length,0);assert(p.get('handbook408-random').disabled);p.click('#handbook408-reset');
const first=items[0];p.set('search',first.title);assert(p.visible().some(x=>x.id===first.id));p.click('#'+first.id+' [data-mark="review"]');assert.equal(store.get('true-path-handbook408-mark-v1-'+first.id),'review');
let again=page(false,'#'+first.id);assert(again.get(first.id).open);assert.equal(again.get(first.id).querySelector('[data-mark="review"]').getAttribute('aria-pressed'),'true');
assert.equal(store.get('true-path-408-mark-v2-k001'),'review','Original review record must remain independent');
again.set('state','review');assert.equal(again.visible().length,1);again.click('#'+first.id+' [data-mark="review"]');assert.equal(again.visible().length,0);assert.equal(again.document.lastFocused.id,'handbook408-state');
let blocked=page(true);blocked.click('#'+first.id+' [data-mark="mastered"]');assert(blocked.get('handbook408-storage').textContent.includes('本次'));
// Two tabs changing independent entries must not overwrite each other.
const a=page(),b=page(),second=items[1];a.click('#'+first.id+' [data-mark="review"]');b.click('#'+second.id+' [data-mark="mastered"]');store.set('true-path-handbook408-progress-v1','{bad');const merged=page();assert.equal(merged.get(first.id).querySelector('[data-mark="review"]').getAttribute('aria-pressed'),'true');assert.equal(merged.get(second.id).querySelector('[data-mark="mastered"]').getAttribute('aria-pressed'),'true');
const print=page();print.set('subject',first.subject);const openBefore=print.visible().map(x=>x.open);print.window.dispatchEvent(new print.window.Event('beforeprint'));assert(print.visible().every(x=>x.open));print.window.dispatchEvent(new print.window.Event('afterprint'));assert.deepEqual(print.visible().map(x=>x.open),openBefore);
print.click('#handbook408-expand');assert(print.visible().every(x=>x.open));print.click('#handbook408-collapse');assert(print.visible().every(x=>!x.open));
console.log('PASS handbook: all cards, subject/chapter filtering, search and empty state, independent persistence, blocked storage, concurrent marks, deep links, expand/collapse, print restoration.');
