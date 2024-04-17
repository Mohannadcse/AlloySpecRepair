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
    all c: Component | c.parts.cposition in c.cposition.*prev
}
assert inv1_Repaired {
    inv1[] iff inv1_OK[]
}
assert inv2_Repaired {
    inv2[] iff inv2_OK[]
}
assert inv3_Repaired {
    inv3[] iff inv3_OK[]
}
assert inv4_Repaired {
    inv4[] iff inv4_OK[]
}
check inv1_Repaired expect 0
check inv2_Repaired expect 0
check inv3_Repaired expect 0
check inv4_Repaired expect 0