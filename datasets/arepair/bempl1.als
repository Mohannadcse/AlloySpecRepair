///*
//Further simplification of Dan's work
//access is granted to all assigned groups.
//problem: employee can grant a key to themselves, not just researchers
//*/

//rooms
sig Room {}
one sig secure_lab extends Room {}

//people
abstract sig Person {
  owns : set Key
}
sig Employee extends Person {}
sig Researcher extends Person {}

// access
sig Key {
  authorized: one Employee,
  opened_by: one Room
}

pred CanEnter(p: Person, r:Room) {
	r in p.owns.opened_by
}

// assertion
assert repair_assert_1 {
  all p : Person | CanEnter[p, secure_lab] implies p in Researcher
}
check repair_assert_1

pred repair_pred_1{
 some opened_by
 some owns
 all p : Person | CanEnter[p, secure_lab] implies p in Researcher
}
run repair_pred_1