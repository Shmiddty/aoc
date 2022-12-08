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

func Intersects(a0 int, a1 int, b0 int, b1 int) bool {
  return (b0 >= a0 && b0 <= a1) || (a0 >= b0 && a0 <= b1)
}

func main() {
  pairs := util.ArgLines()

  cnt1 := 0
  cnt2 := 0
  for _, v := range pairs {
    a0, a1, b0, b1 := ParseLine(v)
    cnt1 += util.Bint(FullyContains(a0, a1, b0, b1))
    cnt2 += util.Bint(Intersects(a0, a1, b0, b1))
  }
  println(cnt1)
  println(cnt2)
}
