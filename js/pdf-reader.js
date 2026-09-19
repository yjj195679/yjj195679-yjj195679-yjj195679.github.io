(() => {
  const button = document.getElementById("page-width-toggle");
  if (!button) return;
  const storageKey = "tpm-pdf-fit-pages";
  const isMobile = () => window.matchMedia("(max-width: 760px)").matches;
  const readPreference = () => {
    try { return window.localStorage.getItem(storageKey) === "true"; }
    catch (_) { return false; }
  };
  const apply = (fit) => {
    document.body.classList.toggle("fit-pdf-pages", fit);
    button.setAttribute("aria-pressed", String(fit));
    button.textContent = fit ? "阅读宽度" : "整页显示";
  };
  apply(isMobile() ? readPreference() : true);
  button.addEventListener("click", () => {
    const fit = !document.body.classList.contains("fit-pdf-pages");
    apply(fit);
    try { window.localStorage.setItem(storageKey, String(fit)); }
    catch (_) {}
  });
})();

