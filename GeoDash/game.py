import pygame
import sys
from block_class import Block
import pyautogui
import random

pygame.init()
clock = pygame.time.Clock()
breite = 800    	
länge = 600
win = pygame.display.set_mode((breite, länge))
spieler = pygame.image.load("game/Player2.png")
hintergrund = pygame.image.load("game/bg.png")

x = 100  # neue X Koordinate
y = 550
boden = 550

springt = False
sprunghöhe = 18
beschleunigung = sprunghöhe
geschwindigkeit = 5
schwerkraft = 1
block_geschwindigkeit = 3

block_texture = pygame.image.load("game/block.png")
blocks = [Block(breite - 80, 550, block_texture), Block(breite - 240, 550, block_texture), Block(breite - 400, 550, block_texture)]
game_over = False

score = 0
pygame.font.init()
my_font = pygame.font.SysFont('Comic Sans MS', 30)

#Kosmetik
pygame.display.set_caption("Geometry Dash 2.0")
pygame.display.set_icon(spieler)

status = "start_menu"

puffer = 35
def collision(entity):
    if x < entity.x + puffer - 5 and \
       x + puffer - 5 > entity.x and \
       y < entity.y + puffer and \
       y + puffer / 2 > entity.y:
        return True
    return False

def valid_block_position(new_x, blocks, min_distance=100):
    for block in blocks:
        if abs(new_x - block.x) < min_distance:
            return False
    return True

def randomX(blocks):
    while True:
        new_x = random.randint(breite, breite + 200)
        if valid_block_position(new_x, blocks):
            return new_x

def randomY():
    return random.randint(500, 550)

def reset_game():
    global x, y, boden, springt, beschleunigung, geschwindigkeit, schwerkraft, block_texture, blocks, game_over, score, block_geschwindigkeit
    x = 100  # neue X Koordinate
    y = 550
    boden = 550
    
    springt = False
    sprunghöhe = 18
    beschleunigung = sprunghöhe
    geschwindigkeit = 5
    schwerkraft = 1
    block_geschwindigkeit = 3

    block_texture = pygame.image.load("game/block.png")
    blocks = [Block(breite - 80, 550, block_texture), Block(breite - 240, 550, block_texture), Block(breite - 400, 550, block_texture)]
    game_over = False

    score = 0
    pygame.font.init()

    #Kosmetik
    pygame.display.set_caption("Geometry Dash 2.0")
    pygame.display.set_icon(spieler)
reset_game()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if status == "start_menu":
        win.blit(hintergrund, (0, 0))
        text = my_font.render("Drück Enter, um das Spiel zu starten", False, (255, 255, 255))
        win.blit(text, (80, länge / 2))

        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_RETURN]:
            status = "spiel"

    if status == "spiel":    
        win.blit(hintergrund, (0, 0))
        win.blit(spieler, (x, y))
        text = my_font.render(f"Score: {str(score)}", False, (255, 255, 255))
        win.blit(text, (0, 0))

        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_SPACE] and y == boden:
            springt = True

        if springt:
            y -= beschleunigung
            beschleunigung -= schwerkraft
            if beschleunigung < -sprunghöhe:
                springt = False
                beschleunigung = sprunghöhe

        if pressed[pygame.K_d]:
            x += geschwindigkeit
        if pressed[pygame.K_a]:
            x -= geschwindigkeit
        if pressed[pygame.K_ESCAPE]:
            status = "pause"

        # Grenzen
        if x <= 0:
            x = 0
        
        if x >= breite - 40: # Bildbreite = 40
            x = breite - 40

        # Block Movement
        for block in blocks:
            block.x -= block_geschwindigkeit
            win.blit(block_texture, (block.x, block.y))
            if block.x <= -40:
                block.x = randomX(blocks)
                block.y = randomY()
                score += 1
                block_geschwindigkeit += 0.1

            if collision(block):
                game_over = True
                break
            
        if game_over:
            status = "game_over"

    if status == "game_over":
        win.blit(hintergrund, (0, 0))
        text = my_font.render(f"Du bist gestorben! Deine Punktzahl: {score}", False, (255, 255, 255))
        win.blit(text, (80, länge / 2))
        text = my_font.render("Drück Enter, um nochmal zu spielen", False, (255, 255, 255))
        win.blit(text, (80, länge / 2 + 100))

        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_RETURN]:
            reset_game()
            status = "spiel"

    clock.tick(60)
    pygame.display.flip()
