abstract sig Color {}
one sig Red extends Color {}
one sig Blue extends Color {}

sig Node {
  neighbors: set Node,
  color: one Color 
} 	

fact undirected {
  neighbors = ~neighbors   -- symmetric
  
  -- no iden & neighbors      -- antireflexive
}

fact graphIsConnected {
  all n1: Node | all n2: Node-n1 | 
    n1 in n2.^neighbors }

fact treeAcyclic {
  all n1, n2: Node | n1 in n2.neighbors implies 
    n1 not in n2.^(neighbors-(n2->n1)) } 

run {} for 3 Node

assert repair_assert_1{
	no iden & neighbors
}
check repair_assert_1

pred repair_pred_1{
	no iden & neighbors
}
run repair_pred_1
