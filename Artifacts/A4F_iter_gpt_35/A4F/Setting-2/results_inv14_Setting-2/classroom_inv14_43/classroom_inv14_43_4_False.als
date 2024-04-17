/* The registered persons. */
sig Person {}
/* The registered groups. */
sig Group {}
/* The registered classes. */
sig Class {}
/* Some persons are teachers. */
sig Teacher in Person {}
/* Some persons are students. */
sig Student in Person {}
/* Each person tutors a set of persons. */
fun Tutors : Person -> set Person {}
/* Each person teaches a set of classes. */
fun Teaches : Person -> set Class {}
/* Each class has a set of persons assigned to a group. */
fun Groups : Class -> Person -> set Group {}
/* Every person is a student. */
pred inv1 {
    all p: Person | p in Student
}
/* There are no teachers. */
pred inv2 {
    no Teacher
}
/* No person is both a student and a teacher. */
pred inv3 {
    no Student & Teacher
}
/* No person is neither a student nor a teacher. */
pred inv4 {
    all p: Person | p in (Student + Teacher)
}
/* There are some classes assigned to teachers. */
pred inv5 {
    some t: Teacher | some t.Teaches
}
/* Every teacher has classes assigned. */
pred inv6 {
    all t: Teacher | some t.Teaches
}
/* Every class has teachers assigned. */
pred inv7 {
    all c: Class | some t: Teacher | t in c.Teaches
}
/* Teachers are assigned at most one class. */
pred inv8 {
    all t: Teacher | lone t.Teaches
}
/* No class has more than a teacher assigned. */
pred inv9 {
    all c: Class | lone t: Teacher | t in c.Teaches
}
/* For every class, every student has a group assigned. */
pred inv10 {
    all c: Class, s: Student | some g: Group | g in c.Groups[s]
}
/* A class only has groups if it has a teacher assigned. */
pred inv11 {
    all c: Class | (some g: Group | g in c.Groups) implies some t: Teacher | t in c.Teaches
}
/* Each teacher is responsible for some groups. */
pred inv12 {
    all t: Teacher | some g: Group | g in (t.Teaches).Groups
}
/* Only teachers tutor, and only students are tutored. */
pred inv13 {
    all p: Person | p in Teacher iff p.Tutors in Person and p in Student iff p.Teaches in Class
}
/* Every student in a class is at least tutored by all the teachers assigned to that class. */
pred inv14 {
    all c: Class, s: Student, t: Teacher | some g: Group | g in c.Groups[s] and g in c.Groups[t]
}
/* The tutoring chain of every person eventually reaches a Teacher. */
pred inv15 {
    all p: Person | some t: Teacher | t in ^Tutors.p
}
/* IFF PERFECT ORACLE */
pred inv1_OK {
    all p: Person | p in Student
}
assert inv1_Repaired {
    inv1[] iff inv1_OK[]
}
pred inv2_OK {
    no Teacher
}
assert inv2_Repaired {
    inv2[] iff inv2_OK[]
}
pred inv3_OK {
    no Student & Teacher
}
assert inv3_Repaired {
    inv3[] iff inv3_OK[]
}
pred inv4_OK {
    all p: Person | p in (Student + Teacher)
}
assert inv4_Repaired {
    inv4[] iff inv4_OK[]
}
pred inv5_OK {
    some t: Teacher | some t.Teaches
}
assert inv5_Repaired {
    inv5[] iff inv5_OK[]
}
pred inv6_OK {
    all t: Teacher | some t.Teaches
}
assert inv6_Repaired {
    inv6[] iff inv6_OK[]
}
pred inv7_OK {
    all c: Class | some t: Teacher | t in c.Teaches
}
assert inv7_Repaired {
    inv7[] iff inv7_OK[]
}
pred inv8_OK {
    all t: Teacher | lone t.Teaches
}
assert inv8_Repaired {
    inv8[] iff inv8_OK[]
}
pred inv9_OK {
    all c: Class | lone t: Teacher | t in c.Teaches
}
assert inv9_Repaired {
    inv9[] iff inv9_OK[]
}
pred inv10_OK {
    all c: Class, s: Student | some g: Group | g in c.Groups[s]
}
assert inv10_Repaired {
    inv10[] iff inv10_OK[]
}
pred inv11_OK {
    all c: Class | (some g: Group | g in c.Groups) implies some t: Teacher | t in c.Teaches
}
assert inv11_Repaired {
    inv11[] iff inv11_OK[]
}
pred inv12_OK {
    all t: Teacher | some g: Group | g in (t.Teaches).Groups
}
assert inv12_Repaired {
    inv12[] iff inv12_OK[]
}
pred inv13_OK {
    all p: Person | p in Teacher iff p.Tutors in Person and p in Student iff p.Teaches in Class
}
assert inv13_Repaired {
    inv13[] iff inv13_OK[]
}
pred inv14_OK {
    all c: Class, s: Student, t: Teacher | some g: Group | g in c.Groups[s] and g in c.Groups[t]
}
assert inv14_Repaired {
    inv14[] iff inv14_OK[]
}
pred inv15_OK {
    all p: Person | some t: Teacher | t in ^Tutors.p
}
assert inv15_Repaired {
    inv15[] iff inv15_OK[]
}
-
check inv1_Repaired expect 0
check inv2_Repaired expect 0
check inv3_Repaired expect 0
check inv4_Repaired expect 0
check inv5_Repaired expect 0
check inv6_Repaired expect 0
check inv7_Repaired expect 0
check inv8_Repaired expect 0
check inv9_Repaired expect 0
check inv10_Repaired expect 0
check inv11_Repaired expect 0
check inv12_Repaired expect 0
check inv13_Repaired expect 0
check inv14_Repaired expect 0
check inv15_Repaired expect 0
pred repair_pred_1{inv14[] iff inv14_OK[] }
run repair_pred_1
assert repair_assert_1{inv14[] iff inv14_OK[] }
check repair_assert_1