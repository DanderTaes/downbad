import pygame as pg
from pygame.math import Vector2
import os
from player import Player, Bullet, Bullet_icon, Life_icon
from enemies import Fatbat
import camera as cam
from globe import *
import map_reader


class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, imgw, imgh, img):
        super().__init__()
        pg.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
    
    def draw(self, win, camera):
        win.blit(self.image, (self.rect.x, self.rect.y - camera.offset.y))

def draw_platform(platform_positions, breakeable = False):
    if breakeable:
        img = PLATFORM_B
    else:
        img = PLATFORM
    platform_group = pg.sprite.Group()
    for platform_position in platform_positions:
        platform = Platform(platform_position[1], platform_position[0], TILE_SIZE, TILE_SIZE, img)
        platform_group.add(platform)
    return platform_group

def draw_fatbat(fatbat_positions):
    fatbat_group = pg.sprite.Group()
    for fatbat_position in fatbat_positions:
        fatbat = Fatbat(fatbat_position[1], fatbat_position[0], TILE_SIZE, TILE_SIZE)
        fatbat_group.add(fatbat)
    return fatbat_group


def draw_ammo_icons(icon_total, player_y): # TODO delete icons each time b4 drawing
    icon_group = pg.sprite.Group()
    for i in range(icon_total):
        icon_sprite = Bullet_icon(0+i*(TILE_SIZE/2), player_y + TILE_SIZE*10, i)
        icon_group.add(icon_sprite)
    return icon_group

def draw_life_icons(icon_total, player_y): # TODO delete icons each time b4 drawing
    icon_group = pg.sprite.Group()
    for i in range(icon_total):
        icon_sprite = Life_icon(0+i*(TILE_SIZE/2), player_y + TILE_SIZE*10, i)
        icon_group.add(icon_sprite)
    return icon_group

def draw_window(objects, camera):
    WIN.fill((0,0,0))
    for item in objects:
        item.draw(WIN, camera)

def player_reset(player):
    player.pos.y = HEIGHT/2
    player.pos.x = WIDTH/2
    player.vel.y = 0
    player.vel.x = 0
    player.life = player.life_max
    player.bullets = player.bullets_max





def main_loop():

    all_sprites = pg.sprite.Group()
    all_enemies = pg.sprite.Group()
    all_icons = pg.sprite.Group()
    all_platforms = pg.sprite.Group()
    resetables = pg.sprite.Group()

    
    def level_set(lvl:int):# Load sprites 
        url = f"./imgs/map{lvl}.png"
        POS_PLATFORM = map_reader.map_array(url, TILE_SIZE, (51,51,51))
        POS_PLATFORM_B = map_reader.map_array(url, TILE_SIZE, (216,0,255))
        POS_FATBAT = map_reader.map_array(url, TILE_SIZE, (29,255,0))


        platforms = draw_platform(POS_PLATFORM)
        platforms_b = draw_platform(POS_PLATFORM_B, True)
        all_platforms.add(platforms, platforms_b)
        all_fatbats = draw_fatbat(POS_FATBAT)
        all_enemies.add(all_fatbats)
        resetables.add(all_enemies, platforms_b)

        return platforms, platforms_b
    
    # Load camera and player
    
    player = Player(WIDTH/2, HEIGHT/2, all_platforms, all_enemies)
    ammo_icons = draw_ammo_icons(player.bullets_max, player.pos.y)
    life_icons = draw_life_icons(player.life_max, player.pos.y)
    all_icons.add(ammo_icons, life_icons)

    platforms, platforms_b = level_set(1)
    all_sprites.add(all_platforms, all_enemies, all_icons, player)
    camera = cam.Camera(WIDTH, HEIGHT, player)
    border = cam.Border(camera,player)
    camera.setmethod(border)
    
    
    clock = pg.time.Clock()
    dt = 0
    run = True

    while run:        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    if player.is_falling == False:
                        player.vel.y = -400
                        player.pos.y -= 20
                        player.is_falling = True                       
                    elif player.bullets > 0:
                        player.vel.y = -50
                        player.pos.y -= 5
                        fireball = Bullet(player.pos.x+player.width/2, player.pos.y+player.height, platforms, platforms_b)
                        all_sprites.add(fireball)
                        player.bullets -= 1
                        pg.key.set_repeat(400, 200)
                elif event.key == pg.K_a and player.invulnerable == False:
                    player.vel.x = -220
                    player.direction = "l"
                elif event.key == pg.K_d and player.invulnerable == False:
                    player.vel.x = 220
                    player.direction = "r"
            elif event.type == pg.KEYUP:
                if event.key == pg.K_SPACE:
                    player.is_jumping = True
                elif event.key == pg.K_a and player.vel.x < 0:
                    player.vel.x = 0
                elif event.key == pg.K_d and player.vel.x > 0:
                    player.vel.x = 0
                elif event.key == pg.K_ESCAPE:
                    run = False
        

            
       

        all_sprites.update(dt, camera, player)
        #print(camera.offset)
        camera.scroll()
        
        
        draw_window(all_sprites, camera)
        if player.life == 0:
            player_reset(player)

            for sprite in resetables:
                sprite.kill()
            platforms, platforms_b = level_set(1)
        

        
        keys_pressed = pg.key.get_pressed()

        pg.display.flip()
        dt = clock.tick(60) / 1000

    pg.quit()

if __name__ == "__main__": 
    pg.init()
    main_loop()