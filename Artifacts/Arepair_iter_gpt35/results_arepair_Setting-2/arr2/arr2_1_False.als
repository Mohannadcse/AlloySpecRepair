sig Element {}

one sig Array {
i2e: Int -> Element,
length: Int
}

fact Reachable {
Element = Array.i2e[Int]
}

pred InBound {
all i:Array.i2e.Element | i >= 0
all i:Array.i2e.Element | i < Array.length
Array.length >= 0
}

fact NoConflict {
all i:Array.i2e.Element | #Array.i2e[i] = 1
}

assert repair_assert_1{
InBound <=> {
all i:Array.i2e.Element | i >= 0
all i:Array.i2e.Element | i < Array.length
Array.length >= 0
}
}
check repair_assert_1

pred repair_pred_1{
InBound and {
all i:Array.i2e.Element | i >= 0
all i:Array.i2e.Element | i < Array.length
Array.length >= 0
}
}
run repair_pred_1