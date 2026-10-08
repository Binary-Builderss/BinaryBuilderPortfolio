// Hero motion: a drifting field of bits on canvas, and the headline decoding from bits to letters.
// Under prefers-reduced-motion the field is drawn once and the headline is shown as is.

const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
const hero = document.querySelector(".hero");
const canvas = hero.querySelector(".hero-canvas");
const ctx = canvas.getContext("2d");

const CELL = 18;      // px between bits
const RADIUS = 140;   // px of cursor influence
let cols = 0, rows = 0, bits, colors, raf = 0, last = 0, visible = true;
const pointer = { x: -1e4, y: -1e4 };

function readColors() {
  const s = getComputedStyle(document.documentElement);
  colors = { ink: s.getPropertyValue("--muted").trim(), accent: s.getPropertyValue("--accent").trim() };
}

// Three overlapping sine waves: smooth enough to look like weather, no noise library needed.
const field = (x, y, t) =>
  (Math.sin(x * 0.11 + t) + Math.sin(y * 0.17 - t * 0.8) + Math.sin((x + y) * 0.07 + t * 0.5)) / 3;

function draw(time) {
  const t = time / 2400;
  ctx.clearRect(0, 0, cols * CELL, rows * CELL);
  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols; c++) {
      const v = field(c, r, t);
      const x = c * CELL + CELL / 2, y = r * CELL + CELL / 2;
      const d = Math.hypot(x - pointer.x, y - pointer.y);
      const near = d < RADIUS;
      if (v < 0.2 && !near) continue;
      const i = r * cols + c;
      if (Math.random() < (near ? 0.08 : 0.003)) bits[i] ^= 1;
      ctx.globalAlpha = near ? 0.9 - (d / RADIUS) * 0.6 : (v - 0.2) * 0.45;
      ctx.fillStyle = near ? colors.accent : colors.ink;
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
  ctx.font = '500 12px "Geist Mono", monospace';
  ctx.textAlign = "center";
  ctx.textBaseline = "middle";
  cols = Math.ceil(width / CELL);
  rows = Math.ceil(height / CELL);
  bits = Uint8Array.from({ length: cols * rows }, () => (Math.random() < 0.5 ? 1 : 0));
  draw(last);
}

function loop(now) {
  if (now - last > 40) { last = now; draw(now); } // ~25fps is plenty for a slow drift
  raf = visible ? requestAnimationFrame(loop) : 0;
}
const start = () => { if (!raf && !reduce) raf = requestAnimationFrame(loop); };

hero.addEventListener("pointermove", (e) => {
  const b = canvas.getBoundingClientRect();
  pointer.x = e.clientX - b.left;
  pointer.y = e.clientY - b.top;
}, { passive: true });
hero.addEventListener("pointerleave", () => { pointer.x = pointer.y = -1e4; });
matchMedia("(prefers-color-scheme: dark)").addEventListener("change", () => { readColors(); draw(last); });
new IntersectionObserver(([e]) => { visible = e.isIntersecting; if (visible) start(); }).observe(canvas);

// Headline: wrap each letter, show a random bit over it, resolve left to right.
const h1 = hero.querySelector(".decode");
if (!reduce) {
  const chars = [];
  h1.innerHTML = h1.textContent
    .split(" ")
    .map((word) => `<span class="w">${[...word].map((ch) => `<span class="ch">${ch}</span>`).join("")}</span>`)
    .join(" ");
  h1.querySelectorAll(".ch").forEach((el) => chars.push(el));
  const flip = () => chars.forEach((el) => { if (el.dataset.g) el.dataset.g = Math.random() < 0.5 ? "0" : "1"; });
  chars.forEach((el) => (el.dataset.g = "0"));
  flip();
  let done = 0;
  const timer = setInterval(() => {
    flip();
    if (done < chars.length) delete chars[done++].dataset.g;
    else clearInterval(timer);
  }, 45);
}

readColors();
await document.fonts.ready;
new ResizeObserver(resize).observe(canvas);
start();
