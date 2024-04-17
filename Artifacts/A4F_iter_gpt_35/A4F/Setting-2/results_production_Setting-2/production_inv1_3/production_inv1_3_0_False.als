open util/ordering[Position]
sig Position {}
sig Product {}
sig Component extends Product {
    parts : set Product,
    cposition : one Position
}
sig Resource extends Product {}
sig Robot {
    rposition : one Position
}
pred inv1 { // A component requires at least one part
    all c:Component | some c.parts
}
pred inv2 { // A component cannot be a part of itself
    all c:Component | c not in c.^parts
}
pred inv3 { // The position where a component is assembled must have at least one robot
    all c:Component | some r:Robot | r.rposition = c.cposition
}
pred inv4 { // The parts required by a component cannot be assembled in a later position
    all c:Component, p:Product | p in c.parts implies p.cposition in c.cposition.*prev
}
pred inv1_OK {
    all c:Component | some c.parts
}
assert inv1_Repaired {
    inv1[] iff inv1_OK[]
}
pred inv2_OK {
    all c:Component | c not in c.^parts
}
assert inv2_Repaired {
    inv2[] iff inv2_OK[]
}
pred inv3_OK {
    all c:Component | some r:Robot | r.rposition = c.cposition
}
assert inv3_Repaired {
    inv3[] iff inv3_OK[]
}
pred inv4_OK {
    all c:Component, p:Product | p in c.parts implies p.cposition in c.cposition.*prev
}
assert inv4_Repaired {
    inv4[] iff inv4_OK[]
}
check inv1_Repaired expect 0
check inv2_Repaired expect 0
check inv3_Repaired expect 0
check inv4_Repaired expect 0