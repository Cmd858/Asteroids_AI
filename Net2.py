from Node2 import Node
from random import randint, random
from pygame import draw


class Net:
    def __init__(self, innum, outnum, basepop, a=0, b=0, c=0, d=0, e=0, f=0):
        # depreciated for now
        # self.popobj = popobj  # brings in the population object to allow transfer of innovation numbers
        self.base = basepop  # inherited class to interact with innov functions
        self.net = [[], []]  # current net: [input nodes (index 0), output nodes (index -1 to allow expansion)]
        self.colour = (0, 0, 0)  # used exclusively in drawnet
        self.innum = innum  # number of input nodes, must be equal to num of maininputs or something will go wrong
        self.outnum = outnum  # num of output nodes
        self.nodecount = innum + outnum  # total current nodes in the system, used for innovs I think
        self.innovs = []  # stores innovs in this net for easy access
        for i in range(innum):  # add all required inputs
            self.net[0].append([Node(0, i), random() * 2 - 1])
        for i in range(outnum):  # add all required outputs
            self.net[-1].append([Node(-1, i + len(self.net[0])), random() * 2 - 1])  # use -1 to allow for dynamic size

    def mutate(self):  # add var to create minimum mutations, prevent going though with no change
        # self.base.add_innov('mate')
        innovs = self.base.get_innovs()  # get innov from base class (Pop2)
        if randint(0, 1) == 0:  # connection input, arbitrary randint values, change later to represent config settings
            index1 = randint(1, len(self.net) - 1)  # exclude input layer by starting from 1
            index2 = randint(0, len(self.net[index1]) - 1)
            connode1 = self.net[index1][index2]  # select the right connection node (output)
            index3 = randint(0, index1 - 1)  # probably useful somewhere
            index4 = randint(0, len(self.net[index3]) - 1)  # oh right, selects nodes by getting random pos
            connode2 = self.net[index3][index4]  # select second node (input)
            if not (connode2[0].nodenum, connode1[0].nodenum) in self.innovs:
                connode1[0].inputs.append(connode2)  # append node object to inputs
                self.base.add_innov((connode2[0].nodenum, connode1[0].nodenum))  # create connection between nodes
                self.innovs.append((connode2[0].nodenum, connode1[0].nodenum))  # adds innov value to pop and local
            # self.popobj.add_innov((connode2, connode1))  # should show in > out
        # Node Addition Mutation
        if randint(0, 1) == 0:  # node mutation
            # figure out way way to add more than one layer but not too many
            gotlayer = False
            layer = randint(0, len(self.net) - 1)
            # layer = len(self.net) - 1
            # while not gotlayer:  # recurse back through possibilities
            #    if randint(0, 1) != 0:  # 1/4 chance to fail
            #        gotlayer = True
            #    else:
            #        layer -= 1  # maybe add var for hard cap to stop infinite expansion
            if len(self.net) >= 7:
                layer -= 1  # attempt to hard cap
            if layer > 0:  # 1 bc this node needs to have an input
                nodeindex = randint(0, len(self.net[layer]) - 1)  # get index of output node used (second index)
                if len(self.net[layer][nodeindex][0].inputs) > 1:  # bc cant have randrange of len 1
                    inpindex = randint(0, len(self.net[layer][nodeindex][0].inputs) - 1)  # get index of input
                else:
                    inpindex = 0
                if len(self.net[layer][nodeindex][0].inputs) > 0:  # make sure there is possible node to connect to
                    targetnode = self.net[layer][nodeindex][0].inputs[inpindex]  # get input node object
                    newnode = [Node(layer, self.nodecount, [targetnode]), 1]  # create new node object to intersect I/O
                    self.net[layer][nodeindex][0].inputs.pop(inpindex)  # pops output node's obsolete input
                    if layer - targetnode[0].layer > 1:  # check to see if there is a gap layer between connections
                        self.net[layer - 1].append(newnode)  # appends node in gap layer to left of output node
                    else:
                        if len(self.net) < 10:
                            self.net.insert(layer, [newnode])  # if no gap layer, creates one here
                            layer += 1
                            for i in range(len(self.net[layer])):
                                self.net[layer][i][0].layer += 1  # adjusts layer var in base
                        else:
                            return  # prevents net growing too large
                    # if len(self.net[layer][nodeindex][0].inputs) > 0:
                    self.net[layer][nodeindex][0].inputs.append(newnode)  # appends new input to net's vars
                    inmid = (targetnode[0].nodenum, newnode[0].nodenum)  # get tuple of connection intersection
                    midout = (newnode[0].nodenum, self.net[layer][nodeindex][0].nodenum)  # mess but works
                    self.base.add_innov(inmid)  # (in > new)
                    self.base.add_innov(midout)  # (new > out)
                    self.innovs.append(inmid)
                    self.innovs.append(midout)  # intersects new node in-between existing connection
                    self.nodecount += 1
                    self.correct_layers()  # make sure all layer vars are correct
                    # else:
                    #   print('hmm probs shouldnt happen')
        if randint(0, 1) == 0:  # weight mutation
            pass  # work in progress, to be added later
        if randint(0, 1) == 0:  # bias mutation
            pass
            # TODO: add innovs appends in node mutation
            # TODO: add bias and weight mutation

    def run_net(self, inputs):  # inputs are program maininputs, this func run from func reference from Pop2 (probs)
        if len(inputs) != len(self.net[0]):
            raise ValueError('Number of inputs values does not match input node number')
        outputs = []
        for i in range(len(self.net[0])):
            self.net[0][i][0].take_main_input(inputs[i])
        self.untick_nodes()  # make sure all nodes recalculate with new inputs
        for i in range(len(self.net[-1])):  # iterate through all output nodes
            outputs.append(0)
            for j in range(len(self.net[-1][i][0].inputs)):  # for each of the node's inputs, get outputs (can recur)
                # print(f'{len(self.net)} {self.net}')
                outputs[-1] += self.net[-1][i][0].get_out(self.net[-1][i][0].inputs[j][1])  # invalid arg (maybe)
        return outputs  # return completed output to list

    def untick_nodes(self):  # force recalculation because of new value inputs
        for i in range(len(self.net)):
            for j in range(len(self.net[i])):  # iter through all nodes in each layer
                self.net[i][j][0].ticked = 0

    def getlayers(self):  # temp func to detect faults
        for i in range(len(self.net)):
            for j in range(len(self.net[i])):  # tbh not really sure why this is here
                pass
                # print(self.net[i][j][0].nodenum, self.net[i][j][0].layer, i)

    def draw_net(self, screen, x, y, xbuf, ybuf, r):  # func for visual representation of connections
        # xbuf == buffer space between nodes on x axis
        # x, y for top left because nets needs room to expand
        # print('drawnet')
        width = len(self.net)
        maxh = 0
        for i in self.net:
            if maxh < len(i):
                maxh = len(i)  # get max node height
        for i in range(len(self.net)):  # iter through: layers, nodes in layer, inputs in node (i, j, k)
            # print(f'len {i}: {len(self.net[i])}')
            for j in range(len(self.net[i])):  # should probs rename loop vars but cba
                x1 = x - xbuf * (width - i)  # calculate location of node
                y1 = y + ybuf * (j + (maxh - len(self.net[i])) / 2)
                draw.circle(screen, (255, 255, 255), (x1, y1), r)
                for k in range(len(self.net[i][j][0].inputs)):  # iterate through all nodes to draw inputs
                    # print(i, j, k)
                    # print(self.net)
                    # out = self.net[-i][j]
                    inp = self.net[i][j][0].inputs[k][0]
                    x2 = x - xbuf * (width - inp.layer)  # complicated calcs for positions
                    # print(self.net[i][j][0].inputs[k])
                    y2 = y + ybuf * (self.net[inp.layer].index(self.net[i][j][0].inputs[k]) + (
                                maxh - len(self.net[inp.layer])) / 2)
                    # gets pos of list
                    if self.net[i][j][0].inputs[k][1] >= 0:
                        self.colour = (220, 0, 0)  # set colour and draw net connections
                        draw.line(screen, self.colour, (x1, y1), (x2, y2), int(self.net[i][j][0].inputs[k][1] * 3))
                    if self.net[i][j][0].inputs[k][1] < 0:
                        self.colour = (0, 0, 220)
                        draw.line(screen, self.colour, (x1, y1), (x2, y2), int(self.net[i][j][0].inputs[k][1] * -3))
                        # *-3 because lines can't have negative width
                    # ofset on y axis to center on middle, not top

    def correct_layers(self):
        for i in range(len(self.net)):  # iterate through each net layer
            for j in range(len(self.net[i])):  # iterate through each node in layer i
                self.net[i][j][0].layer = i  # to fix for new layer creation

# TODO: Pop2 controlled innov nums
# TODO: prevent duplicate connections
