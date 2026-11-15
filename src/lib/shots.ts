// Project and case images, built by Astro from high-resolution sources.
//
// Sources live in src/assets/ (2x screenshots as PNG: 2880x1800 for a 1440x900 page). Astro
// turns each into WebP at several widths with a light touch (QUALITY), so small text and
// buttons stay crisp, and the browser picks the size it needs (srcset). Built files get a
// content hash in their name, so a replaced source never shows a cached old version.
//
// In src/data/projects.ts an image is named by its path inside src/assets/
// ("work/prolog-hero.png"). Paths starting with /assets/ are older WebPs in public/ and are
// used as they are until they get a source here.
import type { ImageMetadata } from "astro";
import { getImage } from "astro:assets";
import path from "node:path";
import sharp from "sharp";

const QUALITY = 90;
const WIDTHS = [720, 1080, 1440, 2160, 2880];

const sources = import.meta.glob<{ default: ImageMetadata }>("/src/assets/**/*.{png,jpg,jpeg,webp}", { eager: true });

export interface Shot {
  src: string;
  srcset?: string;
  width: number;
  height: number;
}

export function source(name: string): ImageMetadata | undefined {
  return sources[`/src/assets/${name}`]?.default;
}

// One image, ready for <img src srcset width height>. `width` is the size for plain-src uses
// (the hover preview, posters); the srcset covers the rest.
export async function shot(name: string, width = 1440): Promise<Shot> {
  const meta = source(name);
  if (!meta) {
    // Older images in public/: used as they are, with their real size read from the file
    // (the hero stack sizes each card from it, e.g. portrait phone shots).
    if (name.startsWith("/")) {
      const { width = 1440, height = 900 } = await sharp(path.join(process.cwd(), "public", name)).metadata();
      return { src: name, width, height };
    }
    throw new Error(`No image source at src/assets/${name}`);
  }
  const widths = WIDTHS.filter((w) => w < meta.width).concat(meta.width);
  const img = await getImage({ src: meta, format: "webp", quality: QUALITY, widths });
  const single = await getImage({ src: meta, format: "webp", quality: QUALITY, width: Math.min(width, meta.width) });
  return { src: single.src, srcset: img.srcSet.attribute, width: meta.width, height: meta.height };
}

// Several at once, keyed by name.
export async function shots(names: (string | undefined)[], width?: number) {
  const list = [...new Set(names.filter((n): n is string => !!n))];
  const done = await Promise.all(list.map((n) => shot(n, width)));
  return new Map(list.map((n, i) => [n, done[i]]));
}
