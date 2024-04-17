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
all n: This.header.*link | n in n.^link
}

assert repair_assert_1{
all l : List | Loop[l] <=> {no l.header or one n: l.header.*link | n = n.link}
}
check repair_assert_1

pred repair_pred_1{
all l : List | Loop[l] <=> {no l.header or one n: l.header.*link | n = n.link}
}
run repair_pred_1

pred Sorted(This: List) {
all n: This.header.*link | n.elem < n.link.elem
}

pred RepOk(This: List) {
Loop[This]
Sorted[This]
}

pred Count(This: List, x: Int, result: Int) {
RepOk[This]
all n: This.header.*link | n.elem = x
}

abstract sig Boolean {}
one sig True, False extends Boolean {}

pred Contains(This: List, x: Int, result: Boolean) {
RepOk[This]
all n: This.header.*link | n.elem = x
}

fact IGNORE {
one List
List.header.*link = Node
}