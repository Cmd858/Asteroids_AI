from Net2 import Net

class Pop:
    def __init__(self, popnum, rannum, keepnum):
        self.popnum = popnum  # total size of population
        self.rannum = rannum  # number of randomly generated networks in each generation
        self.keepnum = keepnum  # number of nets to keep in each generation
        self.main_inputs = None  # starts as None for some reason, can't remember why
        self.innovlist = []
        self.nets = []
        for i in range(popnum):  # populates self.nets with popnum amount of nets
            self.nets.append(Net(8, 4, self))
            for j in range(10):
                # print(j)
                self.nets[i].mutate()  # applies ten starting mutations to net, maybe should start with less but idk
        # hmm no bc dealt with in main, maybe should do in here though?
        # TODO: introduce speciation

    def mutate_all(self, repval, start=0, end=None):  # value to repeat mutation
        if end is not None:
            poprange = range(start, end)
        else:
            poprange = range(start, self.popnum)
        for i in poprange:
            for j in range(repval):  # iterates through all nets and muatates them
                self.nets[i].mutate()
                self.nets[i].getlayers()  # idk why this is still here

    def take_main_inputs(self, inputs):  # takes main net inputs from program as list
        self.main_inputs = inputs

    def get_outputs(self):
        pass

    def get_innovs(self):
        return self.innovlist  # give list of innovs to nets when requested, yes could be property pycharm but idc

    def add_innov(self, innov):  # take innov as (in, out)
        if not innov in self.innovlist:  # check if innov in list
            self.innovlist.append(innov)  # adds innov to list
            # return len(self.innovlist)-1  # makes first num 0
        # else:
        # do i need to return a value here?

    # generic functions to stop errors  # bc im lazy

    def combfunc(self, a, b):
        pass
        # TODO: actually breed best of the species

    def filesave(self, a, b, c, d):
        pass

    def fileload(self, a):
        pass

    def draw_net(self, net, screen, x, y, xbuf, ybuf, r):
        net.draw_net(screen, x, y, xbuf, ybuf, r)  # calls drawnet() for last net in population bc idk why

# TODO: copy using inheritance instead of deepcopy
# TODO: maybe use same obj instead of expensive delete & remake
# TODO: paper notes below

# NOTE: 30 pg NEAT paper, pg 11 line 3: node mutations have new > out = old weight, in > new = 1 (to minimise impact)
# probs should do something like this maybe  # completed

# NOTE2: pg 12 of NEAT paper for combining nets properly

# NOTE3: pg 13 for details of speciation

# NOTE4: pg 10, fig 3; make sure to record disjoint genes

# NOTE5: pg 13 footnotes may be useful

# LINK: http://nn.cs.utexas.edu/downloads/papers/stanley.ec02.pdf

# TODO: move population management to pop2, only allow I/O from external classes
# TODO: maybe reintroduce random asteroids with fitness as mean of attempts
