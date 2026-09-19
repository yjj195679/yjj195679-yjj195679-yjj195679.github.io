(() => {
  const STORAGE_KEY = "tpm-vocabulary-progress-v1";
  const state = { data: [], byId: new Map(), order: [], position: 0, revealed: false, known: new Set(), unknown: new Set(), mode: "全部词组" };
  const el = {};
  const ids = ["known-count", "unknown-count", "all-button", "shuffle-button", "review-button", "jump-form", "jump-input", "reset-button", "progress-label", "mode-label", "progress-bar", "study-card", "card-number", "card-status", "card-front", "card-answer", "term-list", "answer-list", "previous-button", "reveal-button", "unknown-button", "known-button", "next-button", "study-message"];

  function loadProgress() {
    try {
      const saved = JSON.parse(localStorage.getItem(STORAGE_KEY) || "{}");
      state.known = new Set(saved.known || []);
      state.unknown = new Set(saved.unknown || []);
      return Number(saved.lastId) || 1;
    } catch (_) { return 1; }
  }

  function currentCard() { return state.byId.get(state.order[state.position]); }
  function saveProgress() { const card = currentCard(); localStorage.setItem(STORAGE_KEY, JSON.stringify({ known: [...state.known], unknown: [...state.unknown], lastId: card ? card.id : 1 })); }
  function padId(value) { return String(value).padStart(3, "0"); }
  function stripPartOfSpeech(term) { return term.replace(/\s+(?:n|v|vi|vt|adj|adv|prep|conj|pron|num|phr|idm|aux|abbr|det|interj)\.$/i, ""); }

  function speak(term) {
    if (!("speechSynthesis" in window)) return;
    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(stripPartOfSpeech(term));
    utterance.lang = "en-US";
    utterance.rate = 0.88;
    window.speechSynthesis.speak(utterance);
  }

  function termRow(entry) {
    const row = document.createElement("div"); row.className = "term-item";
    const button = document.createElement("button"); button.className = "speak-button"; button.type = "button"; button.setAttribute("aria-label", `朗读 ${stripPartOfSpeech(entry.term)}`); button.textContent = "▶";
    button.addEventListener("click", event => { event.stopPropagation(); speak(entry.term); });
    const word = document.createElement("span"); word.textContent = entry.term;
    row.append(button, word); return row;
  }

  function answerRow(entry) {
    const row = document.createElement("div"); row.className = "answer-item";
    const term = document.createElement("div"); term.className = "answer-term"; term.textContent = entry.term;
    const definition = document.createElement("div"); definition.className = "answer-definition"; definition.textContent = entry.definition;
    row.append(term, definition); return row;
  }

  function render() {
    const card = currentCard(); if (!card) return;
    state.revealed = false;
    el["card-number"].textContent = padId(card.id);
    el["term-list"].replaceChildren(...card.entries.map(termRow));
    el["answer-list"].replaceChildren(...card.entries.map(answerRow));
    el["card-front"].hidden = false; el["card-answer"].hidden = true; el["reveal-button"].textContent = "查看释义";
    el["card-status"].textContent = state.known.has(card.id) ? "已掌握" : state.unknown.has(card.id) ? "需复习" : "未标记";
    el["progress-label"].textContent = `第 ${state.position + 1} / ${state.order.length} 组`;
    el["mode-label"].textContent = state.mode;
    el["progress-bar"].style.width = `${((state.position + 1) / state.order.length) * 100}%`;
    el["known-count"].textContent = state.known.size; el["unknown-count"].textContent = state.unknown.size; el["study-message"].textContent = ""; saveProgress();
  }

  function toggleAnswer() { state.revealed = !state.revealed; el["card-front"].hidden = state.revealed; el["card-answer"].hidden = !state.revealed; el["reveal-button"].textContent = state.revealed ? "隐藏释义" : "查看释义"; }
  function move(delta) { if (!state.order.length) return; state.position = (state.position + delta + state.order.length) % state.order.length; render(); }
  function mark(kind) { const card = currentCard(); if (!card) return; if (kind === "known") { state.known.add(card.id); state.unknown.delete(card.id); } else { state.unknown.add(card.id); state.known.delete(card.id); } saveProgress(); move(1); }
  function showAll(targetId) { state.order = state.data.map(card => card.id); state.mode = "全部词组"; const index = state.order.indexOf(targetId); state.position = index >= 0 ? index : 0; render(); }

  function shuffle() {
    state.order = state.data.map(card => card.id);
    for (let i = state.order.length - 1; i > 0; i -= 1) { const j = Math.floor(Math.random() * (i + 1)); [state.order[i], state.order[j]] = [state.order[j], state.order[i]]; }
    state.mode = "随机顺序"; state.position = 0; render();
  }

  function reviewUnknown() {
    if (!state.unknown.size) { el["study-message"].textContent = "目前没有标记为“不会”的词组。"; return; }
    state.order = [...state.unknown].sort((a, b) => a - b); state.mode = "只背不会"; state.position = 0; render();
  }

  function bindEvents() {
    el["study-card"].addEventListener("click", toggleAnswer); el["reveal-button"].addEventListener("click", toggleAnswer);
    el["previous-button"].addEventListener("click", () => move(-1)); el["next-button"].addEventListener("click", () => move(1));
    el["unknown-button"].addEventListener("click", () => mark("unknown")); el["known-button"].addEventListener("click", () => mark("known"));
    el["all-button"].addEventListener("click", () => showAll(currentCard()?.id || 1)); el["shuffle-button"].addEventListener("click", shuffle); el["review-button"].addEventListener("click", reviewUnknown);
    el["jump-form"].addEventListener("submit", event => { event.preventDefault(); const id = Number(el["jump-input"].value); if (!state.byId.has(id)) { el["study-message"].textContent = "请输入 1 到 357 之间的编号。"; return; } showAll(id); el["jump-input"].value = ""; });
    el["reset-button"].addEventListener("click", () => { if (!window.confirm("确定清除已掌握和需复习的全部记录吗？")) return; state.known.clear(); state.unknown.clear(); localStorage.removeItem(STORAGE_KEY); showAll(1); });
    document.addEventListener("keydown", event => { if (event.target.matches("input, textarea")) return; if (event.code === "Space") { event.preventDefault(); toggleAnswer(); } if (event.key === "ArrowLeft") move(-1); if (event.key === "ArrowRight") move(1); if (event.key === "1") mark("unknown"); if (event.key === "2") mark("known"); });
  }

  async function init() {
    ids.forEach(id => { el[id] = document.getElementById(id); }); bindEvents();
    try {
      const response = await fetch("data/vocabulary.json?v=20260919-2"); if (!response.ok) throw new Error(`HTTP ${response.status}`);
      state.data = await response.json(); state.byId = new Map(state.data.map(card => [card.id, card])); showAll(loadProgress());
    } catch (error) { el["progress-label"].textContent = "载入失败"; el["study-message"].textContent = "单词数据暂时无法载入，请刷新页面重试。"; console.error(error); }
  }

  init();
})();
