import pygame
from settings import *
import random


class mob(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mobs
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.kill_radius = pygame.Rect(x * TILESIZE, y * TILESIZE, TILESIZE * 20, TILESIZE * 20)
        self.x = x
        self.y = y
        self.moveDelay = 0
        self.chance = 1
        self.speed = 40

    def update(self):
        self.collision_etc()
        self.rect.x, self.rect.y = self.x * TILESIZE, self.y * TILESIZE
        self.plan_move(self.game.player.x, self.game.player.y)

    def plan_move(self, x, y):
        self.kill_radius.center = self.rect.center
        if self.kill_radius.colliderect(self.game.player.rect):
            if self.x != x:
                if x < self.x:
                    self.dx = -1
                    self.dy = 0
                if x > self.x:
                    self.dx = 1
                    self.dy = 0
                self.move(self.dx, self.dy)
            if self.y != y:
                if y < self.y:
                    self.dy = -1
                    self.dx = 0
                if y > self.y:
                    self.dy = 1
                    self.dx = 0
                self.move(self.dx, self.dy)
        
        else:
            self.WalkCycle()

    def WalkCycle(self):
        self.chance += 1#random.randint(1,4)
        if self.chance == 4:
            self.chance = 1
        if self.chance == 1:
            self.move(1,0)
        if self.chance == 2:
            self.move(0,-1)
        if self.chance == 3:
            self.move(-1,0)
        if self.chance == 4:
            self.move(0,1)

    def move(self, dx, dy):
        self.moveDelay += 1
        if self.moveDelay >= 40 and not self.collide_with_walls(dx, dy) and not self.collision_etc():
            self.x += dx
            self.y += dy
            self.moveDelay = 0

    def collide_with_walls(self, dx=0, dy=0):
        for wall in self.game.walls:
            if (
                wall.rect.centerx == self.rect.centerx + dx * TILESIZE
                and wall.rect.centery == self.rect.centery + dy * TILESIZE
            ):
                return True
        return False
    
    def collision_etc(self):
        if pygame.sprite.spritecollideany(self, self.game.Bullets):
            self.kill()
            return True