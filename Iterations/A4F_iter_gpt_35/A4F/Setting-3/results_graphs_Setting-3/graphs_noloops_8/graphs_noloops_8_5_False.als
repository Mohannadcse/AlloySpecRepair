sig Node { adj: set Node } pred noLoops { all a: Node | a not in a.adj } pred noLoopsOK { no (iden & adj) }