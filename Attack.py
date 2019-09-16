#################################################################
# Attack Class
# Your Name:Denise Yang
# Your Andrew ID: denisey
# Your Section: C
#################################################################
'''
Attack.py
framework from https://github.com/LBPeraza/Pygame-Asteroids/blob/master/Asteroids/Bullet.py
Lukas Peraza, 2015 for 15-112 Pygame Lecture
'''
from GameObject import GameObject
import pygame
import math
class Attack(GameObject):
    speed = 10
    time = 50  
    size = 10
    def __init__(self, x, y, angle, power):
        #initialize attack stats
        self.pow = power
        size = 10
        image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        pygame.draw.circle(image, (150, 150, 255), (size // 2, size // 2), size // 2)
        super(Attack, self).__init__(x, y, image, size // 2)
        vx = Attack.speed * math.sin((angle + math.pi/2))
        vy = -Attack.speed * math.cos((angle+ math.pi/2))
        self.velocity = vx, vy
        self.timeOnScreen = 0
        

    def update(self, screenWidth, screenHeight,grid, nodeSize, scrollX, scrollY):
        #updates position of attack
        #kills attack after some time
        super(Attack, self).update(screenWidth, screenHeight)
        self.timeOnScreen += 1
        if self.timeOnScreen > Attack.time or self.rect.right > screenWidth or self.rect.right < 0 or self.rect.top >= screenHeight or self.rect.bottom < 0:
            self.kill()
        elif grid[int(self.x//nodeSize) - scrollX][int(self.y//nodeSize) - scrollY][2] == 1:
            self.kill()      

class SpAttack(Attack):
    #creates a special attack
    def __init__(self, x, y, angle, power):
        super().__init__( x, y, angle, power)
        image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)

        pygame.draw.circle(image, (175, 150, 200), (self.size // 2, self.size // 2), self.size // 2)
