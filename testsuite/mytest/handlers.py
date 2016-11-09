#/usr/bin/env python

import random
import os
import traceback
import shutil
import hashlib
import base64
import sys
import subprocess
import time

from . import mytest_common
#from common import *
import numpy

RED = mytest_common.RED
BLACK = mytest_common.BLACK
BLUE = mytest_common.BLUE


class Handler(object):
    answer = None

    def setup(self):
        if not os.path.isdir(mytest_common.RESSOURCES_DIRECTORY):
            try:
                os.mkdir(mytest_common.RESSOURCES_DIRECTORY)
            except Exception:
                pass
        if not os.path.isdir(mytest_common.OUTPUT_DIRECTORY):
            try:
                os.mkdir(mytest_common.OUTPUT_DIRECTORY)
            except Exception:
                pass
        if not os.path.isdir(mytest_common.PRGM_DIRECTORY):
            print RED, "no program directrory", BLACK
            sys.exit(1)
        if not os.path.isdir(self.temp_dir):
            try:
                os.mkdir(self.temp_dir)
            except Exception:
                pass
    def __init__(self, interpreter="node", program_path="generic.js",
        temp_progam_name="generic.js", verbose=0, temp_dir="",
        remove_temp=False, cleanall=False,debug=False):
        
        self.interpreter = interpreter
        self.program_path = program_path
        self.temp_progam_name = temp_progam_name
        self.verbose = verbose
        self.temp_dir = temp_dir
        self.remove_temp = remove_temp
        self.modified_executable = ""
        self.cleanall = cleanall
        self.reference_executable = ""
        self.debug = debug

    def create_reference_executable(self):
        self.reference_executable = mytest_common.getnewfilename(directory=self.temp_dir,
            prefix=self.temp_progam_name, postfix=".js")
        f = open(self.reference_executable, "w")
        f.write(mytest_common.TOINCLUDE + open(self.program_path).read())
        f.close()
        
#        shutil.copy(self.program_path, self.reference_executable)

    def create_file_from_tree(self):
        self.modified_executable = mytest_common.getnewfilename(directory=self.temp_dir,
            prefix=self.temp_progam_name, postfix=".js")
        f = open(self.modified_executable, "w")
        f.write(mytest_common.TOINCLUDE + format(self.program_tree))
        f.flush()
        f.close()    

    def create_files(self):
        self.create_reference_executable()
        self.create_file_from_tree()

    def cleanup(self):
        try:
            if self.remove_temp:
                if self.modified_executable != "":
                    if self.verbose >2:
                        print "rm ",self.modified_executable
                    os.remove(self.modified_executable)
                if self.reference_executable != "":
                    if self.verbose >2:
                        print "rm ",self.reference_executable
                    os.remove(self.reference_executable)
                    
        except Exception as e:
            if self.verbose > 1:
                print traceback.print_exc()
                print e

    def runner(self, program_tree):
        raise NotImplemented


class GenericHandler(Handler):
    def default_runner(self):
        if self.answer is None:
            self.create_files()
            answer, cmd_res2 = mytest_common.execute_command(
                self.interpreter + " " + self.reference_executable, get_res=True)
            if cmd_res2 != 0:
                if self.verbose >= 2:
                    print (self.program_path,
                        self.interpreter, "return a non-zero value")

            self.answer = answer

    def runner(self, program_tree):
        self.program_tree = program_tree
        self.setup()
        self.create_files()
        result, tim, cmd_res = mytest_common.execute_command(self.interpreter +
            " " + self.modified_executable, verbose=self.verbose, get_time=True,
            get_res=True)
        self.default_runner()
        self.cleanup()

        return self.answer, result, tim, cmd_res


class AlertHandler(Handler):
    def runner(self, program_tree):
        inp = [str(jshadobf_random.randint(0, 999)) for i in range(1000)]
        self.setup()
        self.program_tree = program_tree
        self.create_files()
        cmd1 = self.interpreter + " " + self.reference_executable
        if self.verbose > 1:
            print BLUE, cmd1, BLACK

        p = subprocess.Popen(cmd1, shell=True, stdout=subprocess.PIPE,
            stdin=subprocess.PIPE)
        for i in inp:
            p.stdin.write(i + "\n")
        p.stdin.close()
        answer = p.stdout.read()
        cmd2 = self.interpreter + " " + self.modified_executable
        if self.verbose > 1:
            print BLUE, cmd2, BLACK

        t1 = time.time()
        p = subprocess.Popen(cmd2, shell=True, stdout=subprocess.PIPE,
            stdin=subprocess.PIPE)
        t2 = time.time()
        for i in inp:
            p.stdin.write(i + "\n")
        p.stdin.close()
        cmd_res = p.wait()
        res = p.stdout.read()
