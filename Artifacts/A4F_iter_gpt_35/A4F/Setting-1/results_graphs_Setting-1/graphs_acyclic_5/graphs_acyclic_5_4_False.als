sig Node { adj : set Node } pred undirected { adj = ~adj } pred oriented { no adj & ~adj } pred acyclic { all n : Node | no n.*(~adj) & n } pred complete { all n:Node | n.adj = Node } pred noLoops { no (iden & adj) } pred weaklyConnected { all n:Node | n in n.*(adj+~adj) } pred stonglyConnected { all n:Node | n in n.*adj } pred transitive { adj.adj in adj }