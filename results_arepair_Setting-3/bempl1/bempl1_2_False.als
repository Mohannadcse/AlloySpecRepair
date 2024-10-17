// rooms
sig Room {}
one sig secure_lab extends Room {}

// people
abstract sig Person {
  owns : set Key
}
sig Employee extends Person {}
sig Researcher extends Person {}

// access
sig Key {
  authorized: one Person,
  opened_by: one Room
} {
  opened_by = secure_lab implies authorized in Researcher
}

pred CanEnter(p: Person, r: Room) {
  some k: Key | k in p.owns and r = k.opened_by and p = k.authorized
}

// assertion
assert repair_assert_1 {
  all p : Person | CanEnter[p, secure_lab] implies p in Researcher
}
check repair_assert_1

pred repair_pred_1 {
  some opened_by
  some owns
  all p : Person | CanEnter[p, secure_lab] implies p in Researcher
}
run repair_pred_1