#!/usr/bin/env python
#-*- coding:utf-8 -*-

import unittest
import random
import os
import sys
import subprocess
from jshadobf.transformations.list_transformations import TRANSFORMATIONS
from jshadobf.common.convert import convert_string, convert
from jshadobf.common.tree_printer import print_level_order




RED ="\033[1;31m"
GREEN ="\033[1;32m"
BLACK = "\033[0m"
YELLOW ="\033[1;33m"
BLUE ="\033[1;34m"
PURPULE =  "\033[1;35m"



PRGM_DIRECTORY="prgms"
RANDOM_LIST = "ressources/randomlist"

FIBO_PRGM = "fibo_rhino.js"
SORT_PRGM = "sort_rhino.js"
ALERT_PRGM = "test_alert_rhino.js"


tempfile = "tmp/alert_if.js"
#    lout = "tmp/l_out"
alert_prgm = ALERT_PRGM 


 

if __name__=="__main__":
    import sys
    import optparse


    sys.setrecursionlimit(1000000)
  
    optparser = optparse.OptionParser(usage="usage: %prog [options]")
#  optparser.add_option("-t" , "--print-tree" ,dest="printtree",default=False, action='store_true',help="print the tree")
    optparser.add_option("-a" , "--all" ,dest="all", type='int',default=0, help="apply all the transformation (nombre de fois)")
    optparser.add_option("-t" , "--apply" ,dest="apply_t", default=[] , action='append' , help="print the list of available transformations")
    optparser.add_option("-l" , "--list-of-transformaations" ,dest="get_list", default=False , action='store_true' , help="print the list of available transformations")
    optparser.add_option("-v" , "--verbose" ,dest="verbose",default=0,action="count", help="verbose")
    optparser.add_option("-p" , "--print-tree" ,dest="printtree",default=False,action="store_true", help="Print the tree after transformations")
    optparser.add_option("-f" , "--file" ,dest="file",default="", help="input file name")
    optparser.add_option("-o" , "--output-file" ,dest="ofile",default="", help="output file name")
    optparser.add_option("-1" , "--onelinefile" ,dest="onelinefile",default=False,action="store_true", help="print the file without \\n")
    optparser.add_option("-s" , "--seed" ,dest="seed",default=-1, help="set seed")
  
    (option , arg ) = optparser.parse_args(sys.argv)
    if option.get_list :
        for t in TRANSFORMATIONS:
            print t.__name__
        sys.exit()

#    if option.file == "":
#        optparser.print_help()
#        sys.exit()
  
    if option.seed != -1:
        random.seed(option.seed)
  
    to_apply = []
#  print option
    for t in option.apply_t:
  
        name = t.split(",")[0]
        name = name.split(" ")[0]
        times = 1 
        temp = t.split(",")[-1]
        temp = temp.split(" ")[-1]
        if temp != name :
            try :
                times = int ( temp)
            except Exception, e:
                print e
        
        for tt in TRANSFORMATIONS:
            if tt.__name__.find(name) != -1 :
                to_apply.append( (tt,times))
    
    if option.file == "":
        
        c =  convert_string(sys.stdin.read(),option.verbose > 2 )
    else:
        c =  convert(option.file,option.verbose > 2 )
    d = c
#  print to_apply
    for transfo,num in to_apply:
        if option.verbose > 1 :
            print "Applying transfo : %s , times %d "% (transfo.__name__ , num)
        for i in xrange(num):
            d = transfo(d,option.verbose)
  
    for i in xrange(option.all):
        for transfo in TRANSFORMATIONS:
            d = transfo(d,option.verbose)


    if option.printtree :
        print_level_order(d,option.verbose)

    if option.onelinefile : 
        output = d.oneline_str()
    else:
        output = format(d)

    if option.ofile == "":
        print output
    else:
     
        f = open( option.ofile,"w")
        f.write(output)
        f.close()
  
