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

    def update_act(self):
        eInput = 0
        for node in self.connected_enodes:
            eInput += node.effect
        iInput = 0
        for node in self.connected_inodes:
            iInput += node.effect
        self.input = self.probe_input + (node.ex_ia*eInput) - (node.in_ia*iInput)

        if self.input > 0:
            self.effect = (node.M-self.effect)*self.input
        elif self.input < 0:
            self.effect = (self.effect-node.m)*self.input
        self.effect -= node.decay_rate*(self.effect-node.resting_value)


class inode(node):

    def connect(self, *other):
        for x in other:
            self.connected_pnodes.append(x)


class pnode(node):

    def connect(self, *other):
        for x in other:
            if isinstance(x, inode):
                self.connected_enodes.append(x)
            elif isinstance(x, pnode):
                self.connected_inodes.append(x)


class build():  # Used to create the nodal structure
    g = open("ginfo.txt").read()
    lines = g.splitlines()
    cats = lines[0].split(' ')

    def compose(self): # Is run on a build object to create the dictionary containing the nodes and their connective information

        llines = [x.split(' ') for x in build.lines]
        dic = {}
        for x in llines[1:]: #Builds dictionary out of inode objects
            dic[x[0]]=inode(x[0],build.cats[0])
        for x in llines[1:]: #Adds to dictionary the pnode objects
            c= 1
            for y in x[1:]:
                dic[y]= pnode(y,build.cats[c])
                c+=1
        for x in build.cats[1:]: #Connects the properties in the same category
            samecatlist=[]
            for y in dic:
                if dic[y].category==x:
                    samecatlist.append(dic[y])
            for y in dic:
                if dic[y].category==x:
                    dic[y].connect(*samecatlist)
        for x in llines[1:]: #Connects the inodes to their respective pnodes
            l = [dic[y] for y in x[1:]]
            dic[x[0]].connected_enodes = dic[x[0]].connected_enodes + l
        for x in dic:  # Connects pnodes to their respective inodes
            if isinstance(dic[x],inode):
                for y in dic[x].connected_enodes:
                    y.connected_enodes.append(dic[x])

        inodelist = []

        for x in dic:   # Connects instances to the other instances
            if isinstance(dic[x], inode):
                inodelist.append(dic[x])
        for x in dic:
            if isinstance(dic[x], inode):
                dic[x].connected_inodes = inodelist

        for x in dic:   # Removes pnodes from their respective inode and enode lists
            if type(dic[x]) == pnode:
                dic[x].connected_inodes.remove(dic[x])
            f = []
            if type(dic[x]) == inode:
                for y in dic:
                    if type(dic[y]) == inode:
                        if dic[x] != dic[y]:
                            f.append(dic[y])
                dic[x].connected_inodes = f
        self.dic=dic


class network():

    def __init__(self, dic):
        self.dic = dic

    def probe(self, *strnodes):  # Specifies the node(s) to be probed
        for strnode in strnodes:
            self.dic[strnode].probe_input = .2

    def activate(self, epochs=200):  # Sends the activation through the network
        for x in range(0,epochs):
            for node in self.dic:
                self.dic[node].update_act()

    def check(self, *strnodes):  # Takes arguments as strings of instances or properties and outputs their respective effects
        s = ''
        for strnode in strnodes:
            effect = self.dic[strnode].effect
            binding = '{0}: {1} \n'.format(strnode,effect)
            s = s + binding
        print(s)