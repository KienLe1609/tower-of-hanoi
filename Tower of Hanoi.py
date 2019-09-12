import pygame, sys, time


# The objects involved can be categorized into three classes: 
# Buttons: the objects used to navigate the menu 
class Button:
    def __init__(self, image, x, y):
        self.image = pygame.image.load(image).convert()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

# Columns: the stationery objects which the Discs are moving toward
class Column:
    def __init__(self, x):
        self.image = pygame.Surface((20, 140))
        self.rect = self.image.get_rect()
        self.rect.center = (x, 150)
        self.x = x

# Discs: objects moving aroung the columns to eventually land on the last column  
class Disc:
    def __init__(self, size, color):
        self.image = pygame.Surface((size, 20))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.isup = 0
        self.column = 1


# Check if the disc needs to be moved after it has been moved to the new column
def check_for_disc_collision(disc_list, column, n, y):
    for j in range(n):
        if disc_list[i] != disc_list[j] and disc_list[i].rect.colliderect(
                disc_list[j]) and i < j:  # If the disc collides with a bigger disc in the new column:
            y = y - 20  # Move the disc up 20 pixel (The size of a disc)
        elif disc_list[i] != disc_list[j] and disc_list[i].rect.colliderect(
                disc_list[j]) and i > j:  # If the disc collides with a smaller disc in the new column:
            return 0  # Break out of the function
    disc_list[i].rect.center = (column.x, y)  # Change the disc's location
    return y


# Move the disc to the column then check if it needs to be moved
def move_disc_to_column(list, n, i, column):
    x_list, y_list = list[i].rect.center  # Save the original location of the disc
    list[i].rect.center = (column.x, 210)  # Move the disc to the desired column
    _, y = list[i].rect.center  # Take the height of the disc for use in the function above
    for _ in range(n):  # The collision check must be done n times to ensure that the collision check is finished
        y = check_for_disc_collision(disc_list, column, n, y)
        if y == 0:  # If the disc we are moving touch a smaller disc in the column
            list[i].rect.center = (x_list, y_list)  # Return the disc to its original position
            break  # End the function


# Check the event queue for important events
def check_event():
    location = (-1, -1)  # Reset the location of the mouse click
    for events in pygame.event.get():
        if events.type == pygame.QUIT:
            sys.exit()  # Exit the program
        if events.type == pygame.MOUSEBUTTONDOWN:
            location = pygame.mouse.get_pos()  # Get the location of the mouse click
    return location


# Create the colors needed to fill the discs
disc_color = [(230, 108, 128), (242, 209, 88), (62, 203, 222), (136, 216, 176), (189, 155, 197)]

# Create black and white pixels
white = (255, 255, 255)
black = (0, 0, 0)

# Create a screen and name it
size = width, height = 720, 300
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Tower of Hanoi')

# Create the three columns
column1 = Column(120)
column2 = Column(360)
column3 = Column(600)

# Create the screens
start = pygame.image.load('start menu.png').convert()
choice = pygame.image.load('choice menu.png').convert()
end = pygame.image.load('end screen.png').convert()
background = pygame.image.load('main background.png').convert()

# Create the buttons to control the game
start_button = Button('start button.png', 418, 130)
exit_button = Button('exit button.png', 418, 209)
three_button = Button('3 button.png', 194, 105)
four_button = Button('4 button.png', 320, 105)
five_button = Button('5 button.png', 446, 105)
restart_button = Button('restart button.png', 636, 269)
play_again_button = Button('play again button.png', 235, 143)
main_menu_button = Button('main menu button.png', 0, 269)

# Make the black borders transparent
restart_button.image.set_colorkey(black)
main_menu_button.image.set_colorkey(black)

while 1:

    click_location = check_event()

    # Draw everything to the screen
    screen.blit(start, (0, 0))
    screen.blit(start_button.image, start_button.rect)
    screen.blit(exit_button.image, exit_button.rect)

    # Exit the program if "Exit" is pressed
    if exit_button.rect.collidepoint(click_location):
        sys.exit()

    # Continue to the next loop if "Start" is pressed
    if start_button.rect.collidepoint(click_location):
        break

    # Update the screen to show the images
    pygame.display.update()
    pygame.time.Clock().tick(60)

