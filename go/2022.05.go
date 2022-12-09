package main

import (
  "agoc/util"
  "agoc/ds"
  "strings"
)

func ParseCrates(s string) []ds.Stack {
  lines := util.Lines(s)
  lns := len(lines)
  cols := lines[lns - 1]
  numCols := cols[len(cols) - 2] - 48

  out := make([]ds.Stack, numCols)

  for i := 2; i <= lns; i++ {
    line := lines[lns - i]
    for c, v := range line {
      if v > 64 && v < 91 {
        cidx := (c + 3) / 4 - 1
        //out[cidx] = append(out[cidx], string(v))
        out[cidx].Push(string(v))
      }
    }
  }

  return out
}


func ParseInstruction(s string) []int {
  parts := strings.Split(s, " ")
  return util.Minty([]string{parts[1], parts[3], parts[5]})
}

// I want regex for this.
// regexp.Match(s, "\d+") eeeeezzzzzz
// could also split on spaces and take 1, 3, 5
func ParseInstructions(s string) (out [][]int) {
  for _, v := range util.Lines(s) {
    out = append(out, ParseInstruction(v))
  }
  return
}

func followInstruction(inst []int, s []ds.Stack) {
  for i := 0; i < inst[0]; i++ {
    s[inst[2] - 1].Push(s[inst[1] - 1].Pop())
  }
}

func createMover9001(inst []int, s []ds.Stack) {
  t := ds.Stack{}
  for i := 0; i < inst[0]; i++ {
    t.Push(s[inst[1] - 1].Pop())
  }
  for t.Size() > 0 {
    s[inst[2] - 1].Push(t.Pop())
  }
}

func tops(s []ds.Stack) (out []interface{}) {
  for _, v := range s {
    out = append(out, v.Peek())
  }
  return
}

func main() {
  inp := util.Args()
  parts := strings.Split(inp, "\n\n")
  crates := ParseCrates(parts[0]) // is this going to be annoying to parse?
  inst := ParseInstructions(parts[1])

  for _, v := range inst {
    followInstruction(v, crates)
  }

  for _, v := range tops(crates) {
    print(v.(string))
  }
  println()

  // this is bad and wrong but I'm lazy
  crates = ParseCrates(parts[0]) // is this going to be annoying to parse?

  for _, v := range inst {
    createMover9001(v, crates)
  }

  for _, v := range tops(crates) {
    print(v.(string))
  }
  println()
}
