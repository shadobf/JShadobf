from jshadobf.common.classes import Statements,EmptyStatement
from jshadobf.common.common import deepcopy
from jshadobf.common.tree_walker import walker
from jshadobf.transformations.common import NUMBERMAX

def remove_empty_statement(program_tree,verbose=False,numbermax=NUMBERMAX):
    if verbose:
        print "apply remove_empty_statement transformation"
    p = deepcopy(program_tree)
    walker(p,remove_empty_statement_func,arg=[])
    return p

def remove_empty_statement_func(program, arg):
    if isinstance(program,Statements):
        mylist = map(lambda x: x.__class__ , program.statements_list)
        while EmptyStatement in mylist:
            i = mylist.index(EmptyStatement) 
            del program.statements_list[i]
            del mylist[i]
        for s in program.statements_list:
            remove_empty_statement_func(s,arg)
        if isinstance(program.parent,Statements):
            if len(program.statements_list) == 0:
                i = program.parent.statements_list.index(program)
                del  program.parent.statements_list[i]
    return [] , arg

