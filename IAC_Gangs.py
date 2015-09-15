g = open("ginfo.txt").read()
lines = g.splitlines()

cats = lines[0].split(' ')

dProbe_input = .2
ex_ia = .05
in_ia = .03
decay_rate = .05
resting_value = .1
m = -0.2
M = 1.0


class node():   # Will be the superclass of inode and pnode
    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.connected_enodes = []
        self.connected_inodes = []
        self.resting_value = resting_value
        self.probe_input=0
        self.input = 0
        self.effect = 0

    def update_act(self):
        eInput = 0
        for node in self.connected_enodes:
            eInput += node.effect
        iInput = 0
        for node in self.connected_inodes:
            iInput -= node.effect
        self.input = self.probe_input + (ex_ia*eInput) + (in_ia*iInput)
        if self.input > 0:
            self.effect = (M-self.effect)*self.input
        else:
            self.effect = (self.effect-m)*self.input
        self.effect -= decay_rate*(self.effect-resting_value)


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

llines = [x.split(' ') for x in lines]
dic = {}
for x in llines[1:]: #Builds dictionary out of inode objects
    dic[x[0]]=inode(x[0],cats[0])
for x in llines[1:]: #Adds to dictionary the pnode objects
    c= 1
    for y in x[1:]:
        dic[y]= pnode(y,cats[c])
        c+=1
for x in cats[1:]: #Connects the properties in the same category
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

class network():
    def __init__(self):
        self.previouslyActiveNode=None

    def probe(self, nodes):  # Specifies the node(s) to be probed
        for node in nodes:
            node.probe_input = .2

    def activate(self, epochs=200):  # Sends the activation through the network
        for x in range(0,epochs):
            for node in dic:
                dic[node].update_act()


net = network() # Create network object
net.probe([dic['Sharks']]) # Probe node(s)
net.activate(100) # Begin to update network | default epochs = 200
print(dic['Phil'].effect, dic['Rick'].effect, dic['Doug'].effect )