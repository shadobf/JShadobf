import sys
from jshadobf.common.classes import Number, Expr, Statements, EmptyStatement, If
from jshadobf.common.common import deepcopy, jshadobf_random
from jshadobf.common.tree_walker import walker
from jshadobf.transformations.common import NUMBERMAX, count_object, shouldi, genPredicate

def add_if_statement(program_tree,verbose=0,numbermax=NUMBERMAX):
    if verbose >1:
        print "apply add_if_statement transformation" , "with" , numbermax
    p = deepcopy(program_tree)
    arg={"numbermax":numbermax}
    arg["size"] = count_object(p,[Statements])
    walker(p,postfunction=add_if_statement_func_post,arg=arg)
    return p

def add_if_statement_func_post(program,arg):
    if program.__class__ == Statements:   
        if shouldi(arg=arg):
            ie = If(genPredicate(program),Statements([EmptyStatement()]),Statements([EmptyStatement()]))
#      print GREEN,"gen " , ie.__class__ , "%x"% id(ie),BLACK
            program.insert(jshadobf_random.randint(0,len(program.statements_list)), ie)
    return [],arg

