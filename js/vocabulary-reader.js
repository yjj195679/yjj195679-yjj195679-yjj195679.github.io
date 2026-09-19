(() => {
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
    document.getElementById(`group-${String(value).padStart(3, "0")}`)?.scrollIntoView({ behavior: "smooth", block: "start" });
  });
  input.addEventListener("input", () => input.setCustomValidity(""));
})();

