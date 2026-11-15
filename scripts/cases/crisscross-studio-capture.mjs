// Captures Puzzle Studio (local read-only preview) at 1440x900, 2x: logs in with the local
// preview password, then one PNG per tab. Usage: node cap.mjs <outdir> <password> <topic?>
import { spawn } from "node:child_process";
import { writeFileSync } from "node:fs";
const [out, password, topic] = process.argv.slice(2);
const port = 9361, W = 1440, H = 900;
const bin = `${process.env.HOME}/Library/Caches/ms-playwright/chromium_headless_shell-1148/chrome-mac/headless_shell`;
const chrome = spawn(bin, [`--remote-debugging-port=${port}`, "--hide-scrollbars", `--window-size=${W},${H}`, "about:blank"], { stdio: "ignore" });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
try {
  let targets;
  for (let i = 0; i < 80 && !targets; i++) { try { targets = await (await fetch(`http://127.0.0.1:${port}/json`)).json(); } catch { await sleep(100); } }
  const ws = new WebSocket(targets.find((t) => t.type === "page").webSocketDebuggerUrl);
  await new Promise((r) => (ws.onopen = r));
  let id = 0; const pending = new Map();
  ws.onmessage = (e) => { const m = JSON.parse(e.data); if (m.id && pending.has(m.id)) { pending.get(m.id)(m); pending.delete(m.id); } };
  const send = (method, params = {}) => new Promise((r) => { const i = ++id; pending.set(i, r); ws.send(JSON.stringify({ id: i, method, params })); });
  const ev = async (expression) => (await send("Runtime.evaluate", { expression, awaitPromise: true, returnByValue: true })).result?.result?.value;
  await send("Emulation.setDeviceMetricsOverride", { width: W, height: H, deviceScaleFactor: 2, mobile: false });
  await send("Page.enable");
  await send("Page.navigate", { url: "http://127.0.0.1:8765/admin/login" });
  await sleep(1500);
  await ev(`(() => { const i = document.querySelector('input[type=password]'); i.value = ${JSON.stringify(password)}; i.form.requestSubmit ? i.form.requestSubmit() : i.form.submit(); })()`);
  await sleep(3000);
  if (topic) { console.error("topic", await ev(`(() => { const s = [...document.querySelectorAll('select')].find(s => [...s.options].some(o => o.text.startsWith(${JSON.stringify(topic)}))); if (!s) return 'none'; const o = [...s.options].find(o => o.text.startsWith(${JSON.stringify(topic)})); s.value = o.value; s.dispatchEvent(new Event('change', {bubbles:true})); return o.text; })()`)); await sleep(2500); }
  for (const tab of ["Word list", "Grids", "Audio", "Flashcards"]) {
    console.error(tab, await ev(`(() => { const b = [...document.querySelectorAll('button')].find(b => b.textContent.trim() === ${JSON.stringify(tab)}); if (!b) return 'missing'; b.click(); return 'ok'; })()`));
    await sleep(2500);
    await ev("scrollTo(0,0)");
    const shot = await send("Page.captureScreenshot", { format: "png" });
    writeFileSync(`${out}/studio-${tab.toLowerCase().replace(/ /g, "-")}.png`, Buffer.from(shot.result.data, "base64"));
  }
} finally { chrome.kill(); process.exit(0); }
