import pygame
import random
pygame.init()


screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('SNAKE GAME')
font = pygame.font.SysFont('freesansbold.ttf', 30)
list_of_score = [0]

def high_score(score): #eg: [0,1,2,3,4]
    for i in range(0,len(list_of_score)):
        highscore = max(list_of_score) +1
        return str(highscore)


def start_game():

    # variables
    snake_pos = [[300, 300], [320, 300], [340, 300], [360, 300]]
    step = 20
    up = (0, -step)  # (0,-20) #I have used step as 30
    left = (-step, 0)  # (-20,0)
    right = (step, 0)  # (20,0)
    down = (0, step)
    direction = left  # default
    timer = 0
    apple_pos = [260, 300]
    score = 0
    font = pygame.font.SysFont('Arial', 30)
    game_over = 0
    border_pos = [[0, 0, 800, 10], [0, 590, 800, 10], [0, 0, 10, 600], [790, 0, 10, 600]]

    running = True
    while running:

        pygame.time.Clock().tick(120)
        screen.fill((120, 20, 200))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print('QUIT')
                running = False
            if event.type == pygame.KEYDOWN:  # seeing if a key(down) is pressed/IF ANY KEY IS PRESSED
                if event.key == pygame.K_DOWN:
                    direction = down
                    print('DOWN')
                elif event.key == pygame.K_LEFT:
                    direction = left
                    print('LEFT')
                elif event.key == pygame.K_RIGHT:
                    direction = right
                    print('RIGHT')
                elif event.key == pygame.K_UP:
                    direction = up
                    print('UP')

            # snake_pos = [[300,300], [320,300], [340,300],[360,300]]
            for x, y in snake_pos:
                pygame.draw.circle(screen, (200, 10, 10), (x, y), 10)

            pygame.draw.circle(screen, (200, 210, 10), apple_pos, 10)

            # move our snake

            timer += 1
            if timer == 5:
                snake_pos = [[snake_pos[0][0] + direction[0], snake_pos[0][1] + direction[1]]] + snake_pos[:-1]
                timer = 0

            if snake_pos[0] == apple_pos:
                x = (random.randint(20, 780) // 20) * 20
                y = (random.randint(20, 580) // 20) * 20
                apple_pos = [x, y]
                snake_pos.append(snake_pos[-1])
                global list_of_score
                list_of_score.append(score)
                score += 1

            # border_pos = [[0, 0, 800, 10], [0, 590, 800, 10], [0, 0, 10, 600], [790, 0, 10, 600]]
            for x, y, z, i in border_pos:
                pygame.draw.rect(screen, (255, 0, 0), (x, y, z, i))

            for i in range(1, len(snake_pos)):
                if snake_pos[0] == snake_pos[i]:
                    running = False
                    print('GAME OVER')
                    game_over = 1

            for x, y in snake_pos:
                if x >= 800 or x <= 0 or y >= 600 or y <= 0:
                    running = False
                    game_over = 1



            # font = pygame.font.SysFont('Arial', 30)
            screen.blit( font.render(('YOUR SCORE IS :' + str(score)), True, (255, 255, 255)), (0, 0))
            screen.blit(font.render(('HIGH SCORE :' + high_score(score)), True, (255, 255, 255)), (0, 30))

            if game_over == 1:
                run = True
                while run:
                    screen.fill((255, 255, 255))
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            run = False
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_SPACE:
                                print('Quit')
                                run = False

                        text = font.render(('GAME OVER, PRESS SPACE TO CONTINUE PLAYING'), True, (0, 0, 0))
                        screen.blit(text, (0, 10))
                        pygame.display.update()

            pygame.display.update()

#welcome page
going = True
while going:
    screen.fill((200,25,155))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            going = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                start_game()

    text = font.render(('WELCOME TO SNAKE GAME,Press space to continue'), True, (255, 255, 255))
    screen.blit(text, (0, 0))




    pygame.display.update()

