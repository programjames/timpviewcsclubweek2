# Use a genetic algorithm to get an approximation for e using 0, 1, 2, ..., 9.
import random
import numpy as np
import math
import dependency
import time
import matplotlib.pyplot as plt

np.random.seed(2)
random.seed(2)

#### This code (between these comments) is taken from https://blog.klipse.tech/python/2016/09/22/python-reverse-polish-evaluator.html

ops = {
  "+": (lambda a, b: a + b),
  "-": (lambda a, b: a - b),
  "*": (lambda a, b: a * b),
  "/": (lambda a, b: a / b),
  "^": (lambda a, b: a**b)
}

def eval(expression):
  tokens = expression.split()
  stack = []

  for token in tokens:
    if token in ops:
      arg2 = stack.pop()
      arg1 = stack.pop()
      if(token == "^" and arg2 * math.log(abs(arg1)) > 50):
          raise Exception("Too big!")
      result = ops[token](arg1, arg2)
      stack.append(result)
    else:
      stack.append(int(token))

  return stack.pop()

####

codetoop = {
    0: "+",
    1: "-",
    2: "*",
    3: "/",
    4: "^"
}

num = 9

class Genome(object):
    
    def __init__(self, order=None, ops=None):
        if(order is None):
            self.order = np.random.permutation(list(range(1, num+1)) + ["op"]*(num-1))
        else:
            self.order = order
        if(ops is None):
            self.ops = np.random.randint(len(codetoop), size=num-1)
        else:
            self.ops = ops
        self.s = None
        self.v = None

    def string(self):
        s = ""
        j = 0
        for i in self.order:
            if i == "op":
                s += codetoop[self.ops[j]] + " "
                j += 1
            else:
                s += str(i) + " "
        return s[:-1]

    def value(self):
        try:
            k = eval(self.string())
            if not isinstance(k, complex):
                self.v = k
                return k
            else:
                self.v = 1 << 20
                return 1 << 20
        except Exception as e:
            self.v = 1 << 20
            return 1 << 20
    
    def score(self):
        if self.s is not None:
            return self.s
        try:
            self.s = (math.e - self.value())**2
            return self.s
        except:
            self.s = 1 << 41
            return 1 << 41
        
    def mutate_order(self):
        a, b = np.random.choice(range(2*num-1), size=2, replace=False)
        self.order[a], self.order[b] = self.order[b], self.order[a]

    def mutate_ops(self):
        a = np.random.randint(num-1)
        self.ops[a] = np.random.randint(len(codetoop))

    def copy(self):
        return Genome(self.order.copy(), self.ops.copy())

pop_size = 1000

def new_generation(pop):
    l = len(pop)
    pop = sorted(pop, key=lambda g: g.score())
    proportion = l//100
    best = pop[:proportion]
    new_pop = best[:]
    for i in range(proportion*30):
        g = random.choice(best).copy()
        for i in range(1 + np.random.randint(num*2-1)):
            g.mutate_order()
        new_pop.append(g)
    for i in range(proportion*30):
        g = random.choice(best).copy()
        for i in range(1 + np.random.randint(num)):
            g.mutate_ops()
        new_pop.append(g)
    while len(new_pop) < pop_size:
        new_pop.append(Genome())
    
    return new_pop, pop[0]

def dot_plot(x, r=0.1):
    # returns sorted points and limits
    def dist_squared(x1, y1, x2, y2):
        return (x1 - x2)**2 + (y1-y2)**2
    def taxicab(x1, y1, x2, y2):
        return abs(x1-x2) + abs(y1-y2)
    x.sort()
    r_squared = r*r
    points = []
    for i, v in enumerate(x):
        #print(i)
        close = []
        j = i-1
        y = 0
        if abs(v) < 100:
          while j >= 0 and v - x[j] < r:
            close.append(points[j])
            j -= 1
        while any(dist_squared(p[0], p[1], v, y) < r_squared for p in close):
            y += r
            for p in close:
                d = dist_squared(p[0], p[1], v, y)
                if p[1] <= y and d > r_squared:
                    close.remove(p)
        points.append([v, y])
    return points


plt.ion()
fig, ax = plt.subplots()
x, y = [], []
sc = ax.scatter(x, y)
plt.xlim(-100, 100)
plt.ylim(0, 10)

plt.draw()

population = [Genome() for i in range(pop_size)]
while True:
    new_population, best = new_generation(population)
    k = best.s**0.5
    n = 0
    for g in population:
      if g.s < best.s * 10:
        n += 1

    r = 0.1
    points = dot_plot([g.v for g in population], r)
    d = 10
    plt.xlim(math.e - d, math.e + d)
    plt.ylim(0, 10)
    sc.set_offsets(points)
    fig.canvas.draw_idle()
    plt.pause(0.1)

    population = new_population
    print(f"Closest value: {best.value()}")
    print(f"With string: {best.string()}")
