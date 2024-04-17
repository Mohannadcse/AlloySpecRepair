pred inv15_OK {
no s : Student | some Teacher & ^Tutors.s
}
assert inv15_Repaired {
inv15[] = inv15_OK[]
}