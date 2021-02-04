import pygame
import random
import time

pygame.init()  # Required

# Setup window and colors
display_width = 800
display_height = 600
black = (0, 0, 0)  # Define black color in RGB colorspace
white = (255, 255, 255)  # Define white color in RGB colorspace

red = (200, 0, 0)
green = (0, 200, 0)
blue = (0, 0, 200)

bright_red = (255, 0, 0)
bright_green = (0, 255, 0)
bright_blue = (0, 0, 255)

block_color = (53, 115, 255)

# Setting up the surface
game_display = pygame.display.set_mode((display_width, display_height))  # Called a surface
pygame.display.set_caption('A bit Racey')
clock = pygame.time.Clock()  # Init game clock

# Player Icon Setup
car_img_r = pygame.image.load('C:\\Users\\jwhitten\\Documents\\Python\\Top Down Racing\\sonic_r.png')
car_img_l = pygame.image.load('C:\\Users\\jwhitten\\Documents\\Python\\Top Down Racing\\sonic_l.png')
car_direction = car_img_r
(car_width, car_height) = car_img_r.get_rect().size  # Get Car's size

# Set Icon for game window
icon_img = pygame.image.load('C:\\Users\\jwhitten\\Documents\\Python\\Top Down Racing\\sonic_icon.png')
pygame.display.set_icon(icon_img)

# Setting sounds and music
crash_sound = pygame.mixer.Sound('C:\\Users\\jwhitten\\Documents\\Python\\Top Down Racing\\crash.wav')
pygame.mixer.music.load('C:\\Users\\jwhitten\\Documents\\Python\\Top Down Racing\\background_music.mp3')

# Define texts
large_text = pygame.font.Font('freesansbold.ttf', 115)  # Sets font and font size
medium_text = pygame.font.Font('freesansbold.ttf', 60)  # Sets font and font size
small_text = pygame.font.Font('freesansbold.ttf', 20)  # Sets font and font size

# Global variables
pause = False
# Buttons
startx = int(display_width * .1875)
starty = int(display_height * .75)
endx = int(display_width * .6875)
button_width = 100
button_height = 50


def things_dodged(count):
    font = pygame.font.SysFont(None, 25)
    text = font.render('Dodged: ' + str(count), True, green)
    game_display.blit(text, (0, 0))  # Display score on the screen


def draw_block(thingx, thingy, thingw, thingh, color):  # things to avoid
    pygame.draw.rect(game_display, color, [thingx, thingy, thingw, thingh])  # draw to display, color, [location, size]


def car(img, width, height):
    game_display.blit(img, (width, height))


def text_objects(text, font, color):
    text_surface = font.render(text, True, color)
    return text_surface, text_surface.get_rect()


def message_display(text, font, color):
    text_surf, text_rect = text_objects(text, font, color)  # Get text surface
    text_rect.center = (int(display_width / 2), int(display_height / 2))  # Get center of text surface
    game_display.blit(text_surf, text_rect)  # Display message on the screen


def crash():
    pygame.mixer_music.stop()
    pygame.mixer.Sound.play(crash_sound)
    message_display('You crashed.', large_text, black)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # game_display.fill(white)

        button('Play Again?', startx, starty, button_width, button_height, green, bright_green, select_difficulty)
        button('Quit', endx, starty, button_width, button_height, red, bright_red, quit_game)

        pygame.display.update()
        clock.tick(15)


def button(msg, x, y, w, h, ic, ac, action=None, arg=None):
    # msg = Message to display on button
    # x = Start x pos
    # y = Start y pos
    # w = Button width
    # h = Button height
    # ic = button inactive color
    # ac = button active color

    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        # User is within start button
        pygame.draw.rect(game_display, ac, (x, y, w, h))
        if click[0] == 1 and action is not None:
            if arg is not None:
                action(arg)
            else:
                action()
    else:
        pygame.draw.rect(game_display, ic, (x, y, w, h))

    text_surf, text_rect = text_objects(msg, small_text, black)
    text_rect.center = (int(x + (w / 2)), int(y + (h / 2)))
    game_display.blit(text_surf, text_rect)


def quit_game():
    pygame.quit()
    quit()


def game_unpause():
    global pause
    pygame.mixer.music.unpause()
    pause = False


def game_pause():
    pygame.mixer.music.pause()
    message_display('Paused', large_text, black)

    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        button('Continue', startx, starty, button_width, button_height, green, bright_green, game_unpause)
        button('Quit', endx, starty, button_width, button_height, red, bright_red, quit_game)

        pygame.display.update()
        clock.tick(15)


