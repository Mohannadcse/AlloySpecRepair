sig Element {}

one sig Array {
    i2e: Int -> Element,
    length: Int
}

fact Reachable {
    Element = Array.i2e[Int]
}

fact InBound {
    all i: Int | i >= 0 and i < Array.length
    Array.length >= 0
}

pred NoConflict() {
    no disj idx, idx2: Int | idx in Array.i2e.Element and idx2 in Array.i2e.Element and idx = idx2
}

run NoConflict

assert repair_assert_1{
    NoConflict
    all i: Int | i >= 0 and i < Array.length
}

check repair_assert_1

pred repair_pred_1{
    NoConflict
    all i: Int | i >= 0 and i < Array.length
}

run repair_pred_1