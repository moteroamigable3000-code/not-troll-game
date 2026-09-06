// ============ Not A Troll Game — motor principal ============

const canvas = document.getElementById('game');
const ctx = canvas.getContext('2d');
const W = canvas.width, H = canvas.height;

const bgImage = new Image();
let bgImageReady = false;
bgImage.onload = () => { bgImageReady = true; };
bgImage.src = 'recursos/FONDO_JUEGO.png';

const levelLabel = document.getElementById('levelLabel');
const deathLabel = document.getElementById('deathLabel');
const overlayTitle = document.getElementById('overlayTitle');
const overlaySub = document.getElementById('overlaySub');
const progressFill = document.getElementById('progressFill');
document.getElementById('restartBtn').onclick = () => restartLevel();

// ---------- Studio splash ----------
const splashScreen = document.getElementById('splashScreen');
let splashActive = true;
const splashSound = new Audio('recursos/splash_inicio.mp3');
splashSound.volume = 0.75;

function playSplashSound() {
  if (!splashActive || localStorage.getItem('notTrollSoundOn') === '0') return;
  try {
    splashSound.currentTime = 0;
    splashSound.play().catch(() => {});
  } catch (e) { /* autoplay can be blocked until the first gesture */ }
}

function dismissSplash() {
  if (!splashActive) return;
  splashActive = false;
  // Let the sting finish playing even if the visual splash is skipped —
  // stopping it here would cut it off the instant a click/keydown unlocks
  // audio, since play() and this dismiss fire in the same handler.
  splashScreen.classList.add('fadeOut');
  setTimeout(() => { splashScreen.hidden = true; }, 650);
}
playSplashSound();
setTimeout(dismissSplash, 2200);
splashScreen.addEventListener('click', () => {
  playSplashSound();
  dismissSplash();
});
window.addEventListener('keydown', () => {
  playSplashSound();
  dismissSplash();
}, { once: true });

// ---------- Menus (main menu, level map, options) ----------
const mainMenu = document.getElementById('mainMenu');
const levelMap = document.getElementById('levelMap');
const optionsMenu = document.getElementById('optionsMenu');
const profileMenu = document.getElementById('profileMenu');
const infoMenu = document.getElementById('infoMenu');
const levelGrid = document.getElementById('levelGrid');
const mapPath = document.getElementById('mapPath');
const mapScroll = document.getElementById('mapScroll');
const mapInner = document.getElementById('mapInner');
const soundToggleBtn = document.getElementById('soundToggleBtn');
let paused = false;
let soundOn = localStorage.getItem('notTrollSoundOn') !== '0';

// ---------- Sound (synthesized, no assets needed) ----------
const Sound = (() => {
  let ctxA = null;
  function ac() {
    if (!ctxA) {
      try { ctxA = new (window.AudioContext || window.webkitAudioContext)(); }
      catch (e) { return null; }
    }
    if (ctxA.state === 'suspended') ctxA.resume().catch(() => {});
    return ctxA;
  }
  function tone(freq, dur, type, gain, glideTo) {
    if (!soundOn) return;
    const a = ac();
    if (!a) return;
    try {
      const osc = a.createOscillator();
      const g = a.createGain();
      osc.type = type || 'square';
      osc.frequency.setValueAtTime(freq, a.currentTime);
      if (glideTo) osc.frequency.exponentialRampToValueAtTime(glideTo, a.currentTime + dur);
      g.gain.setValueAtTime(gain || 0.15, a.currentTime);
      g.gain.exponentialRampToValueAtTime(0.001, a.currentTime + dur);
      osc.connect(g); g.connect(a.destination);
      osc.start();
      osc.stop(a.currentTime + dur);
    } catch (e) { /* audio unsupported in this context — fail silently */ }
  }
  function noise(dur, gain) {
    if (!soundOn) return;
    const a = ac();
    if (!a) return;
    try {
      const bufSize = a.sampleRate * dur;
      const buf = a.createBuffer(1, bufSize, a.sampleRate);
      const data = buf.getChannelData(0);
      for (let i = 0; i < bufSize; i++) data[i] = (Math.random() * 2 - 1) * (1 - i / bufSize);
      const src = a.createBufferSource();
      src.buffer = buf;
      const g = a.createGain();
      g.gain.setValueAtTime(gain || 0.2, a.currentTime);
      g.gain.exponentialRampToValueAtTime(0.001, a.currentTime + dur);
      src.connect(g); g.connect(a.destination);
      src.start();
    } catch (e) { /* ignore */ }
  }
  return {
    jump: () => tone(420, 0.12, 'square', 0.12, 680),
    land: () => tone(160, 0.08, 'sine', 0.15, 90),
    death: () => { tone(300, 0.35, 'sawtooth', 0.18, 40); noise(0.25, 0.15); },
    goal: () => { tone(523, 0.1, 'square', 0.15, 523); setTimeout(() => tone(659, 0.1, 'square', 0.15, 659), 90); setTimeout(() => tone(784, 0.22, 'square', 0.18, 784), 180); },
    pop: () => tone(200, 0.08, 'square', 0.1, 90),
    crumble: () => noise(0.15, 0.12),
    boom: () => { tone(90, 0.3, 'sawtooth', 0.2, 40); noise(0.3, 0.22); },
    resume: () => ac(),
  };
})();
window.addEventListener('keydown', () => Sound.resume(), { once: true });
window.addEventListener('pointerdown', () => Sound.resume(), { once: true });

function applySoundButtonLabel() {
  soundToggleBtn.textContent = 'Sonido: ' + (soundOn ? 'ON' : 'OFF');
}
soundToggleBtn.addEventListener('click', () => {
  soundOn = !soundOn;
  localStorage.setItem('notTrollSoundOn', soundOn ? '1' : '0');
  applySoundButtonLabel();
});
applySoundButtonLabel();

// ---------- Music — two mutually-exclusive tracks. Gameplay music plays
// only during an actual level (state === 'playing'); menu music plays only
// over the main menu and the level map — never both, never over options
// or the level intro/dead/complete transitions. ----------
const musicToggleBtn = document.getElementById('musicToggleBtn');
let musicOn = localStorage.getItem('notTrollMusicOn') !== '0';
const bgMusic = new Audio('recursos/musica_indie_gameplay.wav');
bgMusic.loop = true;
bgMusic.volume = 0.35;
const menuMusic = new Audio('recursos/musica_menu_y_mapa.wav');
menuMusic.loop = true;
menuMusic.volume = 0.35;

function applyMusicButtonLabel() {
  musicToggleBtn.textContent = 'Musica: ' + (musicOn ? 'ON' : 'OFF');
}
musicToggleBtn.addEventListener('click', () => {
  musicOn = !musicOn;
  localStorage.setItem('notTrollMusicOn', musicOn ? '1' : '0');
  applyMusicButtonLabel();
});
applyMusicButtonLabel();

// Stop both tracks the moment the tab is closed/hidden/backgrounded — a
// looping <audio> otherwise keeps playing (and keeps the tab "alive" in
// some browsers) after the user navigates away or closes it.
function stopAllMusic() {
  bgMusic.pause();
  menuMusic.pause();
}
window.addEventListener('pagehide', stopAllMusic);
document.addEventListener('visibilitychange', () => {
  if (document.hidden) stopAllMusic();
});

// Checked every frame.
function updateMusicPlayback() {
  const menuVisible = !mainMenu.hidden || !levelMap.hidden;
  const shouldPlayGameplay = musicOn && state === 'playing' && !paused;
  const shouldPlayMenu = musicOn && menuVisible;
  if (shouldPlayGameplay && bgMusic.paused) bgMusic.play().catch(() => {});
  else if (!shouldPlayGameplay && !bgMusic.paused) bgMusic.pause();
  if (shouldPlayMenu && menuMusic.paused) menuMusic.play().catch(() => {});
  else if (!shouldPlayMenu && !menuMusic.paused) menuMusic.pause();
}

// Browsers require a real user gesture before any audio can play at all —
// "prime" both tracks here, then immediately hand control back to
// updateMusicPlayback() so only the right one actually plays.
function primeMusic() {
  bgMusic.play().then(() => { if (state !== 'playing' || paused) bgMusic.pause(); }).catch(() => {});
  menuMusic.play().then(() => { if (mainMenu.hidden && levelMap.hidden) menuMusic.pause(); }).catch(() => {});
}
window.addEventListener('keydown', primeMusic, { once: true });
window.addEventListener('pointerdown', primeMusic, { once: true });

// ---------- Click sound — any UI button (menu, map node, options, HUD),
// but not the on-screen movement pad, which fires far too rapidly for it. ----------
const clickSound = new Audio('recursos/clic.wav');
clickSound.volume = 0.5;
document.addEventListener('click', e => {
  const btn = e.target.closest('button');
  if (!btn || btn.classList.contains('touchBtn') || !soundOn) return;
  try { clickSound.currentTime = 0; clickSound.play().catch(() => {}); } catch (err) { /* ignore */ }
});

// ---------- Lock it down like a game, not a webpage ----------
window.addEventListener('contextmenu', e => e.preventDefault());
window.addEventListener('selectstart', e => e.preventDefault());
canvas.addEventListener('dragstart', e => e.preventDefault());

// ---------- Input ----------
const keys = {};
const JUMP_CODES = ['Space', 'ArrowUp', 'KeyW'];
window.addEventListener('keydown', e => {
  if (e.code === 'Escape') {
    if (level) {
      if (paused) closeAllScreens();
      else openLevelMap();
    }
    return;
  }
  if (paused) return;
  if (JUMP_CODES.includes(e.code) && !keys[e.code] && typeof player !== 'undefined' && player) {
    player.jumpBuffer = JUMP_BUFFER_TIME;
  }
  keys[e.code] = true;
  if (e.code === 'KeyR') restartLevel();
  if (['Space', 'ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight'].includes(e.code)) e.preventDefault();
});
window.addEventListener('keyup', e => keys[e.code] = false);

// ---------- Touch controls (mobile) ----------
function bindHoldButton(el, code, isJump) {
  const press = (e) => {
    e.preventDefault();
    if (isJump && !keys[code] && typeof player !== 'undefined' && player) {
      player.jumpBuffer = JUMP_BUFFER_TIME;
    }
    keys[code] = true;
    el.classList.add('active');
  };
  const release = (e) => {
    e.preventDefault();
    keys[code] = false;
    el.classList.remove('active');
  };
  el.addEventListener('pointerdown', press);
  el.addEventListener('pointerup', release);
  el.addEventListener('pointercancel', release);
  el.addEventListener('pointerleave', release);
  el.addEventListener('contextmenu', e => e.preventDefault());
}

