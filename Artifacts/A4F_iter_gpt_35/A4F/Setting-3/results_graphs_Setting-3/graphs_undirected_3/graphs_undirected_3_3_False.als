sig Node { adj : set Node }

pred undirected {
    all a,b:Node | a->b in adj implies b->a not in adj
}

run undirected