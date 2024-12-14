import pygame, sys, threading, math
from pygame.transform import scale
import keybinds as kb # file kus on kõik keybindid
pygame.init()
pygame.font.init()

# Põhi sätted
font = pygame.font.Font('GOTHIC.ttf', 40)  # valib fondi ja selle suuruse
timer = pygame.time.Clock()
FPS = 60
pygame.display.set_caption("Mäng")

# Ekraan
ekraan_laius,ekraan_pikkus = 880, 700
ekraan_suurus = (ekraan_laius, ekraan_pikkus)  # kui suur on aken kus mäng toimub
aken = pygame.display.set_mode(ekraan_suurus,pygame.NOFRAME)
time = 0

# Mõned värvid
must = (0, 0, 0)
valge = (255, 255, 255)

class Objekt:
    def __init__(self, sprite, pos = None, speed = None, width = None, base_speed = None):
        self.speed = speed or [0,0]
        self.pos = pos or [0, 0]
        self.sprite = pygame.image.load("Sprites/"+sprite)
        self.width = width or self.sprite.get_width()
        heightdivwidth = (self.sprite.get_height() / self.sprite.get_width())
        if self.width is not None:
            self.sprite = pygame.transform.scale(self.sprite,(self.width, heightdivwidth*self.width) )
        self.base_speed = base_speed or [0,0]
    def render(self):
        self.pos = [i + j for i, j in zip(self.pos, self.speed)]
        aken.blit(self.sprite, self.pos)
    def __str__(self):
        aken.blit(self.sprite, self.pos)
# pmst kui  callid objekti siis objekt(sprite filei nimi, pos = (X,Y) /
#kiirus, kui suureks teha sprite), ainuke nõutud on sprite file


class Pintsel(Objekt):
    def render(self):
        global speed_length
        mouse_pos = pygame.mouse.get_pos()
        mouse_x = mouse_pos[0]
        mouse_y = mouse_pos[1] -self.sprite.get_height() # selleks, et pintsli vasak alumine äär oleks kursori peal
        speed_x = mouse_x - self.pos[0]
        speed_y = mouse_y - self.pos[1]
        if speed_length  < 20:
            self.pos = [mouse_x, mouse_y]
        else:
            jump_slow = 3.75
            speed_length = math.sqrt(speed_x ** 2 + speed_y ** 2)
            self.speed = (speed_x/jump_slow, speed_y/jump_slow)
        super().render()
#self.speed toimib nii et võtab asukoha kuhu saada tahab ja asukoha, kus on ja leieb nende vektori
#,suunaga sinna poole kuhu saada tahetakse ja jagab selle jump slow-iga

class Värv(Objekt):
    brush = pygame.Surface((10, 10))  #
    brush_positions = []  # List to store all the brush positions drawn

taust = Objekt('background.png', width=ekraan_laius)
mikro = Objekt("mikro_side.png", pos=[100,100], width=100, base_speed=8)
pintsel = Pintsel("pencil.png", width=200 )
# Mängu tsükkel
joonistab = False
while True:
    taust.render()
    mikro.render()
    if joonistab:
        pintsel.render()
        #pygame.draw.circle(aken, must, pintsel.pos, 20)
    #iga kord kui on sündmus
    for event in pygame.event.get():
        #quit event
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()
        #klaviatuuri nupp alla
        elif event.type == pygame.KEYDOWN:
            if event.key in kb.up:
                mikro.speed[1] -= mikro.base_speed
            if event.key in kb.down:
                mikro.speed[1] += mikro.base_speed
            if event.key in kb.left:
                mikro.speed[0] -= mikro.base_speed
            if event.key in kb.right:
                mikro.speed[0] += mikro.base_speed
        #klaviatuuri nupp üles
        elif event.type == pygame.KEYUP:
            if event.key in kb.up:
                mikro.speed[1] += mikro.base_speed
            if event.key in kb.down:
                mikro.speed[1] -= mikro.base_speed
            if event.key in kb.left:
                mikro.speed[0] += mikro.base_speed
            if event.key in kb.right:
                mikro.speed[0] -= mikro.base_speed
        #hiire nupp alla
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_LEFT:
                joonistab = True
                speed_length = float('inf') #lõppmatus
                mouse_x, mouse_y = pygame.mouse.get_pos()
                a = [mouse_x,mouse_y,ekraan_laius-mouse_x,ekraan_pikkus-mouse_y]
                match a.index(min(a)):
                    case 0:
                        pintsel.pos = (-pintsel.sprite.get_width(), mouse_y - pintsel.sprite.get_height())
                    case 1:
                        pintsel.pos = (mouse_x, -pintsel.sprite.get_height())
                    case 2:
                        pintsel.pos = (ekraan_laius + pintsel.sprite.get_width(), mouse_y-pintsel.sprite.get_height())
                    case 3:
                        pintsel.pos = (mouse_x, ekraan_pikkus + pintsel.sprite.get_height())

        #hiire nupp üles
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == pygame.BUTTON_LEFT:
                joonistab = False


    # Uuendame ekraani
    pygame.display.update()
    timer.tick(FPS)