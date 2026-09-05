(() => {
  const select = (selector, root = document) => root.querySelector(selector);
  const selectAll = (selector, root = document) => [...root.querySelectorAll(selector)];

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
        noWeatherData: "No weather data was returned.",
        weatherUpdating: "Weather updating",
        relocate: "Update location",
        unavailable: "Unavailable",
        denied: "Location permission was not granted.",
        retry: "Try again",
        sectionNav: "On this page",
        backToTop: "Back to top",
        search: "Quick navigation",
        searchPlaceholder: "Search pages and projects…",
        searchHint: "Type to filter · ↑↓ to select · Enter to open",
        closeSearch: "Close quick navigation",
        noResults: "No matching pages.",
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
        noWeatherData: "未获取到天气数据",
        weatherUpdating: "天气更新中",
        relocate: "重新定位",
        unavailable: "暂时无法显示",
        denied: "你没有授权定位",
        retry: "再次尝试",
        sectionNav: "本页导航",
        backToTop: "返回顶部",
        search: "快捷导航",
        searchPlaceholder: "搜索页面、项目或知识方向…",
        searchHint: "输入筛选 · ↑↓ 选择 · 回车打开",
        closeSearch: "关闭快捷导航",
        noResults: "没有匹配的页面。",
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
  const closeMenu = () => {
    if (!menuButton || !nav) return;
    menuButton.setAttribute("aria-expanded", "false");
    menuButton.setAttribute("aria-label", copy.openMenu);
    nav.classList.remove("open");
    document.body.classList.remove("menu-open");
  };

  if (menuButton && nav) {
    menuButton.addEventListener("click", () => {
      const isOpen = menuButton.getAttribute("aria-expanded") === "true";
      menuButton.setAttribute("aria-expanded", String(!isOpen));
      menuButton.setAttribute("aria-label", isOpen ? copy.openMenu : copy.closeMenu);
      nav.classList.toggle("open", !isOpen);
      document.body.classList.toggle("menu-open", !isOpen);
    });
    selectAll("a", nav).forEach((link) => link.addEventListener("click", closeMenu));
    window.addEventListener("resize", () => {
      if (window.innerWidth > 980) closeMenu();
    });
    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape") closeMenu();
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
      if (background && !reducedMotion.matches) {
        const offset = Math.min(window.scrollY * 0.028, 22);
        background.style.transform = `translateY(${offset}px) scale(1.025)`;
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
    ? [...main.children].filter((element) => element.classList.contains("section"))
    : [];

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

    const links = pageSections.map((section, index) => {
      if (!section.id) section.id = `${page}-section-${index + 1}`;
      const heading = select("h2, h3", section);
      const link = document.createElement("a");
      link.href = `#${section.id}`;
      link.innerHTML = `<span aria-hidden="true"></span>${heading ? heading.textContent.trim() : `${index + 1}`}`;
      navInner.append(link);
      return link;
    });

    sectionNav.append(navInner);
    main.prepend(sectionNav);

    const setActiveSection = (id) => {
      links.forEach((link) => {
        if (link.hash === `#${id}`) link.setAttribute("aria-current", "location");
        else link.removeAttribute("aria-current");
      });
    };
    setActiveSection(pageSections[0].id);

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

  const topbarTools = select(".topbar-tools");
  if (topbarTools) {
    const searchItems = isEnglish
      ? [
          ["Home", "Profile and current focus", "index.html", "about research"],
          ["Projects", "Research overview", "projects.html", "portfolio work"],
          ["DPSR reproduction", "Super-resolution", "projects.html#dpsr", "srresnet pnp admm"],
          ["Primal–Dual deblurring", "Optimization", "projects.html#deblur", "chambolle pock fft tv"],
          ["UNet / Restormer", "Deep restoration", "projects.html#hybrid", "transformer stability"],
          ["Education", "Learning path", "education.html", "methods timeline"],
          ["Study", "Knowledge map", "courses.html", "408 mathematics vision"],
          ["Achievements", "Completed work", "achievements.html", "results milestones"],
          ["Life", "Current work", "life.html", "learning notes"],
          ["Daily philosophy", "Bilingual thought of the day", "life.html#interlude", "philosophy Chinese English"],
          ["Ambient player", "Generative study sound", "life.html#music", "music focus reading audio"],
          ["Guestbook", "Visitor messages", "guestbook.html", "contact message"],
          ["GitHub", "Code and repositories", "https://github.com/yjj195679", "source code"],
        ]
      : [
          ["首页", "个人简介与当前方向", "index.html", "home 关于 研究"],
          ["项目", "研究与实验概览", "projects.html", "作品 实验"],
          ["DPSR 复现", "超分辨率", "projects.html#dpsr", "srresnet pnp admm"],
          ["Primal–Dual 去模糊", "优化方法", "projects.html#deblur", "chambolle pock fft tv"],
          ["UNet / Restormer", "深度图像复原", "projects.html#hybrid", "transformer 稳定性"],
          ["教育", "学习路径", "education.html", "方法 时间线"],
          ["学习", "知识地图", "courses.html", "408 数学 图像复原"],
          ["成果", "已完成工作", "achievements.html", "结果 文档"],
          ["生活", "近期状态", "life.html", "学习 记录"],
          ["每日哲思", "中英对照的每日思考", "life.html#interlude", "哲学 中文 英文"],
          ["氛围音乐", "浏览器生成的学习声音", "life.html#music", "音乐 专注 阅读 播放器"],
          ["留言板", "访客交流", "guestbook.html", "联系 留言"],
          ["GitHub", "代码与公开项目", "https://github.com/yjj195679", "仓库 源码"],
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
        arrow.textContent = "↗";
        link.append(text, arrow);
        fragment.append(link);
      });
      searchResults.append(fragment);
      updateSelectedResult();
    };

    const openSearch = () => {
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
        const first = focusable[0];
        const last = focusable[focusable.length - 1];
        if (event.shiftKey && document.activeElement === first) {
          event.preventDefault();
          last.focus();
        } else if (!event.shiftKey && document.activeElement === last) {
          event.preventDefault();
          first.focus();
        }
      }
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
        const response = await fetch(endpoint, { headers: { Accept: "application/json" } });
        if (!response.ok) throw new Error(copy.weatherUnavailable);
        const data = await response.json();
        const current = data.current;
        if (!current) throw new Error(copy.noWeatherData);
        const description = weatherDescriptions[current.weather_code] || copy.weatherUpdating;
        setWeather(
          `${Math.round(current.temperature_2m)}°C · ${description}`,
          copy.weatherDetails(current),
        );
        weatherButton.textContent = copy.relocate;
      } catch (error) {
        const denied = error && error.code === 1;
        setWeather(copy.unavailable, denied ? copy.denied : error.message || copy.weatherUnavailable);
        weatherButton.textContent = copy.retry;
      } finally {
        weatherButton.disabled = false;
      }
    });
  }
})();
