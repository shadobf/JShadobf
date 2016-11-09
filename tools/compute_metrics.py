#!/usr/bin/env python
import sys
import traceback
import os

import time
import subprocess

from jshadobf.common.convert import convert

import optparse

import tempfile
from jshadobf.metrics.halstead import halstead
from jshadobf.metrics.mccabe import mccabe
from jshadobf.metrics.harrison import harrison
from jshadobf.metrics.oviedo import oviedo
from jshadobf.metrics.henry import henry

RED ="\033[1;31m"
GREEN ="\033[1;32m"
BLACK = "\033[0m"
YELLOW ="\033[1;33m"
BLUE ="\033[1;34m"
PURPULE =  "\033[1;35m"


def execute_command(cmd,verbose=0,get_time=False,get_res=False):
    ret = None
    if verbose >1:
        print BLUE + cmd + BLACK
    t1 = time.time()
    p = subprocess.Popen(cmd, shell=True, stdout = subprocess.PIPE)
    t2 = time.time()
    ret = [p.stdout.read()]
    sts = os.waitpid(p.pid, 0)[1]

    if verbose>2:
        print ret
    if get_time :
        ret.append(t2-t1)
    if get_res :
        ret.append(p.poll())
    if len (ret )> 1:
        return tuple(ret)
    return ret[0]



def getnewfilename(directory="/tmp",prefix="",postfix=".js"):

    return tempfile.mktemp(suffix=postfix,prefix=prefix,dir=directory)
#  while prefix + "%06d"% num + postfix in files:
#    num += 1
#  return directory + os.sep + prefix + "%06d"% num + postfix 
		

def compute_metrics(files,metrics,verbose=0):
    list_dict=[]

    try :

        for f in files:
            c =  convert(f,verbose)
            d = {(0,"name"):f[f.rfind(os.sep)+len(os.sep):]}
            if metrics["halstead"] :
                d[(1,"halstead")]= halstead(c)
            if metrics["mccabe"]:
                d[(2,"mccabe")]= mccabe(c)
            if metrics["harrison"]:
                d[(3,"harrison")]= harrison(c)
            if metrics["oviedo"]:
                d[(4,"oviedo")]= oviedo(c)
            if metrics["henry"]:
                d[(5,"henry")]= henry(c)
            list_dict.append(d)
    except Exception,e:
        print traceback.print_exc()
        print e
        print "Failed to compute metrics on  "+format(files)

#  keys = list(d.viewkeys())
#  keys.sort()
    return list_dict
  
def print_metrics(list_dict):
    if len (list_dict) == 0 :
        return 
    keys = list(list_dict[0])
    keys.sort()
    for k in keys:
        print "% 10s"%k[1],":","% 20s"*len(list_dict) % tuple(map(lambda x: str(x[k]) , list_dict))


if __name__=="__main__":

    optparser = optparse.OptionParser(usage="usage: %prog [options]")
  
    optparser.add_option("-a" , "--all" ,dest="all",default=False, action='store_true',help="compute all the metrics")
    optparser.add_option("-1" , "--halstead" ,dest="halstead",default=False, action='store_true',help="compute the halstead metric")
    optparser.add_option("-2" , "--mccabe" ,dest="mccabe",default=False, action='store_true',help="compute the mccabe metric")
    optparser.add_option("-3" , "--harrison" ,dest="harrison",default=False, action='store_true',help="compute the harrison metric")
    optparser.add_option("-4" , "--oviedo" ,dest="oviedo",default=False, action='store_true',help="compute the oviedo metric")
    optparser.add_option("-5" , "--henry" ,dest="henry",default=False, action='store_true',help="compute the henry metric")
    optparser.add_option("-6" , "--munson" ,dest="munson",default=False, action='store_true',help="compute the munson metric")
    optparser.add_option("-f" , "--file" ,dest="file",default=[],action="append", help="file to compute the metrics on")
    optparser.add_option("-v" , "--verbose" ,dest="verbose",default=False,action="store_true", help="verbose")
   
    (option , arg ) = optparser.parse_args(sys.argv)
    if option.file == []:
        optparser.print_help()
        sys.exit()

    if option.all :
        option.halstead,option.mccabe,option.harrison,option.oviedo,option.henry = [True]*5
    metrics = {}
    for m in ["halstead","mccabe","harrison","oviedo","henry"]:
        metrics[m] = getattr(option,m)
    values = compute_metrics(option.file,metrics, option.verbose)
    print_metrics(values)






