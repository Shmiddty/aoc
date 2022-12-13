package main

import (
  "agoc/util"
  "strconv"
)

// this is not very efficient
func isVisible(row int, col int, theMap [][]int) bool {
  wid := len(theMap[0])
  hei := len(theMap)

  if row == 0 || col == 0 || row == hei - 1 || col == wid - 1 {
    return true
  }

  height := theMap[row][col]
  up := true
  for y := row - 1; y >= 0; y-- {
    if theMap[y][col] >= height {
      up = false
      break
    }
  }
  if up { return true }
  down := true
  for y := row + 1; y < hei; y++ {
    if theMap[y][col] >= height {
      down = false
      break
    }
  }
  if down { return true }
  left := true
  for x := col - 1; x >= 0; x-- {
    if theMap[row][x] >= height {
      left = false
      break
    }
  }
  if left { return true }
  for x := col + 1; x < wid; x++ {
    if theMap[row][x] >= height {
      return false
    }
  }
  return true
}

func scenicScore(row int, col int, theMap [][]int) int {
  wid := len(theMap[0])
  hei := len(theMap)
  height := theMap[row][col]

  up := 0
  for y := row - 1; y >= 0; y-- {
    up += 1
    if theMap[y][col] >= height {
      break
    }
  }
  down := 0
  for y := row + 1; y < hei; y++ {
    down += 1
    if theMap[y][col] >= height {
      break
    }
  }
  left := 0
  for x := col - 1; x >= 0; x-- {
    left += 1
    if theMap[row][x] >= height {
      break
    }
  }
  right := 0
  for x := col + 1; x < wid; x++ {
    right += 1
    if theMap[row][x] >= height {
      break
    }
  }

  return up * down * left * right
}

func main() {
  inp := util.ArgLines()
  theMap := make([][]int, len(inp))
  for y, row := range inp {
    for _, cell := range row {
      val, _ := strconv.ParseInt(string(cell), 10, 0)
      theMap[y] = append(theMap[y], int(val))
    }
  }

  // part 1 & 2
  cnt := 0
  max := 0 // usually you'd do -maxint, but it isn't necessary here
  for x, row := range theMap {
    for y, _ := range row {
      if isVisible(x, y, theMap) {
        cnt += 1
      }
      score := scenicScore(x, y, theMap)
      if score > max {
        max = score
      }
    }
  }
  println(cnt)
  println(max)
}
