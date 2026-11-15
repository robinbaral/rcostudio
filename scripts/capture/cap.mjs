// Two modes, via the Chrome DevTools Protocol on Playwright's headless shell.
//   node cap.mjs full <url> <out.png> [mobile]          full page at 1x (for matching)
//   node cap.mjs clips <url> <outdir> <json> [mobile]    2x/3x clips: json = [{name, y}]
// Env PREP: JS run after load (hide cookie banners etc.). PORT: debugging port.
import { spawn } from "node:child_process";
import { writeFileSync, mkdirSync } from "node:fs";

const [mode, url, out, json, mob] = process.argv.slice(2);
const mobile = mode === "full" ? json === "mobile" : mob === "mobile";
const W = mobile ? 390 : 1440, H = mobile ? 844 : 900;
const scale = mode === "full" ? 1 : 2;
const port = Number(process.env.PORT || 9351);
const bin = `${process.env.HOME}/Library/Caches/ms-playwright/chromium_headless_shell-1148/chrome-mac/headless_shell`;
const chrome = spawn(bin, [`--remote-debugging-port=${port}`, "--hide-scrollbars", `--window-size=${W},${H}`, "about:blank"], { stdio: "ignore" });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const timer = setTimeout(() => { chrome.kill(); process.exit(2); }, Number(process.env.TIMEOUT || 240000));

