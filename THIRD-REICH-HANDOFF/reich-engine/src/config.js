// ── reich-engine — Third Reich documentary assembler ─────────────────────────
// Archival clips + still images (Ken Burns) + animated map graphics, narrated,
// with documentary-grade transitions. Ported motion/crossfade patterns from
// forbidden-engine, tuned calmer (monotonic pan/zoom instead of oscillating —
// documentary Ken Burns moves in one direction across a shot, it doesn't
// ping-pong like a floating character portrait).
export const FPS = 30;
export const WIDTH = 1920;
export const HEIGHT = 1080;

export const SANS = "'Inter', 'Segoe UI', Arial, sans-serif";

// ── Transition timings (frames) ──────────────────────────────────────────────
export const DUR = {
  xfade: 12, // crossfade — within a sequence/act
  dipToBlack: 20, // total frames (half out, half in) — between chapters/acts
};

// ── Still-image Ken Burns presets ────────────────────────────────────────────
// Monotonic across the whole scene duration (not a repeating cycle like the
// character-portrait engine): s0/s1 = scale endpoints, x0/x1 & y0/y1 = translate
// endpoints in % of the image layer. Kept subtle — max ~1.15x zoom — so archival
// stills read as documentary evidence, not a Ken-Burns cliché.
// Motion amplitudes were roughly halved (2026-07-20) — the narration re-time
// shortened many scenes, which made the previous 1.15 zoom / ±4% pan read as
// too fast. Kept subtle: max ~1.07x zoom, ±2% pan.
export const IMAGE_MOTIONS = {
  "slow-push": { s0: 1.0, s1: 1.07, x0: 0, x1: 0, y0: 0, y1: 0 },
  "slow-pull": { s0: 1.07, s1: 1.0, x0: 0, x1: 0, y0: 0, y1: 0 },
  "pan-left": { s0: 1.05, s1: 1.05, x0: 2, x1: -2, y0: 0, y1: 0 },
  "pan-right": { s0: 1.05, s1: 1.05, x0: -2, x1: 2, y0: 0, y1: 0 },
  settle: { s0: 1.06, s1: 1.0, x0: 0, x1: 0, y0: -1.5, y1: 1.5 },
};
export const DEFAULT_IMAGE_MOTION = "slow-push";

// Idle float — much smaller than the character engine's (this rides on top of
// the monotonic pan/zoom to keep even a "settle" shot from ever going glass-still).
export const FLOAT = { ampPct: 0.35, period: 220 };

// Returns { transform, opacity } for a still image at `frame` within a scene of
// `durationInFrames` length. Progress is linear 0..1 across the full scene
// (eased with a gentle ease-in-out) rather than a repeating cycle.
export function imageMotion(frame, motionName, durationInFrames) {
  const m = IMAGE_MOTIONS[motionName] || IMAGE_MOTIONS[DEFAULT_IMAGE_MOTION];
  const t = durationInFrames > 0 ? Math.min(1, Math.max(0, frame / durationInFrames)) : 0;
  // ease-in-out (smoothstep)
  const eased = t * t * (3 - 2 * t);

  const lerp = (a, b) => a + (b - a) * eased;
  const scale = lerp(m.s0, m.s1);
  const x = lerp(m.x0, m.x1);
  const yBase = lerp(m.y0, m.y1);
  const yFloat = Math.sin((frame / FLOAT.period) * Math.PI * 2) * FLOAT.ampPct;

  // No per-scene fade-in from opacity 0. With hard-cut transitions, that
  // 10-frame fade-in produces a visible dark flash at every scene start,
  // most obvious on callbacks (the same image appearing to briefly go dark
  // and come back), which is the effect the creative direction explicitly
  // rejected. Full opacity from frame 0.
  return {
    transform: `scale(${scale}) translate(${x}%, ${(yBase + yFloat).toFixed(3)}%)`,
    opacity: 1,
  };
}

// ── Clip (video) subtle zoom ──────────────────────────────────────────────────
// Keeps static/locked-off archival shots from feeling frozen: a barely-there
// zoom across the whole scene, independent of the source clip's own motion.
export const CLIP_ZOOM = { s0: 1.0, s1: 1.04 };
export function clipMotion(frame, durationInFrames) {
  const t = durationInFrames > 0 ? Math.min(1, Math.max(0, frame / durationInFrames)) : 0;
  const scale = CLIP_ZOOM.s0 + (CLIP_ZOOM.s1 - CLIP_ZOOM.s0) * t;
  return { transform: `scale(${scale})` };
}

// ── Duration ──────────────────────────────────────────────────────────────────
export function computeDuration(spec) {
  const scenesSec = (spec.scenes || []).reduce((a, s) => a + (s.durationSec || 6), 0);
  return Math.max(1, Math.round(scenesSec * FPS));
}

// ── active spec ────────────────────────────────────────────────────────────────
// The engine renders src/active-episode.json by default; the assembly stage
// overwrites this file per real render (same convention as forbidden-engine's
// active-story.json). Pass --props=<file>.json at render time to use a
// different spec without touching this file (e.g. for test renders).
import ACTIVE from "./active-episode.json";
export const DEFAULT_SPEC = ACTIVE;
