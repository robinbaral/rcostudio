import type { ComponentProps } from "astro/types";
import type CaseBoard from "../components/cases/CaseBoard.astro";

type BoardProps = ComponentProps<typeof CaseBoard>;

// The "Selected Projects" list, in display order. Add a project by adding an entry.
// Each row opens a drawer (src/components/ProjectDrawer.astro) with the preview image, the
// summary, the services and a link out.
//
// Images are named by their path in src/assets/ ("work/prolog-hero.png"): high-resolution
// sources (2x screenshots, 2880x1800 for a 1440x900 page; phone shots 780x1688) that Astro
// turns into WebP at several sizes (src/lib/shots.ts). Built files get a content hash, so a
// source can be replaced under the same name. A path starting with /assets/ is an older WebP
// in public/ and is used as it is.
//
// - preview: shown on hover and at the top of the drawer. Optional for coming-soon projects,
//   which never show a hover image anyway (Robin, 2026-11-15).
// - tags: the short list on the row itself.
// - gallery: more 16:10 shots (sections of the site) shown below the preview in the drawer.
//   Captured with a headless browser at 2x.
// - galleryBleed: the gallery images are composed boards with their own background (sketches,
//   print layouts), so they fill their block edge to edge instead of sitting inset in a frame
//   like site screenshots. The preview above them stays framed; "all" lets it fill its block
//   too (when the preview is a composed board as well). galleryFramed lists images that stay
//   framed anyway (site screenshots among boards).
// - galleryBoard: a case board (src/components/cases/CaseBoard.astro, same props) shown after
//   the gallery, edge to edge. Its background is the --board token, so it follows dark mode,
//   where a board saved as one image keeps its light background.
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
// - caseStudy: path of the project's case page ("/cases/prolog"), linked first in the drawer.
// - soon: greyed out, "Coming soon" on the right, no hover colour, no link in the drawer.
// - accent: fixed hover colour; otherwise it's taken from the preview image. One colour is
//   darkened or lightened only if it can't be read on that background; { onDark, onLight }
//   sets each background's colour exactly (the section is dark in light OS mode and the
//   other way round).
// - portrait: tall phone screenshot instead of a landscape page.
// - stack: extra cards for the homepage hero stack (posters, covers …), captioned with the
//   project and their own tags. They're dealt in one after each of the projects that follow, so the project's own
//   cards don't sit in a row.

export interface Project {
  name: string;
  tags: string;
  preview?: string;
  // false: the preview stays out of the hero stack (hover and drawer still use it).
  heroCard?: boolean;
  summary: string | string[];
  services: string[];
  href?: string;
  appStore?: string;
  caseStudy?: string;
  linkLabel?: string;
  soon?: boolean;
  accent?: string | { onDark: string; onLight: string };
  portrait?: boolean;
  gallery?: string[];
  galleryBleed?: boolean | "all";
  galleryFramed?: string[];
  galleryBoard?: BoardProps;
  drawerImage?: string;
  galleryMobile?: string[];
  video?: { desktop: string; mobile: string; poster: string; mobilePoster: string };
  stack?: { image: string; tags: string }[];
}

