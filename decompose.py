from quad import Quadrant as Q
from sklearn.tree import DecisionTreeClassifier
import numpy as np
from sklearn.tree import _tree

def QuadTreeDecompositon(quadrant):
    full_quads = []
    empty_quads = []
    impure_quads = [quadrant]

    new_impure_quads = []
    while len(impure_quads) > 0:
        for q in impure_quads:
            q_children = q.decompose()
            for q_child in q_children:
                if q_child.getPurity() == 0:
                    empty_quads.append(q_child)
                elif q_child.getPurity() == -1:
                    full_quads.append(q_child)
                else:
                    new_impure_quads.append(q_child)

        impure_quads = new_impure_quads
        new_impure_quads = []

    return full_quads, empty_quads

def FBSP(map_):
    labels = np.array(list(map_.values())).astype('int')
    features = np.array(list(map_.keys()))
    clf = DecisionTreeClassifier(
            criterion = 'entropy')
    clf.fit(features,labels)

    n_nodes = clf.tree_.node_count

    children_left = clf.tree_.children_left

    children_right = clf.tree_.children_right

    feature = clf.tree_.feature

    threshold = clf.tree_.threshold


    def find_path(node_numb, path, x):

        path.append(node_numb)

        if node_numb == x:
            return True

        left = False

        right = False

        if (children_left[node_numb] !=-1):

            left = find_path(children_left[node_numb], path, x)

        if (children_right[node_numb] !=-1):

            right = find_path(children_right[node_numb], path, x)

        if left or right :

            return True

        path.remove(node_numb)

        return False

    def get_rule(path, column_names):

        mask ={'x':0,'y':0,'width':100,'height':100}

        for index, node in enumerate(path):

            #We check if we are not in the leaf
            if index!=len(path)-1:

                # Do we go under or over the threshold ?

                if (children_left[node] == path[index+1]):

                    if(column_names[feature[node]] == 'x'):
                        mask['width'] = min(threshold[node],mask['width'])
                    if(column_names[feature[node]] == 'y'):
                        mask['height'] = min(threshold[node],mask['height'])

                else:

                    if(column_names[feature[node]] == 'x'):
                        mask['x'] = max(threshold[node],mask['x'])
                    if(column_names[feature[node]] == 'y'):
                        mask['y'] = max(threshold[node],mask['y'])

        mask['height'] = mask['height'] -mask['y']
        mask['width'] = mask['width'] -mask['x']
        return mask

    # Leaves

    features = np.array(list(map_.keys()))

    leave_id = clf.apply(features)

    paths ={}

    for leaf in np.unique(leave_id):

        path_leaf = []

        find_path(0, path_leaf, leaf)

        paths[leaf] = np.unique(np.sort(path_leaf))

    rules = {}

    for key in paths:

        rules[key] = get_rule(paths[key], ['x','y'])


    full = []
    emp = []
    for rule in list(rules.values()):
        empty = clf.predict([[rule['x'] + rule['width']/2
            ,rule['y'] + rule['height']/2]]).squeeze()

        quad = Q(rule['x'],rule['y'],rule['width']
                ,rule['height'],map_)
        if empty == 1:
            emp.append(quad)
        elif empty == 0:
            full.append(quad)

    return full,emp


class InitialState:
    def __init__(self,domain,decomposition = 'QTD'):
        q = Q(0,0,domain.width,domain.height,domain.getMap())
        if decomposition == 'QTD':
            full,emp = QuadTreeDecompositon(q)
        if decomposition == 'FBSP':
            full,emp = FBSP(domain.getMap())
        

        self.ix = domain.ix
        self.iy = domain.iy
        self.gx = domain.gx
        self.gy = domain.gy

        self.nodes = self.buildNodes(full,emp)
        self.edges = self.buildEdges(emp)

    #Finds the the middle point of the boundrey
    #between two neighboring quadrants
    def buildNodes(self,full_quads,empty_quads):
        nodes = []
        for q1 in empty_quads:
            # Find the neighboring quads
            all_ = empty_quads.copy()
            all_.extend(full_quads.copy())
             
            neighbors = []
            for q2 in all_:
                right = (q1.x + q1.width) == q2.x
                left = q1.x == (q2.x + q2.width)
                up = (q1.y + q1.height) == q2.y
                down = q1.y == (q2.y + q2.height)
                
                y_bottom_point = max(q1.y,q2.y)
                y_top_point = min(q1.y + q1.height,q2.y + q2.height)
                y_overlap = y_top_point - y_bottom_point
                y_mid_point = (y_overlap // 2) + y_bottom_point

                x_bottom_point = max(q1.x,q2.x)
                x_top_point = min(q1.x + q1.width,q2.x + q2.width)
                x_overlap = x_top_point - x_bottom_point
                x_mid_point = (x_overlap // 2) + x_bottom_point

                if right and y_overlap > 0:
                    nodes.append((q2.x,y_mid_point))
                
                if left and y_overlap > 0:
                    nodes.append((q1.x,y_mid_point))
                
                if up and x_overlap > 0:
                    nodes.append((x_mid_point,q2.y))
                
                if down and x_overlap > 0:
                    nodes.append((x_mid_point,q1.y))

            #remove duplicates
            nodes = list(set(nodes))

        return nodes

    def buildEdges(self,empty_quads):
        edges = []
        set_ = []
        for quad in empty_quads:
            set_ = []
            nodes = self.nodes.copy()
            nodes.extend([(self.ix,self.iy),(self.gx,self.gy)])
            for node in nodes:
                inX = (node[0] >= quad.x) and (node[0] <= quad.x + quad.width)
                inY = (node[1] >= quad.y) and (node[1] <= quad.y + quad.height)
                 
                if inX and inY:
                    set_.append(node)
            
            for node in set_:
                set_copy = set_.copy()
                set_copy.remove(node)
                for other_node in set_copy:
                    edges.append((node,other_node))
        
        edges_dict = {}
        nodes = self.nodes.copy()
        nodes.extend([(self.ix,self.iy),(self.gx,self.gy)])
        for node in nodes:
            neighbors = []
            for edge in edges:
                if node == edge[0]:
                    neighbors.append(edge[1])
            edges_dict[node] = neighbors

        return edges_dict
