from jshadobf.common.colors import BLACK, RED

class Selfsmallprinter():
    def smallprint(self):
        return ("%s" % str(self)).replace("\n","")

class Onelineisstr():
    def oneline_str(self):
        return ("%s" % str(self)).replace("\n","")

class Textsmallprinter():
    def smallprint(self):
        return "%s" % self

class Nonesmallprinter():
    def smallprint(self):
        return "" 

class Getliner():
    def getLine(self):
        return self.line

def through_exp(arg,condition):
    if isinstance ( arg , Expr):
        if len(arg.exprs) == 1:
            return through_exp(arg.exprs[0],condition)
        else:
            return False
    if isinstance(arg, MemberExpr):
        if len(arg.suffix_list) == 0:
            return through_exp(arg.expr,condition)
        else:
            return False
    return condition(arg)

def cleaner(obj):
    if getattr(obj,"getChildren"):
        for c in list(obj.getChildren()):
            cleaner(c)
            c.parent = None

class Expr(object, Selfsmallprinter,Getliner):
    text = "Expr"
    parent= None
    operator = ""
    line = -1
    exprs = []

    def __init__(self, exprs=[]):
        self.exprs = exprs[:]
        for i in range(len(self.exprs)):
            if (not isinstance(self.exprs[i],str)) and (not isinstance(self.exprs[i],unicode)):
                self.exprs[i].parent = self 

    def insert(self, index=0,value=None):
        self.exprs.insert(index,value)
        value.parent = self         

    def replace(self, index=0,value=None):
        self.exprs[index] = value
        value.parent = self

    def index(self, item):
        return self.exprs.index(item)

    def replace_item(self, item,value):
        index = self.index(item)
        self.exprs[index]=value
        value.parent = self

    def replace_expr(self, efrom=None,value=None):
        index = self.exprs.index(efrom)
        self.exprs[index] = value
        value.parent = self

    def __str__(self):
        if len(self.exprs) ==0:
            return ""
        pb,pe = "",""
        if len(self.exprs) != 1 and not isinstance(self.parent,Statements):
            pb,pe = "(",")"
        expr = []
        for e in self.exprs:
            if e == "-":
                expr.append(" - ")
            else :
                expr.append(e)
        return pb + " ".join(map(format,expr)) + pe
    
    def oneline_str(self):
        if len(self.exprs) ==0:
            return ""
        pb,pe = "",""
        if len(self.exprs) != 1 and not isinstance(self.parent,Statements):
            pb,pe = "(",")"
        expr = []
        for e in self.exprs:
            if e == "-":
                expr.append(" - ")
            else :
                if "oneline_str" in dir(e):
                    expr.append(e.oneline_str())
                else:
                    expr.append(e)
        return pb + " ".join(map(format,expr)) + pe
    
    def getChildren(self):
        return filter (lambda x : type(x) != str and  type(x) != unicode, self.exprs)


class Var(object, Selfsmallprinter,Getliner):
    text = "Var"
    parent= None
    args_dec_list =[] # VarDeclaration()
    line = -1

    def __init__(self,args_dec_list=[]):
        self.args_dec_list = args_dec_list[:]
        for l in self.args_dec_list:
            l.parent = self

    def __str__(self):
        if self.args_dec_list != []:
            return "var " + ",".join(map(lambda x : "%s"%x,self.args_dec_list)) #+";"
        return ""

    def oneline_str(self):
        if self.args_dec_list != []:
            return "var " + ",".join(map(lambda x : "%s"%x.oneline_str(),self.args_dec_list)) #+";"
        return ""

    def insert(self, index=0,value=None):
        self.args_dec_list.insert(index,value)
        value.parent = self

    def replace(self, index=0,value=None):
        self.args_dec_list[index]=value
        value.parent = self

    def getChildren(self):
        return self.args_dec_list


