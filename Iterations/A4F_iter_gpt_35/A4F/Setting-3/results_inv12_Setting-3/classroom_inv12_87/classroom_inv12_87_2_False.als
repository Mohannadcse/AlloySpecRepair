pred inv12_OK {
all t : Teacher | some (t.Teaches).Groups
}
assert repair_assert_1{inv12[] iff inv12_OK[] }