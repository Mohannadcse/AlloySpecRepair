sig List  {
    header: lone Node
}

sig Node {
    link: lone Node,
    elem: one Int
}

fact CardinalityConstraints {
    all l: List | lone l.header
    all n: Node | lone n.link
    all n: Node | one n.elem
}

pred Loop(This: List) {
    no This.header || one n: This.header.*link | n in n.link
}

pred Sorted(This: List) {
    all n: This.header.*link | some n.link => n.elem <= n.link.elem
}

pred RepOk(This: List) {
    Loop[This]
    Sorted[This]
}

pred Count(This: List, x: Int, result: Int) {
    RepOk[This]
    #{n: This.header.*link | n.elem = x} = result
}

abstract sig Boolean {}
one sig True, False extends Boolean {}

pred Contains(This: List, x: Int, result: Boolean) {
    RepOk[This]
    {some n: This.header.*link | n.elem = x } => result = True
    {no n: This.header.*link | n.elem = x } => result = False
}

fact { some Node }

assert repair_assert_1{
    all l:List | all x:Int | all res:Boolean |
    Contains[l, x, res] <=>
    {
        RepOk[l]
        {some n: l.header.*link | n.elem = x } <=> res = True
    }
}
check repair_assert_1

pred repair_pred_1{
    all l:List | all x:Int | all res:Boolean |
    Contains[l, x, res] <=>
    {
        RepOk[l]
        {some n: l.header.*link | n.elem = x } <=> res = True
    }
}
run repair_pred_1

fact IGNORE {
    one List
    List.header.*link = Node
}