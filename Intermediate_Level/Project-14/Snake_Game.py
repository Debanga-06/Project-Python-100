import pygame
import time
import random

# Initialize pygame
pygame.init()

# Screen dimensions
width = 600
height = 400

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

# Create game window
dis = pygame.display.set_mode((width, height))
pygame.display.set_caption('Snake Game by Jiban')

# Clock for controlling speed
clock = pygame.time.Clock()

snake_block = 10
snake_speed = 15

font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)


def score_display(score):
    value = score_font.render("Your Score: " + str(score), True, black)
    dis.blit(value, [0, 0])


def snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, black, [x[0], x[1], snake_block, snake_block])


def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [width / 6, height / 3])


def draw_border():
    # Draw border around the play area
    pygame.draw.rect(dis, green, [0, 0, width, height], 5)


def gameLoop():
    game_over = False
    game_close = False

    # Snake starting position
    x1 = width / 2
    y1 = height / 2

    x1_change = 0
    y1_change = 0

    snake_list = []
    length_of_snake = 1

    # Food position
    foodx = round(random.randrange(20, width - 20) / 10.0) * 10.0
    foody = round(random.randrange(20, height - 20) / 10.0) * 10.0

    while not game_over:

        while game_close:
            dis.fill(blue)
            message("You Lost! Press C-Play Again or Q-Quit", red)
            score_display(length_of_snake - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0

        # Boundaries (with border)
        if x1 >= width - 5 or x1 < 5 or y1 >= height - 5 or y1 < 5:
            game_close = True

        x1 += x1_change
        y1 += y1_change
        dis.fill(white)

        # Draw food
        pygame.draw.rect(dis, red, [foodx, foody, snake_block, snake_block])

        # Draw snake
        snake_head = [x1, y1]
        snake_list.append(snake_head)
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        for x in snake_list[:-1]:
            if x == snake_head:
                game_close = True

        snake(snake_block, snake_list)

        # Draw border
        draw_border()

        score_display(length_of_snake - 1)
        pygame.display.update()

        # Eating food
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(20, width - 20) / 10.0) * 10.0
            foody = round(random.randrange(20, height - 20) / 10.0) * 10.0
            length_of_snake += 1

        clock.tick(snake_speed)

    pygame.quit()
    quit()


gameLoop()