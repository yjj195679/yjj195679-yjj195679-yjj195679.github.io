import { createClient } from "https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2.115.0/+esm";

const SUPABASE_URL = "https://lbnmkxmvdalavcjdxtpy.supabase.co";
const SUPABASE_PUBLISHABLE_KEY = "sb_publishable_51L4uutI9UYKfIxyq_adFQ_ZDaoL4F6";
const supabase = createClient(SUPABASE_URL, SUPABASE_PUBLISHABLE_KEY, {
  auth: { persistSession: true, autoRefreshToken: true, detectSessionInUrl: false },
});

const panels = {
  login: document.querySelector("#login-panel"),
  mfa: document.querySelector("#mfa-panel"),
  enroll: document.querySelector("#enroll-panel"),
  dashboard: document.querySelector("#dashboard-panel"),
};
const status = document.querySelector("#admin-status");
const messageList = document.querySelector("#admin-message-list");
const stats = document.querySelector("#admin-stats");
let messages = [];
let activeFilter = "all";
let enrollmentFactorId = "";

const showPanel = (name) => {
  Object.entries(panels).forEach(([key, panel]) => {
    panel.hidden = key !== name;
  });
};

const setStatus = (message, state = "") => {
  status.textContent = message;
  status.dataset.state = state;
};

const setBusy = (form, busy) => {
  form.querySelectorAll("button, input, textarea").forEach((control) => {
    control.disabled = busy;
  });
};

const formatTime = (value) =>
  value
    ? new Intl.DateTimeFormat("zh-CN", {
        year: "numeric",
        month: "short",
        day: "numeric",
        hour: "2-digit",
        minute: "2-digit",
      }).format(new Date(value))
    : "";

const isAdmin = (session) => session?.user?.app_metadata?.role === "admin";

const renderMessages = () => {
  const filtered = messages.filter((message) => {
    if (activeFilter === "unreplied") return !message.reply;
    if (activeFilter === "hidden") return !message.is_visible;
    return true;
  });

  stats.replaceChildren();
  [
    [messages.length, "全部留言"],
    [messages.filter((message) => !message.reply).length, "尚未回复"],
    [messages.filter((message) => !message.is_visible).length, "已隐藏"],
  ].forEach(([value, label]) => {
    const item = document.createElement("div");
    item.className = "admin-stat glass";
    const number = document.createElement("strong");
    number.textContent = String(value);
    const text = document.createElement("span");
    text.textContent = label;
    item.append(number, text);
    stats.append(item);
  });

  messageList.replaceChildren();
  if (!filtered.length) {
    const empty = document.createElement("div");
    empty.className = "empty-state";
    empty.textContent = "当前筛选条件下没有留言。";
    messageList.append(empty);
    return;
  }

  filtered.forEach((message) => {
    const card = document.createElement("article");
    card.className = "admin-message-card glass";
    card.dataset.messageId = message.id;

    const head = document.createElement("div");
    head.className = "message-head";
    const name = document.createElement("strong");
    name.className = "message-name";
    name.textContent = message.name;
    const time = document.createElement("time");
    time.className = "message-time";
    time.dateTime = message.created_at;
    time.textContent = formatTime(message.created_at);
    head.append(name, time);

    const content = document.createElement("p");
    content.className = "message-content";
    content.textContent = message.content;

    const field = document.createElement("div");
    field.className = "field admin-reply-field";
    const label = document.createElement("label");
    label.htmlFor = `reply-${message.id}`;
    label.textContent = "管理员回复";
    const textarea = document.createElement("textarea");
    textarea.id = label.htmlFor;
    textarea.maxLength = 1000;
    textarea.placeholder = "输入回复；清空后保存即可删除回复。";
    textarea.value = message.reply || "";
    field.append(label, textarea);

    const actions = document.createElement("div");
    actions.className = "admin-message-actions";
    const save = document.createElement("button");
    save.className = "button primary";
    save.type = "button";
    save.dataset.action = "save-reply";
    save.textContent = "保存回复";
    const visibility = document.createElement("button");
    visibility.className = "button secondary";
    visibility.type = "button";
    visibility.dataset.action = "toggle-visibility";
    visibility.textContent = message.is_visible ? "隐藏留言" : "恢复公开";
    const replyTime = document.createElement("span");
    replyTime.className = "message-time";
    replyTime.textContent = message.replied_at ? `上次回复：${formatTime(message.replied_at)}` : "尚未回复";
    actions.append(save, visibility, replyTime);
    card.append(head, content, field, actions);
    messageList.append(card);
  });
};

const loadMessages = async () => {
  messageList.setAttribute("aria-busy", "true");
  setStatus("正在读取留言…");
  const { data, error } = await supabase
    .from("messages")
    .select("id,name,content,created_at,is_visible,reply,replied_at")
    .order("created_at", { ascending: false });
  messageList.removeAttribute("aria-busy");
  if (error) {
    setStatus("无法读取留言。请确认已通过动态密码验证后重试。", "error");
    return;
  }
  messages = data || [];
  renderMessages();
  setStatus(`已加载 ${messages.length} 条留言。`, "success");
};

const enterDashboard = async (session) => {
  showPanel("dashboard");
  document.querySelector("#admin-account").textContent = `已登录：${session.user.email}`;
  await loadMessages();
};

