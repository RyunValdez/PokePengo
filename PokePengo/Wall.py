################################################################################
##                          PokePengo                                         ##
##                          Wall Class                                        ##
##                                                                            ##
##              Programmed by Ryun Valdez                                     ##
##                                                                            ##
################################################################################

import pygame

class wall(pygame.sprite.Sprite):

    s = pygame.sprite.Group()
    
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self, wall.s)
        self.x = x*32
        self.y = y*32+64
        #Initialize
        self.rect = pygame.Rect(x*32,y*32+64, 32, 32)


