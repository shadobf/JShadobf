from jshadobf.common.classes import (Statements,VarDeclaration,This,Break,Ident,Assignment,
        Function,Functioncall,Expr,ExpressionStatement,Listarguments,Index,Number,Var,
        MemberExpr,Return,List)
from jshadobf.common.common import is_return_inside,is_function_inside,detect_presence,examine_function_vars,include_ident, jshadobf_random
from jshadobf.common.finder import get_all_ident,get_upper_function,get_all_upper_statement_and_pos
from jshadobf.common.common import deepcopy,removeindex,ident_is_property,ident_is_in_left_handside_assignment,BLACK,RED
from jshadobf.common.tree_walker import walker
from jshadobf.transformations.common import NUMBERMAX, count_object, shouldi, genVarNotIn

"""This module is to apply outlining on a parse tree"""

def outlining(program_tree,verbose=0,numbermax=NUMBERMAX):
    if verbose >1:
        print "apply outlining transformation"
    p = deepcopy(program_tree)
    ret = get_all_ident(program_tree)
    arg={"ident_present":ret,"encountered":[],"numbermax":numbermax}
    arg["size"]=count_object(p,[Statements])
    walker(p,postfunction=outlining_post_func,arg=arg)
    return p

def find_var_dec_in_function(function,untill):
    walk_condition = lambda x,y:not isinstance(x,Function)  and y["function_init"] != x
    decbefore = []
    if isinstance(function,Function):
        decbefore = [a.name for a in function.args_dec.args_list ]
    ret ,arg = walker(program=function,function=find_var_dec_in_function_func,arg={"function_init" : function,"untill":untill,"decbefore":decbefore,"decafter":[]},walk_condition=walk_condition)
    return arg["decbefore"],arg["decafter"]

def find_var_dec_in_function_func(function,arg):
    if function == arg["untill"]:
        arg["untill"] = False
    if isinstance(function,VarDeclaration):
        if  arg["untill"]:
            arg["decbefore"].append(function.var.name)
        else:
            arg["decafter"].append(function.var.name)
    return [] , arg

def findrefvar(program,arg):
  #~ print program.__class__
    if arg == None:
        return [],None
    if isinstance(program,VarDeclaration):
        arg["var_dec_in"].append(program.var.name)
    if isinstance(program,Assignment):
        pv = deepcopy(program.var)
        removeindex(pv)
        arg["assignment"].append(str(pv))
    if isinstance(program,This):
        return [], None   
    if isinstance(program,Break):
        return [], None  
    if isinstance(program,Ident):
        if program.name == "eval":
            print RED, "FIND EVAL OR THIS",BLACK
            return [], None
        if not ident_is_property(program) : #and not ident_is_function(program) :
            a= ident_is_in_left_handside_assignment(program) 
            if not a or a.typeof != "=":
                arg["ref"].append(program.name)
    return [] , arg
  
def find_ref_and_out_var(statements,encountered):  
    if len(statements) > 0:
        function = get_upper_function(statements[0])
        (decbefore,decafter) = find_var_dec_in_function(function,statements[0])
        arg={"this_present": False ,"eval_present":False, "vardec":decbefore,"var_dec_in":[],"assignment":[],"ref":[],"encountered":encountered}
        for s in statements:
            ret,arg=walker(s,function=findrefvar,arg=arg)
        if arg == None:
            return None , None , None
        varout = list(set(arg["assignment"]))
        nameargs = list(set(arg["ref"]))
        vardecout = list(set(arg["var_dec_in"]))
        varout = filter(lambda x: not x in vardecout , varout)
        nameargs = filter(lambda x : x in arg["vardec"] ,nameargs)
        return nameargs ,varout,vardecout
    return None , None

def undeclare_var ( statements , variables):
    walker(statements,postfunction=undeclare_var_func_post,arg=variables,walk_condition = lambda x,y:not isinstance(x,Function))

def get_types_func(program ,types):
    ret = []
    if program.__class__ in types:
        ret = [program]
    return ret,types

def get_types(statements ,types):
    ret = []
    if not isinstance(statements, list):
        statements = [statements]
    for s in statements:
        r,dummy = walker(s,function=get_types_func,arg=types)
        ret += r
    return ret

def all_function_call_are_functionnal(outline):
  #~ TODO discover all function which are functionnal
  #~ discover_fonctionnal_function(main_program)
    functions  = []
    functioncalls = get_types(outline,[Functioncall])
    res = True
    for fc in functioncalls:
        discovered = filter(lambda f : f.name == fc.name , functions)
        if len(discovered) != 1:
            res = False
            break
        else :
            if discovered[0].name == fc.name:
                if discovered[0].fonctionnal == False:
                    res = False
                    break
    return res

