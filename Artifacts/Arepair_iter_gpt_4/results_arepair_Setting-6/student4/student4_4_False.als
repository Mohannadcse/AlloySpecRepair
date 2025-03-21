sig List {
header: set Node
}

sig Node {
link: set Node,
elem: set Int
}

// Correct
fact CardinalityConstraints {
all l:List | lone l.header
all n:Node | lone n.link
all n:Node | one n.elem
}

// Correct
pred Loop(This: List) {
no This.header || one n:This.header.^link | n = n.link
}

// Fixed
pred Sorted(This: List) {
all n:(This.header.*link) | all n2: n.link | n.elem <= n2.elem
}

assert repair_assert_1 {
all l: List | Sorted[l] <=> { all n: l.header.*link | all n2: n.link => n.elem <= n2.elem
}}
check repair_assert_1

pred repair_pred_1 {
all l: List | Sorted[l] <=> { all n: l.header.*link | all n2: n.link => n.elem <= n2.elem
}}
run repair_pred_1


pred RepOk(This: List) {
Loop[This]
Sorted[This]
}

// Correct
pred Count(This: List, x: Int, result: Int) {
RepOk[This]
result = #{n: This.header.*link | n.elem = x}
}

abstract sig Boolean {}
one sig True, False extends Boolean{}

// Correct
pred Contains(This: List, x: Int, result: Boolean) {
RepOk[This]
x in This.header.*link.elem => result = True else result = False
}

fact IGNORE {
one List
List.header.*link = Node
}