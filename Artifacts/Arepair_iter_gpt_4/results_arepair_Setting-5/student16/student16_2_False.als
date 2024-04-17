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

// Corrected Loop predicate
pred Loop(This: List) {
all n: This.header.*link | n not in n.^link
}

assert repair_assert_1{
all l : List | Loop[l] <=> {no l.header or one n: l.header.*link | n = n.^link}
}
check repair_assert_1

// Corrected Sorted predicate
pred Sorted(This: List) {
all n: Node, n2: n.link | n.elem < n2.elem
}

pred RepOk(This: List) {
Loop[This]
Sorted[This]
}

// Corrected Count predicate
pred Count(This: List, x: Int, result: Int) {
RepOk[This]
result = #(This.header.*link.elem & x)
}

abstract sig Boolean {}
one sig True, False extends Boolean {}

// Corrected Contains predicate
pred Contains(This: List, x: Int, result: Boolean) {
RepOk[This]
result = if x in This.header.*link.elem then True else False
}

fact IGNORE {
one List
List.header.*link = Node
}