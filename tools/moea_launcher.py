import traceback
import sys
import os
import time
from jshadobf.transformations.list_transformations import TRANSFORMATIONS
from jshadobf.moea.jshadobf_ea import  JShadobf_Population
from jshadobf.moea.moead import MOEAD
from copy import deepcopy
from jshadobf.moea.moea_common import available_objectives
from jshadobf.common.runner import GenericRunner
from jshadobf.moea.nsga2 import NSGAII
dirname = os.path.dirname(__file__)

if __name__ == "__main__":
    import optparse
    sys.setrecursionlimit(1000000)
  
    optparser = optparse.OptionParser(usage="usage: %prog [options]")

    option_dict = {"genmax": 30,"algo":"nsga2","island":False,"graph":[],"maxtime":-1,
                   "test":False,"numbermax":10,"popmax":100,"server_work":"","verbose":0,
                   "individus":[],"testntimes":1,"config":"shadobf.conf",
                   "tempdir":"/dev/shm/jshadobf","outputdir":os.path.expanduser("~") + os.sep + "temp/shadobf.%d"%time.time(),
                   "program_initial":"","dirty":False,"dumptime":5,"objectives":[],
                   "strict":False, "extra_end_file": None, "process":1
                   #,"runner":"GenericRunner"
                   }
    option_dict_default = deepcopy(option_dict)
    option_dict_config =  deepcopy(option_dict)

    optparser.add_option("-g" , "--gen-max" ,dest="genmax",default=option_dict["genmax"],type="int", help="Number of generations")
    optparser.add_option("-p" , "--pop-max" ,dest="popmax",default=option_dict["popmax"],type="int", help="Maximum pupulation")
    optparser.add_option("-s" , "--server-work" ,dest="server_work",default=option_dict["server_work"], help="server:port of the server from which to steal work")
    optparser.add_option("-1" , "--program-initial", dest="program_initial" , default = option_dict["program_initial"], help="program_initial")
    optparser.add_option("-v" , "--verbose" ,dest="verbose",default=option_dict["verbose"],action="count", help="verbose")
    optparser.add_option("-i" , "--individus" ,dest="individus",default=option_dict["individus"],action="append", help="file or directory containing individuals")
    optparser.add_option("-d" , "--dirty" ,dest="dirty",default=option_dict["dirty"],action="store_true", help="verbose")
    #optparser.add_option("-r" , "--runner" ,dest="runner",default=option_dict["runner"], help="name of the runner class for the execution")
    optparser.add_option("-e" , "--extra-end-file" ,dest="extra_end_file",default=option_dict["extra_end_file"], 
                         help="file containing the JavaScript code necessary to add at the end of the program to run the code during the execution_time test phase")
    optparser.add_option("-c" , "--config" ,dest="config",default=option_dict["config"], help="config file")
    optparser.add_option("-o" , "--outputdir" ,dest="outputdir",default=option_dict["outputdir"], help="output directory")
    optparser.add_option("-t" , "--test-n-time" ,dest="testntimes",default=option_dict["testntimes"],type="int", help="number of time the test of the execution time has to be performed")
    optparser.add_option("-m" , "--number-max" ,dest="numbermax",default=option_dict["numbermax"],type="int", help="number modification apply by a transformation")
    optparser.add_option("-T" , "--temp-dir" ,dest="tempdir",default=option_dict["tempdir"],type="string", help="number modification apply by a transformation")
    optparser.add_option("-a" , "--algo" ,dest="algo",default=option_dict["algo"],type="string", help="algorithm to run")
    optparser.add_option("-G" , "--graph" ,dest="graph",default=option_dict["graph"],action="append",help="show graph m1:m2")
    optparser.add_option("-I" , "--island" ,dest="island",default=option_dict["island"],action="store_true", help="algorithm to run")
    optparser.add_option("" , "--test" ,dest="test",default=option_dict["test"],action="store_true", help="test distributed workers")
    optparser.add_option("-M" , "--max-time" ,dest="maxtime",default=option_dict["maxtime"], help="Maximum execution time for the individual")
    optparser.add_option("-D" , "--dump-time" ,dest="dumptime",type=int,default=option_dict["dumptime"], help="dump individuals every n generation (-1: never)")
    optparser.add_option("-O" , "--objectives" ,dest="objectives",default=option_dict["objectives"],action="append", help="select the objectives")
    optparser.add_option("-L" , "--list-metric" ,dest="list_objectives",default=False,action="store_true", help="print the available objectives")
    optparser.add_option("-S" ,  "--strict",dest="strict",default=option_dict["strict"],action='store_true',help="stop on bad individual, not avail with parallel version")
    optparser.add_option("-P" ,  "--process",dest="process",default=option_dict["process"], type=int,help="set number of process for parallelizable operations")
    
    (option , arg ) = optparser.parse_args(sys.argv)
    if option.list_objectives:
        for m in available_objectives:
            print m
        sys.exit(1)

    if os.path.isfile(option.config):
        for l in open(option.config).read().splitlines():
            print l
            o = None
            if  l.find ("=") != -1:
                o = l.split("=")
                o = map(lambda x : x.strip() , o)
            if o == None:
                print "config line error:", l
                continue
            if option_dict_config.has_key(o[0]):
                option_dict_config [o[0]] = eval (o[1])
            else:
                print "unkonw parameter :" + o[0]

    for k in option_dict_default.keys():
        if getattr(option, k) == option_dict_default[k]:
            setattr(option,k,option_dict_config[k])
    if option.verbose > 0:
        print "options:", option  
    
    if option.objectives == []:
        objectives = ["mu1","mu2","mu3","mu4","mu5","exectime","summu"]
    else:
        objectives = []
        for o in option.objectives:
            if o in available_objectives:
                objectives.append(o)
    options = {"process": option.process,
                "pop_max":option.popmax,
               "n_generations_max":option.genmax ,"data_output_dir":option.outputdir,
               "existing_individuals":option.individus,
               "verbose":option.verbose,"graph":option.graph,"mutation_rate":.5,"dumptime":option.dumptime,
#               "objectives":objectives,
                   "individual_options" :{"strict":option.strict,"runner":None,
                                          "test_n_times":option.testntimes,"numbermax":option.numbermax,
                                          "objectives":objectives,"transformations_available":TRANSFORMATIONS,
                                          }
               }
    
    maxtime = int(option.maxtime)
    interpreter = "node"
    if maxtime != -1:
        interpreter = "timeout %d %s" % (maxtime,interpreter)

    hn = GenericRunner(interpreter=interpreter, 
        program_path=option.program_initial,
        temp_progam_name="generic.js", verbose=option.verbose,
        temp_dir=option.tempdir,
        remove_temp=not option.dirty, extra_end_file=option.extra_end_file)

    options["individual_options"]["runner"] = hn
    population = JShadobf_Population(**options)
    if option.algo == "nsga2":
        ea = NSGAII(population=population,verbose=option.verbose)
    if option.algo == "moead":
        ea = MOEAD(population=population,verbose=option.verbose)

    open(option.outputdir + os.sep +"cmdline","w").write(" ".join(sys.argv))
    try :                 
        ea.run()
    except Exception as e:
        print traceback.print_exc()
        print "Exception received," , e
    continu = False
