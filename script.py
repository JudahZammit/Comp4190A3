from createDomain import Domain as D
from quad import Quadrant as Q
from qtd import QuadTreeDecompositon as QTD
from qtd import InitialState as I

d = D(0)
d.drawDomain()
state = I(d)
d.drawDomain(nodes = state.nodes)

