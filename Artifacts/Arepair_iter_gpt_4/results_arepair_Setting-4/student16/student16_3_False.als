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

// Underconstraint.
pred Loop(This: List) {
    some n: This.header.*link | n in n.^link
}

assert repair_assert_1{
    all l : List | Loop[l] <=> {no l.header or one n: l.header.*link | n = n.link}
}
check repair_assert_1

pred repair_pred_1{
    all l : List | Loop[l] <=> {no l.header or one n: l.header.*link | n = n.link}
}
run repair_pred_1

// Underconstraint.
pred Sorted(This: List) {
    all n: This.header.*link - This.header | let next = n.link | next != none => n.elem < next.elem
}

pred RepOk(This: List) {
    Loop[This]
    Sorted[This]
}

// Underconstraint.
pred Count(This: List, x: Int, result: Int) {
    RepOk[This]
    result = #(This.header.*link.elem & x)
}

abstract sig Boolean {}
one sig True, False extends Boolean {}

// Underconstraint.
pred Contains(This: List, x: Int, result: Boolean) {
    RepOk[This]
    result = if x in This.header.*link.elem then True else False
}

fact IGNORE {
    one List
    List.header.*link = Node
}