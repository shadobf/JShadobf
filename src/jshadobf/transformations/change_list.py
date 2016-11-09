from jshadobf.transformations.common import NUMBERMAX, count_object, shouldi, genVarNotIn
from jshadobf.common.common import deepcopy, is_functioncall_inside, jshadobf_random
from jshadobf.common.finder import get_all_ident, get_all_upper_statements_and_pos
from jshadobf.common.classes import List, PropertyName, Ident, Expr, CallExpressionSuffix, Listarguments, Property, Functioncall, MemberExpr
from jshadobf.common.tree_walker import walker

def change_list(program_tree,verbose=0,numbermax=NUMBERMAX):
    if verbose >1:
        print "apply change_list transformation" , "with" , numbermax
    p = deepcopy(program_tree)
    ret = get_all_ident(program_tree)
    arg={"numbermax":numbermax,"ident_present":ret}
    arg["size"] = count_object(p,[List])
    walker(p,postfunction=change_list_func_post,arg=arg)
    return p

def change_list_func_post(program,arg):
    if isinstance(program,List):
        if len(program.value) > 1:    
            list_upper_statements = get_all_upper_statements_and_pos(program)
            if list_upper_statements != [] and (not isinstance(program.parent,PropertyName)) and not is_functioncall_inside(program): # and program != program.parent.name):
                if shouldi(arg=arg):
                    ident_inside = count_object(program,[Ident])
                    if  ident_inside:
                        depth = 0
                    else:
                        depth = jshadobf_random.randrange(0,len(list_upper_statements))
                    s = list_upper_statements[depth][0] 
                    maxi = list_upper_statements[depth][1]
                    mini = 0
                    mylist = []
                    if ident_inside:
                        mini = maxi
                    after_escape = False
                    i = 0
                    oi = 0
                    l = program.value
                    while len(l)!=i:
                        i = oi + int(abs(jshadobf_random.gauss(0,len(l)/3)))+1
                        i = min(len(l),i)
                        vardeclist,name=genVarNotIn(arg["ident_present"],Expr([List(l[oi:i])])) 
                        pos = jshadobf_random.randint(mini,maxi)
                        maxi = maxi + 1
                        s.insert(pos,vardeclist)
                        mylist.append(name)
                        oi = i 
                    varlist = map(lambda x:Ident(x),mylist)
                    if len(varlist)> 1:
                        callexprsuffix = CallExpressionSuffix(
                                    sum([[Property(Ident("concat")),  Listarguments([Expr([varlist[i]])])]
                                         for i in range(2,len(varlist))],[]))
                        expr = Expr([Functioncall( MemberExpr(Expr([varlist[0]]),[Property(Ident("concat"))])
                                      ,Listarguments([varlist[ 1]])
                                      ,callexprsuffix)])
                    else:
                        expr = Expr(varlist)
                    program.parent.replace_item(program,expr)
    return [],arg

