sig List {
  header: lone Node
}

sig Node {
  link: lone Node,
  elem: one Int
}

// Correct
fact CardinalityConstraints {
  all l: List | lone l.header
  all n: Node | lone n.link
  all n: Node | one n.elem
}

// Correct
pred Loop(This: List) {
  no This.header || one n: This.header.^link | n = n.link
}

// Fixed Sorted predicate to handle non-looping lists
pred Sorted(This: List) {
  all n: (This.header.*link) - This.header | n.link != none => n.elem <= n.link.elem
}

assert repair_assert_1 {
  all l: List | Sorted[l] <=> { all n: l.header.*link | some n.link => n.elem <= n.link.elem }
}
check repair_assert_1

pred repair_pred_1 {
  all l: List | Sorted[l] <=> { all n: l.header.*link | some n.link => n.elem <= n.link.elem }
}
run repair_pred_1

pred RepOk(This: List) {
  Loop[This]
  Sorted[This]
}

// Correct
pred Count(This: List, x: Int, result: Int) {
  RepOk[This]
  result = #{n: This.header.*link | n.elem = x}
}

abstract sig Boolean {}
one sig True, False extends Boolean{}

// Correct
pred Contains(This: List, x: Int, result: Boolean) {
  RepOk[This]
  x in This.header.*link.elem => result = True else result = False
}

fact IGNORE {
  one List
  List.header.*link = Node
}