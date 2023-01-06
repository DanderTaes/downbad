import pygame as pg
from globe import *

class Fatbat(pg.sprite.Sprite):
    def __init__(self, x, y, imgw, imgh):
        super().__init__()
        pg.sprite.Sprite.__init__(self)
        self.image = FATBAT1
        self.images = [FATBAT1, FATBAT2]
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        self.index = 0
        self.animation_time = 0.2
        self.current_time = 0
        self.animation_frames = 3
        self.current_frame = 0
        self.offset = TILE_SIZE
        self.additive = 1
    
    def draw(self, win, camera):
        win.blit(self.image, (self.rect.x, self.rect.y - camera.offset.y))
    
    def update(self, dt, camera, *args):
        if self.offset == 0:
            self.offset = TILE_SIZE
            self.additive *= -1
        self.rect.y -= self.additive
        self.offset -=1



        self.current_time += dt
        if self.current_time >= self.animation_time:
            self.current_time = 0
            self.index = (self.index + 1) % len(self.images)
            self.image = self.images[self.index]