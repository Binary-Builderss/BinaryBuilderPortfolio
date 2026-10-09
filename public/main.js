// Page motion: a drifting field of bits on canvas and the headline decoding from bits to letters.
// Under prefers-reduced-motion the field is drawn once and the headline is shown as is.

const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;

// Headline: wrap each letter, show a random bit over it, resolve left to right, repeat every 30s.
// Between runs the h1 goes back to plain text, so screen readers never meet the per-letter spans for long.
const h1 = document.querySelector(".decode");
const headline = h1.textContent;
function decode() {
  h1.innerHTML = headline
    .split(" ")
    .map((word) => `<span class="w">${[...word].map((ch) => `<span class="ch">${ch}</span>`).join("")}</span>`)
    .join(" ");
  const chars = [...h1.querySelectorAll(".ch")];
  const flip = () => chars.forEach((el) => { if (el.dataset.g) el.dataset.g = Math.random() < 0.5 ? "0" : "1"; });
  chars.forEach((el) => (el.dataset.g = "0"));
  flip();
  let done = 0;
  const timer = setInterval(() => {
    flip();
    if (done < chars.length) delete chars[done++].dataset.g;
    else { clearInterval(timer); h1.textContent = headline; }
  }, 45);
}
if (!reduce) { decode(); setInterval(decode, 30000); }

// Bit field
const canvas = document.querySelector(".bits");
const ctx = canvas.getContext("2d");
const CELL = 18;      // px between bits
let radius = 140;     // px of highlight, smaller on narrow screens
let cols = 0, rows = 0, w = 0, h = 0, bits, colors, last = 0;
const pointer = { x: -1e4, y: -1e4 };
// No hover on touch screens: the highlight wanders on its own instead. A real mouse takes over.
let wander = matchMedia("(hover: none)").matches;

function readColors() {
  const s = getComputedStyle(document.documentElement);
  colors = { ink: s.getPropertyValue("--muted").trim(), accent: s.getPropertyValue("--accent").trim() };
}

// Three overlapping sine waves: smooth enough to look like weather, no noise library needed.
const field = (x, y, t) =>
  (Math.sin(x * 0.11 + t) + Math.sin(y * 0.17 - t * 0.8) + Math.sin((x + y) * 0.07 + t * 0.5)) / 3;

function draw(time) {
  const t = time / 2400;
  if (wander) {
    // Lissajous path: smooth, never repeats quickly, stays inside the screen.
    pointer.x = w * (0.5 + 0.4 * Math.sin(t * 1.3));
    pointer.y = h * (0.5 + 0.4 * Math.sin(t * 0.9 + 1));
  }
  ctx.clearRect(0, 0, w, h);
  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols; c++) {
      const v = field(c, r, t);
      const x = c * CELL + CELL / 2, y = r * CELL + CELL / 2;
      const d = Math.hypot(x - pointer.x, y - pointer.y);
      const near = d < radius;
      // Ambient bits fade out toward the footer; the highlight shows everywhere.
      const fade = Math.min(1, Math.max(0, (0.85 * h - y) / (0.55 * h)));
      if (!near && (v < 0.2 || fade === 0)) continue;
      const i = r * cols + c;
      if (Math.random() < (near ? 0.08 : 0.003)) bits[i] ^= 1;
      ctx.globalAlpha = near ? 0.9 - (d / radius) * 0.6 : (v - 0.2) * 0.45 * fade;
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
  if (now - last > 40) { last = now; draw(now); } // ~25fps is plenty for a slow drift; rAF pauses in hidden tabs
  requestAnimationFrame(loop);
}

addEventListener("pointermove", (e) => {
  if (e.pointerType !== "mouse") return;
  wander = false;
  pointer.x = e.clientX;
  pointer.y = e.clientY;
}, { passive: true });
document.documentElement.addEventListener("pointerleave", () => { pointer.x = pointer.y = -1e4; });
matchMedia("(prefers-color-scheme: dark)").addEventListener("change", () => { readColors(); draw(last); });

readColors();
await document.fonts.ready;
new ResizeObserver(resize).observe(canvas);
if (!reduce) requestAnimationFrame(loop);
