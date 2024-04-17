//people
sig Person {
    member_of: some Group
}

pred CanEnter(p: Person, r: Room) {
    p.member_of in r.located_in
}

// groups
sig Group {}
one sig alas extends Group {}
one sig peds extends Group {}
one sig Group0 extends Group {}

//rooms
sig Room {
    located_in: set Group
}
one sig seclab extends Room {}

fact {
    alas in seclab.located_in and peds in seclab.located_in and Group0 in seclab.located_in
}

// assertion
assert repair_assert_1 {
    all p: Person | CanEnter[p, seclab] implies alas in p.member_of or peds in p.member_of or Group0 in p.member_of
}
check repair_assert_1

pred repair_pred_1 {
    all p: Person | CanEnter[p, seclab] implies alas in p.member_of or peds in p.member_of or Group0 in p.member_of
}
run repair_pred_1