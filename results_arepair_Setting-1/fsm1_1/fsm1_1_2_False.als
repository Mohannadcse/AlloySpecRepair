one sig FSM {
  start: one State,
  stop: one State
}

sig State {
  transition: set State
}

// Part (a)
fact OneStartAndStop {
  // FSM only has one start state.
  all start1, start2 : FSM.start | start1 = start2

  // FSM only has one stop state.
  all stop1, stop2 : FSM.stop | stop1 = stop2

  // There is always a stop state.
  some FSM.stop
}

// Part (b)
fact ValidStartAndStop {
  // A state cannot be both a start state and a stop state.
  FSM.start != FSM.stop

  // No transition ends at the start state.
  all s : State | FSM.start !in s.transition

  // If no transition then stop state
  all s: State | s.transition = none => s = FSM.stop
}

// Part (c)
fact Reachability {
  // All states are reachable from the start state.
  all s: State | s in FSM.start.*transition

  // The stop state is reachable from any state.
  all s: State | FSM.stop in s.*transition or s = FSM.stop
}

//run {} for 5

assert repair_assert_1 {
  no FSM.stop.transition
}
check repair_assert_1

pred repair_pred_1 {
  no FSM.stop.transition
}
run repair_pred_1