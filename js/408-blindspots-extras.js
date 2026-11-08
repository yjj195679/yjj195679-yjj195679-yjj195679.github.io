(function () {
  'use strict';
  const hex = value => '0x' + (value >>> 0).toString(16).toUpperCase().padStart(8, '0');
  function branchImmediate(pcText, targetText) {
    const parse = text => {
      const value = String(text).trim();
      if (!/^(?:0x)?[0-9a-f]{1,8}$/i.test(value)) throw new Error('请输入 1–8 位十六进制地址，可带 0x 前缀。');
      return parseInt(value.replace(/^0x/i, ''), 16);
    };
    const pc = parse(pcText), target = parse(targetText);
    if (pc % 4 || target % 4) throw new Error('经典 32 位指令地址须 4 B 对齐，请检查 PC 和目标地址。');
    const base = (pc + 4) >>> 0;
    const delta = (target - base) | 0;
    const immediate = delta / 4;
    if (immediate < -32768 || immediate > 32767) throw new Error('目标超出 16 位有符号分支偏移范围：−32768～32767 个指令字。');
    return {pc, target, base, delta, immediate, encoding:'0x' + (immediate & 0xFFFF).toString(16).toUpperCase().padStart(4, '0')};
  }
  if (typeof module !== 'undefined' && module.exports) module.exports = {branchImmediate};
  if (typeof document === 'undefined') return;
  const boxes = [...document.querySelectorAll('[data-priority]')];
  const prefix = 'true-path-408-blindspots-priority-v1-';
  const storageNote = document.getElementById('priority-storage');
  const update = () => {
    const count = boxes.filter(box => box.checked).length;
    document.getElementById('priority-count').textContent = `${count} / ${boxes.length} 已掌握`;
    document.getElementById('priority-progress').value = count;
  };
  const failed = () => { storageNote.textContent = '浏览器暂不允许保存，清单进度仅在本次打开期间有效。'; };
  boxes.forEach(box => {
    try { box.checked = localStorage.getItem(prefix + box.dataset.priority) === '1'; } catch (_) { failed(); }
    box.addEventListener('change', () => {
      try { localStorage.setItem(prefix + box.dataset.priority, box.checked ? '1' : '0'); } catch (_) { failed(); }
      document.getElementById('priority-reset-note').textContent = '';
      update();
    });
  });
  let undo = null;
  const reset = document.getElementById('priority-reset');
  reset.addEventListener('click', () => {
    if (undo) {
      boxes.forEach((box, i) => { box.checked = undo[i]; });
      undo = null; reset.textContent = '重置清单进度';
      document.getElementById('priority-reset-note').textContent = '已恢复清单进度。';
    } else {
      undo = boxes.map(box => box.checked);
      boxes.forEach(box => { box.checked = false; });
      reset.textContent = '撤销重置';
      document.getElementById('priority-reset-note').textContent = '已清空 15 项清单，卡片标记保留。';
    }
    boxes.forEach(box => { try { localStorage.setItem(prefix + box.dataset.priority, box.checked ? '1' : '0'); } catch (_) { failed(); } });
    update();
  });
  window.addEventListener('storage', event => {
    if (event.key !== null && !event.key.startsWith(prefix)) return;
    try { boxes.forEach(box => { box.checked = localStorage.getItem(prefix + box.dataset.priority) === '1'; }); } catch (_) { failed(); }
    update();
  });
  update();
  const steps = [
    ['读懂题设','beq 位于 0x00400020，目标 0x00400010；需要求 16 位立即数字段。'],
    ['定位基准','分支基准为 PC+4=0x00400024。'],
    ['计算字节差','目标 − 基准 = 0x00400010 − 0x00400024 = −20 B。'],
    ['换算指令字偏移','−20 / 4 = −5，16 位补码是 0xFFFB。'],
    ['反代验证','符号扩展 0xFFFB 得 −5，再左移 2 得 −20；0x00400024−20=0x00400010。']
  ];
  let step = 0;
  const prev = document.getElementById('mips-prev'), next = document.getElementById('mips-next');
  function renderStep() {
    document.getElementById('mips-step-count').textContent = `第 ${step+1} / ${steps.length} 步`;
    document.getElementById('mips-step-title').textContent = steps[step][0];
    document.getElementById('mips-step-text').textContent = steps[step][1];
    prev.disabled = step === 0; next.disabled = step === steps.length - 1;
  }
  prev.addEventListener('click', () => { if (step > 0) --step; renderStep(); });
  next.addEventListener('click', () => { if (step < steps.length-1) ++step; renderStep(); });
  document.getElementById('mips-restart').addEventListener('click', () => { step = 0; renderStep(); });
  document.getElementById('mips-stepper').hidden = false;
  renderStep();
  const form = document.getElementById('mips-address-form');
  function calculate(event) {
    if (event) event.preventDefault();
    const result = document.getElementById('mips-address-result');
    try {
      const r = branchImmediate(document.getElementById('mips-pc').value, document.getElementById('mips-target').value);
      result.textContent = `PC+4=${hex(r.base)}；字节差=${r.delta}；立即数=${r.immediate}；16 位编码=${r.encoding}。反代：${hex(r.base)} + (${r.immediate} × 4) = ${hex(r.target)}。`;
    } catch (error) { result.textContent = error.message; }
  }
  form.addEventListener('submit', calculate); calculate();
})();
