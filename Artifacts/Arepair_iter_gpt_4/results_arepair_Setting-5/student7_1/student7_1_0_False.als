sig List {
  header: set Node
}

sig Node {
  link: set Node,
  elem: set Int
}

fact CardinalityConstraints {
  all l: List | #l.header <= 1
  all n: Node | #n.link <= 1
  all n: Node | #n.elem = 1
}

pred Loop(This: List) {
  no n: Node | n in This.header.*link & n in n.^link
}

pred Sorted(This: List) {
  all n: This.header.*link | n.elem <= n.link.elem
}

assert repair_assert_1 {
  all l: List | Sorted[l] <=> { all n: l.header.*link | no n.link or n.elem <= n.link.elem }
}
check repair_assert_1

pred repair_pred_1 {
  all l: List | Sorted[l] <=> { all n: l.header.*link | no n.link or n.elem <= n.link.elem }
}
run repair_pred_1

pred RepOk(This: List) {
  Loop[This]
  Sorted[This]
}

pred Count(This: List, x: Int, result: Int) {
  RepOk[This]
  result = #(This.header.*link.~elem & x)
}

abstract sig Boolean {}
one sig True, False extends Boolean {}

pred Contains(This: List, x: Int, result: Boolean) {
  RepOk[This]
  some This.header.*link.~elem & x => result = True else result = False
}

fact IGNORE {
  one List
  List.header.*link = Node
}