from jshadobf.common.classes  import *
from jshadobf.common.finder import *

from jshadobf.common.tree_walker import *
from jshadobf.common.colors import BLACK, RED
from jshadobf.parser.JavaScriptParser import VariableDeclarationList
import sys

SEQUENTIALY = [Expr , MemberExpr,Listarguments,Suffix,Index,Functioncall,VariableDeclarationList,
                   Return,Assignment,Statements,VarDeclaration,Var]

class Cfg_element:
    text = ""
    index = 0
    possible_next_steps = []
    previous_steps = []
    element = None
    def __init__(self,element):
        self.possible_next_steps = []
        self.element = element
        self.text = element.text
  
class Cfg:
    list_of_elements = []
    entrypoint = None
    endpoints = []
    functions = []
    function_element = None
  
    def __init__(self,entrypoint,cfgs=[], function_element = None):
        self.list_of_elements = []
        self.functions = []
        self.entrypoint=entrypoint
        self.cfgs = cfgs
        self.add_element(self.entrypoint)
        self.endpoints = []
        self.function_element = function_element

    def add_element(self,cfg_element):
        self.list_of_elements.append((cfg_element.text,cfg_element))

    def new_index(self,class_name):
        return len(filter(lambda x: x[0] == class_name, self.list_of_elements))

    def get_element(self,element):
        el = filter(lambda x: x[1].element is element, self.list_of_elements)
        if len(el) == 1:
            return el[0][1]
        return None

    def get_cfg_function(self,element):
        f = filter(lambda x: x.function_element.element is element, self.functions)
        if len(f) == 1:
            return f[0]
        return None

    def __str__(self):
        depth = 0
        stack = [(self.entrypoint,depth)] 
        s = ""
        while len(stack) != 0:
            (el,depth) = stack.pop()
            s = s + depth*"  " + el.element.smallprint() + "\n"
            if el.element.__class__ == Function:
                cfg = self.get_cfg_function(el.element)
                s = s + "********\n%s\n********\n" % cfg
            for nel in el.possible_next_steps:
                stack.append((nel,depth+1))
        return s        


def continue_cfg(program,arg):
    if program.__class__ != Function:
        return True
    return False

def cfg_builder(program):
    ret , arg = walker(program,function=cfg_builder_func,arg=None,walk_condition=continue_cfg)
    return arg

def cfg_builder_func(program,cfg=None):
    if program.__class__ == While:
        el = cfg.get_element(program)
        cel = Cfg_element(program.predicate)
        cfg.add_element(cel)   
        cel.possible_next_steps = el.possible_next_steps[:]
        el.possible_next_steps = [cel]
        el = cel
        tel = Cfg_element(program.statements)
        cfg.add_element(tel)
        old = el.possible_next_steps[:]
        el.possible_next_steps = [tel] + old[:]
        tel.possible_next_steps = [el] +  old[:]
        if el in cfg.endpoints:
            cfg.endpoints.append(tel)
        return [] , cfg
    if program.__class__ == For:
        el = cfg.get_element(program)
        initel = Cfg_element(program.initpart)
        cfg.add_element(initel)   
        initel.possible_next_steps = el.possible_next_steps[:]
        olds = el.possible_next_steps[:]
        el.possible_next_steps = [initel]
        e1el = Cfg_element(program.expr1)
        cfg.add_element(e1el)
        e1el.possible_next_steps = initel.possible_next_steps[:] + olds[:]
        initel.possible_next_steps = [e1el]
        sel = Cfg_element(program.statements)
        cfg.add_element(sel)
        e2el = Cfg_element(program.expr2)
        cfg.add_element(e2el)
        e1el.possible_next_steps.append(sel)
        old = e1el.possible_next_steps[:]
        sel.possible_next_steps = [e2el]
        e2el.possible_next_steps = [e1el]
        if el in cfg.endpoints:
            del cfg.endpoints[cfg.endpoints.index(el)]
            cfg.endpoints.append(program.expr1)
        return [] , cfg
    if program.__class__ == If:
        el = cfg.get_element(program)
        cel = Cfg_element(program.predicate)
        cfg.add_element(cel)   
        cel.possible_next_steps = el.possible_next_steps[:]
        el.possible_next_steps = [cel]
        tel = Cfg_element(program.statementstrue)
        cfg.add_element(tel)
        old = el.possible_next_steps[:]
        tel.possible_next_steps = old[:]
        if program.statementsfalse != None :
            el.possible_next_steps = [tel]
            fel = Cfg_element(program.statementsfalse)
            cfg.add_element(fel)
            el.possible_next_steps.append(fel)
            fel.possible_next_steps = old[:]
        else:
            el.possible_next_steps.append(tel)
        if el in cfg.endpoints:
            cfg.endpoints.remove(el)
            cfg.endpoints.append(tel)
            if program.statementsfalse != None :
                cfg.endpoints.append(fel)
        return [] , cfg
    if program.__class__ == Program:
        entrypoint = Cfg_element(program)
        cfg = Cfg(entrypoint)
        el = entrypoint
        for s in program.statements_list:
            sel = Cfg_element(s)
            cfg.add_element(sel)
            el.possible_next_steps.append(sel)
            el = sel
        cfg.endpoints.append(el)
        return [] , cfg
    if program.__class__ in SEQUENTIALY:
        iel = cfg.get_element(program)
        if iel == None:
            iel = Cfg_element(program)
            cfg.add_element(iel)
        el = iel
        initnextstep = iel.possible_next_steps[:]
        iel.possible_next_steps = []
        for s in program.getChildren():
            sel = Cfg_element(s)
            cfg.add_element(sel)
            el.possible_next_steps.append(sel)
            el = sel
        if iel in cfg.endpoints:
            cfg.endpoints.remove(iel)
            cfg.endpoints.append(el)
        el.possible_next_steps = initnextstep[:]
        return [] , cfg
    if program.__class__ == Function:
        function_element = cfg.get_element(program)
        if function_element == None:
            print RED,program.smallprint(),BLACK
            sys.exit(0)
        entrypoint = Cfg_element(program.statements)
        ccc = Cfg(entrypoint,  function_element=function_element)
        ret , ccc = walker(program.statements,function=cfg_builder_func,arg=ccc,walk_condition=continue_cfg)
        cfg.functions.append(ccc)
        return [] , cfg
    return [],cfg




