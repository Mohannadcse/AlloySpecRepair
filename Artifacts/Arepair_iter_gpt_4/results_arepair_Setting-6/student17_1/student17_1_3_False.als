sig List {
header: set Node
}

sig Node {
link: set Node,
elem: set Int
}

// Correct.
fact CardinalityConstraints {
List.header.*link = Node
all l: List | lone l.header
all n: Node | lone n.link
all n: Node | one n.elem
}

// Modified to allow no header.
pred Loop(This: List) {
lone n: This.header.*link | n.link = n
}

// Modified to allow equal elements.
pred Sorted(This: List) {
all n: This.header.*link | n.elem <= n.link.elem
}

assert repair_assert_1 {
all l: List | Sorted[l] <=> { all n: l.header.*link | some n.link => n.elem <= n.link.elem
}}
check repair_assert_1

pred repair_pred_1 {
all l: List | Sorted[l] <=> { all n: l.header.*link | some n.link => n.elem <= n.link.elem
}}
run repair_pred_1

// Correct
pred Count(This: List, x: Int, result: Int) {
RepOk[This]
result = #{n: This.header.*link | n.elem = x}
}

abstract sig Boolean {}
one sig True, False extends Boolean {}

// Correct
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