class Statements(object, Textsmallprinter,Getliner):
    text = "Statements"
    parent= None 
    statements_list = []
    line = -1

    def __init__(self, l=[]):
        self.statements_list = l[:]
        for s in self.statements_list:
            s.parent = self

    def oneline_str(self):
        string = ""
        for s in self.statements_list:
            if not through_exp(s,lambda x : x.__class__ in [Statements,Function,If,For,While,Switch,Try]):
                string += format(s.oneline_str()) +";"
            else:
                string += format(s.oneline_str()) +""
        ret = ""
        if self.parent.__class__ in [Program,CaseBlock] and string.strip() != "":
            ret = string
        else:
            ret = "{"+string  +"}"
        return ret

    def  __str__(self,INDENT="  "):
        string = ""
        for s in self.statements_list:
            if not through_exp(s,lambda x : x.__class__ in [Statements,Function,If,For,ForIn,While,Switch,Try]):
                if format(s).strip() !="":
                    string += format(s) +";\n"
            else:
                string += format(s) +""
        ret = ""
        string = "\n".join(map(lambda x: INDENT+ format(x),string.splitlines()))
        if self.parent.__class__ in [Program,CaseBlock] and string.strip() != "":
            ret = string
        else:
            ret = "{\n"+string  +"\n}\n"
        return ret

    def insert(self, index=0,value=None):
        self.statements_list.insert(index,value)
        value.parent = self

    def remove(self, index=0):
        del self.statements_list[index]

    def append(self, value):
        self.statements_list.append(value)
        value.parent = self

    def append_list(self, value):
        for v in value:
            self.append(v)

    def replace(self, index=0,value=Expr()):
        self.statements_list[index]=value
        value.parent = self

    def index(self,item):
        return self.statements_list.index(item)

    def replace_item(self, item,value):
        index = self.statements_list.index(item)
        self.statements_list[index]=value
        value.parent = self
      
    def replaceall(self, value=[]):
        self.statements_list = []
        for v in value:
            self.append(v)

    def getChildren(self):
        return self.statements_list


class Listarguments(object, Selfsmallprinter,Getliner):
    text = "Listarguments"
    args_list =[] # [Var()]
    parent= None
    line = -1

    def __init__(self,args_list=[]):
        self.args_list = args_list[:]
        for l in args_list:
            l.parent = self

    def __str__(self):

        return "(" + ",".join(map(lambda x : "%s"%x,self.args_list)) + ")"

    def oneline_str(self):
        return "(" + ",".join(map(lambda x : "%s"%x.oneline_str(),self.args_list)) + ")"

    def insert(self, index=0,value=None):
        self.args_list.insert(index,value)
        value.parent = self

    def replace(self, index=0,value=None):
        self.args_list[index]=value
        value.parent = self

    def replace_item(self, item,value):
        index = self.args_list.index(item)
        self.args_list[index]=value
        value.parent = self

    def getChildren(self):
        return self.args_list
    
class Ident(object, Selfsmallprinter,Getliner,Onelineisstr):
    text = "Ident"
    parent= None
    assigned = False
    name = ""
    line = -1
    
    def __init__(self,name="",assigned = False):
        self.assigned = assigned
        self.name =name 

    def __str__(self):
        return "%s" % (str(self.name))

    def getChildren(self):
        return []


class MemberExpr(object, Textsmallprinter,Getliner):
    text = "MemberExpr"
    parent= None
    suffix_list = []
    expr = None
    name = ""
    line = -1

    def __init__(self,expr=Expr(),suffix_list=[]):
        self.expr =expr
        self.expr.parent = self 
        self.suffix_list =suffix_list[:]
        for s in self.suffix_list:
            s.parent = self 

    def __str__(self):
        return "%s" % (self.expr) + "".join(map(format,self.suffix_list))

    def oneline_str(self):
        return "%s" % (self.expr.oneline_str()) + "".join(map(lambda x:x.oneline_str(),self.suffix_list))

    def getChildren(self):
        return [self.expr]+self.suffix_list

    
class Suffix(object, Nonesmallprinter,Getliner):
    text = "Suffix"
    parent= None
    suffix = None
    name = ""
    line = -1

    def __init__(self,suffix):
        self.suffix =suffix
        suffix.parent = self

    def __str__(self):
        return "%s"%self.suffix

    def oneline_str(self):
        return self.suffix.oneline_str()

    def getChildren(self):
        return [self.suffix]


class PropertyGet(object, Getliner):
    text = "PropertyGet"
    parent= None
    statements = None
    name = None
    name = ""
    line = -1

    def __init__(self,name,statements):
        self.name = name
        self.name.parent = self
        self.statements =statements
        self.statements.parent = self

    def __str__(self):
        return "get %s() {%s}"%(self.name,self.statements)

    def oneline_str(self):
        return "get %s() {%s}"%(self.name.oneline_str(),self.statements.oneline_str())

    def getChildren(self):
        return [self.name,self.statements]


class PropertySet(object, Getliner):
    text = "PropertySet"
    parent= None
    statements = None
    name = None
    ident = None
    line = -1

    def __init__(self,name,ident,statements):
        self.name = name
        self.name.parent = self
        self.ident = ident
        self.ident.parent = self
        self.statements =statements
        self.statements.parent = self

    def __str__(self):
        return "set %s(%s) {%s}"%(self.name,self.ident,self.statements)

    def oneline_str(self):
        return "set %s(%s) {%s}"%(self.name.oneline_str(),self.ident.oneline_str(),self.statements.oneline_str())

    def getChildren(self):
        return [self.name,self.ident,self.statements]


