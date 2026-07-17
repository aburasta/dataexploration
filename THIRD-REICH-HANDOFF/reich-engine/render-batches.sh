#!/bin/bash
# Batched render driver for ep003 love-life, to work around this machine's
# RAM-exhaustion death-spiral on long single-pass renders. Each batch gets its
# own fresh `remotion render` invocation (fresh browser process), then all
# batches are losslessly concatenated into the final single mp4.
set -e

cd "C:/Users/asamo/Claude Files/reich-engine"
BATCH_DIR="../Third Reich/renders/love-life-batches"
FINAL_OUT="../Third Reich/renders/ep003-hitler-love-life.mp4"
LOG_DIR="../Third Reich/episodes/ep003-hitler-love-life"
FFMPEG="node_modules/@remotion/compositor-win32-x64-msvc/ffmpeg.exe"

# start,end (inclusive) frame ranges — 7 batches covering 0..17418
BATCHES=(
  "0-2499"
  "2500-4999"
  "5000-7499"
  "7500-9999"
  "10000-12499"
  "12500-14999"
  "15000-17418"
)

mkdir -p "$BATCH_DIR"

for i in "${!BATCHES[@]}"; do
  RANGE="${BATCHES[$i]}"
  OUT="$BATCH_DIR/batch-$(printf '%02d' "$i").mp4"
  LOG="$LOG_DIR/render-batch-$(printf '%02d' "$i").log"

  if [ -f "$OUT" ]; then
    echo "BATCH $i ($RANGE) already exists, skipping"
    continue
  fi

  echo "=== BATCH $i: frames $RANGE -> $OUT ==="

  # pre-clean: kill any lingering render processes + webpack cache, so every
  # batch starts from a truly clean state regardless of prior batch outcome
  powershell -NoProfile -Command "Get-Process -Name 'chrome-headless-shell','node' -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue" >/dev/null 2>&1 || true
  rm -rf node_modules/.cache/webpack
  rm -rf out/*

  npx remotion render src/index.jsx Documentary "$OUT" --frames="$RANGE" --concurrency=1 > "$LOG" 2>&1

  if [ ! -f "$OUT" ]; then
    echo "BATCH $i FAILED - no output file produced, see $LOG"
    exit 1
  fi
  echo "BATCH $i done: $(du -h "$OUT" | cut -f1)"
done

echo "=== All batches rendered. Concatenating... ==="
CONCAT_LIST="$BATCH_DIR/concat-list.txt"
> "$CONCAT_LIST"
for i in "${!BATCHES[@]}"; do
  OUT="$BATCH_DIR/batch-$(printf '%02d' "$i").mp4"
  ABS=$(cd "$(dirname "$OUT")" && pwd)/$(basename "$OUT")
  echo "file '$ABS'" >> "$CONCAT_LIST"
done

"$FFMPEG" -y -f concat -safe 0 -i "$CONCAT_LIST" -c copy "$FINAL_OUT"

echo "=== CONCAT DONE ==="
ls -la "$FINAL_OUT"
echo "BATCHED_RENDER_SUCCESS"
