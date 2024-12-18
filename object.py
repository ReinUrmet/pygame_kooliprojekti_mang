import pygame
import functions_values as fv

ekraan_laius, ekraan_pikkus = 880, 700
ekraan_suurus = (ekraan_laius, ekraan_pikkus)  # kui suur on aken kus mäng toimub
aken = pygame.display.set_mode(ekraan_suurus, pygame.NOFRAME)
time = 0

class Objekt:
    def __init__(self, sprite=None, pos=None, speed=None, width=None, base_speed=None):
        self.speed = speed or [0, 0]
        self.pos = pos or [0, 0]
        self.width = width or self.sprite.get_width()
        self.change_sprite(sprite)
        self.base_speed = base_speed or [0, 0]

    def render(self):
        self.pos = [i + j for i, j in zip(self.pos, self.speed)]
        aken.blit(self.sprite, self.pos)

    def change_sprite(self, sprite=None):
        sprite = sprite or "placeholder.png"
        self.sprite = pygame.image.load("Sprites/" + sprite)
        heightdivwidth = (self.sprite.get_height() / self.sprite.get_width())
        if self.width is not None:
            self.sprite = pygame.transform.scale(self.sprite, (self.width, heightdivwidth * self.width))
    
    def flip_sprite(self):
        self.sprite = pygame.transform.flip(self.sprite, True, False)
