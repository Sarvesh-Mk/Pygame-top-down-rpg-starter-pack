from settings import *
import pygame

class saveMenu():

    def __init__(self, game):
        self.game = game
        self.loadSaveData = False
    
    def show_save_screen(self):
        self.filename = input("filename: ")
        self.f = open(f"{self.filename}", "w+")
        self.f.write(f"{self.player.rect.x//TILESIZE}\r\n")
        self.f.write(f"{self.player.rect.y//TILESIZE}\r\n")
        self.f.write(f"{self.player.weapon}\r\n")

    def menu(self, Text, color):
        self.button =  Button(WIDTH/2, HEIGHT/2, 12, 5, Text, color, self.game, 32)
        menu = True
        while menu:
            self.game.screen.fill(BACKGROUND_COLOR)
            self.button.update()
            self.game.mouse.update()
            self.game.events()
            pygame.display.flip()
    
    def load_save(self):
        self.menu('open save', ORANGE)
        self.save_data = []
        self.filename = input("filename: ")
        if self.filename == "none":
            self.loadSaveData = False
        if self.filename != "none":
            with open(self.filename, "rt") as f:
                for line in f:
                    self.save_data.append(line.strip())

            self.savex = self.save_data[0]
            self.savey = self.save_data[1]
            self.savex = int(self.savex)
            self.savey = int(self.savey)
            self.loadSaveData = True
        else:
            self.loadSaveData = False

class Button(pygame.sprite.Sprite):
    
    def __init__(self, x, y, width, height, text, color, game, font_size, img=None):
        self.groups = game.all_sprites
        self.game = game
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.width = width
        self.height = height
        self.font_size = font_size
        self.font = pygame.font.Font('freesansbold.ttf', self.font_size)
        if img == None:
            self.img = pygame.Surface((width * TILESIZE, height * TILESIZE))
            self.img.fill(color)
        else:
            self.img = pygame.image.load(img)
        
        self.rect = self.img.get_rect()
    
    def update(self):
        self.events()
        self.rect.centerx = self.x
        self.rect.centery = self.y
        self.renderedText = self.font.render(self.text,True, (0, 0, 0))
        self.game.screen.blit(self.img, self.rect)
        self.game.screen.blit(self.renderedText, (self.rect.x + self.width/2, self.rect.y + self.font_size))
    
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pass

class Mouse(pygame.sprite.Sprite):

    def __init__(self, pos, game, image=None):
        self.groups = game.all_sprites
        self.x, self.y = pos 
        pygame.mouse.set_visible(False)
        if image != None:
            self.img = image
        else:
            self.img = pygame.Surface((TILESIZE/4, TILESIZE/4))
            self.img.fill(WHITE)
        
        self.rect = self.img.get_rect()
    
    def update(self):
        self.rect.center = pygame.mouse.get_pos()