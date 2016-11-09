from jshadobf.common.classes import Number,String,Ident,Ltrue,Lfalse,Expr,VarDeclaration,Listarguments,Statements
from jshadobf.common.convert import convert_string
from jshadobf.common.tree_printer import *
from jshadobf.common.common import deepcopy
from jshadobf.common.tree_walker import walker
import subprocess
from jshadobf.transformations.common import NUMBERMAX

def try_eval(program_tree,verbose=False,numbermax=NUMBERMAX):
    if verbose:
        print "apply try_eval transformation"
    p = deepcopy(program_tree)
    memory=[]
    walker(p,function=try_eval_func,postfunction=try_eval_post_func,arg=memory  )
    return p

def get_tuple_from_list(name,mylist):
    names = []
    if len(mylist) != 0:
        names = zip(*mylist)[0]
    if name in names :
        names = list(names)
        names.reverse()		
        index = names.index(name)
        index = len(names)-index-1
        return mylist[index]
    return False

def get_tuple_by_name_from_database(name,db):
    itera = range(len(db))
    itera.reverse()
    for i in itera:
        t = get_tuple_from_list(name,db[i])
        if t:
            return t
    return False

def evaluate_string(string):
    p = subprocess.Popen("node",stdin=subprocess.PIPE , stdout = subprocess.PIPE,stderr=subprocess.PIPE)
    p.stdin.write("console.log(typeof(%s))\n"%string)
    p.stdin.write("console.log(%s)\n"%string)
    p.stdin.close()
    res = p.stdout.read().splitlines()
    if len(res) == 2:
        typeof = res[0]
        ret = res[1]
        if typeof == "string":
            if ret.find("undefined") != -1:
                return None
            expr = String(ret)
        else:
            prgm  = convert_string(ret)
            expr = prgm.statements.statements_list[0]
        return expr
    return None

def try_eval_func(program,memory):
    return [] , memory

def conv2float(val):
    if isinstance(val,Number):
        return float(val.value)
    if isinstance(val,Ltrue):
        return True
    if isinstance(val,Lfalse):
        return False
  
def try_eval_expr(expr,memory):

    if expr.__class__ in [Number,String,Ident,Ltrue,Lfalse]:
        return expr,True
    if isinstance(expr,Expr):
        if len(expr.exprs) == 1:
            ret , suc = try_eval_expr(expr.exprs[0],memory)
            return ret , suc 
        elif len(expr.exprs) == 2:
            if isinstance( expr.exprs[0],str):
                return expr ,True
            return None , False 
        elif len(expr.exprs) == 0:
            return None, False 
        else:
            rets = expr.exprs
            m = 0
            val = rets[0] 
            if isinstance (rets[0], str):
                print "HERE"
                return None, False
            for i in range (m+2,len (rets),2):
                val2 = rets[i]
                try:
                    val = evaluate_string( str(val) +  expr.exprs[i-1] +str(val2))
                    if val == None:
                        return None, False      
                except Exception: 
                    return None, False      
            return val,True
    return None,False
    
def try_eval_post_func(program,memory):
    if isinstance(program,VarDeclaration):
        memory.append((program.var,program.expr))
    if isinstance(program,Expr):
        e,suc=try_eval_expr(program,memory)
        if suc:
            if isinstance(program.parent,Expr):
                i = program.parent.exprs.index(program) 
                program.parent.replace(i, e)
            if isinstance(program.parent,Listarguments):
                i = program.parent.args_list.index(program) 
                program.parent.replace(i, e)
            if isinstance(program.parent,Statements):
                i = program.parent.statements_list.index(program) 
                ex = e
                program.parent.replace(i, ex)
    return [] , memory

if __name__ == "__main__":
    e1 = Expr([Number("45.4"),'+',Number('3')])
    e1 = try_eval_expr(Expr([Number("45.4"),'+',Number('3')]),[])

    print str(e1)
    print try_eval_expr(e1,[])
    e2 = Expr([Number("45.4"),'+',Expr([Number("3"),"*",Number(10),"/",Number(2)])])

    print str(e2)
    print try_eval_expr(e2,[])


