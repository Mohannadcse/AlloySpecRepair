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
Trash in File
}
/* Some file is deleted. */
pred inv3 {
some Trash
}
/* Protected files cannot be deleted. */
pred inv4 {
no Trash & Protected
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
all x, y : File | x->y in link and x not in Trash and y not in Trash
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