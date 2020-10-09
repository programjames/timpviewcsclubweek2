# Use a genetic algorithm to get an approximation for e using 0, 1, 2, ..., 9.
import random
import numpy as np
import math
import dependency
import time

np.random.seed(2)
random.seed(2)

num = 5

codetoop = {
    0: "+",
    1: "-",
    2: "*",
    3: "/",
    4: "^",
    5: ""
}
class Genome(object):
    
    def __init__(self, order=None, lps=None, rps=None, ops=None):
        if(order is None):
            self.order = np.random.permutation(range(1, num+1))
        else:
            self.order = order
        if(lps is None):
            self.lps = np.random.choice(a=[True, False], size=num)
        else:
            self.lps = lps
        if(rps is None):
            self.rps = np.random.choice(a=[True, False], size=num)
        else:
            self.rps = rps
        if(ops is None):
            self.ops = np.random.randint(6, size=num-1)
        else:
            self.ops = ops
        self.s = None

    def string(self):
        s = "("*8
        p = 8 + sum(1 for p in self.lps if p) - sum(1 for p in self.rps if p)

        if self.lps[0] and self.ops[0] != 5:
            s += "("
        s += str(self.order[0])
        s += codetoop[self.ops[0]]
        for i in range(1, num):
            if self.lps[i] != self.rps[i-1]:
                if self.lps[i]:
                    if self.ops[i-1] != 5:
                        s += "("
                        s += str(self.order[i])
                    else:
                        p -= 1
                        s += str(self.order[i])
                else:
                    if (i == num-1 or self.ops[i] != 5):
                        s += str(self.order[i])
                        s += ")"
                    else:
                        p += 1
                        s += str(self.order[i])
            else:
                s += str(self.order[i])
            if(i != num-1):
                s += codetoop[self.ops[i]]
        if self.rps[-1]:
            s += ")"
        p = s.count("(") - s.count(")")
        if p < 0:
            s = "("*(-p) + s
        if p > 0:
            s += ")"*p
        return s

    def value(self):
        try:
            k = dependency.eval(self.string())
            #print(k)
            if not isinstance(k, complex):
                return k
            else:
                return 1 << 8
        except Exception as e:
            #print(e, self.string())
            return 1 << 8
    
    def score(self):
        if self.s is not None:
            return self.s
        try:
            self.s = (math.e - self.value())**2
            return self.s
        except:
            return 1 << 17

    def mutate_order(self):
        a, b = np.random.choice(range(num), size=2, replace=False)
        self.order[a], self.order[b] = self.order[b], self.order[a]

    def mutate_ops(self):
        a = np.random.randint(num-1)
        self.ops[a] = np.random.randint(6)

    def mutate_lps(self):
        a = np.random.randint(num-1)
        self.lps[a] = np.random.choice([True, False])
    def mutate_rps(self):
        a = np.random.randint(num-1)
        self.rps[a] = np.random.choice([True, False])

    def copy(self):
        return Genome(self.order.copy(), self.lps[:].copy(), self.rps.copy(), self.ops.copy())

pop_size = 1000

def new_generation(pop):
    l = len(pop)
    pop = sorted(pop, key=lambda g: g.score())
    proportion = l//50
    best = pop[:proportion]
    new_pop = best[:]
    for i in range(proportion*10):
        g = random.choice(best).copy()
        for i in range(1 + np.random.randint(num)):
            g.mutate_order()
        new_pop.append(g)
    for i in range(proportion*10):
        g = random.choice(best).copy()
        for i in range(1 + np.random.randint(num)):
            g.mutate_ops()
        new_pop.append(g)
    for i in range(proportion*10):
        g = random.choice(best).copy()
        for i in range(1 + np.random.randint(num)):
            g.mutate_lps()
        new_pop.append(g)
    for i in range(proportion*10):
        g = random.choice(best).copy()
        for i in range(1 + np.random.randint(num)):
            g.mutate_rps()
        new_pop.append(g)
    while len(new_pop) < pop_size:
        new_pop.append(Genome())
    
    return new_pop, pop[0]

population = [Genome() for i in range(pop_size)]
while True:
    population, best = new_generation(population)
    print(best.value(), best.string())
