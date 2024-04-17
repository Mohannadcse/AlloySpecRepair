pred inv14_OK {
all s : Student, c : Class | some t : Teacher | t->s in Tutors implies s in Class and t in Teacher
}
assert inv14_Repaired {
inv14[] iff inv14_OK[]
}