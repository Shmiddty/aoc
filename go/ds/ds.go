package ds

type Stack struct {
  items []interface{}
}

func (s *Stack) Push(v interface{}) {
  s.items = append(s.items, v)
}

func (s *Stack) Pop() interface{} {
  if len(s.items) == 0 {
    return nil
  }
  v := s.Peek()
  s.items = s.items[0:len(s.items) - 1]
  return v
}

func (s *Stack) Peek() interface{} {
  if len(s.items) == 0 {
    return nil
  }
  return s.items[len(s.items) - 1]
}

func (s *Stack) Size() int {
  return len(s.items)
}