class Throw(object, Textsmallprinter,Getliner):
    text = "Throw"
    parent= None
    expr = None
    line = -1

    def __init__(self,expr):
        self.expr =expr
        self.expr.parent = self

    def __str__(self):
        return "throw %s" %self.expr

    def oneline_str(self):
        return "throw %s" %self.expr.oneline_str()

    def getChildren(self):
        return [self.expr]
  
  
class VarDeclaration(object, Textsmallprinter,Getliner):
    text = "VarDeclaration"
    parent= None
    var = None # Ident()
    line = -1
    expr = None
    dummy = False

    def __init__(self,var=Ident(),expr=None):
        self.var =var 
        self.var.parent = self
        self.expr =expr 
        if self.expr != None:
            self.expr.parent = self

    def replace_expr(self,expr):
        self.expr =expr 
        if self.expr != None:
            self.expr.parent = self

    def replace_item(self,dummy,item):
        self.replace_expr(item)
        
    def __str__(self):
        if self.expr != None:
            e = str(self.expr)
            return str(self.var) +" = "+e
        return "%s" % (self.var)    

    def getChildren(self):
        if self.expr != None:
            return [self.var,self.expr]
        return [self.var]

    def oneline_str(self):
        if self.expr != None:
            e = self.expr.oneline_str()
            return str(self.var) +" = "+e
        return "%s" % (self.var)    
    

class Return(object, Selfsmallprinter,Getliner):
    expr = None
    text = "Return"
    parent = None
    line = -1

    def __init__(self,expr=None):
        self.expr = expr
        if self.expr != None:
            self.expr.parent = self

    def __str__(self):
        if self.expr != None:
            return "return %s"%(self.expr) 
        return "return " 

    def oneline_str(self):
        if self.expr != None:
            return "return %s"%(self.expr.oneline_str()) 
        return "return " 

    def getChildren(self):
        if self.expr != None:
            return [self.expr]
        return []


class CallExpressionSuffix  (object, Selfsmallprinter,Getliner):
    text = "CallExpressionSuffix"
    parent= None
    suffix_list= None
    line = -1

    def __init__(self,suffix_list=[]):
        self.suffix_list = suffix_list
        for s in self.suffix_list :
            s.parent = self

    def __str__(self):
        return "".join(map(format,self.suffix_list))

    def oneline_str(self):
        return "".join(map(lambda x:x.oneline_str(),self.suffix_list))

    def getChildren(self):
        return self.suffix_list

 
class Functioncall(object, Selfsmallprinter,Getliner):
    text = "Functioncall"
    parent= None
    args= None
    rest= None
    memberexpr = None
    line = -1

    def __init__(self,memberexpr=MemberExpr(),args=Listarguments(),r=None):
        self.memberexpr = memberexpr
        self.memberexpr.parent = self
        self.args= args
        self.args.parent = self
        if r != None:
            if r.suffix_list == []:
                r = None
        self.rest = r
        if self.rest != None:
            self.rest.parent = self
    
    def __str__(self):
        if len(self.memberexpr.getChildren()) > 0 and isinstance(self.memberexpr.getChildren()[0],Function):
            mexp = "(%s)"%self.memberexpr
        else:
            mexp ="%s"%self.memberexpr
        ret =  "%s%s" % (mexp, self.args)
        if self.rest != None:
            ret +=  "%s" % (self.rest)
        return ret

    def oneline_str(self):
        if len(self.memberexpr.getChildren()) > 0 and isinstance(self.memberexpr.getChildren()[0],Function):
            mexp = "(%s)"%self.memberexpr.oneline_str()
        else:
            mexp ="%s"%self.memberexpr.oneline_str()
        ret =  "%s%s" % (mexp, self.args.oneline_str())
        if self.rest != None:
            ret +=  "%s" % (self.rest.oneline_str())
        return ret

    def getChildren(self):
        if self.rest != None:
            return [self.memberexpr ,self.args,self.rest]
        return [self.memberexpr ,self.args]

    
class Number(object, Selfsmallprinter,Getliner,Onelineisstr):
    text = "Number"
    parent= None
    value= None
    line = -1

    def __init__(self,value=0.0):
        self.value = value

    def __str__(self):
        return format(self.value)

    def getChildren(self):
        return []    


class RegEx(object, Selfsmallprinter,Getliner,Onelineisstr):
    text = "RegEx"
    parent= None
    value= None
    line = -1

    def __init__(self,value="//"):
        self.value = value

    def __str__(self):
        return format(self.value)

    def getChildren(self):
        return []


class NaN(object, Selfsmallprinter,Getliner,Onelineisstr):
    text = "NaN"
    parent= None
    value= "NaN"
    line = -1

    def __str__(self):
        return format(self.value)

    def getChildren(self):
        return []


