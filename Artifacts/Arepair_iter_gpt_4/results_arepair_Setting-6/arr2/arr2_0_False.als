sig Element {}

one sig Array {
    // Maps indexes to elements of Element.
    i2e: Int -> Element,
    // Represents the length of the array.
    length: Int
}

// Assume all objects are in the array.
fact Reachable {
    Element = Array.i2e[Int]
}


pred InBound {
    // All indexes should be greater than or equal to 0
    // and less than the array length
    all i: Int | i in Array.i2e.Int => (i >= 0 and i < Array.length)

    // Array length should be greater than equal to 0,
    // but also since there is a one-to-one mapping from
    // index to element, we restrict the array length to the
    // number of elements.
    Array.length = #Element
}

fact NoConflict {
    // Each index maps to at most on element
    all i: Int | i in Array.i2e.Int => #Array.i2e[i] = 1
}

run InBound for 3

assert repair_assert_1{
    InBound <=> {
        all i: Int | i in Array.i2e.Int => (i >= 0 and i < Array.length)
        Array.length >= 0
        Array.length = #Element
    }
}
check repair_assert_1 for 3

pred repair_pred_1{
    InBound and {
        all i: Int | i in Array.i2e.Int => (i >= 0 and i < Array.length)
        Array.length >= 0
    }
}
run repair_pred_1 for 3