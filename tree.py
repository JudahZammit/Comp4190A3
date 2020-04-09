from createDomain import Domain as D
from quad import Quadrant as Q
from qtd import QuadTreeDecompositon as QTD
from qtd import InitialState as I
from a_star import astar as A
from qtd import FBSP
import numpy as np
from timeit import timeit

d = D(40)
print('hello')

def qtd():
    state = I(d,decomposition = 'QTD')
    path = A(state)
    return state, path
qtd_state ,qtd_path = qtd()
print("qtd time: "+str(timeit(qtd,number = 1)))

def fbsp():
    state = I(d,decomposition = 'FBSP')
    path = A(state)
    return state,path
fbsp_state, fbsp_path = fbsp()
print("fbsp time: "+str(timeit(fbsp,number = 1)))

d.drawDomain()

d.drawDomain(path = qtd_path,nodes = qtd_state.nodes)
d.drawDomain(path = qtd_path)

d.drawDomain(path = fbsp_path,nodes = fbsp_state.nodes)
d.drawDomain(path = fbsp_path)

# add partitioning time
# add search time
# total time
# add num total nodes
# add num nodes in path
