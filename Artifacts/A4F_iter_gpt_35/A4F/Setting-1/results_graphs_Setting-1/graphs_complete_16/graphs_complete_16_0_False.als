sig Node { adj : set Node }

pred undirected { adj = ~adj }

pred oriented { no adj & ~adj }

pred acyclic { all a:Node | a not in a.^adj }

pred complete { all n : Node | Node - n in n.adj }

pred noLoops { no (iden & adj) }

pred weaklyConnected { all n:Node | Node in n.*(adj+~adj) }

pred stonglyConnected { all n:Node | Node in n.*adj }

pred transitive { adj.adj in adj }

pred undirectedOK { adj = ~adj }

pred orientedOK { no adj & ~adj }

pred acyclicOK { all a:Node | a not in a.^adj }

pred completeOK { all n:Node | Node in n.adj }

pred noLoopsOK { no (iden & adj) }

pred weaklyConnectedOK { all n:Node | Node in n.*(adj+~adj) }

pred stonglyConnectedOK { all n:Node | Node in n.*adj }

pred transitiveOK { adj.adj in adj }

assert undirectedRepaired { undirected[] iff undirectedOK[] }

assert orientedRepaired { oriented[] iff orientedOK[] }

assert acyclicRepaired { acyclic[] iff acyclicOK[] }

assert completeRepaired { complete[] iff completeOK[] }

assert noLoopsRepaired { noLoops[] iff noLoopsOK[] }

assert weaklyConnectedRepaired { weaklyConnected[] iff weaklyConnectedOK[] }

assert stonglyConnectedRepaired { stonglyConnected[] iff stonglyConnectedOK[] }

assert transitiveRepaired { transitive[] iff transitiveOK[] }

check undirectedRepaired expect 0
check orientedRepaired expect 0
check acyclicRepaired expect 0
check completeRepaired expect 0
check noLoopsRepaired expect 0
check weaklyConnectedRepaired expect 0
check stonglyConnectedRepaired expect 0
check transitiveRepaired expect 0
pred repair_pred_1{complete[] iff completeOK[] }
run repair_pred_1
assert repair_assert_1{complete[] iff completeOK[] }
check repair_assert_1