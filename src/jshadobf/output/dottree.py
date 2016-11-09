import os
import sys
import pydot
import copy

from jshadobf.common import * 
from jshadobf.common.classes import Ident,Number,List,String,Lfalse,Ltrue,Index
from jshadobf.common.tree_walker import walker

HAS_BOUNDED_DEPTH = ["Listarguments","Ident","VarDeclaration","Var","Functioncall","Number","List","String","Assignement","Expr"]
HAS_PREDICATE =["While","If","Ifelse"]
TO_SMALLPRINT = [Ident,Number,List,String,Lfalse,Ltrue,Index]

def gen_dot_file(program_tree,filename=""):
  
    if filename == "":
        ld = os.listdir(".")
        num = 0
        filename =  "dottree_%03d.dot" % num 
        while filename in ld:
            num = num + 1
            filename = "dottree_%03d.dot" % num 
    s = gen_dot(program_tree)
    fi = open(filename ,"w")
    fi.write (s)
    fi.close()
    return 

def gen_dot(program_tree):
    p = copy.deepcopy(program_tree)
    g=pydot.Graph (name = "Tree")
    nodelist=[]
    walker(p,function=tree_dumper,arg=(g,nodelist))
    return g.to_string()

def get_indice((g,nodelist),string):
    return len(nodelist)

def get_name_indice((g,nodelist),string):
    num = get_indice((g,nodelist),string)
    return string+"%d"%num

def add_edge_and_node((g,nodelist),program,label):
    n = pydot.Node(name=program.nodename,label=label)
    nodelist.append({"node":n,"name":program.nodename})
    g.add_node(n)
    if program.parent != None:
        g.add_edge(pydot.Edge(src=program.parent.nodename,dst=program.nodename))  

def tree_dumper(program,(g,nodelist)):
    class_name = program.__class__.__name__
    if program.__class__ in TO_SMALLPRINT :
        program.nodename = get_name_indice((g,nodelist),class_name+"_")
        add_edge_and_node((g,nodelist),program,"'%s :%s'" % (class_name,program.smallprint()))
    else:
        program.nodename = get_name_indice((g,nodelist),class_name+"_")
        add_edge_and_node((g,nodelist),program,"\"%s\""%class_name)
    return [],(g,nodelist)

def cfg_dot_generate_edges(cfg,g):
    for (text,el) in cfg.list_of_elements:
        map (lambda x: g.add_edge(pydot.Edge(src="%s_%d" %(text,id(el)),dst="%s_%d" %(x.text,id(x)))),el.possible_next_steps)

def cfg_dot_generate_nodes(cfg,g,allnames=[]):
    for (text,el) in cfg.list_of_elements:
        label = el.element.smallprint()
        label = label.replace("\"","'") 
        label = "\""+ label +"\""
        name = "%s_%d" %(text,id(el))
        if not name in allnames:
            g.add_node(pydot.Node(name=name ,label=label))
      
def cfg_dot(cfg,g=None):
    if g == None:
        g=pydot.Graph (name = "Tree")
    index = 0
    allnames = []
    for ccfg in cfg.functions:
        functionname = "%s" % ccfg.function_element.element.smallprint()
        subg = pydot.Subgraph("cluster_%d%d"%(id(ccfg), index), label="%s"% functionname,color="black") 
        subg = cfg_dot(ccfg,subg)
        index = index + 1  
        cfg_dot_generate_nodes(ccfg,subg,allnames)
        allnames =allnames + map ( lambda x: x.get_name() , subg.get_node_list())
        g.add_subgraph(subg) 
    cfg_dot_generate_nodes(cfg,g,allnames)
    cfg_dot_generate_edges(cfg,g)
    return g

def cfg_dot_file(cfg_tree,filename=""):
    if filename == "":
        ld = os.listdir(".")
        num = 0
        filename =  "dottree_%03d.dot" % num 
        while filename in ld:
            num = num + 1
            filename = "dottree_%03d.dot" % num 
    cfg = cfg_dot(cfg_tree)
    s = cfg.to_string()
    fi = open(filename ,"w")
    fi.write (s)
    fi.close()
    return filename

def cfg_png_file(cfg_tree,filename=""):
    fn = cfg_dot_file(cfg_tree,filename=filename) # ,withsubgraph=withsubgraph)
    os.system("dot -Tpng -o %s %s" % (fn.replace(".dot",".png"),fn) )
    return 
