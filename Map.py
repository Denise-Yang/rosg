#################################################################
# Map Generator
# Your Name:Denise Yang
# Your Andrew ID: denisey
# Your Section: C
#################################################################

import pygame
import random

'''
map tiles pulled from here
https://www.dotoji.com/two-dungeon-wall-tilesets-opengameartorg-0f2c89e787005c05.html
'''

class Map(object):
    def __init__(self, w = 1000):
        #initialize map
        self.w = w
        self.nodeNum = 50
        self.wall = pygame.transform.scale(pygame.image.load('wall.png'), (20,20))
        self.floor = pygame.transform.scale(pygame.image.load('floor2.png'), (20,20))
        self.size = w//self.nodeNum
        self.grid = []
        self.longBlk = False
        count = 0
        self.rect = pygame.Rect(0,0,self.w,self.w)
        for i in range(self.nodeNum):
            self.grid += [[""]*self.nodeNum]    
            
        #randomly creates obstacles
        for i in range(self.nodeNum):
            for j in range(self.nodeNum):
                isObstacle = random.randint(0,20)
                if self.longBlk == True:
                    self.grid[i][j] = [i,j,1]
                    count += 1
                if count > 1:
                    count = 0
                    self.longBlk = False
                if isObstacle == 1:
                    self.grid[i][j] = [i,j,1] 
                    
                elif isObstacle == 7:
                    self.grid[i][j] = [i,j,1]
                    self.longBlk = True
                    
                else:
                    self.grid[i][j] = [i,j,0] 

    def getGrid(self):
        #returns grid
        return self.grid
    
    def drawMap(self, screen, scrollX, scrollY):
        #draws map
        for row in self.grid:
            for block in row:
                if block[2] == 1:
                    image = self.wall
                else:
                    image = self.floor             
                screen.blit(image, ((block[0] + scrollX)*self.size, (block[1] + scrollY)*self.size))
                
    def sideScroll(self, scrollX, scrollY):
        #scrolls map
        self.rect = pygame.Rect(scrollX*self.size,scrollY*self.size,self.w,self.w)
            
                