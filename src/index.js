import { EmailMessage } from "cloudflare:email";
import { FROM, parseForm, buildMime } from "./contact.mjs";

// Static files in public/ are served by the assets binding before this runs;
// the Worker only sees /api/contact and paths with no matching file.
export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname !== "/api/contact") return env.ASSETS.fetch(request);
    if (request.method !== "POST") {
      return new Response("Method Not Allowed", { status: 405, headers: { Allow: "POST" } });
    }

    const back = (anchor) => Response.redirect(`${url.origin}/#${anchor}`, 303);
    if (Number(request.headers.get("content-length")) > 20000) return back("form-error");

    let parsed;
    try {
      parsed = parseForm(await request.formData());
    } catch {
      return back("form-error");
    }
    if (parsed.spam) return back("form-sent");
    if (parsed.invalid) return back("form-error");

    // ponytail: honeypot only, add Turnstile if spam gets through.
    try {
      const to = env.CONTACT_TO; // secret, must be a verified Email Routing destination
      await env.MAILER.send(new EmailMessage(FROM, to, buildMime(parsed.fields, to)));
      return back("form-sent");
    } catch (err) {
      console.error("contact form send failed", err);
      return back("form-error");
    }
  },
};
