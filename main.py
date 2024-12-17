import pygame, sys, threading, math
from pygame.transform import scale
import functions_values as fv
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
    def __init__(self, sprite = None, pos = None, speed = None, width = None, base_speed = None):
        self.speed = speed or [0,0]
        self.pos = pos or [0, 0]
        self.width = width or self.sprite.get_width()
        self.change_sprite(sprite)
        self.base_speed = base_speed or [0,0]
    def render(self):
        self.pos = [i + j for i, j in zip(self.pos, self.speed)]
        aken.blit(self.sprite, self.pos)
    def change_sprite(self, sprite = None):
        sprite = sprite or "placeholder.png"
        self.sprite = pygame.image.load("Sprites/"+sprite)
        heightdivwidth = (self.sprite.get_height() / self.sprite.get_width())
        if self.width is not None:
            self.sprite = pygame.transform.scale(self.sprite,(self.width, heightdivwidth*self.width))
    def flip_sprite(self):
        self.sprite = pygame.transform.flip(self.sprite, True, False)
# pmst kui  callid objekti siis objekt(sprite filei nimi, pos = (X,Y) /
#kiirus, kui suureks teha sprite), ainuke nõutud on sprite file


class Pintsel(Objekt):
    #Sellega salvestan kirjutatud line
    def __init__(self, sprite, width):
        super().__init__(sprite, width=width)
        self.lines = [] 

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
            speed_length =fv.get_vector_length([speed_x,speed_y])
            self.speed = (speed_x/jump_slow, speed_y/jump_slow)
        
        #Siin salvestan line ainult kui joonistab:
        if joonistab:
            if len(self.lines) > 0:
                self.lines[-1].append((mouse_x, mouse_y))              
            else:
                self.lines.append([(mouse_x, mouse_y)])
        super().render()


        #Seda on vaja et kontrollida kas see joonistatud joon lõikab mõndasi vastaseid
        for line in self.lines:
            for vastane in to_render:  # Check all enemies (if they are in `to_render`)
                split_enemies = lõhesta_sprite_joonel(vastane, line)
                if split_enemies != [vastane]:  # If enemies were split
                    to_render.remove(vastane)
                    to_render.extend(split_enemies)  # Add the new split enemies to the rendering list

#self.speed toimib nii et võtab asukoha kuhu saada tahab ja asukoha, kus on ja leieb nende vektori
#,suunaga sinna poole kuhu saada tahetakse ja jagab selle jump slow-iga


class Värv(Objekt):
    def __init__(self, sprite, pos):
        self.sprite = sprite
        self.pos = pos
        self.speed = [0,0]

# Simple test enemy class
class Vastane(Objekt):
    def __init__(self, sprite, pos, speed=None, width=None):
        super().__init__(sprite, pos=pos, speed=speed, width=width)
        self.width = width or self.sprite.get_width()
        self.pos = pos

    # Optional: You can add movement or behavior to this test enemy

    def render(self):
        aken.blit(self.sprite, self.pos)# Move vertically



#Mõned funktsioonid

# Kontrollib, kas joon lõikab rect'i
#rect on pygames kasutatav objekt mida kasutatakse objekti suuruse ja positsiooni määramiseks
def joon_lõikab_recti(line, rect):
    for i in range(len(line) - 1):
        if rect.clipline(line[i], line[i + 1]):
            return True
    return False

# Lõhub vastase sprite'i kaheks pooleks
def lõhesta_sprite_joonel(vastane, joon):
    vastane_rect = vastane.sprite.get_rect(topleft=vastane.pos)

    if len(joon) == 2 and isinstance(joon[0], tuple) and isinstance(joon[1], tuple):
        x1, y1 = joon[0]
        x2, y2 = joon[1]

        
        if vastane_rect.clipline(x1, y1, x2, y2):
            
            radius = vastane.sprite.get_width() // 2 
            
            ball1_pos = [vastane.pos[0], vastane.pos[1]]
            ball2_pos = [vastane.pos[0] + radius, vastane.pos[1]]

           
            ball1 = Vastane("placeholder.png", pos=ball1_pos, width=radius * 2)  # Red ball 1
            ball2 = Vastane("placeholder.png", pos=ball2_pos, width=radius * 2)  # Red ball 2

            
            ball1.sprite.fill((255, 0, 0))  
            ball2.sprite.fill((255, 0, 0))  

            return [ball1, ball2]  
    
    return [vastane]


taust = Objekt('background.png', width=ekraan_laius)
mikro = Objekt("mikro_left.png", [100,300], width=100, base_speed=8)
pintsel = Pintsel("pencil.png", width=200 )
to_render = []
vastane = Vastane("man_shoot.png", pos=[500, 300], speed=[-2.5, 0], width=100)
to_render.append(vastane)



