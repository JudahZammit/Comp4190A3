from qtd import InitialState as I
import math
import bisect

class Node():
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

    def euc_dist(self,other):
        return math.sqrt((self.position[0] - other.position[0])**2
                + (self.position[1] - other.position[1])**2)
    def __lt__(self,other):
        return self.f < other.f

def astar(state):
    start = (state.ix,state.iy)
    end = (state.gx,state.gy)
    neighbor_lookup_table = state.edges
    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Add the start node
    open_list.append(start_node)

    # Loop until you find the end
    while len(open_list) > 0:

        # Pop current off open list, add to closed list
        current_node = open_list.pop(0)
        closed_list.append(current_node)

        # Found the goal
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1] # Return reversed path

        # Generate children
        children = []
        for new_position in neighbor_lookup_table[current_node.position]:

            # Create new node
            new_node = Node(current_node, new_position)

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:

            # Child is on the closed list
            if child in closed_list:
                continue

            # Create the f, g, and h values
            child.g = current_node.g + current_node.euc_dist(child)
            
            # redundent calculation
            child.h = end_node.euc_dist(child)
            
            child.f = child.g + child.h

            # Child is already in the open list
            if child in open_list:
                index = open_list.index(child)
                if child > open_list[index]:
                    continue
                else:
                    open_list.remove(child)

            # Add   the child to the open list
            # using an orderd insert
            bisect.insort(open_list,child)
