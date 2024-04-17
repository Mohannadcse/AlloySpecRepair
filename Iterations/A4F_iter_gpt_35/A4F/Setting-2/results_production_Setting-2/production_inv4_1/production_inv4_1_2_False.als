open util/ordering[Position]
sig Position {}
sig Product {}
sig Component extends Product {
    parts: set Product,
    cposition: one Position
}
sig Resource extends Product {}
sig Robot {
    rposition: one Position
}
pred inv1 {
    all c: Component | some c.parts
}
pred inv2 {
    all c: Component | c not in c.^parts
}
pred inv3 {
    all c: Component | c.cposition in Robot.rposition
}
pred inv4 {
    all c: Component | all p: c.parts | p.cposition in c.cposition.*prev
}
run inv1 for 3
run inv2 for 3
run inv3 for 3
run inv4 for 3