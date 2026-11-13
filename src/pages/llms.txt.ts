// /llms.txt: a plain-text summary of the studio for language models and AI search
// (llmstxt.org format), built from the same data as the homepage so it stays in sync.
import type { APIRoute } from "astro";
import { profile } from "../data/profile";
import { services, servicesNote } from "../data/services";
import { projects } from "../data/projects";
import { stack } from "../data/stack";

const site = "https://rcostudio.nz";

export const GET: APIRoute = () => {
  const lines: string[] = [
    "# R&Co. Studio",
    "",
    "> A digital-first design studio for sites, interfaces and branding, shaped by 20+ years of experience in strategy, branding and design. Based in New Zealand, working with clients anywhere.",
    "",
    `${profile.opening} ${profile.rest}`,
    "",
    `${profile.setup.title}: ${profile.setup.text.join(" ")}`,
    "",
    "## Services",
    "",
    servicesNote,
    "",
    ...services.flatMap((s) => [
      `- ${s.name}: ${s.lead} ${s.items.join(" ")}`,
    ]),
    "",
    "## Selected projects",
    "",
    ...projects.map((p) => {
      const kind = p.soon ? "coming soon" : p.tags;
      return p.href ? `- [${p.name}](${p.href}): ${kind}` : `- ${p.name}: ${kind}`;
    }),
    "",
    "## Everyday stack",
    "",
    ...stack.map((g) => `- ${g.name}: ${g.tools.join(", ")}`),
    "",
    "## Contact",
    "",
    `- Website: ${site}`,
    "- Email: baralrobin@gmail.com",
    "- Phone: +64 21 082 039 40",
    "",
  ];
  return new Response(lines.join("\n"), {
    headers: { "Content-Type": "text/plain; charset=utf-8" },
  });
};