export const projects: Project[] = [
  {
    name: "Colombo",
    tags: "Coming soon",
    soon: true,
    preview: "work/colombo-desktop.png",
    summary:
      "A winery, cellar door and pizza place in Martinborough. A new website with the wine shop, events and food menu, all kept up to date by the team in one place.",
    services: ["Brand", "Web design", "Development", "Content management", "Online shop"],
  },
  {
    // Coming soon: no image yet, so no hover preview and no hero card. No summary for now
    // (Robin, 2026-11-16).
    name: "Pop Drop",
    tags: "Coming soon",
    soon: true,
    summary: [],
    services: ["App design", "iOS development"],
  },
  {
    name: "CrissCross",
    tags: "Web, App",
    href: "https://www.crisscrosswords.app",
    // No country code, so it opens each visitor's own App Store.
    appStore: "https://apps.apple.com/app/id6781901433",
    caseStudy: "/cases/crisscross",
    preview: "work/crisscross-tiles.png",
    // Website sections with the app itself on iPad and iPhone in between.
    gallery: [
      "work/crisscross-section-1.png",
      "work/crisscross-devices-1.png",
      "work/crisscross-section-2.png",
      "work/crisscross-devices-2.png",
      "work/crisscross-section-3.png",
    ],
    accent: "#dab6fc",
    summary: [
      "CrissCross is a crossword and spelling app for children, on iPhone and iPad. Letter tiles instead of a keyboard, no ads, no subscription, and it works offline.",
      "The app is the visible part. Behind it sits a word set of thousands of answers with clues for young readers, in British and American English, and Puzzle Studio, a tool built to write, generate, review and version more than 800 puzzles and send them straight into the app.",
      "Every answer can be read aloud: every word is transcribed into audio and checked by ear, with exact pronunciations where a voice gets it wrong. In its latest version the app adapts to iPad and iPhone Duo, and its website lets visitors play a puzzle before downloading.",
    ],
    services: ["Brand", "App design", "iOS development", "Puzzle authoring tool", "Word set and audio", "iPad and iPhone Duo", "Website"],
  },
  {
    name: "ProLog",
    tags: "Branding, Web",
    href: "https://www.prolog.ag",
    caseStudy: "/cases/prolog",
    preview: "work/prolog-hero.png",
    gallery: [
      "work/prolog-section-1.png",
      "work/prolog-section-2.png",
      "work/prolog-section-3.png",
      "work/prolog-section-4.png",
    ],
    // The page concepts board from the case (article, sector and audit pages), drawn the same
    // way, so its background follows dark mode. The middle page sits lower, as on the first
    // version of the board (Robin liked the uneven tops).
    galleryBoard: {
      folder: "cases/prolog/boards/prolog-page-concepts",
      alt: "Three page designs side by side: a blog article, a page for public administration and an audit page",
      phoneRows: [[0, 2]],
      crop: 2,
      phoneCrop: 1.5,
      drops: [0, 3.75, 0],
      gap: 3.1,
    },
    accent: "#ff4713",
    summary: [
      "ProLog is a log management system from Germany that runs entirely offline, made for companies working to GDPR, ISO 27001 and NIS2.",
      "In IT security, much of the work happens out of sight. Together with the client, I went through several rounds to find how a modern security company should come across online: credible and clear, without giving too much away. The result tells a complete story with a light touch, and leaves room for the conversations that follow.",
      "The design grew step by step, from early sketches to clickable prototypes the team could try out and comment on. I then built the full site in Webflow and handed it over at the end of the project, ready for the client to run and add to.",
    ],
    services: ["Brand", "Logo", "Web design", "Prototyping", "Webflow build", "Presentation design"],
  },
  {
    name: "Tommy Pickett",
    tags: "Web",
    href: "https://www.tommypickett.com",
    caseStudy: "/cases/tommy-pickett",
    preview: "work/tommy-pickett-desktop.png",
    gallery: ["work/tommy-pickett-section-1.png", "work/tommy-pickett-section-2.png", "work/tommy-pickett-section-3.png"],
    summary: [
      "Tommy Pickett is a singer-songwriter on Waiheke Island, playing original folk-rock songs and familiar covers around New Zealand.",
      "After many years on an older site, the website got a fresh look that puts the music, tour dates and bookings up front. It's built with Astro and a headless CMS, with an editing side designed around the site itself, so Tommy can keep dates, albums and videos up to date without help: simple and straightforward.",
      "Alongside the site, I help him out with some of what surrounds the music: album covers, posters for his tours, and getting new releases out across streaming and other channels, with the artwork and assets each one needs.",
    ],
    services: ["Brand", "Web design", "Astro build", "Content management", "Album covers", "Tour posters"],
    stack: [
      { image: "cases/tommy-pickett/tommy-pickett-stack-poster-2025.png", tags: "Tour poster" },
      { image: "cases/tommy-pickett/tommy-pickett-stack-cover-streetlights.png", tags: "Album cover" },
      { image: "cases/tommy-pickett/tommy-pickett-stack-cover-dive-deep.png", tags: "Album cover" },
    ],
  },
  {
    name: "Event Sitters",
    tags: "Branding, Web",
    href: "https://www.eventsitters.nz",
    preview: "work/eventsitters-hero.png",
    gallery: ["work/event-sitters-section-1.png", "work/event-sitters-section-2.png", "work/event-sitters-section-3.png"],
    galleryMobile: [
      "work/event-sitters-mobile-1.png",
      "work/event-sitters-mobile-2.png",
      "work/event-sitters-mobile-3.png",
      "work/event-sitters-mobile-4.png",
    ],
    summary: [
      "Event Sitters is a small company in Hawke's Bay, run by Samantha, that brings kids' entertainment to weddings, parties and events, on site.",
      "Working together started with finding the name. From there I built a logo and a visual style that lean fully into what Event Sitters does: bright, playful and easy to recognise, for kids and grown-ups alike.",
      "The style carries through everything the business puts out: the website, print communications and the materials used at events, from custom colouring sheets to badges and flags.",
    ],
    services: ["Naming", "Brand", "Logo and visual style", "Web design", "Print", "Event materials"],
  },
  {
    name: "Faster",
    tags: "Web, App",
    href: "https://robinbaral.github.io/faster/",
    // No country code, so it opens each visitor's own App Store.
    appStore: "https://apps.apple.com/app/id6829356882",
    preview: "work/faster-hero.png",
    gallery: ["work/faster-section-1.png", "work/faster-section-2.png", "work/faster-section-3.png", "work/faster-section-4.png"],
    summary: [
      "Faster is a fasting timer for iPhone and Apple Watch. It shows which phase of a fast you're in and what that means, with no account and no tracking.",
      "The challenge was making complex data simple to read and fun to use. The answer was a clean, diagram-style interface, refined over many rounds on both the phone and the watch.",
      "The result works at a glance, with plenty of depth for anyone who wants to dive deeper: learning more about each phase, gaining insights from past fasts, or finding structure and encouragement in a regular schedule.",
    ],
    services: ["App design", "iOS and watchOS development", "Widgets", "Website"],
  },
  {
    name: "Schlosskirche",
    tags: "Web",
    href: "https://www.foerderverein-schlosskirche.de",
    preview: "work/schlosskirche-hero.png",
    gallery: ["work/schlosskirche-section-1.png", "work/schlosskirche-section-2.png", "work/schlosskirche-section-3.png"],
    galleryMobile: [
      "work/schlosskirche-mobile-1.png",
      "work/schlosskirche-mobile-2.png",
      "work/schlosskirche-mobile-3.png",
      "work/schlosskirche-mobile-4.png",
    ],
    // Robin's picks: the site's own yellow on the dark section (light OS mode), deep blue on white.
    accent: { onDark: "#f8e850", onLight: "#2e4057" },
    summary: [
      "The supporters' association of the Schlosskirche St. Michael in Pforzheim keeps the church's music and cultural life going.",
      "It started with a campaign to raise money for a new organ. It ran on billboards, flyers and roll-ups and at events, alongside a website for pipe sponsorships, where people could adopt one of the organ's pipes.",
      "With the organ funded, the site became a home for the association as a whole: a place to win new members, raise donations and promote its concerts and events, all run by the association itself.",
    ],
    services: ["Fundraising campaign", "Billboards, flyers and roll-ups", "Event support", "Web design", "Squarespace build"],
  },
  {
    name: "Pindrop",
    tags: "Web, App",
    href: "https://robinbaral.github.io/pindrop/",
    // No country code, so it opens each visitor's own App Store.
    appStore: "https://apps.apple.com/app/pindrop-scorecard/id6761825783",
    // The OG image from Figma "Pindrop Screens" (node 6:2, exported at 3x), reframed to 16:10 on
    // the light grey of the App Store board: logo lockup and phone, the phone cut off at the
    // bottom as in the original.
    preview: "work/pindrop-og.png",
    heroCard: false, // the stack shows the red phone card instead (Robin, 2026-11-16)
    // Then the website (top of the page, captured at 2x), the three App Store screens side by
    // side (06_Production/App Store in the Pindrop folder) and six plain screens from Figma
    // as phones, three per board (scripts/cases/pindrop-boards.py), plus a card on the app's red
    // for the hero stack.
    gallery: [
      "work/pindrop-website.png",
      "work/pindrop-appstore.png",
      "work/pindrop-screens-1.png",
      "work/pindrop-screens-2.png",
    ],
    // Every slide fills its block (the OG image is on the App Store board's light grey for
    // that), except the website screenshot, framed like the other sites.
    galleryBleed: "all",
    galleryFramed: ["work/pindrop-website.png"],
    stack: [{ image: "work/pindrop-hero.png", tags: "App" }],
    // Dark grey, so the row still shows a hover (the black-and-white preview gives no colour).
    accent: "#4a4a4a",
    summary: [
      "Pindrop is my own score tracker for Finska, the throwing game, on iPhone.",
      "It started as a UI exercise in physicality: what if keeping score felt more like handling the pins than filling in a form? So scores are dragged down and misses swiped away.",
      "It quickly became my favourite way to score a game, whether in the backyard or at the beach.",
    ],
    services: ["App design", "iOS development", "Website"],
  },
  {
    name: "Solarkraftwerk",
    tags: "Branding",
    preview: "/assets/work/solarkraftwerk-desktop.webp",
    // From the brand presentation (Solarkraftwerk Ideen.pdf) and the print files, drawn by
    // scripts/cases/solarkraftwerk-boards.py: logo ideas as pencil sketches like ProLog's, the
    // final mark and how it's built, the landscape and portrait business card drafts, then the
    // roof banner and flyer.
    gallery: [
      "work/solarkraftwerk-logo-sketches.png",
      "work/solarkraftwerk-logo.png",
      "work/solarkraftwerk-cards-landscape.png",
      "work/solarkraftwerk-cards-portrait.png",
      "work/solarkraftwerk-print.png",
    ],
    galleryBleed: true,
    // Robin's picks: a warm yellow from the brand on the dark section, near-black slate on white.
    accent: { onDark: "#ffe433", onLight: "#2a2e33" },
    summary: [
      "Solarkraftwerk came to me with its name settled and the company ready to launch. What it needed was a brand to launch with.",
      "We went through the full branding process together, from rounds of logo design to everything the business puts out: stationery, print, banners and shirts, and the graphics for two company cars.",
      "At the centre sat a concept for the website. The team built the site from the design in Squarespace themselves and runs it on its own, with my technical support when it's needed.",
    ],
    services: ["Brand", "Logo design", "Corporate design", "Stationery and print", "Apparel", "Vehicle graphics", "Website concept"],
  },
  {
    name: "Helga Digel",
    tags: "Web, Print",
    // The site has no https.
    href: "http://www.helga-digel.de",
    preview: "work/helga-digel-desktop.png",
    accent: { onDark: "#dbeec6", onLight: "#809e5f" },
    summary: [
      "Helga Digel is an artist in Pforzheim, working in drawing, painting, collage and objects.",
      "She came to me wanting a website that puts the artwork front and centre. So the site holds back: a calm palette, plenty of space and grid layouts that let each piece set the pace, whether it's a single drawing or a whole series.",
      "Works, exhibitions, acquisitions and her biography each sit in the same quiet frame, so the art always stays the main thing. Business cards followed in the same style.",
    ],
    services: ["Web design", "Development", "Business cards"],
  },
  {
    name: "Design Week PF",
    tags: "Branding",
    preview: "work/design-week.png",
    // Context from Robin (2026-11-15): the organisers approached him; a pitch to the city
    // centre's retailers, never carried out. Summary is a draft.
    summary: [
      "The organisers of a planned design week in Pforzheim came to me with an idea: bring the city centre's retailers together, as members of the local retail association, for a programme of events and activities around town that would draw more people into the centre and its shops.",
      "To get everyone on board, I developed the identity and the full range of communication for the pitch: posters for various applications, banners and flyers for the members, a website, advertising, social media campaigns, partner logos and newspaper inserts.",
      "The concept was well received at first, but the event was eventually called off and never went ahead.",
    ],
    services: ["Brand", "Campaign", "Posters and print", "Website", "Social media", "Pitch"],
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
