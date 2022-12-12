package main

import (
  "agoc/util"
  "strings"
  "strconv"
)

type Op struct {
  name string
  value int
}

func ParseOp(s string) Op {
  parts := strings.Split(s, " ")
  name := parts[0]
  value := 0
  if len(parts) > 1 {
    v, _ := strconv.ParseInt(parts[1], 10, 0)
    value = int(v)
  }
  return Op{name, value}
}

func ParseArgs(a []string) (out []Op) {
  for _, v := range a {
    out = append(out, ParseOp(v))
  }
  return
}

func do(o Op, x int) []int {
  switch o.name {
    case "noop":
      return []int{x}
    case "addx":
      return []int{x, x + o.value}
  }
  return []int{}
}
func run(ops []Op) (out []int) {
  x := 1
  out = append(out, x)
  for _, o := range ops {
    out = append(out, do(o, x)...)
    x = out[len(out) - 1]
  }
  return
}

func main() {
  program := ParseArgs(util.ArgLines())
  cycles := run(program)

  one := 20 * cycles[19] +
    60 * cycles[59] +
    100 * cycles[99] +
    140 * cycles[139] +
    180 * cycles[179] +
    220 * cycles[219]

  println(one)
}
