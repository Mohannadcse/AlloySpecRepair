sig Person { Tutors: set Person, Teaches: set Class } sig Group {} sig Class { Groups: Person -> Group } sig Teacher extends Person {} sig Student extends Person {} pred inv13_OK { Tutors.Person in Teacher and Person.Tutors in Student } assert inv13_Repaired { inv13[] iff inv13_OK[] }