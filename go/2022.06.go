package main

import (
  "agoc/util"
  "strings"
)

// it should not be difficult to write this as a generic function.
// why do I need to specify the type of items an array holds when I'm not even handling the items themselves?
// I thought Go was supposed to be simple and boring.
// I can write it these ways, but apparently I can't use
// a value of type []string for an []interface{} argument or []any argument.
//func divvy(a []interface{}, n int) (out []interface{}) {
//func divvy(a []any, n int) (out []any) {
func divvy(a string, n int) (out []string) {
  for i := 0; i < len(a) - n; i++ {
    out = append(out, a[i:i+n])
  }
  return
}

func isPretty(s string) bool {
  for i, v := range s {
    if strings.Contains(s[i+1:], string(v)) {
      return false
    }
  }
  return true
}

func main() {
  ds := util.Args()
  for i, v := range divvy(ds, 4) {
    if isPretty(v) {
      println(i + 4)
      break
    }
  }
  for i, v := range divvy(ds, 14) {
    if isPretty(v) {
      println(i + 14)
      break
    }
  }
  //Outer:
  //for i := 0; i < len(ds) - 4; i++ {
  //  buf := string(ds[i])
  //  for j := 1; j < 4; j++ {
  //    if strings.Contains(ds[i:i+j], ds[i+j:i+j+1]) {
  //      continue Outer
  //    }
  //  }
  //}
}
