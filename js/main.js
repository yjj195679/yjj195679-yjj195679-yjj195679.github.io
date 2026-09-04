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
        weatherDetails: (current) =>
          `体感 ${Math.round(current.apparent_temperature)}°C　湿度 ${current.relative_humidity_2m}%　风速 ${Math.round(current.wind_speed_10m)} km/h`,
      };

  const year = select("#year");
  if (year) year.textContent = String(new Date().getFullYear());

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
