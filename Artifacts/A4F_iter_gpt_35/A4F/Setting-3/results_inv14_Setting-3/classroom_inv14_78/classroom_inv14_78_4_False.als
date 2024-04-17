/* Fixed Alloy specifications */
sig Person {}
sig Group {}
sig Class { Groups: Person -> Group }
sig Teacher extends Person {}
sig Student extends Person {}

pred inv14_OK {
all s : Person, c : Class, t : Person, g : Group | (c -> s -> g in Groups) and t -> c in Teaches implies t -> s in Tutors
}

run inv14_OK for 5