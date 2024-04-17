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
/* Protected files cannot be in the trash. */
pred inv4 {
no Protected & Trash
}
/* All unprotected files are deleted. */
pred inv5 {
(File - Protected) in Trash
}