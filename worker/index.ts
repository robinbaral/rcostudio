// The site's Worker. Every request passes through it (run_worker_first in wrangler.jsonc).
// Pages and files come straight from the static build (dist/). On any address other than
// rcostudio.nz (the workers.dev address while the domain still points at Vercel, preview
// URLs) they carry `X-Robots-Tag: noindex, nofollow`, so search engines leave those copies
// out. Caching for /assets/ and /_astro/ is set in public/_headers.

interface Env {
	ASSETS: { fetch(request: Request): Promise<Response> };
}

const LIVE_HOSTS = new Set(["rcostudio.nz", "www.rcostudio.nz"]);

export default {
	async fetch(request: Request, env: Env): Promise<Response> {
		const response = await env.ASSETS.fetch(request);
		if (LIVE_HOSTS.has(new URL(request.url).hostname)) return response;
		const staged = new Response(response.body, response);
		staged.headers.set("X-Robots-Tag", "noindex, nofollow");
		return staged;
	},
};
