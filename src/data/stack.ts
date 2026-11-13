// The "Everyday Stack" section above the footer: the tools Robin works in day to day, so teams
// can see R&Co can join in with what they already use. From the Figma frame "Hero" (22:1662),
// plus the tools the recent projects are built with. Claude and GPT are listed as tools (Robin,
// 2026-11-13); the copy elsewhere still doesn't talk about AI (notes/decisions.md). Also used in /llms.txt.

export const stack: { name: string; tools: string[] }[] = [
  {
    name: "Strategy",
    tools: ["FigJam", "Miro", "Jira", "Linear", "Slack", "Zoom", "Keynote", "Microsoft 365 (Excel, PowerPoint, Teams)"],
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
