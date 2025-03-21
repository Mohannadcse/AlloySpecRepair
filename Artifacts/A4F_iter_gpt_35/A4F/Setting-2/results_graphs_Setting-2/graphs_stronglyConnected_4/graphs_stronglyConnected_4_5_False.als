sig Node {
    adj: set Node
}

pred undirected {
    adj = ~adj
}

pred oriented {
    no adj & ~adj
}

pred acyclic {
    all a: Node | a not in a.^adj
}

pred complete {
    all n: Node | n.adj = Node - n
}

pred noLoops {
    no iden & adj
}

pred weaklyConnected {
    all n: Node | n in n.*(adj + ~adj)
}

pred stronglyConnected {
    all n1, n2: Node | (n2 + n1) in n1.^adj
}

pred transitive {
    adj.adj in adj
}

assert undirectedRepaired {
    undirected[] iff undirectedOK[]
}

assert orientedRepaired {
    oriented[] iff orientedOK[]
}

assert acyclicRepaired {
    acyclic[] iff acyclicOK[]
}

assert completeRepaired {
    complete[] iff completeOK[]
}

assert noLoopsRepaired {
    noLoops[] iff noLoopsOK[]
}

assert weaklyConnectedRepaired {
    weaklyConnected[] iff weaklyConnectedOK[]
}

assert stronglyConnectedRepaired {
    stronglyConnected[] iff stronglyConnectedOK[]
}

assert transitiveRepaired {
    transitive[] iff transitiveOK[]
}

check undirectedRepaired expect 0
check orientedRepaired expect 0
check acyclicRepaired expect 0
check completeRepaired expect 0
check noLoopsRepaired expect 0
check weaklyConnectedRepaired expect 0
check stronglyConnectedRepaired expect 0
check transitiveRepaired expect 0