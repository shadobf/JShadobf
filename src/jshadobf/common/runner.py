import subprocess
import os
import tempfile
import time, traceback
from jshadobf.common.colors import blue

def execute_command(cmd,verbose=0,get_time=False,get_res=False):
    if verbose >1:
        print blue(cmd)
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

class GenericRunner(object):
    
    def __init__(self, interpreter, program_path, temp_progam_name, verbose, temp_dir, remove_temp, extra_end_file=None):
        self.interpreter = interpreter
        self.program_path = program_path
        self.temp_progam_name = temp_progam_name
        self.verbose = verbose
        self.temp_dir = temp_dir
        self.remove_temp = remove_temp
        self.extra_end = ''
        if extra_end_file != None:
            self.extra_end = open(extra_end_file).read()
        self.answer = None

    def setup(self):
        if not os.path.isdir(self.temp_dir):
            try:
                os.mkdir(self.temp_dir)
            except Exception:
                pass

    def create_reference_executable(self):
        self.reference_executable = getnewfilename(directory=self.temp_dir,
            prefix=self.temp_progam_name, postfix=".js")
        f = open(self.reference_executable, "w")
        f.write(open(self.program_path).read()+self.extra_end)
        f.close()
        
    def create_file_from_tree(self):
        self.modified_executable = getnewfilename(directory=self.temp_dir,
            prefix=self.temp_progam_name, postfix=".js")
        f = open(self.modified_executable, "w")
        f.write(format(self.program_tree)+self.extra_end)
        f.flush()
        f.close()    

        
    def compute_default_result(self):
        if self.answer is None:
            self.create_reference_executable()
            answer, cmd_res2 = execute_command(
                self.interpreter + " " + self.reference_executable, get_res=True)
            if cmd_res2 != 0:
                if self.verbose >= 2:
                    print (self.program_path,
                        self.interpreter, "return a non-zero value")
            self.answer = answer

    def runner(self, program_tree):
        self.program_tree = program_tree
        self.setup()
        self.create_file_from_tree()
        result, tim, cmd_res = execute_command(self.interpreter +
            " " + self.modified_executable, verbose=self.verbose, get_time=True,
            get_res=True)
        self.compute_default_result()
        self.cleanup()
        return self.answer, result, tim, cmd_res

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

