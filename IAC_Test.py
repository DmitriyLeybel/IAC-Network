from IAC_Gangs import *

x = pnode('dude','stuff')
y = pnode('what', 'otherstuff')
x.connect(y)
print(x.connected_pnodes)