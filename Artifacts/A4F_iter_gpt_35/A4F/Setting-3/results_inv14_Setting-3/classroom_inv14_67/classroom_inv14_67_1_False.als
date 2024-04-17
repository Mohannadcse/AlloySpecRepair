pred inv14_OK {
all s : Person, c : Class, t : Person | s in c.Groups implies some t, t -> c in Teaches
}