#        print cmd_res

    
        self.cleanup()

        return answer, res, t2 - t1, cmd_res


class FiboHandler(Handler):
    def runner(self, program_tree):
        self.setup()
        def fibo(n):
            return fast_fibo(0, 1, n)

        def fast_fibo(n1, n2, i):
            if i == 0:
                return n1
            else:
                return fast_fibo(n2, n1 + n2, i - 1)
        self.program_tree = program_tree
        self.create_files()

        num = jshadobf_random.randint(15, 30)
        num = 28
        answer = fibo(num)

        result, tim, cmd_res = mytest_common.execute_command(self.interpreter +
            " " + self.modified_executable + " %d" % num, verbose=self.verbose,
                get_time=True, get_res=True)
        self.cleanup()
        return answer, int(result), tim, cmd_res


class SwitchcaseHandler(Handler):
    def runner(self, program_tree):
        self.program_tree = program_tree
        self.setup()
        self.create_files()
        result = ""
        t = 0
        tim = 0
        answer = ""
        for i in range(10):
            num = jshadobf_random.randint(0, 4)
            if num == 1:
                answer += "one\n"
            elif num == 2:
                answer += "two\n"
            else:
                answer += "unknown\n"
            r, t, cmd_res = mytest_common.execute_command(self.interpreter +
                " " + self.modified_executable + " %d" % num, verbose=self.verbose,
                get_time=True, get_res=True)
            result += r
            tim += t
        self.cleanup()

        return answer, result, tim, cmd_res


class SortHandler(Handler):
    random_list = ""
    lout = ""

    def setup(self):
        super(SortHandler,self).setup()

        self.random_list = mytest_common.getnewfilename(
            directory=self.temp_dir, prefix="randomlist", postfix="")
        f = open(self.random_list, "w")
        for i in range(1000):
            f.write("%d\n" % jshadobf_random.randint(0, 10000))
        f.close()

    def runner(self, program_tree):
        self.program_tree = program_tree
        self.setup()
        self.create_files()
        self.lout = mytest_common.getnewfilename(directory=self.temp_dir,
            prefix="sort", postfix="")

#  print "rhino " + modified_executable + " %s %s" %(RANDOM_LIST,lout)
        ret, tim, cmd_res = mytest_common.execute_command(self.interpreter +
            " " + self.modified_executable + " %s %s" % (self.random_list, self.lout),
            verbose=self.verbose, get_time=True, get_res=True)

        answer = map(lambda x: int(x),
            filter(lambda x: x != "",
                map(lambda x: x.strip(),
                    open(self.random_list).read().split("\n"))))
        answer.sort()
        result = ""
        try:
            result = map(lambda x: int(x),
                filter(lambda x: x != "",
                    map(lambda x: x.strip(),
                        open(self.lout).read().split("\n"))))
        except Exception as e:
            if self.verbose > 1:
                print e
        self.cleanup()

        return answer, result, tim, cmd_res

    def cleanup(self):
        Handler.cleanup(self)
        if self.remove_temp:
            os.remove(self.lout)
            os.remove(self.random_list)


