(() => {
  const isEnglish = document.documentElement.lang.toLowerCase().startsWith("en");
  const originalTitle = document.title;
  const copy = isEnglish
    ? {
        start: "Start",
        pause: "Pause",
        ready: "Choose a duration and start the timer.",
        running: (mode) => `${mode} session in progress.`,
        paused: (mode) => `${mode} session paused.`,
        complete: (mode) => `${mode} session complete. Time to switch pace.`,
        quoteRefresh: "Another thought",
        play: "Play",
        pauseMusic: "Pause",
        musicReady: "Press play to generate sound locally in your browser.",
        musicPlaying: (mode) => `${mode} is playing.`,
        musicPaused: (mode) => `${mode} is paused.`,
        musicUnavailable: "This browser cannot generate audio. Try a current version of Chrome, Edge, Firefox, or Safari.",
      }
    : {
        start: "开始",
        pause: "暂停",
        ready: "选择时长后开始计时。",
        running: (mode) => `${mode}计时进行中。`,
        paused: (mode) => `${mode}计时已暂停。`,
        complete: (mode) => `${mode}结束，可以切换一下节奏了。`,
        quoteRefresh: "再看一句",
        play: "播放",
        pauseMusic: "暂停",
        musicReady: "点击播放后，浏览器会在本地生成声音。",
        musicPlaying: (mode) => `${mode}正在播放。`,
        musicPaused: (mode) => `${mode}已暂停。`,
        musicUnavailable: "当前浏览器无法生成音频，请尝试最新版 Chrome、Edge、Firefox 或 Safari。",
      };

  const timer = document.querySelector("[data-focus-timer]");
  if (timer) {
    const value = timer.querySelector("#timer-value");
    const modeLabel = timer.querySelector("#timer-mode");
    const progress = timer.querySelector(".timer-progress");
    const progressFill = timer.querySelector(".timer-progress span");
    const toggle = timer.querySelector("#timer-toggle");
    const reset = timer.querySelector("#timer-reset");
    const status = timer.querySelector("#timer-status");
    const presets = [...timer.querySelectorAll("[data-minutes]")];

    let totalSeconds = 25 * 60;
    let remainingSeconds = totalSeconds;
    let deadline = 0;
    let interval = null;
    let running = false;

    const formatTime = (seconds) => {
      const minutes = Math.floor(seconds / 60);
      const rest = seconds % 60;
      return `${String(minutes).padStart(2, "0")}:${String(rest).padStart(2, "0")}`;
    };

    const renderTimer = () => {
      const formatted = formatTime(remainingSeconds);
      const percentage = Math.round((1 - remainingSeconds / totalSeconds) * 100);
      value.textContent = formatted;
      progressFill.style.transform = `scaleX(${Math.max(0, Math.min(percentage / 100, 1))})`;
      progress.setAttribute("aria-valuenow", String(percentage));
      if (running) document.title = `${formatted} · ${originalTitle}`;
    };

    const stopInterval = () => {
      if (interval) window.clearInterval(interval);
      interval = null;
    };

    const finishTimer = () => {
      running = false;
      stopInterval();
      toggle.textContent = copy.start;
      status.textContent = copy.complete(modeLabel.textContent);
      document.title = originalTitle;
      timer.classList.add("timer-complete");
      window.setTimeout(() => timer.classList.remove("timer-complete"), 1400);
    };

    const tick = () => {
      remainingSeconds = Math.max(0, Math.ceil((deadline - Date.now()) / 1000));
      renderTimer();
      if (remainingSeconds === 0) finishTimer();
    };

    toggle.addEventListener("click", () => {
      if (running) {
        running = false;
        remainingSeconds = Math.max(0, Math.ceil((deadline - Date.now()) / 1000));
        stopInterval();
        toggle.textContent = copy.start;
        status.textContent = copy.paused(modeLabel.textContent);
        document.title = originalTitle;
        renderTimer();
        return;
      }
      if (remainingSeconds === 0) remainingSeconds = totalSeconds;
      running = true;
      deadline = Date.now() + remainingSeconds * 1000;
      toggle.textContent = copy.pause;
      status.textContent = copy.running(modeLabel.textContent);
      tick();
      interval = window.setInterval(tick, 250);
    });

    const resetTimer = () => {
      running = false;
      stopInterval();
      remainingSeconds = totalSeconds;
      toggle.textContent = copy.start;
      status.textContent = copy.ready;
      document.title = originalTitle;
      renderTimer();
    };

    reset.addEventListener("click", resetTimer);
    presets.forEach((preset) => {
      preset.addEventListener("click", () => {
        totalSeconds = Number(preset.dataset.minutes) * 60;
        modeLabel.textContent = preset.dataset.mode;
        presets.forEach((item) => item.classList.toggle("selected", item === preset));
        resetTimer();
      });
    });

    renderTimer();
  }

  const quoteTool = document.querySelector("[data-quote-tool]");
  if (quoteTool) {
    const text = quoteTool.querySelector("#quote-text");
    const translation = quoteTool.querySelector("#quote-translation");
    const source = quoteTool.querySelector("#quote-source");
    const refresh = quoteTool.querySelector("#quote-refresh");
    const date = quoteTool.querySelector("#quote-date");
    const thoughts = [
      {
        zh: "未经审视的人生是不值得过的。",
        en: "The unexamined life is not worth living.",
        authorZh: "苏格拉底",
        authorEn: "Socrates",
        workZh: "《申辩篇》",
        workEn: "Apology",
      },
      {
        zh: "困扰我们的不是事物本身，而是我们对事物的判断。",
        en: "It is not things themselves that trouble us, but our judgments about them.",
        authorZh: "爱比克泰德",
        authorEn: "Epictetus",
        workZh: "《手册》",
        workEn: "Enchiridion",
      },
      {
        zh: "我思，故我在。",
        en: "I think, therefore I am.",
        authorZh: "勒内·笛卡尔",
        authorEn: "René Descartes",
        workZh: "《方法论》",
        workEn: "Discourse on the Method",
      },
      {
        zh: "要敢于求知，也要有勇气运用自己的理性。",
        en: "Dare to know; have the courage to use your own understanding.",
        authorZh: "伊曼努尔·康德",
        authorEn: "Immanuel Kant",
        workZh: "《什么是启蒙？》",
        workEn: "What Is Enlightenment?",
      },
      {
        zh: "知之为知之，不知为不知，是知也。",
        en: "To know what you know, and to know what you do not know—this is knowledge.",
        authorZh: "孔子",
        authorEn: "Confucius",
        workZh: "《论语·为政》",
        workEn: "Analects, Book II",
      },
      {
        zh: "人不能两次踏入同一条河流。",
        en: "No one steps into the same river twice.",
        authorZh: "赫拉克利特",
        authorEn: "Heraclitus",
        workZh: "残篇",
        workEn: "Fragments",
      },
      {
        zh: "知人者智，自知者明。",
        en: "Those who know others are wise; those who know themselves are enlightened.",
        authorZh: "老子",
        authorEn: "Laozi",
        workZh: "《道德经》第三十三章",
        workEn: "Tao Te Ching, Chapter 33",
      },
      {
        zh: "心灵有它的理由，而理性并不了解这些理由。",
        en: "The heart has its reasons, which reason does not know.",
        authorZh: "布莱兹·帕斯卡",
        authorEn: "Blaise Pascal",
        workZh: "《思想录》",
        workEn: "Pensées",
      },
      {
        zh: "读书使人充实，讨论使人敏捷，写作使人严谨。",
        en: "Reading makes a full person, conversation a ready person, and writing an exact person.",
        authorZh: "弗朗西斯·培根",
        authorEn: "Francis Bacon",
        workZh: "《论读书》",
        workEn: "Of Studies",
      },
      {
        zh: "我们在想象中受的苦，往往多于在现实中受的苦。",
        en: "We suffer more often in imagination than in reality.",
        authorZh: "塞涅卡",
        authorEn: "Seneca",
        workZh: "《致鲁西流书信集》第十三封",
        workEn: "Moral Letters, Letter 13",
      },
      {
        zh: "只知道自己一方论点的人，对它所知甚少。",
        en: "He who knows only his own side of the case knows little of that.",
        authorZh: "约翰·斯图亚特·密尔",
        authorEn: "John Stuart Mill",
        workZh: "《论自由》",
        workEn: "On Liberty",
      },
      {
        zh: "理性是激情的奴隶，而且也应当如此。",
        en: "Reason is, and ought only to be, the slave of the passions.",
        authorZh: "大卫·休谟",
        authorEn: "David Hume",
        workZh: "《人性论》",
        workEn: "A Treatise of Human Nature",
      },
    ];

    const now = new Date();
    const localDay = Date.UTC(now.getFullYear(), now.getMonth(), now.getDate()) / 86400000;
    const dailyIndex = Math.floor(localDay) % thoughts.length;
    let currentIndex = dailyIndex;

    const renderThought = () => {
      const thought = thoughts[currentIndex];
      text.textContent = isEnglish ? thought.en : thought.zh;
      translation.textContent = isEnglish ? thought.zh : thought.en;
      const author = isEnglish ? thought.authorEn : thought.authorZh;
      const work = isEnglish ? thought.workEn : thought.workZh;
      source.textContent = `— ${author} · ${work}`;
      date.textContent = currentIndex === dailyIndex
        ? new Intl.DateTimeFormat(isEnglish ? "en-US" : "zh-CN", { month: "long", day: "numeric" }).format(now)
        : isEnglish ? "More philosophy" : "更多哲思";
      quoteTool.dataset.state = "ready";
    };

    refresh.addEventListener("click", () => {
      currentIndex = (currentIndex + 1) % thoughts.length;
      renderThought();
      refresh.textContent = copy.quoteRefresh;
    });
    renderThought();
  }

  const musicPlayer = document.querySelector("[data-music-player]");
  if (musicPlayer) {
    const AudioContext = window.AudioContext || window.webkitAudioContext;
    const toggle = musicPlayer.querySelector("#music-toggle");
    const previous = musicPlayer.querySelector("#music-prev");
    const next = musicPlayer.querySelector("#music-next");
    const track = musicPlayer.querySelector("#music-track");
    const description = musicPlayer.querySelector("#music-description");
    const time = musicPlayer.querySelector("#music-time");
    const volume = musicPlayer.querySelector("#music-volume");
    const volumeValue = musicPlayer.querySelector("#music-volume-value");
    const status = musicPlayer.querySelector("#music-status");
    const modeButtons = [...musicPlayer.querySelectorAll("[data-music-mode]")];
    const modes = [
      {
        nameZh: "深度专注",
        nameEn: "Deep Focus",
        descriptionZh: "平稳的低频和弦，为阅读与推导留出空间。",
        descriptionEn: "Steady low-frequency chords that leave room for reading and reasoning.",
        tones: [110, 164.81, 220],
        wave: "triangle",
        cutoff: 620,
        drift: 2.4,
      },
      {
        nameZh: "夜间阅读",
        nameEn: "Night Reading",
        descriptionZh: "更暗、更慢的音层，适合夜间整理笔记。",
        descriptionEn: "A darker, slower sound bed for organizing notes at night.",
        tones: [98, 146.83, 196],
        wave: "sine",
        cutoff: 480,
        drift: 1.7,
      },
      {
        nameZh: "安静清晨",
        nameEn: "Quiet Dawn",
        descriptionZh: "较明亮的开放和弦，让清晨学习保持轻盈。",
        descriptionEn: "Brighter open chords for a lighter morning study session.",
        tones: [130.81, 196, 261.63],
        wave: "sine",
        cutoff: 920,
        drift: 3.1,
      },
    ];

    let context = null;
    let masterGain = null;
    let activeNodes = [];
    let modeIndex = 0;
    let isPlaying = false;
    let elapsed = 0;
    let startedAt = 0;
    let clockInterval = null;
    let restartTimeout = null;

    const modeName = (mode) => isEnglish ? mode.nameEn : mode.nameZh;
    const modeDescription = (mode) => isEnglish ? mode.descriptionEn : mode.descriptionZh;
    const gainLevel = () => Number(volume.value) / 100;
    const formatElapsed = (milliseconds) => {
      const seconds = Math.floor(milliseconds / 1000);
      const minutes = Math.floor(seconds / 60);
      return `${String(minutes).padStart(2, "0")}:${String(seconds % 60).padStart(2, "0")}`;
    };

    const updateTime = () => {
      const milliseconds = elapsed + (isPlaying ? Date.now() - startedAt : 0);
      const formatted = formatElapsed(milliseconds);
      time.textContent = formatted;
      time.dateTime = `PT${Math.floor(milliseconds / 1000)}S`;
    };

    const stopClock = () => {
      if (clockInterval) window.clearInterval(clockInterval);
      clockInterval = null;
    };

    const stopNodes = (nodes = activeNodes) => {
      nodes.forEach(({ oscillator, lfo }) => {
        try {
          oscillator.stop();
          lfo.stop();
        } catch {
          // Nodes may already be stopped when the page is closing.
        }
      });
      if (nodes === activeNodes) activeNodes = [];
    };

    const createSound = () => {
      const mode = modes[modeIndex];
      const filter = context.createBiquadFilter();
      filter.type = "lowpass";
      filter.frequency.value = mode.cutoff;
      filter.Q.value = 0.45;
      filter.connect(masterGain);

      activeNodes = mode.tones.map((frequency, index) => {
        const oscillator = context.createOscillator();
        const voiceGain = context.createGain();
        const lfo = context.createOscillator();
        const lfoDepth = context.createGain();
        oscillator.type = mode.wave;
        oscillator.frequency.value = frequency;
        oscillator.detune.value = (index - 1) * 3;
        voiceGain.gain.value = 0.07 / mode.tones.length;
        lfo.type = "sine";
        lfo.frequency.value = 0.035 + index * 0.012;
        lfoDepth.gain.value = mode.drift;
        lfo.connect(lfoDepth);
        lfoDepth.connect(oscillator.detune);
        oscillator.connect(voiceGain);
        voiceGain.connect(filter);
        oscillator.start();
        lfo.start();
        return { oscillator, lfo };
      });
    };

    const ensureAudio = async () => {
      if (!AudioContext) throw new Error("Web Audio unavailable");
      if (!context) {
        context = new AudioContext();
        masterGain = context.createGain();
        masterGain.gain.value = 0.0001;
        masterGain.connect(context.destination);
      }
      if (context.state === "suspended") await context.resume();
    };

    const renderMode = () => {
      const mode = modes[modeIndex];
      track.textContent = modeName(mode);
      description.textContent = modeDescription(mode);
      modeButtons.forEach((button, index) => {
        button.classList.toggle("selected", index === modeIndex);
        button.setAttribute("aria-pressed", String(index === modeIndex));
      });
      if (!isPlaying) status.textContent = copy.musicReady;
    };

    const play = async () => {
      try {
        await ensureAudio();
        stopNodes();
        createSound();
        masterGain.gain.cancelScheduledValues(context.currentTime);
        masterGain.gain.setValueAtTime(0.0001, context.currentTime);
        masterGain.gain.exponentialRampToValueAtTime(Math.max(gainLevel(), 0.0001), context.currentTime + 0.8);
        isPlaying = true;
        startedAt = Date.now();
        musicPlayer.classList.add("is-playing");
        toggle.textContent = copy.pauseMusic;
        toggle.setAttribute("aria-pressed", "true");
        status.textContent = copy.musicPlaying(modeName(modes[modeIndex]));
        stopClock();
        clockInterval = window.setInterval(updateTime, 1000);
        updateTime();
      } catch {
        status.textContent = copy.musicUnavailable;
        toggle.disabled = true;
      }
    };

    const pause = () => {
      if (!isPlaying) return;
      const nodesToStop = activeNodes;
      activeNodes = [];
      elapsed += Date.now() - startedAt;
      isPlaying = false;
      stopClock();
      updateTime();
      if (context && masterGain) {
        masterGain.gain.cancelScheduledValues(context.currentTime);
        masterGain.gain.setTargetAtTime(0.0001, context.currentTime, 0.08);
      }
      window.setTimeout(() => stopNodes(nodesToStop), 320);
      musicPlayer.classList.remove("is-playing");
      toggle.textContent = copy.play;
      toggle.setAttribute("aria-pressed", "false");
      status.textContent = copy.musicPaused(modeName(modes[modeIndex]));
    };

    const selectMode = (index) => {
      if (restartTimeout) window.clearTimeout(restartTimeout);
      const wasPlaying = isPlaying;
      if (wasPlaying) pause();
      modeIndex = (index + modes.length) % modes.length;
      elapsed = 0;
      updateTime();
      renderMode();
      if (wasPlaying) {
        restartTimeout = window.setTimeout(() => {
          restartTimeout = null;
          play();
        }, 360);
      }
    };

    toggle.addEventListener("click", () => {
      if (restartTimeout) {
        window.clearTimeout(restartTimeout);
        restartTimeout = null;
      }
      return isPlaying ? pause() : play();
    });
    previous.addEventListener("click", () => selectMode(modeIndex - 1));
    next.addEventListener("click", () => selectMode(modeIndex + 1));
    modeButtons.forEach((button) => {
      button.addEventListener("click", () => selectMode(Number(button.dataset.musicMode)));
    });
    volume.addEventListener("input", () => {
      volumeValue.textContent = `${volume.value}%`;
      if (context && masterGain && isPlaying) {
        masterGain.gain.setTargetAtTime(Math.max(gainLevel(), 0.0001), context.currentTime, 0.06);
      }
    });
    window.addEventListener("pagehide", () => {
      if (restartTimeout) window.clearTimeout(restartTimeout);
      stopClock();
      stopNodes();
      if (context) context.close();
    });

    renderMode();
  }
})();
