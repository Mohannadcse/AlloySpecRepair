open util/ordering[Position]
sig Position {}
sig Product {}
sig Component extends Product {parts : set Product, cposition : one Position}
sig Resource extends Product {}
sig Robot {rposition : one Position}
pred inv1 {all c:Component | some c.parts}
pred inv2 {all c:Component | c not in c.^parts}
pred inv3 {all c:Component | some r:Robot | r.rposition = c.cposition}
pred inv4 {all c:Component | c.parts.cposition in c.cposition.*prev}
pred inv1_OK {all c:Component | some c.parts}
assert inv1_Repaired {inv1[] iff inv1_OK[]}
pred inv2_OK {all c:Component | c not in c.^parts}
assert inv2_Repaired {inv2[] iff inv2_OK[]}
pred inv3_OK {Component.cposition in Robot.rposition}
assert inv3_Repaired {inv3[] iff inv3_OK[]}
pred inv4_OK {all c:Component | c.parts.cposition in c.cposition.*prev}
assert inv4_Repaired {inv4[] iff inv4_OK[]}
check inv1_Repaired expect 0
check inv2_Repaired expect 0
check inv3_Repaired expect 0
check inv4_Repaired expect 0
pred repair_pred_1{inv3[] iff inv3_OK[] }
run repair_pred_1
assert repair_assert_1{inv3[] iff inv3_OK[] }
check repair_assert_1