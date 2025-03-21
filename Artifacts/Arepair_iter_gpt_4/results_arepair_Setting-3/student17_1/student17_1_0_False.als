sig List {
header: lone Node
}

sig Node {
link: lone Node,
elem: one Int
}

fact CardinalityConstraints {
List.header.*link = Node
all l: List | lone l.header
all n: Node | lone n.link
all n: Node | one n.elem
}

pred Loop(This: List) {
no n: This.header.*link | n.link = n
}

pred Sorted(This: List) {
all n: This.header.*link | no n.link or n.elem < n.link.elem
}

assert repair_assert_1 {
all l: List | Sorted[l] <=> { all n: l.header.*link | no n.link or n.elem <= n.link.elem
}}
check repair_assert_1

pred repair_pred_1 {
all l: List | Sorted[l] <=> { all n: l.header.*link | no n.link or n.elem <= n.link.elem
}}
run repair_pred_1

pred Count(This: List, x: Int, result: Int) {
RepOk[This]
result = #{n: This.header.*link | n.elem = x}
}

abstract sig Boolean {}
one sig True, False extends Boolean {}

pred Contains(This: List, x: Int, result: Boolean) {
RepOk[This]
result = True <=> x in This.header.*link.elem
}

pred RepOk(This: List) {
Loop[This]
Sorted[This]
}

fact IGNORE {
one List
List.header.*link = Node
}