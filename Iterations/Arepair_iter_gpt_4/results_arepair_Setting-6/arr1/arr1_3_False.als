sig Element {}

one sig Array {
    // Maps indexes to elements of Element.
    i2e: Int -> Element,
    // Represents the length of the array.
    length: Int
}

// Assume all elements are in the array.
fact Reachable {
    all i: Int | i >= 0 and i < Array.length implies i -> Element in Array.i2e
}

fact InBound {
    // All indexes should be greater than or equal to 0 and less than the array length.
    all i: Int | i >= 0 and i < Array.length
    // Array length should be greater than or equal to 0.
    Array.length >= 0
}

pred NoConflict() {
    // Each index maps to at most one element.
    all idx: Int | idx >= 0 and idx < Array.length implies lone idx -> Array.i2e[idx]
}

run NoConflict

assert repair_assert_1{
    NoConflict
    all i: Int | i >= 0 and i < Array.length implies i -> Element in Array.i2e
}

check repair_assert_1

pred repair_pred_1{
    NoConflict
    all i: Int | i >= 0 and i < Array.length implies i -> Element in Array.i2e
}

run repair_pred_1