#/bin/bash/
indir=~/proj/aoc/input/

RED='\033[0;31m'
GREEN='\033[0;32m'
NONE='\033[0m'

declare -A extcmds
extcmds["py"]="python"
extcmds["clj"]="clj -M"
extcmds["js"]="node"
extcmds["mjs"]="node"

for file in $@; do
  # todo need to make this more dynamicer
  ext="${file##*.}"
  name=$(basename -s ."$ext" $file)
  cmd=${extcmds[$ext]}
  start=$(date +%s.%N)
  diff=$(cat "$indir$name".in | $cmd "$file" | diff "$indir$name".out -)
  time=$(echo "($(date +%s.%N) - $start)*1000" | bc) 

  if [ "$diff" ]; then
    printf "${name}.${ext}\t%.2fms\t${RED}failure${NONE}\n" $time
  else
    printf "${name}.${ext}\t%.2fms\t${GREEN}success${NONE}\n" $time
  fi
done
