class node():   # Will be the superclass of inode and pnode

    ex_ia = .05
    in_ia = .03
    decay_rate = .05
    m = -0.2
    M = 1.0
    resting_value = .1

    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.connected_enodes = []
        self.connected_inodes = []
        self.resting_value = node.resting_value
        self.probe_input=0
        self.input = 0
        self.effect = 0
        self.buffered_effect = 0

    def update_act(self):
        self.effect=0
        self.input=0
        eInput = 0

        for node in self.connected_enodes:
            eInput += node.buffered_effect

        iInput = 0

        for node in self.connected_inodes:
            iInput += node.buffered_effect

        self.input = self.probe_input + (node.ex_ia*eInput) - (node.in_ia*iInput)

        # if self.name == 'node0':  ####DEBUGING
        #    print('eInput:{0} || iInput: {1}'.format(eInput,iInput))
        if self.input > 0:
            self.effect = (node.M-self.effect)*self.input

        elif self.input <= 0:
            self.effect = (self.effect-node.m)*self.input
        # if self.name == 'node0':  ####DEBUGING
        #    print(self.effect)
        self.effect -= node.decay_rate*(self.effect-node.resting_value)


class inode(node):

    pass


class pnode(node):

    pass


class build():  # Used to create the nodal structure
    g = open("ginfo.txt").read()
    lines = g.splitlines()
    cats = lines[0].split(' ')

    def compose(self): # Is run on a build object to create the dictionary containing the nodes and their connective information

        llines = [x.split(' ') for x in build.lines]
        dic = {}
        for x in llines[1:]:    # Builds property nodes and adds them to dictionary
            for y in range(len(build.cats)):
                dic[x[y]] = pnode(x[y],build.cats[y])

        for x,y in zip(llines[1:],range(len(llines)-1)):    # Builds instance nodes, connects them to property nodes
            dic['node{0}'.format(y)] = inode('node{0}'.format(y),'node')
            for a in range(len(build.cats)):
                dic['node{0}'.format(y)].connected_enodes.append(dic[x[a]])
                dic[x[a]].connected_enodes.append(dic['node{0}'.format(y)]) # Also populates connected_enodes of property nodes

        ilist = []
        for x in dic:   # Populates the connected_inodes of the instance nodes
            if dic[x].category == 'node':
                ilist.append(dic[x])
        for x in dic:
            if dic[x].category == 'node':
                for y in ilist:
                    if dic[x].name != y.name:
                        dic[x].connected_inodes.append(y)


        for x in dic:    # Populates property nodes' connected_inodes
            if dic[x].category in build.cats:
                for y in dic:
                    if dic[y].category == dic[x].category and dic[x] != dic[y]:
                        dic[x].connected_inodes.append(dic[y])

        self.dic = dic


class network():

    def __init__(self, dic):
        self.dic = dic

    def probe(self, *strnodes):  # Specifies the node(s) to be probed
        for strnode in strnodes:
            self.dic[strnode].probe_input = .2
            self.dic[strnode].buffered_effect = .2

    def update(self, iterations=200, debug=0, dname=''):  # Sends the activation through the network
        for x in range(0,iterations):
            for node in self.dic:
                self.dic[node].update_act()
                if debug == 1:
                    if self.dic[node].name == dname:
                        print(self.dic[node].effect)
            for node in self.dic:
                self.dic[node].buffered_effect = self.dic[node].effect

    def check(self, *strnodes):  # Takes arguments as strings of instances or properties and outputs their respective effects
        s = ''
        for strnode in strnodes:
            effect = self.dic[strnode].effect
            binding = '{0}: {1} \n'.format(strnode,effect)
            s = s + binding
        print(s)