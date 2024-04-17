one sig DLL {
    header: lone Node
}

sig Node {
    pre, nxt: lone Node,
    elem: Int
}

// All nodes are reachable from the header node.
fact Reachable {
    Node = DLL.header.*nxt
}

// Part (a)
fact Acyclic {
    all n : Node | n !in n.^nxt
}

// Part (b)
pred UniqueElem() {
    all n1, n2 : Node | n1 != n2 => n1.elem != n2.elem
}

// Part (c)
pred Sorted() {
    all n : Node | no n.nxt or n.elem < n.nxt.elem
}

// Part (d)
pred ConsistentPreAndNxt() {
    all n : Node | (n.pre.nxt = n and n.nxt.pre = n)
}

pred RepOk() {
    UniqueElem
    Sorted
    ConsistentPreAndNxt
}

//run RepOk for 5

assert repair_assert_1{
    Sorted <=>
    all n : Node | no n.nxt or n.elem <= n.nxt.elem
}
check repair_assert_1

pred repair_pred_1{
    Sorted <=>
    all n : Node | no n.nxt or n.elem <= n.nxt.elem
}
run repair_pred_1 for 5