
(() => {
  "use strict";
  const root = document.body;
  if (!root.classList.contains("writing-page")) return;
  const search = document.getElementById("writing-search");
  const kind = document.getElementById("writing-kind");
  const state = document.getElementById("writing-state");
  const priority = document.getElementById("writing-priority");
  const entries = [...document.querySelectorAll(".writing-entry")];
  const groups = [...document.querySelectorAll("[data-collection]")];
  const live = document.getElementById("writing-count");
  const empty = document.getElementById("writing-empty");
  const masteredCount = document.getElementById("writing-mastered-count");
  const testButton = document.getElementById("writing-test");
  const storageKey = "true-path-writing-vocab-v1";
  let marks = {};
  try {
    const stored = JSON.parse(localStorage.getItem(storageKey) || "{}");
    if (stored && typeof stored === "object" && !Array.isArray(stored)) marks = stored;
  } catch { marks = {}; }
  const valid = new Set(["mastered","review"]);
  function save() {
    try { localStorage.setItem(storageKey, JSON.stringify(marks)); } catch {}
    queueSync();
  }
  function applyMark(entry) {
    const current = valid.has(marks[entry.id]) ? marks[entry.id] : "unmarked";
    entry.dataset.state = current;
    entry.querySelectorAll("[data-mark]").forEach(btn => {
      btn.setAttribute("aria-pressed", String(btn.dataset.mark === current));
    });
  }
  function update() {
    const query = search.value.trim().toLocaleLowerCase();
    let shown = 0;
    entries.forEach(entry => {
      const match = (!query || entry.textContent.toLocaleLowerCase().includes(query))
        && (!kind.value || entry.dataset.kind === kind.value)
        && (!state.value || entry.dataset.state === state.value)
        && (!priority.checked || entry.dataset.priority === "1");
      entry.hidden = !match;
      if (match) shown++;
    });
    groups.forEach(group => { group.hidden = !group.querySelector(".writing-entry:not([hidden])"); });
    empty.hidden = shown > 0;
    live.textContent = "显示 " + shown + " / " + entries.length + " 组";
    masteredCount.textContent = String(entries.filter(e => e.dataset.state === "mastered").length);
  }
  entries.forEach(applyMark);
  [search,kind,state,priority].forEach(control => control.addEventListener(control === search ? "input" : "change", update));
  document.querySelectorAll("[data-mark]").forEach(button => button.addEventListener("click", () => {
    const entry = button.closest(".writing-entry");
    const next = button.dataset.mark;
    if (marks[entry.id] === next) delete marks[entry.id];
    else marks[entry.id] = next;
    save();
    applyMark(entry);
    update();
  }));
  testButton.addEventListener("click", () => {
    const on = root.classList.toggle("is-testing");
    testButton.setAttribute("aria-pressed", String(on));
    testButton.textContent = on ? "显示中文 · 结束自测" : "隐藏中文 · 开始自测";
    entries.forEach(entry => {
      entry.classList.remove("is-revealed");
      const reveal = entry.querySelector(".writing-reveal");
      reveal.setAttribute("aria-pressed", "false");
      reveal.textContent = "查看释义";
    });
  });
  document.querySelectorAll(".writing-reveal").forEach(button => button.addEventListener("click", () => {
    const entry = button.closest(".writing-entry");
    const revealed = entry.classList.toggle("is-revealed");
    button.setAttribute("aria-pressed", String(revealed));
    button.textContent = revealed ? "隐藏释义" : "查看释义";
  }));
  document.getElementById("writing-random").addEventListener("click", () => {
    const visible = entries.filter(e => !e.hidden);
    if (!visible.length) { live.textContent = "没有可抽查的词条，请重置筛选"; return; }
    const card = visible[Math.floor(Math.random() * visible.length)];
    entries.forEach(e => e.classList.remove("is-picked"));
    card.classList.add("is-picked");
    if (root.classList.contains("is-testing")) {
      card.classList.remove("is-revealed");
      const reveal = card.querySelector(".writing-reveal");
      reveal.setAttribute("aria-pressed", "false");
      reveal.textContent = "查看释义";
    }
    card.scrollIntoView({behavior:window.matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto" : "smooth", block:"center"});
    card.focus({preventScroll:true});
    live.textContent = "已抽取：" + card.querySelector(".writing-term").textContent;
  });
  document.getElementById("writing-reset").addEventListener("click", () => {
    search.value = ""; kind.value = ""; state.value = ""; priority.checked = false;
    entries.forEach(e => e.classList.remove("is-picked"));
    update();
  });
  document.getElementById("writing-print").addEventListener("click", () => window.print());
  window.addEventListener("storage", event => {
    if (event.key !== storageKey) return;
    try {
      const parsed = JSON.parse(event.newValue || "{}");
      marks = parsed && typeof parsed === "object" && !Array.isArray(parsed) ? parsed : {};
    } catch { marks = {}; }
    entries.forEach(applyMark);
    update();
  });

  // Keep existing local marks; sync a per-browser device to Supabase.
  const syncLabel=document.getElementById("writing-sync-status");
  const baselineKey="true-path-writing-vocab-v1-cloud-baseline";
  const cookieName="tpm_writing_device";
  const api="https://lbnmkxmvdalavcjdxtpy.supabase.co/functions/v1/writing-progress";
  const knownIds=new Set(entries.map(e=>e.id));
  const sanitize=v=>{
    const result={};
    if(v && typeof v==="object"&&!Array.isArray(v))for(const [id,s] of Object.entries(v))if(knownIds.has(id)&&valid.has(s))result[id]=s;
    return result;
  };
  function readJSON(k){try{return JSON.parse(localStorage.getItem(k)||"{}")}catch{return {}}}
  function storeJSON(k,v){try{localStorage.setItem(k,JSON.stringify(v))}catch{}}
  function deviceCookie(){
    try{
      const item=document.cookie.split(";").map(s=>s.trim()).find(s=>s.startsWith(cookieName+"="));
      const existing=item?decodeURIComponent(item.slice(cookieName.length+1)):"";
      if(/^wv1_[0-9a-f]{64}$/.test(existing))return existing;
      if(!window.isSecureContext)return "";
      const bytes=crypto.getRandomValues(new Uint8Array(32));
      const token="wv1_"+[...bytes].map(b=>b.toString(16).padStart(2,"0")).join("");
      document.cookie=cookieName+"="+token+"; Max-Age=31536000; Path=/; SameSite=Lax; Secure";
      return document.cookie.includes(cookieName+"=")?token:"";
    }catch{return ""}
  }
  const token=deviceCookie();
  const fingerprint=token.slice(-16);
  let cloudReady=false,cloudBusy=false,cloudDirty=false,timer=0;
  function setSync(s,mode=""){if(syncLabel){syncLabel.textContent=s;syncLabel.dataset.state=mode}}
  const baseline=()=>{const x=readJSON(baselineKey);return x?.device===fingerprint?sanitize(x.marks):{}};
  const saveBaseline=snapshot=>storeJSON(baselineKey,{device:fingerprint,marks:sanitize(snapshot)});
  const identical=(a,b)=>{const ak=Object.keys(a).sort(),bk=Object.keys(b).sort();return ak.length===bk.length&&ak.every((k,i)=>k===bk[i]&&a[k]===b[k])};
  async function cloud(action,snapshot){
    const abort=new AbortController(),timeout=window.setTimeout(()=>abort.abort(),9000);
    try{
      const response=await fetch(api,{method:"POST",mode:"cors",credentials:"omit",cache:"no-store",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify(action==="read"?{action,cookie:token}:{action,cookie:token,marks:snapshot}),
        signal:abort.signal});
      if(!response.ok)throw new Error("Sync HTTP "+response.status);
      return await response.json();
    }finally{window.clearTimeout(timeout)}
  }
  function queueSync(){
    if(!token){setSync("Cookie 不可用，进度仅保存在本地浏览器。","local");return}
    if(!cloudReady){setSync("进度已保存在本地，等待 Supabase 连接。","pending");return}
    cloudDirty=true;setSync("本地已保存，正在同步…","pending");
    window.clearTimeout(timer);timer=window.setTimeout(flushCloud,700);
  }
  async function flushCloud(){
    if(!cloudReady||cloudBusy||!cloudDirty)return;
    cloudBusy=true;cloudDirty=false;
    const snapshot=sanitize(marks);
    try{
      await cloud("save",snapshot);
      saveBaseline(snapshot);
      setSync("已同步至 Supabase · 使用本机 Cookie 识别","success");
    }catch{
      cloudDirty=true;setSync("云端保存失败，进度仍在本地。","error");
    }finally{
      cloudBusy=false;
      if(!identical(marks,snapshot)){
        cloudDirty=true;window.clearTimeout(timer);timer=window.setTimeout(flushCloud,700);
      }
    }
  }
  async function initializeCloud(){
    if(!token){setSync("Cookie 不可用，记录仅保存在本地。","local");return}
    if(cloudReady){if(cloudDirty)flushCloud();return}
    setSync("正在从 Supabase 恢复进度…","pending");
    try{
      const last=baseline();
      const remote=sanitize((await cloud("read")).marks);
      const local=sanitize(marks);
      const merged={...remote};
      for(const id of knownIds){
        const previous=last[id]||null,current=local[id]||null;
        if(previous!==current){
          if(current)merged[id]=current;
          else delete merged[id];
        }
      }
      marks=sanitize(merged);
      storeJSON(storageKey,marks);
      entries.forEach(applyMark);update();
      saveBaseline(remote);cloudReady=true;
      if(!identical(marks,remote))queueSync();
      else setSync("Supabase 学习记录已恢复。","success");
    }catch{setSync("云端暂不可用，本地记录已保留。","error")}
  }
  window.addEventListener("online",()=>cloudReady?flushCloud():initializeCloud());
  document.addEventListener("visibilitychange",()=>{
    if(document.visibilityState==="visible"){
      if(!cloudReady)initializeCloud();
      else if(cloudDirty)flushCloud();
    }
  });
  update();
  initializeCloud();
})();
