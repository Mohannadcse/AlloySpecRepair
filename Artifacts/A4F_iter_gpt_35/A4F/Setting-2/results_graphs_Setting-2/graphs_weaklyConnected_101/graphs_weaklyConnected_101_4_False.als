/*This file was automatically generated by AUnit v1.0's coverage-based test generation feature.
Test Suite Details:
----------
Tests generated over: GRAPHS_templateAllCorrect.als
Number Valuations: 8
Number Tests: 38
Scope used: 5*/
/*
Each node has a set of outgoing edges, representing a directed graph without multiple edges.
*/
sig Node {
    adj: set Node
}
/*
The graph is undirected, i.e., edges are symmetric.
http://mathworld.wolfram.com/UndirectedGraph.html
*/
pred undirected {
    adj = ~adj
}
/*
The graph is oriented, i.e., contains no symmetric edges.
http://mathworld.wolfram.com/OrientedGraph.html
*/
pred oriented {
    no adj & ~adj
}
/*
The graph is acyclic, i.e., contains no directed cycles.
http://mathworld.wolfram.com/AcyclicDigraph.html
*/
pred acyclic {
    all a: Node | a not in a.^adj
}
/*
The graph is complete, i.e., every node is connected to every other node.
http://mathworld.wolfram.com/CompleteDigraph.html
*/
pred complete {
    all n: Node | n in n.adj
}
/*
The graph contains no loops, i.e., nodes have no transitions to themselves.
http://mathworld.wolfram.com/GraphLoop.html
*/
pred noLoops {
    no (iden & adj)
}
/*
The graph is weakly connected, i.e., it is possible to reach every node from every node ignoring edge direction.
http://mathworld.wolfram.com/WeaklyConnectedDigraph.html
*/
pred weaklyConnected {
    all x: Node | Node in x.^adj + ^adj.x
}
/*
The graph is strongly connected, i.e., it is possible to reach every node from every node considering edge direction.
http://mathworld.wolfram.com/StronglyConnectedDigraph.html
*/
pred stronglyConnected {
    all n: Node | Node in n.*adj
}
/*
The graph is transitive, i.e., if two nodes are connected through a third node, they are also connected directly.
http://mathworld.wolfram.com/TransitiveDigraph.html
*/
pred transitive {
    adj.adj in adj
}

run {} for 5