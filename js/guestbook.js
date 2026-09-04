(() => {
  const SUPABASE_URL = "https://lbnmkxmvdalavcjdxtpy.supabase.co";
  // Publishable keys are designed for browser use. Access is restricted by grants and RLS.
  const SUPABASE_PUBLISHABLE_KEY = "sb_publishable_51L4uutI9UYKfIxyq_adFQ_ZDaoL4F6";
  const API_URL = `${SUPABASE_URL}/rest/v1/messages`;
  const COOLDOWN_MS = 30_000;

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
    submitButton.textContent = loading ? "正在提交…" : "发布留言";
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
      if (!response.ok) throw new Error(`请求失败（${response.status}）`);
      return response;
    } finally {
      window.clearTimeout(timer);
    }
  };

  const formatTime = (value) =>
    new Intl.DateTimeFormat("zh-CN", {
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
      empty.textContent = "还没有公开留言。你可以成为第一位访客。";
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
      fragment.append(article);
    });
    list.append(fragment);
  };

  const loadMessages = async () => {
    list.setAttribute("aria-busy", "true");
    try {
      const query = "?select=name,content,created_at&is_visible=eq.true&order=created_at.desc&limit=30";
      const response = await request(`${API_URL}${query}`);
      renderMessages(await response.json());
    } catch (error) {
      const empty = document.createElement("div");
      empty.className = "empty-state";
      empty.textContent = "留言暂时无法加载，请稍后刷新。";
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
      setStatus("名字需为 1–40 个字符。", "error");
      return;
    }
    if (!content || content.length > 500) {
      setStatus("留言需为 1–500 个字符。", "error");
      return;
    }

    const remaining = COOLDOWN_MS - (Date.now() - getLastSubmit());
    if (remaining > 0) {
      setStatus(`请在 ${Math.ceil(remaining / 1000)} 秒后再提交。`, "error");
      return;
    }

    setLoading(true);
    setStatus("正在安全提交…");
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
      setStatus("留言已发布，谢谢你。", "success");
      await loadMessages();
    } catch (error) {
      const message = error.name === "AbortError" ? "请求超时，请稍后再试。" : "提交失败，请稍后再试。";
      setStatus(message, "error");
    } finally {
      setLoading(false);
    }
  });

  loadMessages();
})();
