#################################################################
# Main Game
# Your Name:Denise Yang
# Your Andrew ID: denisey
# Your Section: C
#################################################################
'''
Framework from:
https://github.com/LBPeraza/Pygame-Asteroids/blob/master/Asteroids/pygamegame.py 
created by Lukas Peraza

'''
import pygame, sys
from pygame.locals import *
pygame.font.init() 
import random
import math


from Map import Map
from Bar import Bar
from Bar import Lvl
from Player import Player
from Monster import Monster
from Monster import Boss
from Attack import Attack  
from Attack import SpAttack
from AttackScreen import AttackScreen
from Item import Item
from Item import Potion
from Item import Bag
                                  
                                  
                                  
                                  
class PygameGame(object):

    def init(self):
        self.gameStart, self.gameOver, self.showInstructions = False, False, False
        self.bgColor = (0,0,0)
        self.map = Map()
        self.grid = self.map.getGrid()
        self.menuSize = 200
        self.madeMove = False
        self.bossAppear = False
        self.bag  = Bag()
        self.size = 20
        self.scrn = AttackScreen(self.width//2 - 60 ,625)
        self.tic = 0
        self.win = False
        self.isScroll = [False,False,False,False] #if is scrolling in dirs [up,down, l, r]
        self.scrollX = 0
        self.scrollY = 0
        self.p = Player(self.width//2*20//20,self.height//2*20//20)
        self.b = None #initialize boss

        
        #initialize text
        self.myfont = pygame.font.SysFont(None, 60)
        self.subfont = pygame.font.SysFont(None, 20)        
        self.loseTxt =  self.myfont.render("Everyone is forever sad", False,(255,255,255))
        self.winTxt =  self.myfont.render("Now everyone's happy!", False,(255,255,255))
        self.restartTxt =  self.subfont.render("Press r to restart", False,(255,255,255))
        self.title = self.myfont.render("Realm of the Sad God", False,(255,255,255))
        self.subtitle = self.subfont.render("press enter to continue", False,(255,255,255))
        text = "Use WASD to move, and f to pick up items"
        text2 = "Swap any 2 orbs to make a match of 3"
        text3 = "Kill the boss to win the game, but don't touch any monsters"
        self.instructions = self.subfont.render(text, False,(255,255,255))
        self.instructions2 = self.subfont.render(text2, False,(255,255,255))
        self.instructions3 = self.subfont.render(text3, False,(255,255,255))

        #initialize groups
        self.play = pygame.sprite.GroupSingle(self.p)
        self.monsters = pygame.sprite.Group()
        self.items = pygame.sprite.Group()
        self.boss = pygame.sprite.GroupSingle()
        self.mAttacks = pygame.sprite.Group()
        self.pAttacks = pygame.sprite.Group()
        


    def mousePressed(self, x, y):
        #check if clicking the attack screen
        px, py, = self.p.x,self.p.y
        self.scrn.orbClicked(x,y,px,py)      
        if self.scrn.canAttk == True:
            self.madeMove = False
            self.pAttacks.add(self.createSpell(px,py,x,y,self.size, self.p.str, False))
            self.madeMove = True
        if self.madeMove == True:
            self.scrn.canAttk = False
        #check if bag is clicked
        self.bag.update(x,y, self.p)
        
    def mouseReleased(self, x, y):
        pass

    def mouseMotion(self, x, y):
        pass

    def mouseDrag(self, x, y):
        pass

    def keyPressed(self, keyCode, modifier):
        if self.isKeyPressed(pygame.K_i):
            #show player stats
            self.p.printStats()

       
        if self.isKeyPressed(pygame.K_PERIOD):
            #show instructions
            self.showInstructions = not self.showInstructions
            self.gameStart = True
            
        if self.isKeyPressed(pygame.K_RETURN):
            #start game
            self.gameStart = True
        
        if self.isKeyPressed(pygame.K_l):
            #buff stats and level for demo
            self.p.lvlNum = 10
            self.p.str = 100
            self.p.hpBar.max = 1000
            self.p.hpBar.curr = 1000


        
        if self.isKeyPressed(pygame.K_o):
            #creates boss
            x = random.randint(0,self.width//self.size*self.size)
            y = random.randint(0,self.height//self.size*self.size)
            self.b = Boss(x,y,self.size,self.grid, self.p.lvlNum)
            self.monsters.add(self.b)
            self.bossAppear = True

        
        if self.isKeyPressed(pygame.K_t):
            #add stick
            x = random.randint(0,self.width)//self.size*self.size
            y = random.randint(0,self.height- self.menuSize)//self.size*self.size
            self.items.add(Item(x, y))
            
        if self.isKeyPressed(pygame.K_y):
            #add potion
            x = random.randint(0,self.width)//self.size*self.size
            y = random.randint(0,self.height- self.menuSize)//self.size*self.size
            self.items.add(Potion(x, y))
        
        if self.isKeyPressed(pygame.K_f):
            #pick up items
            for item in self.items:
                if self.p.x == item.x and self.p.y == item.y:
                    self.bag.addItem(item)
                    if not self.bag.isFull:
                        item.onMap = False
            
        if self.isKeyPressed(pygame.K_r) and self.gameOver:
            print(True)
            #restart
            self.init()

        #Keypressed wasd controls player movement and scrolling
        if self.isKeyPressed(pygame.K_a):
            if self.p.x - self.p.speed < self.width/4 and self.map.rect.left != 0:
                if self.grid[(self.p.x//self.size) - self.scrollX - 1][int(self.p.y //self.size) - self.scrollY + 0][2] == 0:
                    self.scrollX += 1
                    self.isScroll[2] = True
                    
                        
        elif self.isKeyPressed(pygame.K_d):
            if self.p.x + self.p.speed > self.width * 3/4 and self.map.rect.right != self.width:
                if self.grid[(self.p.x//self.size) - self.scrollX + 1][int(self.p.y //self.size) - self.scrollY + 0][2] == 0:
                    self.scrollX -= 1
                    self.isScroll[3] = True
                    
     
        elif self.isKeyPressed(pygame.K_w):
            if self.p.y < self.height/4 and self.map.rect.top != 0:
                if self.grid[(self.p.x//self.size) - self.scrollX + 0][int(self.p.y //self.size) - self.scrollY - 1][2] == 0:
                    self.scrollY  += 1
                    self.isScroll[0] = True
                    

        elif self.isKeyPressed(pygame.K_s):
            if self.p.y > self.height//2 and self.map.rect.bottom != self.height - self.menuSize:
                if self.grid[(self.p.x//self.size) - self.scrollX + 0][int(self.p.y //self.size) - self.scrollY + 1][2] == 0:
                    self.scrollY -= 1
                    self.isScroll[1] = True
                    


    def keyReleased(self, keyCode, modifier):
        pass

    def timerFired(self, dt):  
    
        if self.gameStart and not self.showInstructions:
            if self.p.hpBar.curr == 0:
                self.gameOver = True
                self.win = False  
                
            if self.bossAppear:
                if self.b.hpBar.curr == 0:
                    self.gameOver = True
                    self.win = True
            self.tic += 1
            
            if self.p.lvlNum == 10 and not self.bossAppear:
                #generate boss at lvl 10
                x = random.randint(0,self.width//self.size*self.size)
                y = random.randint(0,self.height//self.size*self.size)
                self.b = Boss(x,y,self.size,self.grid,self.p.lvlNum)
                self.monsters.add(self.b)
                self.bossAppear = True
              
            #scrolls items and attacks
            for item in self.items:
                item.shift(self.isScroll, self.scrollX,self.scrollY, self.size)
            self.map.sideScroll(self.scrollX,self.scrollY)
            self.mAttacks.update(self.width, self.height - self.menuSize, self.grid, self.size, self.scrollX, self.scrollY)
            self.pAttacks.update(self.width, self.height - self.menuSize, self.grid, self.size, self.scrollX, self.scrollY)
        
            #update player and monsters
            if self.tic%5 == 0:
                self.play.update(self.isKeyPressed,self.width, self.height- self.menuSize, self.grid, self.scrollX,  self.scrollY, self.isScroll, self.tic)
            for monster in self.monsters:
                monster.shift(self.isScroll, self.scrollX, self.scrollY, self.p.x, self.p.y)
            self.isScroll = [False,False,False,False]
            if self.tic%10 ==0:
                self.monsters.update((self.p.x,self.p.y), self.scrollX, self.scrollY)
                self.boss.update((self.p.x,self.p.y), self.scrollX, self.scrollY)
    
    
            if self.tic%50 == 0:
                if len(self.monsters) <= 1:
                    # generates monsters every couple of seconds
                    x = random.randint(0,self.width)//self.size*self.size
                    y = random.randint(0,self.height- self.menuSize)//self.size*self.size
                    monster = Monster(x,y, self.size, self.grid, self.p.lvlNum)
                    self.monsters.add(monster)   
                    
                for monster in self.monsters:
                    #updates monster's path
                    monster.updatePath(self.p.x,self.p.y, self.scrollX, self.scrollY)
            for monster in self.monsters:
                #checks if monster died/give exp pts/item drops
                if monster.y == self.p.y and monster.x == self.p.x:
                    monster.kill()
                    self.p.hpBar.curr = 0
                if monster.hpBar.curr == 0:
                    self.p.lvlBar.affect(10)
                    createItem = random.randint(0,6)
                    if createItem > 3:
                        self.items.add(Item(monster.x, monster.y))
                    if createItem < 2:
                        self.items.add(Potion(monster.x, monster.y))
                    monster.kill()
    
            if self.tic%100 == 0: 
            #detecting attack collisions/ deal damage               
                if len(self.monsters) > 0:
                    for m in self.monsters:
                        if type(m) == Boss:
                            attk = self.createSpell(m.x,m.y, self.p.x,self.p.y, m.r, m.str, True)
                        else:
                            attk = self.createSpell(m.x,m.y, self.p.x,self.p.y, m.r, m.str, False)
                        self.mAttacks.add(attk)
            
            pAttkLanded = pygame.sprite.groupcollide(self.monsters,self.pAttacks, False, True)
            mAttkLanded = pygame.sprite.groupcollide(self.mAttacks,self.play, True, False)
            for attk in mAttkLanded:
                if type(attk) == SpAttack:
                    y = random.randint(0,len(self.scrn.orbScrn) - 1)
                    x = random.randint(0,len(self.scrn.orbScrn[y]) - 1)
                    self.scrn.orbScrn[x][y][4] = 1 
                self.p.hpBar.affect(-1*attk.pow)
            for mon in pAttkLanded:
                mon.hpBar.affect(-self.p.str)
            self.scrn.removeMatches()
                
                

    def createSpell(self,sx,sy,endx,endy, size, power, isSpAttk):
        #shoots spell in certain direction
        if endx-sx != 0:
            angle = math.atan((endy-sy)/(endx-sx))
        elif endy > sy:
            angle = math.pi/2
        else:
            angle = -math.pi/2
        if endx < sx:
            angle -= math.pi
        if isSpAttk:
            attk = SpAttack(sx + size//2,sy + size//2, angle, power)
        else:
            attk = Attack(sx + size//2,sy + size//2, angle, power)
        return attk
        
        

    def redrawAll(self, screen):
        #draw start screen
        if not self.gameStart:
            screen.blit(self.title,(self.width * 1/8,(self.height-self.menuSize) * 1/2))
            screen.blit(self.subtitle,(self.width* 1/4,self.height * 5/12))
        #draw instructions
        if self.showInstructions:
            screen.blit(self.instructions,(10,self.height * 1/4))
            screen.blit(self.instructions2,(10,self.height * 3/8))
            screen.blit(self.instructions3,(10,self.height * 1/2))

        #draw gameplay
        elif self.gameStart and not self.gameOver:
            self.map.drawMap(screen, self.scrollX, self.scrollY)
            self.play.draw(screen)
            self.boss.draw(screen)
            self.mAttacks.draw(screen)
            self.pAttacks.draw(screen)
            for item in self.items:
                if item.onMap:
                    screen.blit(item.image, (item.x,item.y))
            for m in self.monsters:
                m.hpBar.draw(screen)
            self.monsters.draw(screen)
            
            pygame.draw.rect(screen, (0,0,0), [0,600,self.width,200])
            self.bag.drawBag(screen)
            self.p.drawStats(screen)
            self.scrn.drawScrn(self.p.x, self.p.y, screen)
        #draw endscreen
        if self.gameOver:
            if self.win:
                screen.blit(self.winTxt,(self.width * 1/8,(self.height-self.menuSize) * 1/2))

            else:
                screen.blit(self.loseTxt,(self.width * 1/8,(self.height-self.menuSize) * 1/2))
            screen.blit(self.restartTxt,(self.width* 1/4,self.height * 1/2))
            
            
        

    def isKeyPressed(self, key):
        ''' return whether a specific key is being held '''
        return self._keys.get(key, False)

    def __init__(self, width=600, height = 800, fps=50, title="Realm of The Sad God"):
        self.width = width
        self.height = height
        self.fps = fps
        self.title = title
        self.bgColor = (255, 255, 255)
        pygame.init()


    def run(self):

        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((self.width, self.height))
        # set the title of the window
        pygame.display.set_caption(self.title)

        # stores all the keys currently being held down
        self._keys = dict()

        # call game-specific initialization
        self.init()
        playing = True
        while playing:
            time = clock.tick(self.fps)
            self.timerFired(time)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.mousePressed(*(event.pos))
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.mouseReleased(*(event.pos))
                elif (event.type == pygame.MOUSEMOTION and
                      event.buttons == (0, 0, 0)):
                    self.mouseMotion(*(event.pos))
                elif (event.type == pygame.MOUSEMOTION and
                      event.buttons[0] == 1):
                    self.mouseDrag(*(event.pos))
                elif event.type == pygame.KEYDOWN:
                    self._keys[event.key] = True
                    self.keyPressed(event.key, event.mod)
                elif event.type == pygame.KEYUP:
                    self._keys[event.key] = False
                    self.keyReleased(event.key, event.mod)
                elif event.type == pygame.QUIT:
                    playing = False
            screen.fill(self.bgColor)
            self.redrawAll(screen)
            pygame.display.flip()

        pygame.quit()


def main():
    game = PygameGame()
    game.run()

if __name__ == '__main__':
    main()
