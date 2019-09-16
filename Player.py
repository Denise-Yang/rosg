#################################################################
# Player Class
# Your Name:Denise Yang
# Your Andrew ID: denisey
# Your Section: C
#################################################################
'''
framework taken from 
https://github.com/LBPeraza/Pygame-Asteroids/blob/master/Asteroids/Ship.py
by LBPeraza

Sprite sheet:
http://pixelartmaker.com/art/20e1bc371d3ceaa

modified code for text display
https://stackoverflow.com/questions/20842801/how-to-display-text-in-pygame

'''

import pygame
from Bar import Lvl
from Bar import Bar
pygame.font.init()


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        
        pygame.sprite.Sprite.__init__(self)
        self.size  = 20
        super(Player, self).__init__()
        
        #initialize animation
        self.images = []
        self.images.append(pygame.transform.scale(pygame.image.load('playeranimation/playerF1.png'), (20,20)))
        self.images.append(pygame.transform.scale(pygame.image.load('playeranimation/playerF2.png'), (20,20)))
        self.images.append(pygame.transform.scale(pygame.image.load('playeranimation/playerF3.png'), (20,20)))
        self.images.append(pygame.transform.scale(pygame.image.load('playeranimation/playerF4.png'), (20,20)))
        self.images.append(pygame.transform.scale(pygame.image.load('playeranimation/playerB1.png'), (20,20)))
        self.images.append(pygame.transform.scale(pygame.image.load('playeranimation/playerB2.png'), (20,20)))
        self.images.append(pygame.transform.scale(pygame.image.load('playeranimation/playerB3.png'), (20,20)))
        self.images.append(pygame.transform.scale(pygame.image.load('playeranimation/playerB4.png'), (20,20)))
        self.images.append(pygame.transform.scale(pygame.image.load('playeranimation/playerL1.png'), (20,20)))
        self.images.append(pygame.transform.scale(pygame.image.load('playeranimation/playerL2.png'), (20,20)))
        self.images.append(pygame.transform.scale(pygame.image.load('playeranimation/playerL3.png'), (20,20)))
        self.images.append(pygame.transform.scale(pygame.image.load('playeranimation/playerL4.png'), (20,20)))
        self.images.append(pygame.transform.scale(pygame.image.load('playeranimation/playerR1.png'), (20,20)))
        self.images.append(pygame.transform.scale(pygame.image.load('playeranimation/playerR2.png'), (20,20)))
        self.images.append(pygame.transform.scale(pygame.image.load('playeranimation/playerR3.png'), (20,20)))
        self.images.append(pygame.transform.scale(pygame.image.load('playeranimation/playerR4.png'), (20,20)))
        self.index, self.dir = 0, 0
        self.image = self.images[self.index]
        self.seq = 4
        self.str = 10
        self.hp = 40
        self.x =  x
        self.y = y
        self.lvlNum = 1

        #initialize stats
        self.hpBar = Bar(self.hp,(255,0,0), 10, 630, 200, 20, "HP")
        self.lvlBar = Lvl(20, (0,255,0), 10, 675, 200, 10, self.lvlNum)
        self.myfont = pygame.font.SysFont(None, 20)
        self.lvlFont  = pygame.font.SysFont('Comic Sans MS', 15)
        self.hpFont = pygame.font.SysFont('Comic Sans MS', 25)
        self.lvlTxt = self.lvlFont.render ("lvl:"+ str(self.lvlNum), False,(255,255,255))
        self.hpTxt = self.hpFont.render ("HP", False,(255,255,255))
        self.speed = 20
        self.updateRect()
        
        
    def printStats(self):
        #print player hp, and strength
        print("Player stats:\n\tPOW: ", self.str, "\n\tHP:", self.hpBar.curr, "/", self.hpBar.max)
        
    def drawStats(self, screen):
        #draw stats on screen
        self.hpBar.draw(screen)
        self.lvlBar.draw(screen)
        screen.blit(self.hpTxt,(10,600))
        self.pow = self.myfont.render ("pow:" + str(self.str), False,(255,255,255))
        screen.blit(self.pow, (10,700))
        self.lvlTxt = self.lvlFont.render ("lvl:"+ str(self.lvlNum), False,(255,255,255))
        screen.blit(self.lvlTxt, (10,650))


    def boost(self, amount):
        #boost stats
        self.str += amount
    
        
    def updateRect(self):
        #updates player rect
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
        
    def moveOnScrn(self, move, w, h):
        #checks if the next move is on the screen
        return self.x + move[0] >= 0 and self.x + move[0] <= w and self.y + move[1] >= 0 and self.y + move[1] <= h 
        
    def makeMove(self, move, grid, w,h, scrollx, scrolly):
        #makes the next move
        if self.moveOnScrn(move,w,h):
            if grid[int((self.x + move[0])//self.size) - scrollx][int((self.y + move[1])//self.size) - scrolly][2] == 0:
                self.x = self.x + move[0]
                self.y = self.y + move[1]

    def update(self, keysDown, scrnW, scrnH, nodes, scrollX, scrollY, scrollDir, tic):
        self.image = self.images[self.index%self.seq + 4*self.dir]
        
        if self.lvlBar.lvlUp:
            #lvl up and boost stats
            self.lvlNum += 1
            self.hpBar.increaseMax(int(self.hp*1.2))
            self.str += self.lvlNum*2
            self.lvlBar.curr = 0
            self.lvlBar.lvlUp = False
        
        #movement control
        move = ()
        if keysDown(pygame.K_a):
            self.index += 1
            self.dir = 2
            if self.rect.left > 0:
                if not scrollDir[2]:
                    move = [-self.speed, 0]
                    self.makeMove(move, nodes, scrnW, scrnH,scrollX, scrollY)

        elif keysDown(pygame.K_d):
            self.index += 1

            self.dir = 3
            if self.rect.right < scrnW:
                 if not scrollDir[3]:
                    move = [self.speed, 0]
                    self.makeMove(move, nodes, scrnW, scrnH,scrollX, scrollY)

        elif keysDown(pygame.K_w):
            self.index += 1

            self.dir = 1
            if self.rect.top >= 0:
                if not scrollDir[0]:
                    move = [0, -self.speed]
                    self.makeMove(move, nodes, scrnW, scrnH,scrollX, scrollY)

        elif keysDown(pygame.K_s):
            self.index += 1

            self.dir = 0
            if self.rect.bottom < scrnH:
                if not scrollDir[1]:
                    move = [0, self.speed]
                    self.makeMove(move, nodes, scrnW, scrnH,scrollX, scrollY)
        else:
            self.index = 0
    
    
        self.updateRect()
        super(Player, self).update(scrnW, scrnH)


    

