// Page motion: a drifting field of bits on canvas, headlines decoding from bits to letters, a terminal caret cursor.
// Home: full-screen field, headline replays every 30s. Content pages: a band of field behind the header, title decodes once.
// Under prefers-reduced-motion the field is drawn once and nothing else moves.

const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
const home = !!document.querySelector(".hero");

// Headline: wrap each letter, show a random bit over it, resolve left to right.
// Afterwards the h1 goes back to plain text, so screen readers never meet the per-letter spans for long.
const h1 = document.querySelector(".decode");
const headline = h1.textContent;
const esc = (ch) => (ch === "&" ? "&amp;" : ch === "<" ? "&lt;" : ch);
function decode() {
  h1.innerHTML = headline
    .split(" ")
    .map((word) => `<span class="w">${[...word].map((ch) => `<span class="ch">${esc(ch)}</span>`).join("")}</span>`)
    .join(" ");
  const chars = [...h1.querySelectorAll(".ch")];
  const flip = () => chars.forEach((el) => { if (el.dataset.g) el.dataset.g = Math.random() < 0.5 ? "0" : "1"; });
  chars.forEach((el) => (el.dataset.g = "0"));
  flip();
  let done = 0;
  // Long titles resolve in about the same time as the short home headline.
  const step = home ? 45 : Math.max(12, Math.round(900 / chars.length));
  const timer = setInterval(() => {
    flip();
    if (done < chars.length) delete chars[done++].dataset.g;
    else { clearInterval(timer); h1.textContent = headline; }
  }, step);
}
if (!reduce) { decode(); if (home) setInterval(decode, 30000); }

// Caret cursor: a block that follows the mouse and blinks when it rests, like a terminal.
// Only for a real mouse; over links and buttons it hides and the native hand takes over.
if (!reduce && matchMedia("(pointer: fine)").matches) {
  const caret = document.createElement("div");
  caret.className = "caret over"; // hidden until the mouse first moves
  caret.setAttribute("aria-hidden", "true");
  document.body.append(caret);
  document.documentElement.classList.add("has-caret");
  let rest;
  addEventListener("pointermove", (e) => {
    if (e.pointerType !== "mouse") return;
    caret.style.transform = `translate(${e.clientX}px, ${e.clientY}px)`;
    caret.classList.toggle("over", !!e.target.closest?.("a, button"));
    caret.classList.remove("rest");
    clearTimeout(rest);
    rest = setTimeout(() => caret.classList.add("rest"), 600);
  }, { passive: true });
  document.documentElement.addEventListener("pointerleave", () => caret.classList.add("over"));
}

// Bit field
const canvas = document.querySelector(".bits");
const ctx = canvas.getContext("2d");
const CELL = 18;      // px between bits
let radius = 140;     // px of highlight, smaller on narrow screens
let cols = 0, rows = 0, w = 0, h = 0, bits, colors, last = 0, visible = true;
// Two highlights: one always wandering on its own (so touch screens get one too), one following the mouse.
// Pointer is kept in viewport coordinates and mapped onto the canvas each frame (the content-page band scrolls).
const pointer = { x: -1e4, y: -1e4 };
const wander = { x: -1e4, y: -1e4 };
// Clicks and taps send a ring through the field.
const waves = [];
const WAVE_SPEED = 900, WAVE_LIFE = 1.1, WAVE_BAND = 28; // px/s, s, px

function readColors() {
  const s = getComputedStyle(document.documentElement);
  colors = { ink: s.getPropertyValue("--muted").trim() };
}

// Three overlapping sine waves: smooth enough to look like weather, no noise library needed.
const field = (x, y, t) =>
  (Math.sin(x * 0.11 + t) + Math.sin(y * 0.17 - t * 0.8) + Math.sin((x + y) * 0.07 + t * 0.5)) / 3;

