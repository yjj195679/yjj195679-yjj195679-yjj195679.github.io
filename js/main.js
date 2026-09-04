(() => {
  const select = (selector, root = document) => root.querySelector(selector);
  const selectAll = (selector, root = document) => [...root.querySelectorAll(selector)];

  const year = select("#year");
  if (year) year.textContent = String(new Date().getFullYear());

  const clock = select("#clock");
  const updateClock = () => {
    if (!clock) return;
    clock.textContent = new Intl.DateTimeFormat("zh-CN", {
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
    nav.classList.remove("open");
    document.body.classList.remove("menu-open");
  };

  if (menuButton && nav) {
    menuButton.addEventListener("click", () => {
      const isOpen = menuButton.getAttribute("aria-expanded") === "true";
      menuButton.setAttribute("aria-expanded", String(!isOpen));
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
  const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
  let framePending = false;
  const moveBackground = () => {
    if (!background || reducedMotion.matches) return;
    if (framePending) return;
    framePending = true;
    window.requestAnimationFrame(() => {
      const offset = Math.min(window.scrollY * 0.028, 22);
      background.style.transform = `translateY(${offset}px) scale(1.025)`;
      framePending = false;
    });
  };
  window.addEventListener("scroll", moveBackground, { passive: true });

  const weatherButton = select("#weather-button");
  const weatherValue = select("#weather-value");
  const weatherMeta = select("#weather-meta");
  const weatherDescriptions = {
    0: "晴朗",
    1: "大部晴朗",
    2: "局部多云",
    3: "阴天",
    45: "有雾",
    48: "雾凇",
    51: "小毛毛雨",
    53: "毛毛雨",
    55: "较强毛毛雨",
    61: "小雨",
    63: "中雨",
    65: "大雨",
    71: "小雪",
    73: "中雪",
    75: "大雪",
    80: "小阵雨",
    81: "阵雨",
    82: "强阵雨",
    95: "雷暴",
    96: "雷暴伴小冰雹",
    99: "雷暴伴冰雹",
  };

  const setWeather = (value, meta) => {
    if (weatherValue) weatherValue.textContent = value;
    if (weatherMeta) weatherMeta.textContent = meta;
  };

  const requestPosition = () =>
    new Promise((resolve, reject) => {
      if (!("geolocation" in navigator)) {
        reject(new Error("当前浏览器不支持定位"));
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
      weatherButton.textContent = "正在获取…";
      setWeather("—", "等待浏览器定位授权");
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
        if (!response.ok) throw new Error("天气服务暂时不可用");
        const data = await response.json();
        const current = data.current;
        if (!current) throw new Error("未获取到天气数据");
        const description = weatherDescriptions[current.weather_code] || "天气更新中";
        setWeather(
          `${Math.round(current.temperature_2m)}°C · ${description}`,
          `体感 ${Math.round(current.apparent_temperature)}°C　湿度 ${current.relative_humidity_2m}%　风速 ${Math.round(current.wind_speed_10m)} km/h`,
        );
        weatherButton.textContent = "重新定位";
      } catch (error) {
        const denied = error && error.code === 1;
        setWeather("暂时无法显示", denied ? "你没有授权定位，网站不会保存位置信息" : error.message || "请稍后再试");
        weatherButton.textContent = "再次尝试";
      } finally {
        weatherButton.disabled = false;
      }
    });
  }
})();
