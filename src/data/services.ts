// The Services section, in order. Wording from the Figma Services frame
// (22:1603), moved from "I" to "we" and toned down to short, plain lines (drafts). The live
// wording is kept in notes/copy.md.

export interface Service {
  id: string;
  name: string;
  lead: string;
  // Optional opening sentence of the lead, set in full colour.
  emphasis?: string;
  items: { title: string; text: string }[];
}

// The left column: a note and a quiet, contextual contact line (drafts, see notes/copy.md).
export const servicesNote =
  "Not every project needs every step. Some start with strategy, others go straight to a prototype, and sometimes we join your team for a while. We'll work out the right mix together.";
export const servicesContact = { lead: "Not sure where yours starts?", link: "Get in touch" };

export const services: Service[] = [
  {
    id: "strategy",
    name: "Strategy",
    lead: "First, we work out what the project needs to do.",
    items: [
      {
        title: "The big idea",
        text: "One clear message, carried through colour, type and layout.",
      },
      {
        title: "Project goals",
        text: "Your goals set the direction. The design follows from them.",
      },
    ],
  },
  {
    id: "design",
    name: "Design",
    lead: "The idea first, then the details.",
    items: [
      {
        title: "Moodboards",
        text: "A shared picture of the direction, before anything gets designed.",
      },
      {
        title: "Concepts",
        text: "One idea, worked through into design choices.",
      },
      {
        title: "UI/UX & digital design",
        text: "Interfaces that look right and are easy to use.",
      },
      {
        title: "No-code tools",
        text: "Landing pages and sites built with no-code tools.",
      },
    ],
  },
  {
    id: "prototyping",
    name: "Prototyping",
    lead: "We prototype early, so ideas get tried on something real.",
    items: [
      {
        title: "Clickable prototypes",
        text: "Working versions in the browser or on a phone, to click through rather than imagine, and improve with each round of feedback.",
      },
      {
        title: "Real content, real devices",
        text: "Your actual words and images, on the screens people will use.",
      },
    ],
  },
  {
    id: "development",
    name: "Development",
    lead: "We take care with the details.",
    items: [
      {
        title: "Refinement",
        text: "We refine the chosen concept together, through feedback.",
      },
      {
        title: "Build",
        text: "We build what we design: sites and apps that are fast, accessible and easy to look after.",
      },
    ],
  },
];
