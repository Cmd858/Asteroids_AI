from Net2 import Net


class Pop:
    def __init__(self, popnum, rannum, keepnum):
        self.popnum = popnum  # total size of population
        self.rannum = rannum  # number of randomly generated networks in each generation
        self.keepnum = keepnum  # number of nets to keep in each generation
        self.main_inputs = None
        self.innovlist = []
        self.nets = []
        for i in range(popnum):
            self.nets.append(Net(8, 4, self))
            for j in range(10):
                # print(j)
                self.nets[i].mutate()
        # hmm no bc dealt with in main, maybe should do in here though?

    def mutate_all(self, repval):  # value to repeat mutation
        for i in range(len(self.nets)):
            for j in range(repval):  #
                self.nets[i].mutate()
                self.nets[i].getlayers()

    def take_main_inputs(self, inputs):  # takes main net inputs from program as list
        self.main_inputs = inputs

    def get_outputs(self):
        pass

    def get_innovs(self):
        return self.innovlist

    def add_innov(self, innov):  # take innov as (in, out)
        if not innov in self.innovlist:
            self.innovlist.append(innov)
            # return len(self.innovlist)-1  # makes first num 0
        # else:
        # do i need to return a value here?

    # generic functions to stop errors  # bc im lazy

    def combfunc(self, a, b):
        pass

    def filesave(self, a, b, c, d):
        pass

    def fileload(self, a):
        pass

    def draw_net(self, screen, x, y, xbuf, ybuf, r):
        self.nets[-1].draw_net(screen, x, y, xbuf, ybuf, r)

# TODO: copy using inheritance instead of deepcopy
# TODO: maybe use same obj instead of expensive delete & remake
# TODO: paper notes below

# NOTE: 30 pg NEAT paper, pg 11 line 3: node mutations have new > out = old weight, in > new = 1 (to minimise impact)
# probs should do something like this maybe  # done this i think

# NOTE2: pg 12 of NEAT paper for combining nets properly

# NOTE3: pg 13 for details of speciation

# NOTE4: pg 10, fig 3; make sure to record disjoint genes

# NOTE5: pg 13 footnotes may be useful

# LINK: http://nn.cs.utexas.edu/downloads/papers/stanley.ec02.pdf

# TODO: move population management to pop2, only allow I/O from external classes
