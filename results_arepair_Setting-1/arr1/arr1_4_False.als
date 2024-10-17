sig Element {}

one sig Array {
  // Maps indexes to elements of Element.
  i2e: Int -> lone Element,
  // Represents the length of the array.
  length: Int
}

fact Reachable {
  Element = Array.i2e[Int]
}

fact InBound {
  // All indexes should be greater than or equal to 0 and less than the array length.
  all i: Int | (i >= 0 and i < Array.length)
  // Array length should be greater than or equal to 0.
  Array.length >= 0
}

pred NoConflict() {
  // Each index maps to at most one element.
  all idx: Int | lone Array.i2e[idx]
}

run NoConflict

assert repair_assert_1 {
  NoConflict
  all i: Int | (i >= 0 and i < Array.length)
}

check repair_assert_1

pred repair_pred_1 {
  NoConflict
  all i: Int | (i >= 0 and i < Array.length)
}

run repair_pred_1