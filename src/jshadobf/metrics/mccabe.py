from jshadobf.common.tree_walker import walker
from jshadobf.common.classes import *

def mccabe(program_tree):
    l,a = walker(program_tree,mccabe_func,arg=None)
    s = sum (l)
    return s
def mccabe_func(program,arg=[]):
    if isinstance(program,While):
        return [1], arg
    if isinstance(program,If):
        return [1], arg
    if isinstance(program,For):
        return [1], arg
    if isinstance(program,Switch):
        return [len(program.caseblock)], arg
    return [],arg


