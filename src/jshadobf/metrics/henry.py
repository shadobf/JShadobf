from jshadobf.common.tree_walker import walker
from jshadobf.common.common import ident_is_functioncall, ident_is_suffix, ident_is_in_left_handside_assignment
from jshadobf.common.classes import *

def compute_henry(l):
    m = 0
    ll = []
    for i in l:
        if i > m :
            m = i
        else:
            ll.append(m)
            m = i
    ll.append(m)
    return ll

def henry(program_tree):
    arg = [{"global_access_read":[],"global_access_write":[] , "return":[] , "program_arg":["arguments"] ,"local_var": [] }]
    l,a = walker(program_tree,henry_func,henry_post_func,arg=arg)
    oarg = arg[0]
    (fanin,fanout) = (len(  oarg ["global_access_read"] +  oarg ["program_arg"] ),len(  oarg ["global_access_write"] +  oarg ["return"] ))
    s = sum(l)  + fanin*fanout
    return s

def check_global_var(program,arg):
    if ident_is_functioncall(program):
        return False
    if ident_is_suffix(program):
        return False
    if program.name in map(lambda x:x.name , arg[-1]['local_var']):
        return False
    return True 

def check_and_add_new_variable_read(program,arg):
    if not program.name in map(lambda x:x.name , arg[-1]['global_access_read']):
        arg[-1]['global_access_read'].append(program)

def check_and_add_new_variable_write(program,arg):
    if not program.name in map(lambda x:x.name , arg[-1]['global_access_write']):
        arg[-1]['global_access_write'].append(program)
  
def henry_func(program,arg=[]):
    if isinstance(program,Return):
        arg[-1]["return"].append(program)
    if isinstance(program,Function):
        prgident = []
        if program.ident != None:
            prgident = [program.ident]
        narg = {"global_access_read":[],"global_access_write":[] , "return":[] , "program_arg":program.args_dec.args_list ,"local_var": [] }
        arg.append(narg)
    if isinstance(program, VarDeclaration):
        arg[-1]['local_var'].append(program.var)
    if isinstance(program, Ident):
        if check_global_var(program,arg):
            if ident_is_in_left_handside_assignment(program):
                check_and_add_new_variable_write(program,arg)
            else:
                check_and_add_new_variable_read(program,arg)
    return [],arg
  
def henry_post_func(program,arg=[0]):
    if isinstance ( program,Function):
        oarg =  arg.pop()
        (fanin,fanout) = (len(  oarg ["global_access_read"] +  oarg ["program_arg"] ),len(  oarg ["global_access_write"] +  oarg ["return"] ))
        return [fanin*fanout] , arg
    return [],arg
