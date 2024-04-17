pred stonglyConnectedOK {
    all n:Node | Node in n.*adj
}
assert stonglyConnectedRepaired {
    stonglyConnected[]  iff stonglyConnectedOK[]
}