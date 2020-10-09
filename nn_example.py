# A simple neural net example. Rather than using the chain rule to find the gradient (derivative) it approximates it by adding a small delta.

import numpy as np

def sigmoid(x):
    return 1/(1+np.exp(-x))

def sigmoid_prime(x):
    e = np.exp(-x)
    return e/(1+e)**2

def leaky_relu(x):
    return np.maximum(x, 0.1*x)

class NeuralNet():
    def __init__(self, layers, function=sigmoid):
        self.ms = [np.random.rand(layers[i], layers[i+1])*2-1
                   for i in range(len(layers)-1)]
        self.bs = [np.random.rand(layers[i])*2-1 for i in range(1, len(layers))]
        self.function = function

    def evaluate(self, ins):
        for m, b in zip(self.ms, self.bs):
            ins = self.function(np.matmul(ins, m) + b)
        return ins

    def diff(self, data_ins, data_outs):
        ys = np.array([self.evaluate(ins) for ins in data_ins])
        off = np.linalg.norm(ys - data_outs)
        return off

    def train(self, data_ins, data_outs, step=1, dx=0.1):
        for i, m in enumerate(self.ms):
            for j, n in enumerate(m):
                off = self.diff(data_ins, data_outs)
                self.ms[i][j] += dx
                new_off = self.diff(data_ins, data_outs)
                self.ms[i][j] -= dx + step*(new_off - off)/dx
        for i, b in enumerate(self.bs):
            off = self.diff(data_ins, data_outs)
            self.bs[i] += dx
            ys = np.array([self.evaluate(ins) for ins in data_ins])
            new_off = self.diff(data_ins, data_outs)
            self.bs[i] -= dx + step*(new_off - off)/dx
                
if __name__ == "__main__":
    import matplotlib.pyplot as plt

    np.random.seed(1)
    ins = [1, 2]
    nn = NeuralNet([2, 4, 4, 1], function=leaky_relu)
    data_ins = [[0, 0], [1, 0], [0, 1], [1, 1]]
    data_outs = [[0], [1], [1], [0]]
    def output(nn):
        l = []
        for di in data_ins:
            l.append('{}'.format(str(nn.evaluate(di)[0])))
        print(", ".join(l))

    plt.ion()
    fig, ax = plt.subplots()
    ax.set_title("Error of Neural Net")
    x, y = [], []
    Ln, = ax.plot(x, y)

    plt.draw()

    i = 0
    while True:
        d = nn.diff(data_ins, data_outs)
        nn.train(data_ins, data_outs, step=d/100, dx = d/1000)

        x.append(i)
        y.append(d)

        if(i%100 == 0):            
            Ln.set_xdata(x)
            Ln.set_ydata(y)
            k = min(y[0], y[max(0, i-100)]*10)
            start = 0
            while y[start] > k:
                start += 1
            plt.xlim(start, i+5)
            plt.ylim(0, k)
            fig.canvas.draw_idle()
            plt.pause(0.001)
        
        if(i%300 == 0):
            output(nn)
        i += 1
