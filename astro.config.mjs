// @ts-check
import { defineConfig } from "astro/config";

// Static site, deployed to Cloudflare from GitHub (see wrangler.jsonc). Pages are built as
// files (cases/prolog.html, not cases/prolog/index.html), so Cloudflare serves them without
// a trailing slash, the addresses the site has always used.
export default defineConfig({
  site: "https://rcostudio.nz",
  output: "static",
  trailingSlash: "never",
  build: { format: "file" },
});
