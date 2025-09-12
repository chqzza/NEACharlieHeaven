


from re import S
import pygame, sys, pytmx
from classes import *
pygame.init()

SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("NEA")

# Fps movement
FPS = 120
clock = pygame.time.Clock()
dt = 0

# Colors
DARK_GRAY = (30, 30, 30)
BUTTON_COLOR = (50, 50, 80)
SELECTION_COLOR = (0, 255, 0) 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)




selection_y = 95
selected = 0


play_button = Button((515, 100, 250, 100), BUTTON_COLOR)

options_button = Button((515, 210, 250, 100), BUTTON_COLOR)

quit_button = Button((515, 320, 250, 100), BUTTON_COLOR)

selection_box = pygame.Rect(510, selection_y, 260, 110)

menu_buttons = [play_button, options_button, quit_button]

def selection_up():
    global selection_y
    global selection_box
    global selected 
    if selection_y > 95:
        selection_y -= 110
    selection_box = pygame.Rect(510, selection_y, 260, 110)
    selected -= 1

def selection_down():
    global selection_y
    global selection_box
    global selected
    if selection_y < 320:
        selection_y += 110
    selection_box = pygame.Rect(510, selection_y, 260, 110)
    selected += 1

def draw_buttons(surface, buttons_list):
     for button in buttons_list:
            button.draw(SCREEN)

def get_font(size):
    return pygame.font.Font("assets/fonts/path.ttf", size)


def draw_health_bar(surface, x, y, current_health, max_health):
    bar_width = 250
    bar_height = 30
    fill = (current_health / max_health) * bar_width
    outline_rect = pygame.Rect(x, y, bar_width, bar_height)
    fill_rect = pygame.Rect(x, y, fill, bar_height)
    pygame.draw.rect(surface, (0, 255, 0), fill_rect)
    pygame.draw.rect(surface, WHITE, outline_rect, 2)

def handle_menu(num):
    if selected == 0:

        play()
    elif selected == 1:
        options()
    elif selected == 2:
        pygame.quit()
        sys.exit()




player = Player("Player", 640, 360,  100, 10, 5, 250, (14,60,190))

practice_enemy = Enemy("Practice Enemy", 100, 100, 50, 5, 2, 200,(255,0,0))

characters = [player, practice_enemy]    


def play():
    clock.tick(FPS)

    pygame.display.set_caption("Play")
    running = True
    while running:
        SCREEN.fill(DARK_GRAY)
        for event in pygame.event.get():
             if event.type == pygame.QUIT:
                running = False
             if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        draw_health_bar(SCREEN, 1020, 10, player.hp, player.hp_max)
        dt = clock.tick(FPS) / 1000


        k = pygame.key.get_pressed()
        player.move(dt ,k)
        player.meelee(k, SCREEN)
        practice_enemy.track(player, dt)


        for character in characters:
         
             character.draw(SCREEN)
             



        

        pygame.display.flip()




def options():
    pygame.display.set_caption("Options")
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        SCREEN.fill(DARK_GRAY)
        font = get_font(40)
        text = font.render("Options Screen - Press ESC to return to menu", True, WHITE)
        text_rect = text.get_rect(center=(640, 360))
        SCREEN.blit(text, text_rect)
        pygame.display.flip()


def main_menu():
    pygame.display.set_caption("Main Menu")
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_s:
                     selection_down()


                elif event.key == pygame.K_w:
                     selection_up()


                elif event.key == pygame.K_SPACE:
                    handle_menu(selected)

        SCREEN.fill(DARK_GRAY)
        pygame.draw.rect(SCREEN, SELECTION_COLOR, selection_box)
        draw_buttons(SCREEN, menu_buttons)

        # Draw button text
        font = get_font(40)

        play_text = font.render("Play", True, WHITE)
        options_text = font.render("Options", True, WHITE)
        quit_text = font.render("Quit", True, WHITE)
        SCREEN.blit(play_text, play_text.get_rect(center=play_button.pygame_rect.center))
        SCREEN.blit(options_text, options_text.get_rect(center=options_button.pygame_rect.center))
        SCREEN.blit(quit_text, quit_text.get_rect(center=quit_button.pygame_rect.center))


        pygame.display.flip()
    pygame.quit()
    sys.exit()


def start_screen():
    pygame.display.set_caption("Start Screen")
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running = False
        SCREEN.fill(DARK_GRAY)
        font = get_font(40)
        text = font.render("Press Space to start", True, WHITE)
        text_rect = text.get_rect(center=(640, 360))
        SCREEN.blit(text, text_rect)
        pygame.display.flip()
start_screen()
main_menu()
