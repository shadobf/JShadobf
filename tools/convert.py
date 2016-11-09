#!/usr/bin/env python
import sys
import traceback
import os




from jshadobf.common.tree_printer import *
from jshadobf.common.convert import *
from jshadobf.common.classes import *


if __name__=="__main__":
    import sys
    import optparse
    sys.setrecursionlimit(1000000)
    optparser = optparse.OptionParser(usage="usage: %prog [options]")
    optparser.add_option("-t" , "--print-tree" ,dest="printtree",default=False, action='store_true',help="print the tree")
    optparser.add_option("-p" , "--print-file" ,dest="printfile",default=False, action='store_true',help="print the file")
    optparser.add_option("-f" , "--file" ,dest="file",default="", help="print the file")
    optparser.add_option("-l" , "--onelinefile" ,dest="onelinefile",default=False,action="store_true", help="print the file without \\n")
    optparser.add_option("-v" , "--verbose" ,dest="verbose",default=0,action="count", help="verbose")
  
    (option , arg ) = optparser.parse_args(sys.argv)
    f = "" 
    c = None
    if option.file == "":
        c =  convert_string( sys.stdin.read() ,option.verbose)
    else:
        c =  convert(option.file ,option.verbose)
  
    if option.printtree :
        print_level_order(c,printable=["Ident","List","Number","Ltrue","Lfalse"])

    if option.printfile:
        print c

    if option.onelinefile:
        print c.oneline_str()
