
(() => {
  "use strict";
  const root = document.body;
  if (!root.classList.contains("writing-page")) return;
  const search = document.getElementById("writing-search");
  const kind = document.getElementById("writing-kind");
  const state = document.getElementById("writing-state");
  const priority = document.getElementById("writing-priority");
  const entries = [...document.querySelectorAll(".writing-entry")];
  const groups = [...document.querySelectorAll("[data-collection]")];
  const live = document.getElementById("writing-count");
  const empty = document.getElementById("writing-empty");
  const masteredCount = document.getElementById("writing-mastered-count");
  const testButton = document.getElementById("writing-test");
  const storageKey = "true-path-writing-vocab-v1";
  let marks = {};
  try {
    const stored = JSON.parse(localStorage.getItem(storageKey) || "{}");
    if (stored && typeof stored === "object" && !Array.isArray(stored)) marks = stored;
  } catch { marks = {}; }
  const valid = new Set(["mastered","review"]);
  function save() {
    try { localStorage.setItem(storageKey, JSON.stringify(marks)); } catch {}
  }
  function applyMark(entry) {
    const current = valid.has(marks[entry.id]) ? marks[entry.id] : "unmarked";
    entry.dataset.state = current;
    entry.querySelectorAll("[data-mark]").forEach(btn => {
      btn.setAttribute("aria-pressed", String(btn.dataset.mark === current));
    });
  }
  function update() {
    const query = search.value.trim().toLocaleLowerCase();
    let shown = 0;
    entries.forEach(entry => {
      const match = (!query || entry.textContent.toLocaleLowerCase().includes(query))
        && (!kind.value || entry.dataset.kind === kind.value)
        && (!state.value || entry.dataset.state === state.value)
        && (!priority.checked || entry.dataset.priority === "1");
      entry.hidden = !match;
      if (match) shown++;
    });
    groups.forEach(group => { group.hidden = !group.querySelector(".writing-entry:not([hidden])"); });
    empty.hidden = shown > 0;
    live.textContent = "显示 " + shown + " / " + entries.length + " 组";
    masteredCount.textContent = String(entries.filter(e => e.dataset.state === "mastered").length);
  }
  entries.forEach(applyMark);
  [search,kind,state,priority].forEach(control => control.addEventListener(control === search ? "input" : "change", update));
  document.querySelectorAll("[data-mark]").forEach(button => button.addEventListener("click", () => {
    const entry = button.closest(".writing-entry");
    const next = button.dataset.mark;
    if (marks[entry.id] === next) delete marks[entry.id];
    else marks[entry.id] = next;
    save();
    applyMark(entry);
    update();
  }));
  testButton.addEventListener("click", () => {
    const on = root.classList.toggle("is-testing");
    testButton.setAttribute("aria-pressed", String(on));
    testButton.textContent = on ? "显示中文 · 结束自测" : "隐藏中文 · 开始自测";
    entries.forEach(entry => {
      entry.classList.remove("is-revealed");
      const reveal = entry.querySelector(".writing-reveal");
      reveal.setAttribute("aria-pressed", "false");
      reveal.textContent = "查看释义";
    });
  });
  document.querySelectorAll(".writing-reveal").forEach(button => button.addEventListener("click", () => {
    const entry = button.closest(".writing-entry");
    const revealed = entry.classList.toggle("is-revealed");
    button.setAttribute("aria-pressed", String(revealed));
    button.textContent = revealed ? "隐藏释义" : "查看释义";
  }));
  document.getElementById("writing-random").addEventListener("click", () => {
    const visible = entries.filter(e => !e.hidden);
    if (!visible.length) { live.textContent = "没有可抽查的词条，请重置筛选"; return; }
    const card = visible[Math.floor(Math.random() * visible.length)];
    entries.forEach(e => e.classList.remove("is-picked"));
    card.classList.add("is-picked");
    if (root.classList.contains("is-testing")) {
      card.classList.remove("is-revealed");
      const reveal = card.querySelector(".writing-reveal");
      reveal.setAttribute("aria-pressed", "false");
      reveal.textContent = "查看释义";
    }
    card.scrollIntoView({behavior:window.matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto" : "smooth", block:"center"});
    card.focus({preventScroll:true});
    live.textContent = "已抽取：" + card.querySelector(".writing-term").textContent;
  });
  document.getElementById("writing-reset").addEventListener("click", () => {
    search.value = ""; kind.value = ""; state.value = ""; priority.checked = false;
    entries.forEach(e => e.classList.remove("is-picked"));
    update();
  });
  document.getElementById("writing-print").addEventListener("click", () => window.print());
  window.addEventListener("storage", event => {
    if (event.key !== storageKey) return;
    try {
      const parsed = JSON.parse(event.newValue || "{}");
      marks = parsed && typeof parsed === "object" && !Array.isArray(parsed) ? parsed : {};
    } catch { marks = {}; }
    entries.forEach(applyMark);
    update();
  });
  update();
})();
