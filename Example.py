from IAC_Gangs import *

com = build() # Builds an object to contain the nodes and their respective features
com.compose() # Composes the proper nodal properties and connections
net = network(com.dic) # Creates a network object which can be probed, and activations, spread
net.probe('Jets') # String argument as the property or instance to be probed
net.update() # Spreads the activation in the network for a select number of epochs
net.check('Jets','20', 'JH', 'sing.', 'pusher') # Checks the final values of the desired nodes