class ExprsHandler(Handler):
    modified_executable = ""

    def __init__(self, *args):
        Handler.__init__(self, *args)

        
    def setup(self):
        super(ExprsHandler,self).setup()
        numbers = [jshadobf_random.randint(0, 1000) for i in range(10)]
        numbers = list(set(numbers))
        varlist = []
        ##["var%d"% n for n in numbers ]
        operators = ['+', '-', '*', '/', "%", ">>", '<<']
        compoperators = ['==', '!=', '<', '>', '<=', '>=']
        booleanbit = ["&&", "&", "||", "|", "^"]

        lenghtmax = 2
        numexprs = 20

        def randname(n):
            return "".join([chr(jshadobf_random.randint(97, 97 + 26))
                for i in range(n)])

        def gennumberorstrorvar(varlist):
            s = ""
            if False:
                s = varlist[jshadobf_random.randint(0, len(varlist) - 1)]
            else:
                if jshadobf_random.randint(0, 6) < 3:
                    s = "%f" % (jshadobf_random.randint(1, 10000) /
                        float(jshadobf_random.randint(1, 10000)))
                else:
                    if jshadobf_random.randint(0, 6) < 3:
                        s = "'" + randname(10) + "'"
                    else:
                        s = "%d" % random.randint(1, 10000)
            return s

        def gennumberorstr():
            s = ""

            if jshadobf_random.randint(0, 6) < 3:
                s = "%f" % (jshadobf_random.randint(1, 10000) /
                    float(jshadobf_random.randint(1, 10000)))
            else:
                if jshadobf_random.randint(0, 6) < 3:
                    s = "'" + randname(10) + "'"
                else:
                    s = "%d" % jshadobf_random.randint(1, 10000)
            return s
        i = 0

        strout = ""
        for v in varlist:
            strout += "var %s = %s" % (v, gennumberorstr())

        for i in range(numexprs):
            j = 0
            expr = ""
            while jshadobf_random.randint(1, lenghtmax) - j > 0:
                j += 1
                k = 0
                expr2 = ""
                while jshadobf_random.randint(1, lenghtmax) - k > 0:
                    expr3 = gennumberorstrorvar(varlist)
                    k += 1
                    l = 0
                    while jshadobf_random.randint(1, lenghtmax) - l > 0:
                        l += 1
                        if jshadobf_random.randint(0, lenghtmax) == 0:
                            expr3 += compoperators[jshadobf_random.randint(0,
                                len(compoperators) - 1)] + gennumberorstrorvar(
                                    varlist)
                        elif jshadobf_random.randint(0, lenghtmax) == 0:
                            expr3 += booleanbit[jshadobf_random.randint(0,
                                len(booleanbit) - 1)] + gennumberorstrorvar(
                                    varlist)
                        else:
                            expr3 += operators[jshadobf_random.randint(0,
                                len(operators) - 1)] + gennumberorstrorvar(
                                    varlist)
                    if expr2 != "":
                        expr2 += operators[
                            jshadobf_random.randint(0, len(operators) - 1)]
                    expr2 += "(" + expr3 + ")"
                if expr != "":
                    expr += operators[jshadobf_random.randint(0, len(operators) - 1)]
                expr += "(" + expr2 + ")"

            strout += "print(" + expr + ");\n"

#    def setup(self):

        self.reference_executable = mytest_common.getnewfilename(directory=self.temp_dir,
            prefix=self.temp_progam_name, postfix=".js")
        
#        f.write(mytest_common.TOINCLUDE + open(self.program_path).read())
        
        f = open(self.reference_executable, "w")
        f.write(mytest_common.TOINCLUDE + strout)
        f.close()

    def runner(self, program_tree):
        self.setup()
        self.program_tree = program_tree
        self.create_files()
        result, tim, cmd_res = mytest_common.execute_command(self.interpreter
            + " " + self.modified_executable, verbose=self.verbose,
            get_time=True, get_res=True)
        answer = mytest_common.execute_command(self.interpreter
            + " " + self.reference_executable)
        self.cleanup()

        return answer, result, tim, cmd_res


class MatmulHandler(Handler):
    mataf = ""
    matbf = ""
    lout = ""
    modified_executable = ""

    def setup(self):
#        print "setup"
        super(MatmulHandler,self).setup()
        Handler.setup(self)
        self.mataf = mytest_common.getnewfilename(directory=self.temp_dir,
            prefix="mata", postfix="")
        self.matbf = mytest_common.getnewfilename(directory=self.temp_dir,
            prefix="matb", postfix="")
        self.lout = mytest_common.getnewfilename(directory=self.temp_dir,
            prefix="list", postfix="")


    #~ w,h  = random.randint(100,200),random.randint(100,200)
        w, h = 150, 150
        self.mata = mytest_common.gen_random_mat(w, h)
        self.matb = mytest_common.gen_random_mat(h, w)
        f = open(self.mataf, "w")
        for l in self.mata:
            f.write(",".join(map(format, l)) + "\n")
        f.close()
        f = open(self.matbf, "w")
        for l in self.matb:
            f.write(",".join(map(format, l)) + "\n")
        f.close()

    def runner(self, program_tree):
        self.program_tree = program_tree
        self.setup()
        self.create_file_from_tree()
        ret, tim, cmd_res = mytest_common.execute_command(self.interpreter
            + " " + self.modified_executable + " %s %s %s" % (self.mataf, self.matbf,
                self.lout),
            verbose=self.verbose, get_time=True, get_res=True)
        c = numpy.dot(self.mata, self.matb)
        answer = map(list, c)
        result = None
        try:
            result = map(lambda x:
                map(lambda y: int(y), x.split(",")),
                    filter(lambda x: x != "",
                        map(lambda x: x.strip(),
                            open(self.lout).read().splitlines())))
        except Exception as e:
            if self.verbose > 1:
                print traceback.print_exc()
                print e
