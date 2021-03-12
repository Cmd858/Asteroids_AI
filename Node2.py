from random import random


class Node:
    def __init__(self, layer, nodenum, inputs=None):
        if inputs is None:
            inputs = []
        self.inputs = inputs  # self.inputs stored with [Node class, connection weight]
        self.layer = layer  # layer of network
        self.trigval = random() * 2 - 1  # required value to trigger node
        self.nodenum = nodenum  # TODO: setup the node innovation system
        self.main_input = None
        self.bias = 0  # TODO: add biases
        self.ticked = 0  # var to determine whether node has been calculated, avoids re-recursion
        self.tickedreturnval = 0  # once calculated, save to this

    def take_main_input(self, inp):  # call in net to take input
        self.tickedreturnval = inp  # take input for layer 0
        self.ticked = 1  # mark as calculated

    def get_out(self, conw):  # recursive function
        # print('GetOut')
        if self.ticked == 1:  # check for calculated
            return self.tickedreturnval  # completely skips over recalculation
        tval = 0  # triggerval, the amount of input required to activate the next node
        for i in range(len(self.inputs)):  # stop recursion at input layer
            if self.inputs[i][0].layer == 0:
                return self.inputs[i][0].tickedreturnval  # returns main input gotten from program
            else:
                # print(f'Input Nodenum: {self.inputs[i][0].nodenum}, {self.inputs[i][0].layer}, {conw}')
                tval += self.inputs[i][0].get_out(self.inputs[i][1])  # adds up values of all input node connection
        if tval >= self.trigval + self.bias:  # eh probs wrong
            self.tickedreturnval = 1 * conw  # multiply by connection weight
            self.ticked = 1  # marks the connection as calculated, preventing recalculation
            return self.tickedreturnval  # returns relevant value
        else:
            self.tickedreturnval = 0  # less that activation value, so returns 0
            self.ticked = 1  # marks as calculated
            return self.tickedreturnval

# TODO: check for multiple of same mutation, could screw with recalculation
