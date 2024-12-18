import pygame
import sys
import random
import math
from pygame.transform import scale
import functions_values as fv
from object import Objekt
from enemy import Enemy
from Pintsel_Värv import Pintsel, Värv
from main_menu import main_menu

pygame.init()
pygame.font.init()

# Lisab taustamuusika
pygame.mixer.init()
pygame.mixer.music.load('fun-retro-game-175468.mp3')  # Asenda faili nimi oma muusikafailiga
pygame.mixer.music.set_volume(0.5)  # Seab helitugevuse
pygame.mixer.music.play(-1)  # Mängib taustamuusikat lõputult

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

def start_screen(aken):
    """Kuvab algusekraani, kust mängu saab alustada."""
    start_font = pygame.font.Font('GOTHIC.ttf', 60)
    button_font = pygame.font.Font('GOTHIC.ttf', 40)

    # Määrab värvid
    black = (0, 0, 0)
    white = (255, 255, 255)
    blue = (0, 0, 255)

    # Joonistab tausta
    aken.fill(black)

    # Kuvab "Start Game" teksti
    start_text = start_font.render("START GAME", True, blue)
    start_rect = start_text.get_rect(center=(ekraan_laius // 2, ekraan_pikkus // 3))
    aken.blit(start_text, start_rect)

    # Loob nupu
    button_text = button_font.render("PLAY", True, white)
    button_rect = button_text.get_rect(center=(ekraan_laius // 2, ekraan_pikkus // 2))
    pygame.draw.rect(aken, blue, button_rect.inflate(20, 10), border_radius=10)
    aken.blit(button_text, button_rect)

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    return "start_game"

def pause_menu(aken):
    """Kuvab pausimenüü koos "Resume", "Quit" ja helinuppudega."""
    pause_font = pygame.font.Font('GOTHIC.ttf', 60)
    button_font = pygame.font.Font('GOTHIC.ttf', 40)

    # Määrab värvid
    black = (0, 0, 0)
    white = (255, 255, 255)
    gray = (100, 100, 100)

    # Loob osaliselt läbipaistva tausta
    overlay = pygame.Surface((ekraan_laius, ekraan_pikkus))
    overlay.set_alpha(200)
    overlay.fill(black)
    aken.blit(overlay, (0, 0))

    # Kuvab "Paused" teksti
    pause_text = pause_font.render("PAUSED", True, gray)
    pause_rect = pause_text.get_rect(center=(ekraan_laius // 2, ekraan_pikkus // 3))
    aken.blit(pause_text, pause_rect)

    # Loob nupud
    resume_text = button_font.render("RESUME", True, white)
    resume_rect = resume_text.get_rect(center=(ekraan_laius // 2, ekraan_pikkus // 2 - 50))
    pygame.draw.rect(aken, gray, resume_rect.inflate(20, 10), border_radius=10)
    aken.blit(resume_text, resume_rect)

    quit_text = button_font.render("QUIT", True, white)
    quit_rect = quit_text.get_rect(center=(ekraan_laius // 2, ekraan_pikkus // 2 + 50))
    pygame.draw.rect(aken, gray, quit_rect.inflate(20, 10), border_radius=10)
    aken.blit(quit_text, quit_rect)

    def draw_mute_button():
        """Draw the mute/unmute button and return its rect."""
        mute_text = button_font.render(
            "MUTE", True, white) if pygame.mixer.music.get_volume() > 0 else button_font.render("UNMUTE", True, white)
        mute_rect = mute_text.get_rect(topleft=(20, 20))
        pygame.draw.rect(aken, gray, mute_rect.inflate(20, 10), border_radius=10)
        aken.blit(mute_text, mute_rect)
        return mute_rect

    mute_rect = draw_mute_button()
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if resume_rect.collidepoint(event.pos):
                    return "resume"
                elif quit_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
                elif mute_rect.collidepoint(event.pos):
                    # Toggle mute/unmute
                    if pygame.mixer.music.get_volume() > 0:
                        pygame.mixer.music.set_volume(0)
                    else:
                        pygame.mixer.music.set_volume(0.5)
                    mute_rect = draw_mute_button()
                    pygame.display.update()

def game_over_screen(aken):
    """Kuvab kaotuseekraani koos taaskäivitamise nupuga."""
    game_over_font = pygame.font.Font('GOTHIC.ttf', 60)
    button_font = pygame.font.Font('GOTHIC.ttf', 40)

    # Määrab värvid
    black = (0, 0, 0)
    white = (255, 255, 255)
    red = (255, 0, 0)

    # Joonistab tausta
    aken.fill(black)

    # Kuvab "Game Over" teksti
    game_over_text = game_over_font.render("GAME OVER", True, red)
    game_over_rect = game_over_text.get_rect(center=(ekraan_laius // 2, ekraan_pikkus // 3))
    aken.blit(game_over_text, game_over_rect)

    # Loob nupu
    button_text = button_font.render("GO AGAIN", True, white)
    button_rect = button_text.get_rect(center=(ekraan_laius // 2, ekraan_pikkus // 2))
    pygame.draw.rect(aken, red, button_rect.inflate(20, 10), border_radius=10)
    aken.blit(button_text, button_rect)

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    return "restart"

def completion_screen(aken):
    """Kuvab lõpuekraani, kui mäng on võidetud."""
    completion_font = pygame.font.Font('GOTHIC.ttf', 60)
    button_font = pygame.font.Font('GOTHIC.ttf', 40)

    # Määrab värvid
    black = (0, 0, 0)
    white = (255, 255, 255)
    green = (0, 255, 0)

    # Joonistab tausta
    aken.fill(black)

    # Kuvab "You Win" teksti
    win_text = completion_font.render("YOU WIN!", True, green)
    win_rect = win_text.get_rect(center=(ekraan_laius // 2, ekraan_pikkus // 3))
    aken.blit(win_text, win_rect)

    # Loob nupu
    button_text = button_font.render("PLAY AGAIN", True, white)
    button_rect = button_text.get_rect(center=(ekraan_laius // 2, ekraan_pikkus // 2))
    pygame.draw.rect(aken, green, button_rect.inflate(20, 10), border_radius=10)
    aken.blit(button_text, button_rect)

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    return "restart"

# Põhimenüükäivitamine
action = start_screen(aken)
if action == "start_game":
    print("Mäng algab!")
else:
    pygame.quit()
    sys.exit()

# Mängu objektid
taust = Objekt('background.png', width=ekraan_laius)
mikro = Objekt("mikro_left.png", [100, 300], width=100, base_speed=8)
pintsel = Pintsel("pencil.png", width=200)

# Mängija tervis
player_health = 100

# Raundi muutujad
round_number = 1
enemies = []

def initialize_enemies(round_number):
    """Algatab vaenlased praeguseks raundiks."""
    global enemies
    enemies = []  # Nullib vaenlased uueks raundiks
    for i in range(round_number):  # Lisab igas raundis ühe vaenlase rohkem
        x = random.randint(50, ekraan_laius - 50)
        y = random.randint(50, ekraan_pikkus - 50)
        enemies.append(Enemy(x, y, 100, 200, punane, [x, y], screen=aken))

# Algatab esimese raundi vaenlased
initialize_enemies(round_number)

# Mängu tsükkel
joonistab = False
strokes = []
walk_change, brush_size, brush_size2, last_pos = 0, 0, 0, None
to_render = []
alpha = 0  
speed_length = float('inf')

# Fontid loendurite jaoks
counter_font = pygame.font.Font('GOTHIC.ttf', 30)
health_font = pygame.font.Font('GOTHIC.ttf', 30)

while True:
    time += 1
    taust.render()
    to_render.append(mikro)

    # Joonistab raundi loenduri
    round_text = counter_font.render(f"Round: {round_number}", True, must)
    round_rect = round_text.get_rect(center=(ekraan_laius // 2, 30))
    aken.blit(round_text, round_rect)

    # Joonistab tervise loenduri
    health_text = health_font.render(f"Health: {player_health}", True, valge)
    health_outline = health_font.render(f"Health: {player_health}", True, punane)
    health_rect = health_text.get_rect(bottomleft=(20, ekraan_pikkus - 20))
    aken.blit(health_outline, (health_rect.x - 2, health_rect.y - 2))  # Punane ääris
    aken.blit(health_outline, (health_rect.x + 2, health_rect.y - 2))
    aken.blit(health_outline, (health_rect.x - 2, health_rect.y + 2))
    aken.blit(health_outline, (health_rect.x + 2, health_rect.y + 2))
    aken.blit(health_text, health_rect)

    # Uuendab ja joonistab kõik vaenlased
    for vastane in enemies[:]:  # Kasutab nimekirja koopiat ohutuks iteratsiooniks
        if vastane.update(mikro.pos, ekraan_laius, ekraan_pikkus):
            enemies.remove(vastane)
        else:
            vastane.render()

    # Kontrollib, kas kõik vaenlased on alistatud, et järgmisesse raundi liikuda
    if not enemies:
        round_number += 1
        if round_number > 10:  # Lõpetab mängu pärast 10 raundi
            result = completion_screen(aken)
            if result == "restart":
                player_health = 100
                round_number = 1
                initialize_enemies(round_number)
                continue
            else:
                pygame.quit()
                sys.exit()
        else:
            print(f"Round {round_number}")
            initialize_enemies(round_number)

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


    # Joonistab kuule ja kontrollib kokkupõrkeid mängijaga
    for vastane in enemies:
        for bullet in vastane.bullets:
            bullet.move()
            bullet.render(aken)
            if bullet.rect.colliderect(pygame.Rect(mikro.pos[0], mikro.pos[1], mikro.width, mikro.width)):
                player_health -= 10
                vastane.bullets.remove(bullet)
                print(f"Mikro tervis: {player_health}")
                if player_health <= 0:
                    result = game_over_screen(aken)
                    if result == "restart":
                        player_health = 100
                        round_number = 1
                        initialize_enemies(round_number)
                        continue

    for stroke in strokes:
        stroke.render()
    to_render = []

    # Iga kord, kui toimub sündmus
    for event in pygame.event.get():
        # Pausimenüüa avamine
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            result = pause_menu(aken)
            if result == "resume":
                continue

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.USEREVENT:  # Taastab liikumise pärast tulistamist
            for vastane in enemies:
                vastane.handle_shoot_event()

        # Klaviatuuri nupp alla
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

        # Klaviatuuri nupp üles
        elif event.type == pygame.KEYUP:
            if event.key in fv.up:
                mikro.speed[1] += mikro.base_speed
            if event.key in fv.down:
                mikro.speed[1] -= mikro.base_speed
            if event.key in fv.left:
                mikro.speed[0] += mikro.base_speed
            if event.key in fv.right:
                mikro.speed[0] -= mikro.base_speed

        # Klaviatuuri nupp üles
        elif event.type == pygame.KEYUP:
            if event.key in fv.up:
                mikro.speed[1] += mikro.base_speed
            if event.key in fv.down:
                mikro.speed[1] -= mikro.base_speed
            if event.key in fv.left:
                mikro.speed[0] += mikro.base_speed
            if event.key in fv.right:
                mikro.speed[0] -= mikro.base_speed

        # Hiire nupp alla
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_LEFT:
                joonistab = True
                brush_size2, alpha, last_pos = 1, 0, None
                speed_length = float('inf')  # Lõppmatus
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

        # Hiire nupp üles
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == pygame.BUTTON_LEFT:
                joonistab = False

                collided = False
                for stroke in strokes:
                    stroke_rect = pygame.Rect(stroke.pos[0], stroke.pos[1], brush_size, brush_size)
                    for vastane in enemies:
                        if vastane.rect.colliderect(stroke_rect):
                            collided = True
                            break

                if collided:  # Kontrollib suunda ainult kokkupõrke korral
                    direction = vastane.calculate_direction(strokes)
                    print(f"Cut direction: {direction}")  # Silumine

                    if direction:
                        vastane.play_animation(direction)  # Muudab välimust vastavalt suunale

                strokes = []

    # Uuendame ekraani
    pygame.display.update()
    timer.tick(FPS)
