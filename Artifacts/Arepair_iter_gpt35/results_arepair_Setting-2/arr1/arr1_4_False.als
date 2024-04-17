sig Element {}
one sig Array {
i2e: Int -> Element,
length: Int
}
fact Reachable {
Element = Array.i2e[Int]
}
fact InBound {
all i: Array.i2e.Element | i>=0 and i<Array.length
Array.length>=0
}
pred NoConflict() {
all idx: Array.i2e.Element | lone Array.i2e[idx]
}
run NoConflict

assert repair_assert_1{
NoConflict
all i: Array.i2e.Element | i>=0 and i<Array.length
}
check repair_assert_1

pred repair_pred_1{
NoConflict
all i: Array.i2e.Element | i>=0 and i<Array.length
}
run repair_pred_1