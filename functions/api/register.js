// Cloudflare Pages Function: POST /api/register
// Stores each registration in the KV namespace bound as REGISTRATIONS.
// Optional: set NOTIFY_WEBHOOK (e.g. a Zapier catch hook) to forward each signup.

const json = (body, status = 200) =>
  new Response(JSON.stringify(body), {
    status,
    headers: { "Content-Type": "application/json", "Cache-Control": "no-store" },
  });

export async function onRequestPost({ request, env }) {
  let data;
  try {
    data = await request.json();
  } catch {
    return json({ ok: false, error: "Invalid JSON" }, 400);
  }

  // Honeypot: bots fill the hidden "website" field.
  if (data.website) return json({ ok: true });

  const email = String(data.email || "").trim().toLowerCase();
  const name = String(data.name || "").trim();
  if (!name || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    return json({ ok: false, error: "Name and a valid email are required" }, 400);
  }

  const clip = (v, n = 2000) => String(v ?? "").slice(0, n);
  const record = {
    name: clip(name, 200),
    email,
    phone: clip(data.phone, 40),
    state: clip(data.state, 60),
    commitment: clip(data.commitment, 80),
    timeline: clip(data.timeline, 80),
    involvement: [].concat(data.involvement || []).map((v) => clip(v, 80)),
    message: clip(data.message),
    updates: data.updates === "yes",
    submittedAt: new Date().toISOString(),
    country: request.headers.get("cf-ipcountry") || "",
  };

  if (!env.REGISTRATIONS) return json({ ok: false, error: "Storage not configured" }, 500);
  await env.REGISTRATIONS.put(`reg:${email}`, JSON.stringify(record));

  if (env.NOTIFY_WEBHOOK) {
    try {
      await fetch(env.NOTIFY_WEBHOOK, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(record),
      });
    } catch {}
  }
  return json({ ok: true });
}

export const onRequest = () => json({ ok: false, error: "Method not allowed" }, 405);
