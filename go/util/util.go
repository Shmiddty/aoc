package util

import (
  "io"
  "os"
  "strings"
  "strconv"
)

func Args() (string) {
  return Slurp(os.Stdin)
}

// Contents returns the file's contents as a string.
func Contents(filename string) (string, error) {
    f, err := os.Open(filename)
    if err != nil {
        return "", err
    }
    defer f.Close()  // f.Close will run when we're finished.

    var result []byte
    buf := make([]byte, 100)
    for {
        n, err := f.Read(buf[0:])
        result = append(result, buf[0:n]...) // append is discussed later.
        if err != nil {
            if err == io.EOF {
                break
            }
            return "", err  // f will be closed if we return here.
        }
    }
    return string(result), nil // f will be closed if we return here.
}

func Slurp(r io.Reader) (string) {
  var result []byte
  buf := make([]byte, 100)
  for {
    n, err  := r.Read(buf[0:])
    result = append(result, buf[0:n]...)
    if err != nil {
      if err == io.EOF {
        break
      }
      return ""
    }
  }
  return string(result)
}

func Lines(s string) []string {
  return strings.Split(s, "\n")
}

func Blocks(s string) []string {
  return strings.Split(s, "\n\n")
}

func Minty(s []string) []int {
  var i []int = make([]int, len(s))
  for j := 0; j < len(s); j++ {
    v, e := strconv.ParseInt(s[j], 10, 0)
    if e != nil {
      break
    }
    i[j] = int(v)
  }
  return i
}

func Sum(a *[]int) (sum int) {
    for _, v := range *a {
        sum += v
    }
    return
}

func Min(a ...int) (int, int) {
    min := int(^uint(0) >> 1)  // largest int
    mini := 0
    for x, i := range a {
        if i < min {
            min = i
            mini = x
        }
    }
    return min, mini
}
func Max(a ...int) (int, int) {
    max := -int(^uint(0) >> 1)  // smolest int
    maxi := 0
    for x, i := range a {
        if i > max {
            max = i
            maxi = x
        }
    }
    return max, maxi
}


