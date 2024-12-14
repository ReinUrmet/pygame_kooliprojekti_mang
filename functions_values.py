import pygame, random

#keybinds
up = [pygame.K_UP, pygame.K_w]
down = [pygame.K_DOWN, pygame.K_s]
left = [pygame.K_LEFT, pygame.K_a]
right = [pygame.K_RIGHT,pygame.K_d]


#get random texture for drawing
def get(width, height):
    img = pygame.image.load("Sprites/draw_texture.png").convert_alpha()
    x = random.randint(0, img.get_width() - width)
    y = random.randint(0, img.get_height() - height)
    return img.subsurface((x, y, width, height))
