// Centerline pen strokes for the word "Prince" in a casual (printed) hand.
// Coordinates are in a local "writing" space (baseline 620, x-top 520, cap-top
// 380); PrinceInk.tsx scales + centres this space on the 1920x1080 frame.
// Each entry is ONE pen-down motion; the renderer lifts the pen between them.

export type Stroke = { id: string; d: string };

export const STROKES: Stroke[] = [
  { id: "P-stem", d: "M700,384 C698,470 696,548 694,620" },
  { id: "P-bowl", d: "M700,390 C755,380 790,402 788,450 C786,492 748,500 698,498" },
  { id: "r", d: "M832,620 C834,585 834,552 834,520 C838,504 856,500 872,512" },
  { id: "i", d: "M918,520 C919,560 920,590 920,620" },
  { id: "n", d: "M958,620 C957,575 958,545 958,522 C962,504 1004,498 1030,520 C1032,548 1032,585 1032,620" },
  { id: "c", d: "M1128,536 C1104,516 1068,522 1064,568 C1061,606 1096,620 1126,606" },
  { id: "e", d: "M1150,572 C1176,566 1204,566 1210,568 C1224,572 1220,538 1196,528 C1170,518 1146,536 1148,566 C1150,596 1176,614 1204,602" },
];

// First point of each stroke (fallback nib pos before path measurement).
export const STROKE_STARTS = [
  { x: 700, y: 384 },
  { x: 700, y: 390 },
  { x: 832, y: 620 },
  { x: 918, y: 520 },
  { x: 958, y: 620 },
  { x: 1128, y: 536 },
  { x: 1150, y: 572 },
];

// Dot on the "i" (final tap), above the i stem.
export const I_DOT = { x: 920, y: 486 };

// Local bounding-box centre of the word (for centring on the frame).
export const WORD_CENTER = { x: 958, y: 500 };
