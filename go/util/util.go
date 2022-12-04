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

// https://itnext.io/generic-map-filter-and-reduce-in-go-3845780a591c

type Iterator[T any] interface {
	Next() bool
	Value() T
}

type SliceIterator[T any] struct {
	Elements []T
	value    T
	index    int
}

// Create an iterator over the slice xs
func NewSliceIterator[T any](xs []T) Iterator[T] {
	return &SliceIterator[T]{
		Elements: xs,
	}
}

// Move to next value in collection
func (iter *SliceIterator[T]) Next() bool {
	if iter.index < len(iter.Elements) {
		iter.value = iter.Elements[iter.index]
		iter.index += 1
		return true
	}

	return false
}

// Get current element
func (iter *SliceIterator[T]) Value() T {
	return iter.value
}

type mapIterator[T any] struct {
	source Iterator[T]
	mapper func(T) T
}

// advance to next element
func (iter *mapIterator[T]) Next() bool {
	return iter.source.Next()
}

func (iter *mapIterator[T]) Value() T {
	value := iter.source.Value()
	return iter.mapper(value)
}

func Map[T any](iter Iterator[T], f func(T) T) Iterator[T] {
	return &mapIterator[T]{
		iter, f,
	}
}

type filterIterator[T any] struct {
	source Iterator[T]
	pred   func(T) bool
}

func (iter *filterIterator[T]) Next() bool {
	for iter.source.Next() {
		if iter.pred(iter.source.Value()) {
			return true
		}
	}
	return false
}

func (iter *filterIterator[T]) Value() T {
	return iter.source.Value()
}

func Filter[T any](iter Iterator[T], pred func(T) bool) Iterator[T] {
	return &filterIterator[T]{
		iter, pred,
	}
}

func Collect[T any](iter Iterator[T]) []T {
	var xs []T

	for iter.Next() {
		xs = append(xs, iter.Value())
	}

	return xs
}

type Reducer[T, V any] func(accum T, value V) T

// Reduce values iterated over to a single value
func Reduce[T, V any](iter Iterator[V], f Reducer[T, V]) T {
	var accum T
	for iter.Next() {
		accum = f(accum, iter.Value())
	}
	return accum
}
