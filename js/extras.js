(() => {
  const isEnglish = document.documentElement.lang.toLowerCase().startsWith("en");
  const originalTitle = document.title;
  const copy = isEnglish
    ? {
        start: "Start",
        pause: "Pause",
        ready: "Choose a duration and start the timer.",
        running: (mode) => `${mode} session in progress.`,
        paused: (mode) => `${mode} session paused.`,
        complete: (mode) => `${mode} session complete. Time to switch pace.`,
        quoteLoading: "Finding another line…",
        quoteRefresh: "Another line",
        quoteFallback: "The quote service is resting, so a saved line is shown instead.",
      }
    : {
        start: "开始",
        pause: "暂停",
        ready: "选择时长后开始计时。",
        running: (mode) => `${mode}计时进行中。`,
        paused: (mode) => `${mode}计时已暂停。`,
        complete: (mode) => `${mode}结束，可以切换一下节奏了。`,
        quoteLoading: "正在寻找另一句话……",
        quoteRefresh: "换一句",
        quoteFallback: "一言服务暂时休息，已显示本地收藏。",
      };

  const timer = document.querySelector("[data-focus-timer]");
  if (timer) {
    const value = timer.querySelector("#timer-value");
    const modeLabel = timer.querySelector("#timer-mode");
    const progress = timer.querySelector(".timer-progress");
    const progressFill = timer.querySelector(".timer-progress span");
    const toggle = timer.querySelector("#timer-toggle");
    const reset = timer.querySelector("#timer-reset");
    const status = timer.querySelector("#timer-status");
    const presets = [...timer.querySelectorAll("[data-minutes]")];

    let totalSeconds = 25 * 60;
    let remainingSeconds = totalSeconds;
    let deadline = 0;
    let interval = null;
    let running = false;

    const formatTime = (seconds) => {
      const minutes = Math.floor(seconds / 60);
      const rest = seconds % 60;
      return `${String(minutes).padStart(2, "0")}:${String(rest).padStart(2, "0")}`;
    };

    const renderTimer = () => {
      const formatted = formatTime(remainingSeconds);
      const percentage = Math.round((1 - remainingSeconds / totalSeconds) * 100);
      value.textContent = formatted;
      progressFill.style.transform = `scaleX(${Math.max(0, Math.min(percentage / 100, 1))})`;
      progress.setAttribute("aria-valuenow", String(percentage));
      if (running) document.title = `${formatted} · ${originalTitle}`;
    };

    const stopInterval = () => {
      if (interval) window.clearInterval(interval);
      interval = null;
    };

    const finishTimer = () => {
      running = false;
      stopInterval();
      toggle.textContent = copy.start;
      status.textContent = copy.complete(modeLabel.textContent);
      document.title = originalTitle;
      timer.classList.add("timer-complete");
      window.setTimeout(() => timer.classList.remove("timer-complete"), 1400);
    };

    const tick = () => {
      remainingSeconds = Math.max(0, Math.ceil((deadline - Date.now()) / 1000));
      renderTimer();
      if (remainingSeconds === 0) finishTimer();
    };

    toggle.addEventListener("click", () => {
      if (running) {
        running = false;
        remainingSeconds = Math.max(0, Math.ceil((deadline - Date.now()) / 1000));
        stopInterval();
        toggle.textContent = copy.start;
        status.textContent = copy.paused(modeLabel.textContent);
        document.title = originalTitle;
        renderTimer();
        return;
      }
      if (remainingSeconds === 0) remainingSeconds = totalSeconds;
      running = true;
      deadline = Date.now() + remainingSeconds * 1000;
      toggle.textContent = copy.pause;
      status.textContent = copy.running(modeLabel.textContent);
      tick();
      interval = window.setInterval(tick, 250);
    });

    const resetTimer = () => {
      running = false;
      stopInterval();
      remainingSeconds = totalSeconds;
      toggle.textContent = copy.start;
      status.textContent = copy.ready;
      document.title = originalTitle;
      renderTimer();
    };

    reset.addEventListener("click", resetTimer);
    presets.forEach((preset) => {
      preset.addEventListener("click", () => {
        totalSeconds = Number(preset.dataset.minutes) * 60;
        modeLabel.textContent = preset.dataset.mode;
        presets.forEach((item) => item.classList.toggle("selected", item === preset));
        resetTimer();
      });
    });

    renderTimer();
  }

  const quoteTool = document.querySelector("[data-quote-tool]");
  if (quoteTool) {
    const text = quoteTool.querySelector("#quote-text");
    const source = quoteTool.querySelector("#quote-source");
    const refresh = quoteTool.querySelector("#quote-refresh");
    const credit = quoteTool.querySelector("#quote-credit");
    const cacheKey = "true-path-hitokoto";
    const fallbacks = [
      { hitokoto: "知之为知之，不知为不知，是知也。", from: "《论语》", from_who: "孔子" },
      { hitokoto: "纸上得来终觉浅，绝知此事要躬行。", from: "《冬夜读书示子聿》", from_who: "陆游" },
      { hitokoto: "路漫漫其修远兮，吾将上下而求索。", from: "《离骚》", from_who: "屈原" },
    ];

    const renderQuote = (data, fallback = false) => {
      text.textContent = data.hitokoto;
      const attribution = [data.from_who, data.from].filter(Boolean).join(" · ");
      source.textContent = attribution ? `— ${attribution}` : "— 一言";
      if (data.uuid && !fallback) {
        credit.href = `https://hitokoto.cn?uuid=${encodeURIComponent(data.uuid)}`;
        credit.hidden = false;
      } else {
        credit.href = "https://hitokoto.cn/";
        credit.hidden = false;
      }
      quoteTool.dataset.state = fallback ? "fallback" : "ready";
    };

    const readCache = () => {
      try {
        const cached = JSON.parse(window.sessionStorage.getItem(cacheKey) || "null");
        return cached && cached.hitokoto ? cached : null;
      } catch {
        return null;
      }
    };

    const loadQuote = async (force = false) => {
      const cached = readCache();
      if (cached && !force) {
        renderQuote(cached);
        return;
      }

      refresh.disabled = true;
      refresh.textContent = copy.quoteLoading;
      quoteTool.dataset.state = "loading";
      const controller = new AbortController();
      const timeout = window.setTimeout(() => controller.abort(), 8000);
      try {
        const response = await fetch(
          "https://v1.hitokoto.cn/?c=d&c=i&c=k&encode=json&max_length=55",
          { headers: { Accept: "application/json" }, signal: controller.signal },
        );
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        const data = await response.json();
        if (!data.hitokoto) throw new Error("Empty quote");
        renderQuote(data);
        try {
          window.sessionStorage.setItem(cacheKey, JSON.stringify(data));
        } catch {
          // Session caching is an optimization; the quote is already available.
        }
      } catch {
        const fallback = fallbacks[Math.floor(Math.random() * fallbacks.length)];
        renderQuote(fallback, true);
        source.textContent += ` · ${copy.quoteFallback}`;
      } finally {
        window.clearTimeout(timeout);
        refresh.disabled = false;
        refresh.textContent = copy.quoteRefresh;
      }
    };

    refresh.addEventListener("click", () => loadQuote(true));
    loadQuote();
  }
})();