while 1:

    click_location = check_event()

    # Draw everything to the screen
    screen.blit(choice, (0, 0))
    screen.blit(three_button.image, three_button.rect)
    screen.blit(four_button.image, four_button.rect)
    screen.blit(five_button.image, five_button.rect)

    # Get the selection and exit the loop
    if three_button.rect.collidepoint(click_location):
        n = 3
        break
    elif four_button.rect.collidepoint(click_location):
        n = 4
        break
    elif five_button.rect.collidepoint(click_location):
        n = 5
        break

    # Update the screen
    pygame.display.update()
    pygame.time.Clock().tick(60)

# Create the discs
disc_list = []
point_1 = (170 - (n - 3) * 20)
for i in range(1, n + 1):
    disc_list.append(Disc(i * 40, disc_color[i - 1]))
    disc_list[i - 1].rect.center = (120, point_1)
    point_1 = point_1 + 20

able_to_move_up = 1

while 1:

    click_location = check_event()

    # Draw everything to the screen
    screen.blit(background, (0, 0))
    screen.blit(column1.image, column1.rect)
    screen.blit(column2.image, column2.rect)
    screen.blit(column3.image, column3.rect)
    screen.blit(restart_button.image, restart_button.rect)
    screen.blit(main_menu_button.image, main_menu_button.rect)

    # If "Main menu" button is pressed, execute the file again to return to the start menu
    if main_menu_button.rect.collidepoint(click_location):
        execfile('Tower of Hanoi.py')

    # Check for click on the restart button
    if restart_button.rect.collidepoint(click_location):
        point_1 = 170 - (n - 3) * 20

        # Reset everything to their original position
        for i in range(n):
            disc_list[i].rect.center = (120, point_1)
            point_1 = point_1 + 20

    # Check if a disc is up
    for i in range(n):
        if disc_list[i].isup == 1:
            able_to_move_up = 0  # Prevent any disc from being moved up

    # Check for click on a disc and move that disc up if possible
    if able_to_move_up:
        for i in range(n):
            if disc_list[i].rect.collidepoint(click_location):

                # Check if the disc is on top of the column
                x_disc, y_disc = disc_list[i].rect.center  # Save the original location of the disc
                no_up = 0
                for j in range(n):
                    disc_list[i].rect.center = (x_disc, y_disc - 20)
                    if disc_list[i] != disc_list[j] and disc_list[i].rect.colliderect(
                            disc_list[j]):  # If the disc touch another disc:
                        no_up = 1  # It can not be moved up

                # Do not move the disc if it is not on top of the column
                if no_up == 1:
                    disc_list[i].rect.center = (x_disc, y_disc)  # Return the disc to its original position

                # Move the disc up otherwise
                else:
                    disc_list[i].rect.center = (x_disc, 50)
                    disc_list[i].isup = 1

    for i in range(n):
        # Execute when a disc is up
        if disc_list[i].isup:

            click_location = check_event()

            if click_location != (-1, -1):

                # Check click and move disc to column 1
                if column1.rect.collidepoint(click_location):
                    move_disc_to_column(disc_list, n, i, column1)

                # Check click and move disc to column 2
                elif column2.rect.collidepoint(click_location):
                    move_disc_to_column(disc_list, n, i, column2)

                # Check click and move disc to column 3
                elif column3.rect.collidepoint(click_location):
                    move_disc_to_column(disc_list, n, i, column3)

                    # Check if the disc is up
                _, y_disc = disc_list[i].rect.center
                if y_disc > 50:
                    disc_list[i].isup = 0
                    able_to_move_up = 1

    # Draw every disc to the screen
    for i in range(n):
        screen.blit(disc_list[i].image, disc_list[i].rect)

    # Update the screen
    pygame.display.update()

    # Check if the discs are in the winning positions
    point_1, score = 210, 0
    for i in range(n - 1, -1, -1):
        if disc_list[i].rect.center == (600, point_1):
            score += 1
        point_1 -= 20

    # Check if the game is won
    if score == n:
        time.sleep(2)
        break

    # Reset the counters
    else:
        point_1, score = 170 - (n - 3) * 20, 0
    pygame.time.Clock().tick(60)

while 1:

    click_location = check_event()

    # Draw everything to the screen
    screen.blit(end, (0, 0))
    screen.blit(play_again_button.image, play_again_button.rect)

    # Check if replay button is pressed and open the game again
    if play_again_button.rect.collidepoint(click_location):
        execfile('Tower of Hanoi.py')

    # Update the screen
    pygame.display.update()
    pygame.time.Clock().tick(60)