class This(object, Selfsmallprinter,Getliner,Onelineisstr):
    text = "This"
    parent= None
    value= "this"
    line = -1

    def __str__(self):
        return format(self.value)

    def getChildren(self):
        return []


class List(object, Getliner):
    text = "List"
    parent= None
    value=None
    line = -1

    def __init__(self,value=[]):
        self.value = value[:]
        for v in self.value:
            v.parent = self

    def __str__(self):
        return "[%s]" % ",".join(map(lambda x : "%s"%x,self.value))    

    def oneline_str(self):
        return "[%s]" % ",".join(map(lambda x : "%s"%x.oneline_str(),self.value))    

    def getChildren(self):
        return self.value

    def insert(self,value,i,item):
        self.value.insert(i,item)
        item.parent = self

    def replace(self,value,i,item):
        self.value[i] = item
        item.parent = self

    def replace_item(self, item,value):
        index = self.value.index(item)
        self.value[index]=value
        value.parent = self

    def smallprint(self):
        return "[%s]"% ",".join(map(lambda x : str(x).replace("\"",""),self.value))  


class ListCreation(object, Selfsmallprinter,Getliner):
    text = "List"
    parent= None
    expr=None
    fors= None
    line = -1

    def __init__(self,expr,fors):
        self.expr = expr
        self.fors = fors
        self.expr.parent = self
        self.fors.parent = self

    def oneline_str(self):
        return "[%s %s]" % (self.expr.oneline_str(), self.fors.oneline_str())     

    def __str__(self):
        return "[%s %s]" % (self.expr, self.fors)   

    def getChildren(self):
        return [self.expr, self.fors]


class ObjectLiteral(object, Getliner):
    text = "ObjectLiteral"
    parent= None
    value=None
    line = -1

    def __init__(self,value=[]):
        self.value = value[:]
        for v in self.value:
            v.parent = self

    def __str__(self):
        return "{%s}" % ",".join(map(lambda x : "%s"%x,self.value))    

    def getChildren(self):
        return self.value

    def insert(self,value,i,item):
        self.value.insert(i,item)
        item.parent = self

    def replace(self,value,i,item):
        self.value[i]=item
        item.parent = self

    def replace_item(self, item,value):
        index = self.value.index(item)
        self.value[index]=value
        value.parent = self

    def oneline_str(self):
        return "{%s}" % ",".join(map(lambda x : x.oneline_str(),self.value))    
    
    def smallprint(self):
        return "{%s}"% ",".join(map(lambda x : str(x).replace("\"",""),self.value))  

    
class String(object, Selfsmallprinter,Getliner,Onelineisstr):
    text = "String"
    parent= None
    value=None
    line = -1

    def __init__(self,value=""):
        self.value = value[:]

    def __str__(self):
        return (self.value.encode("utf-8"))

    def getChildren(self):
        return []

    def smallprint(self):
        return  str(self.value)
        

class Assignment(object, Selfsmallprinter,Getliner):
    text = "Assignment"
    parent= None
    typeof = ""
    var = None
    expr = None
    line = -1

    def __init__(self,var=Expr(),typeof="=",expr=Expr()):
        self.typeof= typeof
        self.var = var
        self.var.parent = self
        self.expr = expr 
        self.expr.parent = self

    def __str__(self):
        return "(%s %s %s)" %(str(self.var),str(self.typeof ),str(self.expr))

    def oneline_str(self):
        return "(%s %s %s)" %(str(self.var.oneline_str()),str(self.typeof ),str(self.expr.oneline_str()))

    def getChildren(self):
        return [self.var, self.expr]


class Switch(object, Getliner):
    text = "Switch"
    parent= None
    caseblock = []
    expr = None
    line = -1

    def __init__(self,expr=Expr(),caseblock=[]):
        self.caseblock = caseblock[:]
        for cb in caseblock:
            cb.parent = self
        self.expr = expr 
        self.expr.parent = self

    def __str__(self):
        return "switch (%s) {%s}" %(self.expr,"".join(map(format,self.caseblock )))

    def oneline_str(self):
        return "switch (%s) {%s}" %(self.expr.oneline_str(),"".join(map(lambda x : x.oneline_str(),self.caseblock )))
    
    def getChildren(self):
        return [self.expr]+ self.caseblock

    def smallprint(self):
        return "switch (%s)" %(self.expr )


class CaseBlock(object, Getliner):
    text = "CaseBlock"
    parent= None
    line = -1
    statement = None
    expr = None

    def __init__(self,statement=Statements(),expr=None):
        self.statement = statement
        self.statement.parent = self
        if expr != None:
            self.expr = expr 
            self.expr.parent = self

    def __str__(self):
        if self.expr != None:
            return "case %s : %s" %(self.expr,self.statement )
        return "default : %s" %(self.statement )

    def oneline_str(self):
        if self.expr != None:
            return "case %s : %s" %(self.expr,self.statement.oneline_str() )
        return "default : %s" %(self.statement.oneline_str() )

    def getChildren(self):
        ret = []
        if self.expr != None:
            ret.append(self.expr)
        return ret+ [self.statement]

    def smallprint(self):
        return "case %s" %(self.expr )
    
    
