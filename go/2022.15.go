package main

import (
  "agoc/util"
  "agoc/cart"
)

func makeGrid(a []string) *cart.Grid {
  out := &cart.Grid{map[cart.Vec2d]int{}}
  for _, ln := range a {
    nums := util.Numbers(ln)
    sens := cart.Vec2d{nums[0], nums[1]}
    beac := cart.Vec2d{nums[2], nums[3]}
    //d := sens.Manhattan(beac)
    //for y := sens.Y - d; y <= sens.Y + d; y++ {
    //  rx := sens.Y - y
    //  for x := sens.X - d + rx; x <= sens.X + d - rx; x++ {
    //    pt := cart.Vec2d{x, y}
    //    if sens.Manhattan(pt) <= d {
    //      out.Cells[pt] = 1
    //    }
    //  }
    //}
    out.Cells[sens] = 2
    out.Cells[beac] = 3
  }
  return out
}

func beacant(a *cart.Grid, y int) int {
  mn, mx := a.GetBounds()
  tot := 0
  for x := mn.X; x <= mx.X; x++ {
    v := a.Cells[cart.Vec2d{x, y}]
    if v == 1 {
      tot += 1
    }
  }
  return tot
}

func main() {
  grid := makeGrid(util.ArgLines()) // doesn't finish for real input
  // need to do this without building a grid
  // filter signals and beacons whose manhattan distance crosses the target y
  // then do the beacant
  // but meh.
  println("pong", len(grid.Cells))
  //grid.Display(".#SB")
  //println(beacant(grid, 10))
  //println(beacant(grid, 2000000))
}
