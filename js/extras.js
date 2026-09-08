(() => {
  const isEnglish = document.documentElement.lang.toLowerCase().startsWith("en");
  const copy = isEnglish
    ? { quoteRefresh: "Another thought" }
    : { quoteRefresh: "再看一句" };

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

})();
