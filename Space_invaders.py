# import modules
import pygame
import random
import math

# initialize pygame
pygame.init()

# screen
WW = 800
WH = 600
screen = pygame.display.set_mode((WW,WH))

# title and icon
pygame.display.set_caption("SPACE INVADERS")
icon = pygame.image.load('imgs/bullet.png')
pygame.display.set_icon(icon)

# background
background = pygame.image.load('imgs/background.png')

# bcakground music
pygame.mixer.music.load('sounds/background.wav')
pygame.mixer.music.play(-1)

#variables
running = True
welcome = True
welcome_two = False

#fonts
msg = pygame.font.SysFont('freesansbold.ttf', 64)
fs = pygame.font.SysFont('freesansbold.ttf', 32)



playerimg = pygame.image.load('imgs/si.png')
pX = 360
pY = 480
pXchange = 0
pYchange = 0
speed = 4


def player(x, y):
    screen.blit(playerimg, (x, y))



enemyimg = []
eX = []
eY = []
eXchange = []
eYchange = []
num_of_enemy = 10

for i in range(num_of_enemy):
    enemyimg.append(pygame.image.load('imgs/alien.png'))
    eX.append(random.randint(100, 700))
    eY.append(random.randint(100, 300))
    eXchange.append(3)
    eYchange.append(15)


def enemy(x, y, i):
    screen.blit(enemyimg[i], (x, y,))


# bullet
bulletimg = pygame.image.load('imgs/bullet.png')
bX = pX
bY = pY
bYchange = -10
bState = 0  # READY
# 0 = no, 1 = yes

def fire_bullet(x, y):
    global bState
    bState = 1  # FIRING
    screen.blit(bulletimg, (x, y))



# score
score = 0
sCoord = (10, 10)
score_visible = True



def score_print(scr):
    if score_visible == True:
        #font.render(text, TRUE/FALSE, colour)
        screen.blit(fs.render("Score: " + str(scr), True, (255, 255, 255)), sCoord)


def spaceship_near_alien(EX,EY,PX,PY):  #homework 4
    distance = math.sqrt((PX - EX) ** 2 + (PY - EY) ** 2)
    if distance <= 30 :
        return True
    return False


def isCollision(EX, EY, BX, BY):
    distance = math.sqrt((BX - EX) ** 2 + (BY - EY) ** 2) #sqrt((x1^2 - x2^2) + (y1^2 -y2^2))
    if distance <= 30 and bState == 1 :
        return True
    return False


def welcome_page(): #HOMEWORK 1
    global running, welcome, welcome_two
    if welcome == True:
        screen.blit(fs.render('WELCOME TO SPACE INVADERS GAME', True, (255,255,255)), (10, 100))
        screen.blit(fs.render('Press "0" to continue ', False, (255, 255, 255)), (100,200))
        screen.blit(fs.render('Press space to fire bullet ', False , (255,255,255)), (100,250))
        screen.blit(fs.render('Use arrow keys to move the player to fire bullet ', False, (255, 255, 255)), (100,300))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                welcome = False
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_0:
                    welcome = False
                    welcome_two = True


# game over text
def game_over_text(score):
    global bState
    mCoord = (180, 200)
    screen.blit(msg.render("GAME OVER!!", True, (255, 255, 255)), mCoord)
    fsCoord = (280, 300)
    screen.blit(fs.render("FINAL SCORE: " + str(score), True, (255, 255, 255)), fsCoord)
    bState = 0



def main_screen():
    global eX,pX,eY,pY,bX,bY,pYchange,pXchange,eYchange, eXchange,bYchange,score, score_visible,bState,running
    if welcome_two == True and welcome == False:
        for event in pygame.event.get():
            # QUIT
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT: pXchange = -speed
                if event.key == pygame.K_RIGHT: pXchange = speed
                if event.key == pygame.K_UP: pYchange = -speed
                if event.key == pygame.K_DOWN: pYchange = speed
                if event.key == pygame.K_SPACE:
                    bSound = pygame.mixer.Sound('sounds/laser.wav')
                    bSound.play()
                    bX, bY = pX, pY
                    fire_bullet(bX, bY)


            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    pXchange = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    pYchange = 0
                if event.key == pygame.K_SPACE:
                    bullet_on_screen = 'yes'

        # player movement
        pX += pXchange
        pY += pYchange
        if pX <= 0:
            pX = 736
        elif pX >= 736:
            pX = 0
        player(pX, pY)

        # enemy movement
        for i in range(num_of_enemy):
            # Game over
            if eY[i] >= 400:
                for j in range(num_of_enemy):
                    eY[j] = 800
                game_over_text(score)
                score_visible = False
                break

            if spaceship_near_alien(eX[i],eY[i],pX,pY):
                game_over_text(score)
                score_visible = False
                for j in range(num_of_enemy):
                    eY[j] = 800
                score_visible = False
                break

            eX[i] += eXchange[i]  # eXchange=3  eYchange=15
            if eX[i] >= 736:
                eYchange[i] += 2  #HOMEWORK 3
                eY[i] += eYchange[i]
                eXchange[i] = -eXchange[i]
                print('list showing change in alien speed-')
                print(eYchange)
            if eX[i] <= 0:
                eYchange[i] += 2
                eY[i] += eYchange[i]
                eXchange[i] = -eXchange[i]
                print(eYchange)

            # collision
            collision = isCollision(eX[i], eY[i], bX, bY)
            if collision:
                eX[i] = random.randint(100, 700)
                eY[i] = random.randint(100, 300)
                bState = 0
                eYchange[i] = 15
                score += 1
            enemy(eX[i], eY[i], i)

        # bullet movement
        if bState == 1 :
            fire_bullet(bX, bY)
            bY += bYchange  # bYchange = -10
            if bY <= 0:
                bState = 0

        pygame.draw.line(screen, (255,255,255), (0,400), (800,400), 5)

        score_print(score)



#main_loop

while running:
    screen.fill((40, 40, 40))
    screen.blit(background, (0, 0))
    welcome_page()
    main_screen()



    pygame.display.update()