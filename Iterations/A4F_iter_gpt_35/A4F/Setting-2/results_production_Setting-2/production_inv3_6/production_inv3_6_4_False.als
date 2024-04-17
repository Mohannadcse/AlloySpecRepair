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
pred inv1 { all c:Component | some c.parts }
pred inv2 { all c:Component | c not in c.^parts }
pred inv3 { all c:Component, r:Robot | c.cposition = r.rposition }
pred inv4 { all c:Component | c.parts.cposition in c.cposition.*prev }
pred inv3_OK { Component.cposition in Robot.rposition }
assert inv3_Repaired { inv3[] iff inv3_OK[] }
run inv3_Repaired