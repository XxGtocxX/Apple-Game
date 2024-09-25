import pygame
import random
import sys

pygame.init() # Initialize the game object
screen = pygame.display.set_mode((350, 600)) # it will jst create a screen that disappears but to keep it open we need a game loop
clock = pygame.time.Clock() # create a obj of clock class to regulate the fps or else it will run as fast as it can

class Apple:
    def __init__(self, img, pos, speed): # requires you to take a self argument
        self.image = img
        self.rect = self.image.get_rect(topleft = pos)
        self.speed = speed
    def move(self):
        self.rect.y += self.speed
        if self.rect.y > screen.get_height():
            self.rect.y = -TILESIZE

# varibles
speed = 3
score = 0

# CONSTANTS
TILESIZE = 32

# Floor
floor_img = pygame.image.load("./assets/floor.png").convert_alpha()
floor_img = pygame.transform.scale(floor_img, (TILESIZE * 15, TILESIZE * 5))
floor_rect = floor_img.get_rect(bottomleft = (0, screen.get_height()))

# Player 
player_img = pygame.image.load("./assets/player_static.png").convert_alpha() # convert_alpha optimised the imgs in pygame
player_img = pygame.transform.scale(player_img, (TILESIZE, TILESIZE * 2 + 1))
player_rect = player_img.get_rect(center = (screen.get_width() / 2, screen.get_height() - floor_img.get_height() - (player_img.get_height() / 2)))

# Apple 
apple_img = pygame.image.load("./assets/apple.png").convert_alpha()
apple_img = pygame.transform.scale(apple_img, (TILESIZE, TILESIZE))

apples = [
    Apple(apple_img, (100, 0), 3),
    #Apple(apple_img, (300, 0), 3),
    Apple(apple_img, (200, 0), 3)
]

# Fonts 
font = pygame.font.Font("./assets/PixeloidMono.ttf", TILESIZE // 2)

# Sound effects
pickup = pygame.mixer.Sound('./assets/powerup.mp3')
pickup.set_volume(0.1)

running = True

def update():
    global speed
    global score

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        player_rect.x -= 7
    if keys[pygame.K_RIGHT]:
        player_rect.x += 7
    # Apple management
    for apple in apples:
        apple.move()
        if apple.rect.colliderect(floor_rect):
            apples.remove(apple)
            # now we want to respawn the apples
            apples.append(Apple(apple_img, (random.randint(50, 300), -50), speed))
            pygame.quit()
            
        elif apple.rect.colliderect(player_rect):
            apples.remove(apple)
            apples.append(Apple(apple_img, (random.randint(50, 300), -50), speed))
            speed += 0.1
            score += 1
            pickup.play()
            

def draw():
    screen.fill("lightblue") # you can also give rgb values if u want
    # since we know the boundaries we will assign the player at the center of the screen(also the top lft boundary is 0,0)
    screen.blit(floor_img, floor_rect)
    screen.blit(player_img, player_rect)

    for apple in apples:
        screen.blit(apple.image, apple.rect)

    score_text = font.render(f'Score: {score}', True, "white")
    screen.blit(score_text, (5, 5))

# Game loop
while running:
    for event in pygame.event.get():       # looping through every signle event
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    update()
    draw()

    clock.tick(60)
    pygame.display.update() # this will open the screen and update it every second
