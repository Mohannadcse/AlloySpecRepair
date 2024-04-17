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
  // The list has no directed cycle along nxt, i.e., no node is
  // reachable from itself following one or more traversals along nxt.
  all n:DLL.header.*nxt | n !in n.^nxt
}

// Part (b)
pred UniqueElem() {
  // Unique nodes contain unique elements.
  #DLL.header.*nxt.elem = #Node
}

// Part (c)
pred Sorted() {
  // The list is sorted in ascending order (<=) along nxt.
  all n:Node {
    n.nxt.elem > n.elem
  }
}

// Part (d)
pred ConsistentPreAndNxt() {
  // For any node n1 and n2, if n1.nxt = n2, then n2.pre = n1; and vice versa.
  all n1:Node | all n2:Node | n1.nxt = n2 <=> n2.pre = n1
}

pred RepOk() {
  UniqueElem
  Sorted
  ConsistentPreAndNxt
}

//run RepOk for 3

assert repair_assert_1{
	Sorted <=>
	all n : Node | some n.nxt => n.elem <= n.nxt.elem
}
check repair_assert_1

pred repair_pred_1{
	Sorted and
	all n : Node | some n.nxt => n.elem <= n.nxt.elem
}
run repair_pred_1
