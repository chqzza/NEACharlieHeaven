import pygame


class Button:
    def __init__(self, rect, colour):
        self.rect = rect
        self.colour = colour
        self.pygame_rect = pygame.Rect(rect)
    
    def draw(self, surface):
        pygame.draw.rect(surface, self.colour, self.rect)



class Character:
    def __init__(self, name , x, y, hp, attack, defence, speed, colour):
        self.name = name
        self.x = x
        self.y = y
        self.hp = hp
        self.attack = attack
        self.defence = defence
        self.speed = speed
        self.colour = colour
    def draw(self, surface):
        # Placeholder for drawing the character
        pygame.draw.circle(surface, self.colour, (int(self.x), int(self.y)), 10)

class Player(Character):
    def __init__(self, name, x, y, hp, attack, defence, speed, colour):
        super().__init__(name, x, y, hp, attack, defence, speed, colour)
        self.inventory = []
        self.equipped_items = []
        self.gold = 0
        self.level = 1
        self.experience = 0
    def move(self, dt, k):


        if k[pygame.K_w]:
            self.y -= self.speed * dt
        if k[pygame.K_s]:
            self.y += self.speed * dt
        if k[pygame.K_a]:
            self.x -= self.speed * dt
        if k[pygame.K_d]:
            self.x += self.speed * dt



class Enemy(Character):
    def __init__(self, name, x, y, hp, attack, defence, speed, colour):
        super().__init__(name, x, y, hp, attack, defence, speed, colour)


    def track(self, tracking, dt):
        dx = tracking.x - self.x
        dy = tracking.y - self.y
        distance_squared = dx**2 + dy**2
        distance = distance_squared ** 0.5

        if distance < 400 and distance > 0:  
            nx = dx / distance
            ny = dy / distance

            self.x += nx * self.speed * dt
            self.y += ny * self.speed * dt
        else:
            return False