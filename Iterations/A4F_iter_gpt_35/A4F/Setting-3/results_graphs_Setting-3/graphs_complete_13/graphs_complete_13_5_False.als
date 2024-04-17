sig Node { adj : set Node }

pred completeOK { all n:Node | (Node - n) in n.^adj }

pred repair_pred_1 { complete[] iff completeOK[] }