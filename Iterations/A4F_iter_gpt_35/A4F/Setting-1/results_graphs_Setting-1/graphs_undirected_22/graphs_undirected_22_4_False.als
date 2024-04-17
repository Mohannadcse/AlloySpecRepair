/* Fixed specification */
sig Node {
    adj: set Node
}

pred undirected {
    all n: Node | n.adj = ~n.adj
}

pred oriented {
    no adj & ~adj
}

pred acyclic {
    no iden & adj.^adj
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
    all n: Node | n in n.*adj
}

pred transitive {
    adj.adj in adj
}

run {}
