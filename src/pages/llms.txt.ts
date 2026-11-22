// /llms.txt: a plain-text summary of the studio for language models and AI search
// (llmstxt.org format), built from the same data as the homepage so it stays in sync.
import type { APIRoute } from "astro";
import { profile } from "../data/profile";
import { services, servicesNote } from "../data/services";
import { projects, projectId } from "../data/projects";
import { stack, awards } from "../data/stack";

const site = "https://rcostudio.nz";

export const GET: APIRoute = () => {
  const lines: string[] = [
    "# R&Co. Studio",
    "",
    "> A digital-first design studio for sites, interfaces and branding, shaped by 20+ years of experience in strategy, branding, development and design. Based in New Zealand, working with clients anywhere.",
    "",
    `${profile.opening} ${profile.rest}`,
    "",
    `${profile.setup.title}: ${profile.setup.text.join(" ")}`,
    "",
    "## Services",
    "",
    servicesNote.join(" "),
    "",
    ...services.flatMap((s) => [
      `- ${s.name}: ${s.lead} ${s.text}`,
    ]),
    "",
    "## Selected work",
    "",
    ...projects.map((p) => {
      if (p.soon) return `- ${p.name}: coming soon`;
      // The project's page here, then its own site where there is one.
      const link = p.href ? ` (live: ${new URL(p.href, site).href})` : "";
      return `- [${p.name}](${site}/work/${projectId(p)}): ${p.tags}${link}`;
    }),
    "",
    "## Everyday stack",
    "",
    ...stack.map((g) => `- ${g.name}: ${g.tools.join(", ")}`),
    "",
    `## ${awards.name}`,
    "",
    `${awards.note}: ${awards.names.join(", ")}.`,
    "",
    "## Contact",
    "",
    `- Website: ${site}`,
    "- Email: info@rcostudio.nz",
    "- Phone: +64 21 082 039 40",
    "",
  ];
  return new Response(lines.join("\n"), {
    headers: { "Content-Type": "text/plain; charset=utf-8" },
  });
};
