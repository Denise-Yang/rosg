#################################################################
# Item Class
# Your Name:Denise Yang
# Your Andrew ID: denisey
# Your Section: C
#################################################################

'''
Stick sprite:
https://forums.terraria.org/index.php?threads/a-few-summoner-additions.47449/

Potion sprite:
https://www.kisspng.com/png-pixel-art-art-pixel-coloring-by-number-sandbox-pix-2037835/
'''
import pygame, sys
import random
pygame.font.init()


class Item(pygame.sprite.Sprite):
    def __init__(self,x,y):
        size = 20
        self.x, self.y = x, y
        super(Item, self).__init__()
        self.type = "stick"
        self.inUse = False
        self.trashed = False
        self.image = pygame.transform.scale(pygame.image.load('stick.png').convert_alpha(),(size, size))
        self.rect = pygame.Rect(self.x, self.y, size, size)
        self.onMap = True
        self.boost = random.randint(0,20)
   
    def use(self, p):
        #use item
        if not self.inUse:
            p.boost(self.boost)
            self.inUse = True

    def trash(self,p):
        #trash item
        if self.inUse and not self.trashed:
            p.boost(-self.boost)
        self.trashed = True
            
    def shift(self, isScroll, scrollX, scrollY, size): 
        #shift item on screen       
        if isScroll[2] == True:
            self.x += size
        elif isScroll[3] == True: 
            self.x -= size
        elif isScroll[0] == True:
            self.y += size
        elif isScroll[1] == True: 
            self.y -= size


    
class Potion(Item):
    def __init__(self,x,y):
        size = 10
        super().__init__(x,y)
        self.type = "potion"    
        self.heal = random.randint(10,30)
        self.image = pygame.transform.scale(pygame.image.load('potion.png').convert_alpha(),(20, 20))
        
    def use(self, p):
        #heal player
        p.hpBar.curr += self.boost
        if p.hpBar.curr > p.hpBar.max:
            p.hpBar.curr  = p.hpBar.max


class Bag(object):
    def __init__(self):
        #initialize bag objects
        self.storage = []
        self.maxItems = 2
        self.items = [[425,625,50,50],[425,700,50,50]]
        self.useButtons = [[500,625,60,25],[500,700,60,25]]
        self.trashButtons = [[500,660,60,25],[500,735,60,25]]

        self.color = (50,50,50)
        self.offSet = 5
        self.isFull = False

        self.myfont = pygame.font.SysFont('Comic Sans MS', 20)
        self.bagFull = self.myfont.render("Your bag is full", False,(255,255,255))
        self.trashTxt = self.myfont.render("Trash", False,(255,255,255))
        self.useTxt = self.myfont.render("Use", False,(255,255,255))

        
    def checkClick(self, mx, my, button):
        #check if button
        return mx >= button[0] and mx <= button[0] + button[2] and my >= button[1] and my <= button[1] + button[3] 
    
    def addItem(self, item): 
        #adds item to bag
        if len(self.storage) > 1:
            self.isFull = True
        else:
            self.storage.append(item)
                
    #sees if you clicked use or trash item
    def update(self, mx, my, p):
        self.isFull = False
        if len(self.storage) > 0:
            for i in range(len(self.storage)):
                if self.checkClick(mx, my, self.useButtons[i]):
                    self.storage[i].use(p)
                    if isinstance(self.storage[i], Potion):
                        self.storage.remove(self.storage[i])
            for i in range(len(self.storage)):
                if self.checkClick(mx, my, self.trashButtons[i]):
                    self.storage[i].trash(p)
                    self.storage.remove(self.storage[i])
                    
    
    def drawBag(self,screen):
        if self.isFull:
            screen.blit(self.bagFull, (10,725))
        
        #draw bag buttons
        for i in range(self.maxItems):
            pygame.draw.rect(screen,self.color, self.items[i])            
            pygame.draw.rect(screen,self.color, self.trashButtons[i])
            pygame.draw.rect(screen,self.color, self.useButtons[i])
            screen.blit(self.trashTxt, (self.trashButtons[i][0], self.trashButtons[i][1]))
            screen.blit(self.useTxt, (self.useButtons[i][0] + self.offSet, self.useButtons[i][1]))

        #draws items in bag
        for i in range(len(self.storage)):
            if isinstance(self.storage[i], Item):
                screen.blit(pygame.transform.scale(self.storage[i].image,(self.items[i][2] - self.offSet,self.items[i][3] - self.offSet)), (self.items[i][0]+ self.offSet, self.items[i][1]+ self.offSet))
            


            
    
    
        