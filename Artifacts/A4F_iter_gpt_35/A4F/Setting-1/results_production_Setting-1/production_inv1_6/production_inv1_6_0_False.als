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
    some c: Component | some c.parts
}
pred inv2 {
    all c: Component | c not in c.^parts
}
pred inv3 {
    all c: Component | c.cposition in Robot.rposition
}
pred inv4 {
    all c: Component | c.parts.cposition in c.cposition.*prev
}
run inv1 for 3