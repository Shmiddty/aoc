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

func main() {
  rounds := util.Lines(util.Args())
  tot := 0

  for i, v := range rounds {
    if i == len(rounds) - 1 {
      break
    }
    parts := strings.Split(v, " ")
    elf := strings.Index("ABC", parts[0])
    you := strings.Index("XYZ", parts[1])
    result := Play(elf, you)
    tot += result * 3 + 3 + you + 1
  }
  println(tot)
}
