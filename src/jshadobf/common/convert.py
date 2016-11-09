import sys
import antlr3
from jshadobf.common.colors import RED
from jshadobf.common.classes import Statements, Program, VarDeclaration, Ident,\
    Suffix, MemberExpr, Return, ObjectLiteral, PropertyGet, PropertySet,\
    Function, Var, Listarguments, EmptyStatement, If, Yield, Let, For, Each,\
    ForIn, Try, While, DoWhile, Switch, Throw, CatchClause, FinallyClause,\
    CaseBlock, Break, Continue, UnaryExpr, PropertyName, Property, Number,\
    Ternary, RegEx, List, ListCreation, String, Assignment, ExpressionStatement,\
    This, Expr, New, Null, Ltrue, Lfalse, Index, CallExpressionSuffix,\
    Functioncall
from jshadobf.parser.JavaScriptLexer import JavaScriptLexer
from jshadobf.parser.JavaScriptParser import JavaScriptParser

def statement_convertor(t):
    if not isinstance(t,Statements):
        t = Statements([t])
    return t

def convert_tree(tree,verbose=0):
    children = tree.getChildren()
    p = []
    if verbose > 3:
        print tree.getLine() ,":",tree.text
    if tree.text == "Program":
        p = Program(Statements([ convert_tree(c,verbose) for c in children] ))
    if tree.text == "VarDeclaration":
        if len(children) > 1:
            p = VarDeclaration(convert_tree(children[0],verbose),convert_tree(children[1],verbose))
        else:
            p = VarDeclaration(convert_tree(children[0],verbose))
    if tree.text == "Ident":
        p = Ident(children[0].text)
    if tree.text == "Suffix":
        p = Suffix(convert_tree(children[0],verbose))
    if tree.text == "MemberExpr":
        if len(children) > 1:
            p = MemberExpr(convert_tree(children[0],verbose),map(convert_tree,children[1:]))
        else:
            p = convert_tree(children[0],verbose)
    if tree.text == "Return":
        e = None
        if len(children) == 1 :
            e = convert_tree(children[0],verbose)
        p = Return(e)
    if tree.text == "ObjectLiteral" :
        o = [ convert_tree(c,verbose) for c in children]
        p = ObjectLiteral(o)
    if tree.text == "PropertyGet" :
        if children[0].text != "get":
            print "error expecting get"
            sys.exit(1)
        n = convert_tree(children[1],verbose)
        b = convert_tree(children[2],verbose)
        p = PropertyGet(n,b)
    if tree.text == "PropertySet" :
        if children[0].text != "set":
            print "error expecting set"
            sys.exit(1)
        n = convert_tree(children[1],verbose)
        i = convert_tree(children[2],verbose)
        b = convert_tree(children[3],verbose)
        p = PropertySet(n,i,b)
    if tree.text == "Function" or tree.text == "FunctionExpr":
        a = convert_tree(children[0],verbose)
        s = statement_convertor(convert_tree(children[1],verbose))
        i = None
        if len(children) == 3:
            i = convert_tree(children[2],verbose)
        funcexpr = (tree.text == "FunctionExpr")
        p = Function(i,a,s,funcexpr)
    if tree.text == "VariableStatement":
        p = convert_tree(children[0],verbose)
    if tree.text == "Var":
        p = Var(map(lambda x:convert_tree(x,verbose),children))
    if tree.text == "Listarguments":
        p = Listarguments(map(lambda x:convert_tree(x,verbose),children))
    if tree.text == "Statements":
        s = map(lambda x:convert_tree(x,verbose),children) 
        s = filter ( lambda x : x != [] , s)
        p = Statements(s)
        for i in s:
            if i.parent != p :
                print RED,"error"
                sys.exit(1)
    if tree.text == "EmptyStatement":
        p = EmptyStatement()
    if tree.text == "If":
        p = convert_tree(children[0],verbose)
        tt = convert_tree(children[1],verbose)
        t = statement_convertor(tt)
        f = None
        if (len (children) ==3 ):
            f = statement_convertor(convert_tree(children[2],verbose))
        p = If(p,t,f)
    if tree.text == "Yield":
        e = convert_tree(children[0],verbose)
        p = Yield(e)
    if tree.text == "Let":
        v = convert_tree(children[0],verbose)
        t = None
        if (len (children) ==2 ):
            tt = convert_tree(children[1],verbose)
            t = statement_convertor(tt)
        p = Let(v,t)
    if tree.text == "For":
        i = convert_tree(children[0],verbose)
        e1 = convert_tree(children[1],verbose)
        e2 = convert_tree(children[2],verbose)
        s = statement_convertor(convert_tree(children[3],verbose))
        p = For(i,e1,e2,s)
    if tree.text == "each":
        p = Each()
    if tree.text == "ForIn":
        i = convert_tree(children[0],verbose)
        e1 = convert_tree(children[1],verbose)
        each = children[2]
        s = None
        if len(children) == 4:
            s = convert_tree(children[3],verbose)
        print each
        if len(each.getChildren()) == 0:
            each = False
        elif each.getChildren()[0].text == "each":
            each = True
        else:
            print "%d:error: for cannot be followed by %s" %(each.getLine() ,each.getChildren()[0].text)
            sys.exit(0)
        if s != None:
            s = statement_convertor(s)
        p = ForIn(i,s,e1,each)
    if tree.text == "Try":
        s = convert_tree(children[0],verbose)
        rest =  map(lambda x:convert_tree(x,verbose),children[1:])
        t = statement_convertor(s)
        p = Try(t,rest)
    if tree.text == "While":
        p = convert_tree(children[0],verbose)
        t = statement_convertor(convert_tree(children[1],verbose))
        p = While(p,t)
    if tree.text == "DoWhile":
        p = convert_tree(children[1],verbose)
        t = statement_convertor(convert_tree(children[0],verbose))
        p = DoWhile(p,t)
    if tree.text == "Switch":
        e = convert_tree(children[0],verbose)
        cb = map(lambda x:convert_tree(x,verbose),children[1:])
        p = Switch(e,cb)
    if tree.text == "Throw":
        e = convert_tree(children[0],verbose)
        p = Throw(e)
    if tree.text == "CatchClause":
        i = convert_tree(children[0],verbose)
        e = statement_convertor(convert_tree(children[1],verbose))
        ex = None
        if len (children ) == 3:
            ex = convert_tree(children[2],verbose)
        p = CatchClause(i,e,ex)
    if tree.text == "FinallyClause":
        e = statement_convertor(convert_tree(children[0],verbose))
        p = FinallyClause(e)
    if tree.text == "CaseClause":
        e = convert_tree(children[0],verbose)
        cc = Statements(filter(lambda x : x != [] , map(lambda x:convert_tree(x,verbose),children[1:])))
        p = CaseBlock(cc,e)
    if tree.text == "DefaultBlock":
        cc = Statements(filter(lambda x : x != [] , map(lambda x:convert_tree(x,verbose),children[:])))
        p = CaseBlock(cc)
    if tree.text == "Break":
        i = None
        if len(children) != 0:
            i = convert_tree(children[0],verbose)
        p = Break(i)
    if tree.text == "Continue":
        i = None
        if len(children) != 0:
            i = convert_tree(children[0],verbose)
        p = Continue(i)
    if tree.text == "UnaryExpr":
        c1 = convert_tree(children[1],verbose)
        p = UnaryExpr( children[0].text,c1)
    if tree.text == "PropertyName":
        if  len(children)==2: 
            c1 = convert_tree(children[1],verbose)
            c0 = convert_tree(children[0],verbose)
            p = PropertyName( c0,c1)
        else:
            p = PropertyName( convert_tree(children[0],verbose))
    if tree.text == "Property":
        p = Property( convert_tree(children[0],verbose))
    if tree.text == "Zero":
        p = Number(0)
    if tree.text == "Ternary":
        if len(children)==3:
            p = Ternary(convert_tree(children[0],verbose),convert_tree(children[1],verbose),convert_tree(children[2],verbose))
        else:
            p = convert_tree(children[0],verbose)
    if tree.text == "Number":
        if children[0].text == "NaN":
            p = NaN()
        else:
            p = Number( children[0].text)
    if tree.text == "RegEx":
        p = RegEx( children[0].text)
    if tree.text == "List":
        p = List([ convert_tree(c,verbose) for c in children])
    if tree.text == "ListCreation":
        e = convert_tree(children[0],verbose)
        f = convert_tree(children[1],verbose)
        p = ListCreation(e,f)
    if tree.text == "String":
        p = String( children[0].text)
    if tree.text == "Assignment":
        v = convert_tree(children[0],verbose)
        t = children[1].text
        e = convert_tree(children[2],verbose)
        p = Assignment(v,t,e)
    if tree.text == "ExpressionStatement":
        p = ExpressionStatement([convert_tree(c,verbose) for c in children])
    if tree.text == "This":
        p = This()
    if tree.text == "Expr" :
        l = []
        for c in children:
            conv = convert_tree(c,verbose)
            if conv == []:
                if c.text == "And":
                    l.append("&&")
                elif c.text == "Or":
                    l.append("||")
                elif c.text == "BAnd":
                    l.append("&")
                elif c.text == "BOr":
                    l.append("|")
                elif c.text == "BXor":
                    l.append("^")
                else:
                    l.append(c.text)
            else:
                l.append(conv)
        if len(l) == 0:
            p = Expr()
        elif len(l) == 1 :
            if isinstance( l[0],Expr):
                p = l[0]
            else:
                p = Expr(l)
        else:
            if l[1] == ",":
                p = Statements([l[i] for i in range (0,len(l)+1,2)])
            else:
                p = Expr(l)
    if tree.text == "New":
        e = convert_tree(children[0],verbose)
        a = None
        if len(children) == 2:
            a = convert_tree(children[1],verbose)
        p = New(e,a)
    if tree.text == "Null":
        p = Null()
    if tree.text == "Ltrue":
        p = Ltrue()
    if tree.text == "Lfalse":
        p = Lfalse()
    if tree.text == "Index":
        p = Index(convert_tree(children[0],verbose))
    if tree.text == "Functioncall":
        if len (children) == 1 :
            p = convert_tree(children[0],verbose)
        else:
            i = convert_tree(children[0],verbose)
            a = convert_tree(children[1],verbose)
            r = None
            if len (children)> 2:
                r = CallExpressionSuffix(map( convert_tree,children[2:]))
        p = Functioncall(i,a,r)
    if p != [] :
        p.line = tree.getLine()
    return p

def convert_charstream(char,verbose=0):
    lexer = JavaScriptLexer(char)
    tokens = antlr3.CommonTokenStream(lexer)
    pp = JavaScriptParser(tokens)
    prgm = pp.program()
    tree = prgm.tree
    return convert_tree(tree,verbose)

def convert_string(string,verbose=0):
    char_stream = antlr3.ANTLRStringStream(string)
    return convert_charstream(char_stream,verbose)

def convert(path,verbose=0):
    char_stream = antlr3.ANTLRFileStream(path,encoding='utf-8')
    return convert_charstream(char_stream,verbose)
