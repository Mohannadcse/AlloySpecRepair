sig State { trans : Event -> State } sig Init in State {} sig Event {} pred inv1 { all s:State | some trans } pred inv1_OK { all s: State | some s.trans } assert inv1_Repaired { inv1[] iff inv1_OK[] } pred repair_pred_1 { inv1[] iff inv1_OK[] } assert repair_assert_1 { inv1[] iff inv1_OK[] }