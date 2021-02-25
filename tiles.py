import pygame
from settings import *

class Wall(pygame.sprite.Sprite):
    def __init__(self, game, x, y, sprite='none'):
        self.groups = game.all_sprites, game.walls
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        if sprite =='none':
            self.image = pygame.Surface((TILESIZE, TILESIZE))
        else:
            self.image = sprite
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Chest(pygame.sprite.Sprite):
    def __init__(self, game, x, y, sprite='none'):
        self.groups = game.all_sprites, game.chests
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        if sprite == 'none':
            self.image = pygame.Surface((TILESIZE, TILESIZE))
        else:
            pass
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.opened = False

    def update(self):
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE
        self.check_if_opened()

    def check_if_opened(self):
        if self.opened == False:
            if self.game.player.rect.colliderect(self.rect):
                self.opened = True
                self.game.player.weapon = 'bullet'

class door(pygame.sprite.Sprite):
    def __init__(self,game,x,y,velx,vely,sprite='none'):
        self.groups = game.all_sprites, game.walls
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        if sprite == 'none':
            self.image = pygame.Surface((TILESIZE, TILESIZE))
        else:
            pass
        self.image.fill(ORANGE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE
        self.velx = velx
        self.vely = vely
        self.locked = True
        self.opened = False
        self.moveDelay = 0

    def update(self):
        self.check()
        if self.locked == False and self.opened == False:
            self.open_animation()
    
    def open_animation(self):
        for x in range(32):
            self.x += self.velx
            self.y += self.vely
        self.opened = True
        return x
    
    def check(self):
        if len(self.game.enemies) <= 0:
            self.locked = False
