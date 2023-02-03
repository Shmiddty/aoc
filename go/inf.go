package main

import (
  "agoc/util"
  "agoc/cart"
)

func main() {
  lns := util.ArgLines()
  grid := cart.Grid{map[cart.Vec2d]int{}}
  for y, ln := range lns {
    for x, cell := range ln {
      if cell > 46 {
        grid.Cells[cart.Vec2d{x,y}] = int(cell - 47)
      }
    }
  }
  grid.Display(".#@.....SEP")
}
