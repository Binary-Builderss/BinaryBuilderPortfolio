// Runs only for "/" (see run_worker_first in wrangler.jsonc); every other path is served straight from public/.
// Visitors from Italy land on /it/. The language link on the home pages goes to /?lang=en|it, which
// stores the choice in a cookie that wins over the country from then on.
const YEAR = 60 * 60 * 24 * 365;

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    // Paths with no matching file also reach the Worker: let the assets layer answer them with the 404 page.
    if (url.pathname !== "/") return env.ASSETS.fetch(request);
    const chosen = url.searchParams.get("lang");
    if (chosen === "en" || chosen === "it") {
      return new Response(null, {
        status: 302,
        headers: {
          Location: chosen === "it" ? "/it/" : "/",
          "Set-Cookie": `lang=${chosen}; Path=/; Max-Age=${YEAR}; SameSite=Lax; Secure`,
        },
      });
    }
    const saved = request.headers.get("Cookie")?.match(/(?:^|;\s*)lang=(en|it)\b/)?.[1];
    const lang = saved ?? (request.cf?.country === "IT" ? "it" : "en");
    if (lang === "it") return Response.redirect(new URL("/it/" + url.search, url), 302);
    return env.ASSETS.fetch(request);
  },
};
