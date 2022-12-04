package main

import (
  "agoc/util"
)

func prep(inp string) [][]int {
  elves := util.Blocks(inp)
  var out [][]int
  for _, elf := range elves {
    out = append(out, util.Minty(util.Lines(elf)))
  }
  return out
}

func Minted(elves [][]int) []int {
  var out []int
  for _, elf := range elves {
    out = append(out, util.Sum(&elf))
  }
  return out
}

func main() {
  elves := prep(util.Args())
  dinner := Minted(elves)
  cals, _ := util.Max(dinner...)
  println(cals)
}
