
sig List {
header: set Node
}

sig Node {
link: set Node,
elem: set Int
}

fact CardinalityConstraints {
List.header.*link = Node
all l: List | lone l.header
all n: Node | lone n.link
all n: Node | one n.elem
}

pred Loop(This: List) {
one n: This.header.*link | n.link = n
}

pred Sorted(This: List) {
all n: This.header.*link | all n': n.link | n.elem <= n'.elem
}

assert repair_assert_1 {
all l: List | Sorted[l] <=> { all n: l.header.*link | all n': n.link | n.elem <= n'.elem }
}
check repair_assert_1

pred repair_pred_1 {
all l: List | Sorted[l] <=> { all n: l.header.*link | all n': n.link | n.elem <= n'.elem }
}
run repair_pred_1

pred Count(This: List, x: Int, result: Int) {
RepOk[This]
result = #{n: This.header.*link | n.elem = x}
}

abstract sig Boolean {}
one sig True, False extends Boolean {}

pred Contains(This: List, x: Int, result: Boolean) {
RepOk[This]
result = True <=> x in This.header.*link.elem
}

pred RepOk(This: List) {
Loop[This]
Sorted[This]
}

fact IGNORE {
one List
List.header.*link = Node
}
