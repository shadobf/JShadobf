from jshadobf.common.classes import Statements
from jshadobf.common.finder import get_all_ident
from jshadobf.common.tree_walker import walker
from jshadobf.common.common import deepcopy, jshadobf_random
from jshadobf.transformations.common import NUMBERMAX, count_object, genVarNotIn,\
    shouldi

def add_dummy_variables(parse_tree,verbose=0,numbermax=NUMBERMAX):
    """This function takes in arpument parse_tree as a parse tree, and will add some dummy variables,
    it will return a new parse tree, with these dummy variables
    the verbose argument allows to increase verbosity"""
    if verbose >1:
        print "apply add_dummy_var transformation"
    p = deepcopy(parse_tree)
    ret = get_all_ident(parse_tree)
    arg={"ident_present":ret,"numbermax":numbermax}
    arg["size"]=count_object(p,[Statements])
    walker(p,postfunction=add_dummy_var_func_post,arg=arg)
    return p

def add_dummy_var_func_post(program,arg):
    if program.__class__ == Statements:
        if shouldi(arg=arg):
            dummyvar,name = genVarNotIn(arg["ident_present"]) 
            dummyvar.dummy = True
            program.insert(jshadobf_random.randint(0,len(program.statements_list)),dummyvar)
    return [],arg
  
  
  
  