from jshadobf.common.classes import *
from jshadobf.common.finder import getfirstident
import tree_walker
import cPickle

verbose = 1
import random

HAS_BEEN_ASSIGNED = 1

def deepcopy(d):
    return cPickle.loads(cPickle.dumps(d, -1))

class jshadobf_random():
    @staticmethod
    def randrange(f, t):
        return random.randrange(f,t)
    
    @staticmethod
    def randint(f, t):
        return random.randint(f,t)

    @staticmethod
    def shuffle(l):
        return random.shuffle(l)

    @staticmethod
    def random():
        return random.random()

    @staticmethod
    def choice(l):
        return random.choice(l)

    @staticmethod
    def gauss(x, sig2):
        return random.gauss(x, sig2)

    @staticmethod
    def seed (seed):
        return random.seed(seed)


def global_counter_gen():
    i = 0
    while 1:
        yield i
        i+=1 
global_counter = global_counter_gen()


class jshadobf_random_fake():

    @staticmethod
    def randrange( f, t=None):
        if t is None:
            t = f
            f = 0
        return f + (next(global_counter) % (t-f))

    @staticmethod
    def randint(f, t):
        return f + (next(global_counter) % (t-f+1))

    @staticmethod
    def shuffle(l):
        return l

    @staticmethod
    def random():
        return (next(global_counter) % 1000 / 1000.)

    @staticmethod
    def choice(l):
        i = next(global_counter)%len(l) 
        return l[i]

    @staticmethod
    def gauss(x, sig2):
        return x

    @staticmethod
    def seed (seed):
        return 


def check_depth_type(program, depth, t):
    p = program
    for i in range(depth):
        if p.parent is not None:
            p = p.parent
    if isinstance(p, t):
        return True
    return False

def ident_is_functioncall(program):
    return check_depth_type(program, 3, Functioncall)

def ident_is_function(program):
    return (check_depth_type(program, 1, Ident) and
        check_depth_type(program, 2, Function))

def ident_is_suffix(program):
    return check_depth_type(program, 2, Suffix)

def ident_is_property(program):
    return check_depth_type(program, 1, Property)

def ident_is_propertyname(program):
    return check_depth_type(program, 1, PropertyName)

def ident_is_in_this_property(program):
    return (check_depth_type(program, 1, Property) and
        check_depth_type(program, 2, MemberExpr) and
        isinstance( program.parent.parent.expr,  Expr) and
        isinstance( program.parent.parent.expr.exprs[0], This))

def ident_is_in_prototype_property(program):
    return  (check_depth_type(program, 1, Property) and
        check_depth_type(program, 2, MemberExpr) and
        isinstance( program.parent.parent.expr,  MemberExpr) and
        isinstance( program.parent.parent.expr.suffix_list[0], Property) and
        program.parent.parent.expr.suffix_list[0].name.name == "prototype")

def ident_is_in_left_handside_assignment(program):
    p = program
    while p.parent != None:
        if isinstance(p.parent, Assignment) and p == p.parent.var:
            return p.parent
        if p.parent.__class__ in [Function, Statements, Program]:
            return False
        p = p.parent
    return False

def ident_in_index(program):
    p = program
    while p.parent != None:
        if isinstance(p.parent, Index) :
            return p.parent
        if p.parent.__class__ in [Function, Statements, Program]:
            return False
        p = p.parent
    return False

def position_in_exprstatement(program, p=0):
    if program.parent != None:
        if isinstance(program.parent, Expr):
            if len(program.parent.exprs) > 2 :
                if program.parent.exprs[1] == ", ":
                    return program.parent.exprs.index(program)
        if isinstance(program.parent, Statements):
            return 0
        return position_in_exprstatement(program.parent)
    return None

def is_function_inside(program):
    return is_element_inside(program, Function)

def is_break_inside(program):
    return is_element_inside(program, Break)

def is_break_inside_weak(program):
    return is_element_inside(program, Break,[Function,Switch])

def is_functioncall_inside(program):
    return is_element_inside(program, Functioncall)

def is_return_inside(program):
    return is_element_inside(program, Return, [Function])

def check_tree (tree):
    children = tree.getChildren()
    err = ""
    for child in children:
        if child.parent != tree:
            err += "\n" + "0x%x  != 0x%x" % (id(child.parent),id(tree))
            err += "\n" + "%s 's parent != %s" % (format(child),format(tree))
        err += check_tree(child)
    return err

def is_element_inside(program, typeof, stopcase=[]):
    if program.__class__ in  stopcase:
        return False
    ss = program 
    if not isinstance(program, list):
        ss = program.getChildren()
    if isinstance(program, typeof):
        return True
    for s in ss :
        if is_element_inside(s, typeof,stopcase):
            return True
    return False

def removeindex(program):
    ret , arg = tree_walker.walker(program=program, function=removeindex_func)

def removeindex_func(program, arg):
    if isinstance(program, MemberExpr):
        inds = range(len(program.suffix_list))
        inds.reverse()
        for i in inds:
            if isinstance(program.suffix_list[i], Index):
                del program.suffix_list[i]
    return [] ,  arg
  
def include_ident(listoftuple, ident):
    if listoftuple.has_key(ident.name):
        listoftuple[ident.name].append(ident)
    else:
        listoftuple[ident.name] = [ident]

