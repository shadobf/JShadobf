from jshadobf.common.tree_walker import walker
from jshadobf.common.classes import Function, Ident, Statements, Program,\
	ExpressionStatement

def get_funcs(program):
    ret,arg = walker(program,function=get_funcs_func)
    return ret 

def get_funcs_func(program,arg):
    if program.__class__ == Function:
        ret = [program]
        return ret , arg
    return [],arg

def find_func(program,funcname):
    ret,arg = walker(program,function=find_func_func,arg=funcname)
    return ret

def find_ident(program, name):
    ret,arg = walker(program,function=find_ident_func,arg=name)
    return ret

def find_ident_func(program,arg):
    if program.__class__ == Ident:
        if program.name == arg:
            ret = [program]
            return ret , arg
    return [],arg

def find_func_func(program,arg):
    if program.__class__ == Function:
        if program.ident.name == arg :
            ret = [program]
            return ret , arg
    return [],arg

def get_all_ident(program):
    ret,arg = walker(program,function=get_all_ident_func,arg=None)
    ret = list(set(ret))
    return ret

def get_all_ident_func(program,arg):
    if program.__class__ == Ident:
        ret = [program.name]
        return ret , arg
    return [],arg

def get_upper_statement_and_pos(program):
    if program.parent != None:
        if isinstance(program.parent, Statements):
            return program.parent, program.parent.index(program)
        return get_upper_statement_and_pos(program.parent)
    
    return None, None

def get_upper_function(program):
    if program.parent != None:
        if isinstance(program.parent, Function):
            return program.parent
        if isinstance(program.parent, Program):
            return program.parent
        return get_upper_function(program.parent)
    return None

def get_root(program):
    if isinstance(program, Program):
        return program
    return get_root(program.parent)

def get_all_upper_statements_and_pos(program):
    if program.parent != None:
        
        ret = []
        if isinstance(program.parent, Statements):
            ret =  [( program.parent ,  program.parent.index(program) )]
        return ret + get_all_upper_statements_and_pos(program.parent)
    return []

def getfirstident(parse_tree):
    if isinstance(parse_tree, Ident):
        return parse_tree
    for s in parse_tree.getChildren():
        ret = getfirstident(s)
        if isinstance(ret, Ident):
            return ret
    return None

def get_upper_expression_statement_and_pos(program):
    if program.parent != None:
        if isinstance(program.parent,Statements):
            return None,None
        if isinstance(program.parent,ExpressionStatement):
            return program.parent,program.parent.exprs.index(program)
        return get_upper_expression_statement_and_pos(program.parent)
    return None,None

def get_all_upper_statement_and_pos(program):
    p = program 
    result = []
    while p != None:
        prog , pos = get_upper_statement_and_pos(p)
        if prog != None:
            result.append((prog , pos))
        p = prog
    return result
