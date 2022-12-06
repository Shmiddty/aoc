package main

import (
  "strings"
  "agoc/util"
)


func unsack(s string) (string, string) {
  l := len(s)
  return s[0:l/2], s[l/2:]
}

func common(A string, B string) string {
  for _, a := range A {
    for _, b := range B {
      if a == b {
        return string(a)
      }
    }
  }
  return ""
}

func main() {
  tgbabw := " abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
  sacks := util.Lines(util.Args())

  tot := 0
  for _,v := range sacks {
    one, two := unsack(v)
    both := common(one, two)
    tot += strings.Index(tgbabw, both)
  }
  println(tot)
}
