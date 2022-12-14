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

type Queue struct {
  items []interface{}
}

func (q *Queue) Enqueue(v interface{}) {
  q.items = append(q.items, v)
}

func (q *Queue) Dequeue() interface{} {
  if len(q.items) == 0 {
    return nil
  }
  v := q.Peek()
  q.items = q.items[1:]
  return v
}

func (q *Queue) Peek() interface{} {
  if len(q.items) == 0 {
    return nil
  }
  return q.items[0]
}

func (q *Queue) Size() int {
  return len(q.items)
}

func (q *Queue) Contains(v interface{}) bool {
  for _, V := range q.items {
    if &V == &v { return true }
  }
  return false
}

type Node struct {
  Value interface{}
  neighbors []*Node
}

func (n *Node) SetValue(v interface{}) {
  n.Value = v
}

func (n *Node) AddNeighbor(a *Node) {
  n.neighbors = append(n.neighbors, a)
}

func (n *Node) GetNeighbors() []*Node {
  return n.neighbors
}

func contains(a []Node, v Node) bool {
  // this might be wrong. 
  for _, c := range a {
    if &c == &v { return true }
  }
  return false
}

func Seek(start *Node, end *Node) []Node {
  out := []Node{}
  q := Queue{}
  q.Enqueue(start)

  cameFrom := map[*Node]*Node{}
  score := map[*Node]int{start:0}

  for q.Size() > 0 {
    cur := q.Dequeue().(*Node)
    if cur == end {
      n := cur
      for n != nil {
        out = append(out, *n)
        n = cameFrom[n]
      }
      break
    }
    for _, n := range cur.neighbors {
      s := score[cur] + 1
      v, e := score[n]
      if !e || s < v {
        cameFrom[n] = cur
        score[n] = s

        if !q.Contains(n) {
          q.Enqueue(n)
        }
      }
    }
  }

  return out
}
