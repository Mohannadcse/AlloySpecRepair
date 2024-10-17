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

// Adjusted Loop predicate to avoid overconstraint and underconstraint
pred Loop(This: List) {
  all n: Node | n in This.header.*link => n.link != This.header
  some n: Node | n in This.header.*link && n.link = This.header
}

// Adjusted Sorted predicate to avoid overconstraint
pred Sorted(This: List) {
  all n: Node | n in This.header.*link && some n.link => n.elem <= n.link.elem
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
  result = #{n: Node | n in This.header.*link && n.elem = x}
}

abstract sig Boolean {}
one sig True, False extends Boolean {}

// Correct
pred Contains(This: List, x: Int, result: Boolean) {
  RepOk[This]
  #{n: Node | n in This.header.*link && n.elem = x} > 0 => result = True else result = False
}

fact IGNORE {
  one List
  List.header.*link = Node
}