#/usr/bin/env python

import copy

from mytest_common import jshadobf
#import jshadobf
import mytest_common
#import common

import traceback

class MyTest(object):
    success = True
    errors = []
    failed = []
    cleanall = False

    def __init__(self, runner):
        print runner.__class__
        self.errors = []
        self.failed = []
        self.runner = runner
        self.program_path = runner.program_path
        self.temp_progam_name = runner.temp_progam_name
        self.cleanall = runner.cleanall
        self.verbose = runner.verbose
        self.temp_dir = runner.temp_dir
        self.remove_temp = runner.remove_temp
        self.verbose = runner.verbose
        self.success = False
        self.debug = runner.debug

    def assertEqual(self, a1, a2,msg=""):
        if a1 != a2:
            self.success = False
            err = "assertEqual failed"
            if self.verbose > 0:
                err += "\n" + format(a1) + "!=" + format(a2)
            self.errors.append(err)
    def assertTrue(self, v,msg=""):
        if not v:
            self.success = False
            err = "assertTrue failed"
            if self.verbose > 0:
                err += "\n" + format(v) + "!= True " + msg
            self.errors.append(err)
    def assertFalse(self, v,msg=""):
        if v:
            self.success = False
            err = "assertTrue failed"
            if self.verbose > 0:
                err += "\n" + format(v) + "!= False"  
            self.errors.append(err)

    def assertRunWell(self, value,msg=""):
        if value:
            self.success = False
            err = "assertRunWell failed"
            if self.verbose > 0:
                err += "\n" + "return value : %d" % value
            self.errors.append(err)
    
    
    def assertValidTree (self,tree,msg=""):
        err = jshadobf.common.common.check_tree(tree)
        if err != "":
            self.errors.append("assertValidTree failed\n"+err)
            self.success = False
            
    def assertReturnCode(self,msg=""):
        if self.cmd_res != 0 :  
            self.errors.append("assertReturnCode failed %s != 0\n" %self.cmd_res + "\n" + format(self.runner.modified_executable))
            self.success = False
#            print self.runner.
        
        

    def run_test(self):
        self.success = True
        try:
            ret = self.test()
            if ret != 0:
                self.success = False
                self.errors.append(format(ret))
        except Exception as e:
            self.success = False
            self.errors.append(e)
            if self.verbose > 1:
                traceback.print_exc()
                print e

#classes starting with "Test" are considered as test

class Generic_TestTransformation(MyTest):
    transformations = None

    def run_test(self):
        self.runner.setup()
        MyTest.run_test(self)
#        if self.success or self.cleanall:
#            self.runner.cleanup()

    def test(self):
        if self.transformations is None:
            raise NotImplemented
        c = jshadobf.common.convert(self.program_path)
        for t in self.transformations:
            if self.verbose > 2:
                print "applying transfo:", t.__name__
            c = t(c)
            if self.debug:
                (self.attend, self.result, self.time,
                    self.cmd_res) = self.runner.runner(c)
                self.assertReturnCode()
                self.assertEqual(self.attend, self.result)
                
                self.assertValidTree(c)
                
                c2, c3 = mytest_common.print_tree_and_parse_again(c, self.verbose)
                self.assertEqual(c2, c3)
                if self.errors != []:
                    print self.errors


        
        (self.attend, self.result, self.time,
            self.cmd_res) = self.runner.runner(c)
        self.assertReturnCode()
        self.assertEqual(self.attend, self.result)
        
        self.assertValidTree(c)
        
        c2, c3 = mytest_common.print_tree_and_parse_again(c, self.verbose)

        self.assertEqual(c2, c3)
        

        return self.cmd_res


def pick_function():
    length = len(jshadobf.transformations.transformations)
    return jshadobf.transformations.transformations[
        jshadobf_random.randint(0, length - 1)]



class TestTransformationRename (Generic_TestTransformation):
    def test(self):
        self.transformations = [jshadobf.transformations.rename_variables]
        return Generic_TestTransformation.test(self)


class TestTransformationAddDummyVariables (Generic_TestTransformation):
    def test(self):
        self.transformations = [jshadobf.transformations.add_dummy_variables
            for i in xrange(mytest_common.NTIMES)]
        return Generic_TestTransformation.test(self)


class TestTransformationAddDummyExprs (Generic_TestTransformation):
    def test(self):
        self.transformations = [jshadobf.transformations.add_dummy_exprs
            for i in xrange(mytest_common.NTIMES)]
        return Generic_TestTransformation.test(self)


