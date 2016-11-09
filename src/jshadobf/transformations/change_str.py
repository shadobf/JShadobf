from jshadobf.common.classes import String,PropertyName,Var,Ident,Expr,VarDeclaration, Functioncall, Listarguments
from jshadobf.common.tree_walker import walker
from jshadobf.common.common import deepcopy, jshadobf_random
from jshadobf.common.finder import get_all_ident,get_all_upper_statements_and_pos
from jshadobf.transformations.common import NUMBERMAX, count_object, shouldi, genVarNotIn

def change_str(program_tree,verbose=0,numbermax=NUMBERMAX):
    if verbose >1:
        print "apply change_str transformation" , "with" , numbermax
    p = deepcopy(program_tree)
    ret = get_all_ident(program_tree)
    arg={"numbermax":numbermax,"ident_present":ret}
    arg["size"] = count_object(p,[String])
    walker(p,postfunction=change_str_func,arg=arg)
    return p
  
def change_str_func(program,arg):
    if isinstance(program,String):
        if len(program.value) > 1:    
            list_upper_statements = get_all_upper_statements_and_pos(program)
            if list_upper_statements != [] and (not isinstance(program.parent,PropertyName)): # and program != program.parent.name):
                if shouldi(arg=arg):
                    depth = jshadobf_random.randint(0,len(list_upper_statements)-1)
                    s = list_upper_statements[depth][0] 
                    maxi = list_upper_statements[depth][1]
                    mylist = []
                    after_escape = False
                    i = 0
                    oi = 0
                    l = program.value
                    sel = range(len(l))
                    jshadobf_random.shuffle(sel)
                    sel2 = sel[:3]
                    sel2.sort()
                    for index in sel2+[None]:
                        i = 0
                        if index :
                            while ord(l[index - i]) >= 128 :
    
                                print index -i 
                                i += 1
                                if index - i == oi:
                                    break
                            if not (i % 2):
                                index -= 1
                        vardeclist,name=genVarNotIn(arg["ident_present"],Expr([String(repr(l[oi:index].encode("utf-8")))]))
                        pos = jshadobf_random.randint(0,maxi)
                        maxi = maxi + 1
                        s.insert(pos,vardeclist)
                        mylist.append(name)
                        oi = index 
#                    
                    varlist = map(lambda x:Ident(x),mylist)
                    [varlist.insert(i*2 - 1,"+") for i in range(1,len(varlist))]
                    expr = Expr([Functioncall(Expr([Ident("eval")]),Listarguments([Expr(varlist)]))])
                    if program.parent.__class__ in [Expr,VarDeclaration,PropertyName]: 
                        program.parent.replace_item(program,expr)
    return [],arg

