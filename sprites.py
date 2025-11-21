import pygame
from settings import *
from random import choice, randint
class BG(pygame.sprite.Sprite): #creates bg object that behaves like pygame sprite
    def __init__(self,groups, scale_factor): #runs setup: which group it belongs to and how big it should be
        super().__init__(groups) #sets up bg object as real pygame sprite and add it to the given groups
        bg_image = pygame.image.load('environment/background1.png').convert() #loads bg image from file and convert it for faster display
        
        #.getheight method
        full_height = bg_image.get_height() * scale_factor #calculate new height of bg img after scaling
        full_width = bg_image.get_width() * scale_factor #calculate new width of bg img after scaling

        self.image = pygame.transform.scale(bg_image,(full_width, full_height)) #resize bg img to desired height and width and store in sprite's img attribute
        self.rect = self.image.get_rect(topleft = (0,0)) #create rectangle for sprite that dedines its position for human interaction,
        self.pos = pygame.math.Vector2(self.rect.topleft) #stores sprite's position as 2D vector for easier movement and math operations

    def update(self, dt): #define update method for sprite to change its state every frame
        self.pos.x -= 300 * dt #moves sprite left at speed of 300 px per second, scaled by time passed in sec since last frame
        self.rect.x = round(self.pos.x) #updates sprites rectangle position to match Vector2 position, rounding to an integer
        if self.rect.right <= 0:
            self.pos.x = 0
        self.rect.x = round(self.pos.x)