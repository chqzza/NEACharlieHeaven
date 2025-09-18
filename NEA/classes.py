from calendar import c
from msvcrt import kbhit
from tkinter import SE
import pygame, math


class Button:
    def __init__(self, rect, colour):
        self.rect = rect
        self.colour = colour
        self.pygame_rect = pygame.Rect(rect)
    
    def draw(self, surface):
        pygame.draw.rect(surface, self.colour, self.rect)



class Character:
    def __init__(self, name , x, y, hp_max, attack, defence, speed, colour):
        self.name = name
        self.x = x
        self.y = y
        self.hp_max = hp_max
        self.hp = hp_max
        self.attack = attack
        self.defence = defence
        self.speed = speed
        self.colour = colour
        self.direction = 'up'


    def directional_check(self):
        direction = self.direction
        if direction == 'up':
            self.colour = (0,255,0)
        elif direction == 'down':
            self.colour = (255,0,0)
        elif direction == 'left':
            self.colour = (0,0,255)
        elif direction == 'right':
            self.colour = (255,255,0)

    def draw(self, surface):
        self.directional_check()
        pygame.draw.circle(surface, (0,0,0), (int(self.x), int(self.y)), 12)
        pygame.draw.circle(surface, self.colour, (int(self.x), int(self.y)), 10)


class Player(Character):
    def __init__(self,*args):
        super().__init__(*args)
        self.inventory = []
        self.equipped_items = []
        self.gold = 0
        self.level = 1
        self.experience = 0

    def move(self, dt, k):


        #normalising movement so diagonal isnt faster
        if (k[pygame.K_w] or k[pygame.K_s]) and (k[pygame.K_a] or k[pygame.K_d]):
            self.speed = 180
        else:
                self.speed = 250
        
        if k[pygame.K_w] and self.y > 5:
            self.y -= self.speed * dt
            self.direction = 'up'

        if k[pygame.K_s] and self.y < 715:
            self.y += self.speed * dt
            self.direction = 'down'

        if k[pygame.K_a] and self.x > 5:
            self.x -= self.speed * dt
            self.direction = 'left'   

        if k[pygame.K_d] and self.x < 1275:
            self.x += self.speed * dt
            self.direction = 'right'

       #code for a dash that triggers for a second when left shift is 
        if k[pygame.K_LSHIFT]:
            if self.direction == 'up' and self.y > 20:
                self.y -= self.speed * 2 * dt
            if self.direction == 'down' and self.y < 700:
                self.y += self.speed * 2 * dt
            if self.direction == 'left' and self.x > 20:
                self.x -= self.speed * 2 * dt
            if self.direction == 'right' and self.x < 1260:
                self.x += self.speed * 2 * dt


    def weapon_rotate(self, SCREEN):
        #Make code that rotates about the player in a circle 
        weapon_x, weapon_y = self.x, self.y -6
        weapon = (weapon_x, weapon_y, 40,10)
        pygame.draw.rect(SCREEN, (255,0,0), weapon)

    def meelee(self, k, SCREEN):
        if k[pygame.K_SPACE]:
            pygame.draw.circle(SCREEN, (255,255,0), (int(self.x), int(self.y)), 20, 2)
            self.weapon_rotate(SCREEN)

    



class Enemy(Character):
    def __init__(self,*args):
        super().__init__(*args)



    def track(self, tracking, dt, enemies):
        dx = tracking.x - self.x
        dy = tracking.y - self.y
        distance_squared = dx**2 + dy**2
        distance = distance_squared ** 0.5

        if 25 < distance < 400:
            # Normalize direction to player
            nx = dx / distance
            ny = dy / distance

            # --- Avoid other enemies ---
            sep_x, sep_y = 0, 0
            for other in enemies:
                if other is self:
                    continue
                ox = self.x - other.x
                oy = self.y - other.y
                dist2 = ox**2 + oy**2
                if dist2 < 80**2:  # 40 px "personal space"
                    dist = dist2 ** 0.5
                    # Push away more strongly the closer they are
                    sep_x += ox / dist
                    sep_y += oy / dist

            # Combine seek + separation
            move_x = nx + sep_x
            move_y = ny + sep_y

            # Normalize combined vector
            mag = (move_x**2 + move_y**2) ** 0.5
            if mag > 0:
                move_x /= mag
                move_y /= mag

            # Apply movement
            self.x += move_x * self.speed * dt
            self.y += move_y * self.speed * dt
        else:
            return False