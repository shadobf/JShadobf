#!/usr/bin/env python
import sys
import traceback
import os
from jshadobf.common.convert import convert
from jshadobf.output.dottree import gen_dot_file, cfg_dot_file
from jshadobf.common.cfg import cfg_builder







if __name__=="__main__":
    import sys
    import optparse
  
    optparser = optparse.OptionParser(usage="usage: %prog [options]")
    optparser.add_option("-a" , "--ast" ,dest="ast",default=False, action='store_true',help="print the tree")
    optparser.add_option("-c" , "--cfg" ,dest="cfg",default=False, action='store_true',help="print the file")
    optparser.add_option("-f" , "--file" ,dest="file",default="", help="file name")
    optparser.add_option("-o" , "--output" ,dest="fileo",default="output", help="output basename")
    optparser.add_option("-v" , "--verbose" ,dest="verbose",default=False, action='store_true',help="verbose")
  
    (option , arg ) = optparser.parse_args(sys.argv)
    if option.file == "":
        optparser.print_help()
        sys.exit()
  
    c =  convert(option.file)
    if option.ast:
        gen_dot_file(c,filename=option.fileo+".ast.dot")
        os.system("dot -Tpng -o "+option.fileo+".ast.png "+ option.fileo+".ast.dot")
    if option.cfg:
        cfg = cfg_builder(c)
#    print RED, cfg,BLACK
        cfg_dot_file(cfg,filename=option.fileo+".cfg.dot")
        os.system("dot -Tpng -o "+option.fileo+".cfg.png "+ option.fileo+".cfg.dot")
    
