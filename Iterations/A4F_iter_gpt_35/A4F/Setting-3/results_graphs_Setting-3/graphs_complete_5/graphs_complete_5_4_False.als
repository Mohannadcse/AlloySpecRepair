sig Node { adj : set Node } pred undirected { adj = ~adj } pred oriented { no adj & ~adj } pred acyclic { all a:Node | a not in a.^adj } pred complete { all a : Node | a in a.*(adj+~adj) } pred noLoops { no (iden & adj) } pred weaklyConnected { all n:Node | Node in n.*(adj+~adj) } pred stronglyConnected { all n:Node | n in n.*(adj+~adj) }