import pygame
from object import Objekt
import functions_values as fv

# Defineerime speed_length globaalselt
speed_length = float('inf')  # Esialgne väärtus, määratud lõpmatusse

class Pintsel(Objekt):
    def render(self):
        global speed_length  # Viidatakse globaalsele muutujale
        mouse_pos = pygame.mouse.get_pos()
        mouse_x = mouse_pos[0]
        mouse_y = mouse_pos[1] - self.sprite.get_height()  # Selleks, et pintsli vasak alumine äär oleks kursori peal
        speed_x = mouse_x - self.pos[0]
        speed_y = mouse_y - self.pos[1]
        if speed_length < 20:
            self.pos = [mouse_x, mouse_y]
        else:
            jump_slow = 3.75
            speed_length = fv.get_vector_length([speed_x, speed_y])
            self.speed = (speed_x / jump_slow, speed_y / jump_slow)
        super().render()

class Värv(Objekt):
    def __init__(self, sprite, pos):
        self.sprite = sprite
        self.pos = pos
        self.speed = [0, 0]