try {
  let targets;
  for (let i = 0; i < 80 && !targets; i++) {
    try { targets = await (await fetch(`http://127.0.0.1:${port}/json`)).json(); } catch { await sleep(100); }
  }
  const ws = new WebSocket(targets.find((t) => t.type === "page").webSocketDebuggerUrl);
  await new Promise((r) => (ws.onopen = r));
  let id = 0;
  const pending = new Map();
  ws.onmessage = (e) => { const m = JSON.parse(e.data); if (m.id && pending.has(m.id)) { pending.get(m.id)(m); pending.delete(m.id); } };
  const send = (method, params = {}) => new Promise((r) => { const i = ++id; pending.set(i, r); ws.send(JSON.stringify({ id: i, method, params })); });
  const ev = async (expression) => (await send("Runtime.evaluate", { expression, awaitPromise: true, returnByValue: true })).result?.result?.value;

  await send("Emulation.setDeviceMetricsOverride", { width: W, height: H, deviceScaleFactor: scale, mobile });
  if (mobile) await send("Emulation.setUserAgentOverride", { userAgent: "Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1" });
  await send("Page.enable");
  await send("Page.navigate", { url });
  await sleep(5000); console.error("loaded");
  if (process.env.PREP) await ev(process.env.PREP);
  // Walk down the page so lazy images and scroll reveals fire, then back to the top.
  if (!process.env.NOWALK) await ev(`(async () => { const h = document.documentElement.scrollHeight; for (let y = 0; y < h; y += ${H / 2}) { scrollTo(0, y); await new Promise(r => setTimeout(r, 250)); } scrollTo(0, 0); await new Promise(r => setTimeout(r, 1200)); })()`);
  const height = await ev("document.documentElement.scrollHeight"); console.error("walked", height);

  const hideFixed = `document.querySelectorAll("body *").forEach((e) => { const p = getComputedStyle(e).position; if (p === "fixed" || p === "sticky") e.style.setProperty("visibility", "hidden", "important"); })`;
  if (mode === "full") {
    // Viewport-sized tiles, stitched by match.py's caller (tiles.py). Fixed bars hidden after
    // the first tile so they don't repeat.
    mkdirSync(out, { recursive: true });
    let n = 0;
    for (let y = 0; y < height; y += H) {
      if (y > 0 && n === 1) await ev(hideFixed);
      await ev(`(async () => { scrollTo(0, ${y}); await new Promise(r => setTimeout(r, 700)); })()`);
      const sy = await ev("scrollY");
      const shot = await send("Page.captureScreenshot", { format: "png" });
      writeFileSync(`${out}/${String(n).padStart(3, "0")}-${sy}.png`, Buffer.from(shot.result.data, "base64"));
      n++;
    }
    console.log("height", height, "tiles", n);
  } else {
    mkdirSync(out, { recursive: true });
    for (const item of JSON.parse(json)) {
      const { name, keepFixed } = item;
      let y = item.y ?? 0;
      await ev(`document.querySelectorAll("[data-cap-hidden]").forEach((e) => { e.style.removeProperty("visibility"); e.removeAttribute("data-cap-hidden"); })`);
      if (item.at !== undefined) {
        await ev(`(async () => { scrollTo(0, ${item.at}); await new Promise(r => setTimeout(r, 800)); })()`);
        await ev(`(() => { const e = document.elementFromPoint(${W / 2}, ${H / 2}); e.setAttribute("data-cap-target", ""); })()`);
        item.text = "\u0000"; // use the marked element below
      }
      if (item.text) {
        // Frame one section by its text: hide everything but it, centre it if it fits,
        // otherwise start 40px above it.
        y = await ev(`(() => {
          const want = ${JSON.stringify(item.text.toLowerCase())};
          const marked = document.querySelector("[data-cap-target]");
          if (marked) marked.removeAttribute("data-cap-target");
          const hits = marked ? [marked] : [...document.querySelectorAll("h1,h2,h3,h4,h5,p,span,div,a")].filter((e) => e.children.length < 3 && (e.textContent || "").toLowerCase().includes(want) && e.offsetHeight > 0);
          if (!hits.length) return -1;
          const hit = hits[${item.nth || 0}];
          let block = null;
          if (${!!item.fit}) { for (let e = hit; e && e !== document.body && e.offsetHeight <= ${H * (item.fit || 1)}; e = e.parentElement) block = e; }
          else for (let e = hit; e && e !== document.body; e = e.parentElement) if (e.matches(${JSON.stringify(item.sel || "section, footer")})) block = e;
          if (!block) { block = hit; while (block.parentElement !== document.body && block.offsetHeight < 300) block = block.parentElement; }
          for (let e = block; e && e !== document.body; e = e.parentElement)
            for (const sib of e.parentElement.children) if (sib !== e && !["SCRIPT","STYLE"].includes(sib.tagName)) { sib.style.setProperty("visibility", "hidden", "important"); sib.setAttribute("data-cap-hidden", ""); }
          if (${JSON.stringify(item.bg || "")}) for (let e = block.parentElement; e; e = e.parentElement) e.style.setProperty("background", ${JSON.stringify(item.bg || "")}, "important");
          const r = block.getBoundingClientRect(), top = r.top + scrollY, h = r.height;
          if (${!!item.alignTop}) return Math.max(0, Math.round(top - ${item.pad ?? 0}));
          return Math.max(0, Math.round(h < ${H} ? top - (${H} - h) / 2 : top - ${item.pad ?? 40}));
        })()`);
        if (y < 0) { console.log(name, "TEXT NOT FOUND"); continue; }
      }
      await ev(`(async () => { scrollTo(0, ${y}); await new Promise(r => setTimeout(r, 1200)); })()`);
      if (y > 0 && !keepFixed) await ev(hideFixed.replace('"hidden", "important")', '"hidden", "important"), e.setAttribute("data-cap-hidden", "")'));
      await sleep(300);
      const sy = await ev("scrollY");
      if (item.halves) {
        // Two half-height clips (some pages hang Chrome on a full 2x frame), joined by tiles.py.
        for (const [k, cy] of [[0, 0], [1, H / 2]]) {
          const part = await send("Page.captureScreenshot", { format: "png", clip: { x: 0, y: sy + cy, width: W, height: H / 2, scale: 1 } });
          writeFileSync(`${out}/${name}.half${k}.png`, Buffer.from(part.result.data, "base64"));
        }
        console.log(name, y, "halves");
        continue;
      }
      const shot = await send("Page.captureScreenshot", { format: "png" });
      writeFileSync(`${out}/${name}.png`, Buffer.from(shot.result.data, "base64"));
      console.log(name, y, "scrollY", sy);
    }
  }
} finally {
  clearTimeout(timer);
  chrome.kill();
}
