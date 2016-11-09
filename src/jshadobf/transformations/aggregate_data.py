#!/usr/bin/env python
#-*- coding:utf-8 -*-



import sys
import copy

from common import *
import copy
from jshadobf.common.classes import Number,Functioncall,Expr,Ident
from jshadobf.common.common import *
from jshadobf.common.finder import get_all_ident,get_upper_statement_and_pos
from jshadobf.common.common import deepcopy
from jshadobf.common.tree_walker import walker

def aggregate_data(program_tree,verbose=0,numbermax=NUMBERMAX):
    if verbose >1:
        print "apply aggregate_data transformation"
    p = deepcopy(program_tree)
    ret = get_all_ident(program_tree)
    arg={"ident_present":ret,"numbermax":numbermax,"list_aggregation":[]}
    arg["size"]=count_object(p,[Number])
    walker(p,aggregate_data_func,aggregate_data_post_func,arg=arg)
    return p
  
  


def aggregate_data_func(program,arg):
    if isinstance(program,Program) or isinstance(program,Function):
        arg["list_aggregation"].append([])
    if isinstance(program,Number):
        if shouldi(arg=arg):
            arg["list_aggregation"][-1].append(program)
    if isinstance(program,String):
        if shouldi(arg=arg):
            arg["list_aggregation"][-1].append(program)


    return [] , arg

def permute_list(l,permutations):
    newl = []
    for i in range(len(l)):
        newl.append(l[permutations[i]])
    return newl 
    
    


def aggregate_data_post_func(program,arg):
    if program.__class__ in [Program,Function]:
        l = arg["list_aggregation"].pop()
        perm = random_list_int_exclusive(0,len(l)-1)
#        perm = range(0,len(l))
        newl = deepcopy(l)
        newl = permute_list(newl,perm)
        vardeclist,name=genVarNotIn(arg["ident_present"],List(newl))
        i = 0
        for item in l:
            item.parent.replace_item(item,Expr([Ident(name),Index(Number(perm.index(i)))]))
            i += 1
        program.statements.insert(0,vardeclist)
#  #      if vardeclist != None:
#  #      s.statements_list.insert(pos,Statement_plus_ending(Statements([Assignment(Var(Ident(name)),"=",program.expr)])))
#                s.insert(whereto,vardeclist)
#                if isinstance(program.parent,Expr):
#                    program.parent.replace_expr(program, Expr([Ident(name)]))
                        
    return [] , arg

