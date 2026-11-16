// The "Everyday Stack" section above the footer: the tools Robin works in day to day, so teams
// can see R&Co can join in with what they already use. From the Figma frame "Hero" (22:1662),
// plus the tools the recent projects are built with. Claude and GPT are listed as tools (Robin,
// 2026-11-13); the copy elsewhere still doesn't talk about AI (notes/decisions.md). Also used in /llms.txt.

export const stack: { name: string; tools: string[] }[] = [
  {
    name: "Strategy",
    tools: ["FigJam", "Miro", "Jira", "Linear", "Obsidian", "Slack", "Zoom", "Keynote", "Microsoft 365 (Excel, PowerPoint, Teams)"],
  },
  {
    name: "Design",
    tools: ["Figma", "Photoshop", "Illustrator", "InDesign", "Premiere"],
  },
  {
    name: "Development",
    tools: ["HTML", "CSS", "JavaScript", "Astro", "Webflow", "Squarespace", "Sanity", "Xcode", "Claude", "GPT", "GitHub", "Vercel", "Cloudflare"],
  },
];

// Recognition, a small subsection after the stack, set the same way: awards won by projects Robin worked on in
// agency roles (from fg-branddesign.com/awards; the agency stays unnamed, Robin 2026-11-15).
// Names only, no years or logos, the best-known ones (Robin's pick, 2026-11-15), most widely known first. Wording is (draft) until Robin
// confirms it; notes/copy.md has it too. Also used in /llms.txt.
export const awards = {
  name: "Recognition",
  note: "Awards for agency projects I worked on",
  names: [
    "Red Dot",
    "iF Design Award",
    "German Design Award",
    "German Brand Award",
    "Good Design Award",
    "German Innovation Award",
    "New York Festivals",
  ],
};
