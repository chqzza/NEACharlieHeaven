


from re import S
import pygame, sys, pytmx
from classes import *
from random import randint
import os
pygame.init()

SCREEN = pygame.display.set_mode((1280, 720))


# Fps movement
FPS = 120
clock = pygame.time.Clock()
dt = 0

# Colors
DARK_GRAY = (30, 30, 30)
BUTTON_COLOUR = (50, 50, 80)
SELECTION_COLOUR = (0, 255, 0) 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)



selection_y = 95
selected = 0


play_button = Button((515, 100, 250, 100), BUTTON_COLOUR)

options_button = Button((515, 210, 250, 100), BUTTON_COLOUR)

quit_button = Button((515, 320, 250, 100), BUTTON_COLOUR)

selection_box = pygame.Rect(510, selection_y, 260, 110)

menu_buttons = [play_button, options_button, quit_button]


character_changes = []

for i in range(2):
    for j in range(4):
        character_changes.append(Button((125 + j * 260, 100 + i * 260, 250, 250), BUTTON_COLOUR))
    
options_buttons = [Button((515,100 + i *110, 250, 100),BUTTON_COLOUR ) for i in range(4) ]



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
font = get_font(40)

def draw_health_bar(surface, x, y, current_health, max_health):
    bar_width = 250
    bar_height = 30
    fill = (current_health / max_health) * bar_width
    outline_rect = pygame.Rect(x, y, bar_width, bar_height)
    fill_rect = pygame.Rect(x, y, fill, bar_height)
    pygame.draw.rect(surface, (0, 255, 0), fill_rect)
    pygame.draw.rect(surface, WHITE, outline_rect, 2)



def handle_menu():
    if selected == 0:

        play()
    elif selected == 1:
        options()
    elif selected == 2:
        pygame.quit()
        sys.exit()





def play():
    clock.tick(FPS)
    px, py = 0,0
    pygame.display.set_caption("Play")
    running = True
    cycle = 0
    delay = 0
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

        # only cycle when moving    
        if px == player.x and py == player.y:
            player.draw(SCREEN, 1)
        else:
            player.draw(SCREEN, cycle)


        for enemy in enemies:
            enemy.track(player, dt, enemies)
            if enemy.tracking:

                enemy.draw(SCREEN,cycle)
            else:
                enemy.draw(SCREEN,1)


        if cycle <2:
            if delay < 20:
                delay+=1
            if delay >= 20:
                cycle +=1
                delay = 0
        else: 
            cycle = 0
         
             
        px, py = player.x, player.y


        

        pygame.display.flip()
    pass


### ~~~~ CHARACTER LIST - DISPLAY ALL IN MALE, FEMALE, XMAS and OTHER ~~~~ ###
## displays 8 squares at a time - needs to scroll through them all - total of  ~ 100 ##

def char_select_box(direction, char_box):
    if direction == 1 and char_box.y > 95:
        char_box.y -= 260
    elif direction == 2 and char_box.x < 900:
        char_box.x += 260
    elif direction == 3 and char_box.y < 355:
        char_box.y += 260
    elif direction == 4 and char_box.x > 120:
        char_box.x -= 260

    return char_box



def character_select():
    running = True
    char_box = pygame.Rect(120, 95, 260, 260)
    while running:
        pygame.display.set_caption("Character Select")      
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_w:
                    char_box = char_select_box(1, char_box)

                elif event.key == pygame.K_d:
                     char_box = char_select_box(2, char_box)

                elif event.key == pygame.K_s:
                    char_box = char_select_box(3, char_box)

                elif event.key == pygame.K_a:
                    char_box = char_select_box(4, char_box)

                elif event.key == pygame.K_SPACE:
                    pass

        SCREEN.fill(DARK_GRAY)
        pygame.draw.rect(SCREEN, RED, char_box)
        draw_buttons(SCREEN, character_changes)

        text = font.render("Character Select - Press ESC to return to menu", True, WHITE)
        text_rect = text.get_rect(center=(640, 20))

        SCREEN.blit(text, text_rect)

        pygame.display.flip()


def handle_options():
    if selected == 0:
        character_select()




def options():
    pygame.display.set_caption("Options")
    running = True


    while running:
        pygame.display.set_caption("Options")
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
                    handle_options()

        SCREEN.fill(DARK_GRAY)

        text = font.render("Options Screen - Press ESC to return to menu", True, WHITE)

        text_rect = text.get_rect(center=(640, 20))
        SCREEN.blit(text, text_rect)
        pygame.draw.rect(SCREEN, SELECTION_COLOUR, selection_box)
        draw_buttons(SCREEN, options_buttons)





        pygame.display.flip()


def main_menu():
    pygame.display.set_caption("Main Menu")
    running = True
    
    while running:
        pygame.display.set_caption("Main Menu")      
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
                    handle_menu()

        SCREEN.fill(DARK_GRAY)
        pygame.draw.rect(SCREEN, SELECTION_COLOUR, selection_box)
        draw_buttons(SCREEN, menu_buttons)

        # Draw button text


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

        text = font.render("Press Space to start", True, WHITE)
        text_rect = text.get_rect(center=(640, 360))
        SCREEN.blit(text, text_rect)
        pygame.display.flip()

start_screen()



player = Player("Player", 640, 360,  100, 10, 5, 250, "Assets/characters/Male/Male 07-2.png")
enemies = []
files = [f for f in os.listdir('Assets/characters/Enemy') if f.endswith(".png")]

for i in range (len(files)-1):
    files[i] = 'Assets\characters\Enemy/' + files[i]


for i in range(1):
    enemy = Enemy(f"Enemy {i+1}", randint(0,1280), randint(0,720), 50, 5, 2, 200,random.choice(files))
    enemies.append(enemy)


characters = [player, enemies]    


main_menu()