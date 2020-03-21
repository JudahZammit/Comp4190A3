import createDomain as cd
import math
import numpy as np


class Node(cd.Obstacle):
    # parent is a node
    # tup is a tuple
    def __init__(self, tup, parent=None):
        super().__init__(tup[0], tup[1], 0.001, 0.001)
        self.parent = parent

    def getParent(self):
        return self.parent

    def setParent(self, parent):
        self.parent = parent

    # L2 distance
    def distance(self, node):
        return np.linalg.norm(np.asarray(self.getCoordinate()) - np.asarray(node.getCoordinate()))


class Tree:
    def __init__(self, root):
        self.root = root
        self.nodes = [root]  # this list keeps all the nodes in the tree

    # traget is a node, this method will return the nearest node in the tree to the target
    def findNearestNode(self, target):
        distances = {node: target.distance(node) for node in self.nodes}
        return min(distances, key=distances.get)

    # add a node into the tree
    def addNode(self, node):
        self.nodes.append(node)
