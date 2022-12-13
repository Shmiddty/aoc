package main

import (
  "agoc/util"
  "agoc/ds"
  "strings"
  "strconv"
)

type File struct {
  size int
  name string
}

type Directory struct {
  name string
  // TODO: how make recursive type?
  //parent Directory
  children map[string]*Directory
  files []File
}



func ParseInput(a string) (root Directory) {
  cmds := strings.Split(a, "$ ")
  // we can reliably know that the first line is "$ cd /"
  root.name = "/"
  root.children = map[string]*Directory{}
  cur := &root // what I suspect is that when I update cur, root is not also updated
  par := ds.Stack{}
  par.Push(cur)

  for _, cmdblock := range cmds[2:] {
    parts := strings.Split(strings.TrimSpace(cmdblock), "\n")
    cparts := strings.Split(parts[0], " ")
    cmd := cparts[0]
    args := cparts[1:]
    switch cmd {
      case "ls":
        for _, f := range parts[1:] {
          fparts := strings.Split(f, " ")
          fname := fparts[1]
          ftype := fparts[0]
          if ftype == "dir" {
            (*cur).children[fname] = &Directory{fname, map[string]*Directory{}, nil}
          } else {
            size, _ := strconv.ParseInt(ftype, 10, 0)
            (*cur).files = append((*cur).files, File{int(size), fname})
          }
        }
        break
      case "cd":
        name := args[0]
        if name == ".." {
          d := par.Pop().(Directory)
          cur = &d
        } else {
          par.Push(*cur)
          d := cur.children[name]
          cur = d
        }
        break
    }
  }
  return
}

func (d Directory) Size() (out int) {
  for _, f := range d.files {
    out += f.size
  }

  for _, c := range d.children {
    out += c.Size()
  }

  return
}

func (d Directory) Flatten() (out []Directory) {
  out = append(out, d)
  for _, c := range d.children {
    out = append(out, c.Flatten()...)
  }
  return
}

func main() {
  tree := ParseInput(util.Args())
  ftree := tree.Flatten()
  tot := 0
  for _, t := range ftree {
    s := t.Size()
    if s <= 100000 {
      tot += s
    }
  }
  println(tot)

  avail := 70000000 - tree.Size()
  min := int(^uint(0) >> 1)
  for _, t := range ftree {
    s := t.Size()
    if avail + s >= 30000000 && s < min {
      min = s
    }
  }
  println(min)
}
