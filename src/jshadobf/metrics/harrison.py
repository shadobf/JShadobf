from jshadobf.common.classes import *
from jshadobf.common.tree_walker import walker

INCREASE = [If, While, Switch, For,Function]

def compute_harrison(l):
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

def harrison(program_tree):
    l,a = walker(program_tree,harrison_func,harrison_post_func,arg=[0])
    if len (l)>0:
        s = max (l)
    else :
        s = 0
    return s

def harrison_func(program,arg=[0]):
    if program.__class__ in INCREASE:
        return [arg[0]+1], [arg[0]+1]
    return [],arg

def harrison_post_func(program,arg=[0]):
    if program.__class__ in INCREASE:
        return [], [arg[0]-1]
    return [],arg

