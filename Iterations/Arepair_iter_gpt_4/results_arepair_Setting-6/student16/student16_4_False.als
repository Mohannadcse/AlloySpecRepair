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

// Corrected Loop predicate to check for cycles.
pred Loop(This: List) {
some n: This.header.*link | n in n.^link
}

// Corrected assertion to reflect the Loop predicate.
assert repair_assert_1{
all l : List | Loop[l] <=> {no l.header or some n: l.header.*link | n in n.^link}
}
check repair_assert_1

// Corrected Loop predicate in the context of repair_pred_1.
pred repair_pred_1{
all l : List | Loop[l] <=> {no l.header or some n: l.header.*link | n in n.^link}
}
run repair_pred_1

// Corrected Sorted predicate to check if the list is sorted.
pred Sorted(This: List) {
all n: This.header.*link - This.header | all m: n.link | n.elem < m.elem
}

pred RepOk(This: List) {
Loop[This]
Sorted[This]
}

// Corrected Count predicate to count occurrences of x in the list.
pred Count(This: List, x: Int, result: Int) {
RepOk[This]
result = #(This.header.*link.elem & x)
}

abstract sig Boolean {}
one sig True, False extends Boolean {}

// Corrected Contains predicate to check if x is in the list.
pred Contains(This: List, x: Int, result: Boolean) {
RepOk[This]
result = if x in This.header.*link.elem then True else False
}

fact IGNORE {
one List
List.header.*link = Node
}