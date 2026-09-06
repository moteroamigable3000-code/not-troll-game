// Builds a static, upload-ready copy of the game for a specific HTML5 game
// portal. The game always talks to our own backend (evildevil-ghost.online)
// over HTTPS, so these builds are just the frontend files plus, for portals
// that require it, their ad SDK <script> tag.
//
// Usage:
//   node scripts/build-portal.mjs itch
//   node scripts/build-portal.mjs crazygames
//   node scripts/build-portal.mjs poki
//   node scripts/build-portal.mjs android
//
// Output goes to dist/<portal>/ — zip that folder's *contents* (not the
// folder itself) and upload the zip to the portal.
//
// `android` is special: instead of dist/android/, it writes straight into
// android/app/src/main/assets/ so the WebView app picks up the latest
// frontend. Run it whenever game.js/style.css/recursos change and rebuild
// the app.

import { mkdirSync, rmSync, copyFileSync, cpSync, readFileSync, writeFileSync, existsSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const portal = process.argv[2];

const SDK_TAGS = {
  itch: '',
  plain: '',
  android: '',
  crazygames: '<script src="https://sdk.crazygames.com/crazygames-sdk-v3.js"></script>\n  ',
  poki: '<script src="//game-cdn.poki.com/scripts/v2/poki-sdk.js"></script>\n  ',
};

if (!portal || !(portal in SDK_TAGS)) {
  console.error('Usage: node scripts/build-portal.mjs <itch|crazygames|poki|plain|android>');
  process.exit(1);
}

const outDir = portal === 'android'
  ? path.join(ROOT, 'android', 'app', 'src', 'main', 'assets')
  : path.join(ROOT, 'dist', portal);
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

if (portal === 'android') {
  console.log('Assets sincronizados en android/app/src/main/assets/');
  console.log('Ahora recompila la app (android/gradlew assembleDebug o desde Android Studio).');
} else {
  console.log(`Build listo en dist/${portal}/`);
  if (!existsSync(path.join(ROOT, 'backend'))) {
    console.log('(nota: la carpeta backend/ no se copia a propósito, el juego solo necesita el frontend)');
  }
  console.log('Para empaquetar en zip:');
  console.log('  NOTA: PowerShell Compress-Archive guarda rutas con "\\" y varios');
  console.log('  portales (itch.io incluido) no reconocen eso como carpetas, así que');
  console.log('  la carpeta recursos/ se pierde. Usa Python en su lugar:');
  console.log(`  python -c "import zipfile,os; z=zipfile.ZipFile('dist/${portal}.zip','w',zipfile.ZIP_DEFLATED); [z.write(os.path.join(r,f), os.path.relpath(os.path.join(r,f),'dist/${portal}').replace(os.sep,'/')) for r,_,fs in os.walk('dist/${portal}') for f in fs]"`);
}
