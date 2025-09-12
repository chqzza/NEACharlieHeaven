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
    def draw(self, surface):
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


        if k[pygame.K_w] and self.y > 5:
            self.y -= self.speed * dt
        if k[pygame.K_s] and self.y < 715:
            self.y += self.speed * dt
        if k[pygame.K_a] and self.x > 5:
            self.x -= self.speed * dt
        if k[pygame.K_d] and self.x < 1275:
            self.x += self.speed * dt


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



    def track(self, tracking, dt):
        dx = tracking.x - self.x
        dy = tracking.y - self.y
        distance_squared = dx**2 + dy**2
        distance = distance_squared ** 0.5 

        if distance < 400 and distance > 25:  
            nx = dx / distance
            ny = dy / distance

            self.x += nx * self.speed * dt
            self.y += ny * self.speed * dt
        else:
            return False
