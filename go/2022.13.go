package main

import (
  "agoc/util"
  "agoc/ds"
)

func getNodes(a string) (out []*ds.Node) {
  for _, n := range util.Numbers(a) {
    node := &ds.Node{}
    node.SetValue(n)
    out = append(out, node)
  }
  return
}

func parsePacket(a string) (int, *ds.Node) {
  out := &ds.Node{}
  out.SetValue(-1)
  buf := ""
  l := len(a)
  for i := 0; i < l; i++ {
    c := string(a[i])
    if c == "[" {
      if len(buf) > 0 {
        out.AddNeighbors(getNodes(buf))
        buf = ""
      }
      n, t := parsePacket(a[i+1:])
      i += n + 1
      out.AddNeighbor(t)
    } else if c == "]" {
      if len(buf) > 0 {
        out.AddNeighbors(getNodes(buf))
      }
      return i, out
    } else {
      buf += c
    }
  }
  return l, out
}

func parseBlock(a string) (out []*ds.Node) {
  for _, ln := range util.Lines(a) {
    _, n := parsePacket(ln)
    nb := n.GetNeighbors()
    out = append(out, nb[0])
  }
  return
}

func parseInput(a string) (out [][]*ds.Node) {
  for _, bl := range util.Blocks(a) {
    out = append(out, parseBlock(bl))
  }
  return
}

func comp(a int, b int) int {
  if a > b {
    return -1
  } else if b < a {
    return 1
  }
  return 0
}

func compare(a *ds.Node, b *ds.Node) int {
  A := a.Value.(int)
  B := b.Value.(int)
  left := a.GetNeighbors()
  right := b.GetNeighbors()

  if A != -1 && B != -1 { // both are integers
    return comp(A,B)
  } else if A != -1 { // a is not a list
    left = []*ds.Node{a}
  } else if B != -1 { // b is not a list
    right = []*ds.Node{b}
  }

  r := len(right)
  for i, l := range left {
    if i == r { return -1 } // right ran out of items first
    switch compare(l, right[i]) {
      case -1:
        return -1
      case 1:
        return 1
    }
  }
  return 1
}

func debug(n *ds.Node, depth int) {
  pad := ""
  for i := 0; i < depth; i++ {
    pad += "  "
  }
  println(pad, n.Value.(int))
  nb := n.GetNeighbors()
  for _, N := range nb {
    debug(N, depth + 1)
  }
}

func main() {
  blocks := parseInput(util.Args())
  tot := 0
  for i, block := range blocks {
    if compare(block[0], block[1]) == 1 {
      tot += i + 1
    }
  }
  println(tot)
}
