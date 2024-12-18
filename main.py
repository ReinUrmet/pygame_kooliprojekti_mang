import pygame
import sys
import math
from pygame.transform import scale
import functions_values as fv
from object import Objekt
from enemy import Enemy
from Pintsel_Värv import Pintsel, Värv
from main_menu import main_menu

pygame.init()
pygame.font.init()

# Põhi sätted
font = pygame.font.Font('GOTHIC.ttf', 40)  # valib fondi ja selle suuruse
timer = pygame.time.Clock()
FPS = 60
pygame.display.set_caption("Mäng")

# Ekraan
ekraan_laius, ekraan_pikkus = 880, 700
ekraan_suurus = (ekraan_laius, ekraan_pikkus)  # kui suur on aken kus mäng toimub
aken = pygame.display.set_mode(ekraan_suurus, pygame.NOFRAME)
time = 0

# Mõned värvid
must = (0, 0, 0)
valge = (255, 255, 255)
roheline = (0, 255, 0)
punane = (255, 0, 0)

# Põhimenüü käivitamine
action = main_menu(aken)
if action == "start_game":
    print("Mäng algab!")
else:
    pygame.quit()
    sys.exit()

# Mängu objektid
taust = Objekt('background.png', width=ekraan_laius)
mikro = Objekt("mikro_left.png", [100, 300], width=100, base_speed=8)
pintsel = Pintsel("pencil.png", width=200)
vastane = Enemy(700, 300, 100, 200, (255, 0, 0), [500, 300], screen=aken)

# Player Health
player_health = 100

# Mängu tsükkel
joonistab = False
strokes = []
walk_change, brush_size, brush_size2, last_pos = 0, 0, 0, None
to_render = []
alpha = 0  
speed_length = float('inf')

while True:
    time += 1
    taust.render()
    to_render.append(mikro)

    # Update and render the enemy
    if vastane:
        if vastane.update(mikro.pos, ekraan_laius, ekraan_pikkus):  # If update returns True, remove enemy
            vastane = None
        else:
            vastane.render()

    if joonistab:
        pintsel.render()

        brush_size = int(brush_size2)
        if brush_size < 5:
            brush_size2 += 0.5
        if alpha < 100:
            alpha += 10
        image = fv.pencil_sprite(brush_size, brush_size)
        mouse_pos = pygame.mouse.get_pos()
        if last_pos:
            vektor = [i - j for i, j in zip(mouse_pos, last_pos)]
            vektor_length = fv.get_vector_length(vektor)
            spaces = max(1, int(vektor_length / brush_size * 3))

            for space in range(1, spaces + 1):
                factor = space / spaces
                new_pos = [lp + v * factor for lp, v in zip(last_pos, vektor)]
                strokes.append(Värv(image, new_pos))

        last_pos = mouse_pos

    fv.big_render(to_render)

    # Render bullets and check for collisions with the player
    if vastane:
        for bullet in vastane.bullets:
            bullet.move()
            bullet.render(aken)
            if bullet.rect.colliderect(pygame.Rect(mikro.pos[0], mikro.pos[1], mikro.width, mikro.width)):
                player_health -= 10
                vastane.bullets.remove(bullet)
                print(f"Mikro tervis: {player_health}")
                if player_health <= 0:
                    print("Mäng läbi!")
                    pygame.quit()
                    sys.exit()

    for stroke in strokes:
        stroke.render()
    to_render = []

    # iga kord kui on sündmus
    for event in pygame.event.get():
        # quit event
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()

        if event.type == pygame.USEREVENT:  # Resume movement after shooting
            if vastane:
                vastane.handle_shoot_event()

        # klaviatuuri nupp alla
        elif event.type == pygame.KEYDOWN:
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

        # klaviatuuri nupp üles
        elif event.type == pygame.KEYUP:
            if event.key in fv.up:
                mikro.speed[1] += mikro.base_speed
            if event.key in fv.down:
                mikro.speed[1] -= mikro.base_speed
            if event.key in fv.left:
                mikro.speed[0] += mikro.base_speed
            if event.key in fv.right:
                mikro.speed[0] -= mikro.base_speed

        # hiire nupp alla
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_LEFT:
                joonistab = True
                brush_size2, alpha, last_pos = 1, 0, None
                speed_length = float('inf')  # lõppmatus
                mouse_x, mouse_y = pygame.mouse.get_pos()
                last_pos = pygame.mouse.get_pos()
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

        # hiire nupp üles
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == pygame.BUTTON_LEFT:
                joonistab = False

                collided = False
                for stroke in strokes:
                    stroke_rect = pygame.Rect(stroke.pos[0], stroke.pos[1], brush_size, brush_size)
                    if vastane and vastane.rect.colliderect(stroke_rect):
                        collided = True
                        break  

                if collided:  # Only process direction if there is a collision
                    direction = vastane.calculate_direction(strokes)
                    print(f"Cut direction: {direction}")  # Debugging

                    if direction:
                        vastane.play_animation(direction)  # Change appearance based on the direction

                strokes = []

    # Uuendame ekraani
    pygame.display.update()
    timer.tick(FPS)