const routeSession = async (session) => {
  if (!session) {
    showPanel("login");
    return;
  }
  if (!isAdmin(session)) {
    await supabase.auth.signOut();
    showPanel("login");
    setStatus("当前账户没有管理员权限。", "error");
    return;
  }
  const { data, error } = await supabase.auth.mfa.getAuthenticatorAssuranceLevel();
  if (error) {
    setStatus("无法检查动态验证状态，请重新登录。", "error");
    return;
  }
  if (data.currentLevel === "aal2") {
    await enterDashboard(session);
  } else if (data.nextLevel === "aal2") {
    showPanel("mfa");
    document.querySelector("#admin-totp").focus();
  } else {
    showPanel("enroll");
  }
};

document.querySelector("#login-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const form = event.currentTarget;
  const data = new FormData(form);
  setBusy(form, true);
  setStatus("正在验证邮箱和密码…");
  const result = await supabase.auth.signInWithPassword({
    email: String(data.get("email") || "").trim(),
    password: String(data.get("password") || ""),
  });
  setBusy(form, false);
  if (result.error) {
    setStatus("邮箱或密码不正确。", "error");
    return;
  }
  form.reset();
  setStatus("第一步验证成功，请输入动态密码。", "success");
  await routeSession(result.data.session);
});

document.querySelector("#mfa-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const form = event.currentTarget;
  const code = String(new FormData(form).get("totp") || "").trim();
  setBusy(form, true);
  setStatus("正在验证动态密码…");
  const factors = await supabase.auth.mfa.listFactors();
  const factor = factors.data?.totp?.find((item) => item.status === "verified");
  if (factors.error || !factor) {
    setBusy(form, false);
    setStatus("没有找到可用的 TOTP 验证器。", "error");
    return;
  }
  const challenge = await supabase.auth.mfa.challenge({ factorId: factor.id });
  const verified = challenge.error
    ? { error: challenge.error }
    : await supabase.auth.mfa.verify({ factorId: factor.id, challengeId: challenge.data.id, code });
  setBusy(form, false);
  if (verified.error) {
    setStatus("动态密码不正确或已经过期。", "error");
    return;
  }
  form.reset();
  const { data } = await supabase.auth.getSession();
  setStatus("双重验证成功。", "success");
  await routeSession(data.session);
});

document.querySelector("#start-enrollment").addEventListener("click", async (event) => {
  event.currentTarget.disabled = true;
  setStatus("正在生成验证器绑定信息…");
  const { data, error } = await supabase.auth.mfa.enroll({ factorType: "totp", friendlyName: "True Path M Admin" });
  event.currentTarget.disabled = false;
  if (error) {
    setStatus("无法生成绑定信息，请稍后重试。", "error");
    return;
  }
  enrollmentFactorId = data.id;
  document.querySelector("#totp-qr").src = data.totp.qr_code;
  document.querySelector("#totp-secret").textContent = data.totp.secret;
  document.querySelector("#enrollment-details").hidden = false;
  setStatus("请扫描二维码并输入动态密码。", "success");
});

document.querySelector("#enroll-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const form = event.currentTarget;
  const code = String(new FormData(form).get("code") || "").trim();
  setBusy(form, true);
  const challenge = await supabase.auth.mfa.challenge({ factorId: enrollmentFactorId });
  const verified = challenge.error
    ? { error: challenge.error }
    : await supabase.auth.mfa.verify({ factorId: enrollmentFactorId, challengeId: challenge.data.id, code });
  setBusy(form, false);
  if (verified.error) {
    setStatus("动态密码不正确，请等待新密码后重试。", "error");
    return;
  }
  const { data } = await supabase.auth.getSession();
  setStatus("验证器绑定成功。", "success");
  await routeSession(data.session);
});

messageList.addEventListener("click", async (event) => {
  const button = event.target.closest("button[data-action]");
  const card = event.target.closest("[data-message-id]");
  if (!button || !card) return;
  const message = messages.find((item) => item.id === card.dataset.messageId);
  if (!message) return;
  button.disabled = true;
  let changes;
  if (button.dataset.action === "save-reply") {
    const reply = card.querySelector("textarea").value.trim();
    changes = { reply: reply || null, replied_at: reply ? new Date().toISOString() : null };
  } else {
    changes = { is_visible: !message.is_visible };
  }
  const { error } = await supabase.from("messages").update(changes).eq("id", message.id);
  button.disabled = false;
  if (error) {
    setStatus("保存失败，请确认登录状态后重试。", "error");
    return;
  }
  setStatus(button.dataset.action === "save-reply" ? "回复已保存。" : "公开状态已更新。", "success");
  await loadMessages();
});

document.querySelector(".admin-filter").addEventListener("click", (event) => {
  const button = event.target.closest("button[data-filter]");
  if (!button) return;
  activeFilter = button.dataset.filter;
  document.querySelectorAll("[data-filter]").forEach((item) => item.setAttribute("aria-pressed", String(item === button)));
  renderMessages();
});

document.querySelector("#refresh-messages").addEventListener("click", loadMessages);
document.querySelectorAll('[data-action="signout"]').forEach((button) => {
  button.addEventListener("click", async () => {
    await supabase.auth.signOut();
    messages = [];
    showPanel("login");
    setStatus("已安全退出。", "success");
  });
});

const { data } = await supabase.auth.getSession();
await routeSession(data.session);
