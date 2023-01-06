import pygame as pg
vec = pg.math.Vector2
from abc import ABC, abstractmethod

class Camera:
    def __init__(self, WIDTH, HEIGHT, player):
        self.player = player
        self.offset = vec(300,400)
        self.offset_float = vec(0,0)
        self.DISPLAY_W, self.DISPLAY_H = WIDTH, HEIGHT
        self.CONST = vec(0, -self.DISPLAY_H/2+player.rect.h/2)
    
    def setmethod(self, method):
        self.method = method

    def scroll(self):
        
        self.method.scroll()

class CamScroll(ABC):
    def __init__(self, camera, player):
        self.camera = camera
        self.player = player
    
    @abstractmethod
    def scroll(self):
        pass

class Follow(CamScroll):
    def __init__(self, camera, player):
        CamScroll.__init__(self, camera, player)
    
    def scroll(self):
        self.camera.offset_float.y += (self.player.rect.y - self.camera.offset_float.y + self.camera.CONST.y)
        self.camera.offset.y = int(self.camera.offset_float.y)

class Border(CamScroll):
    def __init__(self, camera, player):
        CamScroll.__init__(self, camera, player)
    
    def scroll(self):
        self.camera.offset_float.y += (self.player.rect.y - self.camera.offset_float.y + self.camera.CONST.y)
        self.camera.offset.y = int(self.camera.offset_float.y)
        # self.camera.offset.y = min(self.player.rect.centery, self.camera.offset.y)
        # print(self.camera.offset.y, self.player.rect.bottom - self.camera.DISPLAY_H)
        # self.camera.offset.y = max(self.camera.offset.y , self.player.rect.bottom - self.camera.DISPLAY_H)

class NoCam(CamScroll):
    def __init__(self, camera, player):
        CamScroll.__init__(self, camera, player)
    
    def scroll(self):
        self.camera.offset.y = 0



