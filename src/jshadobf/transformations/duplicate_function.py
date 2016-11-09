from jshadobf.common.classes import Number, Expr, Statements, EmptyStatement, If, Function, Ident
from jshadobf.common.common import deepcopy,check_tree, jshadobf_random
from jshadobf.common.tree_walker import walker
from jshadobf.transformations.common import NUMBERMAX, count_object, shouldi
from jshadobf.common.finder import get_all_ident, get_upper_statement_and_pos
from jshadobf.common.colors import red


def duplicate_function(program_tree,verbose=0,numbermax=NUMBERMAX):
    if verbose >1:
        print "apply duplicate_function transformation" , "with" , numbermax
    p = deepcopy(program_tree)
    ret = get_all_ident(program_tree)
    arg={"ident_present":ret,"numbermax":numbermax}
    arg["size"] = count_object(p,[Statements])
    walker(p,postfunction=duplicate_function_func_post,arg=arg)
    return p

def duplicate_function_func_post(program,arg):
    if program.__class__ == Function:   
        if shouldi(arg=arg):
            if program.ident != None:
                newfunc = deepcopy(program)
                statement,pos = get_upper_statement_and_pos(program)
                statement.insert(jshadobf_random.randint(0,len(statement.statements_list)-1),newfunc)
                sl = newfunc.statements.statements_list
                if len (sl) > 0:
                    for i in range(max(1,len(sl)/3)):
                        del sl[jshadobf_random.randint(0,len(sl)-1)]
                i = 0
                newname = program.ident.name
                n =newname
                while  newname in arg["ident_present"]:
                    i = i + 1
                    newname = program.ident.name+format(i)
                    n += " " + newname
                print red(n)
                arg["ident_present"].append(newname)
                newfunc.replace_ident( Ident(newname))
    return [],arg



