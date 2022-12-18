package main

import (
  "agoc/util"
  "strings"
  "strconv"
  "sort"
)

func add(a int) func(int)int {
  return func(b int) int {
    return a + b
  }
}

func mul(a int) func(int)int {
  return func(b int) int {
    return a * b
  }
}

func div(a int) func(int)int {
  return func(b int) int {
    return b / a
  }
}

func mod(a int) func(int)int {
  return func(b int) int {
    return b % a
  }
}

func pow(a int) func(int)int {
  return func(b int) int {
    out := b
    for i := 0; i < a - 1; i++ {
      out *= b
    }
    return out
  }
}

func noop(a int) func(int)int {
  return func(b int) int {
    return b
  }
}

func makeTest(f func(int)int, t func(int)bool) func(int)bool {
  return func(a int) bool {
    return t(f(a))
  }
}

func compose(a func(int) int) func(func(int)int) func(int)int {
  return func(b func(int) int)  func(int)int{
    return func(c int) int {
      return a(b(c))
    }
  }
}

// TODO: function that gets all numbers from a string (already exists in some package, I think)
type Item struct {
  worry int
}

type Monkey struct {
  items []*Item
  op func(int)int
  test func(int)bool
  left *Monkey  // if true
  right *Monkey // if false
}
func (m *Monkey) Inspect() {
  itm := m.items[0]
  m.items = m.items[1:] // is this the problem?
  itm.worry = m.op(itm.worry)
  itm.worry /= 3
  if m.test(itm.worry) {
    (*m.left).items = append(m.left.items, itm)
  } else {
    (*m.right).items = append(m.right.items, itm)
  }
}

func parseItems(a string) (out []*Item) {
  pts := strings.Split(a, ": ")
  nms := strings.Split(pts[1], ", ")

  for _, v := range nms {
    itm, _ := strconv.ParseInt(v, 10, 0)
    out = append(out, &Item{int(itm)})
  }
  return
}

func parseOperator(a string) func(int)int {
  pts := strings.Split(a, "new = old ")
  opn := string(pts[1][0])
  opd := pts[1][2:]
  if opd == "old" {
    return pow(2)
  }
  v, _ := strconv.ParseInt(opd, 10, 0)
  opval := int(v)
  switch opn {
    case "+":
      return add(opval)
    case "*":
      return mul(opval)
  }
  return noop(0)
}

// parseField, amright

func getNum(a string) int {
  pts := strings.Split(a, " ")
  v, _ := strconv.ParseInt(pts[len(pts) - 1], 10 ,0)
  return int(v)
}

func parseMonkeys(a []string) (out []*Monkey) {
  for range a {
    t := makeTest(
        noop(0),
        func (a int) bool {
          return a==a
        },
      )
    m := Monkey{[]*Item{}, noop(0), t, nil, nil}
    out = append(out, &m)
  }

  for i, block := range a {
    m := out[i]
    lines := util.Lines(block)
    m.items = append(m.items, parseItems(lines[1])...)
    m.op = parseOperator(lines[2])
    m.test = makeTest(mod(getNum(lines[3])), func(a int)bool { return a == 0 })
    m.left = out[getNum(lines[4])]
    m.right = out[getNum(lines[5])]
  }

  return
}

func simulate(a []*Monkey, rounds int) []int {
  out := make([]int, len(a))

  for r := 0; r < rounds; r++ {
    for i, mky := range a {
      // is modifying mky.items in the loop going to cause problems?
      // apparently not
      for range mky.items {
        out[i] += 1
        mky.Inspect()
      }
    }
  }
  return out
}

func dbg(m *Monkey) {
  for _, itm := range m.items {
    print(itm.worry, ", ")
  }
}
func debug(a []*Monkey) {
  for i, m := range a {
    print(i, ": ")
    dbg(m)
    println()
  }
}

func main () {
  inp := util.Args()
  monkeys := parseMonkeys(strings.Split(inp, "\n\n"))
  l := len(monkeys)
  icnt := simulate(monkeys, 20)[:]
  sort.Sort(sort.IntSlice(icnt))
  println(icnt[l-2]*icnt[l-1])

}
