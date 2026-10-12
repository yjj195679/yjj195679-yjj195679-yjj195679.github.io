/* No network requests: cards and explanations are static HTML. */
(function () {
  'use strict';
  const normalize = value => String(value || '').normalize('NFKC').toLowerCase().trim();
  function matches(card, filter, marks) {
    const state = marks[card.id] || 'unmarked';
    const words = normalize(filter.query).split(/\s+/).filter(Boolean);
    return (!filter.subject || card.subject === filter.subject)
      && (!filter.chapter || card.chapter === filter.chapter)
      && (!filter.tag || card.tags.includes(filter.tag))
      && (!filter.state || filter.state === state)
      && words.every(word => normalize(card.search).includes(word));
  }
  function validId(id) {
    return /^(k|c)\d{3}$/.test(id) && +id.slice(1) > 0 && +id.slice(1) <= (id[0] === 'k' ? 80 : 8);
  }
  function parseMarks(raw) {
    const clean = Object.create(null);
    try {
      const saved = JSON.parse(raw);
      if (!saved || typeof saved !== 'object' || Array.isArray(saved)) return clean;
      Object.entries(saved).forEach(([id, state]) => {
        if (validId(id) && (state === 'review' || state === 'mastered')) clean[id] = state;
      });
    } catch (_) { /* Corrupt storage is ignored. */ }
    return clean;
  }
  function toggleMark(marks, id, next) {
    if (!validId(id) || !['review', 'mastered'].includes(next)) return;
    if (marks[id] === next) delete marks[id];
    else marks[id] = next;
  }
  const core = { normalize, matches, parseMarks, toggleMark };
  if (typeof module !== 'undefined' && module.exports) module.exports = core;
  if (typeof document === 'undefined') return;
  const byId = id => document.getElementById(id);
  const fieldset = byId('study-filters');
  if (!fieldset) return;
  const query = byId('study-search'), subject = byId('study-subject');
  const chapter = byId('study-chapter'), tag = byId('study-tag'), state = byId('study-state');
  const cards = [...document.querySelectorAll('.study-card')];
  const records = cards.map(el => ({el, id: el.id, subject: el.dataset.subject,
    chapter: el.dataset.chapter, tags: el.dataset.tags.split(' '), search: el.dataset.search}));
  const sections = [...document.querySelectorAll('.study-subject')];
  const chapters = [...document.querySelectorAll('.study-chapter')];
  const storageKey = 'true-path-408-marks-v1';
  let marks = Object.create(null);
  try { marks = parseMarks(localStorage.getItem(storageKey)); }
  catch (_) { byId('study-storage').textContent = '当前浏览器不允许保存：标记在本次打开期间有效。'; }
  function save() {
    try { localStorage.setItem(storageKey, JSON.stringify(marks)); }
    catch (_) { byId('study-storage').textContent = '无法保存到浏览器：标记在本次打开期间有效。'; }
  }
  function readFilter() {
    return { query: query.value, subject: subject.value, chapter: chapter.value,
      tag: tag ? tag.value : '', state: state.value };
  }
  function updateChapters() {
    const previous = chapter.value;
    const names = [...new Set(records.filter(r => !subject.value || r.subject === subject.value).map(r => r.chapter))];
    chapter.replaceChildren(new Option('全部章节', ''), ...names.map(n => new Option(n, n)));
    chapter.value = names.includes(previous) ? previous : '';
  }
  function syncMarks(record) {
    const current = marks[record.id];
    const bar = record.el.querySelector('.study-mark');
    bar.hidden = false;
    bar.querySelectorAll('[data-mark]').forEach(button => {
      button.setAttribute('aria-pressed', String(button.dataset.mark === current));
    });
    bar.querySelector('.study-state-text').textContent = current === 'review' ? '待复习' : current === 'mastered' ? '已掌握' : '未标记';
  }
  function apply() {
    const filter = readFilter();
    records.forEach(record => { record.el.hidden = !matches(record, filter, marks); });
    chapters.forEach(group => { group.hidden = ![...group.querySelectorAll('.study-card')].some(el => !el.hidden); });
    sections.forEach(group => { group.hidden = ![...group.querySelectorAll('.study-card')].some(el => !el.hidden); });
    // main.js creates a shared section navigation; hide filtered-out subject links as well.
    document.querySelectorAll('.section-nav a').forEach(link => {
      const target = byId(link.hash.slice(1));
      if (target && target.classList.contains('study-subject')) link.hidden = target.hidden;
    });
    const visible = records.filter(record => !record.el.hidden);
    const review = visible.filter(record => marks[record.id] === 'review').length;
    const mastered = visible.filter(record => marks[record.id] === 'mastered').length;
    byId('study-count').textContent = `显示 ${visible.length} / ${records.length} 条 · 待复习 ${review} · 已掌握 ${mastered}`;
    byId('study-empty').hidden = visible.length !== 0;
  }
  function reset() {
    query.value = ''; subject.value = ''; chapter.value = ''; state.value = '';
    if (tag) tag.value = '';
    updateChapters(); apply();
  }
  fieldset.hidden = false;
  updateChapters();
  records.forEach(record => {
    syncMarks(record);
    record.el.querySelectorAll('[data-mark]').forEach(button => {
      button.addEventListener('click', () => {
        toggleMark(marks, record.id, button.dataset.mark);
        syncMarks(record); save(); apply();
        // If a selected-state filter hides this card, move focus to a stable visible control.
        if (record.el.hidden) state.focus();
      });
    });
  });
  query.addEventListener('input', apply);
  subject.addEventListener('change', () => { updateChapters(); apply(); });
  [chapter, tag, state].filter(Boolean).forEach(el => el.addEventListener('change', apply));
  byId('study-reset').addEventListener('click', reset);
  byId('study-expand').addEventListener('click', () => cards.filter(el => !el.hidden).forEach(el => { el.open = true; }));
  byId('study-collapse').addEventListener('click', () => cards.filter(el => !el.hidden).forEach(el => {
    el.open = false; el.querySelectorAll('details').forEach(nested => { nested.open = false; });
  }));
  function revealHash() {
    let id;
    try { id = decodeURIComponent(location.hash.slice(1)); } catch (_) { return; }
    const target = byId(id);
    if (!target || !(target.classList.contains('study-card') || target.classList.contains('study-subject'))) return;
    if (target.hidden) reset();
    if (target.classList.contains('study-card')) target.open = true;
    requestAnimationFrame(() => target.scrollIntoView({block: 'start'}));
  }
  window.addEventListener('hashchange', revealHash);
  // Clicking the existing hash should also reopen a collapsed card.
  document.addEventListener('click', event => {
    const link = event.target.closest && event.target.closest('a');
    if (link && link.hash && link.origin === location.origin && link.pathname === location.pathname && link.hash === location.hash) revealHash();
  });
  let printSnapshot = [];
  window.addEventListener('beforeprint', () => {
    printSnapshot = [...document.querySelectorAll('.study-card, .study-recall')].map(el => [el, el.open]);
    cards.filter(el => !el.hidden).forEach(el => {
      el.open = true; el.querySelectorAll('.study-recall').forEach(recall => { recall.open = true; });
    });
  });
  window.addEventListener('afterprint', () => { printSnapshot.forEach(([el, open]) => { el.open = open; }); });
  window.addEventListener('storage', event => {
    if (event.key !== storageKey && event.key !== null) return;
    marks = parseMarks(event.key === null ? null : event.newValue);
    records.forEach(syncMarks); apply();
  });
  apply(); revealHash();
})();
