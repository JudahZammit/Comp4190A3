import matplotlib.pyplot as plt
import numpy as np
import random
import copy


class Rectangle:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def CalculateOverlap(self, obs):
        #print('CalculateOverlap {0},{1}->{2},{3} with {4},{5}->{6},{7}'.format(self.x, self.y, self.x + self.width, self.y+self.height, obs.x, obs.y, obs.x + obs.width, obs.y + obs.height) )
        if (self.x < obs.x):
            min = self.x
        else:
            min = obs.x
        if ((self.x + self.width) < (obs.x + obs.width)):
            max = obs.x + obs.width
        else:
            max = self.x + self.width
        overlapX = (max - min) - (self.width + obs.width)
        #print('CalculateOverlap max', max, 'min', min, 'overlapX', overlapX)
        if (self.y < obs.y):
            min = self.y
        else:
            min = obs.y
        if ((self.y + self.height) < (obs.y + obs.height)):
            max = obs.y + obs.height
        else:
            max = self.y + self.height
        overlapY = (max - min) - (self.height + obs.height)
        #print('CalculateOverlap max', max, 'min', min, 'overlapY', overlapY)
        if (overlapX < 0) and (overlapY < 0):
            overlap = overlapX * overlapY
        else:
            overlap = 0.0
        #print('CalculateOverlap returns {0}'.format(overlap))
        return overlap


class Obstacle(Rectangle):
    def __init__(self, x, y, width, height, color=None):
        super().__init__(x, y, width, height)
        self.color = color
        if (color is not None):
            self.patch = plt.Rectangle(
                (self.x, self.y), self.width, self.height, facecolor=color, edgecolor='#202020')

    def inside(self,x,y):
        in_x = (x >= self.x and x <= (self.x+self.width))
        in_y = (y >= self.y and y <= (self.y+self.height))
        in_obs = in_x and in_y
        return in_obs 
    
    def getCoordinate(self):
        return (self.x, self.y)


class Domain:
    def __init__(self, onum):
        self.width = 100
        self.height = 100
        self.obstacles = self.CreateObstacles(onum)
        (self.ix, self.iy), (self.gx, self.gy) = self.CreateProblemInstance()
        self.map = None

    def getMap(self):
        if(self.map == None):
            self.map = {}
            for x in range(self.width):
                for y in range(self.height):
                    self.map[(x,y)] = True
                    for obs in self.obstacles:
                        if (obs.inside(x,y)):
                            self.map[(x,y)] = False
                            break

        return self.map

    def getInitial(self):
        return self.ix, self.iy

    def getGoal(self):
        return self.gx, self.gy

    # this method returns a list of obstacles(object type)
    # if you wanna access the obstacle:
    # obs.x obs.y obs.width obs.height (where obs is the obstacle)
    def getObstacels(self):
        return self.obstacles

    def CreateObstacles(self, onum):
        obstacles = []

        while(len(obstacles) < onum):
            x = int(random.uniform(0.0, self.width))
            y = int(random.uniform(0.0, self.height))
            w = int(random.uniform(10, 20))
            h = int(random.uniform(10, 20))
            if (x + w) > self.width:
                w = self.width - x
            if (y + h) > self.height:
                h = self.height - y
            obs = Obstacle(x, y, w, h, '#808080')
        # if you don't allow the obstacles to overlap, use the following
            found = False
            
            for o in obstacles:
                if (o.CalculateOverlap(obs) > 0.0):
                    found = True
                    break
            if (not found):
                obstacles = obstacles + [obs]
        # if you allow the obstacles to overlap, use the following
            # obstacles.append(obs)
        return obstacles

    # randomly choose a initial position and goal
    def CreateProblemInstance(self):
        found = False
        while (not found):
            ix = random.randint(0, self.width)
            iy = random.randint(0, self.height)

            oinitial = Obstacle(ix, iy, 0.1, 0.1)
            found = True
            for obs in self.obstacles:
                if (obs.inside(ix,iy)):
                    found = False
                    break

        found = False
        while (not found):
            gx = random.randint(0, self.width)
            gy = random.randint(0, self.height)

            ogoal = Obstacle(gx, gy, 0.1, 0.1)
            found = True
            for obs in self.obstacles:
                if (obs.inside(gx,gy)):
                    found = False
                    break
            if (oinitial.x == ogoal.x or oinitial.y == ogoal.y):
                found = False

        return((ix, iy), (gx, gy))

    def CheckOverlap(self, r):
        overlap = False
        for o in self.obstacles:
            if (r.CalculateOverlap(o) > 0):
                overlap = True
                break
        return overlap

    def CalculateCoverage(self, path, dim):
        x = np.arange(0.0, self.width, dim)
        y = np.arange(0.0, self.height, dim)
        counts = np.zeros((len(y), len(x)))
        for p in path:
            i = int(p[1] / dim)
            j = int(p[0] / dim)
            counts[j][i] = counts[j][i] + 1
        return (x, y, counts)

    # this method will draw your domain (with your final path)
    # you can pass a list of coordinates(tuples) as argument, the first tuple should be the initial coordinate
    # and the last one should be the goal
    # if argument is not specified, then it will draw the domain
    def drawDomain(self,nodes=None, path=None):
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1, aspect='equal')
        ax.set_xlim(0.0, self.width)
        ax.set_ylim(0.0, self.height)
        for o in self.obstacles:
            ax.add_patch(copy.copy(o.patch))
        ip = plt.Rectangle((self.ix, self.iy), .81, .81,
                           facecolor='#ff0000', label='initial')
        ax.add_patch(ip)
        g = plt.Rectangle((self.gx, self.gy), .81, .81,
                          facecolor='#00ff00', label='goal')
        ax.add_patch(g)

        if nodes is not None:
            for node in nodes:
                 plt.plot(node[0],node[1],'b.')

        if path is not None:
            x = [x for (x, y) in path]
            y = [y for (x, y) in path]
            plt.plot(x, y, label='path')
        ax.legend(bbox_to_anchor=(1.04, 1), loc="upper left")
        plt.show()


if __name__ == '__main__':
    # beware the x and y for an obstacle is the lower left vertex
    # how do you create a domain? see the following code! the number 20 means the number of obstacles is 20
    x = Domain(20)
    print(x.getObstacels()[0].x, x.getObstacels()[0].y)
    x.drawDomain(path=[(13, 24), (18, 45), (34, 57)])
