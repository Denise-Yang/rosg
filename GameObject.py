'''
Taken from:
https://github.com/LBPeraza/Pygame-Asteroids/blob/master/Asteroids/GameObject.py
GameObject.py
implements the base GameObject class
Lukas Peraza, 2015 for 15-112 Pygame Lecture
'''
import pygame

from Map import Map 

class GameObject(pygame.sprite.Sprite):
    def __init__(self, x, y, image, radius):
        super(GameObject, self).__init__()
        # x, y define the center of the object
        self.x, self.y, self.image, self.radius = x, y, image, radius
        self.baseImage = image.copy()  # non-rotated version of image
        w, h = image.get_size()
        self.updateRect()


    def updateRect(self):
        # update the object's rect attribute with the new x,y coordinates
        w, h = self.image.get_size()
        self.width, self.height = w, h
        self.rect = pygame.Rect(self.x - w / 2, self.y - h / 2, w, h)

    def update(self, screenWidth, screenHeight):
        vx, vy = self.velocity
        self.x += vx
        self.y += vy
        self.updateRect()
        