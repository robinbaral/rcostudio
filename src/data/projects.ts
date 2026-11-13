// The "Selected Projects" list, in display order. Add a project by adding an entry.
// Each row opens a drawer (src/components/ProjectDrawer.astro) with the preview image, the
// summary, the services and a link out.
//
// - preview: image in public/assets/work/, shown on hover and at the top of the drawer. Use a
//   new filename when replacing an image: /assets/ is cached for a year (vercel.json), so a
//   reused name keeps showing the old one.
// - tags: the short list on the row itself.
// - gallery: more 1440x900 shots (sections of the site) that crossfade after the preview in
//   the drawer. Made with a headless browser; same naming rule as preview.
// - drawerImage: a 16:10 image to open the drawer with instead of the preview (for portrait
//   previews, which don't fit the frame). The hover keeps the preview.
// - galleryMobile: phone shots of the same sections, in the same order as [preview,
//   ...gallery]. Shown in a phone frame over the desktop shot, switching in step.
// - video: a slow scroll down the site (desktop), with the same scroll on a phone on top. Used
//   instead of the gallery when set. Recorded with a headless browser; posters are the first
//   frames.
// - summary: the drawer text, one string or a list of paragraphs (drafts until Robin
//   confirms them, see notes/copy.md).
// - services: what R&Co did, listed at the bottom of the drawer.
// - href: omit for projects without a public link. linkLabel overrides the button text.
// - appStore: an App Store link shown next to the website link ("Download on the App Store").
// - soon: greyed out, "Coming soon" on the right, no hover colour, no link in the drawer.
// - accent: fixed hover colour; otherwise it's taken from the preview image. One colour is
//   darkened or lightened only if it can't be read on that background; { onDark, onLight }
//   sets each background's colour exactly (the section is dark in light OS mode and the
//   other way round).
// - portrait: tall phone screenshot instead of a landscape page.

export interface Project {
  name: string;
  tags: string;
  preview: string;
  summary: string | string[];
  services: string[];
  href?: string;
  appStore?: string;
  linkLabel?: string;
  soon?: boolean;
  accent?: string | { onDark: string; onLight: string };
  portrait?: boolean;
  gallery?: string[];
  drawerImage?: string;
  galleryMobile?: string[];
  video?: { desktop: string; mobile: string; poster: string; mobilePoster: string };
}

