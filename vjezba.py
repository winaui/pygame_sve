import pygame
import random, math

#inicijalizacija pygame funkcija
pygame.init()

#kreiranje zaslona
screen = pygame.display.set_mode((800, 600))
background = pygame.image.load('background.png')

#postavljanje naslova i ikone za igricu
pygame.display.set_caption("Space Invasion")
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)

#PLAYER
playerImage = pygame.image.load("player.png")
playerX = 370
playerY = 480
playerX_change = 0

#ENEMY
enemyImage = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
numOfEnemies = 6

for i in range (numOfEnemies):
    enemyImage.append(pygame.image.load("ufo.png"))
    enemyX.append(random.randint(0, 736)) 
    enemyY.append(random.randint(50, 149))
    enemyX_change.append(5)
    enemyY_change.append(20) 

#BULLET
bulletImage = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletY_change = 10
# ready - spremno za pucat 
# fire - ispucan metak
bullet_state = "ready"

score = 0
font = pygame.font.Font('enter-the-gungeon-small.ttf', 32)
font_x = 10
font_y = 12

game_over_font = pygame.font.Font('enter-the-gungeon-small.ttf', 62)

def show_score(x, y):
    score_value = font.render("Score : " + str(score), True, (255, 255, 255))
    screen.blit(score_value, (x, y))

def player(x, y):
    screen.blit(playerImage, (playerX, playerY))

def enemy(x, y, i):
    screen.blit(enemyImage[i], (x,y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImage, (x + 16, y + 10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
    if distance < 27:
        return True
    else:
        return False    

def game_over():
    game_over_text = game_over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(game_over_text, (220, 250))

#game loop
running = True
while running:
    screen.fill((0, 0, 0))
    #pozadina
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
        #if za pritisnutu tipku
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -3.5
            if event.key == pygame.K_RIGHT:
                playerX_change = 3.5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
        
    #da se ne može izać iz okvira (0 - 800)    
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    for i in range (numOfEnemies):
        #game over tekstić
        if enemyY[i] > 420:
            for j in range(numOfEnemies):
                enemyY[j] = 2000
            game_over()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 5
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -5
            enemyY[i] += enemyY_change[i]
        #sudar opa
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bulletY = 480
            bullet_state = "ready"
            score += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 149)  
        
        enemy(enemyX[i], enemyY[i], i)  

    #kretanje metka
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change


    player(playerX, playerY)
    show_score(font_x, font_y)
    pygame.display.update()