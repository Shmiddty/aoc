package main

import (
  "strings"
  "agoc/util"
)


func ParseRange(s string) (min int, max int) {
  parts := util.Minty(strings.Split(s, "-"))
  min = parts[0]
  max = parts[1]
  return
}
func ParseLine(s string) (a0 int, a1 int, b0 int, b1 int) {
  parts := strings.Split(s, ",")
  a0, a1 = ParseRange(parts[0])
  b0, b1 = ParseRange(parts[1])
  return
}

func FullyContains(a0 int, a1 int, b0 int, b1 int) bool {
  return (a0 >= b0 && a1 <= b1) || (b0 >= a0 && b1 <= a1)
}

func main() {
  pairs := util.ArgLines()

  cnt := 0
  for _, v := range pairs {
    cnt += util.Bint(FullyContains(ParseLine(v)))
  }
  println(cnt)
}
