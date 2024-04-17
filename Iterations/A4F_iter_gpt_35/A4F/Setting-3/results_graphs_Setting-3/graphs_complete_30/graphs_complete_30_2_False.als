sig Node { adj : set Node }
pred undirected { adj = ~adj }
pred oriented { no adj & ~adj }
pred acyclic { all a:Node | a not in a.^adj }
pred complete { Node in Node.^adj }
pred noLoops { no (iden & adj) }
pred weaklyConnected { all n:Node | Node in n.*(adj+~adj) }
pred stronglyConnected { all n:Node | Node in n.*(adj+~adj) }
pred transitive { adj in adj.adj }
assert undirectedRepaired { undirected[] iff undirectedOK[] }
assert orientedRepaired { oriented[] iff orientedOK[] }
assert acyclicRepaired { acyclic[] iff acyclicOK[] }
assert completeRepaired { complete[] iff completeOK[] }
assert noLoopsRepaired { noLoops[] iff noLoopsOK[] }
assert weaklyConnectedRepaired { weaklyConnected[] iff weaklyConnectedOK[] }
assert stronglyConnectedRepaired { stronglyConnected[] iff stronglyConnectedOK[] }
assert transitiveRepaired { transitive[] iff transitiveOK[] }