package main

import (
  "strings"
  "agoc/util"
)


func unsack(s string) (string, string) {
  l := len(s)
  return s[0:l/2], s[l/2:]
}

func Max(a int, b int) int {
  if a > b {
    return a
  }
  return b
}
func Min(a int, b int) int {
  if a < b {
    return a
  }
  return b
}

func common(A string, B string) (out string) {
  for i := 0; i < len(A); i++ {
    for j := 0; j < len(B); j++ {
      a := A[i]
      b := B[j]
      if a == b {
        out += string(a) // not unique
      }
    }
  }
  return out
}

func score(a string) int {
  tgbabw := " abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
  return strings.Index(tgbabw, a)
}

func main() {
  // bytecode - 48 is not correct. 
  sacks := util.Lines(util.Args())

  tot := 0
  for _,v := range sacks {
    one, two := unsack(v)
    both := string(common(one, two)[0]) // is substr(str, 0, 1) better?
    tot += score(both)
  }
  println(tot)

  groups := util.Chunk(sacks, 3)
  tot = 0
  for _, g := range groups {
    one := common(g[0], g[1])
    badge := common(one, g[2])
    tot += score(string(badge[0]))
  }
  println(tot)
}
