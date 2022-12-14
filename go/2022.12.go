package main

import (
  "agoc/util"
  "agoc/ds"
)

// TODO: move to package
type Vec2d struct {
  x int
  y int
}

func makeGraph(a []string) (start *ds.Node, end *ds.Node, grid map[Vec2d]*ds.Node) {
  grid = map[Vec2d]*ds.Node{}

  for y, row := range a {
    for x, cell := range row {
      v := string(cell)
      hei := int(cell - 97)
      n := &ds.Node{}
      n.SetValue(hei)

      if v == "S" {
        n.SetValue(0)
        start = n
      }
      if v == "E" {
        n.SetValue(25)
        end = n
      }
      grid[Vec2d{x,y}] = n

      up, uex := grid[Vec2d{x, y - 1}]
      if uex {
        if n.Value.(int) <= up.Value.(int) + 1 {
          up.AddNeighbor(n)
        }
        if up.Value.(int) <= n.Value.(int) + 1 {
          n.AddNeighbor(up)
        }
      }
      lft, lex := grid[Vec2d{x-1, y}]
      if lex {
        if n.Value.(int) <= lft.Value.(int) + 1 {
          lft.AddNeighbor(n)
        }
        if lft.Value.(int) <= n.Value.(int) + 1 {
          n.AddNeighbor(lft)
        }
      }
    }
  }

  return
}

func GetByValue(grid map[Vec2d]*ds.Node, v interface{}) (out []*ds.Node) {
  for _, n := range grid {
    if n.Value == v {
      out = append(out, n)
    }
  }
  return
}

func main() {
  start, end, grid := makeGraph(util.ArgLines())
  path := ds.Seek(start, end)
  println(len(path) - 1)

  basin := GetByValue(grid, 0)
  plens := []int{}
  for _, s := range basin {
    pth := len(ds.Seek(s, end))
    if pth > 0 {
      plens = append(plens, pth)
    }
  }
  mn, _ := util.Min(plens...)
  println(mn - 1)
}