class TestTransformationAddIf (Generic_TestTransformation):
    def test(self):
        self.transformations = [jshadobf.transformations.add_if_statement
            for i in xrange(mytest_common.NTIMES)]
        return Generic_TestTransformation.test(self)
class TestTransformationAddIf2 (Generic_TestTransformation):
    def test(self):
        self.transformations = [jshadobf.transformations.add_if_statement_2
            for i in xrange(mytest_common.NTIMES)]
        return Generic_TestTransformation.test(self)

class TestTransformationModifyDataFlow1 (Generic_TestTransformation):
    def test(self):
        self.transformations = [jshadobf.transformations.modify_data_flow_1
            for i in xrange(mytest_common.NTIMES)]
        return Generic_TestTransformation.test(self)

class TestTransformationModifyDataFlow2 (Generic_TestTransformation):
    def test(self):
        self.transformations = [jshadobf.transformations.modify_data_flow_2
            for i in xrange(mytest_common.NTIMES)]
        return Generic_TestTransformation.test(self)

class TestTransformationModifyControlFlow1 (Generic_TestTransformation):
    def test(self):
        self.transformations = [jshadobf.transformations.modify_control_flow_1
            for i in xrange(mytest_common.NTIMES)]
        return Generic_TestTransformation.test(self)

class TestTransformationChangeStr (Generic_TestTransformation):
    def test(self):
        self.transformations = [jshadobf.transformations.change_str]
        return Generic_TestTransformation.test(self)


class TestTransformationChangeList (Generic_TestTransformation):
    def test(self):
        self.transformations = [jshadobf.transformations.change_list]
        return Generic_TestTransformation.test(self)



class TestTransformationAggregateData (Generic_TestTransformation):
    def test(self):
        self.transformations = [jshadobf.transformations.aggregate_data]
        return Generic_TestTransformation.test(self)




class TestTransformationDuplicateFunction (Generic_TestTransformation):
    def test(self):
        self.transformations = [jshadobf.transformations.duplicate_function]
        return Generic_TestTransformation.test(self)


class TestTransformationOutlining (Generic_TestTransformation):
    def test(self):
        self.transformations = [jshadobf.transformations.outlining
            for i in xrange(mytest_common.NTIMES)]
        return Generic_TestTransformation.test(self)



class TestTransformationSimplifyIf (Generic_TestTransformation):
    def test(self):
        self.transformations = [jshadobf.transformations.simplify_if]
        return Generic_TestTransformation.test(self)



class TestTransformationRemoveEmptyStatement (Generic_TestTransformation):
    def test(self):
        self.transformations = [
            jshadobf.transformations.remove_empty_statement]
        return Generic_TestTransformation.test(self)


class TestTransformationTryEval (Generic_TestTransformation):
    def test(self):
        self.transformations = [jshadobf.transformations.try_eval]
        return Generic_TestTransformation.test(self)


class TestTransformationAll (Generic_TestTransformation):
    def test(self):
        self.transformations = [pick_function()
            for i in xrange(mytest_common.NTIMES)]
        return Generic_TestTransformation.test(self)



class TestDotOutput(MyTest):

    def test(self):
        self.runner.setup()
        c = jshadobf.common.convert(self.program_path, self.verbose)
        jshadobf.output.dottree.gen_dot(c)
        return 0


class TestMetrics(MyTest):

    def test(self):
        self.runner.setup()

        c = jshadobf.common.convert(self.program_path, self.verbose)
        jshadobf.metrics.halstead(c)
        jshadobf.metrics.mccabe(c)
        jshadobf.metrics.harrison(c)
        jshadobf.metrics.oviedo(c)
        jshadobf.metrics.henry(c)
        jshadobf.metrics.munson(c)
        return 0


class TestParsing(MyTest):

    def test(self):
        self.runner.setup()
        c = jshadobf.common.convert(self.program_path)
        self.assertValidTree(c)
        # PRGM_DIRECTORY+"/"+jsfile,verbose)
        c2, c3 = mytest_common.print_tree_and_parse_again(c, self.verbose)
        self.assertEqual(c2, c3)
        return 0

class MOEA_test(MyTest):
    def __init__(self,**args):
        super(MyTest,self).__init__(**args)

    def test(self):
        self.runner.setup()
        
