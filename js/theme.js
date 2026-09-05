(() => {
  const storageKey = "true-path-theme";
  const allowedModes = new Set(["system", "light", "dark"]);
  const root = document.documentElement;
  const systemTheme = window.matchMedia("(prefers-color-scheme: dark)");

  const getStoredMode = () => {
    try {
      const value = window.localStorage.getItem(storageKey);
      return allowedModes.has(value) ? value : "system";
    } catch {
      return "system";
    }
  };

  const resolvedTheme = (mode) => (mode === "system" ? (systemTheme.matches ? "dark" : "light") : mode);

  const applyTheme = (mode, persist = false) => {
    const safeMode = allowedModes.has(mode) ? mode : "system";
    const theme = resolvedTheme(safeMode);
    root.dataset.themeMode = safeMode;
    root.dataset.theme = theme;
    root.style.colorScheme = theme;

    const themeColor = document.querySelector('meta[name="theme-color"]');
    if (themeColor) themeColor.content = theme === "dark" ? "#080a0f" : "#f4f7fb";

    if (persist) {
      try {
        window.localStorage.setItem(storageKey, safeMode);
      } catch {
        // The preference still works for this page if storage is unavailable.
      }
    }

    window.dispatchEvent(new CustomEvent("themechange", { detail: { mode: safeMode, theme } }));
  };

  applyTheme(getStoredMode());

  const handleSystemThemeChange = () => {
    if (root.dataset.themeMode === "system") applyTheme("system");
  };
  if (typeof systemTheme.addEventListener === "function") systemTheme.addEventListener("change", handleSystemThemeChange);
  else if (typeof systemTheme.addListener === "function") systemTheme.addListener(handleSystemThemeChange);

  const icons = {
    system: '<svg viewBox="0 0 20 20" aria-hidden="true"><rect x="2.5" y="3.5" width="15" height="10.5" rx="2"></rect><path d="M7 17h6M10 14v3"></path></svg>',
    light: '<svg viewBox="0 0 20 20" aria-hidden="true"><circle cx="10" cy="10" r="3.2"></circle><path d="M10 1.7v2M10 16.3v2M1.7 10h2M16.3 10h2M4.1 4.1l1.4 1.4M14.5 14.5l1.4 1.4M15.9 4.1l-1.4 1.4M5.5 14.5l-1.4 1.4"></path></svg>',
    dark: '<svg viewBox="0 0 20 20" aria-hidden="true"><path d="M16.7 12.6A7 7 0 0 1 7.4 3.3 7 7 0 1 0 16.7 12.6Z"></path></svg>',
  };

  const initControl = () => {
    const isEnglish = root.lang.toLowerCase().startsWith("en");
    const labels = isEnglish
      ? { title: "Appearance", system: "System", light: "Light", dark: "Dark", follows: "Follows device settings" }
      : { title: "外观模式", system: "跟随系统", light: "浅色", dark: "深色", follows: "随设备明暗设置自动切换" };
    const switcher = document.createElement("div");
    switcher.className = "theme-switcher";
    switcher.innerHTML = `
      <button class="theme-toggle" type="button" aria-label="${labels.title}" aria-haspopup="true" aria-expanded="false"></button>
      <div class="theme-menu" role="radiogroup" aria-label="${labels.title}" hidden>
        <div class="theme-menu-head"><strong>${labels.title}</strong><span>${labels.follows}</span></div>
        ${["system", "light", "dark"].map((mode) => `
          <button type="button" role="radio" data-theme-choice="${mode}" aria-checked="false">
            <span class="theme-option-icon">${icons[mode]}</span><span>${labels[mode]}</span><span class="theme-check" aria-hidden="true">✓</span>
          </button>`).join("")}
      </div>`;

    const tools = document.querySelector(".topbar-tools");
    if (tools) {
      const menuToggle = tools.querySelector(".menu-toggle");
      tools.insertBefore(switcher, menuToggle || null);
    } else {
      switcher.classList.add("standalone-theme-switcher");
      document.body.append(switcher);
    }

    const toggle = switcher.querySelector(".theme-toggle");
    const menu = switcher.querySelector(".theme-menu");
    const choices = [...switcher.querySelectorAll("[data-theme-choice]")];

    const syncControl = () => {
      const mode = root.dataset.themeMode || "system";
      toggle.innerHTML = icons[mode];
      toggle.title = `${labels.title}：${labels[mode]}`;
      toggle.setAttribute("aria-label", `${labels.title}：${labels[mode]}`);
      choices.forEach((choice) => choice.setAttribute("aria-checked", String(choice.dataset.themeChoice === mode)));
    };
    const closeMenu = (restoreFocus = false) => {
      menu.hidden = true;
      toggle.setAttribute("aria-expanded", "false");
      if (restoreFocus) toggle.focus();
    };
    const openMenu = () => {
      menu.hidden = false;
      toggle.setAttribute("aria-expanded", "true");
      const selected = choices.find((choice) => choice.getAttribute("aria-checked") === "true");
      window.requestAnimationFrame(() => (selected || choices[0]).focus());
    };

    toggle.addEventListener("click", () => (menu.hidden ? openMenu() : closeMenu()));
    choices.forEach((choice) => choice.addEventListener("click", () => {
      applyTheme(choice.dataset.themeChoice, true);
      syncControl();
      closeMenu(true);
    }));
    switcher.addEventListener("keydown", (event) => {
      if (event.key === "Escape") closeMenu(true);
      if (!menu.hidden && ["ArrowDown", "ArrowUp"].includes(event.key)) {
        event.preventDefault();
        const index = choices.indexOf(document.activeElement);
        const step = event.key === "ArrowDown" ? 1 : -1;
        choices[(index + step + choices.length) % choices.length].focus();
      }
    });
    document.addEventListener("pointerdown", (event) => {
      if (!menu.hidden && !switcher.contains(event.target)) closeMenu();
    });
    window.addEventListener("themechange", syncControl);
    syncControl();
  };

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", initControl, { once: true });
  else initControl();
})();
