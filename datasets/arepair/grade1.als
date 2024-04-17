abstract sig Person {}
sig Student extends Person {}
sig Professor extends Person {}
sig Class {
	assistant_for: set Student,   // as in : "is TA for"
	instructor_of: one Professor
}
sig Assignment {
	associated_with: one Class,
	assigned_to: some Student
}

pred PolicyAllowsGrading(s: Person, a: Assignment) {
	s in a.associated_with.assistant_for or s in a.associated_with.instructor_of
}

assert repair_assert_1 {
	all s : Person | all a: Assignment | PolicyAllowsGrading[s, a] implies not s in a.assigned_to
}

check repair_assert_1

pred repair_pred_1 {
	all s : Person | all a: Assignment | PolicyAllowsGrading[s, a] implies not s in a.assigned_to
}

run repair_pred_1
