import pygame, sys, time
from settings import *
from sprites import BG, Ground,  Baby

class Game: 
    def __init__(self): #function that runs when new object is created

        #setup
        pygame.init() #turns un/starts all python modules game needs
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT)) #creates game window, sets screen surface
        pygame.display.set_caption('Demon Baby') #sets title of game window at top of tab
        self.clock = pygame.time.Clock() #creates clock object that keeps track of time in game
        self.active = True #

        #sprite groups
        self.all_sprites = pygame.sprite.Group() #creates group to store all game sprites
        self.collision_sprites = pygame.sprite.Group() #group to store sprites to check collisions against

        #scale factor
        bg_height = pygame.image.load('environment/background1.png').get_height() #loads image and gets height
        self.scale_factor = WINDOW_HEIGHT / bg_height #calculate scaling factor to resize bg img to fit window height

        #sprite setup
        BG(self.all_sprites, self.scale_factor) #make bg sprite, scale it to screen, and add to main sprite group so it appears in game
        Ground(self.all_sprites, self.scale_factor)
        self.baby = Baby(self.all_sprites, self.scale_factor/ 0.8)

    def run(self): #func will run main logic of gamw
        last_time = time.time() #store current time (in seconds) in variable called last_time
        while True: 

            dt = time.time() - last_time #calculate time difference (delta time) since last frame
            last_time = time.time() #update last_time to current time

            #event loop
            for event in pygame.event.get(): #go through all events Pygame has registered since the last game
                if event.type == pygame.QUIT: #go through all events pygame has registered since last frame
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                     self.baby.jump()

            #game logic
            self.display_surface.fill('black') #fills entire game window w black color
            self.all_sprites.update(dt) #tells all sprites in all sprites group to update themselves
            self.all_sprites.draw(self.display_surface) #draws all sprites in the all_sprites group onto game window (display_surface)
            pygame.display.update() #refresh game window to show everything drawn since last frame
            self.clock.tick(FRAMERATE) #limit game loop to run at maximum number of FPS

if __name__ == '__main__':
        game = Game()
        game.run()