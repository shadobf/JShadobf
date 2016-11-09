#!/usr/bin/env python
import sys
import traceback
import os

import antlr3
from antlr3 import *
from antlr3.tree import *



#print sys.path
from jshadobf.parser.JavaScriptLexer import JavaScriptLexer
from jshadobf.parser.JavaScriptParser import JavaScriptParser
from jshadobf.common.tree_printer import *


if __name__ == "__main__":
    sys.setrecursionlimit(1000000)

	#input = sys.stdin.read()
    if len (sys.argv) >1:
        prg = sys.argv[1]
    else:
        print "no input prgm"
        sys.exit()

	#~ input = open(prg).read()
	#~ print help(antlr3.ANTLRStringStream)
    char_stream = antlr3.ANTLRFileStream(prg,encoding='utf-8')
	## or to parse a file:
	## char_stream = antlr3.ANTLRFileStream(path_to_input)
	## or to parse an opened file or any other file-like object:
	## char_stream = antlr3.ANTLRInputStream(file)

    lexer = JavaScriptLexer(char_stream)
    tokens = antlr3.CommonTokenStream(lexer)
    pp = JavaScriptParser(tokens)
	
	
#parser.program()


	#char_stream = antlr3.ANTLRStringStream(input)
	#lexer = JavaScriptLexer(char_stream)
	#tokens = antlr3.CommonTokenStream(lexer)
	#parser = JavaScriptParser(tokens)
    tree = pp.program().tree 
    if len (sys.argv) > 2 and sys.argv[2] == "n":
        sys.exit()
    print_level_order(tree)
