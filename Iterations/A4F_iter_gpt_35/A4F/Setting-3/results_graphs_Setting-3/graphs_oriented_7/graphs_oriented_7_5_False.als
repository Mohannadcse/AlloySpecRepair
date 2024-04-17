sig Node { adj: set Node } pred undirected { adj = ~adj } pred oriented { all n: Node | no (n.adj & n.~adj) } pred acyclic { all a: Node | a not in a.^adj } pred complete { all n: Node | Node in n.adj } pred noLoops { no (iden & adj) } pred weaklyConnected { all n: Node | Node in n.*(adj+~adj) } pred stonglyConnected { all n: Node | Node in n.*adj } pred transitive { all n1, n2, n3: Node | (n1 -> n2) in adj and (n2 -> n3) in adj => (n1 -> n3) in adj }