# Mängu tsükkel
joonistab = False
strokes = []
walk_change, brush_size,brush_size2,last_pos = 0,0,0,None

while True:
    time +=1
    #TODO: liigutada see vastasesse või objekti
    if time == 120:
        vastane.speed = [0,0]

    taust.render()
    to_render.append(vastane)
    to_render.append(mikro)

    #Vastase kõndimis animatsioon
    if abs(vastane.speed[0]) > 0:
        walk_change += 1
        if walk_change > 10:
            vastane.change_sprite('man_side2.png')
        else:
            vastane.change_sprite('man_side.png')
        if walk_change > 20:
            walk_change = 0
    else:
        vastane.change_sprite('man_shoot.png')



    if joonistab:
        pintsel.render()

        brush_size = int(brush_size2)
        if brush_size < 5:
            brush_size2 += 0.5
        if alpha < 100:
            alpha += 10
        image = fv.pencil_sprite(brush_size, brush_size)
        #image = pygame.transform.scale(pygame.image.load("Sprites/draw_alpha3.png"), (brush_size, brush_size)).set_alpha(alpha)

        mouse_pos = pygame.mouse.get_pos()
        if last_pos:
            vektor = [i - j for i, j in zip(mouse_pos, last_pos)]
            vektor_length = fv.get_vector_length(vektor)
            spaces = max(1, int(vektor_length / brush_size*3))

            for space in range(1, spaces + 1):
                factor = space / spaces
                new_pos = [lp + v * factor for lp, v in zip(last_pos, vektor)]
                strokes.append(Värv(image, new_pos))

        last_pos = mouse_pos

    fv.big_render(to_render)
    for stroke in strokes:
        stroke.render()
    to_render = []

    #Iga kord kui on sündmus

    # Kontrollin kas pintsel lõikab vastaseid
    for joon in pintsel.lines:
        for vastane in to_render: 
            split_enemies = lõhesta_sprite_joonel(vastane, joon)
            if split_enemies != [vastane]: 
                to_render.remove(vastane) 
                to_render.extend(split_enemies)
                #Ei tööta
                print("Lõikas")

    for event in pygame.event.get():
        #quit event
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()
        #klaviatuuri nupp alla
        elif event.type == pygame.KEYDOWN:
            #TODO: sptiteide vahetamiseks võiks objekt files mingi funktsiooni teha
            if event.key in fv.up:
                mikro.change_sprite("mikro_away.png")
                mikro.speed[1] -= mikro.base_speed
            if event.key in fv.down:
                mikro.change_sprite("mikro_forward.png")
                mikro.speed[1] += mikro.base_speed
            if event.key in fv.left:
                mikro.change_sprite("mikro_left.png")
                mikro.speed[0] -= mikro.base_speed
            if event.key in fv.right:
                mikro.change_sprite("mikro_right.png")
                mikro.speed[0] += mikro.base_speed
        #klaviatuuri nupp üles
        elif event.type == pygame.KEYUP:
            if event.key in fv.up:
                mikro.speed[1] += mikro.base_speed
            if event.key in fv.down:
                mikro.speed[1] -= mikro.base_speed
            if event.key in fv.left:
                mikro.speed[0] += mikro.base_speed
            if event.key in fv.right:
                mikro.speed[0] -= mikro.base_speed
        #hiire nupp alla
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_LEFT:
                joonistab = True
                brush_size2, alpha, last_pos = 1, 0, None
                speed_length = float('inf')  # Resetting the drawing state
                mouse_x, mouse_y = pygame.mouse.get_pos()

                # Handle the pencil positioning logic based on the mouse position
                a = [mouse_x, mouse_y, ekraan_laius - mouse_x, ekraan_pikkus - mouse_y]
                match a.index(min(a)):
                    case 0:
                        pintsel.pos = (-pintsel.sprite.get_width(), mouse_y - pintsel.sprite.get_height())
                    case 1:
                        pintsel.pos = (mouse_x, -pintsel.sprite.get_height())
                    case 2:
                        pintsel.pos = (ekraan_laius + pintsel.sprite.get_width(), mouse_y - pintsel.sprite.get_height())
                    case 3:
                        pintsel.pos = (mouse_x, ekraan_pikkus + pintsel.sprite.get_height())

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == pygame.BUTTON_LEFT:
                joonistab = False  # End drawing when mouse button is released

    # Uuendame ekraani
    pygame.display.update()
    timer.tick(FPS)