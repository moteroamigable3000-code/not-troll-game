// Builds a static, upload-ready copy of the game for a specific HTML5 game
// portal. The game always talks to our own backend (evildevil-ghost.online)
// over HTTPS, so these builds are just the frontend files plus, for portals
// that require it, their ad SDK <script> tag.
//
// Usage:
//   node scripts/build-portal.mjs itch
//   node scripts/build-portal.mjs crazygames
//   node scripts/build-portal.mjs poki
//
// Output goes to dist/<portal>/ — zip that folder's *contents* (not the
// folder itself) and upload the zip to the portal.

import { mkdirSync, rmSync, copyFileSync, cpSync, readFileSync, writeFileSync, existsSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const portal = process.argv[2];

const SDK_TAGS = {
  itch: '',
  plain: '',
  crazygames: '<script src="https://sdk.crazygames.com/crazygames-sdk-v3.js"></script>\n  ',
  poki: '<script src="//game-cdn.poki.com/scripts/v2/poki-sdk.js"></script>\n  ',
};

if (!portal || !(portal in SDK_TAGS)) {
  console.error('Usage: node scripts/build-portal.mjs <itch|crazygames|poki|plain>');
  process.exit(1);
}

const outDir = path.join(ROOT, 'dist', portal);
rmSync(outDir, { recursive: true, force: true });
mkdirSync(outDir, { recursive: true });

copyFileSync(path.join(ROOT, 'style.css'), path.join(outDir, 'style.css'));
copyFileSync(path.join(ROOT, 'game.min.js'), path.join(outDir, 'game.min.js'));
cpSync(path.join(ROOT, 'recursos'), path.join(outDir, 'recursos'), { recursive: true });

let html = readFileSync(path.join(ROOT, 'index.html'), 'utf8');
const sdkTag = SDK_TAGS[portal];
if (sdkTag) {
  html = html.replace('<script src="game.min.js', sdkTag + '<script src="game.min.js');
}
writeFileSync(path.join(outDir, 'index.html'), html);

console.log(`Build listo en dist/${portal}/`);
if (!existsSync(path.join(ROOT, 'backend'))) {
  console.log('(nota: la carpeta backend/ no se copia a propósito, el juego solo necesita el frontend)');
}
console.log('Para empaquetar en zip (PowerShell):');
console.log(`  Compress-Archive -Path dist/${portal}/* -DestinationPath dist/${portal}.zip -Force`);
