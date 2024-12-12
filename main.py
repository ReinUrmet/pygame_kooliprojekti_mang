import pygame, sys, threading

pygame.init()
pygame.font.init()

# Põhi sätted
font = pygame.font.Font('GOTHIC.ttf', 40)  # valib fondi ja selle suuruse
timer = pygame.time.Clock()
FPS = 60
pygame.display.set_caption("Mäng")

# Ekraan
ekraan_suurus = (1620, 900)  # kui suur on aken kus mäng toimub
aken = pygame.display.set_mode(ekraan_suurus)
time = 0

# Mõned värvid
must = (0, 0, 0)
valge = (255, 255, 255)
punane = (255, 0, 0)

class Objekt:
    def __init__(self, sprite, pos = None, speed = None, scale = None):
        self.speed = speed or [0,0]
        self.pos = pos or [0, 0]
        self.scale = scale
        self.sprite = pygame.image.load(sprite)
        if self.scale is not None:
            self.sprite = pygame.transform.scale(self.sprite, self.scale)
    def render(self):
        self.pos = [i + j for i, j in zip(self.pos, self.speed)]
        aken.blit(self.sprite, self.pos)
    def __str__(self):
        aken.blit(self.sprite, self.pos)



class Pintsel(Objekt):
    def render(self):
        mouse_pos = pygame.mouse.get_pos()
        self.pos = [mouse_pos[0], mouse_pos[1]-self.sprite.get_height()]
        super().render()
class Värv(Objekt):
    brush = pygame.Surface((10, 10))  # Brush size
    brush.fill(punane)  # Color of the brush
    brush_positions = []  # List to store all the brush positions drawn

taust = Objekt('ART/background.jpg')
mikro = Objekt("main_character.png", pos=[100,100], scale=(200,200))
pintsel = Pintsel("placeholder.png", scale=(100,100) )
# Mängu tsükkel
joonistab = False
while True:
    taust.render()
    mikro.render()
    if joonistab:
        pintsel.render()
    #iga kord kui on sündmus
    for event in pygame.event.get():
        #quit event
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()
        #klaviatuuri nupp alla
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                mikro.speed[1] = -5
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                mikro.speed[1] = 5
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                mikro.speed[0] = -5
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                mikro.speed[0] = 5
        #klaviatuuri nupp üles
        elif event.type == pygame.KEYUP:
            if event.key in [pygame.K_UP, pygame.K_w, pygame.K_DOWN, pygame.K_s]:
                mikro.speed[1] = 0
            if event.key in [pygame.K_LEFT, pygame.K_a, pygame.K_RIGHT, pygame.K_d]:
                mikro.speed[0] = 0

        #hiire nupp alla
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_LEFT:
                joonistab = True
        #hiire nupp üles
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == pygame.BUTTON_LEFT:
                joonistab = False

    # Uuendame ekraani
    pygame.display.flip()
    timer.tick(FPS)
