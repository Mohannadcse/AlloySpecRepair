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
}

pred Loop(This: List) {
all n: Node | n in This.header.*link
no This.header || one n: This.header.*link | n in n.^link
}

pred Sorted(This: List) {
all n: This.header.*link | all m: n.link | n.elem <= m.elem
}

assert repair_assert_1 {
all l: List | Sorted[l] <=> { all n: l.header.*link | all m: n.link | n.elem <= m.elem }
}
check  repair_assert_1

pred RepOk(This: List) {
Loop[This]
Sorted[This]
}

pred Count(This: List, x: Int, result: Int) {
RepOk[This]
result = #{n:This.header.*link | n.elem = x}
}

abstract sig Boolean {}
one sig True, False extends Boolean {}

pred Contains (This: List, x: Int, result: Boolean) {
RepOk[This]
#{n: This.header.*link | x in n.elem} != 0 => result = True
#{n: This.header.*link | x in n.elem} = 0 => result = False
}

fact IGNORE {
one List
List.header.*link = Node
}