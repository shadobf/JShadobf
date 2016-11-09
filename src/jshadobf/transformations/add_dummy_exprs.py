from jshadobf.common.classes import Ident, Number, List, Ltrue, Lfalse, String, Expr, Assignment,Function,Program,Statements,VarDeclaration
from jshadobf.common.common import *
from jshadobf.common.tree_walker import walker
from jshadobf.transformations.common import NUMBERMAX, count_object, shouldi, gen_dummy_expr, pick_one

def add_dummy_exprs(parse_tree,verbose=0,numbermax=NUMBERMAX):
    """This function takes in arpument parse_tree as a parse tree, and will add some dummy exprs,
    it will return a new parse tree, with these dummy variables
    the verbose argument allows to increase verbosity"""
    if verbose >1:
        print "apply add_dummy_exprs transformation" ,"with", numbermax
    p = deepcopy(parse_tree)
  #~ ret = get_all_ident_assigned(parse_tree)
    arg={"ident_ass":[],"dummyvars":[],"numbermax":numbermax}
    arg["size"]=count_object(p,[Statements])
    walker(p,add_dummy_exprs_func,postfunction=add_dummy_exprs_func_post,arg=arg)
    return p

def add_dummy_exprs_func(parse_tree,arg):
    if parse_tree.__class__ in [Function,Program,Statements]:
        arg["dummyvars"].append([])
        arg["ident_ass"].append([])
    if isinstance(parse_tree,Assignment):
        if isinstance(parse_tree.var,Expr):
            if len(parse_tree.var.exprs) == 1 and  isinstance(parse_tree.var.exprs[0],Ident):
                arg["ident_ass"][-1].append(parse_tree.var.exprs[0].name)
    if isinstance(parse_tree,VarDeclaration):
        if parse_tree.dummy:
            arg["dummyvars"][-1].append(parse_tree.var.name)
    if parse_tree.__class__ == Statements:
        if shouldi(arg=arg):
            vartoass =None
            ident_ass=  reduce(lambda x,y : x+ y , arg["ident_ass"] )
            if  shouldi(2):
                dummyvars=  reduce(lambda x,y : x+ y , arg["dummyvars"] )
                if len(dummyvars ) > 0:
                    vartoass = pick_one(dummyvars)
            expr = gen_dummy_expr(vartoass,ident_ass)
            parse_tree.insert(jshadobf_random.randint(0,len(parse_tree.statements_list)),expr)
    return [],arg
  
def add_dummy_exprs_func_post(parse_tree,args):
    if parse_tree.__class__ in [Program,Function,Statements]:
        args["dummyvars"].pop()
        args["ident_ass"].pop()
    return [] , args