def game_intro():
    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        game_display.fill(white)

        message_display('A bit Racey', large_text, black)
        button('GO!', startx, starty, button_width, button_height, green, bright_green, select_difficulty)
        # button('Quit', endx, starty, button_width, button_height, red, bright_red, quit_game)

        pygame.display.update()


def select_difficulty():
    selecting = True

    while selecting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        game_display.fill(white)

        message_display('Select Difficulty', large_text, black)

        # button('Easy', startx, starty, button_width, button_height, green, bright_green, game_loop, 'Easy')
        button('Normal', int((startx + endx) / 2), starty, button_width, button_height, blue, bright_blue, game_loop, 'Normal')
        button('Hard', endx, starty, button_width, button_height, red, bright_red, game_loop, 'Hard')

        pygame.display.update()
        clock.tick(15)


def game_loop(difficulty='Normal'):
    global pause
    global car_direction
    pygame.mixer.music.play(-1)

    x = int(display_width * 0.45)
    y = int(display_height * 0.8)

    x_change = 0
    x_factor = 5

    # TODO Change difficulty here
    if difficulty == 'Easy':
        dif_mod = 999
        thing_speed = 5
        speed_mod = 1
    elif difficulty == 'Normal':
        dif_mod = 5
        thing_speed = 7
        speed_mod = 1
    else:
        dif_mod = 4
        thing_speed = 10
        speed_mod = 2

    # Define block to avoid
    # thing_speed = 7
    thing_width = 100
    thing_height = 100
    dodged = 0

    # Array for blocks
    blocks_y_start = -600
    num_blocks = 5
    min_block_spacing = 200
    blocks = []
    for i in range(num_blocks):
        # Create a list within a list of blocks.
        # blocks = [[x_coord, y_coord], [x_coord, y_coord], ...]
        blocks.append([random.randrange(0, display_width - thing_height), blocks_y_start])
        blocks_y_start -= random.randrange(min_block_spacing, display_height - thing_height)

    game_exit = False

    while not game_exit:  # Game Loop

        for event in pygame.event.get():  # Event Handling Loop
            if event.type == pygame.QUIT:  # Did user quit?
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:  # Did user push any key down?
                if event.key == pygame.K_LEFT:  # Left arrow key
                    x_change = -x_factor
                    car_direction = car_img_l
                elif event.key == pygame.K_RIGHT:
                    x_change = x_factor
                    car_direction = car_img_r
                elif event.key == pygame.K_p:
                    pause = True
                    game_pause()

            if event.type == pygame.KEYUP:  # Did user release key?
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:  # Left or Right?
                    x_change = 0

        x += x_change

        # Draw the screen
        game_display.fill(white)  # Redraw surface

        # Draw Blocks to avoid
        for count in range(len(blocks)):
            # Draw all blocks
            draw_block(blocks[count][0], blocks[count][1], thing_width, thing_height, block_color)
            # Move all blocks down
            blocks[count][1] += thing_speed
            count += 1

        car(car_direction, x, y)  # Display Car
        things_dodged(dodged)

        # Game logic conditions
        # TODO Adjust difficulty with boundary interaction, crash is hard+, put back is normal-

        if x > (display_width - car_width) or x < 0:  # Hit edge
            if difficulty == 'Easy' or difficulty == 'Normal':
                x += -x_change  # Put player back in bounds
            else:
                crash()

        # Dodged Block Condition
        if blocks[0][1] > display_height:  # Block moved off screen
            # Move block
            # Remove the dodged block
            del blocks[0]

            # Add a new block to the top of the list
            # Randomize the start of x between the edges of the screen
            # Randomize the start of y between the length of the screen and the minimum distance between blocks
            random_x = random.randrange(0, display_width - thing_width)
            random_y = random.randrange(blocks[-1][1] - display_height, blocks[-1][1] - min_block_spacing)
            blocks.append([random_x, random_y])

            dodged += 1  # Increase Score

            if dodged % dif_mod == 0:
                thing_speed += speed_mod  # Increase difficulty every 5 dodges
            if dodged % 20 == 0:
                thing_width += 20  # Increase size of blocks every 20 blocks

        # Crash into block Condition, only care about block closest to player.
        if y < blocks[0][1] + thing_height and y + car_height > blocks[0][1]:
            # is car within box?
            if blocks[0][0] < x < blocks[0][0] + thing_width or \
                    blocks[0][0] < x + car_width < blocks[0][0] + thing_width:
                crash()

        pygame.display.update()  # Updates the surface
        clock.tick(60)  # FPS, controls the game speed
        # End for event loop

    # End while crashed loop


game_intro()
game_loop()
pygame.quit()
quit()
