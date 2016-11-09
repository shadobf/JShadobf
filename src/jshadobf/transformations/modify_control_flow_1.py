from jshadobf.common.classes import (CaseBlock,Number,Switch,Break ,While,
                              String,PropertyName,Var,Ident,Expr,Program,
                              VarDeclaration,Assignment,Statements,ExpressionStatement)
from jshadobf.common.tree_walker import walker
from jshadobf.common.common import deepcopy,is_break_inside, jshadobf_random
from jshadobf.common.finder import get_all_ident,get_all_upper_statements_and_pos,get_upper_statement_and_pos,get_upper_expression_statement_and_pos
from jshadobf.transformations.common import NUMBERMAX, count_object, shouldi, genVarNotIn

def modify_control_flow_1(program_tree,verbose=0,numbermax=NUMBERMAX):
    if verbose >1:
        print "apply modify_control_flow_1 transformation"
    p = deepcopy(program_tree)
    ret = get_all_ident(program_tree)
    arg={"ident_present":ret,"numbermax":numbermax}
    arg["size"]=count_object(p,[Statements])
    walker(p,postfunction=modify_control_flow_1_post_func,arg=arg)
    return p

def generate_expr_for_compare(name):
    r = jshadobf_random.randint(0,100000)
    e = Expr([Number(r)])
    gt = Assignment(Expr([Ident(name)]),"=",Expr([Number(r)]))
    return e,gt
  
def modify_control_flow_1_post_func(program,arg):
    if isinstance(program,Statements):
        if shouldi(arg=arg):
            vardeclist,name=genVarNotIn(arg["ident_present"]) 
            old = program.statements_list
            if len(old)!=0 and not is_break_inside(program):
                li = []
                we,wgt = generate_expr_for_compare(name)
                for index in range(len(old)):
                    e,gt = generate_expr_for_compare(name)
                    cb = CaseBlock(Statements([old[index]]),e)
                    li.append((cb,e,gt))
                (cb,e,gt) = li[0]
                ini = gt
                (cb1,e1,gt1) = li[0]
                for i in range(len(li)-1):
                    (cb,e,gt) = li[i]
                    (cb1,e1,gt1) = li[i+1]
                    cb.statement.append(gt1)
                    b = Break()
                    cb.statement.append(b)
                cb1.statement.append(wgt)
                b = Break()
                cb1.statement.append(b)
                sw = Switch(Expr([Ident(name)]),list(zip(*li)[0]))
                wh = While(Expr([we,"!=",Ident(name)]),Statements([sw]))
                program.replaceall([vardeclist,ini,wh])
    return [] , arg

