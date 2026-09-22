(() => {
  document.body.classList.add("js-ready");

  const toolbar = document.querySelector(".reader-toolbar");
  let manuallyHidden = false;
  if (toolbar) {
    const hideToolbar = document.getElementById("toolbar-hide");
    let lastY = window.scrollY;
    let direction = 0;
    let travel = 0;
    let framePending = false;
    const setToolbarHidden = hidden => {
      if (!hidden && manuallyHidden) return;
      if (hidden && toolbar.contains(document.activeElement) && document.activeElement instanceof HTMLElement) {
        document.activeElement.blur();
      }
      toolbar.classList.toggle("is-hidden", hidden);
      toolbar.toggleAttribute("inert", hidden);
      toolbar.setAttribute("aria-hidden", String(hidden));
    };
    hideToolbar?.addEventListener("click", () => {
      manuallyHidden = true;
      setToolbarHidden(true);
    });
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
    setToolbarHidden(false);
  }

  const sheet = document.querySelector(".reader-sheet");
  const smaller = document.getElementById("font-smaller");
  const reset = document.getElementById("font-reset");
  const larger = document.getElementById("font-larger");
  if (!sheet || !smaller || !reset || !larger) return;

  const positionKey = "vocabulary-reader-v1";
  const fallbackKey = "tpm-vocabulary-position";
  let databasePromise;
  let saveTimer = 0;
  let restoringPosition = false;

  const openPositionDatabase = () => {
    if (databasePromise) return databasePromise;
    databasePromise = new Promise((resolve, reject) => {
      const request = indexedDB.open("tpm-reading-progress", 1);
      request.onupgradeneeded = () => {
        const database = request.result;
        if (!database.objectStoreNames.contains("positions")) database.createObjectStore("positions", { keyPath: "key" });
      };
      request.onsuccess = () => resolve(request.result);
      request.onerror = () => reject(request.error);
    });
    return databasePromise;
  };
  const readPosition = async () => {
    try {
      const database = await openPositionDatabase();
      return await new Promise((resolve, reject) => {
        const request = database.transaction("positions", "readonly").objectStore("positions").get(positionKey);
        request.onsuccess = () => resolve(request.result || null);
        request.onerror = () => reject(request.error);
      });
    } catch (_) {
      try { return JSON.parse(localStorage.getItem(fallbackKey)) || null; }
      catch (_) { return null; }
    }
  };
  const writePosition = async position => {
    try {
      const database = await openPositionDatabase();
      await new Promise((resolve, reject) => {
        const transaction = database.transaction("positions", "readwrite");
        transaction.objectStore("positions").put({ key: positionKey, ...position });
        transaction.oncomplete = () => resolve();
        transaction.onerror = () => reject(transaction.error);
      });
    } catch (_) {
      try { localStorage.setItem(fallbackKey, JSON.stringify(position)); }
      catch (_) {}
    }
  };
  const currentReadingPosition = () => {
    const sheetBounds = sheet.getBoundingClientRect();
    const readingLine = Math.min(window.innerHeight - 1, Math.max(1, window.innerHeight * .38));
    const samplePoints = [.25, .75, .5];
    for (const ratio of samplePoints) {
      const x = Math.min(window.innerWidth - 1, Math.max(1, sheetBounds.left + sheetBounds.width * ratio));
      const group = document.elementsFromPoint(x, readingLine).map(element => element.closest?.(".vocab-group")).find(Boolean);
      if (!group) continue;
      const bounds = group.getBoundingClientRect();
      return {
        groupId: group.id,
        progress: Math.max(0, Math.min(1, (readingLine - bounds.top) / Math.max(bounds.height, 1))),
        updatedAt: Date.now(),
      };
    }
    return null;
  };
  const savePosition = () => {
    if (restoringPosition) return;
    const position = currentReadingPosition();
    if (position) void writePosition(position);
  };
  const schedulePositionSave = () => {
    window.clearTimeout(saveTimer);
    saveTimer = window.setTimeout(savePosition, 360);
  };
  const restorePosition = async () => {
    if (/^#group-\d{3}$/.test(window.location.hash)) return;
    const position = await readPosition();
    const target = position?.groupId ? document.getElementById(position.groupId) : null;
    if (!target) return;
    restoringPosition = true;
    target.scrollIntoView({ behavior: "auto", block: "start" });
    window.requestAnimationFrame(() => window.requestAnimationFrame(() => {
      const bounds = target.getBoundingClientRect();
      const readingLine = window.innerHeight * .38;
      const offset = bounds.top + bounds.height * Math.max(0, Math.min(1, Number(position.progress) || 0)) - readingLine;
      window.scrollBy({ top: offset, behavior: "auto" });
      restoringPosition = false;
      if (!manuallyHidden) {
        toolbar?.classList.remove("is-hidden");
        toolbar?.removeAttribute("inert");
        toolbar?.setAttribute("aria-hidden", "false");
      }
    }));
  };
  window.addEventListener("scroll", schedulePositionSave, { passive: true });
  window.addEventListener("pagehide", savePosition);
  document.addEventListener("visibilitychange", () => {
    if (document.visibilityState === "hidden") savePosition();
  });
  void restorePosition();

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
})();
