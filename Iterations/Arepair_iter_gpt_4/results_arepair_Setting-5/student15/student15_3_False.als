sig List {
header: set Node
}

sig Node {
link: set Node,
elem: set Int
}

fact CardinalityConstraints {
all l: List | lone l.header
all n: Node | lone n.link
all n: Node | one n.elem
all n:Node | some l : List | n in l.header.*link
}

pred Loop(This: List) {
no This.header || one n : This.header.*link | n = n.link
}

pred Sorted(This: List) {
all n : This.header.*link | no n.link or n.elem < n.link.elem
}

assert repair_assert_1 {
all l: List | Sorted[l] <=> { all n: l.header.*link | no n.link or n.elem <= n.link.elem }
}
check repair_assert_1

pred RepOk(This: List) {
Loop[This]
Sorted[This]
}

pred Count(This: List, x: Int, result: Int) {
RepOk[This]
result = #{n: (This.header.*link) | n.elem = x}
}

abstract sig Boolean {}
one sig True, False extends Boolean {}

pred Contains(This: List, x: Int, result: Boolean) {
RepOk[This]
(x in (This.header.*link).elem <=> result = True)
}

fact IGNORE {
one List
List.header.*link = Node
}