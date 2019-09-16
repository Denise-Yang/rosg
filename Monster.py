#################################################################
# Monster Class
# Your Name:Denise Yang
# Your Andrew ID: denisey
# Your Section: C
#################################################################
import pygame
import math
import random

from Bar import Bar
'''
framework taken from 
https://github.com/LBPeraza/Pygame-Asteroids/blob/master/Asteroids/Ship.py
by LBPeraza

A* Algorithm logic from: http://theory.stanford.edu/~amitp/GameProgramming/AStarComparison.html

Guidelines for sprite animation here:
https://stackoverflow.com/questions/14044147/animated-sprite-from-few-images

Skull sprite:
https://pixel-poem.itch.io/dungeon-assetpuck

Ghost sprite:
https://opengameart.org/content/ghost-lvl1-2-3-60px
'''

from GameObject import GameObject
from Attack import Attack

class Monster(pygame.sprite.Sprite):            
            
    def __init__(self, x, y,r, grid, pLvl):
        self.x, self.y, self.r = x, y, r
        super(Monster, self).__init__()
        self.images = []
        self.index = 0
        self.initImages()
        self.image = self.images[self.index]
        self.sequence = 4
        self.grid = grid
        self.distance = 100
        self.path = []
        self.hp = 10 * int(math.sqrt(pLvl))
        self.hpBar = Bar(self.hp,(255,0,0), self.x, self.y - 10, 25, 5)
        self.nodes = self.getNodes()
        self.updateRect()
        self.maxStr = 2 * int(math.sqrt(pLvl))
        self.str = random.randint(0,self.maxStr)
        self.speed = 20
        
        
    def initImages(self):
        #initialize images
        self.images = []
        self.images.append(pygame.transform.scale(pygame.image.load('v2/skull_v2_1.png'), (20,20)))
        self.images.append(pygame.transform.scale(pygame.image.load('v2/skull_v2_2.png'), (20,20)))
        self.images.append(pygame.transform.scale(pygame.image.load('v2/skull_v2_3.png'), (20,20)))
        self.images.append(pygame.transform.scale(pygame.image.load('v2/skull_v2_4.png'), (20,20)))
        
    def updateRect(self):
        #updates rect
        r = self.r
        self.hpBar.updatePos(self.x, self.y-10)
        self.rect = pygame.Rect(self.x, self.y, r, r)
    
    def shift(self, isScroll, scrollX, scrollY, px,py):
        #side scrolls monsters
        self.updateRect()
        if isScroll[2] == True:
            self.x += self.r
            isScrolling = True
        elif isScroll[3] == True: 
            self.x -= self.r
            isScrolling = True

        elif isScroll[0] == True:
            self.y += self.r
            isScrolling = True

        elif isScroll[1] == True: 
            self.y -= self.r
            isScrolling = True
        else:
            isScrolling = False
        if isScrolling:
            self.updatePath(px,py, scrollX, scrollY)
        self.updateRect()


    def updatePath(self, px, py, scrollX, scrollY):
        #gets new path to player's current location
        start = (self.x - scrollX* self.r, self.y - scrollY*self.r)
        end = (px -scrollX*self.r,py - scrollY*self.r)
        self.path = []
        self.path = self.getPath(start, end)

    def update(self, pPos, scrollX, scrollY):
        #moves to next place on path
        self.index += 1
        self.image = self.images[self.index % self.sequence]
        self.updateRect()
        if self.getDis((self.x,self.y),(pPos[0],pPos[1])) >= self.distance:
            if self.path != None and len(self.path) != 0:
                nextPos = self.path.pop()
                self.x = nextPos[0] + scrollX * self.r
                self.y = nextPos[1] + scrollY * self.r 
        self.updateRect()

        


##pathfinding algorithm
    def getNodes(self):
        #get nodes of map
        grid = self.grid
        nodes = set()
        for row in range(len(grid)):
            for col in range(len(grid[row])):
                if grid[row][col][2] == 0:
                    nodes.add((row, col))
        return nodes
        
    
    def getNeighbors(self, curr):
        #get neighbors of current node
        x = curr[0]//self.r
        y = curr[1]//self.r
        dir  = [(x, y + 1),(x, y-1),(x + 1,y),(x - 1, y)]
        neighbors = []
        for i in range(len(dir)):
            if dir[i] in self.nodes:
                neighbors.append((dir[i][0]*self.r, dir[i][1]*self.r))
        return neighbors
    
    
    def getDis(self, curr, goal): 
        #get dis between nodes and estimating heuristic
        return ((curr[0]-goal[0])**2 + (curr[1]-goal[1])**2)**.5
    
    def getLowest(self, open,f):
        #return node w/ lowest fscore
        lowestScore = 10**10
        lowestNode = None
        for node in open:
            if f[node] < lowestScore:
                lowestScore = f[node]
                lowestNode = node
        return lowestNode
    
    
    def search(self, start,end):
        #search for path
        open = set()
        open.add((start))
        closed = set()
        curr = start
        f = {}
        g = {}
        cameFrom = {}
        g[start] = 0
        f[start] = g[start] + self.getDis(start,end)
        while len(open) != 0:
            curr = self.getLowest(open, f)
            open.remove(curr)
            closed.add(curr)
            if curr == end:
                return cameFrom
            for neigh in self.getNeighbors(curr):
                gCost = g[curr] + self.getDis(curr,neigh)
                if neigh in open and gCost <= g[neigh]:
                    open.remove(neigh)
                if neigh in closed and gCost< g[neigh]:
                    closed.remove(neigh)
                if neigh not in open and neigh not in closed:
                    g[neigh] = gCost
                    open.add(neigh)
                    f[neigh] = gCost + self.getDis(neigh, end)
                    cameFrom[neigh] = curr 
    
    def getPath(self, start, end):
        #compiles path
        path = []
        camefrom = {}
        cameFrom = self.search(start,end)
        path.append(end)
        if cameFrom != None:
            next = cameFrom.get(end)
            while next != start:
                path.append(next)
                next = cameFrom.get(next)
            path.append(start)
            return path
        
class Boss(Monster):
    #boss monster
    def __init__(self, x,y,r,grid, pLvl):
        super().__init__(x,y,r,grid, pLvl)
        self.image = []
        self.sequence = 2
        self.index = 0
        self.initImages()
        self.image = self.images[self.index]
        self.distance = 80
        self.hp = 100
        self.hpBar = Bar(self.hp,(255,0,0), self.x, self.y - 10, 25, 5)
        self.nodes = self.getNodes()
        self.updateRect()
        self.str = 10
   
    def initImages(self):
        #initialize boss monster images
        self.images.append(pygame.transform.scale(pygame.image.load('boss1.png'), (20,20)))        
        self.images.append(pygame.transform.scale(pygame.image.load('boss2.png'), (20,20)))
        
        
