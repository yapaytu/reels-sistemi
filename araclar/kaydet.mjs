// Bir sahne HTML'ini kare kare MP4'e çevirir.
// Kullanım: node araclar/kaydet.mjs ornekler/kil.html [cikti.mp4] [--ses ses.mp3]
// Sahne sözleşmesi STUDYO.md'de: sayfa window.ciz(kare), window.SURE (sn) ve window.FPS tanımlar, #sahne 1080x1920'dir.
import { chromium } from "playwright";
import { spawn } from "node:child_process";
import path from "node:path";
import fs from "node:fs";

const arg = process.argv.slice(2);
const sesI = arg.indexOf("--ses");
const ses = sesI >= 0 ? arg.splice(sesI, 2)[1] : null;
const [girdi, ciktiArg] = arg;
if (!girdi || !fs.existsSync(girdi)) {
  console.error("Kullanım: node araclar/kaydet.mjs <sahne.html> [cikti.mp4] [--ses ses.mp3]");
  process.exit(1);
}
const cikti = ciktiArg || girdi.replace(/\.html?$/, "") + ".mp4";

const tarayici = await chromium.launch({ args: ["--use-angle=swiftshader", "--enable-unsafe-swiftshader"] });
const sayfa = await tarayici.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
await sayfa.goto("file://" + path.resolve(girdi) + "?kayit=1");
await sayfa.waitForFunction(() => typeof window.ciz === "function" && window.SURE > 0, null, { timeout: 30000 });
await sayfa.evaluate(() => document.fonts.ready);
if (await sayfa.evaluate(() => typeof window.hazir === "function")) await sayfa.evaluate(() => window.hazir());
const { SURE, FPS } = await sayfa.evaluate(() => ({ SURE: window.SURE, FPS: window.FPS || 30 }));
const toplam = Math.round(SURE * FPS);

const ff = spawn("ffmpeg", [
  "-y", "-loglevel", "error",
  "-f", "image2pipe", "-framerate", String(FPS), "-i", "-",
  // ses, sahnedeki ILK karesi (6 kare = 0.2 sn) kadar gecikmeli başlar
  ...(ses ? ["-itsoffset", "0.2", "-i", ses, "-map", "0:v", "-map", "1:a", "-c:a", "aac", "-b:a", "192k"] : []),
  "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "17", "-preset", "medium", "-movflags", "+faststart",
  cikti,
], { stdio: ["pipe", "inherit", "inherit"] });

const sahne = await sayfa.$("#sahne");
for (let f = 0; f < toplam; f++) {
  await sayfa.evaluate((k) => window.ciz(k), f);
  const kare = await sahne.screenshot({ type: "jpeg", quality: 92 });
  if (!ff.stdin.write(kare)) await new Promise((r) => ff.stdin.once("drain", r));
  if (f % FPS === 0) process.stdout.write(`\r${f}/${toplam} kare`);
}
ff.stdin.end();
await new Promise((r) => ff.on("close", r));
await tarayici.close();
console.log(`\r${toplam}/${toplam} kare → ${cikti}`);
