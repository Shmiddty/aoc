package main

import (
  "strings"
  "agoc/util"
)

// no built in map or reduce? icky
// can I even pass functions as arguments in this language?

//func Map(i []T, f func(T) T) []T {
//  out := make([]T, len(i))
//  for k, v := range i {
//    out[k] = f(i[k])
//  }
//  return out
//}

func bint (b bool) int {
  if b {
    return 1
  }
  return 0
}

func Play(A int, B int) int {
  return bint((A + 1)%3 == B) * -1 + bint(A == (B + 1)%3)
}

func Parse (s string) (int, int) {
  parts := strings.Split(s, " ")
  elf := strings.Index("ABC", parts[0])
  you := strings.Index("XYZ", parts[1])
  return elf, you
}

func main() {
  rounds := util.Lines(util.Args())
  tot := 0

  for _, v := range rounds {
    elf, you := Parse(v)
    result := Play(you, elf)
    tot += result * 3 + 3 + you + 1
  }
  println(tot)
}