function draw(time) {
  const t = time / 1000;
  const box = canvas.getBoundingClientRect();
  const px = pointer.x - box.left, py = pointer.y - box.top;
  // Lissajous path: smooth, never repeats quickly, stays inside the canvas.
  wander.x = w * (0.5 + 0.4 * Math.sin(t * 1.35));
  wander.y = h * (0.5 + 0.4 * Math.sin(t * 0.95 + 1));
  for (let i = waves.length - 1; i >= 0; i--) {
    const age = (time - waves[i].t0) / 1000;
    if (age > WAVE_LIFE) { waves.splice(i, 1); continue; }
    waves[i].r = age * WAVE_SPEED;
    waves[i].a = 1 - age / WAVE_LIFE;
  }
  ctx.clearRect(0, 0, w, h);
  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols; c++) {
      const v = field(c, r, t * 1.3);
      const x = c * CELL + CELL / 2, y = r * CELL + CELL / 2;
      const d = Math.min(Math.hypot(x - wander.x, y - wander.y), Math.hypot(x - px, y - py));
      const near = d < radius;
      let ring = 0;
      for (const wv of waves) {
        const k = Math.abs(Math.hypot(x - wv.x + box.left, y - wv.y + box.top) - wv.r);
        if (k < WAVE_BAND) ring = Math.max(ring, wv.a * (1 - k / WAVE_BAND));
      }
      // Ambient bits fade out toward the bottom; highlights and rings show everywhere.
      const fade = Math.min(1, Math.max(0, (0.85 * h - y) / (0.55 * h)));
      if (!near && !ring && (v < 0.2 || fade === 0)) continue;
      const i = r * cols + c;
      if (Math.random() < (ring ? 0.5 : near ? 0.15 : 0.01)) bits[i] ^= 1;
      const base = near ? 0.9 - (d / radius) * 0.6 : Math.max(0, (v - 0.2) * 0.45 * fade);
      ctx.globalAlpha = Math.max(base, ring * 0.9);
      ctx.fillStyle = colors.ink; // all grey: highlights only differ in opacity
      ctx.fillText(bits[i] ? "1" : "0", x, y);
    }
  }
}

function resize() {
  const dpr = Math.min(devicePixelRatio || 1, 2);
  const { width, height } = canvas.getBoundingClientRect();
  canvas.width = Math.round(width * dpr);
  canvas.height = Math.round(height * dpr);
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  ctx.font = '500 12px "JetBrains Mono", monospace';
  ctx.textAlign = "center";
  ctx.textBaseline = "middle";
  w = width; h = height;
  radius = Math.min(140, width * 0.3);
  cols = Math.ceil(width / CELL);
  rows = Math.ceil(height / CELL);
  bits = Uint8Array.from({ length: cols * rows }, () => (Math.random() < 0.5 ? 1 : 0));
  draw(last);
}

function loop(now) {
  // ~30fps is plenty for a drift; rAF pauses in hidden tabs, and the band stops once scrolled away.
  if (visible && now - last > 33) { last = now; draw(now); }
  requestAnimationFrame(loop);
}

addEventListener("pointermove", (e) => {
  if (e.pointerType !== "mouse") return;
  pointer.x = e.clientX;
  pointer.y = e.clientY;
}, { passive: true });
addEventListener("pointerdown", (e) => {
  if (waves.length > 3) waves.shift();
  waves.push({ x: e.clientX, y: e.clientY, t0: performance.now(), r: 0, a: 1 });
}, { passive: true });
document.documentElement.addEventListener("pointerleave", () => { pointer.x = pointer.y = -1e4; });
matchMedia("(prefers-color-scheme: dark)").addEventListener("change", () => { readColors(); draw(last); });

readColors();
await document.fonts.ready;
new ResizeObserver(resize).observe(canvas);
new IntersectionObserver(([e]) => (visible = e.isIntersecting)).observe(canvas);
if (!reduce) requestAnimationFrame(loop);
