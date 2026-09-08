(() => {
  const SUPABASE_URL = "https://lbnmkxmvdalavcjdxtpy.supabase.co";
  // Publishable keys are designed for browser use. Access is restricted by grants and RLS.
  const SUPABASE_PUBLISHABLE_KEY = "sb_publishable_51L4uutI9UYKfIxyq_adFQ_ZDaoL4F6";
  const API_URL = `${SUPABASE_URL}/rest/v1/messages`;
  const COOLDOWN_MS = 30_000;

  const isEnglish = document.documentElement.lang.toLowerCase().startsWith("en");
  const locale = isEnglish ? "en-US" : "zh-CN";
  const copy = isEnglish
    ? {
        submit: "Post message",
        submitting: "Posting…",
        empty: "No public messages yet.",
        loadFailed: "Messages are unavailable. Please try again later.",
        invalidName: "Name must be between 1 and 40 characters.",
        invalidContent: "Message must be between 1 and 500 characters.",
        cooldown: (seconds) => `Please wait ${seconds} seconds before posting again.`,
        sending: "Posting…",
        success: "Message posted. Thank you.",
        timeout: "The request timed out. Please try again.",
        failed: "The message could not be posted. Please try again.",
        rateLimited: "The guestbook is receiving several messages. Please try again in one minute.",
        requestFailed: (statusCode) => `Request failed (${statusCode})`,
        adminReply: "Reply from the site owner",
        offline: "You appear to be offline. Reconnect and try again.",
        charactersRemaining: (remaining) => `${remaining} characters remaining`,
      }
    : {
        submit: "发布留言",
        submitting: "正在提交…",
        empty: "还没有公开留言。你可以成为第一位访客。",
        loadFailed: "留言暂时无法加载，请稍后刷新。",
        invalidName: "名字需为 1–40 个字符。",
        invalidContent: "留言需为 1–500 个字符。",
        cooldown: (seconds) => `请在 ${seconds} 秒后再提交。`,
        sending: "正在提交…",
        success: "留言已发布，谢谢你。",
        timeout: "请求超时，请稍后再试。",
        failed: "提交失败，请稍后再试。",
        rateLimited: "当前留言较多，请一分钟后再试。",
        requestFailed: (statusCode) => `请求失败（${statusCode}）`,
        adminReply: "站长回复",
        offline: "当前似乎已离线，请恢复网络后重试。",
        charactersRemaining: (remaining) => `还可输入 ${remaining} 个字符`,
      };

  const form = document.querySelector("#guestbook-form");
  const list = document.querySelector("#message-list");
  const status = document.querySelector("#form-status");
  const submitButton = document.querySelector("#guestbook-submit");
  if (!form || !list || !status || !submitButton) return;

  const headers = {
    apikey: SUPABASE_PUBLISHABLE_KEY,
    Accept: "application/json",
  };

  const setStatus = (message, state = "") => {
    status.textContent = message;
    status.dataset.state = state;
  };

  const setLoading = (loading) => {
    submitButton.disabled = loading;
    submitButton.textContent = loading ? copy.submitting : copy.submit;
  };

  const fieldsWithLimits = [...form.querySelectorAll("input[maxlength], textarea[maxlength]")];
  const updateCounters = () => {
    fieldsWithLimits.forEach((field) => {
      const counter = document.querySelector(`#${field.id}-counter`);
      if (!counter) return;
      const remaining = Number(field.maxLength) - field.value.length;
      counter.textContent = copy.charactersRemaining(remaining);
      counter.dataset.state = remaining < Math.min(50, Math.ceil(Number(field.maxLength) * 0.1)) ? "near-limit" : "";
    });
  };
  fieldsWithLimits.forEach((field) => {
    const help = field.closest(".field")?.querySelector(".field-help");
    if (!help) return;
    const counter = document.createElement("span");
    counter.className = "field-counter";
    counter.id = `${field.id}-counter`;
    help.id = `${field.id}-help`;
    help.append(counter);
    field.setAttribute("aria-describedby", help.id);
    field.addEventListener("input", updateCounters);
  });
  updateCounters();

  const renderLoading = () => {
    const fragment = document.createDocumentFragment();
    for (let index = 0; index < 3; index += 1) {
      const skeleton = document.createElement("div");
      skeleton.className = "message-card message-skeleton";
      skeleton.setAttribute("aria-hidden", "true");
      skeleton.innerHTML = '<span></span><span></span><span></span>';
      fragment.append(skeleton);
    }
    list.replaceChildren(fragment);
  };

  const request = async (url, options = {}) => {
    const controller = new AbortController();
    const timer = window.setTimeout(() => controller.abort(), 12_000);
    try {
      const response = await fetch(url, {
        ...options,
        credentials: "omit",
        signal: controller.signal,
        headers: { ...headers, ...(options.headers || {}) },
      });
      if (!response.ok) {
        const error = new Error(copy.requestFailed(response.status));
        error.status = response.status;
        throw error;
      }
      return response;
    } finally {
      window.clearTimeout(timer);
    }
  };

  const formatTime = (value) =>
    new Intl.DateTimeFormat(locale, {
      year: "numeric",
      month: "short",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    }).format(new Date(value));

  const renderMessages = (messages) => {
    list.replaceChildren();
    if (!messages.length) {
      const empty = document.createElement("div");
      empty.className = "empty-state";
      empty.textContent = copy.empty;
      list.append(empty);
      return;
    }

    const fragment = document.createDocumentFragment();
    messages.forEach((message) => {
      const article = document.createElement("article");
      article.className = "message-card";

      const head = document.createElement("div");
      head.className = "message-head";

      const name = document.createElement("strong");
      name.className = "message-name";
      name.textContent = message.name;

      const time = document.createElement("time");
      time.className = "message-time";
      time.dateTime = message.created_at;
      time.textContent = formatTime(message.created_at);

      const content = document.createElement("p");
      content.className = "message-content";
      content.textContent = message.content;

      head.append(name, time);
      article.append(head, content);
      if (message.reply) {
        const reply = document.createElement("div");
        reply.className = "message-reply";
        const replyHead = document.createElement("div");
        replyHead.className = "message-reply-head";
        const replyLabel = document.createElement("strong");
        replyLabel.textContent = copy.adminReply;
        replyHead.append(replyLabel);
        if (message.replied_at) {
          const replyTime = document.createElement("time");
          replyTime.className = "message-time";
          replyTime.dateTime = message.replied_at;
          replyTime.textContent = formatTime(message.replied_at);
          replyHead.append(replyTime);
        }
        const replyContent = document.createElement("p");
        replyContent.textContent = message.reply;
        reply.append(replyHead, replyContent);
        article.append(reply);
      }
      fragment.append(article);
    });
    list.append(fragment);
  };

  const loadMessages = async () => {
    list.setAttribute("aria-busy", "true");
    renderLoading();
    try {
      const query = "?select=name,content,created_at,reply,replied_at&is_visible=eq.true&order=created_at.desc&limit=30";
      const response = await request(`${API_URL}${query}`);
      renderMessages(await response.json());
    } catch (error) {
      const empty = document.createElement("div");
      empty.className = "empty-state";
      empty.textContent = navigator.onLine ? copy.loadFailed : copy.offline;
      list.replaceChildren(empty);
    } finally {
      list.removeAttribute("aria-busy");
    }
  };

  const getLastSubmit = () => {
    try {
      return Number(window.localStorage.getItem("guestbook-last-submit") || 0);
    } catch {
      return 0;
    }
  };

  const rememberSubmit = () => {
    try {
      window.localStorage.setItem("guestbook-last-submit", String(Date.now()));
    } catch {
      // The message has already been stored; local cooldown is only a convenience.
    }
  };

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const data = new FormData(form);
    if (String(data.get("website") || "").trim()) return;

    const name = String(data.get("name") || "").trim();
    const content = String(data.get("content") || "").trim();
    if (!name || name.length > 40) {
      setStatus(copy.invalidName, "error");
      return;
    }
    if (!content || content.length > 500) {
      setStatus(copy.invalidContent, "error");
      return;
    }

    const remaining = COOLDOWN_MS - (Date.now() - getLastSubmit());
    if (remaining > 0) {
      setStatus(copy.cooldown(Math.ceil(remaining / 1000)), "error");
      return;
    }

    setLoading(true);
    setStatus(copy.sending);
    try {
      await request(API_URL, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Prefer: "return=minimal",
        },
        body: JSON.stringify({ name, content }),
      });
      rememberSubmit();
      form.reset();
      updateCounters();
      setStatus(copy.success, "success");
      await loadMessages();
    } catch (error) {
      const message = !navigator.onLine
        ? copy.offline
        : error.name === "AbortError"
          ? copy.timeout
          : error.status === 429
            ? copy.rateLimited
            : copy.failed;
      setStatus(message, "error");
    } finally {
      setLoading(false);
    }
  });

  loadMessages();
})();
