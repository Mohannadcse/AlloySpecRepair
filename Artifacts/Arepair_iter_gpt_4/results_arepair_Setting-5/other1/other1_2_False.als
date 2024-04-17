//people
sig Person {
    member_of : some Group
}
pred CanEnter(p: Person, r:Room) {
    p.member_of in r.located_in
}

// groups
sig Group {}
one sig alas extends Group {}
one sig peds extends Group {}

//rooms
sig Room {
    located_in: set Group
}
one sig seclab extends Room {}
// the problem; this permits, but doesn't restrict
fact {
    seclab.located_in = alas + peds
}

// assertion
assert repair_assert_1 {
    all p : Person | CanEnter[p, seclab] implies p.member_of = alas or p.member_of = peds
}
check repair_assert_1

pred repair_pred_1{
    all p : Person | CanEnter[p, seclab] implies p.member_of = alas or p.member_of = peds
}
run repair_pred_1