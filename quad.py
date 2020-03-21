class Quadrant:
    def __init__(self,x,y,width,height,map):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.map = map

        self.purity = None
        self.center = None

    def getPurity(self):
        if(self.purity == None):
            self.purity = 0
            for x in range(self.x,self.width + self.x):
                for y in range(self.y,self.height + self.y):
                    if not self.map[(x,y)]:
                        self.purity = self.purity + 1
            # if every coordinate is obstructed then
            # purity in -1. 
            if(self.purity == self.height * self.width):
                self.purity = -1

        return self.purity

    def getCenter(self):
        if(self.center  == None):
            self.center = (self.x +  (self.width //2), self.y + (self.height//2))
        return self.center

    def decompose(self):
        newWidth1 = self.width // 2
        newWidth2 = self.width - newWidth1

        newHeight1 = self.height // 2
        newHeight2 = self.height - newHeight1
        
        Q1 = Quadrant(self.x,self.y,newWidth1,newHeight1,self.map)
        Q2 = Quadrant(self.x,self.y + newHeight1,newWidth1,newHeight2,self.map)
        Q3 = Quadrant(self.x + newWidth1,self.y,newWidth2,newHeight1,self.map)
        Q4 = Quadrant(self.x + newWidth1,self.y + newHeight1,newWidth2,newHeight2,self.map)

        return Q1,Q2,Q3,Q4

