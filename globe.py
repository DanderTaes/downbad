import pygame as pg


NO_CAM = False
TILE_SIZE = 40
WIDTH, HEIGHT = TILE_SIZE*12, TILE_SIZE*15


WIN = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Downbad")

# pos = [[180,420], [240,420], [300,420], [60,480], [120,480], [180,480]]


PLATFORM_IMAGE = pg.image.load('./imgs/platform.png')
PLATFORM = pg.transform.scale(PLATFORM_IMAGE, (TILE_SIZE, TILE_SIZE))

PLATFORM_B_IMAGE = pg.image.load('./imgs/platform_breakeable.png')
PLATFORM_B = pg.transform.scale(PLATFORM_B_IMAGE, (TILE_SIZE, TILE_SIZE))

##############

FATBAT_IMAGE = pg.image.load('./imgs/fatbat1.png')
FATBAT1 = pg.transform.scale(FATBAT_IMAGE, (TILE_SIZE, TILE_SIZE))

FATBAT_IMAGE2 = pg.image.load('./imgs/fatbat2.png')
FATBAT2 = pg.transform.scale(FATBAT_IMAGE2, (TILE_SIZE, TILE_SIZE))

##############

PLAYER_WIDTH, PLAYER_HEIGHT = TILE_SIZE*0.9, TILE_SIZE*0.9

PLAYER_IMAGE_FALL1 = pg.image.load('./imgs/player_fall1.png')
PLAYER_FALL1 = pg.transform.scale(PLAYER_IMAGE_FALL1, (PLAYER_WIDTH, PLAYER_HEIGHT))
PLAYER_FALL1_M = pg.transform.flip(PLAYER_FALL1, True, False)
PLAYER_IMAGE_FALL2 = pg.image.load('./imgs/player_fall2.png')
PLAYER_FALL2 = pg.transform.scale(PLAYER_IMAGE_FALL2, (PLAYER_WIDTH, PLAYER_HEIGHT))
PLAYER_FALL2_M = pg.transform.flip(PLAYER_FALL2, True, False)
PLAYER_IMAGE_FALL1_5 = pg.image.load('./imgs/player_fall1_5.png')
PLAYER_FALL1_5 = pg.transform.scale(PLAYER_IMAGE_FALL1_5, (PLAYER_WIDTH, PLAYER_HEIGHT))
PLAYER_FALL1_5_M = pg.transform.flip(PLAYER_FALL1_5, True, False)

PLAYER_IMAGE_INV = pg.image.load('./imgs/invul.png')
PLAYER_INV = pg.transform.scale(PLAYER_IMAGE_INV, (PLAYER_WIDTH, PLAYER_HEIGHT))

PLAYER_IMAGE_IDLE = pg.image.load('./imgs/player_idle.png')
PLAYER_IDLE = pg.transform.scale(PLAYER_IMAGE_IDLE, (PLAYER_WIDTH, PLAYER_HEIGHT))
PLAYER_IDLE_M = pg.transform.flip(PLAYER_IDLE, True, False)

BULLET_IMAGE = pg.image.load('./imgs/bullet.png')

BULLET = pg.transform.scale(BULLET_IMAGE, (TILE_SIZE/2.5, TILE_SIZE * 2 / 3))

BULLET_ICON_IMAGE = pg.image.load('./imgs/bullet_icon.png')
BULLET_ICON = pg.transform.scale(BULLET_ICON_IMAGE, (TILE_SIZE/2, TILE_SIZE))
BULLET_ICON_OFF_IMAGE = pg.image.load('./imgs/bullet_icon_off.png')
BULLET_ICON_OFF = pg.transform.scale(BULLET_ICON_OFF_IMAGE, (TILE_SIZE/2, TILE_SIZE))

LIFE_ICON_IMAGE = pg.image.load('./imgs/life_icon.png')
LIFE_ICON = pg.transform.scale(LIFE_ICON_IMAGE, (TILE_SIZE/2, TILE_SIZE))
LIFE_ICON_OFF_IMAGE = pg.image.load('./imgs/life_icon_off.png')
LIFE_ICON_OFF = pg.transform.scale(LIFE_ICON_OFF_IMAGE, (TILE_SIZE/2, TILE_SIZE))