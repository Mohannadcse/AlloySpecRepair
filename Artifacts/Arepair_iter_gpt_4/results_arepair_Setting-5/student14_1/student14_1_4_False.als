sig List {
 header: lone Node
}

sig Node {
 link: lone Node,
 elem: one Int
}

// Overconstraint.  Should be lone l.header and lone n.link
fact CardinalityConstraints {
 all l: List | lone l.header
 all n: Node | lone n.link
 all n: Node | one n.elem
}

// Overconstraint.  Should allow no header.
pred Loop(This: List){
 some n: This.header.*link | n in n.^link
}

// Overconstraint.  Should allow no n.link
pred Sorted(This: List){
 all n: This.header.*link | all m: n.link | n.elem < m.elem
}

assert repair_assert_1 {
 all l: List | Sorted[l] <=> { all n: l.header.*link | no n.link or n.elem < n.link.elem
}}
check repair_assert_1

pred repair_pred_1 {
 all l: List | Sorted[l] <=> { all n: l.header.*link | no n.link or n.elem < n.link.elem
}}
run repair_pred_1

pred RepOk(This: List){
 Loop[This]
 Sorted[This]
}

// Correct
pred Count(This: List, x: Int, result: Int){
 RepOk[This]
 result = #{ n: This.header.*link | x = n.elem }
}

abstract sig Boolean {}
one sig True, False extends Boolean {}

// Correct
pred Contains(This: List, x: Int, result: Boolean) {
 RepOk[This]
 result = True <=> x in This.header.*link.elem
}

fact IGNORE {
 one List
 List.header.*link = Node
}