def detect_presence_func(parse_tree ,  args):
    if args == None:
        return [], None
    if isinstance(parse_tree, This):
        args["this_present"] = True
    if isinstance(parse_tree, Break):
        args["break_present"] = True
    if isinstance(parse_tree, Ident):
        if parse_tree.name == "eval":
            args["eval_present"] = True
        if parse_tree.name == "arguments":
            args["arguments"] = True
    return [] ,  args

def detect_presence(functionorlist):
    walk_condition = lambda x, y:not isinstance(x, Function)  or y["function_init"] == x
    if type(functionorlist) != list:
        functionorlist = [functionorlist]
    args={"this_present":False, "break_present":False, "eval_present":False, "function_init":functionorlist,"arguments":False}
    for s in functionorlist:
        ret ,  args = tree_walker.walker(s, detect_presence_func, arg=args, walk_condition=walk_condition)
    if type(functionorlist) != list:
        functionorlist = [functionorlist]
    for s in functionorlist:
        ret ,  args = tree_walker.walker(s, detect_presence_func, arg=args, walk_condition=walk_condition)
    return args

def examine_function_vars_func(parse_tree ,  args):
    if args == None:
        return [], None
    if parse_tree == args ["till"]:
        args["continue"] = False
        return [], args
    if parse_tree.__class__ in [VarDeclaration, Function, CatchClause]:
        ident = None
        assigned = False
        if isinstance(parse_tree, CatchClause):
            ident = parse_tree.ident
        if isinstance(parse_tree, VarDeclaration):
            ident = parse_tree.var
            assigned = parse_tree.expr != None
        if isinstance(parse_tree, Function):
      #~ args["functions"].append(parse_tree)
            if parse_tree != args["function_init"]:
                ident = parse_tree.ident
            if parse_tree == args["function_init"]:
                for v in parse_tree.args_dec.args_list :
                    include_ident(args["var_dec"], v)
        if ident != None:
            if (not ident_is_property(ident)) and (not ident_is_propertyname(ident)):
                if assigned:
                    include_ident(args["var_dec_and_assigned"], ident)
                else:
                    include_ident(args["var_dec"], ident)
    if isinstance(parse_tree, Ident):
        if (not ident_is_property(parse_tree)) and (not ident_is_propertyname(parse_tree)) : #and not ident_is_function(program) :
            a= ident_is_in_left_handside_assignment(parse_tree) 
            if not a or a.typeof != "=":
                include_ident(args["ref"], parse_tree)
            else:
                if ident_in_index(parse_tree):        
                    include_ident(args["ref"], parse_tree)
    return [] ,  args

def examine_function_vars_func_post(parse_tree ,  args):
    if isinstance(parse_tree, Assignment):
        ident = getfirstident(parse_tree)
        if (not ident_is_property(ident)) and (not ident_is_propertyname(ident)) : #and not ident_is_function(program) :
            if parse_tree.typeof != "=":
                include_ident(args["ref"], ident)
            if not args["ref"].has_key(ident.name):
                include_ident(args["decassignment"], ident) 
            include_ident(args["assignment"], ident)
    return [] ,  args

def examine_function_vars(functionorlist, tillencounter=None):
    walk_condition = lambda x, y:y["continue"] and not x.__class__ in [Try,CatchClause,FinallyClause] and (not isinstance(x, Function)  or y["function_init"] == x)
    args={"function_init":functionorlist, "var_dec":{}, "var_dec_and_assigned":{}, "ref":{}, "thisdotref":{}, "assignment":{}, "decassignment" : {}, 
           'continue' :True,  "till":tillencounter}
    if type(functionorlist) != list:
        functionorlist = [functionorlist]
    for s in functionorlist:
        ret ,  args = tree_walker.walker(s, examine_function_vars_func, examine_function_vars_func_post, arg=args, walk_condition=walk_condition)
    local_var = {}
    for k in  args ["var_dec"].keys():
        local_var[k] = [{"has_been_assigned":False}] +args ["var_dec"][k]
    for k in args ["var_dec_and_assigned"].keys():
        local_var[k]= [{"has_been_assigned":True}] +args ["var_dec_and_assigned"][k]
    for k in args["ref"].keys():
        if local_var.has_key(k):
            local_var[k] += args["ref"].pop(k)
    for k in args["assignment"].keys():
        if local_var.has_key(k):
            local_var[k] += args["assignment"].pop(k)
            local_var[k][0]["has_been_assigned"] = True 
    set_before_ref = args["decassignment"]
    for k in set_before_ref.keys():
        set_before_ref[k] = [{}] +set_before_ref[k]
    var_global_ref = args["ref"]
    for k in var_global_ref.keys():
        var_global_ref[k] = [{}] +var_global_ref[k]
    var_global_set = args["assignment"]
    for k in var_global_set.keys():
        var_global_set[k] = [{}] +var_global_set[k]
    if isinstance(functionorlist, Program):
        for k in var_global_set.keys():
            if local_var.has_key(k):
                local_var[k] += var_global_set [k]
            else:
                local_var[k] = var_global_set [k]
        var_global_set = {}
    return {"local_var":local_var, "var_global_ref":var_global_ref, "var_global_set":var_global_set, "thisdotref":args["thisdotref"]}
