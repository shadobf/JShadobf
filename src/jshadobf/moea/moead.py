import ea
import numpy
import itertools
import math
import gc
import moea_common
from jshadobf.common.common import jshadobf_random
from copy import deepcopy
from jshadobf.moea.moea_common import deepcopy

def nCr(n,r):
    f = math.factorial
    return f(n) / f(r) / f(n-r)

class MOEAD(ea.EA):

    def __init__(self,**kwargs):
#        self.population = population
#        self.initial_objectives = initial_objectives
        super( MOEAD, self ).__init__(**kwargs)
 
#        self.population.selection = self.selection
        self.population.crossover = self.crossover
        self.pop_max =self.population.pop_max
        self.graph = self.population.graph
        self.population.selection = self.selection
        self.nr = 2
        self.delta = 0.9
        self.T = 4


    def generate_lambda(self):
        pop_max,m = self.pop_max,self.m
        l = []
        if m == 2:
            l = [ (r  , 1-r) for r in numpy.linspace(0,1,pop_max)]
        else:
            oldN = 0
            for H in range(pop_max):
#                print H
                N = nCr(H+m-1,m-1)
                if N > pop_max:
                    break
            H = max(H-1,1)
            pas = 1./H
            y = 0.
            x = 0.
            sh = numpy.linspace(0,1,H+1) #   [ float(i)/H for i in range(0,H+1)]
            r = map(lambda x:[x],sh.tolist())
            for i in range(m-1):
                rr= [[r_ +[i] for i in sh] for r_ in r]
                rrr = []
                for rr_ in itertools.chain(rr):
                    rrr += rr_
                rr = rrr
                r = filter(lambda x:sum(x) <= 1,rr )
            l = filter (lambda x: 1.0001 >= sum(x)>=0.9999,r)
            for i in range(nCr(H+m-1,m-1),pop_max):
                ll_ = numpy.array([jshadobf_random.random() for i___ in range(m)])
                ll_ = ll_ / sum(ll_)
                l.append(tuple(ll_))
            print "H:", H , "N:" , nCr(H+m-1,m-1)
        return l[:pop_max]
     
    def compute_B(self):
        l = self.lambda_values
        pop_max = self.pop_max
        ll = numpy.array(l)
        def Bc(i):
            li_ = numpy.array([l[i]]).repeat(len(ll),axis=0)
            ml = numpy.sqrt(numpy.sum((ll - li_)**2,axis=1))
            ml = ml.tolist()
            ml = [ (ml[i_],i_ ) for i_ in range(len(ml))]
            ml.sort()
            ml = ml[:self.T]
            return list(zip(*ml)[1])
        B = []
        for i in range(pop_max):
            B.append(Bc(i))
        return B

    def crossover(self,pop=[]):
        if pop == []:
            pop = self.population.pop_list
        tocross =[]
        for i in range(len(pop)):
            if jshadobf_random.random()< self.delta:
                indexes = self.B[i%self.population.pop_max]
            else:
                indexes = range(len(pop))
            pop.append(deepcopy(pop[i]))
            index = len(pop)-1
            ri = jshadobf_random.choice(indexes)
            tocross.append((index,ri))
        self.population.do_crossover(tocross)

    def initialisation_phase(self):
        self.population.population_initialisation()
        self.adams = deepcopy(self.population.pop_list)
        self.population.conversion()
        self.population.evaluation()
        self.m = len(self.population.pop_list[0].objectives_keys)
        self.lambda_values = self.generate_lambda()
        self.B = self.compute_B()
        self.z = {}

    def selection(self):
        def shuffle(l):
            jshadobf_random.shuffle(l)
            return l
        
        def gte(x,lam):
            obj = [x.objectives[key] for key in x.objectives_keys] 
            obs = [ lam[i]*(abs(obj[i] - self.z[i]))   for i in range(self.m)]
            return max(obs)

        delta = self.delta
        nr = self.nr
        pop_max = self.population.pop_max
        updates= 0
        l = range(len(self.population.pop_list))

        self.z = [self.population.pop_list[0].objectives[k] for k in self.population.pop_list[0].objectives_keys]

        for x in self.population.pop_list:
            obn = x.objectives_keys
            for i_ in range(len(obn)):
                if x.objectives[obn[i_]] < self.z[i_]:
                    self.z[i_] =  x.objectives[obn[i_]] 
        self.gte_= []

        for j in range(len(self.population.pop_list)):
            self.gte_.append( gte(self.population.pop_list[j],self.lambda_values[j%pop_max]) )

        l = range(len(self.population.pop_list))
        jshadobf_random.shuffle(l)

        for i in l:
            #step 2.1
            if jshadobf_random.random() < delta:
                indexes = self.B[i%pop_max][:]
            else:
                indexes = range(pop_max)
            c__ = 0 
            while c__ != nr and indexes != []:
                j = jshadobf_random.choice(indexes)
                if   self.gte_[i]  < self.gte_[j]:
                    self.population.pop_list[j] = deepcopy(self.population.pop_list[i]) 
                    self.gte_[j] = self.gte_[i]
                    c__ += 1
                indexes.remove(j)

        while len(self.population.pop_list) > pop_max:
            del self.population.pop_list[-1] 

