from createDomain import Domain as D
from quad import Quadrant as Q
from qtd import QuadTreeDecompositon as QTD
from qtd import InitialState as I
from a_star import astar as A
from qtd import FBSP
import numpy as np

d = D(1)
d.drawDomain()
state = I(d,decomposition = 'FBSP')
solution = A(state)
