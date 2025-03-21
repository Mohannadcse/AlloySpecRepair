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

all f : File | some g,h : File | f->g in link implies f->h not in link
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
/* Fixed inv6 predicate */
pred inv6_fixed {
no f, g, h : File | f->g in link and f->h in link and g != h
}
assert inv6_fixed_correct {
inv6[] iff inv6_fixed[]
}