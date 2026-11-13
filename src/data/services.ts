// The Services section, in order. Wording from the Figma Services frame
// (22:1603), moved from "I" to "we" and toned down to short, plain lines (drafts). The live
// wording is kept in notes/copy.md.

export interface Service {
  id: string;
  name: string;
  lead: string;
  // One short paragraph per point (drafts, see notes/copy.md).
  items: string[];
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
    items: [
      "We find the big idea: one clear message, carried through colour, type and layout.",
      "Your goals set the direction, and the design follows from them.",
    ],
  },
  {
    id: "design",
    name: "Design",
    lead: "We shape the idea, then the details.",
    items: [
      "Moodboards give everyone a shared picture of the direction, before anything gets designed.",
      "Concepts take one idea and work it through into design choices.",
      "Interfaces and digital design that look right and are easy to use.",
      "Landing pages and sites built with no-code tools.",
    ],
  },
  {
    id: "prototyping",
    name: "Prototyping",
    lead: "We try ideas early, on something real.",
    items: [
      "Clickable prototypes in the browser or on a phone, to click through rather than imagine, and to improve with each round of feedback.",
      "Real content on real devices: your actual words and images, on the screens people will use.",
    ],
  },
  {
    id: "development",
    name: "Development",
    lead: "We build it properly, made to last.",
    items: [
      "We refine the chosen concept together, through feedback.",
      "We build what we design: sites and apps that are fast, accessible and easy to look after.",
    ],
  },
  {
    id: "product",
    name: "Product",
    lead: "We look after products once they're live, and help them grow.",
    items: [
      "Start-ups and teams with a product already in place: we pick up where things stand and help build it out.",
      "We keep track of what's next, weigh it against your goals and plan each release with you.",
      "New features, added step by step to a core that can carry them.",
      "Testing before every release, plus maintenance, updates and support, so things keep running.",
    ],
  },
];
