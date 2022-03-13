#/bin/bash/
indir="../input/" # this could be... better.

RED='\033[0;31m'
GREEN='\033[0;32m'
NONE='\033[0m'

pad="           "
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

  cwd=$PWD
  cd "${file%/*}" # we want to execute in the directory of the file 

  start=$(date +%s.%N)
  diff=$(cat "$indir$name".in | $cmd "$fname" | diff "$indir$name".out -)
  time=$(echo "($(date +%s.%N) - $start)*1000" | bc) 
  time=$(printf "%.2fms" $time)
  result=$pass

  cd $cwd # gotta go back... to the future?

  if [ "$diff" ]; then
    result=$fail
  fi
 
  # TODO: the padding for time is incorrect because it is calculated based on the unformatted time 
  printf "%b %s %s%s\n" $result $fname "${pad:${#time}}" $time
done
