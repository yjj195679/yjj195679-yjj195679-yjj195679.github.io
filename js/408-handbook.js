(() => {
  'use strict';
  const byId = (id) => document.getElementById(id);
  const cards = [...document.querySelectorAll('.handbook408-card')];
  if (!cards.length) return;
  const chapters = [...document.querySelectorAll('#handbook408-groups .formula-chapter')];
  const links = [...document.querySelectorAll('[data-chapter-link]')];
  const search = byId('handbook408-search');
  const subject = byId('handbook408-subject');
  const chapter = byId('handbook408-chapter');
  const status = byId('handbook408-state');
  const random = byId('handbook408-random');
  const readingMeta = document.querySelector('.page-reading-meta');
  if (readingMeta) readingMeta.textContent = `${chapters.length} 个章节 · ${cards.length} 条知识点`;
  const storageKey = 'true-path-handbook408-progress-v1';
  const entryPrefix = 'true-path-handbook408-mark-v1-';
  const ids = new Set(cards.map((card) => card.id));
  const legacyIds = new Map();
  cards.forEach((card) => (card.dataset.legacyIds || '').split(/\s+/).filter(Boolean).forEach((id) => legacyIds.set(id, card.id)));
  const searchable = new Map(cards.map((card) => [card, card.textContent.normalize('NFKC').toLocaleLowerCase('zh-CN')]));
  let marks = Object.create(null);
  let visible = cards;
  let visualFilter = '';
  const visualButtons = [...document.querySelectorAll('[data-visual-filter]')];
  let canSave = true;
  const storageNote = byId('handbook408-storage');
  function readMarks() {
    const next = Object.create(null);
    try {
      let stored = {};
      try { stored = JSON.parse(localStorage.getItem(storageKey) || '{}'); } catch { /* Ignore a damaged legacy snapshot. */ }
      if (stored && typeof stored === 'object' && !Array.isArray(stored)) {
        Object.entries(stored).forEach(([id, value]) => {
          const currentId = ids.has(id) ? id : legacyIds.get(id);
          if (currentId && (value === 'review' || value === 'mastered')) next[currentId] = value;
        });
      }
      ids.forEach((id) => {
        const value = localStorage.getItem(entryPrefix + id);
        if (value === 'review' || value === 'mastered') next[id] = value;
        else if (value !== null) delete next[id];
      });
    } catch { /* Malformed or unavailable storage must not block reading. */ }
    return next;
  }
  marks = readMarks();
  function syncMarks() {
    cards.forEach((card) => {
      const value = marks[card.id] || '';
      card.dataset.state = value;
      card.querySelectorAll('[data-mark]').forEach((button) => button.setAttribute('aria-pressed', String(button.dataset.mark === value)));
      card.querySelector('.formula-state-text').textContent = value === 'mastered' ? '已掌握' : value === 'review' ? '待复习' : '未标记';
    });
    byId('handbook408-progress').textContent = String(Object.values(marks).filter((value) => value === 'mastered').length);
  }
  function buildChapters() {
    const old = chapter.value;
    chapter.replaceChildren(new Option('全部章节', ''));
    chapters.filter((el) => !subject.value || el.dataset.subject === subject.value).forEach((el) => {
      chapter.add(new Option(el.querySelector('h2').textContent, el.id));
    });
    chapter.value = [...chapter.options].some((option) => option.value === old) ? old : '';
  }
  function filter() {
    const terms = search.value.normalize('NFKC').trim().toLocaleLowerCase('zh-CN').split(/\s+/).filter(Boolean);
    visible = [];
    cards.forEach((card) => {
      const state = marks[card.id] || 'unmarked';
      const show = (!subject.value || card.dataset.subject === subject.value)
        && (!chapter.value || card.dataset.chapter === chapter.value)
        && (!visualFilter || card.dataset[visualFilter === 'diagram' ? 'hasDiagram' : 'hasAnimation'] === '1')
        && (!status.value || status.value === state)
        && terms.every((term) => searchable.get(card).includes(term));
      card.hidden = !show;
      if (show) visible.push(card);
    });
    chapters.forEach((el) => {
      const count = [...el.querySelectorAll('.handbook408-card')].filter((card) => !card.hidden).length;
      el.hidden = count === 0;
      el.querySelector('[data-chapter-count]').textContent = String(count);
      const link = links.find((a) => a.dataset.chapterLink === el.id);
      link.hidden = !count;
      link.querySelector('.index-count').textContent = String(count);
    });
    document.querySelectorAll('#handbook408-index .index-subject').forEach((heading) => {
      let next = heading.nextElementSibling;
      let hasVisible = false;
      while (next && !next.classList.contains('index-subject')) {
        if (!next.hidden) hasVisible = true;
        next = next.nextElementSibling;
      }
      heading.hidden = !hasVisible;
    });
    byId('handbook408-empty').hidden = visible.length !== 0;
    byId('handbook408-count').textContent = `显示 ${visible.length} / ${cards.length} 条知识点`;
    random.disabled = !visible.length;
  }
  function reset() {
    search.value = subject.value = status.value = '';
    visualFilter = '';
    visualButtons.forEach(b => b.setAttribute('aria-pressed', String(b.dataset.visualFilter === '')));
    buildChapters();
    chapter.value = '';
    filter();
  }
  function jump(target) {
    if (!target) return;
    if (target.hidden || target.closest('.formula-chapter[hidden]')) reset();
    if (target.matches('.handbook408-card')) target.open = true;
    const focus = target.querySelector('summary,h2');
    if (focus) {
      if (focus.tagName !== 'SUMMARY') focus.tabIndex = -1;
      focus.focus({ preventScroll: true });
    }
    window.scrollTo({ top: Math.max(0, target.getBoundingClientRect().top + window.scrollY - 96), behavior: 'instant' });
    links.forEach((link) => {
      if (link.dataset.chapterLink === (target.dataset.chapter || target.id)) link.setAttribute('aria-current', 'location');
      else link.removeAttribute('aria-current');
    });
  }
  function followHash() {
    let id;
    try { id = decodeURIComponent(location.hash.slice(1)); } catch { return; }
    const el = byId(id) || byId(legacyIds.get(id));
    if (el && (el.matches('.handbook408-card') || chapters.includes(el))) jump(el);
  }
  buildChapters();
  syncMarks();
  filter();
  byId('handbook408-controls').hidden = false;
  document.querySelectorAll('.handbook408-card .formula-actions').forEach((el) => { el.hidden = false; });
  visualButtons.forEach(button => button.addEventListener('click', () => {
    visualFilter = button.dataset.visualFilter;
    visualButtons.forEach(b => b.setAttribute('aria-pressed', String(b === button)));
    filter();
  }));
  search.addEventListener('input', filter);
  subject.addEventListener('change', () => { chapter.value = ''; buildChapters(); filter(); });
  chapter.addEventListener('change', filter);
  status.addEventListener('change', filter);
  byId('handbook408-reset').addEventListener('click', reset);
  byId('handbook408-expand').addEventListener('click', () => visible.forEach((card) => { card.open = true; }));
  byId('handbook408-collapse').addEventListener('click', () => visible.forEach((card) => { card.open = false; }));
  random.addEventListener('click', () => {
    if (visible.length) jump(visible[Math.floor(Math.random() * visible.length)]);
  });
  byId('handbook408-groups').addEventListener('click', (event) => {
    const button = event.target.closest('button[data-mark]');
    if (!button) return;
    const card = button.closest('.handbook408-card');
    const value = button.dataset.mark;
    if (marks[card.id] === value) delete marks[card.id];
    else marks[card.id] = value;
    try { localStorage.setItem(entryPrefix + card.id, marks[card.id] || 'unmarked'); marks = readMarks(); }
    catch {
      canSave = false;
      storageNote.textContent = '当前浏览器无法保存标记；标记仅在本次页面打开期间有效。搜索与阅读可正常使用。';
    }
    syncMarks();
    filter();
    if (card.hidden) status.focus({ preventScroll: true });
  });
  // Preserve the current expanded state, including when the print dialog is cancelled.
  let printState = null;
  function beforePrint() {
    if (printState) return;
    printState = new Map(cards.map((card) => [card, card.open]));
    visible.forEach((card) => { card.open = true; });
  }
  function afterPrint() {
    if (!printState) return;
    printState.forEach((open, card) => { card.open = open; });
    printState = null;
  }
  byId('handbook408-print').addEventListener('click', () => {
    if (window.TruePathDocumentTools) window.TruePathDocumentTools.openExport();
    else if (typeof window.print === 'function') window.print();
  });
  window.addEventListener('beforeprint', beforePrint);
  window.addEventListener('afterprint', afterPrint);
  window.addEventListener('hashchange', followHash);
  links.forEach((link) => link.addEventListener('click', () => jump(byId(link.dataset.chapterLink))));
  document.querySelectorAll('.handbook408-card .formula-actions a').forEach((link) => link.addEventListener('click', () => jump(link.closest('.handbook408-card'))));
  window.addEventListener('storage', (event) => {
    if ((event.key === storageKey || event.key === null || event.key.startsWith(entryPrefix)) && canSave) { marks = readMarks(); syncMarks(); filter(); }
  });
  followHash();
})();
