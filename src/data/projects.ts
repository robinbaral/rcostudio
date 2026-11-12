// The "Selected Projects" list, in display order. Add a project by adding an entry.
//
// - preview: image in public/assets/work/. Use a new filename when replacing an image:
//   /assets/ is cached for a year (vercel.json), so a reused name keeps showing the old one.
// - href: omit for projects without a public link (they still show their preview).
// - soon: greyed out, "Coming soon" on the right, no hover colour.
// - accent: fixed hover colour; otherwise it's taken from the preview image. One colour is
//   darkened or lightened only if it can't be read on that background; { onDark, onLight }
//   sets each background's colour exactly (the section is dark in light OS mode and the
//   other way round).
// - portrait: tall phone screenshot instead of a landscape page.

export interface Project {
  name: string;
  tags: string;
  preview: string;
  href?: string;
  soon?: boolean;
  accent?: string | { onDark: string; onLight: string };
  portrait?: boolean;
}

export const projects: Project[] = [
  { name: "Colombo", tags: "Coming soon", soon: true, preview: "/assets/work/colombo-desktop.webp" },
  {
    name: "CrissCross",
    tags: "Web, App",
    href: "https://www.crisscrosswords.app",
    preview: "/assets/work/crisscross-tiles.webp",
    accent: "#dab6fc",
  },
  {
    name: "ProLog",
    tags: "Branding, Web",
    href: "https://www.prolog.ag",
    preview: "/assets/work/prolog-hero.webp",
    accent: "#ff4713",
  },
  {
    name: "Tommy Pickett",
    tags: "Web",
    href: "https://www.tommypickett.com",
    preview: "/assets/work/tommy-pickett-desktop.webp",
  },
  {
    name: "Event Sitters",
    tags: "Branding, Web",
    href: "https://www.eventsitters.nz",
    preview: "/assets/work/eventsitters-desktop.webp",
  },
  {
    name: "Faster",
    tags: "Web, App",
    // No country code, so it opens each visitor's own App Store.
    href: "https://apps.apple.com/app/id6829356882",
    preview: "/assets/work/faster-hero.webp",
  },
  {
    name: "Schlosskirche",
    tags: "Web",
    href: "https://www.foerderverein-schlosskirche.de",
    preview: "/assets/work/schlosskirche-hero.webp",
  },
  {
    name: "Pindrop",
    tags: "App",
    // No country code, so it opens each visitor's own App Store.
    href: "https://apps.apple.com/app/pindrop-scorecard/id6761825783",
    preview: "/assets/work/pindrop-app.webp",
    portrait: true,
  },
  { name: "Solarkraftwerk", tags: "Branding", preview: "/assets/work/solarkraftwerk-desktop.webp" },
  {
    name: "Helga Digel",
    tags: "Web, Print",
    // The site has no https.
    href: "http://www.helga-digel.de",
    preview: "/assets/work/helga-digel-desktop.webp",
    accent: { onDark: "#dbeec6", onLight: "#809e5f" },
  },
  { name: "Design Week PF", tags: "Branding", preview: "/assets/work/design-week.webp" },
];
