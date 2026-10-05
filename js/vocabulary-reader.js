(() => {
  document.body.classList.add("js-ready");

  const partOfSpeechPattern = /\s+((?:(?:n|v|vt|vi|adj|adv|prep|pron|conj|det|interj|phr|phrv|idm)\.(?:\s*,?\s*)?)+)$/i;
  document.querySelectorAll(".vocab-term").forEach(term => {
    if (term.querySelector(".vocab-pos")) return;
    const value = term.textContent.trim();
    const match = value.match(partOfSpeechPattern);
    if (!match) return;
    const headword = value.slice(0, match.index).trimEnd();
    const label = document.createElement("span");
    label.className = "vocab-pos";
    label.textContent = match[1].trim();
    term.replaceChildren(document.createTextNode(headword), document.createTextNode(" "), label);
  });

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
  let restoreTimer = 0;
  let restoringPosition = true;
  let latestPosition = null;

  if ("scrollRestoration" in history) history.scrollRestoration = "manual";

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
  const positionFromGroup = (group, readingLine) => {
    const bounds = group.getBoundingClientRect();
    return {
      groupId: group.id,
      progress: Math.max(0, Math.min(1, (readingLine - bounds.top) / Math.max(bounds.height, 1))),
      updatedAt: Date.now(),
    };
  };
  const currentReadingPosition = () => {
    const sheetBounds = sheet.getBoundingClientRect();
    const readingLine = Math.min(window.innerHeight - 1, Math.max(1, window.innerHeight * .38));
    const samplePoints = [.25, .75, .5];
    for (const ratio of samplePoints) {
      const x = Math.min(window.innerWidth - 1, Math.max(1, sheetBounds.left + sheetBounds.width * ratio));
      const group = document.elementsFromPoint(x, readingLine).map(element => element.closest?.(".vocab-group")).find(Boolean);
      if (group) return positionFromGroup(group, readingLine);
    }

    let nearestGroup = null;
    let nearestDistance = Number.POSITIVE_INFINITY;
    document.querySelectorAll(".vocab-group").forEach(group => {
      const bounds = group.getBoundingClientRect();
      if (bounds.bottom < 0 || bounds.top > window.innerHeight) return;
      const distance = readingLine < bounds.top
        ? bounds.top - readingLine
        : readingLine > bounds.bottom
          ? readingLine - bounds.bottom
          : 0;
      if (distance < nearestDistance) {
        nearestGroup = group;
        nearestDistance = distance;
      }
    });
    return nearestGroup ? positionFromGroup(nearestGroup, readingLine) : null;
  };
  const savePosition = () => {
    if (restoringPosition) return;
    const position = currentReadingPosition() || latestPosition;
    if (!position) return;
    latestPosition = position;
    void writePosition(position);
  };
  const schedulePositionSave = () => {
    if (restoringPosition) return;
    window.clearTimeout(saveTimer);
    saveTimer = window.setTimeout(savePosition, 240);
  };
  const restorePosition = async () => {
    window.clearTimeout(saveTimer);
    window.clearTimeout(restoreTimer);

    if (/^#group-\d{3}$/.test(window.location.hash)) {
      restoringPosition = false;
      restoreTimer = window.setTimeout(savePosition, 500);
      return;
    }

    const position = await readPosition();
    const target = position?.groupId ? document.getElementById(position.groupId) : null;
    if (!target) {
      restoringPosition = false;
      return;
    }
    latestPosition = position;

    const correctPosition = () => {
      target.scrollIntoView({ behavior: "auto", block: "start" });
      const bounds = target.getBoundingClientRect();
      const readingLine = window.innerHeight * .38;
      const progress = Math.max(0, Math.min(1, Number(position.progress) || 0));
      window.scrollBy({ top: bounds.top + bounds.height * progress - readingLine, behavior: "auto" });
    };

    try { await document.fonts?.ready; }
    catch (_) {}
    correctPosition();
    window.requestAnimationFrame(() => window.requestAnimationFrame(correctPosition));
    window.setTimeout(correctPosition, 180);
    restoreTimer = window.setTimeout(() => {
      correctPosition();
      restoringPosition = false;
      latestPosition = currentReadingPosition() || position;
      if (!manuallyHidden) {
        toolbar?.classList.remove("is-hidden");
        toolbar?.removeAttribute("inert");
        toolbar?.setAttribute("aria-hidden", "false");
      }
    }, 650);
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
