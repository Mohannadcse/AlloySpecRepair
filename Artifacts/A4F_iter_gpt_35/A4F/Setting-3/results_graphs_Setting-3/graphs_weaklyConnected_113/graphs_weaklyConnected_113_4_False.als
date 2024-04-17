sig Node { adj : set Node }

sig Node {}

pred weaklyConnected { all x : Node | Node in x.adj + adj.x + x }

run { #Node = 5 }
check weaklyConnected for 5