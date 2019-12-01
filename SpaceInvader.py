import pygame
import math
import random
from pygame import mixer

#init pygame module
pygame.init()

#screen
screen = pygame.display.set_mode((800, 600))

#bg image
background = pygame.image.load(r'D:\Git\Pygame\bg.png')

#bg sound
mixer.music.load(r'D:\Git\Pygame\bgmusic.wav')
mixer.music.play(-1)

#title and icon of window
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load(r'D:\Git\Pygame\spaceship.png')
pygame.display.set_icon(icon)

#player model
playerImg = pygame.image.load(r'D:\Git\Pygame\player.png')
playerX = 370
playerY = 480
playerX_change = 0

#invader model
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
enemyNum = 6

for i in range(20):
    enemyImg.append(pygame.image.load(r'D:\Git\Pygame\ufo.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(30)

#bullet model
bulletImg = pygame.image.load(r'D:\Git\Pygame\bullet.png')
bulletX = 0
bulletY = 480
bulletY_change = 10
bullet_state = "ready"

#score
scoreVal = 0
font = pygame.font.Font('freesansbold.ttf', 24)
textX = 10
textY = 570

#game over text
overFont = pygame.font.Font('freesansbold.ttf', 1500)

def gameOver():
    overText = font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(overText, (328, 250))    

def score(x, y):
    score = font.render("Score: " + str(scoreVal), True, (255, 255, 255))
    screen.blit(score, (x, y))

def player(x, y):
    screen.blit(playerImg, (x, y))

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x+20, y-20))

def collision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX-bulletX, 2)) + (math.pow(enemyY-bulletY,2)))
    if distance < 40:
        return True
    else:
        return False

#gameloop
running = True

while running:
    #bg color fill in RGB
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    #event checks
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change -= 5
            if event.key == pygame.K_RIGHT:
                playerX_change += 5
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bulletSound = mixer.Sound(r'D:\Git\Pygame\bullet.wav')
                    bulletSound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, playerY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    #player movement    
    playerX += playerX_change

    #offscreen check
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    #enemy movement
    for i in range(enemyNum):
        #game over
        if enemyY[i] > 430:
            for j in range(enemyNum):
                enemyY[j] = 2000
            gameOver()
            break

        enemyX[i] += enemyX_change[i]*(1+scoreVal/100)

        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]

        #collision check
        col = collision(enemyX[i], enemyY[i], bulletX, bulletY)
        if col:
            explosionSound = mixer.Sound(r'D:\Git\Pygame\boom.wav')
            explosionSound.play()
            bullet_state = "ready"
            bulletY = 480
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)
            scoreVal = int(scoreVal) + 1

        enemy(enemyX[i], enemyY[i], i)


    #bullet movement
    if bulletY <= 0:
        bullet_state = "ready"
        bulletY = 480

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    #draw on screen and screen update
    player(playerX, playerY)
    score(textX, textY)
    pygame.display.update()