// The Services section, in order. Wording from the Figma Services frame
// (22:1603), moved from "I" to "we" and toned down to short, plain lines (drafts). The live
// wording is kept in notes/copy.md.

export interface Service {
  id: string;
  name: string;
  lead: string;
  // One paragraph per service (draft, see notes/copy.md).
  text: string;
}

// The left column: the note in paragraphs (the toolkit line moved here from "Small by
// design") and a quiet, contextual contact line (Robin's wording, 2026-11-14).
export const servicesNote = [
  "Not every project needs every step. It can start with strategy, move straight to a prototype or develop an existing product.",
  "A modern toolkit leaves more time to explore ideas, refine the details and create something easy to maintain and build on. We'll work out the right mix together.",
];
export const servicesContact = { lead: "Not sure where yours starts?", link: "Get in touch" };

export const services: Service[] = [
  {
    id: "strategy",
    name: "Strategy",
    lead: "Working out what the project needs to do.",
    text: "Your goals set the direction, and the design follows from them. I find the big idea behind the work: one clear message, carried through, so every part of the project pulls the same way.",
  },
  {
    id: "design",
    name: "Design",
    lead: "Shaping the idea, then the details.",
    text: "Before anything gets designed, I get everyone on board and agree on a shared picture of the direction. From there, a concept takes one idea and works it through into real design choices, down to interfaces that look right and are easy to use.",
  },
  {
    id: "prototyping",
    name: "Prototyping",
    lead: "Trying ideas early, on something real.",
    text: "Prototypes in the browser or on a phone let you click through an idea rather than imagine it, and improve it with each round of feedback. I use your actual words and images, on the screens people will use, so decisions are made on the real thing.",
  },
  {
    id: "development",
    name: "Development",
    lead: "Building it properly, made to last.",
    text: "We refine the chosen concept together, through feedback, then I build what I've designed. The result is a site or app that's fast, accessible and easy to look after.",
  },
  {
    id: "product",
    name: "Product",
    lead: "Looking after products once they're live, and helping them grow.",
    text: "I work with start-ups and teams that already have a product in place. I keep track of what's next, weigh it against your goals and plan each release with you. New features are added step by step to a core that can carry them.",
  },
];