export const projects: Project[] = [
  {
    name: "Colombo",
    tags: "Coming soon",
    soon: true,
    preview: "/assets/work/colombo-desktop-v2.webp",
    summary:
      "A winery, cellar door and pizza place in Martinborough. A new website with the wine shop, events and food menu, all kept up to date by the team in one place.",
    services: ["Web design", "Development", "Content management", "Online shop"],
  },
  {
    name: "CrissCross",
    tags: "Web, App",
    href: "https://www.crisscrosswords.app",
    // No country code, so it opens each visitor's own App Store.
    appStore: "https://apps.apple.com/app/id6781901433",
    preview: "/assets/work/crisscross-tiles.webp",
    // Website sections with the app itself on iPad and iPhone in between.
    gallery: [
      "/assets/work/crisscross-section-1.webp",
      "/assets/work/crisscross-devices-1.webp",
      "/assets/work/crisscross-section-2.webp",
      "/assets/work/crisscross-devices-2.webp",
      "/assets/work/crisscross-section-3.webp",
      "/assets/work/crisscross-devices-3.webp",
      "/assets/work/crisscross-section-4.webp",
    ],
    accent: "#dab6fc",
    summary: [
      "CrissCross is our own crossword and spelling app for children from around age 8, on iPhone and iPad. Letter tiles instead of a keyboard, no ads, no subscriptions, and it works offline.",
      "It started as a practice tool for one young reader and grew into a full app for other families. Behind it sits a custom authoring tool that keeps more than 800 puzzles, their clues and audio in one place and sends them straight into the app, so new packs can be added and kept up to date without touching the code.",
      "Every answer can be read aloud from recorded audio that works offline, and the app speaks and spells in both British and American English. Alongside the app, we built its website.",
    ],
    services: ["App design", "iOS development", "Puzzle authoring tool", "Audio and localisation", "Website"],
  },
  {
    name: "ProLog",
    tags: "Branding, Web",
    href: "https://www.prolog.ag",
    preview: "/assets/work/prolog-hero.webp",
    gallery: ["/assets/work/prolog-section-1.webp", "/assets/work/prolog-section-2.webp", "/assets/work/prolog-section-3.webp", "/assets/work/prolog-section-4.webp"],
    accent: "#ff4713",
    summary: [
      "ProLog is a log management system from Germany that runs entirely offline, made for companies working to GDPR, ISO 27001 and NIS2.",
      "In IT security, much of the work happens out of sight. Together with the client, we went through several rounds to find how a modern security company should come across online: credible and clear, without giving too much away. The result tells a complete story with a light touch, and leaves room for the conversations that follow.",
      "The design grew step by step, from early sketches to clickable prototypes the team could try out and comment on. We then built the full site in Webflow and handed it over at the end of the project, ready for the client to run and add to.",
    ],
    services: ["Logo and branding", "Web design", "Prototyping", "Webflow build", "Presentation design"],
  },
  {
    name: "Tommy Pickett",
    tags: "Web",
    href: "https://www.tommypickett.com",
    preview: "/assets/work/tommy-pickett-desktop.webp",
    gallery: ["/assets/work/tommy-pickett-section-1.webp", "/assets/work/tommy-pickett-section-2.webp", "/assets/work/tommy-pickett-section-3.webp"],
    summary: [
      "Tommy Pickett is a singer-songwriter on Waiheke Island, playing original folk-rock songs and familiar covers around New Zealand.",
      "After many years on an older site, the website got a fresh look that puts the music, tour dates and bookings up front. It's built with Astro and a headless CMS, with an editing side designed around the site itself, so Tommy can keep dates, albums and videos up to date without help: simple and straightforward.",
      "Alongside the site, we design the album covers and the posters for each year's tour, and support the music's release across streaming and other channels, with the artwork and assets each one needs.",
    ],
    services: ["Web design", "Astro build", "Content management", "Album covers", "Tour posters"],
  },
  {
    name: "Event Sitters",
    tags: "Branding, Web",
    href: "https://www.eventsitters.nz",
    preview: "/assets/work/eventsitters-hero-v2.webp",
    gallery: ["/assets/work/event-sitters-section-1.webp", "/assets/work/event-sitters-section-2.webp", "/assets/work/event-sitters-section-3.webp"],
    galleryMobile: [
      "/assets/work/event-sitters-mobile-1.webp",
      "/assets/work/event-sitters-mobile-2.webp",
      "/assets/work/event-sitters-mobile-3.webp",
      "/assets/work/event-sitters-mobile-4.webp",
    ],
    summary: [
      "Event Sitters is a small company in Hawke's Bay, run by Samantha, that brings kids' entertainment to weddings, parties and events, on site.",
      "Working together started with finding the name. From there we built a logo and a visual style that lean fully into what Event Sitters does: bright, playful and easy to recognise, for kids and grown-ups alike.",
      "The style carries through everything the business puts out: the website, print communications and the materials used at events, from custom colouring sheets to badges and flags.",
    ],
    services: ["Naming", "Logo and visual style", "Web design", "Print", "Event materials"],
  },
  {
    name: "Faster",
    tags: "Web, App",
    href: "https://robinbaral.github.io/faster/",
    // No country code, so it opens each visitor's own App Store.
    appStore: "https://apps.apple.com/app/id6829356882",
    preview: "/assets/work/faster-hero.webp",
    gallery: ["/assets/work/faster-section-1.webp", "/assets/work/faster-section-2.webp", "/assets/work/faster-section-3.webp", "/assets/work/faster-section-4.webp"],
    summary: [
      "Faster is our own fasting timer for iPhone and Apple Watch. It shows which phase of a fast you're in and what that means, with no account and no tracking.",
      "It began with a challenge: making complex data simple to read. The answer was a clean, diagram-style interface, refined over many rounds on both the phone and the watch.",
      "What came out is simple to use and clean to look at, with plenty of depth underneath for anyone who wants to look back over their fasts.",
    ],
    services: ["App design", "iOS and watchOS development", "Widgets", "Website"],
  },
  {
    name: "Schlosskirche",
    tags: "Web",
    href: "https://www.foerderverein-schlosskirche.de",
    preview: "/assets/work/schlosskirche-hero.webp",
    gallery: ["/assets/work/schlosskirche-section-1.webp", "/assets/work/schlosskirche-section-2.webp", "/assets/work/schlosskirche-section-3.webp"],
    galleryMobile: [
      "/assets/work/schlosskirche-mobile-1.webp",
      "/assets/work/schlosskirche-mobile-2.webp",
      "/assets/work/schlosskirche-mobile-3.webp",
      "/assets/work/schlosskirche-mobile-4.webp",
    ],
    // Robin's picks: the site's own yellow on the dark section (light OS mode), deep blue on white.
    accent: { onDark: "#f8e850", onLight: "#2e4057" },
    summary: [
      "The supporters' association of the Schlosskirche St. Michael in Pforzheim keeps the church's music and cultural life going.",
      "Our work together started with a campaign to raise money for a new organ. It ran on billboards, flyers and roll-ups and at events, alongside a website for pipe sponsorships, where people could adopt one of the organ's pipes.",
      "With the organ funded, the site became a home for the association as a whole: a place to win new members, raise donations and promote its concerts and events, all run by the association itself.",
    ],
    services: ["Fundraising campaign", "Billboards, flyers and roll-ups", "Event support", "Web design", "Squarespace build"],
  },
  {
    name: "Pindrop",
    tags: "App",
    // No country code, so it opens each visitor's own App Store.
    href: "https://apps.apple.com/app/pindrop-scorecard/id6761825783",
    preview: "/assets/work/pindrop-app.webp",
    portrait: true,
    // Three App Store screens side by side (from 06_Production/Web/App Store in the Pindrop folder).
    drawerImage: "/assets/work/pindrop-appstore.webp",
    // Dark grey, so the row still shows a hover (the black-and-white preview gives no colour).
    accent: "#4a4a4a",
    summary: [
      "Pindrop is our own score tracker for Finska, the throwing game, on iPhone.",
      "It started as a UI exercise in physicality: what if keeping score felt more like handling the pins than filling in a form? So scores are dragged down and misses swiped away.",
      "It quickly became our favourite way to score a game, whether in the backyard or at the beach.",
    ],
    services: ["App design", "iOS development"],
  },
  {
    name: "Solarkraftwerk",
    tags: "Branding",
    preview: "/assets/work/solarkraftwerk-desktop.webp",
    // Robin's picks: a warm yellow from the brand on the dark section, near-black slate on white.
    accent: { onDark: "#ffe433", onLight: "#2a2e33" },
    summary:
      "A corporate design carried through everything the company puts out: banners, vehicle graphics, flyers, the website and shirts.",
    services: ["Corporate design", "Vehicle graphics", "Print", "Website"],
  },
  {
    name: "Helga Digel",
    tags: "Web, Print",
    // The site has no https.
    href: "http://www.helga-digel.de",
    preview: "/assets/work/helga-digel-desktop.webp",
    accent: { onDark: "#dbeec6", onLight: "#809e5f" },
    summary: [
      "Helga Digel is an artist in Pforzheim, working in drawing, painting, collage and objects.",
      "She came to us wanting a website that puts the artwork front and centre. So the site holds back: a calm palette, plenty of space and grid layouts that let each piece set the pace, whether it's a single drawing or a whole series.",
      "Works, exhibitions, acquisitions and her biography each sit in the same quiet frame, so the art always stays the main thing. Business cards followed in the same style.",
    ],
    services: ["Web design", "Development", "Business cards"],
  },
  {
    name: "Design Week PF",
    tags: "Branding",
    preview: "/assets/work/design-week.webp",
    summary: "Branding for a design week in Pforzheim, from the first concepts to the finished identity.",
    services: ["Branding", "Concept presentations"],
  },
];

// A stable id for each project's drawer content ("Tommy Pickett" → "tommy-pickett").
export const projectId = (p: Project) =>
  p.name
    .toLowerCase()
    .normalize("NFD")
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/(^-|-$)/g, "");

// The link button's text: App Store links say so, everything else is a website.
export const projectLinkLabel = (p: Project) =>
  p.linkLabel ?? (p.href?.includes("apps.apple.com") ? "View on the App Store" : "Visit website");
