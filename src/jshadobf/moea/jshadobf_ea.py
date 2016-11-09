import traceback
import time
import os
import sys
import subprocess
import tempfile
from jshadobf.metrics.halstead import halstead
from jshadobf.metrics.mccabe import mccabe
from jshadobf.metrics.munson import munson
from jshadobf.metrics.henry import henry
from jshadobf.metrics.oviedo import oviedo
from jshadobf.moea.moea_common import available_objectives, deepcopy, getnewname_inc
from jshadobf.common.colors import BLACK, BLUE, YELLOW, red, RED, GREEN
from jshadobf.common.common import jshadobf_random
from jshadobf.common.convert import convert, convert_string
from jshadobf.metrics.harrison import harrison
from multiprocessing import Pool, TimeoutError
from jshadobf.common.classes import cleaner
from jshadobf.transformations.common import get_transformation_by_name
from jshadobf.moea.ea import Population


class JShadobf_Individual(object):
    tree = None
    path = ""
    runner = None
    transformations_available = []
    test_n_times = 1
    transformations = []
    apply_transformations = []
    initial_metrics = {}
    n = 0
    verbose = 0
    evaluated = False
    distance = float("infinity")
    objectives = {}
    worst = False

    def __init__(self,runner,tree=None,path="",strict=False, test_n_times=1,numbermax=1000,transformations_available=[],
                 objectives=["mu1","mu2","mu3","mu4","mu5","exectime"],mutation_rate=0.05,evaluated=False,verbose=0):
        self.evaluated = evaluated
        self.verbose = verbose
        self.mutation_rate = mutation_rate
        self.tree = tree
        self.runner = runner
        self.strict = strict
        self.test_n_times = test_n_times
        self.numbermax = numbermax
        if path == "":
            self.path = runner.program_path
        else:
            self.path = path
        self.transformations = []
        self.transformations_available = transformations_available
        self.objectives_keys = objectives
        self.initiate_objectives()

    def __str__(self):
        return "Individu\nid:0x%x, evaluated: %d, objectives:%s" % (id(self),self.evaluated,format(self.objectives)) 

    def __del__(self):
        cleaner(self.tree)
        del self.tree

    def initiate_objectives(self):
        self.objectives = {}
        for k in available_objectives:
            self.objectives [k] = float("infinity")
        
    def list_objectives(self):
        return [self.objectives[k] for k in self.objectives_keys]
    
    def set_worst(self):
        if self.verbose > 1:
            print "SET WORST"
        self.worst = True
        self.initiate_objectives()

    def oneover(self,val):
        if val == 0:
            return 1.
        return 1./val

    def evaluate(self):
        if self.evaluated:
            if self.verbose > 3:
                print "already evaluated"
            return 
        if self.tree == None:
            if self.verbose>2:
                print "convert", self.path
            self.tree =  self.convert(self.path)
        c = self.tree
        self.initiate_objectives()
        
        halstead_p1 = lambda x: 1+halstead(x)
        mccabe_p1 = lambda x: 1+mccabe(x)
        harrison_p1 = lambda x: 1+harrison(x)
        oviedo_p1 = lambda x: 1+ oviedo(x)
        henry_p1 = lambda x: 1+henry(x)
        
        for metric,function in [("mu1",halstead_p1),
                                ("mu2",mccabe_p1),
                                ("mu3",harrison_p1),
                                ("mu4",oviedo_p1),
                                ("mu5",henry_p1)]:
            if self.initial_metrics.has_key(metric):
                self.objectives[metric] = self.initial_metrics[metric]/max(function(c),1)
            else:
                self.initial_metrics[metric] = float(function(c))
                self.objectives[metric] = 1

        self.objectives["mu1mu2"] = self.initial_metrics["mu1"]/max(1,halstead(c)) + \
                self.initial_metrics["mu2"]/max(1,mccabe(c))
        self.objectives["mu1mu2"] /= 2.
        self.objectives["mu1mu2mu3"] = self.initial_metrics["mu1"]/max(1,halstead(c))+ \
                self.initial_metrics["mu2"]/max(1,mccabe(c))+ \
                self.initial_metrics["mu3"]/max(1,harrison(c))
        self.objectives["mu1mu2mu3" ] /= 3.
        self.objectives["mu1mu2mu3mu4"] = self.initial_metrics["mu1"]/max(1,halstead(c))+ \
                self.initial_metrics["mu2"]/max(1,mccabe(c))+ \
                self.initial_metrics["mu3"]/max(1,harrison(c))+ \
                self.initial_metrics["mu4"]/max(1,oviedo(c))
        self.objectives["mu1mu2mu3mu4"] /= 4.
        self.objectives["summu"] = self.initial_metrics["mu1"]/max(1,halstead(c))+ \
                self.initial_metrics["mu2"]/max(1,mccabe(c))+ \
                self.initial_metrics["mu3"]/max(1,harrison(c))+ \
                self.initial_metrics["mu4"]/max(1,oviedo(c))+ \
                self.initial_metrics["mu5"]/max(1,henry(c))
        self.objectives["summu"] /= 5.
        self.evaluated=True

        if "exectime" in self.objectives_keys:
            if self.verbose > 3:
                print ",".join(self.transformations)
            try :
                self.objectives["exectime"] = 0.
                for i in xrange( self.test_n_times ):
                    ans, res, time,cmd_res = self.runner.runner(self.tree)
                    if ans != res :
                        raise ValueError
                    if cmd_res != 0 and cmd_res != None :
                        raise Exception("command result error")
                    self.objectives["exectime"] += time
                self.objectives["exectime"] /= self.test_n_times
                if self.initial_metrics.has_key("exectime"):
                    self.objectives["exectime"] /= self.initial_metrics["exectime"]
                else:
                    self.initial_metrics["exectime"] = self.objectives["exectime"]
                    self.objectives["exectime"] = 1
            except ValueError, e:
                print traceback.print_exc()
                print e
                print "expected answer != result"
                if self.verbose > 1:
                    print BLACK, "*********************"
                    print BLACK, "*********************"
                    print BLACK, "*********************"
                    print res
                self.set_worst()
            except Exception , e:
                self.evaluated=False
                print traceback.print_exc()
                print "Unexpected error:", sys.exc_info()[0]
                if self.strict:
                    print self.tree
                    sys.exit(1)
                self.set_worst()
    
    def format_metrics(self):
        r = self.list_objectives()
        return "% 20e"*len(r) % tuple(r) 

    def format_headers(self):
        return "% 20s"*len(self.objectives_keys) % tuple(self.objectives_keys)

    def convert(self,srccode=None):
        print self.path
        if srccode == None:
            self.tree = convert(self.path)
        else:
            self.tree = convert_string(srccode)

    def mutate(self):
        if self.tree == None:
            if self.verbose>2:
                print "convert", self.path
            self.tree =  self.convert(self.path)
        if self.apply_transformations == []:
            trs = [jshadobf_random.choice(self.transformations_available)]
        else:
            trs = map(lambda x:get_transformation_by_name(x, self.transformations_available), self.apply_transformations)
        for tr in trs:
            self.transformations.append(tr.__name__)
            self.tree = tr(self.tree,verbose=self.verbose) #,numbermax=jshadobf_random.randint(0,self.numbermax))
        self.evaluated = False
        self.apply_transformations = []


