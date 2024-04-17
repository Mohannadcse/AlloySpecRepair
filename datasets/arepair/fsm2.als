one sig FSM {
  start: set State,
  stop: set State
}

sig State {
  transition: set State
}

// Part (a)
fact OneStartAndStop {
  // FSM only has one start state.
  #FSM.start = 1
  // FSM only has one stop state.
  #FSM.stop = 1
}

// Part (b)
fact ValidStartAndStop {
  // A state cannot be both a start state and a stop state.
  FSM.start != FSM.stop
  // No transition ends at the start state.
  all s:State | FSM.start != s.transition
  // No transition begins at the stop state.
  no FSM.stop.transition
}

// Part (c)
fact Reachability {
  // All states are reachable from the start state.
  State = FSM.start.*transition
  // The stop state is reachable from any state.
  all s:(State - FSM.stop) | FSM.stop in s.*transition
}

//run {} for 5
assert repair_assert_1{
	all s: State | FSM.start !in s.transition
}
check repair_assert_1

pred repair_pred_1{
	all s: State | FSM.start !in s.transition
}
run repair_pred_1
