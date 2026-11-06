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
  if(data.tree||data.graph){svg=document.createElementNS('http://www.w3.org/2000/svg','svg');svg.setAttribute('viewBox','0 0 660 260');svg.setAttribute('aria-hidden','true');svg.classList.add('sim-edges');path=document.createElementNS(svg.namespaceURI,'path');svg.append(path);track.append(svg);}
  const nodes=Array.from({length:3},()=>{const n=el('div','sim-node');track.append(n);return n;});
  const cursor=el('div','sim-cursor','↑ 当前操作');if(!data.tree&&!data.graph)track.append(cursor);
  const isBuffer=data.title.includes('容量2'),isTCP=data.title.includes('累计确认');
  const token=el('div','sim-token','产品 A');if(isBuffer)track.append(token);
  let flight,credit;
  if(isTCP){stage.classList.add('sim-tcp');flight=el('div','sim-bar sim-flight');credit=el('div','sim-bar sim-credit');track.append(flight,credit);}
  let mainCells,patternCells,patternRow,packet,pieces,addressToken;
  if(data.graph){[[205,80,'A→B：2'],[455,80,'B→C：1'],[330,195,'A→C：5']].forEach(([x,y,label])=>{const t=document.createElementNS(svg.namespaceURI,'text');t.setAttribute('x',x);t.setAttribute('y',y);t.setAttribute('text-anchor','middle');t.textContent=label;svg.append(t);});}
  if(data.scene==='address'){addressToken=el('div','sim-token','地址请求');track.append(addressToken);}
  if(data.scene==='kmp'){
   stage.classList.add('sim-kmp');nodes.forEach(n=>n.hidden=true);cursor.hidden=true;
   track.append(el('div','kmp-label kmp-label-main','主串 S（下标从0起）'));
   const main=el('div','kmp-row kmp-main');patternRow=el('div','kmp-row kmp-pattern');
   mainCells=[...'abababaca'].map((v,i)=>{const n=el('span','kmp-cell',v);n.title='S['+i+']';main.append(n);return n;});
   patternCells=[...'ababaca'].map((v,i)=>{const n=el('span','kmp-cell',v);n.title='P['+i+']';patternRow.append(n);return n;});
   track.append(main,el('div','kmp-label kmp-label-pattern','模式 P（动画显示对齐位置）'),patternRow);
  }
  if(data.scene==='fragment'){
   stage.classList.add('sim-fragment');nodes.forEach(n=>n.hidden=true);cursor.hidden=true;
   packet=el('div','fragment-packet','原数据报：20B首部 + 3980B数据');track.append(packet);
   pieces=[['片1','数据1480B','偏移0 / MF=1'],['片2','数据1480B','偏移185 / MF=1'],['片3','数据1020B','偏移370 / MF=0']].map(lines=>{const n=el('div','fragment-piece');lines.forEach(v=>n.append(el('span','',v)));track.append(n);return n;});
  }
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
   if(addressToken){addressToken.style.left=(step.positions[step.active][0]/6.6)+'%';addressToken.textContent=index<3?'页号 →':'物理地址 →';}
   if(mainCells){patternRow.style.transform='translateX('+(step.shift*48)+'px)';mainCells.forEach((n,i)=>{n.classList.toggle('kmp-current',i===step.i);n.classList.toggle('kmp-matched',index===5&&i>=2);});patternCells.forEach((n,i)=>{n.classList.toggle('kmp-current',i===step.j);n.classList.toggle('kmp-matched',i<step.j);});}
   if(pieces){packet.style.opacity=index<2?'1':'.35';pieces.forEach((n,i)=>{const show=index>=i+2;n.style.opacity=show?'1':'0';n.style.transform='translate('+(20+i*210)+'px,'+(show?135:30)+'px)';n.classList.toggle('fragment-active',index===i+2);});}
   if(path){const pairs=data.graph?[[0,1],[0,2],[1,2]]:index===0?[]:index<4?(index===1?[[0,1]]:[[0,1],[1,2]]):[[1,0],[1,2]];path.setAttribute('d',pairs.map(([a,b])=>`M${step.positions[a][0]+75} ${step.positions[a][1]+25} L${step.positions[b][0]+75} ${step.positions[b][1]+25}`).join(' '));}
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
