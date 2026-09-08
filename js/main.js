(() => {
  const select = (selector, root = document) => root.querySelector(selector);
  const selectAll = (selector, root = document) => [...root.querySelectorAll(selector)];
  document.body.classList.add("js-ready");

  const isEnglish = document.documentElement.lang.toLowerCase().startsWith("en");
  const locale = isEnglish ? "en-US" : "zh-CN";
  const copy = isEnglish
    ? {
        openMenu: "Open menu",
        closeMenu: "Close menu",
        geolocationUnsupported: "Geolocation is not supported by this browser.",
        locating: "Locating…",
        awaitingPermission: "Waiting for location permission",
        weatherUnavailable: "Weather service is temporarily unavailable.",
        weatherTimeout: "Weather request timed out. Please try again.",
        noWeatherData: "No weather data was returned.",
        weatherUpdating: "Weather updating",
        relocate: "Update location",
        unavailable: "Unavailable",
        denied: "Location permission was not granted.",
        retry: "Try again",
        sectionNav: "On this page",
        openSectionNav: "Open section navigation",
        closeSectionNav: "Close section navigation",
        backToTop: "Back to top",
        search: "Quick navigation",
        searchPlaceholder: "Search pages and projects…",
        searchHint: "Type to filter · ↑↓ to select · Enter to open",
        closeSearch: "Close quick navigation",
        noResults: "No matching pages.",
        readingMode: "Reading mode",
        exitReadingMode: "Exit reading mode",
        copyLink: "Copy link",
        linkCopied: "Link copied",
        copyFailed: "Copy failed",
        printPage: "Print / save PDF",
        readingMeta: (sections, minutes) => `${sections} sections · about ${minutes} min read`,
        sectionLink: "Link to this section",
        weatherDetails: (current) =>
          `Feels like ${Math.round(current.apparent_temperature)}°C · Humidity ${current.relative_humidity_2m}% · Wind ${Math.round(current.wind_speed_10m)} km/h`,
      }
    : {
        openMenu: "打开导航",
        closeMenu: "关闭导航",
        geolocationUnsupported: "当前浏览器不支持定位",
        locating: "正在获取…",
        awaitingPermission: "等待浏览器定位授权",
        weatherUnavailable: "天气服务暂时不可用",
        weatherTimeout: "天气请求超时，请再次尝试",
        noWeatherData: "未获取到天气数据",
        weatherUpdating: "天气更新中",
        relocate: "重新定位",
        unavailable: "暂时无法显示",
        denied: "你没有授权定位",
        retry: "再次尝试",
        sectionNav: "本页导航",
        openSectionNav: "展开本页导航",
        closeSectionNav: "收起本页导航",
        backToTop: "返回顶部",
        search: "快捷导航",
        searchPlaceholder: "搜索页面、项目或知识方向…",
        searchHint: "输入筛选 · ↑↓ 选择 · 回车打开",
        closeSearch: "关闭快捷导航",
        noResults: "没有匹配的页面。",
        readingMode: "阅读模式",
        exitReadingMode: "退出阅读",
        copyLink: "复制链接",
        linkCopied: "链接已复制",
        copyFailed: "复制失败",
        printPage: "打印 / 保存 PDF",
        readingMeta: (sections, minutes) => `${sections} 个章节 · 约 ${minutes} 分钟阅读`,
        sectionLink: "链接到本章节",
        weatherDetails: (current) =>
          `体感 ${Math.round(current.apparent_temperature)}°C　湿度 ${current.relative_humidity_2m}%　风速 ${Math.round(current.wind_speed_10m)} km/h`,
      };

  const year = select("#year");
  if (year) year.textContent = String(new Date().getFullYear());

  const heroDate = select("#hero-date");
  if (heroDate) {
    const now = new Date();
    heroDate.dateTime = now.toISOString().slice(0, 10);
    heroDate.textContent = new Intl.DateTimeFormat(locale, {
      month: "short",
      day: "numeric",
      weekday: "short",
    }).format(now);
  }

  const clock = select("#clock");
  const updateClock = () => {
    if (!clock) return;
    clock.textContent = new Intl.DateTimeFormat(locale, {
      hour: "2-digit",
      minute: "2-digit",
      second: "2-digit",
      hour12: false,
    }).format(new Date());
  };
  updateClock();
  if (clock) window.setInterval(updateClock, 1000);

  const menuButton = select("#menu-toggle");
  const nav = select("#site-nav");
  const closeMenu = ({ restoreFocus = false } = {}) => {
    if (!menuButton || !nav) return;
    menuButton.setAttribute("aria-expanded", "false");
    menuButton.setAttribute("aria-label", copy.openMenu);
    nav.classList.remove("open");
    document.body.classList.remove("menu-open");
    if (restoreFocus) menuButton.focus();
  };

  if (menuButton && nav) {
    menuButton.addEventListener("click", (event) => {
      const isOpen = menuButton.getAttribute("aria-expanded") === "true";
      if (isOpen) {
        closeMenu();
        return;
      }
      menuButton.setAttribute("aria-expanded", "true");
      menuButton.setAttribute("aria-label", copy.closeMenu);
      nav.classList.add("open");
      document.body.classList.add("menu-open");
      window.dispatchEvent(new CustomEvent("ui-overlay-open", { detail: { source: "navigation" } }));
      if (event.detail === 0) {
        window.requestAnimationFrame(() => select("a", nav)?.focus());
      }
    });
    selectAll("a", nav).forEach((link) => link.addEventListener("click", closeMenu));
    document.addEventListener("pointerdown", (event) => {
      const isOpen = menuButton.getAttribute("aria-expanded") === "true";
      if (isOpen && !nav.contains(event.target) && !menuButton.contains(event.target)) closeMenu();
    });
    window.addEventListener("resize", () => {
      if (window.innerWidth > 1199) closeMenu();
    });
    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape" && menuButton.getAttribute("aria-expanded") === "true") {
        closeMenu({ restoreFocus: true });
      } else if (event.key === "Tab" && menuButton.getAttribute("aria-expanded") === "true") {
        const focusable = [menuButton, ...selectAll("a", nav)];
        const current = Math.max(0, focusable.indexOf(document.activeElement));
        const step = event.shiftKey ? -1 : 1;
        event.preventDefault();
        focusable[(current + step + focusable.length) % focusable.length].focus();
      }
    });
    window.addEventListener("ui-overlay-open", (event) => {
      if (event.detail?.source !== "navigation") closeMenu();
    });
  }

  const revealItems = selectAll(".reveal");
  revealItems.forEach((item) => {
    const siblings = selectAll(".reveal", item.parentElement);
    const index = siblings.indexOf(item);
    item.style.setProperty("--reveal-delay", `${Math.min(index * 65, 260)}ms`);
  });
  if ("IntersectionObserver" in window) {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;
          entry.target.classList.add("visible");
          observer.unobserve(entry.target);
        });
      },
      { threshold: 0.1, rootMargin: "0px 0px -30px" },
    );
    revealItems.forEach((item) => observer.observe(item));
  } else {
    revealItems.forEach((item) => item.classList.add("visible"));
  }

  const background = select(".site-bg");
  const topbar = select(".topbar");
  const progress = document.createElement("div");
  progress.className = "scroll-progress";
  progress.setAttribute("aria-hidden", "true");
  document.body.prepend(progress);

  const backToTop = document.createElement("button");
  backToTop.className = "back-to-top";
  backToTop.type = "button";
  backToTop.setAttribute("aria-label", copy.backToTop);
  backToTop.title = copy.backToTop;
  backToTop.innerHTML = '<svg class="icon icon-arrow-up" viewBox="0 0 20 20" aria-hidden="true" focusable="false"><path d="M10 16V5"></path><path d="m6 9 4-4 4 4"></path></svg>';
  document.body.append(backToTop);
  const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
  const allowParallax = window.matchMedia("(prefers-reduced-motion: no-preference) and (min-width: 641px)");

  backToTop.addEventListener("click", () => {
    window.scrollTo({ top: 0, behavior: reducedMotion.matches ? "auto" : "smooth" });
  });
  let framePending = false;
  const updateScrollEffects = () => {
    if (framePending) return;
    framePending = true;
    window.requestAnimationFrame(() => {
      const maxScroll = Math.max(document.documentElement.scrollHeight - window.innerHeight, 1);
      progress.style.transform = `scaleX(${Math.max(0, Math.min(window.scrollY / maxScroll, 1))})`;
      if (topbar) topbar.classList.toggle("is-scrolled", window.scrollY > 24);
      backToTop.classList.toggle("visible", window.scrollY > Math.max(window.innerHeight * 0.75, 520));
      if (background && allowParallax.matches) {
        const offset = Math.min(window.scrollY * 0.028, 22);
        background.style.transform = `translateY(${offset}px) scale(1.025)`;
      } else if (background) {
        background.style.removeProperty("transform");
      }
      framePending = false;
    });
  };
  updateScrollEffects();
  window.addEventListener("scroll", updateScrollEffects, { passive: true });
  window.addEventListener("resize", updateScrollEffects, { passive: true });

  const finePointer = window.matchMedia("(hover: hover) and (pointer: fine)");
  if (finePointer.matches && !reducedMotion.matches) {
    selectAll(".glass").forEach((surface) => {
      surface.classList.add("interactive-surface");
      surface.addEventListener("pointermove", (event) => {
        const bounds = surface.getBoundingClientRect();
        surface.style.setProperty("--pointer-x", `${event.clientX - bounds.left}px`);
        surface.style.setProperty("--pointer-y", `${event.clientY - bounds.top}px`);
      });
      surface.addEventListener("pointerleave", () => {
        surface.style.removeProperty("--pointer-x");
        surface.style.removeProperty("--pointer-y");
      });
    });
  }

  const main = select("#main");
  const page = document.body.dataset.page || "page";
  const pageSections = main
    ? [...main.children].filter(
        (element) => element.classList.contains("section") && element.id && !select(".contact-card", element),
      )
    : [];

  pageSections.forEach((section) => {
    const heading = select(".section-head h2, .section-head h3", section);
    if (!heading || select(".section-anchor", heading)) return;
    const anchor = document.createElement("a");
    anchor.className = "section-anchor";
    anchor.href = `#${section.id}`;
    anchor.setAttribute("aria-label", `${copy.sectionLink}: ${heading.textContent.trim()}`);
    anchor.title = copy.sectionLink;
    anchor.textContent = "#";
    heading.append(anchor);
  });

  const documentPages = new Set(["projects", "education", "study", "achievements", "life"]);
  const subheroCard = select(".subhero-card");
  if (documentPages.has(page) && subheroCard) {
    const mainText = main ? main.innerText : "";
    const cjkCharacters = (mainText.match(/[\u3400-\u9fff]/g) || []).length;
    const latinWords = (mainText.match(/[A-Za-z0-9]+(?:['’-][A-Za-z0-9]+)*/g) || []).length;
    const readingMinutes = Math.max(1, Math.ceil(cjkCharacters / 350 + latinWords / 220));
    const pageTools = document.createElement("div");
    pageTools.className = "page-tools";
    pageTools.setAttribute("aria-label", isEnglish ? "Document tools" : "文档工具");
    pageTools.innerHTML = `
      <span class="page-reading-meta">${copy.readingMeta(pageSections.length, readingMinutes)}</span>
      <button class="page-tool" type="button" data-page-tool="reading" aria-pressed="false">
        <svg class="icon" viewBox="0 0 20 20" aria-hidden="true" focusable="false"><path d="M3.5 4.5c2.5-.7 4.7-.2 6.5 1.2v10c-1.8-1.4-4-1.9-6.5-1.2z"></path><path d="M16.5 4.5c-2.5-.7-4.7-.2-6.5 1.2v10c1.8-1.4 4-1.9 6.5-1.2z"></path></svg>
        <span>${copy.readingMode}</span>
      </button>
      <button class="page-tool" type="button" data-page-tool="copy">
        <svg class="icon" viewBox="0 0 20 20" aria-hidden="true" focusable="false"><path d="M8 12 12 8"></path><path d="M6.5 13.5 5 15a3 3 0 0 1-4-4l3-3a3 3 0 0 1 4.2 0"></path><path d="m13.5 6.5 1.5-1.5a3 3 0 0 1 4 4l-3 3a3 3 0 0 1-4.2 0"></path></svg>
        <span>${copy.copyLink}</span>
      </button>
      <button class="page-tool" type="button" data-page-tool="print">
        <svg class="icon" viewBox="0 0 20 20" aria-hidden="true" focusable="false"><path d="M5 7V3h10v4"></path><path d="M5 14H3V8h14v6h-2"></path><path d="M5 11h10v6H5z"></path></svg>
        <span>${copy.printPage}</span>
      </button>
      <span class="page-tool-status" role="status" aria-live="polite"></span>`;
    subheroCard.append(pageTools);

    const readingButton = select('[data-page-tool="reading"]', pageTools);
    const copyButton = select('[data-page-tool="copy"]', pageTools);
    const printButton = select('[data-page-tool="print"]', pageTools);
    const toolStatus = select(".page-tool-status", pageTools);
    let statusTimer = 0;
    const showToolStatus = (message) => {
      window.clearTimeout(statusTimer);
      toolStatus.textContent = message;
      statusTimer = window.setTimeout(() => {
        toolStatus.textContent = "";
      }, 2400);
    };

    const readingStorageKey = "true-path-reading-mode";
    const setReadingMode = (enabled) => {
      document.body.classList.toggle("reading-mode", enabled);
      readingButton.setAttribute("aria-pressed", String(enabled));
      select("span", readingButton).textContent = enabled ? copy.exitReadingMode : copy.readingMode;
    };
    try {
      setReadingMode(window.localStorage.getItem(readingStorageKey) === "true");
    } catch {
      setReadingMode(false);
    }

    readingButton.addEventListener("click", () => {
      const enabled = !document.body.classList.contains("reading-mode");
      setReadingMode(enabled);
      try {
        window.localStorage.setItem(readingStorageKey, String(enabled));
      } catch {
        // Reading mode still works when storage is unavailable.
      }
    });

    copyButton.addEventListener("click", async () => {
      try {
        await navigator.clipboard.writeText(window.location.href);
        showToolStatus(copy.linkCopied);
      } catch {
        const helper = document.createElement("textarea");
        helper.value = window.location.href;
        helper.setAttribute("readonly", "");
        helper.style.position = "fixed";
        helper.style.opacity = "0";
        document.body.append(helper);
        helper.select();
        const copied = document.execCommand("copy");
        helper.remove();
        showToolStatus(copied ? copy.linkCopied : copy.copyFailed);
      }
    });

    printButton.addEventListener("click", () => window.print());
  }

  if (page !== "home" && pageSections.length >= 2) {
    const sectionNav = document.createElement("nav");
    sectionNav.className = "section-nav";
    sectionNav.setAttribute("aria-label", copy.sectionNav);

    const navInner = document.createElement("div");
    navInner.className = "section-nav-inner";
    const navLabel = document.createElement("span");
    navLabel.className = "section-nav-label";
    navLabel.textContent = copy.sectionNav;
    navInner.append(navLabel);

    const navToggle = document.createElement("button");
    navToggle.className = "section-nav-toggle";
    navToggle.type = "button";
    navToggle.setAttribute("aria-expanded", "false");
    navToggle.setAttribute("aria-label", copy.openSectionNav);
    const navToggleLabel = document.createElement("span");
    const navToggleIcon = document.createElement("span");
    navToggleIcon.className = "section-nav-chevron";
    navToggleIcon.setAttribute("aria-hidden", "true");
    navToggle.append(navToggleLabel, navToggleIcon);
    navInner.append(navToggle);

    const navLinks = document.createElement("div");
    navLinks.className = "section-nav-links";
    navLinks.id = `section-nav-links-${page}`;
    navToggle.setAttribute("aria-controls", navLinks.id);

    const links = pageSections.map((section, index) => {
      const heading = select("h2, h3", section);
      const link = document.createElement("a");
      link.href = `#${section.id}`;
      const label = heading ? heading.textContent.replace("#", "").trim() : `${copy.sectionNav} ${index + 1}`;
      const marker = document.createElement("span");
      marker.setAttribute("aria-hidden", "true");
      link.append(marker, document.createTextNode(label));
      navLinks.append(link);
      return link;
    });
    navInner.append(navLinks);

    sectionNav.append(navInner);
    main.prepend(sectionNav);

    const setActiveSection = (id) => {
      links.forEach((link) => {
        const isActive = link.hash === `#${id}`;
        if (isActive) {
          link.setAttribute("aria-current", "location");
          navToggleLabel.textContent = link.textContent.trim();
          link.scrollIntoView({ block: "nearest", inline: "nearest" });
        } else link.removeAttribute("aria-current");
      });
    };
    setActiveSection(pageSections[0].id);

    const closeSectionNav = () => {
      navInner.classList.remove("open");
      navToggle.setAttribute("aria-expanded", "false");
      navToggle.setAttribute("aria-label", copy.openSectionNav);
    };
    navToggle.addEventListener("click", () => {
      const open = navToggle.getAttribute("aria-expanded") === "true";
      if (!open) window.dispatchEvent(new CustomEvent("ui-overlay-open", { detail: { source: "section-navigation" } }));
      navInner.classList.toggle("open", !open);
      navToggle.setAttribute("aria-expanded", String(!open));
      navToggle.setAttribute("aria-label", open ? copy.openSectionNav : copy.closeSectionNav);
    });
    window.addEventListener("ui-overlay-open", (event) => {
      if (event.detail?.source !== "section-navigation") closeSectionNav();
    });
    links.forEach((link) => {
      link.addEventListener("click", () => {
        closeSectionNav();
        const target = document.getElementById(decodeURIComponent(link.hash.slice(1)));
        const heading = target && select("h2, h3", target);
        if (heading) {
          heading.tabIndex = -1;
          window.setTimeout(() => heading.focus({ preventScroll: true }), 420);
        }
      });
    });

    if ("IntersectionObserver" in window) {
      const sectionObserver = new IntersectionObserver(
        (entries) => {
          const visible = entries
            .filter((entry) => entry.isIntersecting)
            .sort((a, b) => a.boundingClientRect.top - b.boundingClientRect.top);
          if (visible[0]) setActiveSection(visible[0].target.id);
        },
        { rootMargin: "-24% 0px -62%", threshold: 0 },
      );
      pageSections.forEach((section) => sectionObserver.observe(section));
    }
  }

  const prefetched = new Set();
  const prefetchPage = (link) => {
    if (!link || link.origin !== window.location.origin || link.pathname === window.location.pathname) return;
    const href = link.href.split("#")[0];
    if (!href || prefetched.has(href)) return;
    const hint = document.createElement("link");
    hint.rel = "prefetch";
    hint.href = href;
    document.head.append(hint);
    prefetched.add(href);
  };
  document.addEventListener("pointerover", (event) => prefetchPage(event.target.closest?.("a")), { passive: true });
  document.addEventListener("focusin", (event) => prefetchPage(event.target.closest?.("a")));

  const topbarTools = select(".topbar-tools");
  if (topbarTools) {
    const searchItems = isEnglish
      ? [
          ["Home", "Identity and direction", "index.html", "profile about"],
          ["Projects", "Question, process, and result", "projects.html", "portfolio work"],
          ["Project 01", "Reserved project space", "projects.html#project-1", "context method result review"],
          ["Project 02", "Reserved project space", "projects.html#project-2", "project"],
          ["Project 03", "Reserved project space", "projects.html#project-3", "project"],
          ["Method", "Define, develop, and verify", "education.html", "reason test review"],
          ["Study", "Understand, connect, and apply", "courses.html", "learning notes"],
          ["Results", "Completion, evidence, and reflection", "achievements.html", "outcomes"],
          ["Life", "Days, interests, and moments", "life.html", "daily interests"],
          ["Guestbook", "Public messages", "guestbook.html", "contact feedback"],
          ["GitHub", "Code and repositories", "https://github.com/yjj195679", "source code"],
        ]
      : [
          ["首页", "认识与方向", "index.html", "个人 关于"],
          ["项目", "问题、过程与结果", "projects.html", "实践 作品"],
          ["项目一", "预留项目位置", "projects.html#project-1", "背景 方法 结果 复盘"],
          ["项目二", "预留项目位置", "projects.html#project-2", "项目"],
          ["项目三", "预留项目位置", "projects.html#project-3", "项目"],
          ["方法", "定义、推演与验证", "education.html", "思路 检验 复盘"],
          ["学习", "理解、联结与应用", "courses.html", "学习 笔记"],
          ["成果", "完成、证据与反思", "achievements.html", "结果"],
          ["生活", "日常、兴趣与片段", "life.html", "记录"],
          ["留言板", "公开留言", "guestbook.html", "联系 反馈"],
          ["GitHub", "代码与仓库", "https://github.com/yjj195679", "源码"],
        ];

    const searchButton = document.createElement("button");
    searchButton.className = "quick-search-toggle";
    searchButton.type = "button";
    searchButton.setAttribute("aria-label", copy.search);
    searchButton.setAttribute("aria-haspopup", "dialog");
    const shortcutLabel = /Mac|iPhone|iPad/.test(navigator.platform) ? "⌘K" : "Ctrl K";
    searchButton.innerHTML = '<svg class="icon" viewBox="0 0 20 20" aria-hidden="true" focusable="false"><circle cx="8.5" cy="8.5" r="4.5"></circle><path d="m12 12 4 4"></path></svg><span>' + copy.search + "</span><kbd>" + shortcutLabel + "</kbd>";
    topbarTools.prepend(searchButton);

    const overlay = document.createElement("div");
    overlay.className = "command-overlay";
    overlay.hidden = true;
    overlay.innerHTML = `
      <section class="command-panel" role="dialog" aria-modal="true" aria-labelledby="command-title">
        <div class="command-head">
          <label id="command-title" for="command-input">${copy.search}</label>
          <button class="command-close" type="button" aria-label="${copy.closeSearch}">Esc</button>
        </div>
        <div class="command-input-wrap">
          <svg class="icon" viewBox="0 0 20 20" aria-hidden="true" focusable="false"><circle cx="8.5" cy="8.5" r="4.5"></circle><path d="m12 12 4 4"></path></svg>
          <input id="command-input" type="search" autocomplete="off" spellcheck="false" placeholder="${copy.searchPlaceholder}">
        </div>
        <div class="command-results" role="listbox"></div>
        <p class="command-hint">${copy.searchHint}</p>
      </section>`;
    document.body.append(overlay);

    const searchInput = select("#command-input", overlay);
    const searchResults = select(".command-results", overlay);
    const closeSearchButton = select(".command-close", overlay);
    let selectedResult = 0;
    let lastFocused = null;

    const updateSelectedResult = () => {
      const results = selectAll("a", searchResults);
      if (!results.length) return;
      selectedResult = (selectedResult + results.length) % results.length;
      results.forEach((result, index) => {
        result.classList.toggle("selected", index === selectedResult);
        result.setAttribute("aria-selected", String(index === selectedResult));
      });
      results[selectedResult].scrollIntoView({ block: "nearest" });
    };

    const renderSearchResults = (value = "") => {
      const query = value.trim().toLocaleLowerCase(locale);
      const matches = searchItems.filter((item) => item.join(" ").toLocaleLowerCase(locale).includes(query));
      searchResults.replaceChildren();
      selectedResult = 0;
      if (!matches.length) {
        const empty = document.createElement("p");
        empty.className = "command-empty";
        empty.textContent = copy.noResults;
        searchResults.append(empty);
        return;
      }
      const fragment = document.createDocumentFragment();
      matches.forEach(([title, meta, url]) => {
        const link = document.createElement("a");
        link.href = url;
        link.setAttribute("role", "option");
        if (url.startsWith("http")) {
          link.target = "_blank";
          link.rel = "noreferrer";
        }
        const text = document.createElement("span");
        const strong = document.createElement("strong");
        const small = document.createElement("small");
        strong.textContent = title;
        small.textContent = meta;
        text.append(strong, small);
        const arrow = document.createElement("span");
        arrow.className = "command-arrow";
        arrow.setAttribute("aria-hidden", "true");
        arrow.innerHTML = '<svg class="icon icon-arrow-right" viewBox="0 0 20 20" aria-hidden="true" focusable="false"><path d="M5 15 15 5"></path><path d="M8 5h7v7"></path></svg>';
        link.append(text, arrow);
        fragment.append(link);
      });
      searchResults.append(fragment);
      updateSelectedResult();
    };

    const openSearch = () => {
      window.dispatchEvent(new CustomEvent("ui-overlay-open", { detail: { source: "search" } }));
      lastFocused = document.activeElement;
      overlay.hidden = false;
      document.body.classList.add("command-open");
      renderSearchResults();
      window.requestAnimationFrame(() => overlay.classList.add("open"));
      searchInput.focus();
    };

    const closeSearch = () => {
      overlay.classList.remove("open");
      overlay.hidden = true;
      document.body.classList.remove("command-open");
      searchInput.value = "";
      if (lastFocused && typeof lastFocused.focus === "function") lastFocused.focus();
    };

    searchButton.addEventListener("click", openSearch);
    closeSearchButton.addEventListener("click", closeSearch);
    overlay.addEventListener("click", (event) => {
      if (event.target === overlay) closeSearch();
    });
    searchInput.addEventListener("input", () => renderSearchResults(searchInput.value));
    searchInput.addEventListener("keydown", (event) => {
      const results = selectAll("a", searchResults);
      if (event.key === "ArrowDown" || event.key === "ArrowUp") {
        event.preventDefault();
        selectedResult += event.key === "ArrowDown" ? 1 : -1;
        updateSelectedResult();
      } else if (event.key === "Enter" && results[selectedResult]) {
        event.preventDefault();
        results[selectedResult].click();
      }
    });

    document.addEventListener("keydown", (event) => {
      const element = event.target;
      const isEditing = element instanceof HTMLInputElement || element instanceof HTMLTextAreaElement || element.isContentEditable;
      if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === "k") {
        event.preventDefault();
        overlay.hidden ? openSearch() : closeSearch();
      } else if (event.key === "/" && !isEditing && overlay.hidden) {
        event.preventDefault();
        openSearch();
      } else if (event.key === "Escape" && !overlay.hidden) {
        closeSearch();
      } else if (event.key === "Tab" && !overlay.hidden) {
        const focusable = [searchInput, ...selectAll("a", searchResults), closeSearchButton];
        const current = Math.max(0, focusable.indexOf(document.activeElement));
        const step = event.shiftKey ? -1 : 1;
        event.preventDefault();
        focusable[(current + step + focusable.length) % focusable.length].focus();
      }
    });
    window.addEventListener("ui-overlay-open", (event) => {
      if (event.detail?.source !== "search" && !overlay.hidden) closeSearch();
    });
  }

  const weatherButton = select("#weather-button");
  const weatherValue = select("#weather-value");
  const weatherMeta = select("#weather-meta");
  const weatherDescriptions = isEnglish
    ? {
        0: "Clear", 1: "Mostly clear", 2: "Partly cloudy", 3: "Overcast",
        45: "Fog", 48: "Rime fog", 51: "Light drizzle", 53: "Drizzle",
        55: "Heavy drizzle", 61: "Light rain", 63: "Rain", 65: "Heavy rain",
        71: "Light snow", 73: "Snow", 75: "Heavy snow", 80: "Light showers",
        81: "Showers", 82: "Heavy showers", 95: "Thunderstorm",
        96: "Thunderstorm with hail", 99: "Thunderstorm with hail",
      }
    : {
        0: "晴朗", 1: "大部晴朗", 2: "局部多云", 3: "阴天",
        45: "有雾", 48: "雾凇", 51: "小毛毛雨", 53: "毛毛雨",
        55: "较强毛毛雨", 61: "小雨", 63: "中雨", 65: "大雨",
        71: "小雪", 73: "中雪", 75: "大雪", 80: "小阵雨",
        81: "阵雨", 82: "强阵雨", 95: "雷暴",
        96: "雷暴伴小冰雹", 99: "雷暴伴冰雹",
      };

  const setWeather = (value, meta) => {
    if (weatherValue) weatherValue.textContent = value;
    if (weatherMeta) weatherMeta.textContent = meta;
  };

  const weatherCacheKey = `true-path-weather-${locale}`;
  const restoreWeather = () => {
    try {
      const cached = JSON.parse(window.sessionStorage.getItem(weatherCacheKey) || "null");
      if (!cached || Date.now() - cached.savedAt > 15 * 60 * 1000) return;
      setWeather(cached.value, cached.meta);
      if (weatherButton) weatherButton.textContent = copy.relocate;
    } catch {
      // Weather still works when storage is unavailable.
    }
  };

  const cacheWeather = (value, meta) => {
    try {
      window.sessionStorage.setItem(weatherCacheKey, JSON.stringify({ value, meta, savedAt: Date.now() }));
    } catch {
      // Weather still works when storage is unavailable.
    }
  };

  const requestPosition = () =>
    new Promise((resolve, reject) => {
      if (!("geolocation" in navigator)) {
        reject(new Error(copy.geolocationUnsupported));
        return;
      }
      navigator.geolocation.getCurrentPosition(resolve, reject, {
        enableHighAccuracy: false,
        timeout: 10000,
        maximumAge: 10 * 60 * 1000,
      });
    });

  if (weatherButton) {
    weatherButton.addEventListener("click", async () => {
      weatherButton.disabled = true;
      weatherButton.textContent = copy.locating;
      setWeather("—", copy.awaitingPermission);
      try {
        const position = await requestPosition();
        const { latitude, longitude } = position.coords;
        const endpoint = new URL("https://api.open-meteo.com/v1/forecast");
        endpoint.searchParams.set("latitude", latitude.toFixed(4));
        endpoint.searchParams.set("longitude", longitude.toFixed(4));
        endpoint.searchParams.set(
          "current",
          "temperature_2m,apparent_temperature,relative_humidity_2m,weather_code,wind_speed_10m",
        );
        endpoint.searchParams.set("timezone", "auto");
        const controller = new AbortController();
        const timeout = window.setTimeout(() => controller.abort(), 10_000);
        let response;
        try {
          response = await fetch(endpoint, { headers: { Accept: "application/json" }, signal: controller.signal });
        } finally {
          window.clearTimeout(timeout);
        }
        if (!response.ok) throw new Error(copy.weatherUnavailable);
        const data = await response.json();
        const current = data.current;
        if (!current) throw new Error(copy.noWeatherData);
        const description = weatherDescriptions[current.weather_code] || copy.weatherUpdating;
        const value = `${Math.round(current.temperature_2m)}°C · ${description}`;
        const meta = copy.weatherDetails(current);
        setWeather(value, meta);
        cacheWeather(value, meta);
        weatherButton.textContent = copy.relocate;
      } catch (error) {
        const denied = error && error.code === 1;
        const message = denied
          ? copy.denied
          : error?.name === "AbortError"
            ? copy.weatherTimeout
            : error.message || copy.weatherUnavailable;
        setWeather(copy.unavailable, message);
        weatherButton.textContent = copy.retry;
      } finally {
        weatherButton.disabled = false;
      }
    });
    restoreWeather();
  }

  const alignInitialHash = () => {
    if (!window.location.hash) return;
    let id;
    try {
      id = decodeURIComponent(window.location.hash.slice(1));
    } catch {
      return;
    }
    const target = document.getElementById(id);
    if (!target) return;
    window.requestAnimationFrame(() => {
      window.requestAnimationFrame(() => target.scrollIntoView({ block: "start" }));
    });
  };

  const stabilizeInitialHash = () => {
    alignInitialHash();
    if (document.fonts?.ready) document.fonts.ready.then(alignInitialHash);
    window.setTimeout(alignInitialHash, 1200);
  };

  if (document.readyState === "complete") stabilizeInitialHash();
  else window.addEventListener("load", stabilizeInitialHash, { once: true });
})();
