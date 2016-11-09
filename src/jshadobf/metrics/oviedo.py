from jshadobf.common.common import ident_is_functioncall, ident_is_suffix
from jshadobf.common.tree_walker import walker
from jshadobf.common.classes import Statements, VarDeclaration, Ident

OVIEDO_LIST = [Statements]

def check_block_var_and_add(program,arg):
    if ident_is_functioncall(program):
        return False
    if ident_is_suffix(program):
        return False
    if program.name in map(lambda x:x.name , arg[-1]['block_var']):
        return True
    arg[-1]["non_block_var_usage"] += 1 
    return False
  
def oviedo(program_tree):
    arg = [{"block_var": [] , "non_block_var_usage" :0}]
    l,a = walker(program_tree,oviedo_func,oviedo_post_func,arg=arg)
    s = sum(l) 
    return s

def oviedo_func(program,arg=[]):
    if program.__class__ in OVIEDO_LIST:
        prgident = []
        narg = {"block_var": [] , "non_block_var_usage" :0}
        arg.append(narg)
    if isinstance(program, VarDeclaration):
        arg[-1]['block_var'].append(program.var)
    if isinstance(program, Ident):
        check_block_var_and_add(program,arg)

    return [],arg
  
def oviedo_post_func(program,arg=[0]):
    if program.__class__ in OVIEDO_LIST:
        oarg = arg.pop()
        return [oarg["non_block_var_usage"]],arg
    return [],arg

