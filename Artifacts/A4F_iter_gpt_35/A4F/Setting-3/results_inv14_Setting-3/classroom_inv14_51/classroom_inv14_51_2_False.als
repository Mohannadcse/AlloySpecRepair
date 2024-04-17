/* The registered persons. */
sig Person  {
/* Each person tutors a set of persons. */
Tutors : set Person,
/* Each person teaches a set of classes. */
Teaches : set Class
}
/* The registered groups. */
sig Group {}
/* The registered classes. */
sig Class  {
/* Each class has a set of persons assigned to a group. */
Groups : Person -> Group
}
/* Some persons are teachers. */
sig Teacher extends Person  {}
/* Some persons are students. */
sig Student extends Person  {}
/* Every person is a student. */
fact inv1 {
Person in Student
}
/* There are no teachers. */
fact inv2 {
no Teacher
}
/* No person is both a student and a teacher. */
fact inv3 {
no Student & Teacher
}
/* No person is neither a student nor a teacher. */
fact inv4 {
Person in (Student + Teacher)
}
/* There are some classes assigned to teachers. */
fact inv5 {
some Teacher.Teaches
}
/* Every teacher has classes assigned. */
fact inv6 {
Teacher in Teaches.Class
}
/* Every class has teachers assigned. */
fact inv7 {
Class in Teacher.Teaches
}
/* Teachers are assigned at most one class. */
fact inv8 {
all t:Teacher | lone t.Teaches
}
/* No class has more than a teacher assigned. */
fact inv9 {
all c:Class | lone Teaches.c & Teacher
}
/* For every class, every student has a group assigned. */
fact inv10 {
all c:Class, s:Student | some s.(c.Groups)
}
/* A class only has groups if it has a teacher assigned. */
fact inv11 {
all c : Class | (some c.Groups) implies some Teacher & Teaches.c
}
/* Each teacher is responsible for some groups. */
fact inv12 {
all t : Teacher | some (t.Teaches).Groups
}
/* Only teachers tutor, and only students are tutored. */
fact inv13 {
Tutors.Person in Teacher and Person.Tutors in Student
}
/* Every student in a class is at least tutored by all the teachers
* assigned to that class. */
fact inv14 {
all p : Person | some c : Class, g : Group | c->p->g in Groups implies some q : Person | q->c in Teaches
}
/* The tutoring chain of every person eventually reaches a Teacher. */
fact inv15 {
all s : Person | some Teacher & ^Tutors.s
}
/*======== IFF PERFECT ORACLE ===============*/
fact inv1_OK {
Person in Student
}
check inv1_OK expect 0
fact inv2_OK {
no Teacher
}
check inv2_OK expect 0
fact inv3_OK {
no Student & Teacher
}
check inv3_OK expect 0
fact inv4_OK {
Person in (Student + Teacher)
}
check inv4_OK expect 0
fact inv5_OK {
some Teacher.Teaches
}
check inv5_OK expect 0
fact inv6_OK {
Teacher in Teaches.Class
}
check inv6_OK expect 0
fact inv7_OK {
Class in Teacher.Teaches
}
check inv7_OK expect 0
fact inv8_OK {
all t:Teacher | lone t.Teaches
}
check inv8_OK expect 0
fact inv9_OK {
all c:Class | lone Teaches.c & Teacher
}
check inv9_OK expect 0
fact inv10_OK {
all c:Class, s:Student | some s.(c.Groups)
}
check inv10_OK expect 0
fact inv11_OK {
all c : Class | (some c.Groups) implies some Teacher & Teaches.c
}
check inv11_OK expect 0
fact inv12_OK {
all t : Teacher | some (t.Teaches).Groups
}
check inv12_OK expect 0
fact inv13_OK {
Tutors.Person in Teacher and Person.Tutors in Student
}
check inv13_OK expect 0
fact inv14_OK {
all s : Person, c : Class, t : Person, g : Group | (c -> s -> g in Groups) and t -> c in Teaches implies t -> s in Tutors
}
check inv14_OK expect 0
fact inv15_OK {
all s : Person | some Teacher & ^Tutors.s
}
check inv15_OK expect 0
