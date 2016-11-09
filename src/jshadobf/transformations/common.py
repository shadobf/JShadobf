from jshadobf.common.classes import VarDeclaration,Ident,Var
from jshadobf.common.common import *
from jshadobf.common.finder import *
from jshadobf.common.tree_walker import walker

COMPARATORS =   [ "==" ,  "<=" ,">=","!=","<",">"]
MAXI = 10**4
MAXILEN = 10
NUMBERMAX = 5

class TransformationUnavailable(Exception):
    pass


def get_transformation_by_name(name, transformations_available):
    print name, transformations_available
    transfos = filter(lambda x: x.__name__ == name,transformations_available)
    if len(transfos) >= 1:
        return transfos[0]
    raise TransformationUnavailable(name)


def random_range_exlusif(int_from, int_to , list_exclusion=[]):
    while True:
        r = jshadobf_random.randrange(int_from,int_to)
        if not r in list_exclusion:
            return r

def random_list_int_exclusive(min,max,length=None,list_exclusion=[]):
    l = range(min,max+1)
    for i in list_exclusion:
        if i in l :
            del l[l.index(i)]
    if length == None:
        length = len(l)
    lis = []
    for i in xrange(length):
        ind = jshadobf_random.randrange(0,len(l))
        lis.append(l[ind])
        del l[ind]
    return lis

def genPredicate_1(program,true_or_false=None):
    if true_or_false == None:
        true_or_false = True if jshadobf_random.randint(0,1) else False
    rl = random_list_int_exclusive(0,1000,length=jshadobf_random.randint(2,20))
    l = List(map(lambda x:Number("%d"%x),rl))
    while True:
        swap = jshadobf_random.randint(0,1)
        another = jshadobf_random.randint(0,1)
        ind = jshadobf_random.randrange(0,len(rl))
        comp = COMPARATORS[jshadobf_random.randrange(0,len(COMPARATORS))]
        if another:
            num = jshadobf_random.randrange(0,1000)
        else:
            num = rl[jshadobf_random.randrange(0,len(rl))]
        n1 = rl[ind]
        n2 = num
        if swap:
            n1,n2=n2,n1
        if eval("%d"%n1 + comp + "%d"%n2) == true_or_false:
            break
    if swap:
        exprs = Expr([Number(num),comp, Expr([l,Index(Number(ind))])])
    else:
        exprs = Expr([Expr([l,Index(Number(ind))]) , comp, Number(num)])
    return exprs

def genPredicate(program,true_or_false=None):
    Pred_true_false = [genPredicate_1]
    Pred_None = [genPredicate_0,genPredicate_1]
    if true_or_false != None:
        return jshadobf_random.choice(Pred_true_false)(program, true_or_false)
    return jshadobf_random.choice(Pred_None)(program)
    
def genPredicate_0(program,true_or_false=None):
    upfunc =get_upper_function(program)    
    examine_func = examine_function_vars ( upfunc  )
    e = gen_dummy_expr(vartoass=None)
    return e

def count_object(p,list_obj):
    arg = {}
    arg["size"] = 0
    arg["tocount"] = list_obj
    walker(p,function=count_object_func,arg=arg)
    return arg["size"]

def count_object_func(program,arg):
    if program.__class__ in arg["tocount"]:   
        arg["size"]+=1
    return [],arg

def shouldi(oneover=5,arg=None):
    if arg == None:
        ans = jshadobf_random.randint(0,oneover) == 0
        return ans
    if not arg["size"]:
        return False
    r = jshadobf_random.randint(0,arg["size"])
    arg["size"] -= 1
    ans=False
    if not arg.has_key("done"):
        arg["done"]= 0
    if (arg["numbermax"] - arg["done"] ) > r :
        arg["done"] += 1
        ans=True
    return ans
  
def genVarNotIn(varnames,expr =None):
    i = jshadobf_random.randint(0,100*len(varnames))
    name = "dummyvar%d"% i  
    while name in varnames:
        i = jshadobf_random.randint(0,100*len(varnames))
        name = "dummyvar%d"% i
    varnames.append(name)
    return Var([VarDeclaration(Ident(name),expr)]),name

def gen_word():
    w = "".join([chr(97+jshadobf_random.randint(0,25)) for i in xrange(8)])
    return w

def pick_num():
    if shouldi(2):
        return Number(jshadobf_random.randint(-MAXI,MAXI))
    return Number((jshadobf_random.random()-.5 )* MAXI *2)

def pick_list():
  #~ print "genlist"
    l = jshadobf_random.randint(0,MAXILEN)
    return List([ pick_type([pick_num,pick_string,pick_bool]) for i in xrange(l)])

def pick_string():
    l = jshadobf_random.randint(0,MAXILEN)
    return String(repr(" ".join([str(gen_word()) for i in xrange(l)])))

def pick_bool():
    return pick_one([Ltrue,Lfalse])()

def pick_type(types=[pick_num,pick_list,pick_string,pick_bool]):
    return pick_one(types)()

def pick_one(mylist):
    return mylist[jshadobf_random.randrange(0,len(mylist))]

def gen_dummy_expr(vartoass=None,i = 0):
    operators = ['+','-','*','/',"%",">>" ,'<<'   ]
    compoperators = ['==' , '!='  ,'<' , '>' , '<=' , '>=' ]
    booleanbit = [ "&&" ,"&" ,"||" ,"|" , "^" ]
    possop = operators + booleanbit + compoperators
    expr = Expr([pick_type()])
    if vartoass != None:
        expr = Assignment(Expr([Ident(vartoass)]),"=",expr)
    return expr


