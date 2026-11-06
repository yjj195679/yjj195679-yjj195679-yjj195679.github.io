/* SVG teaching boards: stable node identity, reversible state, no remote dependencies. */
(() => {
 'use strict';
 const NS='http://www.w3.org/2000/svg';
 const make=(tag,cls,text)=>{const n=document.createElement(tag);if(cls)n.className=cls;if(text)n.textContent=text;return n;};
 const svgEl=(tag,attrs={})=>{const n=document.createElementNS(NS,tag);for(const [k,v] of Object.entries(attrs))n.setAttribute(k,String(v));return n;};
 document.querySelectorAll('.study-sim').forEach((root,uid)=>{
  const raw=root.querySelector('.sim-data');let data;try{data=JSON.parse(raw.textContent);}catch{return;}
  if(data.scene!=='board'||!data.steps?.length)return;
  const host=root.querySelector('.sim-interactive'),card=root.closest('.handbook408-card');
  let index=0,timer=null,ready=false,playing=false,wasOpen=false;
  const transcript=root.querySelector('.sim-transcript');
  let svg,note,heading,explain,count,prev,next,play,seek,speed;
  const nodes=new Map(),paths=new Map(),wires=new Map();
  function stop(){clearTimeout(timer);timer=null;playing=false;if(play){play.textContent='自动演示';play.setAttribute('aria-pressed','false');}}
  function init(){
   if(ready)return;ready=true;host.hidden=false;
   const stage=make('div','board-stage');stage.tabIndex=0;stage.setAttribute('role','region');stage.setAttribute('aria-label',data.title+'，图画可横向滚动');
   svg=svgEl('svg',{viewBox:'0 0 900 '+data.height,role:'img','aria-label':data.title});svg.classList.add('board-svg');
   const defs=svgEl('defs'),marker=svgEl('marker',{id:'board-arrow-'+uid,viewBox:'0 0 10 10',refX:9,refY:5,markerWidth:6,markerHeight:6,orient:'auto'});
   marker.append(svgEl('path',{d:'M0 0 L10 5 L0 10z',fill:'var(--hand-concept)'}));defs.append(marker);svg.append(defs);
   const wireLayer=svgEl('g'),edgeLayer=svgEl('g'),nodeLayer=svgEl('g');svg.append(wireLayer,edgeLayer,nodeLayer);
   for(const step of data.steps){
    for(const wire of step.wires||[]){if(wires.has(wire.id))continue;const p=svgEl('path');p.classList.add('board-wire');wireLayer.append(p);wires.set(wire.id,p);}
    for(const n of step.nodes){if(nodes.has(n.id))continue;const g=svgEl('g');g.classList.add('board-node');const rect=svgEl('rect',{rx:10});g.append(rect);nodeLayer.append(g);nodes.set(n.id,{g,rect});}
    for(const ed of step.edges){const key=ed.a+'|'+ed.b+'|'+ed.label;if(paths.has(key))continue;const path=svgEl('path',{'marker-end':'url(#board-arrow-'+uid+')'}),label=svgEl('text',{'text-anchor':'middle'});path.classList.add('board-edge');label.classList.add('board-edge-label');edgeLayer.append(path,label);paths.set(key,{path,label});}
   }
   stage.append(svg);host.append(stage);note=make('p','board-note');host.append(note);
   const status=make('div','sim-status');status.setAttribute('aria-live','polite');status.setAttribute('aria-atomic','true');count=make('p','sim-count');heading=make('h5','sim-heading');explain=make('p','sim-explain');status.append(count,heading,explain);host.append(status);
   const controls=make('div','sim-buttons');[prev,next,play]=['上一步','下一步','自动演示'].map(t=>make('button','button',t));const reset=make('button','button','重置');
   for(const b of [prev,next,play,reset]){b.type='button';controls.append(b);}host.append(controls);play.setAttribute('aria-pressed','false');
   const settings=make('div','board-settings'),seekLabel=make('label','', '跳转步骤 ');seek=make('input');seek.type='range';seek.min='0';seek.max=String(data.steps.length-1);seek.step='1';seekLabel.append(seek);
   const speedLabel=make('label','','速度 ');speed=make('select');for(const [v,t] of [['4000','慢速'],['2600','标准'],['1300','快速']]){const opt=make('option','',t);opt.value=v;speed.append(opt);}speed.value='2600';speedLabel.append(speed);settings.append(seekLabel,speedLabel);host.append(settings);
   prev.addEventListener('click',()=>{stop();index=Math.max(0,index-1);render();});next.addEventListener('click',()=>{stop();index=Math.min(data.steps.length-1,index+1);render();});reset.addEventListener('click',()=>{stop();index=0;render();});
   seek.addEventListener('input',()=>{stop();index=Number(seek.value);render();});
   play.addEventListener('click',()=>{if(playing){stop();return;}document.dispatchEvent(new CustomEvent('handbook408-play',{detail:root}));if(index===data.steps.length-1)index=0;playing=true;play.textContent='暂停演示';play.setAttribute('aria-pressed','true');render();timer=setTimeout(tick,Number(speed.value));});
   speed.addEventListener('change',()=>{if(playing){clearTimeout(timer);timer=setTimeout(tick,Number(speed.value));}});
   render();
  }
  function render(){
   const s=data.steps[index];
   wires.forEach((p,id)=>{const wire=(s.wires||[]).find(w=>w.id===id);p.style.opacity=wire?'1':'0';if(wire)p.setAttribute('d',wire.points.map(([x,y],i)=>(i?'L':'M')+x+','+y).join(' '));});
   const here=new Map(s.nodes.map(n=>[n.id,n]));
   nodes.forEach(({g,rect},id)=>{const n=here.get(id);g.style.opacity=n&&n.w>4?'1':'0';if(!n)return;g.setAttribute('class','board-node '+n.tone);g.style.transform=`translate(${n.x}px,${n.y}px)`;rect.setAttribute('width',n.w);rect.setAttribute('height',n.h);
    g.querySelectorAll('text').forEach(t=>t.remove());const lines=n.label.split('\n');const units=Math.max(...lines.map(l=>[...l].reduce((a,c)=>a+(c.charCodeAt(0)>255?1:.58),0)));const font=Math.min(19,(n.w-14)/Math.max(1,units),(n.h-12)/lines.length/1.3);
    lines.forEach((line,k)=>{const t=svgEl('text',{x:n.w/2,y:n.h/2+(k-(lines.length-1)/2)*26+7,'text-anchor':'middle','font-size':font});t.textContent=line;g.append(t);});
   });
   const edges=new Set(s.edges.map(ed=>ed.a+'|'+ed.b+'|'+ed.label));paths.forEach(({path,label},key)=>{const show=edges.has(key);path.style.opacity=label.style.opacity=show?'1':'0';if(!show)return;const ed=s.edges.find(e=>e.a+'|'+e.b+'|'+e.label===key);if(ed.directed===false)path.removeAttribute('marker-end');
    const a=here.get(ed.a),b=here.get(ed.b);const ax=a.x+a.w/2,ay=a.y+a.h/2,bx=b.x+b.w/2,by=b.y+b.h/2,dx=bx-ax,dy=by-ay;
    let start=Math.min(dx?(a.w/2+4)/Math.abs(dx):1e6,dy?(a.h/2+4)/Math.abs(dy):1e6),end=Math.min(dx?(b.w/2+8)/Math.abs(dx):1e6,dy?(b.h/2+8)/Math.abs(dy):1e6);if(a.w<5){start=0;end=0;}
    path.style.strokeDasharray=ed.points?'6 5':'';
    path.setAttribute('d',ed.points?ed.points.map(([x,y],i)=>(i?'L':'M')+x+','+y).join(' '):`M${ax+dx*start},${ay+dy*start} L${bx-dx*end},${by-dy*end}`);label.setAttribute('x',(ax+bx)/2);label.setAttribute('y',(ay+by)/2-12);label.style.fontSize=Math.min(18,(Math.abs(dx)>100?Math.abs(dx)-18:180)/Math.max(1,[...ed.label].reduce((a,c)=>a+(c.charCodeAt(0)>255?1:.58),0)))+'px';label.textContent=ed.label;
   });
   note.textContent=s.note||'蓝色为结构；紫色为当前操作；绿色为已处理部分。';count.textContent=`步骤 ${index+1} / ${data.steps.length}`;heading.textContent=s.title;explain.textContent=s.explain;seek.value=String(index);seek.setAttribute('aria-valuetext',`${index+1}：${s.title}`);prev.disabled=index===0;next.disabled=index===data.steps.length-1;
  }
  function tick(){if(document.hidden||card?.hidden||!card?.open){stop();return;}if(index<data.steps.length-1){index++;render();}if(index===data.steps.length-1)stop();else timer=setTimeout(tick,Number(speed.value));}
  card?.addEventListener('toggle',()=>{if(card.open)init();else stop();});if(card?.open)init();
  document.addEventListener('handbook408-play',e=>{if(e.detail!==root)stop();});document.addEventListener('visibilitychange',()=>{if(document.hidden)stop();});
  ['input','change','click'].forEach(type=>document.getElementById('handbook408-controls')?.addEventListener(type,()=>stop()));
  if('IntersectionObserver' in window)new IntersectionObserver(entries=>{if(!entries[0].isIntersecting)stop();}).observe(root);
  window.addEventListener('beforeprint',()=>{stop();wasOpen=transcript.open;transcript.open=true;});window.addEventListener('afterprint',()=>{transcript.open=wasOpen;});
 });
})();
