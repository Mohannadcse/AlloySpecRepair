sig Node { adj : set Node } pred weaklyConnected { all n:Node | Node in (n+ n.adj + adj.n).*adj } pred weaklyConnectedOK { all n:Node | Node in n.*(adj+~adj) } pred repair_pred_1{weaklyConnected[] iff weaklyConnectedOK[] } run repair_pred_1