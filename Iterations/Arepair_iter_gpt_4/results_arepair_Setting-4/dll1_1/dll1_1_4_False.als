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
    all n : Node - last | n.elem < n.nxt.elem
}

// Part (d)
pred ConsistentPreAndNxt() {
    all n : Node | (n.pre + n.nxt).pre = n + n.pre.nxt and n + n.nxt.pre = (n.pre + n.nxt)
}

pred RepOk() {
    UniqueElem
    Sorted
    ConsistentPreAndNxt
}

//run RepOk for 5

assert repair_assert_1{
    Sorted <=>
    all n : Node | some n.nxt => n.elem <= n.nxt.elem
}
check repair_assert_1

pred repair_pred_1{
    Sorted <=>
    all n : Node | some n.nxt => n.elem <= n.nxt.elem
}
run repair_pred_1