sig Node { adj : set Node } pred weaklyConnectedOK { all n:Node | Node in (n.adj + ~n.adj)^n.adj } assert weaklyConnectedRepaired { weaklyConnected[] iff weaklyConnectedOK[] }