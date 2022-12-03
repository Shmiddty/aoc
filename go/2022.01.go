package main

import (
  "agoc/util"
)

func prep(inp string) [][]int {
  elves := util.Blocks(inp)
  var out [][]int = make([][]int, len(elves))
  for e := 0; e < len(elves); e++ {
    food := util.Lines(elves[e])
    out[e] = util.Minty(food)
  }
  return out
}

func Minted(elves [][]int) []int {
  var out []int = make([]int, len(elves))
  for i := 0; i < len(elves); i++ {
    out[i] = util.Sum(&elves[i])
  }
  return out
}

func main() {
  elves := prep(util.Args())
  dinner := Minted(elves)
  cals, _ := util.Max(dinner...)
  println(cals)
}
