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

// Fixed Loop predicate
pred Loop(This: List) {
some n: This.header.*link | n in This.header
}

assert repair_assert_1{
all l : List | Loop[l] <=> {no l.header or one n: l.header.*link | n = n.link}
}
check repair_assert_1

// Fixed Sorted predicate
pred Sorted(This: List) {
all n: This.header.*link - This.header | n.elem < n.link.elem
}

pred RepOk(This: List) {
Loop[This]
Sorted[This]
}

// Fixed Count predicate
pred Count(This: List, x: Int, result: Int) {
RepOk[This]
result = #(This.header.*link.elem & x)
}

abstract sig Boolean {}
one sig True, False extends Boolean {}

// Fixed Contains predicate
pred Contains(This: List, x: Int, result: Boolean) {
RepOk[This]
result = if x in This.header.*link.elem then True else False
}

fact IGNORE {
one List
List.header.*link = Node
}