#################################################################
# Bar Class
# Your Name:Denise Yang
# Your Andrew ID: denisey
# Your Section: C
#################################################################


import pygame, sys



class Bar(object):
    def __init__(self, max, color, x, y, w, h, type =""):
        #initialize bar
        self.curr = max
        self.max = max
        self.type = type
        self.x, self.y, self.w, self.h = x, y, w, h
        self.color = color

    def increaseMax(self, newMax):
        #increases bar max
        self.max = newMax
        self.curr = newMax
    
    def draw(self, screen):
        #draws bar
        width = self.w * (self.curr/self.max)
        pygame.draw.rect(screen, self.color, [self.x, self.y, width, self.h])

    
    def affect(self, pts):
        #restores or damages bar
        self.curr += pts
        if self.curr > self.max:
            self.curr = self.max
        elif self.curr < 0:
            self.curr = 0

        
    def updatePos(self, x, y):
        #shifts bar
        self.x, self.y = x, y
        
        
        
#used to keep track of exp points
class Lvl(Bar):
    def __init__(self, max, color, x, y, w, h, lvl):
        #initialize level up bar
        super().__init__(max, color, x, y, w, h)
        self.curr = 0
        self.lvl = lvl
        self.lvlUp = False

        
    def affect(self,exp):
        #adds experience pts to lvl up bar
        self.curr += exp
        if self.curr >= self.max: 
            self.max = self.max * (1+self.lvl//3)
            self.lvlUp = True
        
        