#        print mytest_common.YELLOW ,"\n".join(traceback.format_stack()), mytest_common.BLACK
        self.cleanup()
        return answer, result, tim, cmd_res

    def cleanup(self):
        
#        print mytest_common.RED ,"\n".join(traceback.format_stack()), mytest_common.BLACK
        try:
            Handler.cleanup(self)
            if self.remove_temp:
                os.remove(self.lout)
                os.remove(self.mataf)
                os.remove(self.matbf)
                if self.verbose > 2 :
                    print "rm,",self.lout
                    print "rm,",self.mataf
                    print "rm,",self.matbf
        except Exception as e:
            if self.verbose > 1:
                print traceback.print_exc()
                print e


class JQueryHandler(Handler):
    jquerydir = mytest_common.JQUERYDIR
    jquery = mytest_common.JQUERY
    config = mytest_common.JQUERY_CONFIG
    answer = None

#  lout = ""version/git/jquery
#  modified_executable = ""

    def create_copydir(self):
        self.reference_directory = mytest_common.getnewfilename(
            directory=self.temp_dir, prefix=self.temp_progam_name,
            postfix=".js")
        shutil.copytree(self.jquerydir, self.reference_directory)

#    def setup(self):
#        Handler.setup(self)

#  def create_files(self):

    def get_default(self):
        if self.answer is None:
#            if self.verbose >= 2:
#                h = hashlib.md5()
#                h.update(open(os.path.join(self.reference_executable,
#                        self.config), "r").read())
#                print "md5 %s %s" % (os.path.join(self.jquerydir, self.jquery),
#                    base64.b16encode(h.digest()))

            answer, dummy, self.cmd_res = mytest_common.execute_command(
                os.path.join(self.reference_directory, "node_modules/grunt/bin/")
                    + "grunt  --config " + os.path.join(self.reference_directory,
                        self.config)
                    + "  qunit", verbose=self.verbose,
                    get_time=True, get_res=True)
            self.answer = answer[:answer.rfind("(")]
            self.answer = "\n".join(filter(lambda x: x.find("file:") != -1,
                self.answer.splitlines()))

    def runner(self, program_tree):
        self.setup()
        self.program_tree = program_tree
        self.create_copydir()
#    self.create_files()
        self.get_default()

        self.modified_executable = mytest_common.getnewfilename(directory=self.temp_dir,
            prefix=self.temp_progam_name, postfix=".js")
        f = open(self.modified_executable, "w")
        f.write(format(self.program_tree))
        f.close()

        shutil.copy(self.modified_executable, os.path.join(self.reference_executable, self.jquery))
        if self.verbose >= 2:
            h = hashlib.md5()
            h.update(open(os.path.join(self.reference_executable,
                self.jquery), "r").read())
            print "md5 %s %s" % (os.path.join(self.reference_executable, self.jquery),
                base64.b16encode(h.digest()))

        result, tim, cmd_res = mytest_common.execute_command(
            os.path.join(self.reference_executable, "node_modules/grunt/bin/")
            + "grunt  --config " + os.path.join(self.reference_executable, self.config)
            + "  qunit", verbose=self.verbose, get_time=True, get_res=True)
        result = result[:result.rfind("(")]
        result = "\n".join(filter(lambda x: x.find("file:") != -1,
            result.splitlines()))
        if cmd_res == self.cmd_res : 
            ret_code = 0
        else:
            ret_code = cmd_res
        self.cleanup()

        return self.answer, result, tim, ret_code

    def cleanup(self):
        try:
            if self.remove_temp:
                shutil.rmtree(self.reference_executable)
            Handler.cleanup(self)
        except Exception as e:
            if self.verbose > 1:
                print traceback.print_exc()
                print e
#