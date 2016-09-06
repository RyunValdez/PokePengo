################################################################################
##                          PokePengo                                         ##
##                          Tile Class                                        ##
##                                                                            ##
##              Programmed by Ryun Valdez                                     ##
##                                                                            ##
################################################################################

import pygame
import Level
import Pokeball
import Specialball
import Enemy
import Wall

class tile(pygame.sprite.Sprite):

    s = pygame.sprite.Group()
    grid = [[0]*17 for i in range(15)]
    
    def __init__(self, object_=None,solid=False):
        pygame.sprite.Sprite.__init__(self, tile.s)
        self.solid = solid
        self.object = object_
        if self.object in Pokeball.pokeball.s:
            self.solid=True
        elif self.object in Specialball.specialball.s:
            self.solid=True
        elif self.object in Wall.wall.s:
            self.solid=True

    def empty(self):
        self.object=None
        self.solid=False
        
    def fill(self,object_):
        self.object=object_
        if self.object in Pokeball.pokeball.s:
            self.solid=True
        elif self.object in Specialball.specialball.s:
            self.solid=True
        elif self.object in Wall.wall.s:
            self.solid=True
        else:
            self.solid=False
            
def set_level():
    for i in range(17):
        for j in range(15):
            if Level.Viridian_Forest[i][j]=='W':
                tile.grid[j][i] = tile(object_=Wall.wall(j,i))
            elif Level.Viridian_Forest[i][j]=='O':
                tile.grid[j][i] = tile(object_=Pokeball.pokeball(j,i))
            elif Level.Viridian_Forest[i][j]=='E':
                tile.grid[j][i] = tile(object_=Enemy.enemy(j,i))
            elif Level.Viridian_Forest[i][j]=='S':
                tile.grid[j][i] = tile(object_=Specialball.specialball(j,i))
            else:
                tile.grid[j][i] = tile(object_=None)

set_level()