#        self.errors = []
#        self.failed = []
#        self.runner = runner
#        self.program_path = runner.program_path
#        self.temp_progam_name = runner.temp_progam_name
#        self.cleanall = runner.cleanall
#        self.verbose = runner.verbose
#        self.temp_dir = runner.temp_dir
#        self.remove_temp = runner.remove_temp
#        self.verbose = runner.verbose
#        self.success = False
#        self.debug = runner.debug
#
#        
#        self,handler,program_path=self.program_path,temp_dir=self.temp_dir,
#                 verbose= self.verbose,temp_progam_name=self.temp_progam_name,remove_temp=False,
#                 cleanall=False,debug=False,test_n_times=1,transformations_available=[],**kwargs ):
#        
#        
#        handler = handler(interpreter=interpreter, 
#            program_path=option.program_initial,
#            temp_progam_name="generic.js", verbose=option.verbose,
#            temp_dir=option.tempdir,
#    #        temp_dir=os.path.expanduser("~")+os.sep+"temp/jshadobf",
#            remove_temp=not option.dirty, cleanall=not option.dirty,debug=False)
    
        objectives = ["mu1","mu2","mu3","mu4","mu5","exectime","summu"]
        jshadobf_random.shuffle(objectives)
        objectives = objectives[:jshadobf_random.randrange(1,len(objectives))]
        if self.verbose > 1:
            print "objectives: ", " ".join(objectives)
        options = {"pop_max":15,
               "n_generations_max":4 ,"data_output_dir":"/dev/shm/jshadobf",
               "existing_individuals":[],
               "verbose":self.verbose-1,"graph":False,"mutation_rate":.5,"dumptime":-1,
#               "objectives":objectives,
                   "individual_options" :{"strict":True,"handler":self.runner,
                                          "test_n_times":1,"numbermax":10,
                                          "objectives":objectives,"transformations_available":jshadobf.transformations.transformations,
                                          "compute_all_obj":True}
               }
        
        self.population = jshadobf.moea.jshadobf_ea.JShadobf_Population(**options)
        

        ea = self.algo(population=self.population,verbose=self.verbose)
           

#        population = jshadobf.moea.jshadobf_ea.JShadobf_Population(
#             handler=self.runner,pop_max=10,n_generations_max=3 ,data_output_dir ="/tmp/jshadobf"   )
#        nsga2 = jshadobf.moea.nsga2.NSGAII(population=self.population,verbose=self.verbose)
#        self.population.selection = nsga2.selection 
#        ea = jshadobf.moea.ea.EA(self.population,self.verbose)
        ea.run()
        objectives_keys = self.population.pop_list[0].objectives_keys
        objectives = self.population.pop_list[0].objectives
        similarity = copy.deepcopy(objectives)
        for key in objectives_keys:
            similarity[key] = False
        
        l = []
        for i in self.population.pop_list:
            (self.attend, self.result, self.tim,
            self.cmd_res) = self.runner.runner(i.tree)
            self.assertEqual(self.attend, self.result,"the individual " + format(i) + "failed")
            self.assertReturnCode()
            t = tuple([  i.objectives[key] for key in objectives_keys])
            l.append(t)
        s = set(l)
            
#            for key in :
#                if objectives[key] != i.objectives[key]:
#                    similarity [key] = True
        self.assertTrue(len(s)> options["pop_max"] * .25,"more than 75% are the same individuals")
        
        return 0
    def run_test(self):
#        self.runner.setup()
        MyTest.run_test(self)
#        if self.success or self.cleanall:
#            self.runner.cleanup()

class TestMOEAD(MOEA_test):
    def __init__ (self,**args):
        super(MOEA_test,self).__init__(**args)
        
        self.algo = mytest_common.jshadobf.moea.moead.MOEAD
class TestNSGAII(MOEA_test):
    def __init__ (self,**args):
        super(MOEA_test,self).__init__(**args)
        
        self.algo = jshadobf.moea.nsga2.NSGAII


class TestParseandrun(MyTest):

    def run_test(self):
#        self.runner.setup()
        MyTest.run_test(self)
#        if self.success or self.cleanall:
#            self.runner.cleanup()

    def test(self):

        c = jshadobf.common.convert(self.program_path)
        (self.attend, self.result, self.tim,
            self.cmd_res) = self.runner.runner(c)
        self.assertEqual(self.attend, self.result)
        return self.cmd_res
#~ t = TestTransformationTryEval(ALERT_PRGM,"alert",AlertRunner,0,temp_
#dir="/tmp",remove_temp = True ,verbose = 1 )
#~ t.run_test()