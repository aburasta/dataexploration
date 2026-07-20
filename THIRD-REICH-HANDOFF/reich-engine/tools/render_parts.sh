#!/usr/bin/env bash
# Render the film in 4 ~8-minute PARTS (resilient: skips finished parts, so a
# container reclaim only costs the in-progress part). Each finished part is a
# deliverable; the full film is the 4 parts concatenated losslessly.
set -u
cd /home/user/dataexploration/THIRD-REICH-HANDOFF/reich-engine
BR=/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell
OUTD=out/parts_render
mkdir -p "$OUTD"
TOTAL=57493
PART=14400   # 8:00 at 30fps
i=0; start=0
while [ "$start" -lt "$TOTAL" ]; do
  end=$(( start + PART - 1 )); [ "$end" -ge "$TOTAL" ] && end=$(( TOTAL - 1 ))
  out="$OUTD/part_0$i.mp4"
  if [ -f "$out" ] && [ "$(stat -c%s "$out")" -gt 100000 ]; then
    echo "SKIP part $i ($start-$end) done"
  else
    echo "RENDER part $i frames $start-$end"
    npx remotion render src/index.jsx Documentary "$out" \
      --frames="$start-$end" --concurrency=4 --browser-executable="$BR" 2>&1 \
      | grep -oE "Rendered [0-9]+/[0-9]+|Encoded [0-9]+/[0-9]+|Error.*" | tail -1
    [ -f "$out" ] || { echo "PART $i FAILED"; exit 1; }
    echo "PART $i DONE"
  fi
  i=$(( i + 1 )); start=$(( end + 1 ))
done
echo "ALL PARTS DONE"