const btnLeft = document.getElementById('btnLeft');
const btnRight = document.getElementById('btnRight');
const btnJump = document.getElementById('btnJump');
if (btnLeft && btnRight && btnJump) {
  bindHoldButton(btnLeft, 'ArrowLeft', false);
  bindHoldButton(btnRight, 'ArrowRight', false);
  bindHoldButton(btnJump, 'Space', true);
}

// ---------- Optional backend API ----------
// Hardcoded so the game keeps talking to our own server even when it's
// embedded on a game portal (CrazyGames/Poki/itch.io load this file from
// their own origin, so relying on location.origin would point nowhere).
const PUBLIC_API_BASE_URL = 'https://evildevil-ghost.online';
const API_BASE_URL = (window.API_BASE_URL || PUBLIC_API_BASE_URL).replace(/\/$/, '');

// ---------- Ad platform adapter ----------
// Detects the CrazyGames or Poki SDK if this build is hosted on their
// portal (they're loaded via a <script> tag added only to that portal's
// build). No-ops everywhere else (our own domain, itch.io), so this is
// always safe to call.
const Ads = (() => {
  const cg = () => window.CrazyGames && window.CrazyGames.SDK;
  const poki = () => window.PokiSDK;

  function init() {
    if (cg()) return cg().init().catch(() => {});
    if (poki()) return poki().init().catch(() => {});
    return Promise.resolve();
  }
  function loadingStop() {
    try {
      if (cg()) cg().game.loadingStop();
      if (poki()) poki().gameLoadingFinished();
    } catch (e) { /* SDK not fully ready, ignore */ }
  }
  function gameplayStart() {
    try {
      if (cg()) cg().game.gameplayStart();
      if (poki()) poki().gameplayStart();
    } catch (e) { /* ignore */ }
  }
  function gameplayStop() {
    try {
      if (cg()) cg().game.gameplayStop();
      if (poki()) poki().gameplayStop();
    } catch (e) { /* ignore */ }
  }
  function midgameBreak() {
    try {
      if (cg()) { cg().ad.requestAd('midgame'); return Promise.resolve(); }
      if (poki()) return poki().commercialBreak().catch(() => {});
    } catch (e) { /* ignore */ }
    return Promise.resolve();
  }

  init().then(loadingStop);
  return { gameplayStart, gameplayStop, midgameBreak };
})();

function getPlayerId() {
  let id = localStorage.getItem('notTrollPlayerId');
  if (!id) {
    id = window.crypto && crypto.randomUUID
      ? crypto.randomUUID()
      : 'p-' + Math.random().toString(36).slice(2) + Date.now().toString(36);
    localStorage.setItem('notTrollPlayerId', id);
  }
  return id;
}

function getAccount() {
  try {
    const raw = localStorage.getItem('notTrollAccount');
    return raw ? JSON.parse(raw) : null;
  } catch (e) {
    return null;
  }
}

function setAccountSession(account) {
  localStorage.setItem('notTrollAccount', JSON.stringify(account));
  PLAYER_ID = account.player_id;
}

function clearAccountSession() {
  localStorage.removeItem('notTrollAccount');
  PLAYER_ID = getPlayerId();
}

const account0 = getAccount();
let PLAYER_ID = account0 ? account0.player_id : getPlayerId();
let unlockedLevels = 1;
let levelsMeta = [];

async function fetchLevelsMeta() {
  const res = await fetch(API_BASE_URL + '/levels');
  if (!res.ok) throw new Error('No se pudo cargar la lista de niveles.');
  return res.json();
}

async function fetchProgress() {
  const res = await fetch(API_BASE_URL + '/progress/' + encodeURIComponent(PLAYER_ID));
  if (!res.ok) throw new Error('No se pudo cargar el progreso.');
  return res.json();
}

async function saveProgress(unlocked) {
  if (!API_BASE_URL) return;
  try {
    const res = await fetch(API_BASE_URL + '/progress', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ player_id: PLAYER_ID, unlocked }),
    });
    if (res.ok) {
      const data = await res.json();
      unlockedLevels = Math.max(unlockedLevels, data.unlocked);
    }
  } catch (e) {
    console.warn('No se pudo guardar el progreso.', e);
  }
}

// ---------- Profile: login / register, backed by the same progress API ----------
const authForm = document.getElementById('authForm');
const authEmail = document.getElementById('authEmail');
const authPassword = document.getElementById('authPassword');
const authError = document.getElementById('authError');
const authSubmitBtn = document.getElementById('authSubmitBtn');
const authTabLogin = document.getElementById('authTabLogin');
const authTabRegister = document.getElementById('authTabRegister');
const profileLoggedOut = document.getElementById('profileLoggedOut');
const profileLoggedIn = document.getElementById('profileLoggedIn');
const profileWelcome = document.getElementById('profileWelcome');
let authMode = 'login';

function setAuthMode(mode) {
  authMode = mode;
  authTabLogin.classList.toggle('active', mode === 'login');
  authTabRegister.classList.toggle('active', mode === 'register');
  authSubmitBtn.textContent = mode === 'login' ? 'Iniciar sesion' : 'Crear cuenta';
  authPassword.autocomplete = mode === 'login' ? 'current-password' : 'new-password';
  authError.hidden = true;
}

authTabLogin.addEventListener('click', () => setAuthMode('login'));
authTabRegister.addEventListener('click', () => setAuthMode('register'));

function refreshProfileScreen() {
  const account = getAccount();
  if (account) {
    profileLoggedOut.hidden = true;
    profileLoggedIn.hidden = false;
    profileWelcome.textContent = 'Sesion iniciada como ' + account.email;
  } else {
    profileLoggedOut.hidden = false;
    profileLoggedIn.hidden = true;
    authForm.reset();
    authError.hidden = true;
    setAuthMode('login');
  }
}

async function applyLoggedInProgress(account) {
  const localUnlocked = unlockedLevels;
  setAccountSession(account);
  try {
    const progress = await fetchProgress();
    unlockedLevels = Math.max(progress.unlocked, localUnlocked);
  } catch (e) {
    unlockedLevels = localUnlocked;
  }
  await saveProgress(unlockedLevels);
  buildLevelGrid();
}

authForm.addEventListener('submit', async e => {
  e.preventDefault();
  if (!API_BASE_URL) {
    authError.textContent = 'Backend no configurado.';
    authError.hidden = false;
    return;
  }
  const email = authEmail.value.trim();
  const password = authPassword.value;
  authSubmitBtn.disabled = true;
  authError.hidden = true;
  try {
    const endpoint = authMode === 'login' ? '/auth/login' : '/auth/register';
    const res = await fetch(API_BASE_URL + endpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password }),
    });
    const data = await res.json();
    if (!res.ok) {
      authError.textContent = data.detail || 'No se pudo completar la operacion.';
      authError.hidden = false;
      return;
    }
    await applyLoggedInProgress(data);
    refreshProfileScreen();
  } catch (err) {
    authError.textContent = 'No se pudo conectar con el servidor.';
    authError.hidden = false;
  } finally {
    authSubmitBtn.disabled = false;
  }
});

document.getElementById('logoutBtn').addEventListener('click', () => {
  clearAccountSession();
  unlockedLevels = 1;
  fetchProgress().then(progress => {
    unlockedLevels = progress.unlocked;
    buildLevelGrid();
  }).catch(() => {});
  refreshProfileScreen();
});

// Procedural zigzag so the map reads as a winding trail rather than a grid,
// and always has consistent spacing no matter how many levels the backend
// reports — no more hand-tuned per-level coordinates that go stale (and
// collide) the moment a level is added or removed.
// Level 1 sits near the bottom of the content; each next level climbs
// higher, so a tall level list becomes a scrollable trail instead of a
// cramped fixed box — the viewport auto-scrolls to reveal newly unlocked
// levels as they're discovered.
const MAP_NODE_STEP = 92;   // vertical px between consecutive levels — comfortably more than the node's max rendered size
const MAP_TOP_PAD = 60;
const MAP_BOTTOM_PAD = 70;

function computeMapLayout(count, viewportH) {
  const contentH = Math.max(viewportH, MAP_TOP_PAD + MAP_BOTTOM_PAD + Math.max(0, count - 1) * MAP_NODE_STEP);
  const positions = [];
  for (let i = 0; i < count; i++) {
    const xPct = 50 + 30 * Math.sin(i * 0.85 + 0.6) + 9 * Math.sin(i * 2.3 + 1.4);
    positions.push({
      x: Math.min(86, Math.max(14, xPct)),
      y: contentH - MAP_BOTTOM_PAD - i * MAP_NODE_STEP,
    });
  }
  return { positions, contentH };
}

// Closed-padlock icon for locked map nodes — a plain line-art lock rather
// than the default emoji, recolored to sit on the node's dark background.
const LOCK_ICON_SVG = '<svg viewBox="0 0 24 24" width="60%" height="60%" fill="none">' +
  '<path d="M7 10V7a5 5 0 0 1 10 0v3" stroke="#9a8fc7" stroke-width="2" stroke-linecap="round"/>' +
  '<rect x="5" y="10" width="14" height="10" rx="2" fill="#332d4d" stroke="#9a8fc7" stroke-width="2"/>' +
  '<circle cx="12" cy="14.3" r="1.5" fill="#9a8fc7"/>' +
  '<rect x="11.1" y="15.2" width="1.8" height="2.6" rx="0.5" fill="#9a8fc7"/>' +
  '</svg>';

function drawMapPath(positions, width, contentH) {
  mapPath.setAttribute('width', width);
  mapPath.setAttribute('height', contentH);
  mapPath.setAttribute('viewBox', `0 0 ${width} ${contentH}`);
  if (positions.length < 2) { mapPath.innerHTML = ''; return; }
  const toD = pts => 'M ' + pts.map(p => (p.x / 100 * width) + ' ' + p.y).join(' L ');
  const traveledCount = Math.min(positions.length, Math.max(1, unlockedLevels));
  mapPath.innerHTML =
    `<path d="${toD(positions)}" class="mapPathGlow"/>` +
    `<path d="${toD(positions)}" class="mapPathFull"/>` +
    `<path d="${toD(positions.slice(0, traveledCount))}" class="mapPathTraveled"/>`;
}

