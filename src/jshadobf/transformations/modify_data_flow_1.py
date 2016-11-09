from jshadobf.common.classes import String,PropertyName,Var,Ident,Expr,VarDeclaration,Assignment,Statements,ExpressionStatement
from jshadobf.common.tree_walker import walker
from jshadobf.common.common import deepcopy,is_functioncall_inside
from jshadobf.common.finder import get_all_ident,get_all_upper_statements_and_pos,get_upper_statement_and_pos,get_upper_expression_statement_and_pos
from jshadobf.transformations.common import NUMBERMAX, count_object, shouldi, genVarNotIn

def modify_data_flow_1(program_tree,verbose=0,numbermax=NUMBERMAX):
    if verbose >1:
        print "apply modify_data_flow_1 transformation"
    p = deepcopy(program_tree)
    ret = get_all_ident(program_tree)
    arg={"ident_present":ret,"numbermax":numbermax}
    arg["size"]=count_object(p,[Assignment])
    walker(p,postfunction=modify_data_flow_1_post_func,arg=arg)
    return p
  
def modify_data_flow_1_post_func(program,arg):
    if isinstance(program,Assignment):
        if shouldi(arg=arg):      
            s,pos = get_upper_statement_and_pos(program)
            s2,pos2 = get_upper_expression_statement_and_pos(program)
            if pos2 == None  and s != None:
                if not is_functioncall_inside(program):# and position_in_exprstatement(program) == 0: # TODO check position_in_exprstatement is working
                    vardeclist,name=genVarNotIn(arg["ident_present"]) 
                    s.insert(pos,Assignment(Expr([Ident(name)]),"=",program.expr))
                    s.insert(0,vardeclist)
                    program.expr = Ident(name)
                    program.expr.parent = program
    return [] , arg

