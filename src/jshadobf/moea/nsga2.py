#!/usr/bin/env python

from jshadobf.moea.moea_common import *

import ea
from jshadobf.common.common import jshadobf_random
class NSGAII(ea.EA):


    verbose = 0

    def __init__(self,**kwargs):
        
 
        
        super( NSGAII, self ).__init__(**kwargs)
        self.pop_max =self.population.pop_max
        self.graph = self.population.graph
        self.population.crossover =self.crossover
        self.population.selection = self.selection
        
    def dominate(self,p,q):
        for key in p.objectives_keys:
            if p.objectives[key]>=q.objectives[key]:
                return False
        return True

    def fast_non_dominated_sort(self,population):
        F = [[]]
        p_ind = 0
        s = {}

        for p in population:
            s[p] = []
            p.n= 0
            for q in population:
                if self.dominate(p,q) :
                    s[p].append(q)
                elif self.dominate (q,p):
                    p.n+=1
            if p.n == 0 :
                p.rank = 1
                F[0].append(p)

        i = 0 
        while F[i] != []:
            Q = []
            for p in F[i]:
                for q in s[p]:
                    q.n -= 1
                    if q.n == 0 :
                        q.rank = i+2
                        Q.append(q)
            i +=1
            F.append(Q)
        i = 0
        assert (sum(map(len,F))==len(population))
        return F

    def inf(self,i,j):
        return i.rank < j.rank or (i.rank == j.rank  and i.distance > j.distance )

    def crossover(self):
        print "here"
        tocross =[]
        pop_max = self.population.pop_max
        indexes = range(pop_max)
        for i in range(pop_max):
#            print indexes
            ri_ = jshadobf_random.randrange(0,len(indexes))
            ri = indexes[ri_]
            del indexes[ri_]
            rj = jshadobf_random.randrange(0,pop_max)
            tocross.append((ri,rj))
        self.population.do_crossover(tocross)


    def crowding_distance_assignment(self,I):
        l = len (I)
        for i in I:
            i.distance = 0.
        for key in I[0].objectives_keys:
            I = sorted(I,cmp= lambda x,y : x.objectives[key]<=y.objectives[key])
            I[0].distance = I[-1].distance = float("infinity")
            for i in range(1,l-1 ):
                if (I[-1].objectives[key] -I[0].objectives[key]) == 0:
                    I[i].distance = float("infinity")
                else:
                    I[i].distance= I[i].distance + (I[i+1].objectives[key] - I[i-1].objectives[key] ) / (I[-1].objectives[key] -I[0].objectives[key])
                
#    def initialisation_phase(self):
#        pass


    def selection(self):
#        self.objectives = self.population.objectives
        pop_max = self.population.pop_max
        F = self.fast_non_dominated_sort(self.population.pop_list)
        Pnew = []
        i = 0
        while len(Pnew) + len(F[i]) <= pop_max:
            Pnew += F[i]
            i += 1 
            if (i>= len(F)):
                break
        if (i < len(F)):
            self.crowding_distance_assignment(F[i])
            F[i] = sorted(F[i],cmp=self.inf)
            Pnew += F[i][0:pop_max-len(Pnew)]
        self.population.pop_list = Pnew
