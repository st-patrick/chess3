import pygame
import sys
from chess import play_chess  # Import the chess game code


# Pygame initialization
pygame.init()

# Constants for the screen
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 640
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
FPS = 60

# Colors
WHITE = (255, 255, 255)

# Initialize the screen and clock
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Main Menu")
clock = pygame.time.Clock()

# Load background image
background_image = pygame.image.load("chess3_bg.png")
background_image = pygame.transform.scale(background_image, SCREEN_SIZE)
# Load button images
play_button_image = pygame.image.load("play_button.png")
settings_button_image = pygame.image.load("settings_button.png")
volume_button_image = pygame.image.load("volume_button.png")
plus_button_image = pygame.image.load("plus_button.png")
minus_button_image = pygame.image.load("minus_button.png")
back_button_image = pygame.image.load("back_button.png")

# Function to display text on the screen with pixelated effect
def draw_text_pixelated(text, font, color, x, y, scale):
    small_font = pygame.font.Font(None, font.get_height())
    text_surface = small_font.render(text, True, color)
    screen.blit(text_surface, (x - text_surface.get_width() // 2, y - text_surface.get_height() // 2))

# Main menu function
def main_menu():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Check for button clicks
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.collidepoint(event.pos):
                    print("Play button clicked")  # Replace this with the desired action when "Play" is clicked
                    play_chess()
                elif settings_button.collidepoint(event.pos):
                    settings_menu()

        # Draw the background image
        screen.blit(background_image, (0, 0))
        #screen.fill((0,0,0))

        # Create and draw the "Play" button
        play_button = play_button_image.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 100))
        screen.blit(play_button_image, play_button)

        # Create and draw the "Settings" button
        settings_button = settings_button_image.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
        screen.blit(settings_button_image, settings_button)

        pygame.display.flip()
        clock.tick(FPS)

# Settings menu function
def settings_menu():
    volume = 50  # Initial volume value
    volume_step = 5  # Step to increase/decrease volume

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Check for button clicks
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(event.pos):
                    return  # Go back to the main menu
                elif increase_button.collidepoint(event.pos):
                    volume = min(100, volume + volume_step)  # Increase volume
                elif decrease_button.collidepoint(event.pos):
                    volume = max(0, volume - volume_step)  # Decrease volume

        # Draw the background image
        #screen.blit(background_image, (0, 0))
        screen.fill((0,0,0))

        # Create and draw the volume value
        draw_text_pixelated("{}".format(volume), pygame.font.Font(None, 40), pygame.Color("white"), 400, 275, 3)


        # Create and draw the "Play" button
        volume_button = volume_button_image.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
        screen.blit(volume_button_image, volume_button)    

        # Create increase and decrease button
        decrease_button = minus_button_image.get_rect(center=(SCREEN_WIDTH/2 + 80, SCREEN_HEIGHT/2))
        screen.blit(minus_button_image, decrease_button)          
        increase_button = plus_button_image.get_rect(center=(SCREEN_WIDTH/2 - 80, SCREEN_HEIGHT/2))
        screen.blit(plus_button_image, increase_button)

        # Create and draw the "Play" button
        back_button = back_button_image.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 200))
        screen.blit(back_button_image, back_button)    

        pygame.display.flip()
        clock.tick(FPS)

# Run the main menu
if __name__ == "__main__":
    main_menu()
