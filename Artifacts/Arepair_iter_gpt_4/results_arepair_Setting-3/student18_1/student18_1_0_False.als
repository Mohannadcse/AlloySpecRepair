sig List {
header : lone Node
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
no This.header.link or one n: This.header.*link | n.link = n
}

pred Sorted(This: List) {
all n: This.header.*link | lone n.link and n.elem < n.link.elem
}

assert repair_assert_1 {
all l: List | Sorted[l] implies { all n: l.header.*link | some n.link and n.elem <= n.link.elem
}}
check repair_assert_1

pred repair_pred_1 {
all l: List | Sorted[l] implies { all n: l.header.*link | some n.link and n.elem <= n.link.elem
}}
run repair_pred_1

pred RepOk(This: List) {
Loop[This]
Sorted[This]
}

pred Count(This: List, x: Int, result: Int) {
RepOk[This]
result = #{n: Node | n in This.header.*link and n.elem = x}
}

abstract sig Boolean {}
one sig True, False extends Boolean {}

pred Contains(This: List, x: Int, result: Boolean) {
RepOk[This]
{some n: This.header.*link | n.elem = x} implies result = True else result = False
}

fact IGNORE {
one List
List.header.*link = Node
}