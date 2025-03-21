 /* A labeled transition system (LTS) is comprised by States, a sub-set of which are Initial, connected by transitions, here represented by Events. */ sig State { trans: Event -> State } sig Init in State {} sig Event {}
/* The LTS does not contain deadlocks, ie, each state has at least a transition. */ pred inv1 { all s: State | some s.trans }
/* There is a single initial state. */ pred inv2 { one s: State | s in Init }
/* The LTS is deterministic, ie, each state has at most a transition for each event. */ pred inv3 { all s: State, e: Event | lone e.(s.trans) }
/* All states are reachable from an initial state. */ pred inv4 { all x: Init | State in Event.*(x.trans) + x }
/* All the states have the same events available. */ pred inv5 { all s, s': State | s.trans.State = s'.trans.State }
/* Each event is available in at least one state. */ pred inv6 { all e: Event | some s, s': State | s.trans[e] = s' }
/* The LTS is reversible, ie, from a reachable state it is always possible to return to an initial state. */ pred inv7 { let tr = {s1, s2: State, e: Event | s1.trans[e] = s2} | all s: Init.^tr | some i: Init | i in s.^tr }
/*======== IFF PERFECT ORACLE ===============*/ pred inv1_OK { all s: State | some s.trans } assert inv1_Repaired { inv1[] iff inv1_OK[] }
pred inv2_OK { one s: State | s in Init } assert inv2_Repaired { inv2[] iff inv2_OK[] }
pred inv3_OK { all s: State, e: Event | lone e.(s.trans) } assert inv3_Repaired { inv3[] iff inv3_OK[] }
pred inv4_OK { let tr = {s1, s2: State, e: Event | s1.trans[e] = s2} | State in Init.^tr } assert inv4_Repaired { inv4[] iff inv4_OK[] }
pred inv5_OK { all s, s': State | s.trans.State = s'.trans.State } assert inv5_Repaired { inv5[] iff inv5_OK[] }
pred inv6_OK { all e: Event | some s, s': State | s.trans[e] = s' } assert inv6_Repaired { inv6[] iff inv6_OK[] }
pred inv7_OK { let tr = {s1, s2: State, e: Event | s1.trans[e] = s2} | all s: Init.^tr | some i: Init | i in s.^tr } assert inv7_Repaired { inv7[] iff inv7_OK[] }
check inv1_Repaired expect 0 check inv2_Repaired expect 0 check inv3_Repaired expect 0 check inv4_Repaired expect 0 check inv5_Repaired expect 0 check inv6_Repaired expect 0 check inv7_Repaired expect 0 