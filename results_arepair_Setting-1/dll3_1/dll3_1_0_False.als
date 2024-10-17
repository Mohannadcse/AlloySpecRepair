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

fact Acyclic {
  all n : Node {
    // The list has no directed cycle along nxt, i.e., no node is
    // reachable from itself following one or more traversals along nxt.
    n not in n.^(nxt)
  }
}

pred UniqueElem() {
  // Unique nodes contain unique elements.
  all disj n1, n2: Node | n1.elem != n2.elem
}

pred Sorted() {
  // The list is sorted in ascending order (<=) along link.
  all n: DLL.header.*nxt | some n.nxt implies n.elem <= n.nxt.elem
}

pred ConsistentPreAndNxt() {
  // For any node n1 and n2, if n1.nxt = n2, then n2.pre = n1; and vice versa.
  all n1, n2: Node | (n1.nxt = n2) implies (n2.pre = n1)
}

pred RepOk() {
  UniqueElem
  Sorted
  ConsistentPreAndNxt
}

run RepOk for 3

assert repair_assert_1 {
  all n: Node | n not in n.^nxt
}
check repair_assert_1

pred repair_pred_1 {
  all n: Node | n not in n.^nxt
}
run repair_pred_1