#################################################################
# Attack Screen
# Your Name:Denise Yang
# Your Andrew ID: denisey
# Your Section: C
#################################################################


import pygame
import random

class AttackScreen(object):
    def __init__(self, x,y, width=150, height=150): 
        self.w = width
        self.h = height
        self.x, self.y = x,y
        self.rowNum = 5
        self.colNum = 5
        self.canAttk = False
        self.r = (self.h//self.rowNum)//2
        self.orbColors = [(68,150,255),(92,62,183),(0,255,150),(255,25,25),(189,255,58)]
        self.swapLst = []
        #generates orbs on attk scrn
        self.orbScrn = []
        for row in range(self.rowNum):
            self.orbScrn += [[1]*self.colNum]
        for row in range(self.rowNum):
            for col in range(self.colNum):
                self.orbScrn [row][col] = [self.r + col* self.w//self.colNum, self.r + row* self.h//self.rowNum, random.choice(self.orbColors), False, 0]
                
    
    #draws the attack screen and orbs
    def drawScrn(self, x, y, screen):
        swapOrbs = []
        # pygame.draw.rect(screen, (150, 150, 255), (self.x, self.y, self.w, self.h))
        for orbRow in self.orbScrn:
            for orb in orbRow:
                if orb[3]:
                    r = self.r//2
                else:
                    r = self.r
                pygame.draw.circle(screen, orb[2], (self.x + orb[0],self.y + orb[1]),r, orb[4])
            
    #checks if orbs are clicked and swaps them
    def orbClicked(self, x, y, px, py):
        #check if orb is clicked
        for row in range(len(self.orbScrn)):
            for col in range(len(self.orbScrn[row])):
                orb = self.orbScrn[row][col]
                if x < orb[0] + self.x + self.r and x > orb[0] + self.x - self.r and y < orb[1] + self.y + self.r and y > orb[1] + self.y - self.r:
                    orb[3] = True 
                    #if two orbs are clicked then swap colors
                    #store index and orb
                    if orb[4] != 1:
                        self.swapLst.append([orb, row, col])
                        if len(self.swapLst) == 2:
                            self.swap()
                            if not self.isValid():
                                self.swap()
                            self.swapLst = []
                    
    #swaps the colors of two orbs
    def swap(self):
        orb1, orb2 = self.swapLst[0][0],self.swapLst[1][0]
        storeColor = orb1[2]
        orb1[2] = orb2[2]
        orb2[2]= storeColor
        orb1[3], orb2[3] = False, False


    #checks if swap is valid
    def isValid(self):
        for orb in self.swapLst:
            color = orb[0][2]
            row = orb[1]
            col = orb[2]
            dir = [[0,1],[0,-1],[1,0],[-1,0]]
            for d in dir:
                if self.moveOnScrn(row + d[1],col + d[0]) and self.orbScrn[row + d[1]][col + d[0]][2] == color:
                    if self.moveOnScrn(row  - d[1], col - d[0]) and  self.orbScrn[row  - d[1]][col - d[0]][2] == color:
                        return True
                        
                    elif self.moveOnScrn(row + 2*d[1],col + 2*d[0]) and self.orbScrn[row + 2*d[1]][col + 2*d[0]][2] == color:
                        return True
        return False

    #checks if index is in orb scrn
    def moveOnScrn(self, row, col):
        return row < self.rowNum and row  >= 0 and col < self.colNum and col >= 0
    
    #get index in orbScrn of coordinate
    def getInd(self,n):
        return (n-self.r)//self.r//2
        
    #checks for three in a row
    def checkMatches(self, checkVert, limCheck, toRemove):
        matchCount = 0
        tentative = []
        #set variables to check whether horizontal or vert
        if checkVert == True:
            horiLim, vertLim = 0, limCheck
            num, vert, hori = self.rowNum, 1, 0
        else:
            horiLim, vertLim = limCheck, 0
            num, vert, hori = self.colNum, 0, 1
        
        #check for matches in specified direction
        for row in range(len(self.orbScrn) - vertLim):
            for col in range(len(self.orbScrn[row]) - horiLim):
                color = self.orbScrn[row][col][2]                
                tentative.append(self.orbScrn[row][col])
                for i in range(1, num):
                    if self.moveOnScrn(row + i*vert,col + i*hori):
                        if color == self.orbScrn[row + i*vert][col + i*hori][2]:
                            tentative.append(self.orbScrn[row + i*vert][col + i*hori])
                            matchCount += 1
                        else:
                            if matchCount < 2:
                                tentative = [] 
                            break
                for orb in tentative:
                    if orb not in toRemove:
                        toRemove.append(orb)
                if matchCount >= 2:
                    self.canAttk = True
                matchCount = 0
                tentative = []
        return toRemove
                    
    #wrapper function for above Color
    def replaceOrbs(self, toRemove):
        while len(toRemove) != 0:
            orb = toRemove.pop(0)
            x = self.getInd(orb[0])
            y = self.getInd(orb[1])
            self.aboveColor(x, y)
                
    #uses recursion to shift orbs down 
    def aboveColor(self, x,y):
        if not self.moveOnScrn(x,y - 1):
            self.orbScrn[y][x][2] = random.choice(self.orbColors)
        else:
            self.orbScrn[y][x][2] = self.orbScrn[y - 1][x][2]
            self.aboveColor(x,y - 1)
            
    #remove matches and slides orbs down
    def removeMatches(self):
        toRemoveHori = []
        toRemoveVert = []
        limCheck = 2
        #check vertical 3 in a row
        toRemoveVert = self.checkMatches(True, limCheck, toRemoveVert)
        #checks horizontal 3 in a rows
        toRemoveHori =  self.checkMatches(False, limCheck, toRemoveHori)
        for orb in toRemoveVert:
            if orb in toRemoveHori:
                toRemoveHori.remove(orb)
        self.replaceOrbs(toRemoveVert)
        self.replaceOrbs(toRemoveHori)
