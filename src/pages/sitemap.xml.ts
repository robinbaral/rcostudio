// /sitemap.xml, generated at build time so <lastmod> is the date of each deploy.
import type { APIRoute } from "astro";
import { projects, projectId } from "../data/projects";

// The homepage, Pindrop's page and each project's own address (src/pages/work/).
const pages = ["/", "/pindrop", ...projects.filter((p) => !p.soon).map((p) => `/work/${projectId(p)}`)];

export const GET: APIRoute = ({ site }) => {
  const lastmod = new Date().toISOString();
  const urls = pages
    .map(
      (path) => `  <url>
    <loc>${new URL(path, site).href}</loc>
    <lastmod>${lastmod}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>1.0</priority>
  </url>`,
    )
    .join("\n");
  return new Response(
    `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${urls}
</urlset>
`,
    { headers: { "Content-Type": "application/xml; charset=utf-8" } },
  );
};
