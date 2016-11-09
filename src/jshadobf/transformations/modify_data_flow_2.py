from jshadobf.common.classes import Number,Functioncall,Expr,Ident, List
from jshadobf.common.finder import get_all_ident,get_upper_statement_and_pos
from jshadobf.common.common import deepcopy, jshadobf_random
from jshadobf.common.tree_walker import walker
from jshadobf.transformations.common import NUMBERMAX, count_object, shouldi, genVarNotIn

def modify_data_flow_2(program_tree,verbose=0,numbermax=NUMBERMAX):
    if verbose >1:
        print "apply modify_data_flow_2 transformation"
    p = deepcopy(program_tree)
    ret = get_all_ident(program_tree)
    arg={"ident_present":ret,"numbermax":numbermax}
    arg["size"]=count_object(p,[Number])
    walker(p,modify_data_flow_2_func,modify_data_flow_2_post_func,arg=arg)
    return p
  
def is_functioncall_inside(program):
    c = program.getChildren()
    if isinstance(program , Functioncall):
        return True
    for i in c : 
        if is_functioncall_inside(i):
            return True
    return False

def modify_data_flow_2_func(program,arg):
    if isinstance(program,Number):
        if shouldi(arg=arg):
            s,pos = get_upper_statement_and_pos(program)
            if s != None:
                whereto = jshadobf_random.randint(0,pos)
                newp = deepcopy(program)
                vardeclist,name=genVarNotIn(arg["ident_present"],newp)
                program.parent.replace_item(program, Ident(name))
                s.insert(whereto,vardeclist)
    if isinstance(program,List):
        if shouldi(arg=arg):
            s,pos = get_upper_statement_and_pos(program)
            if s != None  and not is_functioncall_inside(program):
                whereto = jshadobf_random.randint(0,pos)
                if count_object(program,[Ident] ):
                    whereto = pos
                newp = deepcopy(program)
                vardeclist,name=genVarNotIn(arg["ident_present"],newp)
                program.parent.replace_item(program, Ident(name))
                s.insert(whereto,vardeclist)
    return [] , arg

def modify_data_flow_2_post_func(program,switcher):
    return [] , switcher