class Break(object, Selfsmallprinter,Getliner,Onelineisstr):
    text = "Break"
    parent= None
    line = -1
    ident = None
    
    def __init__(self,ident = None):
        if ident != None:
            self.ident = ident
            self.ident.parent = self

    def __str__(self):
        i = ""
        if self.ident !=None:
            i = format(self.ident)
        return "break " + i #+ ";"

    def getChildren(self):
        if self.ident != None:
            return [self.ident]
        return []

    
class Continue(object, Selfsmallprinter,Getliner,Onelineisstr):
    text = "Continue"
    parent= None
    line = -1
    ident = None

    def __init__(self,ident = None):
        if ident != None:
            self.ident = ident
            self.ident.parent = self

    def __str__(self):
        i = ""
        if self.ident !=None:
            i = format(self.ident)
        return "continue " + i #+ ";"

    def getChildren(self):
        if self.ident != None:
            return [self.ident]
        return []

    
class Yield(object, Selfsmallprinter,Getliner):
    text = "Yield"
    parent= None
    line = -1
    expr = None

    def __init__(self,expr):
        self.expr = expr
        self.expr.parent = self

    def __str__(self):
        return "yield " + format(self.expr)

    def oneline_str(self):
        return "yield %s" %self.expr.oneline_str()

    def getChildren(self):
        return [ self.expr]

    
class Let(object, Selfsmallprinter,Getliner):
    text = "Let"
    parent= None
    line = -1
    vardec = None
    statement = None

    def __init__(self,vardec, statement = None):
        self.vardec = vardec
        self.vardec.parent = self
        if statement != None:
            self.statement = statement
            self.statement.parent = self

    def __str__(self):
        ret = "let "
        if self.statement !=None:
            ret += "(" + format(self.vardec) + ")" +  format(self.statement)
        else:
            ret += format(self.vardec)
        return ret

    def oneline_str(self):
        if self.statement != None:
            return "let (%s) %s" %(self.vardec.oneline_str(),self.statement.oneline_str())
        return "let %s " %self.vardec.oneline_str()

    def getChildren(self):
        ret = [self.vardec ]
        if self.statement !=None:
            ret.append(self.statement)
        return ret
    
 
class ExpressionStatement(object, Selfsmallprinter,Getliner):
    text = "ExpressionStatement"
    parent= None
    operator = ""
    line = -1
    exprs = []

    def __init__(self, exprs=[]):
        self.exprs = exprs[:]
        for i in range(len(self.exprs)):
            if type(self.exprs[i]) != str and type(self.exprs[i]) != unicode:
                self.exprs[i].parent = self 

    def insert(self, index=0,value=Expr()):
        self.exprs.insert(index,value)
        value.parent = self

    def replace(self, index=0,value=Expr()):
        self.exprs[index]=value
        value.parent = self  

    def index(self, item):
        return self.exprs.index(item)

    def replace_item(self, item,value):
        index = self.exprs.index(item)
        self.exprs[index]=value
        value.parent = self
        
    def oneline_str(self):
        return ",".join(map(lambda x : x.oneline_str(),self.exprs ))

    def __str__(self):
        return ",".join(map(format,self.exprs))

    def getChildren(self):
        return self.exprs # filter (lambda x : type(x) != str and  type(x) != unicode, self.exprs)
    
    
class Try(object, Selfsmallprinter,Getliner):
    line = -1
    parent = None
    text = "Try"
    statements = None
    clause_list = []

    def __init__(self, statements=Statements(),clause_list=None):
        self.statements = statements
        self.statements.parent = self
        self.clause_list = clause_list    
        for c in clause_list:
            c.parent = self

    def __str__(self):
        s = "try %s"  % self.statements
        for c in self.clause_list:
            s+= " %s" %c
        return s

    def oneline_str(self):
        s = "try %s"  % self.statements.oneline_str()
        for c in self.clause_list:
            s+= " %s" %c.oneline_str()
        return s

    def getChildren(self):
        ret = [self.statements] + self.clause_list
        return ret


