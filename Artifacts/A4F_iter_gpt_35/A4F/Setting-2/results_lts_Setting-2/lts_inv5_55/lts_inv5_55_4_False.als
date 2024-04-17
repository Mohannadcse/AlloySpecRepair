 sig State { trans : Event -> State } sig Init in State {} sig Event {}
pred inv1 { all s: State | some s.trans }
pred inv2 { one Init }
pred inv3 { all s : State, e : Event | lone e.(s.trans) }
pred inv4 { let tr = { s1, s2 : State | some e : Event | s1->e->s2 in trans } | State in Init.^tr }
pred inv5 { all s:State, s1:State | s.trans.State = s1.trans.State }
pred inv6 { all e:Event | some s1,s2:State | s1->e->s2 in trans }
pred inv7 { let tr = { s1, s2 : State | some e : Event | s1->e->s2 in trans } | all s : Init.^tr | some i : Init | i in s.^tr }
assert inv1_Repaired { inv1[] iff all s: State | some s.trans }
assert inv2_Repaired { inv2[] iff one Init }
assert inv3_Repaired { inv3[] iff all s : State, e : Event | lone e.(s.trans) }
assert inv4_Repaired { inv4[] iff let tr = { s1, s2 : State | some e : Event | s1->e->s2 in trans } | State in Init.^tr }
assert inv5_Repaired { inv5[] iff all s:State, s1:State | s.trans.State = s1.trans.State }
assert inv6_Repaired { inv6[] iff all e:Event | some s1,s2:State | s1->e->s2 in trans }
assert inv7_Repaired { inv7[] iff let tr = { s1, s2 : State | some e : Event | s1->e->s2 in trans } | all s : Init.^tr | some i : Init | i in s.^tr }
check inv1_Repaired expect 0 check inv2_Repaired expect 0 check inv3_Repaired expect 0 check inv4_Repaired expect 0 check inv5_Repaired expect 0 check inv6_Repaired expect 0 check inv7_Repaired expect 0 