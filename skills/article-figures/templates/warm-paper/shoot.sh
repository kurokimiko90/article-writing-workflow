#!/bin/bash
# frames.html の #fN を 1 枚ずつ截圖（cover 1280x670、他 1200x675、@2x）
cd "$(dirname "$0")"
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
names=(00-cover 01-rules-api 02-constraints 03-role 04-method 05-design 06-result 07-closing)
ids=("$@"); [ ${#ids[@]} -eq 0 ] && ids=(0 1 2 3 4 5 6 7)
for i in "${ids[@]}"; do
  size="1200,675"; [ "$i" = 0 ] && size="1280,670"
  for try in 1 2; do
    perl -e 'alarm 60; exec @ARGV' "$CHROME" --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=2 \
      --window-size="$size" --virtual-time-budget=10000 --screenshot="${names[$i]}.png" "file://$PWD/frames.html#f$i" >/dev/null 2>&1 && break
    echo "retry f$i"
  done
done
ls *.png
