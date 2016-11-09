#/usr/bin/env python

#import unittest
import os
import sys
import subprocess
#import re
import time

#~ import test_fibo
#~ import test_sort
#~ import test_matmul
#~ import test_alert

RED = "\033[1;31m"
GREEN = "\033[1;32m"
BLACK = "\033[0m"
YELLOW = "\033[1;33m"
BLUE = "\033[1;34m"
PURPULE = "\033[1;35m"


#print sys.path
#import __init__


# jshadobf
import jshadobf

sep = os.sep



PRGM_DIRECTORY = dirname + sep + "prgms"
RESSOURCES_DIRECTORY = dirname + sep + "ressources"
OUTPUT_DIRECTORY = dirname + sep + "output"
RANDOM_LIST = RESSOURCES_DIRECTORY + sep + "randomlist"
TEST_DIR_NAME = "mytest"
TEST_DIR = dirname + sep + TEST_DIR_NAME
RANDOM_MATA = RESSOURCES_DIRECTORY + sep + "mata"
RANDOM_MATB = RESSOURCES_DIRECTORY + sep + "matb"

FIBO_PRGM = "fibo.js"
SORT_PRGM = "sort.js"
ALERT_PRGM = "alert.js"
ALERTUGLIFYJS_PRGM = "alertuglifyjs.js"
MATMUL_PRGM = "matmul.js"
SWITCHCASE_PRGM = "switchcase.js"
EXPRS_PRGM = "exprs.js"
GENERIC_PRGM = ["functional.js", "trycatch.js", "trycatch2.js",
    "some_examples.js", "closure_modules.js","simple.js",
    "functional_inheritance.js", "hiding_sigletons_with_closure.js",
    "stringtest.js", "globalvar.js", "variables.js","getset.js","var.js"]

JQUERYDIR = os.path.join(os.path.expanduser("~"), "version/git/jquery/")
JQUERY_INIT = "dist/jquery.js.orig"
JQUERY = "dist/jquery.js"
JQUERY_CONFIG = "grunt.js"


INCLUDE = "default.js"
NTIMES = 1
TOINCLUDE = open(PRGM_DIRECTORY + sep + INCLUDE).read()

import tempfile

RANDOM_SEED = time.time()

TEMPRAM = "/dev/shm/jshadobf"
try:
    if not os.path.isdir(TEMPRAM):
        os.makedirs(TEMPRAM)
except OSError as e:
    if e.errno:
        print "race lost for %s creation" %TEMPRAM
    else:
        raise (e)
        
TEMP_DIRECTORY = tempfile.mkdtemp("%f.%d" % (RANDOM_SEED, os.getpid()),
    dir=TEMPRAM)

TRANSFO_TEST = 1
#~ def getclasses ():
  #~ listfiles = os.listdir(TEST_DIR)
  #~ classes = []
  #~ for f in listfiles:
    #~ if f[-3:] == ".py":
      #~ s = open(TEST_DIR+os.sep+f).read()
      #~ for l in s.splitlines() :
        #~ if re.search("^class.*\(.*unittest\.TestCase.*\).*:", l):
          #~ classes.append((f[:-3],l[len("class"):l.find("(")].strip()))
  #~ return classes
#~ def getnamesandclasses (classnames):
  #~ classnamesandclass = []
  #~ listtests = []
  #~ for f,c in classnames:
    #~ module = __import__(".".join([TEST_DIR_NAME,f]))
    #~ for i in dir(getattr(getattr(module,f),c)):
      #~ if i[:5] == "test_":
        #~ filename = f
        #~ classname = c
        #~ classobj = getattr(getattr(module,f),c)
        #~ classandtestfun =c+"."+i
  #~ classnamesandclass.append((filename,classname,classobj,classandtestfun,i))
  #~ return classnamesandclass


def execute_command(cmd, verbose=0, get_time=False, get_res=False):
    ret = None
    if verbose > 1:
        print BLUE + cmd + BLACK
    t1 = time.time()
    p = subprocess.Popen(cmd, shell=True,
        stdout=subprocess.PIPE, stdin=subprocess.PIPE)
    ret = [p.stdout.read()]
    res = p.wait()
    t2 = time.time()

    if verbose > 3:
        print ret
    if get_time:
        ret.append(t2 - t1)
    if get_res:
        ret.append(res)
    if len(ret) > 1:
        return tuple(ret)
    return ret[0]


def getnewfilename(directory="./", prefix="", postfix=".js"):
#    files = os.listdir(directory)
#    num = 0
#    while prefix + "%06d" % num + postfix in files:
#        num += 1
#    return directory + os.sep + prefix + "%06d" % num + postfix
    return tempfile.mktemp(dir=directory,prefix=prefix,suffix=postfix)
    

def writesync(filepath, data):
    f = open(filepath, mode='w')
    f.write(data)  # .encode( "utf-8" ))
    f.close()


def print_tree_and_parse_again(tree, verbose=0):
    filepath = getnewfilename(TEMP_DIRECTORY)
    writesync(filepath, format(tree))
    c2 = jshadobf.common.convert(filepath, False)
    filepath = getnewfilename(TEMP_DIRECTORY)
    writesync(filepath, format(c2))
    c3 = jshadobf.common.convert(filepath)
    if verbose > 3:
        print c2
        jshadobf.common.tree_printer.print_level_order(c2)
        print "---------------------------------------"
        print c3
        jshadobf.common.tree_printer.print_level_order(c3)
    return format(c2), format(c3)


def gen_random_mat(w, h):
    return [[jshadobf_random.randint(0, 10000) for i in range(w)] for j in range(h)]

#