import pygame
from tilemap import collide_hit_rect
from settings import *

# vec = pygame.math.Vector2


def collide_with_walls(sprite, group, dir):
    if dir == "x":
        hits = pygame.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if sprite.vel.x > 0:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
            if sprite.vel.x < 0:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x
    if dir == "y":
        hits = pygame.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if sprite.vel.y > 0:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
            if sprite.vel.y < 0:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y


class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y, weapon="none"):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.health = PLAYER_HEALTH
        # self.vel = vec(0, 0)
        # self.pos = vec(x, y) * TILESIZE
        # self.hit_rect.center = self.rect.center

        self.up = False
        self.down = False
        self.left = False
        self.right = False
        self.weapon = weapon
        self.moveDelay = 0

    def update(self):
        self.collide_etc()
        self.get_keys()
        self.rect.x, self.rect.y = self.x * TILESIZE, self.y * TILESIZE

    def move(self, dx, dy):
        self.moveDelay += 1
        if self.moveDelay >= 8 and not self.collide_with_walls(dx, dy):
            self.x += dx
            self.y += dy
            self.moveDelay = 0

    def get_keys(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.move(0, -1)
            self.up = True
            self.down = False
            self.left = False
            self.right = False
        if keys[pygame.K_s]:
            self.move(0, 1)
            self.up = False
            self.down = True
            self.left = False
            self.right = False
        if keys[pygame.K_a]:
            self.move(-1, 0)
            self.up = False
            self.down = False
            self.left = True
            self.right = False
        if keys[pygame.K_d]:
            self.move(1, 0)
            self.up = False
            self.down = False
            self.left = False
            self.right = True

    def collide_with_walls(self, dx=0, dy=0):
        for wall in self.game.walls:
            if (
                wall.rect.x == self.rect.x + dx * TILESIZE
                and wall.rect.y == self.rect.y + dy * TILESIZE
            ):
                self.rect.centery -= PLAYER_WIDTH / 2
                return True
    
    def collide_etc(self):
        if pygame.sprite.spritecollideany(self, self.game.mobs):
            self.health -= 1
            if self.up == True and not self.collide_with_walls(2,0):
                self.move(2,0)
            if self.down == True and not self.collide_with_walls(-2,0):
                self.move(-2,0)
            if self.right == True and not self.collide_with_walls(0,2):
                self.move(0,2)
            if self.left == True and not self.collide_with_walls(0,-2):
                self.move(0,-2)
            if self.health <= 0 and not self.collide_with_walls:
                self.kill()


class Bullet(pygame.sprite.Sprite):
    def __init__(self, game, x, y, velx, vely):
        self.groups = game.all_sprites, game.Bullets
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.Surface((TILESIZE / 2, TILESIZE / 2))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.velx = velx
        self.vely = vely
        self.kill_timer = 0

    def update(self):
        # self.collision()
        self.collision_else()
        if not self.collision_else():
            self.x += self.velx  # * self.game.dt
            self.y += self.vely  # * self.game.dt
        self.rect.center = self.x, self.y
        if pygame.sprite.spritecollideany(self, self.game.walls):
            self.kill()
        
        
    def collision_else(self):
        if pygame.sprite.spritecollideany(self, self.game.mobs):
            #self.kill_timer += 1
            #if self.kill_timer >= 2:
            self.kill()
            return True
        else:
            return False
            #self.game.bullets.pop(self.game.bullets.index(self))

        # return wall, mob
