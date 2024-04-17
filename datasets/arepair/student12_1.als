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
    This.header.*link = Node
    no This.header || one n: This.header.*link | n in n.link
}

// Overconstraint.  Should not allow link = n1 -> n2 + n2 -> n1
// Underconstraint.  Should allow no n.link
pred Sorted(This: List) {
    all n: This.header.*link | n.elem <= n.^link.elem
}

assert repair_assert_1 {
	all l: List | Sorted[l] <=> { all n: l.header.*link | some n.link => n.elem <= n.link.elem
}}
check repair_assert_1

pred repair_pred_1 {
	all l: List | Sorted[l] <=> { all n: l.header.*link | some n.link => n.elem <= n.link.elem
}}
run repair_pred_1

pred RepOk(This: List) {
    Loop[This]
    Sorted[This]
}

// Correct
pred Count(This: List, x: Int, result: Int) {
    RepOk[This]
    result = #{ n: This.header.*link | n.elem = x }
}

abstract sig Boolean {}
one sig True, False extends Boolean {}

// Overconstraint.  result should be True as long as one of the elem = x.
pred Contains(This: List, x: Int, result: Boolean) {
    RepOk[This]
    { all n: This.header.*link | n.elem = x } =>result = True else result = False
}

fact IGNORE {
  one List
  List.header.*link = Node
}