class CatchClause(object, Selfsmallprinter,Getliner):
    line = -1
    parent = None
    text = "CatchClause"
    statements = None
    ident = None
    expr =None

    def __init__(self, ident=Ident() ,statements=Statements(),expr=None):
        self.ident = ident
        self.ident.parent = self
        if expr != None:
            self.expr = expr
            self.expr.parent = self
        self.statements = statements
        self.statements.parent = self

    def __str__(self):
        ex = ""
        if self.expr != None:
            ex= " if %s" %self.expr 
        return "catch (%s%s) %s" % (self.ident, ex , self.statements)

    def oneline_str(self):
        ex = ""
        if self.expr != None:
            ex= " if %s" %self.expr.oneline_str()
        return "catch (%s%s) %s" % (self.ident, ex , self.statements.oneline_str())

    def getChildren(self):
        ret = [self.ident,self.statements]
        if self.expr != None:
            ret.append(self.expr)
        return ret


class FinallyClause(object, Selfsmallprinter,Getliner):
    line = -1
    parent = None
    text = "FinallyClause"
    statements = None

    def __init__(self, statements=Statements()):
        self.statements = statements
        self.statements.parent = self

    def __str__(self):
        return "finally %s" % self.statements

    def oneline_str(self):
        return "finally %s" % self.statements.oneline_str()

    def getChildren(self):
        return [self.statements]


class Ternary(object, Selfsmallprinter,Getliner):
    text = "Ternary"
    parent= None
    expr = None
    exprtrue = None
    exprfalse = None
    line = -1

    def __init__(self, expr=Expr(),exprtrue=None,exprfalse=None):
        self.expr = expr
        self.exprtrue = exprtrue
        self.exprfalse = exprfalse
        self.expr.parent = self
        if self.exprtrue != None:
            self.exprtrue.parent = self
        if self.exprfalse != None:
            self.exprfalse.parent = self

    def __str__(self):
        if self.exprtrue != None:
            return "(%s?%s:%s)" %(self.expr,self.exprtrue,self.exprfalse)
        else:
            return "%s" % self.expr

    def oneline_str(self):
        if self.exprtrue != None:
            return "(%s?%s:%s)" %(self.expr.oneline_str(),self.exprtrue.oneline_str(),self.exprfalse.oneline_str())
        else:
            return "%s" % self.expr.oneline_str()

    def getChildren(self):
        ret = [self.expr]
        if self.exprtrue != None:
            ret.append(self.exprtrue)
        if self.exprfalse != None:
            ret.append(self.exprfalse)
        return ret


class UnaryExpr(object, Selfsmallprinter,Getliner):
    text = "UnaryExpr"
    parent= None
    typeof = None
    expr = None
    line = -1

    def __init__(self,typeof=None,expr=None):
        self.typeof = typeof
        self.expr = expr
        self.expr.parent = self

    def __str__(self):
        return "%s %s"%(self.typeof ,self.expr)

    def oneline_str(self):
        return "%s %s"%(self.typeof ,self.expr.oneline_str())

    def getChildren(self):
        return [self.expr]


class PropertyName(object, Selfsmallprinter,Getliner):
    text = "PropertyName"
    parent= None
    name = None
    expr = None
    line = -1

    def __init__(self,name=None,expr=None):
        self.name = name
        self.expr = expr
        if self.name != None:
            self.name.parent = self
        if self.expr != None:
            self.expr.parent = self

    def __str__(self):
        if self.expr != None:
            return "%s:%s"%(self.name ,self.expr)
        else:
            return "%s"%(self.name)

    def oneline_str(self):
        if self.expr != None:
            return "%s:%s"%(self.name.oneline_str() ,self.expr.oneline_str())
        else:
            return "%s"%(self.name.oneline_str())

    def replace_expr(self,expr):
        self.expr = expr
        if self.expr != None:
            self.expr.parent = self

    def replace_item(self,dummy,expr):
        self.expr = expr
        self.expr.parent = self

    def getChildren(self):
        if self.expr != None:
            return [self.name, self.expr]
        return [self.name]


class Property(object, Selfsmallprinter,Getliner):
    text = "Property"
    parent= None
    name = None
    line = -1

    def __init__(self,name=None):
        self.name = name
        if self.name != None:
            self.name.parent = self

    def __str__(self):
        return ".%s"%(self.name)

    def oneline_str(self):
        return ".%s"%(self.name.oneline_str())

    def getChildren(self):
        return [self.name]


class Null(object, Selfsmallprinter,Getliner,Onelineisstr):
    text = "Null"
    parent = None
    line = -1

    def __str__(self):
        return "null"

    def getChildren(self):
        return []


class Ltrue(object, Selfsmallprinter,Getliner,Onelineisstr):
    text = "True"
    value = "true"
    parent = None
    line = -1

    def __str__(self):
        return "true"

    def getChildren(self):
        return []


class Typeof(object, Selfsmallprinter,Getliner,Onelineisstr):
    text = "Typeof"
    value = "typeof "
    parent = None
    line = -1

    def __str__(self):
        return "typeof "

    def getChildren(self):
        return []


