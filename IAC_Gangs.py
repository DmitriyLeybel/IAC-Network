g = open("ginfo.txt").read()
lines = g.splitlines()

cats = lines[0].split(' ')

probe_input = .2
ex_ia = .05
in_ia = .03
decay_rate = .05
resting_value = .1
class inode():
    def __init__(self,name,category):
        self.name = name
        self.category = category
        self.connected_pnodes = []
        self.resting_value = resting_value
    def connect(self,*other):
        for x in other:
            self.connected_pnodes.append(other)

class pnode():

    def __init__(self,name,category):
        self.name = name
        self.category = category
        self.connected_pnodes = []
        self.connected_inodes = []
        self.resting_value = resting_value

    def connect(self, *other):
        for x in other:
            if isinstance(other, inode):
                self.connected_inodes.append(x)
            else:
                self.connected_pnodes.append(x)

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
            dic[y].connect(samecatlist)
for x in llines[1:]: #Connects the inodes to their respective pnodes
    l = [dic[y] for y in x[1:]]
    dic[x[0]].connected_pnodes = dic[x[0]].connected_pnodes + l
