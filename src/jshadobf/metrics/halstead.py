from jshadobf.common.tree_walker import walker
from jshadobf.common.classes import *

def halstead(program_tree):
    l,a = walker(program_tree,halstead_func,arg=None)
    s = sum (l)
    return s
  
weight_one = [Ident,Number,String,Assignment,While]
  
def halstead_func(program,arg=[]):
    if isinstance(program,List):
        return [len(program.value) + 1],arg
    if isinstance(program,Listarguments):
        return [max(0,len(program.args_list) - 1)],arg
    if program.__class__ in weight_one:
        return [1],arg
    if isinstance(program,Expr):
        return [len(program.exprs)-1],arg
    if isinstance(program,If):
        ret = 1
        if program.statementsfalse != None:
            ret += 1
        return [ret], arg
    if isinstance(program,Statements):
        return [1], arg
    if isinstance(program,Function):
        return [1], arg
    if isinstance(program,Switch):
        return [1+len(program.caseblock)], arg
    return [],arg