def undeclare_var_func_post ( program , variables):
    if isinstance(program, VarDeclaration):
        toaddafter = []
        indexes = range(len(program.args_dec_list))
        indexes.reverse()
        for i in indexes :
            dec = program.args_dec_list[i]
            if dec.var.name in variables:
                if dec.expr != None:
                    toaddafter.append(Assignment(Ident(dec.var.name),"=",dec.expr))
                del program.args_dec_list[i]
        if isinstance(program.parent,Statements):
            pos_var_dec_list = program.parent.statements_list.index(program)
            for a in toaddafter:
                program.parent.insert(pos_var_dec_list+1,a) # good order due to indexes.reverse()
            if len (program.args_dec_list) == 0:
                del program.parent.statements_list[pos_var_dec_list]
        if isinstance(program.parent,Expr):
            pos_var_dec_list = program.parent.exprs.index(program)
            del program.parent.exprs[pos_var_dec_list]
            if len(toaddafter) == 1 :
                program.parent.insert(pos_var_dec_list,toaddafter[0])
            else:
                program.parent.insert(pos_var_dec_list,ExpressionStatement(toaddafter))
    return [],variables

def outlining_post_func(program,arg):
    if isinstance(program,Statements):
        if shouldi(arg=arg) and len(program.statements_list)!= 0:
            f = jshadobf_random.randint(0,len(program.statements_list)-1)
            t = jshadobf_random.randint(f+1,len(program.statements_list))
            outline = program.statements_list[f:t]
            if not is_return_inside(outline) and not is_function_inside(outline):
                funcobj,funcname = genVarNotIn(arg["ident_present"])
                presence =  detect_presence (outline)
                if not (presence["arguments"] or presence["this_present"] or presence["break_present"] or presence["eval_present"] ):
                    examine_outline =  examine_function_vars (outline)
                    upfunc =get_upper_function(program)
                    examine_before = examine_function_vars (upfunc ,   program.statements_list[f]   )
                    examine_func = examine_function_vars ( upfunc  )
                    if isinstance(upfunc,Function):
                        for v in upfunc.args_dec.args_list :
                            include_ident(examine_before["local_var"],v)
                    nameargs ,varout,vardecout , vardec,todec=  [],[],[],[],[]
                    if all_function_call_are_functionnal ( outline ):
                        for k in examine_outline["local_var"].keys() :
                            if examine_before["local_var"].has_key(k) and examine_before["local_var"][k][0]["has_been_assigned"] :
                                nameargs.append(k)
                        for k in examine_outline["var_global_ref"].keys() :
                            if examine_before["local_var"].has_key(k) :
                                nameargs.append(k)
                            elif  examine_func["local_var"].has_key(k):
                                todec.append(k)
                            elif  examine_before["var_global_set"].has_key(k):
                                nameargs.append(k)
                        for k in examine_outline["var_global_set"].keys() :
                            if examine_before["local_var"].has_key(k):
                                nameargs.append(k)
                            elif  examine_func["local_var"].has_key(k):
                                todec.append(k)
                        for k in examine_outline["local_var"].keys() :
                            vardecout.append(k)
                        for k in examine_outline["local_var"].keys() :
                            if examine_outline["local_var"][k][0]["has_been_assigned"] : 
                                varout.append(k)
                        for k in examine_outline["var_global_set"].keys() :
                            varout.append(k)
                        movable =  all ( [  k in nameargs+ vardecout for k in examine_outline["local_var"].keys()+examine_outline["var_global_ref"].keys()]+
                        [ examine_outline["var_global_set"].keys()==[]]  )
                    elif len(examine_outline["local_var"]) == 0:
                        nameargs ,varout,vardecout =  [],[],[]
                        movable = False
                    else:
                        return [] , arg
       
                    vardecout = list(set(vardecout))
                    varout = list(set(varout))
                    nameargs = list(set(nameargs))
                    rem = range(f,t)
                    rem.reverse()
                    for i in rem:
                        del program.statements_list[i]
                    outline = [ Var([VarDeclaration(Ident(n))]) for n in vardec ] + outline
                    outline += [ Return(Expr([List([Ident(n) for n in varout])]))]
                    listarg = Listarguments([Ident(n) for n in nameargs] )
                    listretobj,listretname = genVarNotIn(arg["ident_present"])
 
                    i = 0
                    for n in varout:
                        program.insert(f, Assignment(Ident(n),"=",
                        MemberExpr(Expr([Ident(listretname)]),[Index(Expr([Number(str(i))]))])))
                        i=i+1
                    for n in vardecout:
                        program.insert(f, Var([VarDeclaration(Ident(n))]))
                        i = i + 1
                    for n in todec:
                        outline.insert(0, Var([VarDeclaration(Ident(n)) ]))
                    
                    program.insert(f, Var([VarDeclaration(Ident(listretname),
                    Functioncall(Ident(funcname),listarg))]))
                    uppers= []
                    if movable:
                        uppers = get_all_upper_statement_and_pos(program)
                    uppers = uppers + [(program,f)]
                    upper , pos = uppers[jshadobf_random.randint(0,len(uppers)-1)]
                    outline_statement = Statements(outline)
                    l1 = deepcopy(listarg)
                    upper.insert(pos,Function(Ident(funcname),l1,outline_statement))
    return [] , arg

