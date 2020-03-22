import Structure
import createDomain
import matplotlib.pyplot as plt
import copy
import random
import numpy as np
import matplotlib.collections as mc
import time


class solver:
    def __init__(self, problem, step=1, threshold=1):
        self.problem = problem
        self.root = Structure.Node(problem.getInitial())
        self.goal = Structure.Node(problem.getGoal())
        # a tree asscociated with the problem
        self.tree = Structure.Tree(self.root)
        self.threshold = threshold  # this control the bias
        self.step = step  # step size
        self.limit = 10000  # maximum nodes generated

    # draw the problem with a given path
    def visualize(self, path=None):
        self.problem.drawDomain(path)

    # this method solves the problem using rrt
    # if it can't solve within the limit then return NoNE
    # it will also plot the graph
    def solve(self):
        q_new = self.root
        q_goal = self.goal
        count = 0
        start_time = time.time()
        while count <= self.limit:
            q_target = self.randomNode(0.1)
            q_nearest = self.tree.findNearestNode(q_target)
            q_new = self.extend(q_nearest, q_target, self.step)
            if q_new is not None:
                print(q_new.getCoordinate())
                q_new.setParent(q_nearest)
                self.tree.addNode(q_new)
                if q_new.distance(q_goal) < self.threshold:
                    q_goal.setParent(q_new)
                    self.tree.addNode(self.root)
                    break
            count += 1
        if count is self.limit:
            return None
        else:
            # self.drawTree()
            path = self.traceBack(q_new)
            path.append(self.goal)

            print('the runtime is: {} s'.format(time.time() - start_time))
            if path is not None:
                print('the solver solved the problem!')
            print('Number of nodes in the path:{}'.format(len(path)))
            print('Number of total nodes in the random tree:{}'.format(
                len(self.tree.nodes)))
            self.finalVisualize([obs.getCoordinate() for obs in path])
            return path

    # generate a random node that does not overlap with obstacles
    # with some bias choose the goal directly
    def randomNode(self, probability):
        if random.random() < probability:
            return self.goal
        found = False
        while found is False:
            coord = (100 * random.random(), 100 * random.random())
            node = Structure.Node(coord)
            if not self.problem.CheckOverlap(node):
                found = True
                return node
        return None

    # given a random node find the nearest node in the tree and try to extend it
    # if it can't do that, then return None
    def extend(self, nearest, target, step):
        if nearest.distance(target) > step:
            (x1, y1), (x2, y2) = nearest.getCoordinate(), target.getCoordinate()
            if x1 == x2:
                coord = (x1, y1 + step * (y2 - y1) / abs(y1 - y2))
            else:
                vec = np.asarray((x2 - x1, y2 - y1))
                normalized = vec / np.linalg.norm(vec)
                difference = normalized * step
                coord = tuple(np.asarray((x1, y1)) + difference)
            node = Structure.Node(coord)
        else:
            node = target
        if not self.problem.CheckOverlap(node):
            return node
        else:
            return None

    # given a node, this method will find all its ancestors
    def traceBack(self, kid):
        result = []
        temp = kid
        limit = 100000
        count = 0

        while temp is not None:
            # print('d3123123')
            result.insert(0, temp)
            if count > limit:
                break
            count += 1
            temp = temp.getParent()
        # print(result)
        return result

    # visualize the tree asscociated with the problem
    def drawTree(self):
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1, aspect='equal')
        ax.set_xlim(0.0, self.problem.width)
        ax.set_ylim(0.0, self.problem.height)
        for o in self.problem.obstacles:
            ax.add_patch(copy.copy(o.patch))
        ip = plt.Rectangle(self.root.getCoordinate(), .81, .81,
                           facecolor='#ff0000', label='initial')
        ax.add_patch(ip)
        g = plt.Rectangle(self.goal.getCoordinate(), .81, .81,
                          facecolor='#00ff00', label='goal')
        ax.add_patch(g)
        collections = []
        for node in self.tree.nodes:
            if node.parent is not None:
                z = [node.getCoordinate(), node.parent.getCoordinate()]
                collections.append(z)
        lc = mc.LineCollection(collections, colors='b', linewidths=0.8)
        ax.add_collection(lc)
        ax.legend(bbox_to_anchor=(1.04, 1), loc="upper left")
        plt.show()

    # this method will draw a path and a tree after solving the problem
    def finalVisualize(self, path):
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1, aspect='equal')
        ax.set_xlim(0.0, self.problem.width)
        ax.set_ylim(0.0, self.problem.height)
        for o in self.problem.obstacles:
            ax.add_patch(copy.copy(o.patch))
        ip = plt.Rectangle(self.root.getCoordinate(), .81, .81,
                           facecolor='#ff0000', label='initial')
        ax.add_patch(ip)
        g = plt.Rectangle(self.goal.getCoordinate(), .81, .81,
                          facecolor='#00ff00', label='goal')
        ax.add_patch(g)
        collections = []
        for node in self.tree.nodes:
            if node.parent is not None:
                z = [node.getCoordinate(), node.parent.getCoordinate()]
                collections.append(z)
        lc = mc.LineCollection(collections, colors='b',
                               linewidths=0.8, label='tree')
        ax.add_collection(lc)
        if path is not None:
            x = [x for (x, y) in path]
            y = [y for (x, y) in path]
            plt.plot(x, y, label='path', color='r')
        ax.legend(bbox_to_anchor=(1.04, 1), loc="upper left")
        plt.show()


if __name__ == '__main__':
    # you can change the number (i.e. 50) to control the number of obstacles
    domain = createDomain.Domain(30)
    solver1 = solver(domain)
    path = solver1.solve()
