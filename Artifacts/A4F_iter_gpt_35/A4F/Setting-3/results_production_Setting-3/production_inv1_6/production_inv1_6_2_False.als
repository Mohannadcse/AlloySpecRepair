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

assert inv1_correct {
	inv1
}
assert inv2_correct {
	inv2
}
assert inv3_correct {
	inv3
}
assert inv4_correct {
	inv4
}
check inv1_correct
check inv2_correct
check inv3_correct
check inv4_correct