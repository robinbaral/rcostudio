// The site's Worker. Every request passes through it (run_worker_first in wrangler.jsonc).
// Pages and files come straight from the static build (dist/). On any address other than
// rcostudio.nz (the workers.dev address while the domain still points at Vercel, preview
// URLs) they carry `X-Robots-Tag: noindex, nofollow`, so search engines leave those copies
// out. www.rcostudio.nz forwards to rcostudio.nz (301). Caching for /assets/ and /_astro/ is
// set in public/_headers.

interface Env {
	ASSETS: { fetch(request: Request): Promise<Response> };
}

const LIVE_HOSTS = new Set(["rcostudio.nz", "www.rcostudio.nz"]);

export default {
	async fetch(request: Request, env: Env): Promise<Response> {
		const url = new URL(request.url);
		// One address for the site: www forwards to the bare domain, keeping the path, so search
		// engines don't see the same pages twice.
		if (url.hostname === "www.rcostudio.nz") {
			url.hostname = "rcostudio.nz";
			return Response.redirect(url.toString(), 301);
		}
		const response = await env.ASSETS.fetch(request);
		if (LIVE_HOSTS.has(url.hostname)) return response;
		const staged = new Response(response.body, response);
		staged.headers.set("X-Robots-Tag", "noindex, nofollow");
		return staged;
	},
};
