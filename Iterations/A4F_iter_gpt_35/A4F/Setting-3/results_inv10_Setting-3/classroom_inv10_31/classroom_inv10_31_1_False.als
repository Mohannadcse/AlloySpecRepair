pred inv10_OK { all c:Class, s:Student | some s.(c.Groups) } assert inv10_Repaired { inv10[] implies inv10_OK[] }