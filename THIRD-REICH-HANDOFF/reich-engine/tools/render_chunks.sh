#!/usr/bin/env bash
# Resilient chunked render: renders the full composition in frame-range chunks,
# skipping any chunk already on disk, then concatenates. Survives container
# reclaim — completed chunks persist and only the missing ones re-render.
set -u
cd /home/user/dataexploration/THIRD-REICH-HANDOFF/reich-engine
BR=/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell
OUTD=out/chunks
mkdir -p "$OUTD"
TOTAL=57493
CHUNK=9582
i=0
start=0
while [ "$start" -lt "$TOTAL" ]; do
  end=$(( start + CHUNK - 1 ))
  [ "$end" -ge "$TOTAL" ] && end=$(( TOTAL - 1 ))
  out="$OUTD/chunk_$(printf '%02d' "$i").mp4"
  if [ -f "$out" ] && [ "$(stat -c%s "$out")" -gt 100000 ]; then
    echo "SKIP chunk $i ($start-$end) already done"
  else
    echo "RENDER chunk $i frames $start-$end -> $out"
    npx remotion render src/index.jsx Documentary "$out" \
      --frames="$start-$end" --concurrency=4 --browser-executable="$BR" 2>&1 \
      | grep -oE "Rendered [0-9]+/[0-9]+|Encoded [0-9]+/[0-9]+|Error.*" | tail -1
    if [ ! -f "$out" ]; then echo "CHUNK $i FAILED"; exit 1; fi
    echo "CHUNK $i DONE"
  fi
  i=$(( i + 1 ))
  start=$(( end + 1 ))
done
echo "ALL CHUNKS DONE — concatenating"
: > "$OUTD/list.txt"
for f in "$OUTD"/chunk_*.mp4; do echo "file '$(basename "$f")'" >> "$OUTD/list.txt"; done
FFMPEG=$(python3 -c "import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())")
(cd "$OUTD" && "$FFMPEG" -loglevel error -y -f concat -safe 0 -i list.txt -c copy ../legal-coup-FULL.mp4)
echo "CONCAT DONE -> out/legal-coup-FULL.mp4"
ls -la out/legal-coup-FULL.mp4