function buildLevelGrid() {
  levelGrid.innerHTML = '';
  const count = levelsMeta.length || totalLevels || 1;
  const viewportW = mapScroll.clientWidth;
  const viewportH = mapScroll.clientHeight;
  const { positions, contentH } = computeMapLayout(count, viewportH);
  mapInner.style.height = contentH + 'px';

  let currentY = contentH;
  for (let i = 0; i < count; i++) {
    const pos = positions[i];
    const meta = levelsMeta[i] || { name: 'Nivel ' + (i + 1) };
    const lockedByProgress = i >= unlockedLevels;
    const locked = meta.locked || lockedByProgress;
    const isCurrent = !locked && i === unlockedLevels - 1;
    if (isCurrent) currentY = pos.y;
    const btn = document.createElement('button');
    btn.className = 'levelNode' + (locked ? ' locked' : '') + (isCurrent ? ' current' : '');
    btn.disabled = locked;
    const label = locked ? meta.name + ' - Bloqueado' : meta.name;
    btn.setAttribute('aria-label', label);
    btn.style.left = pos.x + '%';
    btn.style.top = pos.y + 'px';
    btn.dataset.level = String(i + 1);
    if (locked) {
      btn.innerHTML = LOCK_ICON_SVG;
      if (meta.locked) btn.dataset.badge = 'PROX';
    } else {
      btn.textContent = String(i + 1);
    }
    btn.addEventListener('click', () => {
      if (locked) return;
      closeAllScreens();
      loadLevel(i);
    });
    levelGrid.appendChild(btn);
  }
  drawMapPath(positions, viewportW, contentH);

  // Reveal the current/frontier level by scrolling it toward the middle of
  // the viewport, instead of dumping the player at the top of the trail.
  mapScroll.scrollTop = Math.max(0, Math.min(contentH - viewportH, currentY - viewportH / 2));
}

// Drag-to-pan the level map instead of a visible scrollbar: press and hold
// (mouse or touch), then move up/down to scroll. A click that moved past a
// small threshold is treated as a drag and swallowed so it doesn't also
// select the level node under the pointer.
(function setupMapDrag() {
  let dragging = false;
  let moved = false;
  let startY = 0;
  let startScrollTop = 0;
  let pointerId = null;

  mapScroll.addEventListener('pointerdown', (e) => {
    if (e.pointerType === 'mouse' && e.button !== 0) return;
    dragging = true;
    moved = false;
    startY = e.clientY;
    startScrollTop = mapScroll.scrollTop;
    pointerId = e.pointerId;
  });

  mapScroll.addEventListener('pointermove', (e) => {
    if (!dragging) return;
    const deltaY = e.clientY - startY;
    if (!moved && Math.abs(deltaY) > 4) {
      // Only now does this become an actual drag — capture the pointer so
      // scrolling keeps tracking it past the container's edges. Capturing
      // eagerly on every pointerdown instead would reroute the click event
      // for a plain tap away from the level node under it, since the browser
      // targets the synthesized click at the capturing element, not the
      // node — silently swallowing every level selection.
      moved = true;
      mapScroll.classList.add('dragging');
      mapScroll.setPointerCapture(pointerId);
    }
    if (moved) mapScroll.scrollTop = startScrollTop - deltaY;
  });

  function endDrag() {
    dragging = false;
    mapScroll.classList.remove('dragging');
  }
  mapScroll.addEventListener('pointerup', endDrag);
  mapScroll.addEventListener('pointercancel', endDrag);

  levelGrid.addEventListener('click', (e) => {
    if (moved) {
      e.stopPropagation();
      e.preventDefault();
      moved = false;
    }
  }, true);
})();

function showScreen(el) {
  mainMenu.hidden = true;
  levelMap.hidden = true;
  optionsMenu.hidden = true;
  profileMenu.hidden = true;
  infoMenu.hidden = true;
  el.hidden = false;
  paused = true;
  Ads.gameplayStop();
}

function closeAllScreens() {
  mainMenu.hidden = true;
  levelMap.hidden = true;
  optionsMenu.hidden = true;
  profileMenu.hidden = true;
  infoMenu.hidden = true;
  paused = false;
  if (level) Ads.gameplayStart();
}

function openLevelMap() {
  showScreen(levelMap);
  buildLevelGrid();
}

function openOptionsMenu() {
  showScreen(optionsMenu);
}

function openProfileMenu() {
  showScreen(profileMenu);
  refreshProfileScreen();
}

function openInfoMenu() {
  showScreen(infoMenu);
}

document.addEventListener('click', e => {
  const btn = e.target.closest('#playBtn, #mapMenuBtn, #optionsMenuBtn, #profileMenuBtn, #infoMenuBtn');
  if (!btn) return;
  if (btn.id === 'playBtn') {
    closeAllScreens();
    loadLevel(Math.max(0, unlockedLevels - 1));
  } else if (btn.id === 'mapMenuBtn') {
    openLevelMap();
  } else if (btn.id === 'optionsMenuBtn') {
    openOptionsMenu();
  } else if (btn.id === 'profileMenuBtn') {
    openProfileMenu();
  } else if (btn.id === 'infoMenuBtn') {
    openInfoMenu();
  }
});
document.getElementById('mapBtn').addEventListener('click', () => { if (level) openLevelMap(); });
document.getElementById('optionsBtn').addEventListener('click', () => { if (level) openOptionsMenu(); });
document.getElementById('menuFromOptionsBtn').addEventListener('click', () => showScreen(mainMenu));
document.querySelectorAll('[data-close]').forEach(btn => {
  btn.addEventListener('click', () => {
    closeAllScreens();
    if (!level) mainMenu.hidden = false;
  });
});

async function initMenus() {
  try {
    const meta = await fetchLevelsMeta();
    totalLevels = meta.total_levels;
    levelsMeta = meta.levels;
  } catch (e) {
    console.warn(e);
  }
  try {
    const progress = await fetchProgress();
    unlockedLevels = progress.unlocked;
  } catch (e) {
    console.warn(e);
  }
}

