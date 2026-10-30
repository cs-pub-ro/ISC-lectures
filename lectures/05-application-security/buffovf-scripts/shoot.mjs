#!/usr/bin/env node
// shoot.mjs -- screenshot an HTML page (our terminal card) with Playwright.
//   node shoot.mjs card.html card.png [deviceScaleFactor]
import { chromium } from "playwright-chromium";

const [, , inPath, outPath, scaleArg] = process.argv;
if (!inPath || !outPath) {
  console.error("usage: node shoot.mjs <in.html> <out.png> [scale]");
  process.exit(1);
}
const scale = Number(scaleArg ?? 2);

const browser = await chromium.launch();
const page = await browser.newPage({
  viewport: { width: 1600, height: 1200 },
  deviceScaleFactor: scale,
});
await page.goto(`file://${inPath}`);
await page.waitForTimeout(120); // let fonts settle
await page.locator(".term").screenshot({ path: outPath, omitBackground: true });
await browser.close();
console.log(`wrote ${outPath}`);
