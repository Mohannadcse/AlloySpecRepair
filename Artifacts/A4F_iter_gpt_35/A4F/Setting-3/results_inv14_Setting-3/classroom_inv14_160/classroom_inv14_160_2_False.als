/* The registered persons. */
sig Person {}
/* The registered groups. */
sig Group {}
/* The registered classes. */
sig Class {}
/* Some persons are teachers. */
sig Teacher extends Person {}
/* Some persons are students. */
sig Student extends Person {}
/* Each person tutors a set of persons. */
sig Person  {
Tutors : set Person,
Teaches : set Class
}
/* Each class has a set of persons assigned to a group. */
sig Class  {
Groups : Person -> Group
}
pred inv14 {
all s : Person, c : Class, t : Person, g : Group | (c -> s -> g in Groups) and t -> c in Teaches implies t -> s in Tutors
}