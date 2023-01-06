import pygame as pg
from globe import *
import os


class Bullet(pg.sprite.Sprite):    
    def __init__(self, x, y, platforms, breakeable):
        super().__init__()
        self.image = BULLET
        self.rect = self.image.get_rect()
        self.width = TILE_SIZE/2.5
        self.height = TILE_SIZE * 2 / 3
        self.platforms = platforms
        self.breakeable = breakeable
        self.rect.y = y-self.height/2
        self.rect.x = x-self.width/2
        self.camera = None
    
    def draw(self, win, camera):
        win.blit(self.image, (self.rect.x, self.rect.y - camera.offset.y))

    def update(self, dt, camera, player, *args):
        self.camera = camera
        self.rect.y += 10
        collisions = pg.sprite.spritecollide(self, self.platforms, False)
        for platform in collisions:
            self.kill()
        if self.rect.y > HEIGHT + camera.offset.y:
            self.kill()
        
        collisions = pg.sprite.spritecollide(self, self.breakeable, False)
        for platform in collisions:
            platform.kill()
        enemy_kill = pg.sprite.spritecollide(self, player.enemies, False)
        for enemy in enemy_kill:
            enemy.kill()

class Bullet_icon(pg.sprite.Sprite):
    def __init__(self, x, y, number):
        super().__init__()
        pg.sprite.Sprite.__init__(self)
        self.image = BULLET_ICON
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        self.number = number
    
    def draw(self, win, camera):
        win.blit(self.image, (self.rect.x, self.rect.y - camera.offset.y))
    
    def update(self, dt, camera, player):
        self.rect.y = player.pos.y + TILE_SIZE*6
        if self.number < player.bullets:
            self.image = BULLET_ICON
        else:
            self.image = BULLET_ICON_OFF


class Life_icon(pg.sprite.Sprite):
    def __init__(self, x, y, number):
        super().__init__()
        pg.sprite.Sprite.__init__(self)
        self.image = LIFE_ICON
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        self.number = number
    
    def draw(self, win, camera):
        win.blit(self.image, (self.rect.x, self.rect.y - camera.offset.y))
    
    def update(self, dt, camera, player):
        self.rect.y = player.pos.y + TILE_SIZE*5
        if self.number < player.life:
            self.image = LIFE_ICON
        else:
            self.image = LIFE_ICON_OFF

class Player(pg.sprite.Sprite):
    def __init__(self, x, y, platforms, enemies):
        super().__init__()
        self.acc_y = 1200
        self.vel = pg.math.Vector2(0,0)
        self.pos = pg.math.Vector2(x,y)
        self.platforms = platforms
        self.enemies = enemies
        self.bullets_max = 8
        self.bullets = self.bullets_max
        self.life_max = 1
        self.life = self.life_max
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT

        self.index = 0
        self.animation_time = 0.1
        self.current_time = 0
        self.animation_frames = 3
        self.current_frame = 0
        self.direction = "r"
        
        self.images = []
        self.image = PLAYER_FALL1
        self.falling_images = [PLAYER_FALL1, PLAYER_FALL1_5, PLAYER_FALL2]
        self.falling_images_m = [PLAYER_FALL1_M, PLAYER_FALL1_5_M, PLAYER_FALL2_M]
        self.idle_images = [PLAYER_IDLE]
        self.idle_images_m = [PLAYER_IDLE_M]

        self.images = self.falling_images
        self.time_start = 0
        self.time = 0
        self.rect = pg.Rect(x, y, self.width, self.height)
        self.invulnerable = False
        self.i = 0
        # self.rect_bottom = pg.Rect(x+10, y+50, self.width-20, self.height/6)
        # self.rect_left = pg.Rect(x, y, self.width/6, self.height)
        # self.rect_right = pg.Rect(x+50, y, self.width/6, self.height)
        # self.rect_top = pg.Rect(x+10, y, self.width-20, self.height/6)
        self.is_falling = True
        self.is_jumping = True
        self.camera = None

    
    def draw(self, win, camera):
        win.blit(self.image, (self.rect.x, self.rect.y - camera.offset.y))
    
    def animation_change(self, frames, images, time):
        self.animation_time = time
        self.animation_frames = frames
        self.images = images
    
    def update(self, dt, camera, *args):

        if self.rect.y >= 105*TILE_SIZE:
            self.pos.y = HEIGHT/9
            self.vel.y = 0
        if self.rect.x > WIDTH - self.width:
            self.pos.x = WIDTH - self.width
            # self.vel_x = 0 # TODO: acceleration
        elif self.rect.x < 0:
            self.pos.x = 0
        self.pos.x += self.vel.x * dt
        self.rect.x = self.pos.x

        platform_collisions = pg.sprite.spritecollide(self, self.platforms, False)
        for block in platform_collisions:  
            if self.vel.x > 0:   # Move right
                self.rect.right = block.rect.left  
                
            elif self.vel.x < 0:  # Move left
                self.rect.left = block.rect.right 
            self.pos.x = self.rect.x  

        self.pos.y += self.vel.y * dt
        # +1 to check if we're on a platform each frame.
        self.rect.y = self.pos.y + 1
        # Prevent air jumping when falling.
        if self.vel.y > 0:
            self.is_falling = True

        platform_collisions = pg.sprite.spritecollide(self, self.platforms, False)
        for block in platform_collisions:  # Vertical collision occurred.
            if self.vel.y > 0:  # Moving down.
                self.rect.bottom = block.rect.top  # Reset the rect pos.
                self.vel.y = 0  # Stop falling.
                self.is_jumping = False
                self.bullets = self.bullets_max
                self.is_falling = False
            elif self.vel.y < 0:  # Moving up.
                self.rect.top = block.rect.bottom  # Reset the rect pos.
                self.vel.y = 0  # Stop jumping.
            self.pos.y = self.rect.y  # Update the actual y-position.
        
        enemy_collisions = pg.sprite.spritecollide(self, self.enemies, False)
        for _ in enemy_collisions:
            if self.invulnerable == False:
                self.life -= 1
                self.vel.x *= -0.8
                self.vel.y *= -1
                self.invulnerable = True
                self.i = 60
        
        
        if self.invulnerable and self.i == 0 and self.life > 0:
            self.invulnerable = False
        elif self.invulnerable == False and PLAYER_INV in self.images:
            self.images.remove(PLAYER_INV)
            self.animation_frames -= 1
        elif self.invulnerable:
            if PLAYER_INV not in self.images: 
                self.images.append(PLAYER_INV)
                self.animation_frames += 1
                
        if self.i > 0:
            self.i -= 1
        
        if self.life == 0: # TODO: RESET DEATH
            if PLAYER_INV in self.images:
                self.images.remove(PLAYER_INV)
                self.animation_frames -= 1
            self.invulnerable = False
           
        # Sprite change animations
        if self.is_falling and self.i < 30 :
            if self.direction == "r":
                self.animation_change(3, self.falling_images, 0.1)
            elif self.direction == "l" :
                self.animation_change(3, self.falling_images_m, 0.1)

            # print("falling")

        elif self.is_falling == False:
            if self.direction == "r":
                self.animation_change(1, self.idle_images, 0.1)
            elif self.direction == "l":
                self.animation_change(1, self.idle_images_m, 0.1)
            # print("idle")

            
        
        # Sprites 
        self.current_time += dt
        if self.current_time >= self.animation_time:
            self.current_time = 0
            self.index = (self.index + 1) % len(self.images)
            self.image = self.images[self.index]
            
        self.vel.y += self.acc_y * dt  # Gravity

