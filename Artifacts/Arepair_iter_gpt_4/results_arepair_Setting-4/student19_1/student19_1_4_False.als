sig List {
header: set Node
}

sig Node {
link: set Node,
elem: set Int
}

// Correct
fact CardinalityConstraints {
all l: List | lone l.header
all n: Node | lone n.link
all n: Node | one n.elem
}

// Correct
pred Loop(This: List) {
no This.header || one n: This.header.*link | n in n.^link
}

// Fixed Sorted predicate to allow no n.link
pred Sorted(This: List) {
all n:This.header.*link | no n.link or n.elem < n.link.elem
}

pred RepOk(This: List) {
Loop[This]
Sorted[This]
}

// Fixed Count predicate to correctly count occurrences of x
pred Count(This: List, x: Int, result: Int) {
RepOk[This]
result = #(This.header.*link.elem & x)
}

abstract sig Boolean {}
one sig True, False extends Boolean {}

// Correct.
pred Contains(This: List, x: Int, result: Boolean) {
RepOk[This]
(some n: This.header.*link | x in n.elem && result = True) || (all n: This.header.*link | x !in n.elem && result = False)
}

fact IGNORE {
one List
List.header.*link = Node
}

assert repair_assert_1 {
all l: List | Sorted[l] <=> { all n: l.header.*link | no n.link or n.elem <= n.link.elem
}}
check  repair_assert_1

pred repair_pred_1 {
all l: List | Sorted[l] <=> { all n: l.header.*link | no n.link or n.elem <= n.link.elem
}}
run  repair_pred_1
