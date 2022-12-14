package main

import (
  "agoc/util"
  "strings"
  "strconv"
)

type Vec2d struct {
  x int
  y int
}

func Add(a Vec2d, b Vec2d) Vec2d {
  return Vec2d{a.x + b.x, a.y + b.y}
}

func Diff(a Vec2d, b Vec2d) Vec2d {
  return Vec2d{a.x - b.x, a.y - b.y}
}

func Abs(v int) int {
  if v < 0 { return -v }
  return v
}

func isTouching(a Vec2d, b Vec2d) bool {
  return Abs(a.x - b.x) < 2 && Abs(a.y - b.y) < 2
}

type Movement struct {
  dir Vec2d
  mag int
}

func ParseInput(a []string) (out []Movement) {
  for _, v := range a {
    parts := strings.Fields(v)
    m, _ := strconv.ParseInt(parts[1], 10, 0)
    mag := int(m) // this isn't strictly necessary
    dir := Vec2d{0, 0}
    switch parts[0] {
      case "U":
        dir.y = -1
        break
      case "D":
        dir.y = 1
        break
      case "L":
        dir.x = -1
        break
      case "R":
        dir.x = 1
        break

    }
    out = append(out, Movement{dir, mag})
  }
  return
}

type Knot struct {
  pos Vec2d
  tail *Knot
  idx int
}

func max(a ...int) int {
  mx, _ := util.Max(a...)
  return mx
}

func (k *Knot) Move(dir Vec2d) {
  k.pos = Add(k.pos, dir)
  t := k.tail
  if t != nil && !isTouching(k.pos, t.pos) {
    d := Diff(k.pos, t.pos)
    t.Move(Vec2d{d.x / max(1, Abs(d.x)), d.y / max(1, Abs(d.y))})
  }
}

func GetRope(ipos Vec2d, knots int) (*Knot, *Knot) {
  tail := &Knot{ipos, nil, 1}
  head := &Knot{ipos, tail, 0}
  for i := 2; i < knots; i++ {
    next := &Knot{ipos, nil, i}
    (*tail).tail = next
    tail = next
  }
  return head, tail
}

func MoveAll(moves []Movement) map[Vec2d]bool {
  head := Vec2d{0, 0}
  tail := Vec2d{0, 0}
  out := map[Vec2d]bool{tail:true}

  for _, mv := range moves {
    for i := 0; i < mv.mag; i++ {
      head = Add(head, mv.dir)
      if !isTouching(head, tail) {
        tail = Vec2d{head.x - mv.dir.x, head.y - mv.dir.y}
        out[tail] = true
      }
    }
  }

  return out
}

func display(k *Knot) {
  mp := map[Vec2d]int{k.pos:k.idx}
  for h := k.tail; h != nil; h = h.tail {
    mp[h.pos] = h.idx
  }
  for y := -20; y < 20; y++ {
    for x := -20; x < 20; x++ {
      knt, ex := mp[Vec2d{x, y}]
      if x == 0 && y == 0 {
        print("s")
      } else if ex {
        print(knt)
      } else {
        print(".")
      }
    }
    println()
  }
  println()
}

func MoveAll1(moves []Movement) map[Vec2d]bool {
  head, tail := GetRope(Vec2d{0, 0}, 2)
  out := map[Vec2d]bool{tail.pos:true}

  for _, mv := range moves {
    for i := 0; i < mv.mag; i++ {
      head.Move(mv.dir)
      out[tail.pos] = true
    }
  }
  return out
}

func MoveAll2(moves []Movement) map[Vec2d]bool {
  head, tail := GetRope(Vec2d{0, 0}, 10)
  out := map[Vec2d]bool{tail.pos:true}

  for _, mv := range moves {
    for i := 0; i < mv.mag; i++ {
      head.Move(mv.dir)
      out[tail.pos] = true
    }
  }
  return out
}

func main() {
  moves := ParseInput(util.ArgLines())
  println(len(MoveAll(moves)))
  two := MoveAll2(moves)
  println(len(two))
}
