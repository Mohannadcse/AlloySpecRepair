one sig DLL {
header: lone Node
}

sig Node {
pre, nxt: lone Node,
elem: Int
}

fact Reachable {
Node = DLL.header.*nxt
}

fact Acyclic {
all n : Node {
n not in n.^nxt
}
}

pred UniqueElem() {
all n:Node | no n.pre.elem & n.nxt.elem
}

pred Sorted() {
all n: DLL.header.*nxt | some n.nxt implies n.elem <= n.nxt.elem
}

pred ConsistentPreAndNxt() {
all n1, n2: Node {
some n1.nxt=n2 implies n2.pre = n1
some n1.pre=n2 implies n2.nxt = n1
}
}

pred RepOk() {
UniqueElem
Sorted
ConsistentPreAndNxt
}

assert repair_assert_1{
all n: Node | n not in n.^nxt
}
check repair_assert_1

pred repair_pred_1{
all n: Node | n not in n.^nxt
}
run repair_pred_1