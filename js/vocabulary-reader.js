(() => {
  document.body.classList.add("js-ready");

  const clock = document.getElementById("clock");
  const updateClock = () => {
    if (!clock) return;
    clock.textContent = new Intl.DateTimeFormat("zh-CN", {
      hour: "2-digit",
      minute: "2-digit",
      hour12: false,
    }).format(new Date());
  };
  updateClock();
  if (clock) window.setInterval(updateClock, 60000);

  const menuButton = document.getElementById("menu-toggle");
  const nav = document.getElementById("site-nav");
  const closeMenu = () => {
    if (!menuButton || !nav) return;
    menuButton.setAttribute("aria-expanded", "false");
    menuButton.setAttribute("aria-label", "打开导航");
    nav.classList.remove("open");
    document.body.classList.remove("menu-open");
  };
  if (menuButton && nav) {
    menuButton.addEventListener("click", () => {
      const open = menuButton.getAttribute("aria-expanded") !== "true";
      closeMenu();
      if (!open) return;
      menuButton.setAttribute("aria-expanded", "true");
      menuButton.setAttribute("aria-label", "关闭导航");
      nav.classList.add("open");
      document.body.classList.add("menu-open");
    });
    nav.addEventListener("click", event => {
      if (event.target.closest("a")) closeMenu();
    });
    document.addEventListener("keydown", event => {
      if (event.key === "Escape") closeMenu();
    });
  }

  const toolbar = document.querySelector(".reader-toolbar");
  if (toolbar) {
    let lastY = window.scrollY;
    let direction = 0;
    let travel = 0;
    let framePending = false;
    const setToolbarHidden = hidden => {
      if (hidden && toolbar.contains(document.activeElement)) return;
      toolbar.classList.toggle("is-hidden", hidden);
      toolbar.toggleAttribute("inert", hidden);
      toolbar.setAttribute("aria-hidden", String(hidden));
    };
    const updateToolbar = () => {
      const currentY = Math.max(0, window.scrollY);
      const delta = currentY - lastY;
      const nextDirection = Math.sign(delta);
      if (currentY < 36) {
        setToolbarHidden(false);
        travel = 0;
      } else if (nextDirection) {
        if (nextDirection !== direction) travel = 0;
        travel += Math.abs(delta);
        if (travel >= 14) {
          setToolbarHidden(nextDirection > 0);
          travel = 0;
        }
        direction = nextDirection;
      }
      lastY = currentY;
      framePending = false;
    };
    window.addEventListener("scroll", () => {
      if (framePending) return;
      framePending = true;
      window.requestAnimationFrame(updateToolbar);
    }, { passive: true });
    toolbar.addEventListener("focusin", () => setToolbarHidden(false));
    setToolbarHidden(false);
  }

  const sheet = document.querySelector(".reader-sheet");
  const smaller = document.getElementById("font-smaller");
  const reset = document.getElementById("font-reset");
  const larger = document.getElementById("font-larger");
  const jump = document.getElementById("group-jump");
  const input = document.getElementById("group-number");
  if (!sheet || !smaller || !reset || !larger || !jump || !input) return;
  const storageKey = "tpm-vocabulary-font-scale";
  const clamp = value => Math.min(1.35, Math.max(.85, value));
  const readScale = () => {
    try { return clamp(Number(localStorage.getItem(storageKey)) || 1); }
    catch (_) { return 1; }
  };
  const applyScale = value => {
    const scale = clamp(Math.round(value * 10) / 10);
    sheet.style.setProperty("--reader-scale", String(scale));
    reset.textContent = scale === 1 ? "标准" : `${Math.round(scale * 100)}%`;
    try { localStorage.setItem(storageKey, String(scale)); }
    catch (_) {}
  };
  applyScale(readScale());
  smaller.addEventListener("click", () => applyScale(Number(getComputedStyle(sheet).getPropertyValue("--reader-scale")) - .1));
  larger.addEventListener("click", () => applyScale(Number(getComputedStyle(sheet).getPropertyValue("--reader-scale")) + .1));
  reset.addEventListener("click", () => applyScale(1));
  jump.addEventListener("submit", event => {
    event.preventDefault();
    const value = Number(input.value);
    if (!Number.isInteger(value) || value < 1 || value > 357) {
      input.setCustomValidity("请输入 1 到 357 之间的编号");
      input.reportValidity();
      return;
    }
    input.setCustomValidity("");
    const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    document.getElementById(`group-${String(value).padStart(3, "0")}`)?.scrollIntoView({ behavior: reducedMotion ? "auto" : "smooth", block: "start" });
  });
  input.addEventListener("input", () => input.setCustomValidity(""));
})();
