// @ts-check
import { defineConfig } from "astro/config";

// Static one-page site, deployed to Vercel from GitHub (see vercel.json).
export default defineConfig({
  site: "https://rcostudio.nz",
  output: "static",
});
