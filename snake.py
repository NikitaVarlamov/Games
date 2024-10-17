import pygame
import time
import random

# Initialize pygame
pygame.init()

# Define colors
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

# Screen dimensions
dis_width = 800
dis_height = 600
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake Game')

# Clock and snake settings
clock = pygame.time.Clock()
snake_block = 10
snake_speed = 15

# Fonts
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

# Function to display the score
def display_score(score):
    value = score_font.render(f"Your Score: {score}", True, yellow)
    dis.blit(value, [0, 0])

# Function to draw the snake
def draw_snake(snake_block, snake_list):
    for block in snake_list:
        pygame.draw.rect(dis, black, [block[0], block[1], snake_block, snake_block])

# Function to display messages on the screen
def message(msg, color, position):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, position)

# Main game loop
def gameLoop():
    # Initial game conditions
    game_over = False
    game_close = False

    # Snake initial position and movement
    x = dis_width / 2
    y = dis_height / 2
    x_change = 0
    y_change = 0

    # Snake body
    snake_list = []
    snake_length = 1

    # Food position
    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

    while not game_over:
        while game_close:
            dis.fill(blue)
            message("You Lost! Press C-Play Again or Q-Quit", red, [dis_width / 6, dis_height / 3])
            message(f"Final Score: {snake_length - 1}", yellow, [dis_width / 6, dis_height / 2])
            pygame.display.update()

            # Event handling for game over screen
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        # Event handling for the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x_change == 0:
                    x_change = -snake_block
                    y_change = 0
                elif event.key == pygame.K_RIGHT and x_change == 0:
                    x_change = snake_block
                    y_change = 0
                elif event.key == pygame.K_UP and y_change == 0:
                    y_change = -snake_block
                    x_change = 0
                elif event.key == pygame.K_DOWN and y_change == 0:
                    y_change = snake_block
                    x_change = 0

        # Snake boundaries
        if x >= dis_width or x < 0 or y >= dis_height or y < 0:
            game_close = True

        # Update snake position
        x += x_change
        y += y_change
        dis.fill(blue)

        # Draw food
        pygame.draw.rect(dis, green, [foodx, foody, snake_block, snake_block])

        # Update snake body
        snake_head = [x, y]
        snake_list.append(snake_head)
        if len(snake_list) > snake_length:
            del snake_list[0]

        # Check for collisions with the body
        for block in snake_list[:-1]:
            if block == snake_head:
                game_close = True

        # Draw snake and score
        draw_snake(snake_block, snake_list)
        display_score(snake_length - 1)

        pygame.display.update()

        # Check if the snake eats the food
        if x == foodx and y == foody:
            foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            snake_length += 1

        clock.tick(snake_speed)

    pygame.quit()
    quit()

# Start the game
gameLoop()