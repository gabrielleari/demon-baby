import pygame, sys, time
from settings import *
from sprites import BG, Ground,  Baby, Obstacle

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
        Ground([self.all_sprites, self.collision_sprites], self.scale_factor)
        self.baby = Baby(self.all_sprites, self.scale_factor/ 0.8)

        #timer
        self.obstacle_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.obstacle_timer,1400)

        #text
        self.font = pygame.font.Font()
        self.score = 0
        self.start_offset = 0
        
        #menu
        self.menu_surf = pygame.image.load('environment/game over menu.png').convert_alpha()
        self.menu_surf = pygame.transform.scale(self.menu_surf,(WINDOW_WIDTH,WINDOW_HEIGHT/1.5))
        self.menu_rect = self.menu_surf.get_rect(center = (WINDOW_WIDTH/2,WINDOW_HEIGHT/2))

    def collisions(self):
        if pygame.sprite.spritecollide(self.baby,self.collision_sprites,False, pygame.sprite.collide_mask)\
        or self.baby.rect.top <= 0:
            for sprite in self.collision_sprites.sprites():
                if sprite.sprite_type == 'obstacle':
                    sprite.kill()
            self.active = False
            self.baby.kill()

    def display_score(self):
        if self.active:
            self.score = (pygame.time.get_ticks() - self.start_offset) // 1000
            y = WINDOW_HEIGHT/10
        else:  
            y = WINDOW_HEIGHT / 2 + (self.menu_rect.height / 1.5)

        score_surf = self.font.render(str(self.score), False, 'black')
        score_rect = score_surf
        score_rect = score_surf.get_rect(midtop=(WINDOW_WIDTH/2,y))
        self.display_surface.blit(score_surf,score_rect)
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
                    if self.active:
                        self.baby.jump()
                    else:
                        self.baby = Baby(self.all_sprites, self.scale_factor / 0.8)
                        self.active = True
                        self.start_offset = pygame.time.get_ticks()
                if event.type == self.obstacle_timer and self.active:
                    Obstacle([self.all_sprites,self.collision_sprites], self.scale_factor * 1.1)  
            #game logic
            self.display_surface.fill('black') #fills entire game window w black color
            self.all_sprites.update(dt) #tells all sprites in all sprites group to update themselves
            self.all_sprites.draw(self.display_surface) #draws all sprites in the all_sprites group onto game window (display_surface)
            self.display_score()
            self.clock.tick(FRAMERATE) #limit game loop to run at maximum number of FPS

            if self.active: 
                self.collisions()
            else:
                self.display_surface.blit(self.menu_surf, self.menu_rect)
            pygame.display.update() #refresh game window to show everything drawn since last frame
if __name__ == '__main__':
        game = Game()
        game.run()