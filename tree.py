from createDomain import Domain as D
from quad import Quadrant as Q
from qtd import QuadTreeDecompositon as QTD
from qtd import InitialState as I
from a_star import astar as A
from qtd import FBSP
import numpy as np

d = D(20)
d.drawDomain()
state = I(d,decomposition = 'FBSP')
path = A(state)
d.drawDomain(path = path,nodes = state.nodes)
d.drawDomain(path = path)
