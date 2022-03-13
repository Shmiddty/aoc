#/bin/bash/
indir=~/proj/aoc/input/

RED='\033[0;31m'
GREEN='\033[0;32m'
NONE='\033[0m'

pad="             "
pass="${GREEN}success${NONE}"
fail="${RED}failure${NONE}"

declare -A extcmds
extcmds["py"]="python"
extcmds["clj"]="clj -M"
extcmds["js"]="node"
extcmds["mjs"]="node"

for file in $@; do
  # todo need to make this more dynamicer
  ext="${file##*.}"
  name=$(basename -s ."$ext" $file)
  fname="${name}.${ext}"
  cmd=${extcmds[$ext]}
  start=$(date +%s.%N)
  diff=$(cat "$indir$name".in | $cmd "$file" | diff "$indir$name".out -)
  time=$(echo "($(date +%s.%N) - $start)*1000" | bc) 
  result=$pass

  if [ "$diff" ]; then
    result=$fail
  fi
  
  printf "%s\t%s%.2fms %b\n" $fname "${pad:${#time}}" $time $result
done
