from jshadobf.common.classes import * 
from jshadobf.common.common import deepcopy, is_break_inside_weak, is_return_inside
from jshadobf.common.tree_walker import walker
from jshadobf.transformations.common import NUMBERMAX, count_object, shouldi

def evalification(program_tree,verbose=False,numbermax=NUMBERMAX):
    if verbose :
        print "apply evalification transformation"
    p = deepcopy(program_tree)
    arg={"numbermax":numbermax}
    arg["size"] = count_object(p,[Statements])

    #~ ret =get_all_ident(program_tree)
    walker(p,evalification_func,arg=arg)
    return p

def evalification_func(program,arg):
    #~ print 
    if isinstance(program,Statements):
        for s in program.statements_list:
            if not is_return_inside(s) and not is_break_inside_weak(s):
                if shouldi(arg=arg):
                    ss = repr(s.oneline_str().encode("utf-8"))
                    program.replace_item(s, Expr([Functioncall(Expr([Ident("eval")]),Listarguments([String(ss)]))]))
    return [] , arg



