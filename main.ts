import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

// The poster is drawn by draw_poster.py and committed as entry.png.
// This entrypoint just places that exact image at /output/entry.png,
// so every run writes the same bytes: no network, no clock, no random.
const here = dirname(fileURLToPath(import.meta.url));
mkdirSync("/output", { recursive: true });
copyFileSync(join(here, "entry.png"), "/output/entry.png");
console.log("entry.png written to /output/entry.png");
