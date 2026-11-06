/* Finite, deterministic examples; no network or changes to saved study marks. */
(() => {
 'use strict';
 const el=(tag,cls,text)=>{const n=document.createElement(tag);if(cls)n.className=cls;if(text)n.textContent=text;return n;};
 document.querySelectorAll('.study-sim').forEach(root=>{
  let data;try{data=JSON.parse(root.querySelector('.sim-data').textContent);}catch{return;}
  if(!data.steps?.length)return;
  const host=root.querySelector('.sim-interactive');host.hidden=false;
  let index=0,timer=null,playing=false;
  const stage=el('div','sim-stage'),track=el('div','sim-track');stage.append(track);host.append(stage);
  let svg,path;
  if(data.tree){svg=document.createElementNS('http://www.w3.org/2000/svg','svg');svg.setAttribute('viewBox','0 0 660 260');svg.setAttribute('aria-hidden','true');svg.classList.add('sim-edges');path=document.createElementNS(svg.namespaceURI,'path');svg.append(path);track.append(svg);}
  const nodes=Array.from({length:3},()=>{const n=el('div','sim-node');track.append(n);return n;});
  const cursor=el('div','sim-cursor','↑ 当前操作');if(!data.tree)track.append(cursor);
  const isBuffer=data.title.includes('容量2'),isTCP=data.title.includes('累计确认');
  const token=el('div','sim-token','产品 A');if(isBuffer)track.append(token);
  let flight,credit;
  if(isTCP){stage.classList.add('sim-tcp');flight=el('div','sim-bar sim-flight');credit=el('div','sim-bar sim-credit');track.append(flight,credit);}
  const count=el('p','sim-count'),heading=el('h5','sim-heading'),explain=el('p','sim-explain');
  const status=el('div','sim-status');status.setAttribute('aria-live','polite');status.setAttribute('aria-atomic','true');status.append(count,heading,explain);host.append(status);
  const buttons=el('div','sim-buttons');
  const prev=el('button','button','上一步'),next=el('button','button','下一步'),play=el('button','button','自动演示'),reset=el('button','button','重置');
  [prev,next,play,reset].forEach(b=>{b.type='button';buttons.append(b);});host.append(buttons);
  function stop(){clearTimeout(timer);timer=null;playing=false;play.textContent='自动演示';play.setAttribute('aria-pressed','false');}
  function render(){
   const step=data.steps[index];count.textContent=`步骤 ${index+1} / ${data.steps.length}`;heading.textContent=step.title;explain.textContent=step.explain;
   prev.disabled=index===0;next.disabled=index===data.steps.length-1;
   nodes.forEach((n,i)=>{n.textContent=step.values[i];n.style.left=(step.positions[i][0]/6.6)+'%';n.style.top=step.positions[i][1]+'px';n.classList.toggle('sim-active',i===step.active);n.classList.toggle('sim-pending',step.values[i].includes('未插入'));});
   cursor.style.left=(step.positions[step.active][0]/6.6)+'%';
   if(isBuffer){token.style.left=([30,30,255,255,255,465,465][index]/6.6)+'%';token.style.opacity=index===0?'0':'1';token.textContent=index===6?'A 已消费':'产品 A';}
   if(isTCP){flight.style.width=([.5,1,.5,.5,0][index]*90)+'%';credit.style.width=([.5,0,.5,0,1000/1200][index]*90)+'%';flight.textContent='在途数据';credit.textContent='可新增发送';}
   if(path){const pairs=index===0?[]:index<4?(index===1?[[0,1]]:[[0,1],[1,2]]):[[1,0],[1,2]];path.setAttribute('d',pairs.map(([a,b])=>`M${step.positions[a][0]+75} ${step.positions[a][1]+25} L${step.positions[b][0]+75} ${step.positions[b][1]+25}`).join(' '));}
  }
  function tick(){if(index<data.steps.length-1){index++;render();}if(index===data.steps.length-1)stop();else timer=setTimeout(tick,2600);}
  prev.addEventListener('click',()=>{stop();index=Math.max(0,index-1);render();});next.addEventListener('click',()=>{stop();index=Math.min(data.steps.length-1,index+1);render();});
  reset.addEventListener('click',()=>{stop();index=0;render();});
  play.addEventListener('click',()=>{if(playing){stop();return;}if(index===data.steps.length-1)index=0;playing=true;play.textContent='暂停演示';play.setAttribute('aria-pressed','true');render();timer=setTimeout(tick,2600);});
  root.closest('.handbook408-card')?.addEventListener('toggle',e=>{if(!e.target.open)stop();});
  document.addEventListener('visibilitychange',()=>{if(document.hidden)stop();});
  let wasOpen=false;const transcript=root.querySelector('.sim-transcript');window.addEventListener('beforeprint',()=>{stop();wasOpen=transcript.open;transcript.open=true;});window.addEventListener('afterprint',()=>{transcript.open=wasOpen;});
  render();
 });
})();
