from createDomain import Domain as D
from quad import Quadrant as Q
from decompose import QuadTreeDecompositon as QTD
from decompose import InitialState as I
from a_star import astar as A
from decompose import FBSP
import numpy as np
from timeit import timeit
from operator import add

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
    if(path == None):
        raise Exception("No solution")
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

def getAvgStats(times = 10,num_obs = 20,size = 20):
    qtd_stats = [0,0,0,0,0]
    fbsp_stats= [0,0,0,0,0]
    
    k = 0
    while k < times:
        d = D(num_obs,size)
        try:
            qtd_stats = list(map(add, qtd_stats, 
                stats(d,'QTD',verbose = False)))
            fbsp_stats = list(map(add, fbsp_stats, 
                stats(d,'FBSP',verbose = False)))
        except:
            continue

        k = k + 1
    for i in range(len(qtd_stats)):
        qtd_stats[i] = qtd_stats[i]/times
        fbsp_stats[i] = fbsp_stats[i]/times
    print('Average QTD Stats With '+str(num_obs)+' Obstacles and Obstacle Size '+ str(size)+ ' :')
    print('Average Partition Time: '+ str(qtd_stats[0]))
    print('Average Search Time: ' + str(qtd_stats[1]))
    print('Average Total Time: '+str(qtd_stats[2]))
    print('Average Total Number of Nodes: ' + str(qtd_stats[3]))
    print('Average Number of Nodes in Path: ' + str(qtd_stats[4]))
    print()

    print('Average FBSP Stats With '+str(num_obs)+' Obstacle and Obstacle Size '+ str(size)+ ' :')
    print('Average Partition Time: '+ str(fbsp_stats[0]))
    print('Average Search Time: ' + str(fbsp_stats[1]))
    print('Average Total Time: '+str(fbsp_stats[2]))
    print('Average Total Number of Nodes: ' + str(fbsp_stats[3]))
    print('Average Number of Nodes in Path: ' + str(fbsp_stats[4]))
    print()

def demo(num_obs = 20,size = 20):
        d = D(num_obs,size)
        d.drawDomain()

        qtd_state = I(d,decomposition = 'QTD')
        qtd_path = A(qtd_state)
        
        d.drawDomain(path = qtd_path,nodes = qtd_state.nodes)
        d.drawDomain(path = qtd_path)
        
        fbsp_state = I(d,decomposition = 'FBSP')
        fbsp_path = A(fbsp_state)
        
        d.drawDomain(path = fbsp_path,nodes = fbsp_state.nodes)
        d.drawDomain(path = fbsp_path)

def investigate(num_obs,size):
    print('_________________________________________________________')
    getAvgStats(times = 10, num_obs = num_obs,size = size)
    print('Demo With '+str(num_obs)+' Obstacles and Obstacle Size '+ str(size)+ ' :')
    demo(num_obs = num_obs,size = size)


if __name__ == '__main__':
    test_domains = [(10,20),
                    (10,50),
                    (20,20),
                    (20,50),
                    (30,20),
                    (40,20)]
    for domain in test_domains:
        investigate(domain[0],domain[1])
