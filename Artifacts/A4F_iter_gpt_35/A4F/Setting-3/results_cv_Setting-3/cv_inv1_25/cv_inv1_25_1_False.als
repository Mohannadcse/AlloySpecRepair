abstract sig Source {} sig User extends Source { profile : set Work, visible : set Work } sig Institution extends Source {} sig Id {} sig Work { ids : some Id, source : one Source } pred inv1 { all u : User, w : Work | u->w in profile and w in u.visible } pred inv1_OK { all u:User | u.visible in u.profile } assert inv1_Repaired { inv1[] iff inv1_OK[] } check inv1_Repaired expect 0