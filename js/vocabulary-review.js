(() => {
  const openButton = document.getElementById("review-open");
  const overlay = document.getElementById("review-overlay");
  const panel = overlay?.querySelector(".review-panel");
  const closeButton = document.getElementById("review-close");
  const progress = document.getElementById("review-progress");
  const score = document.getElementById("review-score");
  const term = document.getElementById("review-term");
  const reveal = document.getElementById("review-reveal");
  const definitionLabel = document.getElementById("review-definition-label");
  const definition = document.getElementById("review-definition");
  const choices = document.getElementById("review-choices");
  const afterActions = document.getElementById("review-after");
  const mistakeButton = document.getElementById("review-mistake");
  const nextButton = document.getElementById("review-next");
  const hint = document.getElementById("review-hint");
  const main = document.getElementById("main");
  if (!openButton || !overlay || !panel || !closeButton || !progress || !score || !term || !reveal || !definitionLabel || !definition || !choices || !afterActions || !mistakeButton || !nextButton || !hint) return;

  const words = [...document.querySelectorAll(".vocab-entry")].map((entry, index) => ({
    id: index,
    term: entry.querySelector(".vocab-term")?.textContent.trim() || "",
    definition: entry.querySelector(".vocab-definition")?.textContent.trim() || "",
  })).filter(word => word.term && word.definition);
  const storageKey = "tpm-vocabulary-review-v1";
  const emptyState = () => ({ total: words.length, index: 0, known: 0, unknown: 0, mistake: 0, revealed: false, answer: "" });
  let state = emptyState();
  let lastFocus = null;

  const readState = () => {
    try {
      const saved = JSON.parse(localStorage.getItem(storageKey));
      if (!saved || saved.total !== words.length) return emptyState();
      const index = Math.min(words.length, Math.max(0, Number(saved.index) || 0));
      return {
        total: words.length,
        index,
        known: Math.max(0, Number(saved.known) || 0),
        unknown: Math.max(0, Number(saved.unknown) || 0),
        mistake: Math.max(0, Number(saved.mistake) || 0),
        revealed: index < words.length && Boolean(saved.revealed),
        answer: ["known", "unknown", "mistake"].includes(saved.answer) ? saved.answer : "",
      };
    } catch {
      return emptyState();
    }
  };

  const saveState = () => {
    try { localStorage.setItem(storageKey, JSON.stringify(state)); }
    catch (_) {}
  };

  const render = () => {
    const finished = state.index >= words.length;
    score.textContent = `认识 ${state.known} · 不认识 ${state.unknown} · 记错 ${state.mistake}`;
    choices.hidden = finished || state.revealed;
    reveal.hidden = !state.revealed && !finished;
    afterActions.hidden = !state.revealed && !finished;
    afterActions.classList.toggle("is-single", finished);
    mistakeButton.hidden = finished;
    mistakeButton.disabled = state.answer === "mistake";
    mistakeButton.textContent = state.answer === "mistake" ? "已标记记错" : "记错了";
    nextButton.classList.remove("is-restart");

    if (finished) {
      progress.textContent = `${words.length} / ${words.length}`;
      term.textContent = "本轮完成";
      definitionLabel.textContent = "结果";
      definition.textContent = `认识 ${state.known} 个，不认识 ${state.unknown} 个，记错 ${state.mistake} 个`;
      reveal.hidden = false;
      nextButton.textContent = "重新开始";
      nextButton.classList.add("is-restart");
      hint.textContent = "结果已保存在当前设备";
      return;
    }

    const word = words[state.index];
    definitionLabel.textContent = "中文";
    progress.textContent = `${state.index + 1} / ${words.length}`;
    term.textContent = word.term;
    definition.textContent = word.definition;
    nextButton.textContent = state.index === words.length - 1 ? "查看结果" : "下一个";
    hint.textContent = !state.revealed
      ? "选择后显示中文释义"
      : (state.answer === "mistake" ? "已记录为记错了" : "释义已显示，可改记为“记错了”");
  };

  const openReview = () => {
    if (!words.length) {
      openButton.disabled = true;
      openButton.textContent = "暂无单词";
      return;
    }
    state = readState();
    lastFocus = document.activeElement instanceof HTMLElement ? document.activeElement : openButton;
    render();
    overlay.hidden = false;
    overlay.setAttribute("aria-hidden", "false");
    document.body.classList.add("review-open");
    if (main) main.inert = true;
    window.requestAnimationFrame(() => panel.focus({ preventScroll: true }));
  };

  const closeReview = () => {
    overlay.hidden = true;
    overlay.setAttribute("aria-hidden", "true");
    document.body.classList.remove("review-open");
    if (main) main.inert = false;
    if (lastFocus?.isConnected) lastFocus.focus({ preventScroll: true });
  };

  const answer = value => {
    if (state.revealed || state.index >= words.length) return;
    state[value] += 1;
    state.revealed = true;
    state.answer = value;
    saveState();
    render();
    window.requestAnimationFrame(() => nextButton.focus({ preventScroll: true }));
  };

  const markMistake = () => {
    if (!state.revealed || state.index >= words.length || state.answer === "mistake") return;
    if ((state.answer === "known" || state.answer === "unknown") && state[state.answer] > 0) state[state.answer] -= 1;
    state.mistake += 1;
    state.answer = "mistake";
    saveState();
    render();
    window.requestAnimationFrame(() => nextButton.focus({ preventScroll: true }));
  };

  const next = () => {
    if (state.index >= words.length) {
      state = emptyState();
    } else if (state.revealed) {
      state.index += 1;
      state.revealed = false;
      state.answer = "";
    } else {
      return;
    }
    saveState();
    render();
    window.requestAnimationFrame(() => {
      const firstChoice = choices.querySelector("[data-review-answer]");
      (state.index >= words.length ? nextButton : firstChoice)?.focus({ preventScroll: true });
    });
  };

  const keepFocusInside = event => {
    if (event.key !== "Tab") return;
    const focusable = [...panel.querySelectorAll('button:not([hidden]):not([disabled]), [href], [tabindex]:not([tabindex="-1"])')]
      .filter(element => element.getClientRects().length > 0);
    if (!focusable.length) return;
    const first = focusable[0];
    const last = focusable[focusable.length - 1];
    if (event.shiftKey && document.activeElement === first) {
      event.preventDefault();
      last.focus();
    } else if (!event.shiftKey && document.activeElement === last) {
      event.preventDefault();
      first.focus();
    }
  };

  openButton.addEventListener("click", openReview);
  closeButton.addEventListener("click", closeReview);
  overlay.querySelector("[data-review-close]")?.addEventListener("click", closeReview);
  choices.addEventListener("click", event => {
    const button = event.target.closest("[data-review-answer]");
    if (button) answer(button.dataset.reviewAnswer);
  });
  mistakeButton.addEventListener("click", markMistake);
  nextButton.addEventListener("click", next);
  panel.addEventListener("keydown", event => {
    if (event.key === "Escape") {
      event.preventDefault();
      closeReview();
      return;
    }
    if (!state.revealed && state.index < words.length && (event.key === "1" || event.key === "2")) {
      event.preventDefault();
      answer(event.key === "1" ? "known" : "unknown");
      return;
    }
    if (state.revealed && state.answer !== "mistake" && event.key === "3") {
      event.preventDefault();
      markMistake();
      return;
    }
    if (state.revealed && event.key === "Enter" && document.activeElement === nextButton) {
      event.preventDefault();
      next();
      return;
    }
    keepFocusInside(event);
  });
})();
