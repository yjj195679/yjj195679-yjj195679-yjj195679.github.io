(function () {
  'use strict';
  const signed = value => value >= 128 ? value - 256 : value;
  const hex = value => '0x' + value.toString(16).toUpperCase().padStart(2,'0');
  function parseByte(text) {
    const s = String(text).trim();
    if (!/^(?:0x[0-9a-f]{1,2}|-?\d+)$/i.test(s)) throw new Error('请输入 −128～255 的整数，或 0x00～0xFF。');
    const n = Number(s);
    if (!Number.isSafeInteger(n) || n < -128 || n > 255) throw new Error('8 位示例的输入范围为 −128～255。');
    return n & 255;
  }
  function calculateFlags(operation, aText, bText) {
    if (!['ADD','SUB','CMP','TEST'].includes(operation)) throw new Error('请选择 ADD、SUB、CMP 或 TEST。');
    const a = parseByte(aText), b = parseByte(bText);
    const result = (operation === 'ADD' ? a+b : operation === 'TEST' ? a&b : a-b) & 255;
    const cf = operation === 'ADD' ? +(a+b > 255) : operation === 'TEST' ? 0 : +(a<b);
    const of = operation === 'ADD' ? +Boolean((~(a^b)&(a^result))&128) : operation === 'TEST' ? 0 : +Boolean(((a^b)&(a^result))&128);
    const sf = result >>> 7, zf = +(result===0);
    const jumps = {JE:!!zf,JNE:!zf,JA:!cf&&!zf,JAE:!cf,JB:!!cf,JBE:!!cf||!!zf,JG:!zf&&sf===of,JGE:sf===of,JL:sf!==of,JLE:!!zf||sf!==of,JO:!!of,JNO:!of,JS:!!sf,JNS:!sf};
    return {operation,a,b,result,cf,of,sf,zf,jumps,writes:operation==='ADD'||operation==='SUB'};
  }
  if (typeof module !== 'undefined' && module.exports) module.exports = {parseByte, calculateFlags};
  if (typeof document === 'undefined') return;
  const form = document.getElementById('x86-flags-form');
  if (!form) return;
  const output = document.getElementById('x86-flags-result');
  function render(event) {
    if (event) event.preventDefault();
    output.replaceChildren();
    const add = text => { const p=document.createElement('p');p.textContent=text;output.append(p); };
    try {
      const r = calculateFlags(document.getElementById('x86-operation').value,document.getElementById('x86-a').value,document.getElementById('x86-b').value);
      add(`A=${hex(r.a)}（无符号 ${r.a}／有符号 ${signed(r.a)}）；B=${hex(r.b)}（无符号 ${r.b}／有符号 ${signed(r.b)}）。`);
      add(`8 位${r.writes?'写回':'临时'}结果=${hex(r.result)}（无符号 ${r.result}／有符号 ${signed(r.result)}）；${r.writes?'AL 更新，BL 不变。':'AL、BL 均不变。'}`);
      const flags = document.createElement('div');flags.className='x86-flag-badges';
      for (const name of ['cf','of','sf','zf']) {const badge=document.createElement('span');badge.textContent=`${name.toUpperCase()} = ${r[name]}`;badge.dataset.set=String(r[name]);flags.append(badge);}
      output.append(flags);
      add('若紧接 Jcc 且没有其他指令改标志，下列条件成立：'+Object.entries(r.jumps).filter(([,yes])=>yes).map(([name])=>name).join('、')+'。');
      add(r.operation==='CMP'||r.operation==='SUB'?'CMP／SUB 之后，JA/JB 与 JG/JL 分别对应 A 与 B 的无符号／有符号大小比较。':'本例 Jcc 只按当前标志判断；ADD／TEST 之后，不能把 JA/JG 等直接解释成 A>B。');
    } catch (error) {add(error.message);}
  }
  form.hidden = false;form.addEventListener('submit',render);render();
})();
