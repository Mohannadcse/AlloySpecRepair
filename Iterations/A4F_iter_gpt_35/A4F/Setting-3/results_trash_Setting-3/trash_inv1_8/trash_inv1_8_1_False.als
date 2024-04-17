/* The set of files in the file system. */
sig File {
/* A file is potentially a link to other files. */
link : set File
}
/* The set of files in the trash. */
sig Trash extends File {}
/* The set of protected files. */
sig Protected extends File {}
/* The trash is empty. */
pred inv1 {
no Trash  all f:File | f in Trash
}
/* All files are deleted. */
pred inv2 {
File in Trash
}
/* Some file is deleted. */
pred inv3 {
some Trash
}
/* Protected files cannot be deleted. */
pred inv4 {
no Protected & Trash
}
/* All unprotected files are deleted.. */
pred inv5 {
File - Protected in Trash
}
/* A file links to at most one file. */
pred inv6 {
~link . link in iden
}
/* There is no deleted link. */
pred inv7 {
no link.Trash
}
/* There are no links. */
pred inv8 {
no link
}
/* A link does not link to another link. */
pred inv9 {
no link.link
}
/* If a link is deleted, so is the file it links to. */
pred inv10 {
Trash.link in Trash
}
/*======== IFF PERFECT ORACLE ===============*/
pred inv1_OK {
no Trash
}
assert inv1_Repaired {
no Trash
}
---------
pred inv2_OK {
File in Trash
}
assert inv2_Repaired {
File in Trash
}
--------
pred inv3_OK {
some Trash
}
assert inv3_Repaired {
some Trash
}
--------
pred inv4_OK {
no Protected & Trash
}
assert inv4_Repaired {
no Protected & Trash
}
--------
pred inv5_OK {
File - Protected in Trash
}
assert inv5_Repaired {
File - Protected in Trash
}
--------
pred inv6_OK {
~link . link in iden
}
assert inv6_Repaired {
~link . link in iden
}
--------
pred inv7_OK {
no link.Trash
}
assert inv7_Repaired {
no link.Trash
}
--------
pred inv8_OK {
no link
}
assert inv8_Repaired {
no link
}
--------
pred inv9_OK {
no link.link
}
assert inv9_Repaired {
no link.link
}
--------
pred inv10_OK {
Trash.link in Trash
}
assert inv10_Repaired {
Trash.link in Trash
}
-- PerfectOracleCommands
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
pred repair_pred_1{inv1[] iff inv1_OK[] }
run repair_pred_1
assert repair_assert_1{inv1[] iff inv1_OK[] }
check repair_assert_1