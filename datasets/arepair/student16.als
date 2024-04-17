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
}

pred RepOk(This: List) {
     Loop[This]
     Sorted[This]
}

// Underconstraint.
pred Count(This: List, x: Int, result: Int) {
     RepOk[This]
}

abstract sig Boolean {}
one sig True, False extends Boolean {}

// Underconstraint.
pred Contains(This: List, x: Int, result: Boolean) {
     RepOk[This]
}

fact IGNORE {
  one List
  List.header.*link = Node
}