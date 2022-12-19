package cart

type Vec2d struct {
  X int
  Y int
}

func (a Vec2d) Add(b Vec2d) Vec2d {
  return Add(a, b)
}

func (a Vec2d) Diff(b Vec2d) Vec2d {
  return Diff(a, b)
}

func Add(a Vec2d, b Vec2d) Vec2d {
  return Vec2d{a.X + b.X, a.Y + b.Y}
}

func Diff(a Vec2d, b Vec2d) Vec2d {
  return Vec2d{a.X - b.X, a.Y - b.Y}
}

type Grid struct {
  Cells map[Vec2d]int
}

func (g *Grid) GetBounds() (Vec2d, Vec2d) {
  mn := Vec2d{int(^uint(0) >> 1), int(^uint(0) >> 1)}
  mx := Vec2d{-int(^uint(0) >> 1), -int(^uint(0) >> 1)}

  for k, _ := range g.Cells {
    if k.X < mn.X { mn.X = k.X }
    if k.X > mx.X { mx.X = k.X }
    if k.Y < mn.Y { mn.Y = k.Y }
    if k.Y > mx.Y { mx.Y = k.Y }
  }
  return mn, mx
}

func (g *Grid) Display() {
  mn, mx := g.GetBounds()

  for y := mn.Y; y <= mx.Y; y++ {
    ln := ""
    for x := mn.X; x <= mx.X; x++ {
      ln += string(".#O"[g.Cells[Vec2d{x, y}]])
    }
    println(ln)
  }
}

func (g *Grid) ByValue(val int) (out []Vec2d) {
  for k, v := range g.Cells {
    if v == val {
      out = append(out, k)
    }
  }
  return
}
