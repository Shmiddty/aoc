package main

import (
  "agoc/util"
  "agoc/cart"
  "strings"
)

func parseInput(a []string) [][]*cart.Vec2d {
  out := make([][]*cart.Vec2d, len(a))
  for i, ln := range a {
    out[i] = []*cart.Vec2d{}
    for _, coord := range strings.Split(ln, " -> ") {
      nums := util.Numbers(coord)
      pt := cart.Vec2d{nums[0], nums[1]}
      out[i] = append(out[i], &pt)
    }
  }
  return out
}

func makeGrid(a [][]*cart.Vec2d) *cart.Grid {
  out := &cart.Grid{map[cart.Vec2d]int{}}
  for _, rock := range a {
    for i := 1; i < len(rock); i++ {
      frm := rock[i-1]
      to := rock[i]
      mnx, _ := util.Min(frm.X, to.X)
      mxx, _ := util.Max(frm.X, to.X)
      mny, _ := util.Min(frm.Y, to.Y)
      mxy, _ := util.Max(frm.Y, to.Y)
      for x := mnx; x <= mxx; x++ {
        out.Cells[cart.Vec2d{x, frm.Y}] = 1
      }
      for y := mny; y <= mxy; y++ {
        out.Cells[cart.Vec2d{frm.X, y}] = 1
      }
    }
  }
  return out
}

func makeIsBlocked(a *cart.Grid) func(cart.Vec2d)bool {
  return func(pt cart.Vec2d) bool {
    return isBlocked(a, pt)
  }
}

func isBlocked(a *cart.Grid, pt cart.Vec2d) bool {
  return a.Cells[pt] != 0
}

func step(a *cart.Grid, bot int) bool {
  blocked := makeIsBlocked(a)
  dwn := cart.Vec2d{0, 1}
  lft := cart.Vec2d{-1, 1}
  rgt := cart.Vec2d{1, 1}

  pt := cart.Vec2d{500, 0}
  for pt.Y < bot{
    if !blocked(pt.Add(dwn)) {
      pt = pt.Add(dwn)
    } else if !blocked(pt.Add(lft)) {
      pt = pt.Add(lft)
    } else if !blocked(pt.Add(rgt)) {
      pt = pt.Add(rgt)
    } else {
      a.Cells[pt] = 2
      return true
    }
  }
  return false
}

func simulate(grid *cart.Grid, dbg bool) {
  _, mx := grid.GetBounds()
  bot := mx.Y
  if dbg { grid.Display() }
  dirty := true
  for dirty {
    dirty = step(grid, bot)
    if dbg { grid.Display() }
  }
}

func main() {
  grid := makeGrid(parseInput(util.ArgLines()))
  simulate(grid, false)
  sand := grid.ByValue(2)
  println(len(sand))
}