class Void(object, Selfsmallprinter,Getliner,Onelineisstr):
    text = "Void"
    value = "void "
    parent = None
    line = -1

    def __str__(self):
        return "void "

    def getChildren(self):
        return []


class Delete(object, Selfsmallprinter,Getliner,Onelineisstr):
    text = "Delete"
    value = "delete "
    parent = None
    line = -1

    def __str__(self):
        return "delete "

    def getChildren(self):
        return []


class Each(object, Selfsmallprinter,Getliner,Onelineisstr):
    text = "Each"
    parent = None
    value = "each"
    line = -1

    def __str__(self):
        return "each"

    def getChildren(self):
        return []


class Lfalse(object, Selfsmallprinter,Getliner,Onelineisstr):
    text = "False"
    parent = None
    value = "false"
    line = -1

    def __str__(self):
        return "false"

    def getChildren(self):
        return []


class Index(object, Selfsmallprinter,Getliner):
    text = "Index"
    parent= None
    expr = None
    line = -1

    def __init__(self,expr=Expr()):
        self.expr = expr
        self.expr.parent = self

    def __str__(self):
        return "[%s]"%(self.expr)

    def oneline_str(self):
        return "[%s]"%(self.expr.oneline_str())

    def getChildren(self):
        ret = [self.expr]
        return ret

    def replace_item(self,dummy,item):
        self.expr = item
        self.expr.parent = self


class New(object, Selfsmallprinter,Getliner):
    text = "New"
    parent= None
    expr = None
    arguments = None
    line = -1

    def __init__(self,expr=Expr(),arguments=None):
        self.expr = expr
        self.expr.parent = self
        self.arguments = arguments
        if arguments != None: 
            self.arguments.parent = self
    
    def __str__(self):
        if self.arguments != None :
            return "new %s %s"%(self.expr,self.arguments)
        return "(new %s)"%self.expr

    def oneline_str(self):
        if self.arguments != None :
            return "new %s %s"%(self.expr.oneline_str(),self.arguments.oneline_str())
        return "(new %s)"%self.expr.oneline_str()

    def getChildren(self):
        if self.arguments != None :
            return [self.expr,self.arguments]
        return [self.expr]


class While(object, Getliner):
    text = "While"
    parent= None
    predicate = None
    statements = None
    line = -1

    def __init__(self,predicate=Expr(),statements=Statements()):
        self.predicate = predicate
        self.predicate.parent = self
        self.statements = statements
        self.statements.parent = self

    def oneline_str(self):
        return "while(%s)%s" % (self.predicate.oneline_str(),self.statements.oneline_str())

    def __str__(self):
        return "while (%s) %s" % (format(self.predicate),format(self.statements))

    def getChildren(self):
        return [self.predicate, self.statements]

    def smallprint(self):
        return "while (%s)" % (self.predicate)


class DoWhile(object, Getliner):
    text = "DoWhile"
    parent= None
    predicate = None
    statements = None
    line = -1

    def __init__(self,predicate=Expr(),statements=Statements()):
        self.predicate = predicate
        self.predicate.parent = self
        self.statements = statements
        self.statements.parent = self

    def oneline_str(self):
        return "do %s while(%s)" % (self.statements.oneline_str(),self.predicate.oneline_str())

    def __str__(self):
        return "do %s while(%s)" % (self.statements,self.predicate)

    def getChildren(self):
        return [self.predicate, self.statements]

    def smallprint(self):
        return "dowhile (%s)" % (self.predicate)


class For(object, Getliner):
    text = "For"
    initpart = None
    expr1 = None
    expr2 = None
    statements = None
    line = -1

    def __init__(self,initpart=None,expr1=None,expr2=None, statements = None):
        self.initpart = initpart
        if self.initpart != None:
            self.initpart.parent = self
        self.expr1 = expr1
        if self.expr1 != None:
            self.expr1.parent = self
        self.expr2 = expr2
        if self.expr2 != None:
            self.expr2.parent = self
        self.statements = statements
        if self.statements != None:
            self.statements.parent = self

    def oneline_str(self):
        ret =  "for(%s;%s;%s)%s" % (self.initpart.oneline_str(),self.expr1.oneline_str(),self.expr2.oneline_str(),self.statements.oneline_str())      
        return ret

    def __str__(self):
        ret = "for (%s;%s;%s)%s" % (self.initpart,self.expr1,self.expr2,self.statements)
        return ret

    def getChildren(self):
        ret = []
        if self.initpart != None:
            ret.append(self.initpart)
        if self.expr1 != None:
            ret.append(self.expr1)
        if self.expr2 != None:
            ret.append(self.expr2)
        if self.statements != None:
            ret.append(self.statements)
        return ret

    def smallprint(self):
        return "for (%s;%s;%s)" % (self.initpart,self.expr1,self.expr2)


