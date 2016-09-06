################################################################################
##                          PokePengo                                         ##
##                          Pokeball Class                                    ##
##                                                                            ##
##              Programmed by Ryun Valdez                                     ##
##                                                                            ##
################################################################################

import pygame
import Tile

pygame.mixer.init(44100, -16, 2, 2048)

class pokeball(pygame.sprite.Sprite):

    s = pygame.sprite.Group()
    rolling = pygame.sprite.Group()
    breaking = pygame.sprite.Group()
    
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self, pokeball.s)
        #Roll speed
        self.roll_speed = 8
        #Variables
        self.i=0
        self.j=0
        self.roll_dir = ''
        self.offset = 0
        self.breakTime = pygame.time.get_ticks()
        #Awareness
        self.location=Tile.tile.grid[x][y]
        self.radar=Tile.tile.grid[x][y+1]
        #Initialize image
        self.pokeballSheet = pygame.image.load('Graphics/ball_roll.png')
        self.pokeballSheet.set_clip(pygame.Rect(0,0, 32,32))
        self.pokeballImg = self.pokeballSheet.subsurface(self.pokeballSheet.get_clip())
        self.rect = self.pokeballImg.get_rect()
        #Place rect object at real coordinates
        self.rect.topleft = (x*32,y*32+64)
        self.x = self.rect.x
        self.y = self.rect.y
        #Set timing
        self.last = pygame.time.get_ticks()
        self.cooldown = 50

    def x2grid(self,x):
        xgrid = int(x/32)
        return xgrid

    def y2grid(self,y):
        ygrid = int((y-64)/32)
        return ygrid
    def scanTiles(self):
        #Not working, cyclical reference
##        #Empty old location
##        self.location.empty()
##        #Update new location
##        self.location = Tile.grid[self.x2grid(self.x)][self.y2grid(self.y)]
##        #Fill new location
##        self.location.fill(self)
        #Left
        if self.roll_dir=='left':
            self.radar=Tile.tile.grid[self.x2grid(self.x)-1][self.y2grid(self.y)]
        #Right
        elif self.roll_dir=='right':
            self.radar=Tile.tile.grid[self.x2grid(self.x)+1][self.y2grid(self.y)]
        #Up
        elif self.roll_dir=='up':
            self.radar=Tile.tile.grid[self.x2grid(self.x)][self.y2grid(self.y)-1]
        #Down
        elif self.roll_dir=='down':
            self.radar=Tile.tile.grid[self.x2grid(self.x)][self.y2grid(self.y)+1]
    def roll(self):
        #Scan Ball Vision
        if self.x%32==0 and self.y%32==0:
            self.scanTiles()
        if self.roll_dir == 'left':
            self.j = 0
            self.x -= self.roll_speed
            now = pygame.time.get_ticks()
            if now - self.last >= self.cooldown-25:
                self.last = now
                self.i+=1
                if self.i > 7:
                    self.i=0
        elif self.roll_dir == 'right':
            self.j = 1
            self.x += self.roll_speed
            now = pygame.time.get_ticks()
            if now - self.last >= self.cooldown-25:
                self.last = now
                self.i+=1
                if self.i > 7:
                    self.i=0
        elif self.roll_dir == 'up':
            self.j = 2
            self.y -= self.roll_speed
            now = pygame.time.get_ticks()
            if now - self.last >= self.cooldown:
                self.last = now
                self.i+=1
                if self.i > 7:
                    self.i=1
        elif self.roll_dir == 'down':
            self.j = 3
            self.y += self.roll_speed
            now = pygame.time.get_ticks()
            if now - self.last >= self.cooldown:
                self.last = now
                self.i+=1
                if self.i > 7:
                    self.i=1
        #Object Location Update
        self.rect.topleft = (self.x,self.y)

    def destroy(self, success):
        now = pygame.time.get_ticks()
        if now - self.breakTime >= self.cooldown*20:
            self.kill()
            Tile.tile.grid[self.x2grid(self.x)][self.y2grid(self.y)].empty()
        elif now - self.breakTime >= self.cooldown*16:
            self.offset = 16
            self.pokeballImg = pygame.image.load('Graphics/ball_open.png')
            success=True
            return success
        elif now - self.breakTime >= self.cooldown*6:
            self.pokeballImg = self.pokeballSheet.subsurface(self.pokeballSheet.get_clip())
        elif now - self.breakTime >= self.cooldown*1:
            self.pokeballImg = pygame.image.load('Graphics/ball_tilt.png')
                        
    def update(self, surface):
        #Current Frame Update    
        self.pokeballSheet.set_clip(pygame.Rect(self.i*32,self.j*32, 32,32))
        if self not in pokeball.breaking:
            self.pokeballImg = self.pokeballSheet.subsurface(self.pokeballSheet.get_clip())
        #Image Location Update
        surface.blit(self.pokeballImg,(self.x,self.y-self.offset))