def single_cross((ind1, ind2)):
    trs = ind2.transformations[:]
    jshadobf_random.shuffle(trs)
    ind1.apply_transformations=trs[:1]
    if len(ind1.apply_transformations) != 0: 
        ind1.mutate()
    return ind1

def single_mutation((i, mutation_rate)):
    if jshadobf_random.random() < mutation_rate:
        i.apply_transformations= []
        i.mutate()
    return i

def single_eval(x):
    x.evaluate()
    return x

class JShadobf_Population(Population):
    transformations_available = []
    verbose = 0

    def __init__(self,
                 existing_individuals=[],data_output_dir= "/tmp",
                 verbose=0,graph=[],dumptime=5,individual_options={},process=1,**kwargs ):
        self.verbose = verbose
        self.graph = graph
        print "process", process
        self.process = process
        self.dumptime = dumptime
        self.individual_options = individual_options
        self.individual_options["verbose"] = self.verbose
        self.existing_individuals = existing_individuals
        self.data_output_dir = data_output_dir
        if not os.path.isdir (self.data_output_dir):
            os.makedirs(self.data_output_dir)
        super( JShadobf_Population, self ).__init__(**kwargs)
        
    def conversion(self,pop=None):
        if pop == None:
            pop = self.pop_list
        for i in pop:
            if i.tree == None:
                if self.verbose > 1 :
                    print "converting :" + i.path
                i.convert()
    
    def population_initialisation(self):
        pop = []
        for p in self.existing_individuals:
            if self.verbose > 0:
                print "creating population from" , "\n" , p
            if os.path.isdir(p):
                for pp in os.listdir(p):                    
                    i = JShadobf_Individual(path=pp,**self.individual_options)
                    self.pop_list.append(i)
            else:
                i = JShadobf_Individual(path=p,**self.individual_options)
                self.pop_list.append(i)
            if len(self.pop_list)>= self.pop_max:
                if self.verbose > 1:
                    print "too many individual for ",self.pop_max,", continuing without the rest"
                break
        adam =JShadobf_Individual(**self.individual_options) 
        adam.convert()
        adam.evaluate()
        while len(self.pop_list) < self.pop_max:
            self.pop_list += [deepcopy(adam)]

    def erase_pop_list(self):
        while len(self.pop_list) != 0:
            del self.pop_list[0] 
    
    def mutation(self,pop=None):
        if pop == None:
            pop = self.pop_list
        self.conversion(pop)
        if self.process >= 1:
            pool = Pool(processes=self.process,maxtasksperchild=1)
            r = pool.map_async(single_mutation, zip( pop, [self.mutation_rate]*len(pop)))
            r.wait()
            pop = list(r.get())
            pool.close()
            pool.join()
            pool.terminate()
        else:
            new_pop = []
            for p in pop:
                new_pop.append(single_mutation ( ( p , self.mutation_rate)))
            pop = new_pop
        self.erase_pop_list()     
        self.pop_list = pop

    def evaluation(self,pop=None):
        if pop == None:
            pop = self.pop_list
        self.conversion(pop)
        if self.process >= 1:
            pool = Pool(processes=self.process,maxtasksperchild=1)
            r = pool.map_async(single_eval, pop)
            r.wait()
            pop = list(r.get())
            pool.close()
            pool.join()
            pool.terminate()
        else:
            new_pop = []
            for p in pop:
                new_pop.append(single_eval ( p ))
            pop = new_pop
        self.erase_pop_list()
        self.pop_list = pop

    def do_crossover(self,tocross=[],pop=None):
        if pop == None:
            pop=self.pop_list
        self.conversion(pop)
        inds_to_cross = [(pop[i1], pop[i2]) for i1, i2 in tocross]

        if self.process >= 1:
            pool = Pool(processes=self.process,maxtasksperchild=1)
            r = pool.map_async(single_cross, inds_to_cross)
            r.wait()
            extra_pop = list(r.get())
            pool.close()
            pool.join()
            pool.terminate()
        else:
            new_pop = []
            for inds in inds_to_cross:
                new_pop.append(single_cross ( inds ))
            extra_pop = new_pop
        self.pop_list = pop + extra_pop

    def dumper(self):
        index = 0
        for i in self.pop_list:
            if self.verbose > 1:
                sys.stdout.write( "storing individuals: %.2f%%\r" % (index*100./len(self.pop_list)))
                sys.stdout.flush()
            i.path = getnewname_inc(self.data_output_dir+os.sep+"generation.%d"%self.n_generations,prefix="individu.")
            f = open(i.path,"w")
            f.write(format(i.tree))
            f.close()
            index+=1
        if self.verbose > 2: 
            print "stored" +" "*22

    def dump_metrics(self):
        obj = "" 
        if not os.path.isdir (self.data_output_dir):
            os.makedirs(self.data_output_dir)
        obj = "#%s\n" % self.pop_list[0].format_headers() 
        for i in self.pop_list:
            obj += "#%s\n" % " ".join(i.transformations)
            obj += i.format_metrics() +"\n"
            
        f = open(self.data_output_dir + os.sep + "metrics.%d" %self.n_generations,"w")  
        f.write(obj)
        f.close()

    def extra(self):
        self.dump_metrics()
        if (self.n_generations % self.dumptime) == 0 and self.dumptime!=-1:
            self.dumper()
        if self.verbose > 1 :
            print self.pop_list[0].format_headers()
            for i in self.pop_list:
                print "#", " ".join(i.transformations)
                print i.format_metrics()  


    def print_pop(self,last=False,color=None):
        self.nuance = 12
        self.cp = ["%f" % (.8-.8*float(f)/self.nuance) for f in range(self.nuance)]
        self.col = 0
        if self.graph != []:
            import pylab
            if last :
                pylab.ioff()
                dr = pylab.show
            else:
                pylab.ion()
                dr = pylab.draw
            for i in range(len(self.graph)):
                m1,m2 = self.graph[i].split(":")
                x = [ x_.objectives[m1] for x_ in self.pop_list ]
                y = [ x_.objectives[m2] for x_ in self.pop_list ]
                ax = pylab.subplot(1,len(self.graph),i+1)
                ax.set_yscale('log')
                ax.set_xscale('log')
                if color == None:
                    pylab.plot(x,y,".")#,color=self.cp[self.col%len(self.cp)])
                else:
                    pylab.plot(x,y,".",color=color)#,color=self.cp[self.col%len(self.cp)])
            self.col = self.col+1%self.nuance
            pylab.get_current_fig_manager().canvas.flush_events()
            dr()

