#still to come:
#will implement a change of bet amount next


import pygame
import random
import sys

# Constants for game settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
ROWS = 12  # Number of rows of pegs
MAX_PEGS_IN_ROW = ROWS  # The bottom row will have the most pegs
BUCKET_WIDTH = SCREEN_WIDTH // MAX_PEGS_IN_ROW
PEG_SIZE = 10
BALL_SIZE = 15
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
ROW_HEIGHT = 45
OFFSET = (SCREEN_WIDTH - (BUCKET_WIDTH * (ROWS - 12))) // 2  # Center the triangle
OFFSET1 = (SCREEN_WIDTH - (BUCKET_WIDTH * (ROWS + 1))) // 2  # Adjust buckets

# Player's starting plinko coins
plinko_coins = 100

# Bucket multipliers
BUCKET_MULTIPLIERS = [9, 5, 2.5, 2, 0.75, 0.5, 0.5, 0.75, 2, 2.5, 5, 9]
#BUCKET_MULTIPLIERS = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]

# Initialize pygame
pygame.init()

# Setup the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Plinko Game")
clock = pygame.time.Clock()
font = pygame.font.SysFont('arial', 24)

# Function to blend between two colors
def blend_color(color1, color2, blend_factor):
    return (
        int(color1[0] + (color2[0] - color1[0]) * blend_factor),
        int(color1[1] + (color2[1] - color1[1]) * blend_factor),
        int(color1[2] + (color2[2] - color1[2]) * blend_factor)
    )

# Function to draw the Plinko board with color-coded buckets
def draw_board(rows, current_multiplier):
    screen.fill((0, 0, 0))  # Black background
    # Draw pegs
    for row in range(rows):
        for col in range(row + 1):
            x = OFFSET + col * BUCKET_WIDTH - (BUCKET_WIDTH // 2) * row
            y = ROW_HEIGHT + (row * ROW_HEIGHT)
            pygame.draw.circle(screen, WHITE, (x, y), PEG_SIZE)
    # Draw color-coded buckets
    mid_bucket_index = rows // 2
    for i in range(rows + 1):
        # Calculate blend factor based on distance from the middle bucket
        distance_from_mid = abs(mid_bucket_index - i)
        blend_factor = distance_from_mid / mid_bucket_index
        bucket_color = blend_color(YELLOW, RED, blend_factor)
        bucket_x = OFFSET1 + i * BUCKET_WIDTH
        pygame.draw.rect(screen, bucket_color, (bucket_x, SCREEN_HEIGHT - ROW_HEIGHT, BUCKET_WIDTH, ROW_HEIGHT))
    # Display the current coins and multiplier
    coins_text = font.render(f'Money: ${plinko_coins}', True, WHITE)
    multiplier_text = font.render(f'Last Multiplier: {current_multiplier}x', True, WHITE)
    screen.blit(coins_text, (10, 10))
    screen.blit(multiplier_text, (SCREEN_WIDTH - 220, 10))

# Function to drop the ball and calculate the new coins amount
def drop_ball(rows, bet):
    global plinko_coins
    ball_x = SCREEN_WIDTH // 2
    ball_y = ROW_HEIGHT
    current_multiplier = 0
    while ball_y < SCREEN_HEIGHT - 2 * ROW_HEIGHT:
        draw_board(rows, current_multiplier)
        pygame.draw.circle(screen, RED, (ball_x, ball_y), BALL_SIZE)
        ball_y += ROW_HEIGHT
        move_direction = random.choice([-1, 0, 1])
        ball_x += move_direction * (BUCKET_WIDTH // 2)
        ball_x = max(OFFSET1 + BALL_SIZE, min(ball_x, SCREEN_WIDTH - OFFSET1 - BALL_SIZE))
        pygame.display.flip()
        clock.tick(30)
    # Determine which bucket the ball falls into
    bucket = (ball_x - OFFSET1) // BUCKET_WIDTH
    current_multiplier = BUCKET_MULTIPLIERS[bucket]
    #winnings = bet + bet * current_multiplier
    winnings = bet * current_multiplier
    plinko_coins += winnings - bet  # Subtract the bet and add the winnings
    return current_multiplier

# Main game loop
running = True
current_multiplier = 0  # Initialize the current multiplier

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Player places a bet
                bet = 10  # Example fixed bet, you can make it dynamic as needed
                if plinko_coins >= bet:
                    current_multiplier = drop_ball(ROWS, bet)
                    print(f"Multiplier: {current_multiplier}x | New Balance: {plinko_coins} plinko coins")
                else:
                    print("Not enough plinko coins to place a bet!")

    # Draw the initial board and update the display
    draw_board(ROWS, current_multiplier)
    pygame.display.flip()
    clock.tick(60)

# If the loop is exited, quit the game
pygame.quit()

