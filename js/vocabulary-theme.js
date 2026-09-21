(() => {
  const root = document.documentElement;
  const storageKey = "true-path-theme";
  const allowedModes = new Set(["system", "light", "dark"]);
  const systemTheme = window.matchMedia("(prefers-color-scheme: dark)");

  const readMode = () => {
    try {
      const stored = window.localStorage.getItem(storageKey);
      return allowedModes.has(stored) ? stored : "system";
    } catch {
      return "system";
    }
  };

  const applyTheme = () => {
    const mode = readMode();
    const theme = mode === "system" ? (systemTheme.matches ? "dark" : "light") : mode;
    root.dataset.themeMode = mode;
    root.dataset.theme = theme;
    root.style.colorScheme = theme;
    const themeColor = document.querySelector('meta[name="theme-color"]');
    if (themeColor) themeColor.content = theme === "dark" ? "#080a0f" : "#f4f7fb";
  };

  applyTheme();
  const handleSystemChange = () => {
    if (readMode() === "system") applyTheme();
  };
  if (typeof systemTheme.addEventListener === "function") systemTheme.addEventListener("change", handleSystemChange);
  else if (typeof systemTheme.addListener === "function") systemTheme.addListener(handleSystemChange);
  window.addEventListener("storage", event => {
    if (event.key === storageKey) applyTheme();
  });
})();
