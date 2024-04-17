sig List {
    header: set Node
}

sig Node {
    link: set Node,
    elem: set Int
}

// Correct
fact CardinalityConstraints {
    all l: List | #l.header <= 1
    all n: Node | #n.link <= 1
    all n: Node | #n.elem = 1
}

// Overconstraint. Should allow no l.header
// Underconstraint.  Should not allow link = n1 -> n2 + n2 -> n3 + n3 -> n1
// Overconstraint. Should allow link = n1 -> n2 + n2 -> n3 + n3 -> n3
pred Loop(This: List) {
    all n: Node | n in This.header.link.^(link) implies n in This.header
    no disj n1, n2, n3: Node | n1->n2 + n2->n3 + n3->n1 in This.header.*link
    some n: Node | n in This.header.*link and n.link = n
}

// Overconstraint.  Should allow no n.link
pred Sorted(This: List) {
    all n: Node | n in This.header.*link implies n.elem <= n.link.elem
}

assert repair_assert_1 {
    all l: List | Sorted[l] <=> { all n: l.header.*link | n.link = none or n.elem <= n.link.elem }
}
check repair_assert_1

pred repair_pred_1 {
    all l: List | Sorted[l] <=> { all n: l.header.*link | n.link = none or n.elem <= n.link.elem }
}
run repair_pred_1

pred RepOk(This: List) {
    Loop[This]
    Sorted[This]
}

// Underconstraint.  x.~elem may not be in This. Correct if all nodes in List.
pred Count(This: List, x: Int, result: Int) {
    RepOk[This]
    result = #(This.header.*link.~elem & x)
}

abstract sig Boolean {}
one sig True, False extends Boolean {}
// Underconstraint.  x.~elem may not be in This. Correct if all nodes in List.
pred Contains(This: List, x: Int, result: Boolean) {
    RepOk[This]
    some This.header.*link.~elem & x => result = True else result = False
}

fact IGNORE {
    one List
    List.header.*link = Node
}