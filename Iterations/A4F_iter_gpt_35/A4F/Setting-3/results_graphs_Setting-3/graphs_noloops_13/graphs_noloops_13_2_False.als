sig Node { adj : set Node }

pred undirected { adj = ~adj }

pred oriented { no adj & ~adj }

pred acyclic { all a:Node | a not in a.^adj }

pred complete { Node = adj }

pred noLoops { no adj + iden }

pred weaklyConnected { all n:Node | Node in n.*(adj+~adj) }

pred stronglyConnected { all n:Node | all m:Node | n in m.*adj or m in n.*adj }

pred transitive { adj.adj in adj }

assert completeRepaired { complete }

assert stronglyConnectedRepaired { stronglyConnected }

check completeRepaired expect 0
check stronglyConnectedRepaired expect 0