
from calendar import c
import pygame, math
import random





class Button:
    def __init__(self, rect, colour):
        self.rect = rect
        self.colour = colour
        self.pygame_rect = pygame.Rect(rect)
    
    def draw(self, surface):
        pygame.draw.rect(surface, self.colour, self.rect)



class Character:
    def __init__(self, name , x, y, hp_max, attack, defence, speed, spritesheet):
        self.name = name
        self.x = x
        self.y = y
        self.hp_max = hp_max
        self.hp = hp_max
        self.attack = attack
        self.defence = defence
        self.speed = speed
        self.spritesheet = spritesheet
        self.direction = 'up'
        self.speed_diagonal = speed / math.sqrt(2)
        self.frames = self.animation()


    def animation(self):
        sheet = pygame.image.load(self.spritesheet).convert_alpha()
        frames = [[],[],[],[]]

        for i in range (4):
            for j in range(3):
                frame = sheet.subsurface(pygame.Rect(j*32, i*32, 32, 32))
                frame = pygame.transform.scale(frame, (64, 64))
                frames[i].append(frame)

        return frames
        


    def directional_check(self):
            direction = self.direction
            if direction == 'up':
                return 3
            elif direction == 'down':
                return 0 
            elif direction == 'left':
                return 1 
            elif direction == 'right':
                return 2

    def draw(self, surface, cycle):
        index = self.directional_check()


        if self.__class__ == Enemy and self.tracking == False:

            for i in range (120):
                surface.blit(self.frames[index][cycle], (self.x -32, self.y-32))
        else:
             for i in range (120):
                surface.blit(self.frames[index][cycle], (self.x -32, self.y-32))



class Player(Character):
    def __init__(self,*args):
        super().__init__(*args)
        self.inventory = []
        self.equipped_items = []
        self.gold = 0
        self.level = 1
        self.experience = 0

    def set_image(self, image_path):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (64, 64))

    def move(self, dt, k):

        if k[pygame.K_LSHIFT] :
            dash = 2
        else:
            dash = 1


        if (k[pygame.K_w] or k[pygame.K_s]) and (k[pygame.K_a] or k[pygame.K_d]):
            self.speed = self.speed_diagonal
        else:
            self.speed = self.speed_diagonal * math.sqrt(2)
        
        if k[pygame.K_w] and self.y > 5:
            self.y -= self.speed * dt * dash
            self.direction = 'up'

        if k[pygame.K_s] and self.y < 715:
            self.y += self.speed * dt * dash
            self.direction = 'down'

        if k[pygame.K_a] and self.x > 5:
            self.x -= self.speed * dt * dash
            self.direction = 'left'   

        if k[pygame.K_d] and self.x < 1275:
            self.x += self.speed * dt * dash
            self.direction = 'right'






    def meelee(self, k, SCREEN):
        if k[pygame.K_SPACE]:
            pygame.draw.circle(SCREEN, (255,255,0), (int(self.x), int(self.y)), 20, 2)


    



class Enemy(Character):
    def __init__(self,*args):
        super().__init__(*args)
        self.tracking = False


    def track(self, tracking, dt, enemies):
        dx = tracking.x - self.x
        dy = tracking.y - self.y
        distance_squared = dx**2 + dy**2
        distance = distance_squared ** 0.5
        self.tracking = False
        if 50 < distance < 400:
            # Normalize direction to player
            self.tracking = True
            nx = dx / distance
            ny = dy / distance
            if abs(nx) > abs(ny):
                self.direction = 'right' if nx > 0 else 'left'
            else:
                self.direction = 'down' if ny > 0 else 'up'
            # --- Avoid other enemies ---
            sep_x, sep_y = 0, 0
            for other in enemies:
                if other is self:
                    continue
                ox = self.x - other.x
                oy = self.y - other.y
                dist2 = ox**2 + oy**2
                if dist2 < 100**2:  # personal space radius
                    dist = dist2 ** 0.5
                    if dist > 0:
                        # Scale push by closeness (closer = stronger push)
                        strength = 1 - (dist / 100.0)
                        sep_x += (ox / dist) * strength
                        sep_y += (oy / dist) * strength

            # Combine seek + separation
            move_x = nx + sep_x
            move_y = ny + sep_y


            #move_x += random.uniform(-0.1, 0.1)
            #move_y += random.uniform(-0.1, 0.1)

            # Normalize combined vector
            mag = (move_x**2 + move_y**2) ** 0.5
            if mag > 0:
                move_x /= mag
                move_y /= mag

            # --- Distance-based speed scaling ---
            # Closer = faster, farther = slower
            # Clamp factor so they never fully stop
            speed_factor = max(0.2, min(1.0, (400 - distance) / 400.0))

            # Apply movement
            self.x += move_x * self.speed * speed_factor * dt
            self.y += move_y * self.speed * speed_factor * dt
        else:
            return False