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
from jshadobf.common.runner import GenericRunner
from jshadobf.moea.jshadobf_ea import JShadobf_Individual
from jshadobf.common.common import verbose, deepcopy
from jshadobf.transformations.common import get_transformation_by_name
from jshadobf.common.colors import yellow, red
import shutil
import tempfile




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


alert_prgm = ALERT_PRGM 


 

if __name__=="__main__":
    import sys
    import optparse


    sys.setrecursionlimit(1000000)
  
    optparser = optparse.OptionParser(usage="usage: %prog [options]")
#  optparser.add_option("-t" , "--print-tree" ,dest="printtree",default=False, action='store_true',help="print the tree")

    optparser.add_option("-T" , "--temp-dir" ,dest="tempdir",default="/dev/shm/jshadobf",type="string", help="number modification apply by a transformation")
    optparser.add_option("-a" , "--all" ,dest="all", type='int',default=0, help="apply all the transformation (nombre de fois)")
    optparser.add_option("-t" , "--apply" ,dest="apply_t", default=[] , action='append' , help="apply the  the list of available transformations")
    optparser.add_option("-l" , "--list-of-transformaations" ,dest="get_list", default=False , action='store_true' , help="print the list of available transformations")
    optparser.add_option("-v" , "--verbose" ,dest="verbose",default=0,action="count", help="verbose")
    optparser.add_option("-p" , "--print-tree" ,dest="printtree",default=False,action="store_true", help="Print the tree after transformations")
    optparser.add_option("-f" , "--file" ,dest="file",default="", help="input file name")
    optparser.add_option("-i" , "--interpretor" ,dest="interpretor",default="node", help="command for the interpretor")
    optparser.add_option("-s" , "--seed" ,dest="seed",default=-1, help="set seed")
    optparser.add_option("-o" , "--output-dir" ,dest="output_dir",default="jshadobf", help="paht to store the files which lead to the failure")
    optparser.add_option("-e" , "--extra-end-file" ,dest="extra_end_file",default=None, 
                         help="file containing the JavaScript code necessary to add at the end of the program to run the code during the execution_time test phase")
    
    (option , arg ) = optparser.parse_args(sys.argv)
    
    if not os.path.isdir(option.output_dir):
        os.mkdir(option.output_dir)
    
    if option.get_list :
        for t in TRANSFORMATIONS:
            print t.__name__
        sys.exit()

    if option.seed != -1:
        random.seed(option.seed)

    interpreter = option.interpretor

    runner = GenericRunner(interpreter=interpreter, 
        program_path=option.file,
        temp_progam_name="generic.js", verbose=option.verbose,
        temp_dir=option.tempdir,
        remove_temp=False, extra_end_file=option.extra_end_file)

    if option.apply_t != []:
        transfomations_available = map(lambda x:get_transformation_by_name(x, TRANSFORMATIONS), option.apply_t)
    else:
        transfomations_available = TRANSFORMATIONS
    
    adam = JShadobf_Individual(runner,tree=None,path=option.file,strict=False, test_n_times=1,numbermax=1000,transformations_available=transfomations_available,
                 objectives=["mu1","mu2","mu3","mu4","mu5","exectime"], verbose=option.verbose)
#  print to_apply
    adam.convert()
    print yellow(adam)
    testnum = 0
    cont = True
    
    while cont:
        individual = deepcopy(adam)
        files = []
        testnum += 1
        print yellow("Start %d" %testnum)
        for i in range(20):
            individual.mutate()
            individual.evaluate()
            files.append(individual.runner.modified_executable)
            print individual.objectives
            if individual.worst:
                sum_file_name = tempfile.mktemp(prefix="summary_", suffix=".txt", dir=option.output_dir)
                with open(sum_file_name, "w") as sum_file: 
                    sum_file.write("TRANSFORMATIONS:\n")
                    sum_file.write("\n".join(individual.transformations))
                    sum_file.write("FILES:\n")
                    sum_file.write("\n".join(files) + "\n")
                for f in files:
                    if option.verbose > 3:
                        print red("copy: " + f)
                    shutil.copy(f, option.output_dir)
                cont = False
                break
    for f in files:
        if option.verbose > 3:
            print red("remove: " + f)
        os.remove(f)
                