one sig FSM {
start: one State,
stop: lone State
}

sig State {
transition: set State
}

// Part (a)
fact OneStartAndStop {
// FSM only has one start state.
// FSM only has one stop state.
// DO YOU WANT TO ENFORCE THAT THERE IS ALWAYS A STOP STATE?
some FSM.stop
// Note: It's fine if the student does not state "one FSM.start" because it is implied.
}

// Part (b)
fact ValidStartAndStop {
// A state cannot be both a start state and a stop state.
FSM.start !in FSM.stop

// No transition ends at the start state.
all s : State | FSM.start !in s.transition
// MV: If no transition then stop state
all s: State | s.transition = none => s in FSM.stop
}

// Part (c)
fact Reachability {
// All states are reachable from the start state.
State = FSM.start.*transition

// The stop state is reachable from any state.
all s: State | FSM.stop in s.*transition
}

//run {} for 5

assert repair_assert_1{
no FSM.stop.transition
}
check repair_assert_1

pred repair_pred_1{
no FSM.stop.transition
}
run repair_pred_1