class ForIn(object, Getliner):
    text = "ForIn"
    initpart = None
    statements = None
    line = -1
    each = False

    def __init__(self,initpart=None, statements = None,expr1=None,each=False):
        self.initpart = initpart
        self.expr1 = expr1
        self.expr1.parent = self
        self.initpart.parent = self
        self.statements = statements
        if self.statements != None:
            self.statements.parent = self

    def oneline_str(self):
        s = ""
        if self.statements != None:
            s = self.statements.oneline_str()
        ret =  "for %s(%s in %s) %s" % ("each" if self.each else "" ,self.initpart.oneline_str(),self.expr1.oneline_str(),s)
        return ret

    def __str__(self):
        s = ""
        if self.statements != None:
            s = "%s"%self.statements
        ret =  "for %s(%s in %s) %s" % ("each" if self.each else "" ,self.initpart,self.expr1,s)
        return ret

    def getChildren(self):
        ret = []
        if self.initpart != None:
            ret.append(self.initpart)
        if self.expr1 != None:
            ret.append(self.expr1)
        if self.statements != None:
            ret.append(self.statements)
        return ret

    def smallprint(self):
        return "for %s(%s in %s)" % ("each" if self.each else ""  ,self.initpart,self.expr1)


class EmptyStatement(object, Selfsmallprinter,Getliner,Onelineisstr):
    line = -1
    text = "EmptyStatement"
    parent= None

    def  __str__(self):
        return "" 

    def getChildren(self):
        return []
  
class If(object, Getliner):
    text = "If"
    parent= None
    predicate = None
    statementstrue = None
    statementsfalse= None
    line = -1

    def __init__(self,predicate=Expr(),statementstrue=None,statementsfalse=None):
        self.predicate = predicate
        self.predicate.parent = self
        self.statementstrue = statementstrue
        self.statementstrue.parent = self
        if statementsfalse != None:
            self.statementsfalse = statementsfalse
            self.statementsfalse.parent = self

    def __str__(self):
        if self.statementsfalse == None:
            return "if(%s)%s" %(format(self.predicate),format(self.statementstrue))
        return "if(%s)%selse%s" %(format(self.predicate),format(self.statementstrue),format(self.statementsfalse))

    def oneline_str(self):
        if self.statementsfalse == None:
            return "if(%s)%s" %(self.predicate.oneline_str(),self.statementstrue.oneline_str())
        return "if(%s)%s else %s" %(self.predicate.oneline_str(),self.statementstrue.oneline_str(),self.statementsfalse.oneline_str())

    def getChildren(self):
        l = [self.predicate, self.statementstrue]
        if  self.statementsfalse != None:
            l.append( self.statementsfalse)
        return l

    def smallprint(self):
        if self.statementsfalse == None:
            return "if(%s)" %(self.predicate)
        return "if(%s) else" %(self.predicate)


class Program(object, Textsmallprinter,Getliner):
    text = "Program"
    parent= None
    statements = None
    line = -1

    def __init__(self,statements= Statements()):
        self.statements = statements
        self.statements.parent = self

    def oneline_str(self):
        return format(self.statements.oneline_str())

    def  __str__(self):
        return self.statements.__str__(INDENT="")

    def getChildren(self):
        return [self.statements]


class Function(object, Getliner):
    text = "Function"
    parent= None
    ident = None
    args_dec = None
    statements = None
    functionexpr = False
    functional = False
    line = -1

    def __init__(self, ident = Ident(), args_dec=Listarguments(),statements =Statements(),functionexpr=False):
        self.ident = ident
        if ident != None:
            self.ident.parent = self
        self.statements = statements
        self.statements.parent = self 
        self.args_dec = args_dec
        self.args_dec.parent = self
        self.functionexpr = functionexpr

    def oneline_str(self):
        if self.ident!= None:
            return "function %s %s %s"%(str(self.ident),str(self.args_dec.oneline_str()),str(self.statements.oneline_str()))
        return "function %s %s"%(str(self.args_dec.oneline_str()),str(self.statements.oneline_str()))

    def __str__(self):
        ret = ""
        if self.ident!= None:
            ret = "function %s %s %s"%(str(self.ident),str(self.args_dec),str(self.statements))
        else:
            ret = "function %s %s"%(str(self.args_dec),str(self.statements))
        return ret

    def replace_ident(self,ident):
        self.ident = ident
        self.ident.parent = self 

    def getChildren(self):
        if self.ident != None:
            return [self.ident,self.args_dec,self.statements]
        return [self.args_dec,self.statements]

    def smallprint(self):
        if self.ident!= None:
            return "function %s %s"%(self.ident,self.args_dec)
        return "function %s"%(self.args_dec)

