# Simple Pokemon Battle using Pygame
# Name - ADITYA BHARDWAJ
# Section - D2
# Roll No - 08
# Course – B TECH
# Branch – CSE

import pygame
import sys
import random

pygame.init()
pygame.mixer.init()

# Window
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pokemon Battle")

clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 20)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Load Images
charmander_img = pygame.image.load("Pokemon/4.png").convert_alpha()
squirtle_img = pygame.image.load("Pokemon/7.png").convert_alpha()

charmander_img = pygame.transform.scale(charmander_img, (150, 150))
squirtle_img = pygame.transform.scale(squirtle_img, (150, 150))

# Load Sounds
charmander_cry = pygame.mixer.Sound("Sound/4.ogg")
squirtle_cry = pygame.mixer.Sound("Sound/7.ogg")

# Play cries at start
charmander_cry.play()
pygame.time.delay(800)
squirtle_cry.play()

# Stats
charmander_hp = 39
squirtle_hp = 44

# Main Loop
running = True
battle_over = False

while running:
    clock.tick(60)
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN and not battle_over:
            if event.key == pygame.K_SPACE:
                # Charmander attacks
                damage = random.randint(5, 10)
                squirtle_hp -= damage

                if squirtle_hp <= 0:
                    squirtle_hp = 0
                    battle_over = True

                else:
                    # Squirtle counterattacks
                    damage = random.randint(4, 8)
                    charmander_hp -= damage

                    if charmander_hp <= 0:
                        charmander_hp = 0
                        battle_over = True

    # Draw Pokémon
    screen.blit(charmander_img, (100, 200))
    screen.blit(squirtle_img, (550, 50))

    # Draw HP
    char_text = font.render(f"Charmander HP: {charmander_hp}", True, BLACK)
    squirt_text = font.render(f"Squirtle HP: {squirtle_hp}", True, BLACK)

    screen.blit(char_text, (80, 170))
    screen.blit(squirt_text, (520, 20))

    if battle_over:
        if charmander_hp > 0:
            result = "Charmander Wins!"
        else:
            result = "Squirtle Wins!"

        result_text = font.render(result, True, BLACK)
        screen.blit(result_text, (320, 180))

    pygame.display.flip()

pygame.quit()
sys.exit()
