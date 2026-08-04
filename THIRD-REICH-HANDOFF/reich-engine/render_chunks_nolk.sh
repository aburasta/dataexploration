#!/bin/bash
set -u
CHROME=/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell
PROPS=/home/user/dataexploration/THIRD-REICH-HANDOFF/episodes/special-night-of-long-knives-1934/props-nolk.json
FF=/home/user/dataexploration/THIRD-REICH-HANDOFF/reich-engine/node_modules/@remotion/compositor-linux-x64-gnu/ffmpeg
PARTS=/home/user/dataexploration/THIRD-REICH-HANDOFF/episodes/special-night-of-long-knives-1934/_parts
OUT=/home/user/dataexploration/THIRD-REICH-HANDOFF/episodes/special-night-of-long-knives-1934/night-of-long-knives-1934-SILENT.mp4
mkdir -p "$PARTS"; rm -f "$PARTS"/*.mp4 "$PARTS"/list.txt
TOTAL=36620; CHUNK=4000; i=0
echo "CHUNKED RENDER START $(date)"
for START in $(seq 0 $CHUNK $((TOTAL-1))); do
  END=$((START+CHUNK-1)); [ $END -gt $((TOTAL-1)) ] && END=$((TOTAL-1))
  PART=$(printf "%s/part_%03d.mp4" "$PARTS" "$i")
  ok=0
  for attempt in 1 2 3; do
    echo ">>> chunk $i frames $START-$END attempt $attempt $(date +%H:%M:%S)"
    timeout 900 npx remotion render src/index.jsx Documentary "$PART" \
      --props="$PROPS" --frames=$START-$END --concurrency=4 \
      --browser-executable="$CHROME" --log=info >/tmp/chunk_$i.log 2>&1
    rc=$?
    tail -1 /tmp/chunk_$i.log | tr '\r' '\n' | tail -1
    if [ -f "$PART" ] && [ "$(stat -c %s "$PART")" -gt 10000 ]; then ok=1; echo "chunk $i OK rc=$rc"; break; fi
    echo "!!! chunk $i attempt $attempt failed/timeout rc=$rc, killing chrome + retry"
    pkill -9 -f headless_shell 2>/dev/null; rm -rf /tmp/react-motion-render* 2>/dev/null; sleep 4
  done
  [ $ok -ne 1 ] && { echo "FATAL: chunk $i failed 3x"; exit 1; }
  echo "file '$PART'" >> "$PARTS/list.txt"
  i=$((i+1))
done
echo "=== concatenating $i parts ==="
"$FF" -y -f concat -safe 0 -i "$PARTS/list.txt" -c copy "$OUT" 2>&1 | tail -1
echo "CHUNKS DONE $(date)"; ls -la "$OUT"
"$FF" -v error -show_entries format=duration -of csv=p=0 "$OUT" | awk '{printf "duration %.0fs (%.1f min)\n",$1,$1/60}'
