sig Person { Tutors: set Person, Teaches: set Class } sig Group {} sig Class { Groups: Person -> Group } sig Teacher extends Person {} sig Student extends Person {} pred inv12 { all t : Teacher | some (t.Teaches).Groups } assert repair_assert_1 { inv12[] iff inv12_OK[] }