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

func Play(A int, B int) int {
  return util.Bint((A + 1)%3 == B) * -1 + util.Bint(A == (B + 1)%3)
}

func Parse (s string) (int, int) {
  parts := strings.Split(s, " ")
  elf := strings.Index("ABC", parts[0])
  you := strings.Index("XYZ", parts[1])
  return elf, you
}

func Play2(A int, B int) int {
  return (A + util.Bint(B == 0) * 2 + util.Bint(B == 2)) % 3
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

  tot = 0
  for _, v := range rounds {
    elf, result := Parse(v)
    you := Play2(elf, result)
    tot += (result - 1) * 3 + 3 + you + 1
  }
  println(tot)
}
