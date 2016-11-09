from jshadobf.common.classes import Ident,Function,Program
from jshadobf.common.tree_walker import walker
from jshadobf.common.common import deepcopy,examine_function_vars, jshadobf_random
from jshadobf.common.finder import get_all_ident
from jshadobf.transformations.common import NUMBERMAX, count_object, shouldi

def getnewname(listtoavoid):
    def gennewname2(i):
        return "a%d"%jshadobf_random.randint(0,(i+1)*20)
    newname = ""
    whole_list = listtoavoid
    while (newname in whole_list)   or newname == "":
        newname = gennewname2(len( whole_list))
    listtoavoid.append(newname)
    return newname[:]

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

def rename_variables(program_tree,verbose=0,numbermax=NUMBERMAX):
    if verbose >1:
        print "apply rename_variables transformation"
    p = deepcopy(program_tree)
    ret = get_all_ident(program_tree)
    if "eval" in ret:
        return program_tree
    arg={"idents":ret,"switcher":[],"numbermax":numbermax}
    arg["size"]=count_object(p,[Ident])
    walker(p,rename_variables_func,rename_variables_post_func,arg=arg)
    return p

def rename_variables_func(parse_tree,args):
    if parse_tree.__class__ in [Function,Program]:
        args["switcher"].append([])
        examine = examine_function_vars (parse_tree)
        for k in  examine["local_var"].keys():
            ret = get_tuple_by_name_from_database(k,args["switcher"])
            if ret :
                kk , newname = ret
                for i in examine["local_var"][k][1:]:
                    i.name = newname
            else:    
                if shouldi(arg=args):
                    newname = getnewname(args["idents"])
                    for i in examine["local_var"][k][1:]:
                        i.name = newname
                    args["switcher"][-1].append((k,newname))
        d = examine["var_global_ref"]
        for k in examine["var_global_set"].keys():
            if d.has_key(k):
                d[k] += examine["var_global_set"][k][1:]
            else:
                d[k] =  examine["var_global_set"][k][1:]
        for k in  d.keys():
            ret = get_tuple_by_name_from_database(k,args["switcher"])
            if ret:
                dummy,n = ret
                for i in d[k][1:]:
                    i.name = n
    return [] , args

def rename_variables_post_func(parse_tree,args):
    return [] , args

