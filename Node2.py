from random import random


class Node:
    def __init__(self, layer, nodenum, inputs=None):
        if inputs is None:
            inputs = []
        self.inputs = inputs  # self.inputs stored with [Node class, connection weight]
        self.layer = layer
        self.trigval = random() * 2 - 1  # required value to trigger node
        self.nodenum = nodenum  # TODO: setup the node innovation system
        self.main_input = None
        self.bias = 0  # TODO: add biases
        self.ticked = 0  # var to determine whether node has been calculated, avoids re-recursion
        self.tickedreturnval = 0  # once calculated, save to this

    def take_main_input(self, inp):  # call in net to take input
        self.tickedreturnval = inp
        self.ticked = 1

    def get_out(self, conw):
        # print('GetOut')
        if self.ticked == 1:
            return self.tickedreturnval  # completely skips over recalculation
        tval = 0
        for i in range(len(self.inputs)):
            if self.inputs[i][0].layer == 0:
                return self.inputs[i][0].tickedreturnval
            else:
                # print(f'Input Nodenum: {self.inputs[i][0].nodenum}, {self.inputs[i][0].layer}, {conw}')
                tval += self.inputs[i][0].get_out(self.inputs[i][1])
        if tval >= self.trigval + self.bias:  # eh probs wrong
            self.tickedreturnval = 1 * conw
            self.ticked = 1
            return 1 * conw
        else:
            self.tickedreturnval = 0
            self.ticked = 1
            return self.tickedreturnval

# TODO: check for multiple of same mutation
