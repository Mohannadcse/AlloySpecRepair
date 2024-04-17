/* Specification */
abstract sig Listing { }
sig Address extends Listing { }
sig Name extends Listing { }
sig Book {
	entry: set Name, // T1
	listed: entry ->set Listing // T2
}
fun lookup [b: Book, n: Name] : set Listing {n.^(b.listed)}
// constraints
// T. holeType constraints (multiplicity & range restriction)
// T1
// set
// T2
// A name entry maps to at most one name or address.
fact {all b:Book | all n:b.entry | lone b.listed[n] }
// F. fact constraints
// F1 All names reachable from any name entry in the book are themselves entries.
fact { all b:Book | all n,l:Name | l in lookup[b,n] implies l in b.entry }
// F2 Acyclic
fact { all b:Book | all n:b.entry | not n in lookup[b,n] }


/* Refinement Task */ 
// A. assertion (universal statement over constraints; in this case, C1)
assert repair_assert_1 {
	all b:Book | all n:b.entry | some (lookup[b,n]&Address)
}
check repair_assert_1 for exactly 1 Address, exactly 2 Name, exactly 1 Book
// P. problem (subset of the universal statement over constraints)
// some b:Book | some n:b.entry_in | no (lookup[b,n]&Addr)
//fact {all b:Book | all n:b.entry_in | some b.target_of[n]}

pred repair_pred_1 {
	all b:Book | all n:b.entry | some (lookup[b,n]&Address)
}
run repair_pred_1 for exactly 1 Address, exactly 2 Name, exactly 1 Book
