
const allowedOrigins = new Set(["https://1956799.xyz", "https://www.1956799.xyz"]);
const keyPattern = /^wv1_[a-f0-9]{64}$/;
const idPattern = /^writing-\d{3}$/;

function cors(origin) {
  return {
    "Access-Control-Allow-Origin": allowedOrigins.has(origin) ? origin : "https://1956799.xyz",
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "content-type, apikey, authorization, x-client-info",
    "Access-Control-Max-Age": "86400",
    "Vary": "Origin",
  };
}
function reply(body, status, origin) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { ...cors(origin), "Content-Type": "application/json; charset=utf-8", "Cache-Control": "no-store" },
  });
}
async function hashCookie(cookie) {
  const result = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(cookie));
  return [...new Uint8Array(result)].map(n => n.toString(16).padStart(2, "0")).join("");
}
function cleanMarks(value) {
  if (value === null || typeof value !== "object" || Array.isArray(value)) return null;
  const out = {};
  const entries = Object.entries(value);
  if (entries.length > 68) return null;
  for (const [id, state] of entries) {
    const num = Number(id.slice(8));
    if (!idPattern.test(id) || !Number.isInteger(num) || num < 1 || num > 68 ||
        id !== "writing-" + String(num).padStart(3, "0") || (state !== "mastered" && state !== "review")) return null;
    out[id] = state;
  }
  return out;
}
function serviceKey() {
  const legacy = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY");
  if (legacy) return legacy;
  try {
    const secret = JSON.parse(Deno.env.get("SUPABASE_SECRET_KEYS") || "{}");
    const values = Object.values(secret).flatMap(v => typeof v === "string" ? [v] : typeof v === "object" && v !== null ? Object.values(v) : []);
    return values.find(v => typeof v === "string" && v.startsWith("sb_secret_")) || "";
  } catch { return ""; }
}
Deno.serve(async (request) => {
  const origin = request.headers.get("origin") || "";
  if (!allowedOrigins.has(origin)) return reply({ error: "Origin not allowed" }, 403, origin);
  if (request.method === "OPTIONS") return new Response(null, { status: 204, headers: cors(origin) });
  if (request.method !== "POST") return reply({ error: "Method not allowed" }, 405, origin);
  if (!request.headers.get("content-type")?.includes("application/json")) return reply({ error: "JSON required" }, 415, origin);
  if (Number(request.headers.get("content-length") || 0) > 16000) return reply({ error: "Payload too large" }, 413, origin);

  let body;
  try {
    const raw = await request.text();
    if (raw.length > 16000) return reply({ error: "Payload too large" }, 413, origin);
    body = JSON.parse(raw);
  } catch { return reply({ error: "Invalid JSON" }, 400, origin); }
  if (!body || typeof body !== "object" || !keyPattern.test(body.cookie || "")) return reply({ error: "Invalid device token" }, 400, origin);
  if (body.action !== "read" && body.action !== "save") return reply({ error: "Unknown action" }, 400, origin);
  const marks = body.action === "save" ? cleanMarks(body.marks) : {};
  if (marks === null) return reply({ error: "Invalid progress data" }, 400, origin);

  const url = Deno.env.get("SUPABASE_URL");
  const key = serviceKey();
  if (!url || !key) return reply({ error: "Service unavailable" }, 503, origin);
  const deviceHash = await hashCookie(body.cookie);
  const endpoint = url + "/rest/v1/writing_word_progress";
  const headers = { apikey: key, Authorization: "Bearer " + key, "Content-Type": "application/json", Accept: "application/json" };
  try {
    if (body.action === "read") {
      const response = await fetch(endpoint + "?device_hash=eq." + deviceHash + "&select=marks&limit=1", { method: "GET", headers, signal: AbortSignal.timeout(7000) });
      if (!response.ok) return reply({ error: "Database read failed" }, 503, origin);
      const rows = await response.json();
      return reply({ marks: cleanMarks(rows?.[0]?.marks || {}) || {} }, 200, origin);
    }
    const response = await fetch(endpoint + "?on_conflict=device_hash", {
      method: "POST",
      headers: { ...headers, Prefer: "resolution=merge-duplicates,return=minimal" },
      body: JSON.stringify({ device_hash: deviceHash, marks, updated_at: new Date().toISOString() }),
      signal: AbortSignal.timeout(7000),
    });
    if (!response.ok) return reply({ error: "Database save failed" }, 503, origin);
    return reply({ ok: true }, 200, origin);
  } catch {
    return reply({ error: "Network service unavailable" }, 503, origin);
  }
});
