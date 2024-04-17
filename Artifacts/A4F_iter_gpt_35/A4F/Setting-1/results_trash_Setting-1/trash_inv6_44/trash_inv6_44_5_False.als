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
no Protected & Trash
}
/* All unprotected files are deleted.. */
pred inv5 {
File - Protected in Trash
}
/* A file links to at most one file. */
pred inv6 {
all f1,f2:File | f1.link & f2.link in f1 & f2 implies f1 = f2
}
/* There is no deleted link. */
pred inv7 {
no link & Trash
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