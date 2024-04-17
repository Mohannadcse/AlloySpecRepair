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
	no Trash 
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
 
 all f : File | some f : Protected | f not in Trash 
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
    inv1[] iff inv1_OK[]
}
---------
pred inv2_OK {
	File in Trash 
}
assert inv2_Repaired {
    inv2[] iff inv2_OK[]
}
--------
pred inv3_OK {
		some Trash 
}
assert inv3_Repaired {
    inv3[] iff inv3_OK[]
}
--------
pred inv4_OK {
  	no Protected & Trash  
}
assert inv4_Repaired {
    inv4[] iff inv4_OK[]
}
--------
pred inv5_OK {
  	File - Protected in Trash  
}
assert inv5_Repaired {
    inv5[] iff inv5_OK[]
}
--------
pred inv6_OK {
  ~link . link in iden  
}
assert inv6_Repaired {
    inv6[] iff inv6_OK[]
}
--------
pred inv7_OK {
 no link.Trash  
}
assert inv7_Repaired {
    inv7[] iff inv7_OK[]
}
--------
pred inv8_OK {
 	no link 
}
assert inv8_Repaired {
    inv8[] iff inv8_OK[]
}
--------
pred inv9_OK {
  no link.link  
}
assert inv9_Repaired {
    inv9[] iff inv9_OK[]
}
--------
pred inv10_OK {
  Trash.link in Trash 
}
assert inv10_Repaired {
    inv10[] iff inv10_OK[]
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
pred repair_pred_1{inv4[] iff inv4_OK[] }
run repair_pred_1
assert repair_assert_1{inv4[] iff inv4_OK[] }
check repair_assert_1