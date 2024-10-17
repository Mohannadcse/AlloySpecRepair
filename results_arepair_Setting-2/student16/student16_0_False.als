sig List {
  header: lone Node
}

sig Node {
  link: lone Node,
  elem: one Int
}

fact CardinalityConstraints {
  all l: List | lone l.header
  all n: Node | lone n.link
  all n: Node | one n.elem
}

pred Loop(This: List) {
  no This.header or one n: This.header.*link | n = n.link
}

assert repair_assert_1 {
  all l: List | Loop[l] <=> {no l.header or one n: l.header.*link | n = n.link}
}
check repair_assert_1

pred repair_pred_1 {
  all l: List | Loop[l] <=> {no l.header or one n: l.header.*link | n = n.link}
}
run repair_pred_1

pred Sorted(This: List) {
  all n: This.header.*link | all m: n.link.*link | n.elem <= m.elem
}

pred RepOk(This: List) {
  Loop[This]
  Sorted[This]
}

pred Count(This: List, x: Int, result: Int) {
  RepOk[This]
  result = #(This.header.*link & Node.elem.x)
}

abstract sig Boolean {}
one sig True, False extends Boolean {}

pred Contains(This: List, x: Int, result: Boolean) {
  RepOk[This]
  result = (some n: This.header.*link | n.elem = x) => True else False
}

fact IGNORE {
  one List
  List.header.*link = Node
}