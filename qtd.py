from quad import Quadrant as Q

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


class InitialState:
    def __init__(self,domain,decomposition = 'QTD'):
        q = Q(0,0,domain.width,domain.height,domain.getMap())
        if decomposition == 'QTD':
            full,emp = QuadTreeDecompositon(q)
        
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
