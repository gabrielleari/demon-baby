import pygame
from settings import *

class BG(pygame.sprite.Sprite):
    def __init__(self,groups):
        super().__init__(groups)
        self.image = pygame.image.load('../graphics/environment/background1.png').convert()
        self.rect = self.image.get_rect(topleft = (0,0))