async function submitFinalScore() {
  if (!API_BASE_URL) return;
  const payload = {
    player: localStorage.getItem('notTrollPlayer') || 'Anonimo',
    deaths: totalDeaths,
    levels_completed: totalLevels,
    score: Math.max(0, 10000 - totalDeaths * 100),
  };
  try {
    await fetch(`${API_BASE_URL}/scores`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
  } catch (e) {
    console.warn('No se pudo enviar el puntaje al backend.', e);
  }
}

// ---------- Physics constants ----------
const GRAVITY = 1800;
const CUT_GRAVITY_MULT = 2.4;   // extra gravity when jump released early -> short hop control
const FALL_GRAVITY_MULT = 1.35; // extra gravity while falling -> snappier arcs
const MOVE_ACCEL = 2600;
const AIR_ACCEL_MULT = 0.85;
const FRICTION = 2200;
const MAX_SPEED = 220;
const JUMP_VELOCITY = 620;
const MAX_FALL = 900;
const COYOTE_TIME = 0.09;     // grace jump window after leaving a ledge
const JUMP_BUFFER_TIME = 0.12; // queue a jump pressed slightly before landing
const CAM_SMOOTH = 8;          // higher = camera catches up to target faster
const GROUND_LIFT = 90;        // shift the whole world up, leaving a clear strip at the
                                // bottom of the canvas for the overlaid touch controls

// ---------- Remote level loading ----------
async function fetchLevel(index) {
  if (!API_BASE_URL) {
    throw new Error('Configura window.API_BASE_URL para cargar niveles desde el backend.');
  }
  const res = await fetch(API_BASE_URL + '/levels/' + index + '?player_id=' + encodeURIComponent(PLAYER_ID));
  if (!res.ok) throw new Error('No se pudo cargar el nivel.');
  return res.json();
}

// ---------- Runtime state ----------
let levelIndex = 0;
let totalLevels = 0;
let level, player, camX, camTarget, deaths, totalDeaths, particles, stars, shake, portalMotes;
let saws = [], wallSpikes = [], platformState = [];
let fallingBlocks = [], bombs = [], teleporters = [], runWall = null;
let state = 'menu'; // menu | intro | playing | dead | complete
let stateTimer = 0;
let flash = 0; // full-screen flash overlay alpha, decays each frame
let portalCenter = null, pullStart = null, completeDuration = 1.1;
let advancingLevel = false;
camX = 0;
deaths = 0;
totalDeaths = 0;
particles = [];
stars = [];
shake = { t: 0, mag: 0 };

async function loadLevel(i) {
  try {
    advancingLevel = false;
    state = 'loading';
    overlayTitle.textContent = 'Cargando...';
    overlaySub.textContent = '';
    overlayTitle.classList.add('show');
    const data = await fetchLevel(i);
    levelIndex = data.index;
    totalLevels = data.total_levels;
    level = data.level;
    deaths = 0;
    if (i === 0) totalDeaths = 0;
    levelLabel.textContent = level.name;
    deathLabel.textContent = 'Muertes: 0';
    progressFill.style.width = '0%';
    stars = makeStars(level.width);
    portalMotes = makePortalMotes();
    resetEntities();
    showIntro();
  } catch (e) {
    advancingLevel = false;
    state = 'error';
    levelLabel.textContent = 'API requerida';
    deathLabel.textContent = 'Muertes: 0';
    overlayTitle.textContent = API_BASE_URL ? 'Servidor no responde' : 'Backend no configurado';
    overlaySub.textContent = e.message;
    overlayTitle.classList.add('show');
    overlaySub.classList.add('show');
    console.error(e);
  }
}

async function advanceAfterComplete() {
  if (advancingLevel) return;
  advancingLevel = true;
  const next = levelIndex + 1;
  const nextMeta = levelsMeta[next];
  const reachedEnd = next >= totalLevels || (nextMeta && nextMeta.locked);
  Ads.gameplayStop();
  await Ads.midgameBreak();
  if (reachedEnd) {
    await submitFinalScore();
    await saveProgress(Math.min(totalLevels, unlockedLevels));
    await loadLevel(0);
    return;
  }
  if (next + 1 > unlockedLevels) {
    await saveProgress(next + 1);
  }
  await loadLevel(next);
}

function makePortalMotes() {
  const arr = [];
  const colors = ['#c9a4ff', '#8fe9ff', '#ffffff'];
  for (let i = 0; i < 16; i++) {
    arr.push({
      angle: Math.random() * Math.PI * 2,
      radius: 34 + Math.random() * 44,
      speed: (0.5 + Math.random() * 1.1) * (Math.random() < 0.5 ? 1 : -1),
      bob: Math.random() * Math.PI * 2,
      size: 1.2 + Math.random() * 2.2,
      color: colors[i % colors.length],
    });
  }
  return arr;
}

function makeStars(levelWidth) {
  const arr = [];
  const count = Math.floor(levelWidth / 40);
  for (let i = 0; i < count; i++) {
    arr.push({
      x: Math.random() * levelWidth * 1.4,
      y: Math.random() * H * 0.55,
      r: Math.random() * 1.6 + 0.4,
      twinkle: Math.random() * Math.PI * 2,
    });
  }
  return arr;
}

function resetEntities() {
  player = {
    x: level.spawn.x, y: level.spawn.y,
    w: 26, h: 36,
    vx: 0, vy: 0,
    onGround: false,
    facing: 1,
    dead: false,
    falling: false,
    coyote: 0,
    jumpBuffer: 0,
    squashX: 1, squashY: 1,
    animTime: 0,
    rotation: 0,
    teleportCooldown: 0,
    groundType: null,
    groundPlatform: null,
    bounced: false,
  };
  camX = player.x - W / 2;
  camTarget = camX;
  particles = [];
  shake = { t: 0, mag: 0 };
  flash = 0;
  saws = (level.saws || []).map(s => ({ ...s, dir: 1 }));
  wallSpikes = (level.wallSpikes || []).map(w => ({ ...w, extend: 0, triggered: false, t: 0 }));
  platformState = (level.platforms || []).map(p => {
    const spikeW = p.spikeW || 40;
    return {
      ...p,
      triggered: false,
      t: 0,
      gone: false,
      poppedUp: false,
      spikeW,
      // narrow danger strip inside the platform — wide enough to notice, narrow enough to jump over
      spikeX: p.type === 'hidden_spike' ? p.x + p.w / 2 - spikeW / 2 : 0,
      shardsSpawned: false,
      falling: false,
      fallVy: 0,
      dir: 1,
      baseX: p.x,
      baseY: p.y,
    };
  });
  fallingBlocks = (level.fallingBlocks || []).map(b => ({ ...b, state: 'idle', t: 0, curY: b.y, vy: 0, gone: false }));
  bombs = (level.bombs || []).map(b => ({
    ...b,
    state: 'idle', t: 0,
    curX: b.kind === 'side' ? b.fromX : b.x,
    curY: b.y,
    vy: 0,
    gone: false,
  }));
  teleporters = (level.teleporters || []).map(tp => ({ ...tp }));
  runWall = level.runWall ? { ...level.runWall, x: level.runWall.startX } : null;
}

function restartLevel() {
  if (!level) return;
  deaths++;
  totalDeaths++;
  deathLabel.textContent = 'Muertes: ' + deaths;
  resetEntities();
  state = 'playing';
  Ads.gameplayStart();
}

function showIntro() {
  state = 'intro';
  stateTimer = 1.3;
  overlayTitle.textContent = level.name;
  overlaySub.textContent = level.hint || '';
  overlayTitle.classList.remove('show'); void overlayTitle.offsetWidth; overlayTitle.classList.add('show');
  overlaySub.classList.remove('show'); void overlaySub.offsetWidth; overlaySub.classList.add('show');
}

function addShake(mag, dur) {
  if (mag > shake.mag) shake.mag = mag;
  shake.t = Math.max(shake.t, dur);
}

function spawnBurst(x, y, count, opts) {
  opts = opts || {};
  for (let i = 0; i < count; i++) {
    const ang = Math.random() * Math.PI * 2;
    const spd = (opts.minSpeed || 60) + Math.random() * (opts.speedRange || 300);
    particles.push({
      x, y,
      vx: Math.cos(ang) * spd, vy: Math.sin(ang) * spd - (opts.upBias || 0),
      life: opts.life || 0.5, maxLife: opts.life || 0.5,
      color: opts.color || '#ff5757',
      size: opts.size || 5,
      type: opts.type || 'spark',
      rot: Math.random() * Math.PI * 2,
      rotSpeed: (Math.random() - 0.5) * 10,
      gravity: opts.gravity !== undefined ? opts.gravity : 900,
    });
  }
}

function spawnDust(x, y, count) {
  spawnBurst(x, y, count || 6, {
    color: 'rgba(230,230,230,0.85)', size: 4, life: 0.35, maxLife: 0.35,
    minSpeed: 20, speedRange: 90, upBias: 60, gravity: 250, type: 'dust',
  });
}

function killPlayer(cause) {
  if (player.dead) return;
  player.dead = true;
  state = 'dead';
  stateTimer = 0.55;
  player.squashX = 1.4; player.squashY = 0.5;
  spawnBurst(player.x + player.w / 2, player.y + player.h / 2, 20, {
    color: '#ff5757', size: 5, life: 0.55, maxLife: 0.55, speedRange: 420, gravity: 1000,
  });
  addShake(cause === 'void' ? 4 : 9, 0.3);
  flash = cause === 'void' ? 0.25 : 0.5;
  Sound.death();
}

function completeLevel() {
  state = 'complete';
  stateTimer = 1.1;
  completeDuration = 1.1;
  const g = level.goal;
  portalCenter = { x: g.x + g.w / 2, y: g.y + g.h / 2 };
  pullStart = { x: player.x, y: player.y };
  spawnBurst(portalCenter.x, portalCenter.y, 20, {
    color: '#b266ff', size: 5, life: 0.9, maxLife: 0.9, speedRange: 340, upBias: 150, gravity: 300, type: 'spark',
  });
  addShake(3, 0.2);
  Sound.goal();
}

function spawnPortalPull(cx, cy) {
  const ang = Math.random() * Math.PI * 2;
  const dist = 70 + Math.random() * 30;
  const sx = cx + Math.cos(ang) * dist;
  const sy = cy + Math.sin(ang) * dist * 0.6;
  particles.push({
    x: sx, y: sy,
    vx: (cx - sx) * 3.5, vy: (cy - sy) * 3.5,
    life: 0.4, maxLife: 0.4,
    color: Math.random() < 0.5 ? '#b266ff' : '#66dcff',
    size: 4, type: 'dust', rot: 0, rotSpeed: 0, gravity: 0,
  });
}

// ---------- Update ----------
let lastTime = performance.now();
function frame(now) {
  let dt = (now - lastTime) / 1000;
  lastTime = now;
  if (dt > 0.05) dt = 0.05; // clamp big pauses (tab switch etc.)

  update(dt);
  render();
  updateMusicPlayback();
  requestAnimationFrame(frame);
}

function update(dt) {
  if (paused) return;
  updateShake(dt);
  flash = Math.max(0, flash - dt * 1.8);

  if (state === 'intro') {
    stateTimer -= dt;
    if (stateTimer <= 0) { state = 'playing'; Ads.gameplayStart(); }
    return;
  }
  if (state === 'menu' || state === 'loading' || state === 'error') {
    return;
  }
  if (state === 'complete') {
    const progress = Math.min(1, 1 - stateTimer / completeDuration);
    const ease = progress * progress; // ease-in: accelerates toward the portal
    player.x = pullStart.x + (portalCenter.x - player.w / 2 - pullStart.x) * ease;
    player.y = pullStart.y + (portalCenter.y - player.h / 2 - pullStart.y) * ease;
    player.squashX = player.squashY = Math.max(0, 1 - progress * 1.15);
    player.rotation += dt * 16;
    player.falling = false;
    if (Math.random() < 0.7) spawnPortalPull(portalCenter.x, portalCenter.y);
    updateParticles(dt);
    stateTimer -= dt;
    if (stateTimer <= 0) {
      advanceAfterComplete();
    }
    return;
  }
  if (state === 'dead') {
    updateParticles(dt);
    stateTimer -= dt;
    if (stateTimer <= 0) restartLevel();
    return;
  }

  // state === 'playing'
  updatePlayer(dt);
  updateTraps(dt);
  updateMovingPlatforms(dt);
  updateSaws(dt);
  updateWallSpikes(dt);
  updateFallingBlocks(dt);
  updateBombs(dt);
  updateTeleporters(dt);
  updateRunWall(dt);
  updateParticles(dt);
  checkHazards();
  checkGoal();

  camTarget = Math.max(0, Math.min(player.x - W / 2 + player.facing * 40, level.width - W));
  camX += (camTarget - camX) * Math.min(1, CAM_SMOOTH * dt);

  progressFill.style.width = Math.min(100, Math.max(0, (player.x / level.width) * 100)) + '%';
}

function updateShake(dt) {
  if (shake.t > 0) {
    shake.t -= dt;
    if (shake.t <= 0) shake.mag = 0;
  }
}

function updatePlayer(dt) {
  const left = keys['ArrowLeft'] || keys['KeyA'];
  const right = keys['ArrowRight'] || keys['KeyD'];
  const jumpHeld = keys['Space'] || keys['ArrowUp'] || keys['KeyW'];
  const wasOnGround = player.onGround;
  const onIce = player.onGround && player.groundType === 'ice';
  const accel = MOVE_ACCEL * (player.onGround ? (onIce ? 0.35 : 1) : AIR_ACCEL_MULT);

  if (left && !right) {
    player.vx -= accel * dt;
    player.facing = -1;
  } else if (right && !left) {
    player.vx += accel * dt;
    player.facing = 1;
  } else if (player.onGround) {
    const f = (onIce ? FRICTION * 0.08 : FRICTION) * dt;
    if (player.vx > 0) player.vx = Math.max(0, player.vx - f);
    else if (player.vx < 0) player.vx = Math.min(0, player.vx + f);
  }
  player.vx = Math.max(-MAX_SPEED, Math.min(MAX_SPEED, player.vx));

  if (player.onGround) player.coyote = COYOTE_TIME;
  else player.coyote -= dt;
  player.jumpBuffer -= dt;

  if (player.jumpBuffer > 0 && player.coyote > 0) {
    player.vy = -JUMP_VELOCITY;
    player.onGround = false;
    player.coyote = 0;
    player.jumpBuffer = 0;
    player.squashX = 0.7; player.squashY = 1.35;
    spawnDust(player.x + player.w / 2, player.y + player.h, 5);
    Sound.jump();
  }

  let g = GRAVITY;
  if (player.vy < 0 && !jumpHeld && !player.bounced) g *= CUT_GRAVITY_MULT;
  else if (player.vy > 0) g *= FALL_GRAVITY_MULT;
  player.vy += g * dt;
  if (player.vy > MAX_FALL) player.vy = MAX_FALL;
  if (player.bounced && player.vy >= 0) player.bounced = false;

  // horizontal move + collision
  player.x += player.vx * dt;
  resolveCollisions('x');

  // vertical move + collision
  const impactVy = player.vy;
  player.y += player.vy * dt;
  player.onGround = false;
  player.groundType = null;
  player.groundPlatform = null;
  resolveCollisions('y');

  if (!wasOnGround && player.onGround) {
    const hard = impactVy > 480;
    player.squashX = hard ? 1.45 : 1.25;
    player.squashY = hard ? 0.55 : 0.75;
    spawnDust(player.x + player.w / 2, player.y + player.h, hard ? 9 : 5);
    if (hard) addShake(2.5, 0.12);
    Sound.land();
  }

  player.x = Math.max(0, Math.min(player.x, level.width - player.w));

  // squash/stretch relaxes back toward 1 each frame (framerate independent)
  const relax = 1 - Math.exp(-14 * dt);
  player.squashX += (1 - player.squashX) * relax;
  player.squashY += (1 - player.squashY) * relax;

  // running dust trail + leg animation while grounded and moving
  if (player.onGround && Math.abs(player.vx) > 40) {
    player.animTime += dt * (Math.abs(player.vx) / 60);
    if (Math.random() < 0.35) spawnDust(player.x + player.w / 2, player.y + player.h, 1);
  }

  player.falling = !player.onGround && player.y > H - 40 - GROUND_LIFT;
  if (player.falling) player.rotation += dt * 9 * (player.facing || 1);
  else player.rotation *= Math.max(0, 1 - dt * 10);
}

function solidPlatforms() {
  return platformState.filter(p => {
    if (p.gone) return false;
    if (p.type === 'fake_floor') return false; // never solid — that's the troll
    return true;
  });
}

function resolveCollisions(axis) {
  const solids = solidPlatforms();
  for (const p of solids) {
    if (!overlap(player, p)) continue;
    if (axis === 'x') {
      if (player.vx > 0) player.x = p.x - player.w;
      else if (player.vx < 0) player.x = p.x + p.w;
      player.vx = 0;
    } else {
      if (player.vy > 0) {
        player.y = p.y - player.h;
        if (p.type === 'bounce') {
          player.vy = -(p.power || 950);
          player.bounced = true;
          player.squashX = 0.6; player.squashY = 1.5;
          spawnDust(player.x + player.w / 2, player.y + player.h, 8);
          addShake(2, 0.1);
          Sound.jump();
        } else {
          player.vy = 0;
          player.onGround = true;
          player.groundType = p.type;
          player.groundPlatform = p;
        }
        if (p.type === 'hidden_spike' && !p.triggered) {
          p.triggered = true;
          p.t = 0;
        }
        if (p.type === 'crumble' && !p.triggered) {
          p.triggered = true;
          p.t = 0;
        }
        if (p.type === 'hidden_bomb' && !p.triggered) {
          p.triggered = true;
          p.t = 0;
        }
      } else if (player.vy < 0) {
        player.y = p.y + p.h;
        player.vy = 0;
      }
    }
  }
}

function overlap(a, b) {
  return a.x < b.x + b.w && a.x + a.w > b.x && a.y < b.y + b.h && a.y + a.h > b.y;
}

function rect(x, y, w, h) {
  return { x, y, w, h };
}

function updateTraps(dt) {
  for (const p of platformState) {
    if (p.type === 'hidden_spike') {
      // pops up either when triggered by stepping on it, or when player crosses triggerX (whichever first)
      if (!p.triggered && p.triggerX !== undefined && player.x + player.w > p.triggerX) {
        p.triggered = true;
        p.t = 0;
      }
      if (p.triggered && !p.poppedUp) {
        p.t += dt;
        if (p.t >= p.delay) {
          p.poppedUp = true;
          Sound.pop();
          addShake(1.5, 0.08);
        }
      }
    }
    if (p.type === 'crumble' && p.triggered && !p.gone) {
      p.t += dt;
      if (p.t >= p.delay) {
        p.gone = true;
        Sound.crumble();
        spawnBurst(p.x + p.w / 2, p.y + p.h / 2, 10, {
          color: '#8b5a2b', size: 6, life: 0.6, maxLife: 0.6, speedRange: 140, gravity: 1400, type: 'debris',
        });
      }
    }
    if (p.type === 'hidden_bomb') {
      if (!p.triggered && p.triggerX !== undefined && player.x + player.w > p.triggerX) {
        p.triggered = true;
        p.t = 0;
      }
      if (p.triggered && !p.gone) {
        p.t += dt;
        if (p.t >= p.delay) {
          p.gone = true;
          const cx = p.x + p.w / 2, cy = p.y;
          const dist = Math.hypot((player.x + player.w / 2) - cx, (player.y + player.h / 2) - cy);
          if (!player.dead && dist < (p.blastRadius || 70)) killPlayer('bomb');
          addShake(7, 0.3);
          flash = Math.max(flash, 0.35);
          Sound.boom();
          spawnBurst(cx, cy, 18, {
            color: '#ffb347', size: 6, life: 0.5, maxLife: 0.5, speedRange: 320, gravity: 700, type: 'spark',
          });
        }
      }
    }
    // Fake floor: the moment the player actually falls through it, the
    // block itself drops away too instead of just sitting there — sells
    // the "the floor was never real" gag instead of the player silently
    // clipping through a static tile.
    if (p.type === 'fake_floor' && !p.falling && overlap(player, p)) {
      p.falling = true;
      p.fallVy = 40;
      Sound.crumble();
      spawnBurst(p.x + p.w / 2, p.y + p.h / 2, 12, {
        color: '#3d6b30', size: 6, life: 0.6, maxLife: 0.6, speedRange: 160, gravity: 1200, type: 'debris',
      });
    }
    if (p.falling && !p.gone) {
      p.fallVy += 2000 * dt;
      p.y += p.fallVy * dt;
      if (p.y > H + 200) p.gone = true;
    }
  }
}

function updateMovingPlatforms(dt) {
  for (const p of platformState) {
    if (p.type !== 'moving' || p.gone) continue;
    const prevX = p.x, prevY = p.y;
    if (p.axis === 'y') {
      p.y += p.speed * p.dir * dt;
      if (p.y >= p.maxY) { p.y = p.maxY; p.dir = -1; }
      if (p.y <= p.minY) { p.y = p.minY; p.dir = 1; }
    } else {
      p.x += p.speed * p.dir * dt;
      if (p.x >= p.maxX) { p.x = p.maxX; p.dir = -1; }
      if (p.x <= p.minX) { p.x = p.minX; p.dir = 1; }
    }
    if (player.onGround && player.groundPlatform === p) {
      player.x += p.x - prevX;
      player.y += p.y - prevY;
    }
  }
}

function updateSaws(dt) {
  for (const s of saws) {
    s.x += s.speed * s.dir * dt;
    if (s.x >= s.maxX) { s.x = s.maxX; s.dir = -1; }
    if (s.x <= s.minX) { s.x = s.minX; s.dir = 1; }
  }
}

function updateWallSpikes(dt) {
  for (const w of wallSpikes) {
    if (!w.triggered && player.x + player.w > w.triggerX) {
      w.triggered = true;
      w.t = 0;
    }
    if (w.triggered) {
      w.t += dt;
      const progress = Math.min(1, Math.max(0, (w.t - w.delay) / 0.15));
      if (progress > 0 && w.extend === 0) Sound.pop();
      w.extend = progress * (w.reach || 90);
    }
  }
}

function updateFallingBlocks(dt) {
  for (const b of fallingBlocks) {
    if (b.gone) continue;
    if (b.state === 'idle') {
      if (player.x + player.w > b.triggerX) { b.state = 'warn'; b.t = 0; }
    } else if (b.state === 'warn') {
      b.t += dt;
      if (b.t >= b.delay) { b.state = 'falling'; b.vy = 60; }
    } else if (b.state === 'falling') {
      b.vy += 2200 * dt;
      b.curY += b.vy * dt;
      if (!player.dead && overlap(player, rect(b.x, b.curY, b.w, b.h))) killPlayer('crush');
      if (b.curY + b.h >= b.groundY) {
        b.curY = b.groundY - b.h;
        b.state = 'landed';
        b.t = 0;
        addShake(6, 0.25);
        Sound.boom();
        spawnBurst(b.x + b.w / 2, b.groundY, 14, {
          color: '#8b5a2b', size: 6, life: 0.5, maxLife: 0.5, speedRange: 220, gravity: 900, type: 'debris',
        });
      }
    } else if (b.state === 'landed') {
      b.t += dt;
      if (b.t > 0.6) b.gone = true;
    }
  }
}

function updateBombs(dt) {
  for (const b of bombs) {
    if (b.gone) continue;
    if (b.state === 'idle') {
      if (player.x + player.w > b.triggerX) { b.state = 'warn'; b.t = 0; }
    } else if (b.state === 'warn') {
      b.t += dt;
      if (b.t >= b.delay) {
        b.state = 'active';
        if (b.kind === 'sky') { b.curY = b.y; b.vy = 40; }
      }
    } else if (b.state === 'active') {
      if (b.kind === 'sky') {
        b.vy += 2000 * dt;
        b.curY += b.vy * dt;
        const dx = (player.x + player.w / 2) - b.x;
        const dy = (player.y + player.h / 2) - b.curY;
        if (!player.dead && Math.hypot(dx, dy) < b.radius) killPlayer('bomb');
        if (b.curY >= b.groundY) {
          const bdx = (player.x + player.w / 2) - b.x;
          const bdy = (player.y + player.h / 2) - b.groundY;
          if (!player.dead && Math.hypot(bdx, bdy) < (b.blastRadius || b.radius * 1.8)) killPlayer('bomb');
          addShake(7, 0.3);
          flash = Math.max(flash, 0.35);
          Sound.boom();
          spawnBurst(b.x, b.groundY, 20, {
            color: '#ffb347', size: 6, life: 0.5, maxLife: 0.5, speedRange: 340, gravity: 600, type: 'spark',
          });
          b.gone = true;
        }
      } else {
        b.curX += b.speed * b.dir * dt;
        const dx = (player.x + player.w / 2) - b.curX;
        const dy = (player.y + player.h / 2) - b.y;
        if (!player.dead && Math.hypot(dx, dy) < b.radius) {
          killPlayer('bomb');
          addShake(7, 0.3);
          flash = Math.max(flash, 0.35);
          Sound.boom();
          spawnBurst(b.curX, b.y, 20, {
            color: '#ffb347', size: 6, life: 0.5, maxLife: 0.5, speedRange: 340, gravity: 300, type: 'spark',
          });
          b.gone = true;
        }
        const outOfBounds = b.dir === 1 ? b.curX > b.toX : b.curX < b.toX;
        if (outOfBounds) b.gone = true;
      }
    }
  }
}

function updateTeleporters(dt) {
  if (player.teleportCooldown > 0) { player.teleportCooldown -= dt; return; }
  for (const tp of teleporters) {
    if (overlap(player, tp)) {
      spawnBurst(player.x + player.w / 2, player.y + player.h / 2, 14, {
        color: '#8fe9ff', size: 5, life: 0.4, maxLife: 0.4, speedRange: 260, gravity: 0, type: 'spark',
      });
      player.x = tp.toX;
      player.y = tp.toY;
      player.vx = 0;
      player.vy = 0;
      spawnBurst(player.x + player.w / 2, player.y + player.h / 2, 14, {
        color: '#c9a4ff', size: 5, life: 0.4, maxLife: 0.4, speedRange: 260, gravity: 0, type: 'spark',
      });
      player.teleportCooldown = 0.35;
      addShake(2, 0.15);
      Sound.pop();
      break;
    }
  }
}

function updateRunWall(dt) {
  if (!runWall) return;
  runWall.x += runWall.speed * dt;
  if (!player.dead && player.x < runWall.x) killPlayer('crush');
}

function updateParticles(dt) {
  for (const pt of particles) {
    pt.x += pt.vx * dt;
    pt.y += pt.vy * dt;
    pt.vy += (pt.gravity !== undefined ? pt.gravity : 900) * dt;
    pt.life -= dt;
    if (pt.rot !== undefined) pt.rot += pt.rotSpeed * dt;
  }
  particles = particles.filter(pt => pt.life > 0);
}

function checkHazards() {
  if (player.dead) return;
  for (const h of level.hazards || []) {
    if (h.type === 'void' && overlap(player, h)) { killPlayer('void'); return; }
    if (h.type === 'spike' && overlap(player, h)) { killPlayer('spike'); return; }
  }
  for (const p of platformState) {
    // player's feet rest exactly on p.y after landing, so the spike hitbox
    // must straddle that surface line or a standing player never overlaps it
    if (p.type === 'hidden_spike' && p.poppedUp && overlap(player, rect(p.spikeX, p.y - 8, p.spikeW, 16))) { killPlayer('spike'); return; }
  }
  for (const s of saws) {
    const dx = (player.x + player.w / 2) - s.x;
    const dy = (player.y + player.h / 2) - s.y;
    if (Math.hypot(dx, dy) < s.r + 10) { killPlayer('saw'); return; }
  }
  for (const w of wallSpikes) {
    const spikeRect = w.dir === 1
      ? rect(w.x, w.y, w.extend, w.h)
      : rect(w.x - w.extend, w.y, w.extend, w.h);
    if (w.extend > 10 && overlap(player, spikeRect)) { killPlayer('spike'); return; }
  }
  // fell off the world
  if (player.y > H + 200) killPlayer('void');
}

function checkGoal() {
  if (state !== 'playing') return;
  if (overlap(player, level.goal)) completeLevel();
}

// ---------- Render ----------
function render() {
  ctx.clearRect(0, 0, W, H);
  drawBackground();

  ctx.save();
  let shakeX = 0, shakeY = 0;
  if (shake.t > 0) {
    shakeX = (Math.random() - 0.5) * shake.mag;
    shakeY = (Math.random() - 0.5) * shake.mag;
  }
  ctx.translate(Math.round(-camX + shakeX), Math.round(shakeY));

  if (level && player) {
    drawPlatforms();
    drawHazardsStatic();
    drawRunWall();
    drawTeleporters();
    drawFallingBlocks();
    drawBombs();
    drawSaws();
    drawWallSpikes();
    drawGoal();
    if (!player.dead || state === 'dead') drawPlayer();
    drawParticles();
  }

  ctx.restore();

  drawVignette();
  if (flash > 0) {
    ctx.fillStyle = `rgba(255,60,60,${flash})`;
    ctx.fillRect(0, 0, W, H);
  }
}

function drawBackground() {
  if (bgImageReady) {
    ctx.drawImage(bgImage, 0, 0, W, H);
  } else {
    const g = ctx.createLinearGradient(0, 0, 0, H);
    g.addColorStop(0, '#171a33');
    g.addColorStop(0.6, '#2b2246');
    g.addColorStop(1, '#3a2a4d');
    ctx.fillStyle = g;
    ctx.fillRect(0, 0, W, H);
  }

  // stars (far parallax layer) — kept as a subtle overlay for depth on top of the art
  const t = performance.now() / 500;
  ctx.fillStyle = '#fff';
  for (const s of stars) {
    const sx = s.x - camX * 0.15;
    if (sx < -10 || sx > W + 10) continue;
    ctx.globalAlpha = 0.4 + Math.sin(t + s.twinkle) * 0.3;
    ctx.beginPath();
    ctx.arc(sx, s.y, s.r, 0, Math.PI * 2);
    ctx.fill();
  }
  ctx.globalAlpha = 1;
}

function drawVignette() {
  const r = ctx.createRadialGradient(W / 2, H / 2, H * 0.35, W / 2, H / 2, H * 0.85);
  r.addColorStop(0, 'rgba(0,0,0,0)');
  r.addColorStop(1, 'rgba(0,0,0,0.35)');
  ctx.fillStyle = r;
  ctx.fillRect(0, 0, W, H);
}

function drawPlatforms() {
  for (const p of platformState) {
    if (p.gone) continue;
    if (p.type === 'crumble') {
      const shakeAmt = p.triggered && !p.gone ? (Math.random() - 0.5) * 4 : 0;
      ctx.fillStyle = p.triggered ? '#a86a3d' : '#8b5a2b';
      ctx.fillRect(p.x + shakeAmt, p.y, p.w, p.h);
      ctx.fillStyle = '#6b4423';
      ctx.fillRect(p.x + shakeAmt, p.y, p.w, 6);
      if (p.triggered) {
        const progress = Math.min(1, p.t / p.delay);
        drawCracks(p.x + shakeAmt, p.y, p.w, p.h, progress);
      }
      continue;
    }
    if (p.type === 'fake_floor') {
      // deliberately identical look to normal solid floor — that's the trick
      ctx.fillStyle = '#4a7a3d';
      ctx.fillRect(p.x, p.y, p.w, p.h);
      ctx.fillStyle = '#5f9950';
      ctx.fillRect(p.x, p.y, p.w, 6);
      continue;
    }
    if (p.type === 'hidden_spike') {
      ctx.fillStyle = '#4a7a3d';
      ctx.fillRect(p.x, p.y, p.w, p.h);
      ctx.fillStyle = '#5f9950';
      ctx.fillRect(p.x, p.y, p.w, 6);
      if (p.poppedUp) {
        const wobble = Math.min(1, p.t - p.delay) * 3;
        ctx.fillStyle = '#d63b3b';
        const n = Math.max(1, Math.floor(p.spikeW / 18));
        for (let i = 0; i < n; i++) {
          const sx = p.spikeX + (i + 0.5) * (p.spikeW / n);
          ctx.beginPath();
          ctx.moveTo(sx - 9, p.y);
          ctx.lineTo(sx, p.y - 22 - wobble);
          ctx.lineTo(sx + 9, p.y);
          ctx.closePath();
          ctx.fill();
        }
      } else if (p.triggered) {
        // telegraph: a faint crack where the spikes are about to burst through
        ctx.strokeStyle = 'rgba(0,0,0,0.35)';
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.moveTo(p.spikeX, p.y + 2);
        ctx.lineTo(p.spikeX + p.spikeW, p.y + 2);
        ctx.stroke();
      }
      continue;
    }
    if (p.type === 'ice') {
      ctx.fillStyle = '#bfe9ff';
      ctx.fillRect(p.x, p.y, p.w, p.h);
      ctx.fillStyle = '#eaf9ff';
      ctx.fillRect(p.x, p.y, p.w, 6);
      ctx.strokeStyle = 'rgba(255,255,255,0.55)';
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.moveTo(p.x + p.w * 0.15, p.y + p.h - 4);
      ctx.lineTo(p.x + p.w * 0.45, p.y + 8);
      ctx.moveTo(p.x + p.w * 0.55, p.y + p.h - 4);
      ctx.lineTo(p.x + p.w * 0.85, p.y + 8);
      ctx.stroke();
      continue;
    }
    if (p.type === 'bounce') {
      ctx.fillStyle = '#f7b733';
      ctx.fillRect(p.x, p.y, p.w, p.h);
      ctx.fillStyle = '#ffe08a';
      ctx.fillRect(p.x, p.y, p.w, 6);
      ctx.strokeStyle = '#c9791a';
      ctx.lineWidth = 2;
      ctx.beginPath();
      const coils = Math.max(2, Math.floor(p.w / 22));
      for (let i = 0; i < coils; i++) {
        const cx = p.x + (i + 0.5) * (p.w / coils);
        ctx.moveTo(cx - 8, p.y + p.h * 0.5);
        ctx.lineTo(cx, p.y + 10);
        ctx.lineTo(cx + 8, p.y + p.h * 0.5);
      }
      ctx.stroke();
      continue;
    }
    if (p.type === 'moving') {
      ctx.fillStyle = '#7d8596';
      ctx.fillRect(p.x, p.y, p.w, p.h);
      ctx.fillStyle = '#a8b0c2';
      ctx.fillRect(p.x, p.y, p.w, 6);
      ctx.fillStyle = 'rgba(0,0,0,0.25)';
      const rivetY = p.y + p.h - 8;
      for (let bx = p.x + 8; bx < p.x + p.w; bx += 20) {
        ctx.beginPath();
        ctx.arc(bx, rivetY, 2.2, 0, Math.PI * 2);
        ctx.fill();
      }
      // directional arrow showing the axis it travels
      ctx.fillStyle = 'rgba(200,225,255,0.85)';
      const acx = p.x + p.w / 2, acy = p.y + p.h / 2;
      ctx.save();
      ctx.translate(acx, acy);
      if (p.axis === 'y') ctx.rotate(p.dir > 0 ? Math.PI / 2 : -Math.PI / 2);
      else if (p.dir < 0) ctx.rotate(Math.PI);
      ctx.beginPath();
      ctx.moveTo(7, 0);
      ctx.lineTo(-4, -6);
      ctx.lineTo(-4, 6);
      ctx.closePath();
      ctx.fill();
      ctx.restore();
      continue;
    }
    if (p.type === 'stone') {
      ctx.fillStyle = '#6b6f76';
      ctx.fillRect(p.x, p.y, p.w, p.h);
      ctx.fillStyle = '#888e99';
      ctx.fillRect(p.x, p.y, p.w, 6);
      ctx.strokeStyle = 'rgba(0,0,0,0.3)';
      ctx.lineWidth = 1;
      const rowH = 12;
      let row = 0;
      for (let ry = p.y + 6; ry < p.y + p.h; ry += rowH) {
        const offset = (row % 2) * 17;
        for (let bx = p.x + offset; bx < p.x + p.w; bx += 34) {
          ctx.strokeRect(bx, ry, 34, rowH);
        }
        row++;
      }
      continue;
    }
    // solid — subtle brick texture for depth
    ctx.fillStyle = '#4a7a3d';
    ctx.fillRect(p.x, p.y, p.w, p.h);
    ctx.fillStyle = '#5f9950';
    ctx.fillRect(p.x, p.y, p.w, 6);
    ctx.fillStyle = 'rgba(0,0,0,0.12)';
    for (let bx = p.x; bx < p.x + p.w; bx += 34) {
      ctx.fillRect(bx, p.y + 10, 1, p.h - 10);
    }
  }
}

function drawCracks(x, y, w, h, progress) {
  ctx.strokeStyle = `rgba(0,0,0,${0.3 + progress * 0.4})`;
  ctx.lineWidth = 1.5;
  const lines = Math.floor(progress * 5);
  for (let i = 0; i < lines; i++) {
    const cx = x + (i + 0.5) * (w / 5);
    ctx.beginPath();
    ctx.moveTo(cx, y);
    ctx.lineTo(cx + (Math.random() - 0.5) * 10, y + h * 0.5);
    ctx.lineTo(cx + (Math.random() - 0.5) * 14, y + h);
    ctx.stroke();
  }
}

function drawHazardsStatic() {
  for (const h of level.hazards || []) {
    if (h.type !== 'spike') continue;
    ctx.fillStyle = '#d63b3b';
    const n = Math.max(1, Math.floor(h.w / 20));
    for (let i = 0; i < n; i++) {
      const sx = h.x + (i + 0.5) * (h.w / n);
      ctx.beginPath();
      ctx.moveTo(sx - 10, h.y + h.h);
      ctx.lineTo(sx, h.y);
      ctx.lineTo(sx + 10, h.y + h.h);
      ctx.closePath();
      ctx.fill();
    }
  }
}

function drawSaws() {
  for (const s of saws) {
    ctx.save();
    ctx.fillStyle = 'rgba(0,0,0,0.25)';
    ctx.beginPath();
    ctx.arc(s.x, s.y + 4, s.r * 0.9, 0, Math.PI * 2);
    ctx.fill();
    ctx.translate(s.x, s.y);
    ctx.rotate(performance.now() / 100);
    ctx.fillStyle = '#c9c9c9';
    ctx.beginPath();
    const spikes = 10;
    for (let i = 0; i < spikes * 2; i++) {
      const rad = i % 2 === 0 ? s.r : s.r * 0.7;
      const ang = (i / (spikes * 2)) * Math.PI * 2;
      ctx.lineTo(Math.cos(ang) * rad, Math.sin(ang) * rad);
    }
    ctx.closePath();
    ctx.fill();
    ctx.fillStyle = '#777';
    ctx.beginPath();
    ctx.arc(0, 0, s.r * 0.28, 0, Math.PI * 2);
    ctx.fill();
    ctx.restore();
  }
}

function drawWallSpikes() {
  ctx.fillStyle = '#999';
  for (const w of wallSpikes) {
    ctx.fillRect(w.x - (w.dir === 1 ? 6 : 0), w.y, 6, w.h);
  }
  ctx.fillStyle = '#d63b3b';
  for (const w of wallSpikes) {
    if (w.extend <= 0) continue;
    const bx = w.dir === 1 ? w.x : w.x - w.extend;
    ctx.fillRect(bx, w.y, w.extend, w.h);
  }
}

function drawFallingBlocks() {
  for (const b of fallingBlocks) {
    if (b.gone) continue;
    if (b.state === 'warn') {
      const pulse = 0.4 + Math.sin(performance.now() / 90) * 0.3;
      ctx.fillStyle = `rgba(255,80,80,${0.25 + pulse * 0.25})`;
      ctx.beginPath();
      ctx.ellipse(b.x + b.w / 2, b.groundY - 4, b.w * 0.55, 10, 0, 0, Math.PI * 2);
      ctx.fill();
      ctx.fillStyle = `rgba(255,60,60,${0.6 + pulse * 0.4})`;
      ctx.font = 'bold 20px sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText('!', b.x + b.w / 2, b.groundY - 20);
      ctx.textAlign = 'start';
      continue;
    }
    if (b.state === 'falling' || b.state === 'landed') {
      ctx.fillStyle = '#6b4a2b';
      ctx.fillRect(b.x, b.curY, b.w, b.h);
      ctx.fillStyle = '#8b5a2b';
      ctx.fillRect(b.x + 4, b.curY + 4, b.w - 8, b.h - 8);
      ctx.strokeStyle = 'rgba(0,0,0,0.4)';
      ctx.lineWidth = 2;
      ctx.strokeRect(b.x + 3, b.curY + 3, b.w - 6, b.h - 6);
    }
  }
}

function drawBombIcon(x, y, r) {
  ctx.save();
  ctx.translate(x, y);
  ctx.fillStyle = '#1a1a1a';
  ctx.beginPath();
  ctx.arc(0, 0, r, 0, Math.PI * 2);
  ctx.fill();
  ctx.strokeStyle = '#444';
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.moveTo(r * 0.3, -r * 0.8);
  ctx.lineTo(r * 0.7, -r * 1.4);
  ctx.stroke();
  ctx.fillStyle = '#ffb347';
  ctx.beginPath();
  ctx.arc(r * 0.7, -r * 1.4, 3, 0, Math.PI * 2);
  ctx.fill();
  ctx.restore();
}

function drawBombs() {
  for (const b of bombs) {
    if (b.gone) continue;
    if (b.state === 'warn') {
      const pulse = 0.4 + Math.sin(performance.now() / 90) * 0.3;
      if (b.kind === 'sky') {
        ctx.fillStyle = `rgba(255,140,50,${0.25 + pulse * 0.25})`;
        ctx.beginPath();
        ctx.ellipse(b.x, b.groundY - 4, 34, 9, 0, 0, Math.PI * 2);
        ctx.fill();
      } else {
        const wx = b.dir === 1 ? camX + 26 : camX + W - 26;
        ctx.fillStyle = `rgba(255,140,50,${0.5 + pulse * 0.5})`;
        ctx.beginPath();
        ctx.moveTo(wx, b.y - 14);
        ctx.lineTo(wx + (b.dir === 1 ? 16 : -16), b.y);
        ctx.lineTo(wx, b.y + 14);
        ctx.closePath();
        ctx.fill();
      }
      continue;
    }
    if (b.state === 'active') {
      drawBombIcon(b.kind === 'sky' ? b.x : b.curX, b.kind === 'sky' ? b.curY : b.y, 14);
    }
  }
}

function drawTeleporters() {
  const t = performance.now() / 500;
  for (const tp of teleporters) {
    const cx = tp.x + tp.w / 2, cy = tp.y + tp.h / 2;
    ctx.save();
    ctx.translate(cx, cy);
    ctx.rotate(t);
    ctx.strokeStyle = 'rgba(143,233,255,0.8)';
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.ellipse(0, 0, tp.w / 2, tp.h / 2, 0, 0, Math.PI * 1.5);
    ctx.stroke();
    ctx.restore();
    ctx.save();
    ctx.globalCompositeOperation = 'lighter';
    ctx.fillStyle = 'rgba(143,233,255,0.35)';
    ctx.beginPath();
    ctx.ellipse(cx, cy, tp.w / 2, tp.h / 2, 0, 0, Math.PI * 2);
    ctx.fill();
    ctx.restore();
  }
}

function drawRunWall() {
  if (!runWall) return;
  const fadeStart = Math.max(0, runWall.x - 120);
  const g = ctx.createLinearGradient(fadeStart, 0, runWall.x, 0);
  g.addColorStop(0, 'rgba(10,6,20,0)');
  g.addColorStop(1, 'rgba(10,6,20,0.95)');
  ctx.fillStyle = g;
  ctx.fillRect(fadeStart, runWall.y, runWall.x - fadeStart, runWall.h);
  ctx.fillStyle = '#0a0614';
  ctx.fillRect(0, runWall.y, fadeStart, runWall.h);
  ctx.strokeStyle = 'rgba(178,102,255,0.5)';
  ctx.lineWidth = 3;
  ctx.beginPath();
  ctx.moveTo(runWall.x, runWall.y);
  ctx.lineTo(runWall.x, runWall.y + runWall.h);
  ctx.stroke();
}

function drawGoal() {
  const gpt = level.goal;
  const baseCx = gpt.x + gpt.w / 2, baseCy = gpt.y + gpt.h / 2;
  const bob = Math.sin(performance.now() / 900) * 3;
  const cx = baseCx, cy = baseCy + bob;
  const rx = gpt.w / 2 + 2, ry = gpt.h / 2 + 3;
  const t = performance.now() / 480;
  const pulse = 0.5 + Math.sin(performance.now() / 220) * 0.5;

  // ground light pool — grounds the portal in the scene
  ctx.save();
  ctx.translate(cx, gpt.y + gpt.h + 6);
  const pool = ctx.createRadialGradient(0, 0, 2, 0, 0, rx * 1.6);
  pool.addColorStop(0, `rgba(178,102,255,${0.35 + pulse * 0.15})`);
  pool.addColorStop(1, 'rgba(178,102,255,0)');
  ctx.fillStyle = pool;
  ctx.beginPath();
  ctx.ellipse(0, 0, rx * 1.6, 7, 0, 0, Math.PI * 2);
  ctx.fill();
  ctx.restore();

  drawPortalArch(cx, baseCy, rx, ry);

  ctx.save();
  ctx.translate(cx, cy);

  // outer atmospheric glow (soft, additive so it layers nicely against the arch)
  ctx.globalCompositeOperation = 'lighter';
  const glow = ctx.createRadialGradient(0, 0, ry * 0.3, 0, 0, ry * 2.3);
  glow.addColorStop(0, `rgba(178,102,255,${0.4 + pulse * 0.22})`);
  glow.addColorStop(0.6, `rgba(120,80,220,${0.18 + pulse * 0.1})`);
  glow.addColorStop(1, 'rgba(120,80,220,0)');
  ctx.fillStyle = glow;
  ctx.beginPath();
  ctx.ellipse(0, 0, ry * 2.3, ry * 2.3, 0, 0, Math.PI * 2);
  ctx.fill();

  // portal core — layered gradient: hot white center fading through cyan/purple to near-black rim
  const core = ctx.createRadialGradient(0, 0, 0, 0, 0, Math.max(rx, ry));
  core.addColorStop(0, `rgba(255,255,255,${0.85 + pulse * 0.15})`);
  core.addColorStop(0.28, 'rgba(150,225,255,0.85)');
  core.addColorStop(0.6, 'rgba(150,90,230,0.9)');
  core.addColorStop(1, '#12051f');
  ctx.globalCompositeOperation = 'source-over';
  ctx.fillStyle = core;
  ctx.beginPath();
  ctx.ellipse(0, 0, rx, ry, 0, 0, Math.PI * 2);
  ctx.fill();

  // spiral energy lines winding into the core
  ctx.globalCompositeOperation = 'lighter';
  for (let s = 0; s < 2; s++) {
    ctx.strokeStyle = s === 0 ? 'rgba(210,170,255,0.55)' : 'rgba(140,230,255,0.5)';
    ctx.lineWidth = 1.4;
    ctx.beginPath();
    const dir = s === 0 ? 1 : -1;
    for (let a = 0; a <= Math.PI * 3.4; a += 0.25) {
      const rr = (a / (Math.PI * 3.4));
      const ang = a * dir + t * 2.2 * dir;
      const px = Math.cos(ang) * rx * rr;
      const py = Math.sin(ang) * ry * rr;
      if (a === 0) ctx.moveTo(px, py); else ctx.lineTo(px, py);
    }
    ctx.stroke();
  }

  // rotating vortex rings, alternating direction/color for a spinning feel
  ctx.lineCap = 'round';
  for (let i = 0; i < 4; i++) {
    ctx.strokeStyle = i % 2 === 0 ? 'rgba(198,132,255,0.8)' : 'rgba(122,230,255,0.7)';
    ctx.lineWidth = 2.6 - i * 0.3;
    ctx.beginPath();
    const scale = 0.98 - i * 0.2;
    ctx.ellipse(0, 0, rx * scale, ry * scale, t * (i % 2 === 0 ? 1 : -1) + i, 0, Math.PI * 1.3);
    ctx.stroke();
  }
  ctx.globalCompositeOperation = 'source-over';
  ctx.restore();

  drawPortalMotes(cx, cy);

  // occasional crackle of energy arcing off the rim
  if (Math.random() < 0.045) drawPortalCrackle(cx, cy, rx, ry);
}

function drawPortalArch(cx, cy, rx, ry) {
  const archW = rx * 2 + 26, archH = ry * 2 + 34;
  const left = cx - archW / 2, right = cx + archW / 2, top = cy - archH / 2 + 6, bottom = cy + archH / 2;
  ctx.save();

  const stone = ctx.createLinearGradient(left, 0, right, 0);
  stone.addColorStop(0, '#2e2540');
  stone.addColorStop(0.5, '#3c3055');
  stone.addColorStop(1, '#241d34');
  ctx.fillStyle = stone;

  const pillarW = 12;
  ctx.beginPath();
  ctx.roundRect(left, top, pillarW, bottom - top, 4);
  ctx.fill();
  ctx.beginPath();
  ctx.roundRect(right - pillarW, top, pillarW, bottom - top, 4);
  ctx.fill();
  // arch top connecting the pillars
  ctx.beginPath();
  ctx.moveTo(left, top + 10);
  ctx.quadraticCurveTo(cx, top - 20, right, top + 10);
  ctx.lineTo(right - pillarW, top + 14);
  ctx.quadraticCurveTo(cx, top - 4, left + pillarW, top + 14);
  ctx.closePath();
  ctx.fill();

  // edge highlight for a carved-stone feel
  ctx.strokeStyle = 'rgba(200,170,255,0.25)';
  ctx.lineWidth = 1.5;
  ctx.beginPath();
  ctx.roundRect(left, top, pillarW, bottom - top, 4);
  ctx.stroke();
  ctx.beginPath();
  ctx.roundRect(right - pillarW, top, pillarW, bottom - top, 4);
  ctx.stroke();

  // glowing runes embedded in the pillars, pulsing gently out of sync with each other
  const runeGlow = (phase) => 0.4 + Math.sin(performance.now() / 260 + phase) * 0.4;
  ctx.fillStyle = `rgba(178,102,255,${runeGlow(0)})`;
  ctx.beginPath(); ctx.arc(left + pillarW / 2, top + 26, 3, 0, Math.PI * 2); ctx.fill();
  ctx.fillStyle = `rgba(122,230,255,${runeGlow(1.5)})`;
  ctx.beginPath(); ctx.arc(right - pillarW / 2, top + 46, 3, 0, Math.PI * 2); ctx.fill();
  ctx.fillStyle = `rgba(178,102,255,${runeGlow(3)})`;
  ctx.beginPath(); ctx.arc(left + pillarW / 2, bottom - 24, 3, 0, Math.PI * 2); ctx.fill();

  ctx.restore();
}

function drawPortalMotes(cx, cy) {
  const t = performance.now();
  ctx.save();
  ctx.globalCompositeOperation = 'lighter';
  for (const m of portalMotes) {
    const ang = m.angle + (t / 1000) * m.speed;
    const px = cx + Math.cos(ang) * m.radius;
    const py = cy + Math.sin(ang) * m.radius * 0.5 + Math.sin(t / 300 + m.bob) * 2;
    ctx.globalAlpha = 0.45 + Math.sin(t / 350 + m.bob) * 0.35;
    ctx.fillStyle = m.color;
    ctx.beginPath();
    ctx.arc(px, py, m.size, 0, Math.PI * 2);
    ctx.fill();
  }
  ctx.restore();
  ctx.globalAlpha = 1;
}

function drawPortalCrackle(cx, cy, rx, ry) {
  const ang = Math.random() * Math.PI * 2;
  const startX = cx + Math.cos(ang) * rx * 0.95, startY = cy + Math.sin(ang) * ry * 0.95;
  ctx.save();
  ctx.globalCompositeOperation = 'lighter';
  ctx.strokeStyle = 'rgba(220,190,255,0.9)';
  ctx.lineWidth = 1.5;
  ctx.beginPath();
  ctx.moveTo(startX, startY);
  let x = startX, y = startY;
  for (let i = 0; i < 4; i++) {
    x += Math.cos(ang) * 8 + (Math.random() - 0.5) * 14;
    y += Math.sin(ang) * 8 + (Math.random() - 0.5) * 14;
    ctx.lineTo(x, y);
  }
  ctx.stroke();
  ctx.restore();
}

function drawPlayer() {
  const cx = player.x + player.w / 2;
  const cy = player.y + player.h / 2;
  ctx.save();
  ctx.translate(cx, cy);
  if (player.falling || state === 'complete') ctx.rotate(player.rotation);
  ctx.scale(player.squashX, player.squashY);
  ctx.translate(-player.w / 2, -player.h / 2);

  ctx.fillStyle = player.dead ? 'rgba(30,30,30,0.6)' : '#151515';
  // rounded-ish body
  const r = 6;
  ctx.beginPath();
  ctx.moveTo(r, 0);
  ctx.lineTo(player.w - r, 0);
  ctx.quadraticCurveTo(player.w, 0, player.w, r);
  ctx.lineTo(player.w, player.h - 8);
  ctx.quadraticCurveTo(player.w, player.h, player.w - r, player.h);
  ctx.lineTo(r, player.h);
  ctx.quadraticCurveTo(0, player.h, 0, player.h - 8);
  ctx.lineTo(0, r);
  ctx.quadraticCurveTo(0, 0, r, 0);
  ctx.fill();

  // legs — alternate while running, together while airborne
  if (!player.dead) {
    ctx.fillStyle = '#151515';
    const running = player.onGround && Math.abs(player.vx) > 30;
    const phase = running ? Math.sin(player.animTime * 6) * 5 : 0;
    ctx.fillRect(4 + phase * 0.4, player.h - 2, 7, 6);
    ctx.fillRect(player.w - 11 - phase * 0.4, player.h - 2, 7, 6);
  }

  // eye for facing direction
  ctx.fillStyle = '#fff';
  const ex = player.facing === 1 ? player.w - 9 : 5;
  ctx.fillRect(ex, 9, 4, 4);
  ctx.restore();
}

function drawParticles() {
  for (const p of particles) {
    const alpha = Math.max(0, p.life / p.maxLife);
    ctx.globalAlpha = alpha;
    ctx.fillStyle = p.color;
    if (p.type === 'dust') {
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.size * alpha, 0, Math.PI * 2);
      ctx.fill();
    } else if (p.type === 'debris') {
      ctx.save();
      ctx.translate(p.x, p.y);
      ctx.rotate(p.rot);
      ctx.fillRect(-p.size / 2, -p.size / 2, p.size, p.size);
      ctx.restore();
    } else {
      ctx.fillRect(p.x - p.size / 2, p.y - p.size / 2, p.size, p.size);
    }
  }
  ctx.globalAlpha = 1;
}

// ---------- Start ----------
initMenus();
requestAnimationFrame(frame);
