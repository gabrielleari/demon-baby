import pygame
from settings import *
from random import choice, randint

class BG(pygame.sprite.Sprite): #creates bg object that behaves like pygame sprite
    def __init__(self,groups, scale_factor): #runs setup: which group it belongs to and how big it should be
        super().__init__(groups) #sets up bg object as real pygame sprite and add it to the given groups
        self.background = ('environment/background1.png')
        bg_image = pygame.image.load(self.background).convert() #loads bg image from file and convert it for faster display
        
        #.getheight method
        full_height = bg_image.get_height() * scale_factor #calculate new height of bg img after scaling
        full_width = bg_image.get_width() * scale_factor #calculate new width of bg img after scaling

        full_sized_image = pygame.transform.scale(bg_image,(full_width, full_height)) #resize bg img to desired height and width and store in sprite's img attribute
       
        self.image = pygame.Surface((full_width * 2,full_height))
        self.image.blit(full_sized_image, (0,0))
        self.image.blit(full_sized_image, (full_width,0))

        self.rect = self.image.get_rect(topleft = (0,0)) #create rectangle for sprite that dedines its position for human interaction,
        self.pos = pygame.math.Vector2(self.rect.topleft) #stores sprite's position as 2D vector for easier movement and math operations

    def update(self, dt): #define update method for sprite to change its state every frame
        self.pos.x -= 300 * dt #moves sprite left at speed of 300 px per second, scaled by time passed in sec since last frame
        if self.rect.centerx <= 0:
            self.pos.x = 0
        self.rect.x = round(self.pos.x)  #updates sprites rectangle position to match Vector2 position, rounding to an integer
    
    def change_background(self,score,scale_factor):
        if score > 7:
            self.background = ('environment/background3.png')
        elif score > 3: 
            self.background = ('environment/background2.png')
        else:
            self.background = ('environment/background1.png')
        bg_image = pygame.image.load(self.background).convert()
        full_height = bg_image.get_height() * scale_factor #calculate new height of bg img after scaling
        full_width = bg_image.get_width() * scale_factor #calculate new width of bg img after scaling

        full_sized_image = pygame.transform.scale(bg_image,(full_width, full_height)) #resize bg img to desired height and width and store in sprite's img attribute
       
        self.image = pygame.Surface((full_width * 2,full_height))
        self.image.blit(full_sized_image, (0,0))
        self.image.blit(full_sized_image, (full_width,0))

        

class Ground(pygame.sprite.Sprite):
    def __init__(self,groups,scale_factor):
        super().__init__(groups)
        self.sprite_type = 'ground'
        #image
        ground_surf = pygame.image.load('environment/ground.png').convert_alpha()
        self.image = pygame.transform.scale(ground_surf, pygame.math.Vector2 (ground_surf.get_size()) * scale_factor)
        
        #position
        self.rect = self.image.get_rect(bottomleft = (0,WINDOW_HEIGHT))
        self.pos = pygame.math.Vector2(self.rect.topleft)

        #mask
        self.mask = pygame.mask.from_surface(self.image)
    def update(self, dt):
        self.pos.x -= 360 * dt
        if self.rect.centerx < 0:
            self.pos.x = 0

        self.rect.x = round(self.pos.x)

class Baby(pygame.sprite.Sprite):
    def __init__ (self, groups, scale_factor):
        super().__init__(groups)

        #image
        self.import_frames(scale_factor)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]

        #rect
        self.rect = self.image.get_rect(midleft = (WINDOW_WIDTH / 20, WINDOW_HEIGHT / 2))
        self.pos = pygame.math.Vector2(self.rect.topleft)

        #movement
        self.gravity = 600
        self.direction = 0

        #mask
        self.mask = pygame.mask.from_surface(self.image)
    
    def import_frames(self,scale_factor):
        self.frames = []
        for i in range(3):
            surf = pygame.image.load('Baby\demon baby sprite.png').convert_alpha()
            scaled_surface = pygame.transform.scale(surf, pygame.math.Vector2(surf.get_size()) * scale_factor)
            self.frames.append(scaled_surface)

    def apply_gravity(self,dt):
        self.direction += self.gravity * dt
        self.pos.y += self.direction * dt
        self.rect.y = round(self.pos.y)

    def jump(self):
        self.direction = - 400

    def animate(self,dt):
        self.frame_index += 10 * dt
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def rotate(self): 
        rotated_baby = pygame.transform.rotozoom(self.image,-self.direction * 0.06,1)
        self.image = rotated_baby
        self.mask = pygame.mask.from_surface(self.image)
    def update(self,dt):
        self.apply_gravity(dt)
        self.animate(dt)
        self.rotate()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self,groups,scale_factor):
        super().__init__(groups)
        self.sprite_type = 'obstacle'

        orientation = choice(('up', 'down'))
        surf = pygame.image.load(f'obstacles/Snakes {choice( (2, 3) )}.png').convert_alpha()
        self.image = pygame.transform.scale(surf,pygame.math.Vector2(surf.get_size())* scale_factor)

        x = WINDOW_WIDTH + randint(40,100)
        y = WINDOW_HEIGHT + randint(10,50)
        self.rect = self.image.get_rect(midbottom = (x,y))

        self.pos = pygame.math.Vector2(self.rect.topleft)
        
        #mask
        self.mask = pygame.mask.from_surface(self.image)



    def update(self,dt):
        self.pos.x -= 400 * dt
        self.rect.x = round(self.pos.x)
        if self.rect.right <= -100:
            self.kill()