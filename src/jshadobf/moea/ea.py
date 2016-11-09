import gc
from jshadobf.moea.moea_common import deepcopy
from jshadobf.common.colors import blue, yellow

class Population(object):
    pop_list =[]
    n_generations = 0
    n_generations_max = 20
    pop_max = 100

    def __init__(self, pop_list=[],pop_max=100,n_generations_max=100,mutation_rate=1,objectives=[]):
        self.mutation_rate = mutation_rate
        self.pop_list = pop_list[:]
        self.pop_max = pop_max
        self.n_generations_max = n_generations_max
        self.n_generations = 0
        self.objectives = objectives

    def __str__(self) :
        return "\n".join(map(lambda x : "individu:%d    %s"%(x[0],format(x[1])),     [ (i,self.pop_list[i]) for i in range(len(self.pop_list))] ))

    def raw(self):
        return "\n".join(map(lambda x:self.algo.problem.printer(x), self.pop_list))

    def metric(self):
        return "\n".join(map(lambda x:"  ".join(map(lambda y:"%f"%y(x),self.algo.objectives)) , self.pop_list))

    def evaluation(self):
        raise NotImplementedError

    def population_initialisation(self):
        raise NotImplementedError

    def crossover(self):
        raise NotImplementedError

    def termination(self):
        if self.n_generations == self.n_generations_max:
            return True
        return False

    def selection(self):
        raise NotImplementedError

    def mutation(self):
        raise NotImplementedError

    def extra(self):
        pass


class EA(object):
    population = None
    objectives = None
    verbose = 0

    def __init__ (self,population,verbose=0):
        self.population = population
        self.verbose = verbose

    def initialisation_phase(self):
        self.population.population_initialisation()
        self.adams = deepcopy(self.population.pop_list)
        self.population.conversion()
        self.population.evaluation()
        
    def run(self):
        print 
        if self.verbose > 1:
            print blue("initialisation")
        self.initialisation_phase()
        while True:
            assert self.population.pop_max == len(self.population.pop_list),"len != pop_max"
            self.population.n_generations += 1
            gc.collect()
            if self.verbose >= 1:
                print blue("crossover")
            self.crossover()
            if self.verbose >= 1:
                print blue("mutation")
            self.population.mutation()
            if self.verbose >= 1:
                print yellow( "Generation: %d" %self.population.n_generations) 
            if self.verbose >= 1:
                print blue("evaluation")
            self.population.evaluation()
            if self.population.graph:
                self.population.print_pop(color="r")
            if self.verbose >= 1:
                print blue("selection")
            self.population.selection()
            if self.population.graph:
                self.population.print_pop(color="g")
            self.population.extra()
            if self.population.termination():
                break
        if self.population.graph:
            self.population.print_pop(last=True)
                    