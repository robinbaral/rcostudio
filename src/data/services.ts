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

// The left column: a note and a quiet, contextual contact line (drafts, see notes/copy.md).
export const servicesNote =
  "Not every project needs every step. Some start with strategy, others go straight to a prototype or pick up a product that's already running, and sometimes we work with your team. We'll work out the right mix together.";
export const servicesContact = { lead: "Not sure where yours starts?", link: "Get in touch" };

export const services: Service[] = [
  {
    id: "strategy",
    name: "Strategy",
    lead: "We work out what the project needs to do.",
    text: "Your goals set the direction, and the design follows from them. We find the big idea behind the work: one clear message, carried through, so every part of the project pulls the same way.",
  },
  {
    id: "design",
    name: "Design",
    lead: "We shape the idea, then the details.",
    text: "Before anything gets designed, we get everyone on board and agree on a shared picture of the direction. From there, a concept takes one idea and works it through into real design choices, down to interfaces that look right and are easy to use.",
  },
  {
    id: "prototyping",
    name: "Prototyping",
    lead: "We try ideas early, on something real.",
    text: "Prototypes in the browser or on a phone let you click through an idea rather than imagine it, and improve it with each round of feedback. We use your actual words and images, on the screens people will use, so decisions are made on the real thing.",
  },
  {
    id: "development",
    name: "Development",
    lead: "We build it properly, made to last.",
    text: "We refine the chosen concept together, through feedback, then build what we design. The result is a site or app that's fast, accessible and easy to look after.",
  },
  {
    id: "product",
    name: "Product",
    lead: "We look after products once they're live, and help them grow.",
    text: "We work with start-ups and teams that already have a product in place. We keep track of what's next, weigh it against your goals and plan each release with you. New features are added step by step to a core that can carry them.",
  },
];
