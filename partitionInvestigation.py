from createDomain import Domain as D
from quad import Quadrant as Q
from qtd import QuadTreeDecompositon as QTD
from qtd import InitialState as I
from a_star import astar as A
from qtd import FBSP
import numpy as np
from timeit import timeit
from operator import add

d = D(20)

def wrapper(func, *args, **kwargs):
    def wrapped():
        return func(*args, **kwargs)
    return wrapped

def stats(domain,decomp,verbose = True):
    state = I(domain,decomposition = decomp)
    state_time = timeit(wrapper(I,domain,decomp),number = 1)
    num_nodes = len(state.nodes)

    path = A(state)
    path_time = timeit(wrapper(A,state),number = 1)
    num_nodes_in_path = len(path)

    total_time = state_time + path_time
    if verbose:
        print(decomp + 'Stats:')
        print('Partition Time: '+ str(state_time))
        print('Search Time: ' + str(path_time))
        print('Total Time: '+str(total_time))
        print('Total Number of Nodes: ' + str(num_nodes))
        print('Number of Nodes in Path: ' + str(num_nodes_in_path))
        print()
    return [state_time, path_time, total_time,
            num_nodes,num_nodes_in_path]

def getAvgStats(times = 10,num_obs = 20):
    qtd_stats = [0,0,0,0,0]
    fbsp_stats= [0,0,0,0,0]
    
    for _ in range(times):
        d = D(num_obs)
        qtd_stats = list(map(add, qtd_stats, 
            stats(d,'QTD',verbose = False)))
        fbsp_stats = list(map(add, fbsp_stats, 
            stats(d,'FBSP',verbose = False)))
   
    for i in range(len(qtd_stats)):
        qtd_stats[i] = qtd_stats[i]/times
        fbsp_stats[i] = fbsp_stats[i]/times
    print('Average QTD Stats With '+str(num_obs)+' Obsticles:')
    print('Average Partition Time: '+ str(qtd_stats[0]))
    print('Average Search Time: ' + str(qtd_stats[1]))
    print('Average Total Time: '+str(qtd_stats[2]))
    print('Average Total Number of Nodes: ' + str(qtd_stats[3]))
    print('Average Number of Nodes in Path: ' + str(qtd_stats[4]))
    print()

    print('Average FBSP Stats With '+str(num_obs)+' Obsticles:')
    print('Average Partition Time: '+ str(fbsp_stats[0]))
    print('Average Search Time: ' + str(fbsp_stats[1]))
    print('Average Total Time: '+str(fbsp_stats[2]))
    print('Average Total Number of Nodes: ' + str(fbsp_stats[3]))
    print('Average Number of Nodes in Path: ' + str(fbsp_stats[4]))
    print()


getAvgStats(times = 10)
