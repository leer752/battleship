import pygame
import time
import random

pygame.init()

# Global variables
fps = 60

screen_width = 1000
screen_height = 700
screen_height_margin = 100
screen_width_margin = 50

horizontal_units = 10
vertical_units = 10

unit_margin = 7
unit_size = 25

fontsize = 30
game_font = pygame.font.Font("C:\\Users\\bnr752\\PycharmProjects\\battleship\\assets\\molor.otf", fontsize)

red = (255, 51, 51)
blue = (153, 204, 255)
green = (205, 235, 139)
orange = (255, 128, 0)
white = (255, 255, 255)
black = (0, 0, 0)

# Initialize screen & set sentinel value for main
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Battleship")


# Create a class object that represents the board
# __init__ function defines whether the space belongs to an enemy or player, which ship the unit belongs to,
# the color of the square, the x & y positions of the square, and the rectangle dimensions for the square
class Board(object):
    def __init__(self, alignment, color, number, x, y, rectangle):
        self.alignment = alignment
        self.number = number
        self.ship = alignment + "_" + number
        self.color = color
        self.x = x
        self.y = y
        self.rectangle = rectangle

    def get_board_values(self, value):
        if value == "alignment":
            return self.alignment
        elif value == "color":
            return self.color
        elif value == "x":
            return self.x
        elif value == "y":
            return self.y
        else:
            return self.rectangle


# Assign positions to a list array that is 10x10 units
def create_player_array():
    player_grid = []
    for row in range(10):
        player_grid.append([])
        for column in range(10):
            player_grid[row].append(0)
            player_grid[row][column] = Board("player", white, "empty", row, column, pygame.rect.Rect((unit_margin + unit_size) * column + 80, (unit_margin + unit_size) * row + 60, unit_size, unit_size))
    return player_grid


# Assign positions to a list array that is 10x10 units
def create_enemy_array():
    enemy_grid = []
    for row in range(10):
        enemy_grid.append([])
        for column in range(10):
            enemy_grid[row].append(0)
            enemy_grid[row][column] = Board("enemy", white, "empty", row, column, pygame.rect.Rect((unit_margin + unit_size) * column + 600, (unit_margin + unit_size) * row + 60, unit_size, unit_size))
    return enemy_grid


# Draw the player grid & display it on the screen for the user
def draw_player_grid(player_grid):
    for row in range(10):
        for column in range(10):
            pygame.draw.rect(screen, player_grid[row][column].color, player_grid[row][column].rectangle)
    text = game_font.render("Player (YOU)", 1, white)
    screen.blit(text, (175, 23))


# Draw the enemy grid & display it on the screen for the user
# Keep in mind that enemy tiles are "covered"; the user cannot see the enemy ships
def draw_enemy_grid(enemy_grid):
    for row in range(10):
        for column in range(10):
            pygame.draw.rect(screen, enemy_grid[row][column].color, enemy_grid[row][column].rectangle)
    text = game_font.render("Enemy", 1, white)
    screen.blit(text, (735, 23))


# Check that a ship piece is being placed in a valid area on the player grid
# Piece must not overlap another ship or be placed off the grid
def valid_player_space(checking_ship, ship_number, placed_ships, player_grid, enemy_grid, orientation):
    grid_width = (unit_size * horizontal_units) + (unit_margin * (horizontal_units - 1))
    grid_height = (unit_size * vertical_units) + (unit_margin * (vertical_units - 1))
    counting_units = 0

    if ship_number == 0:
        units = 2
    elif ship_number == 1:
        units = 3
    else:
        units = ship_number + 1

    if checking_ship.x < 80 or checking_ship.x > ((grid_width + 80) - checking_ship.width):
        return False, player_grid
    if checking_ship.y < 60 or checking_ship.y > ((grid_height + 60) - checking_ship.height):
        return False, player_grid

    for row in range(10):
        for column in range(10):
            if pygame.Rect.colliderect(checking_ship, player_grid[row][column].rectangle):
                if player_grid[row][column].color != white:
                    return False, player_grid
                else:
                    counting_units += 1

    if counting_units > units:
        return False, player_grid

    for row in range(10):
        for column in range(10):
            if pygame.Rect.colliderect(checking_ship, player_grid[row][column].rectangle):
                player_grid[row][column].color = green
                player_grid[row][column].number = str(ship_number)
                draw_starting_window(placed_ships, player_grid, enemy_grid, orientation)

    return True, player_grid


# Check if the player has lost the game
def check_lost():
    pass


# Check if the player has won the game
def check_win():
    pass


# Draw the game preparation screen
# Shows both grids (player & enemy) & ship inventory
def draw_starting_window(placed_ships, player_grid, enemy_grid, orientation):
    screen.fill(blue)

    draw_player_grid(player_grid)
    draw_enemy_grid(enemy_grid)
    ship_inventory = draw_ship_inventory(placed_ships, orientation)

    pygame.display.flip()

    return ship_inventory, player_grid, enemy_grid


# Draw the ongoing game screen
# Shows both grids & scores
def draw_playing_window(player_grid, enemy_grid):
    screen.fill(blue)

    draw_player_grid(player_grid)
    draw_enemy_grid(enemy_grid)

    pygame.display.flip()


# Draw the victory screen
# Shows enemy grid & score with victory menu
def draw_victory_window():
    pass


# Draw the defeat screen
# Shows player grid & score with defeat menu
def draw_defeat_window():
    pass


# Generate positions for enemy ships & place them on enemy grid
def get_enemy_positions(enemy_grid):
    for m in range(5):
        generated_number = random.randint(0, 1)
        if generated_number == 0:
            enemy_rotation = "horizontal"
        else:
            enemy_rotation = "vertical"

        space_taken = True

        if m == 0:
            enemy_units = 2
        elif m == 1:
            enemy_units = 3
        else:
            enemy_units = m + 1

        while space_taken:
            enemy_x = random.randint(1, (horizontal_units + 1)) - 1
            enemy_y = random.randint(1, (vertical_units + 1)) - 1
            space_taken = False
            for n in range(enemy_units):
                if enemy_rotation == "horizontal":
                    if (enemy_x + n) > horizontal_units:
                    if (enemy_x + n) > horizontal_units:
                        space_taken = True
                    else:
                        if enemy_grid[enemy_x + n][enemy_y].number != "empty":
                            space_taken = True
                else:
                    if (enemy_y + n) > vertical_units:
                        space_taken = True
                    else:
                        if enemy_grid[enemy_x][enemy_y + n].number != "empty":
                            space_taken = True

        for n in range(enemy_units):
            if enemy_rotation == "horizontal":
                enemy_grid[enemy_x + n][enemy_y].number = str(m)
            else:
                enemy_grid[enemy_x][enemy_y + n].number = str(m)

    return enemy_grid


# Convert dropped ship to X & Y units for the player grid list array
# i.e. if a 3-unit player ship is dropped in the top-left corner horizontally,
# this function should translate the sprite into array positions (1,1), (2,1), & (3,1)
def convert_ship_units():
    pass


# Update scores on screen for enemy based on units hit, missed, & destroyed
def draw_enemy_score():
    pass


# Update scores on screen for player based on units hit, missed, & destroyed
def draw_player_score():
    pass


# Create ships on the ship inventory for dragging purposes
# Set initial X & Y for sprites
def create_ship_sprites():
    pass


# Add player ship to grid & list array & remove placed ship image
def add_player_ship():
    pass


# Check if enemy hit a player unit & change the player tile
def check_player_hit():
    pass


# Check if player hit an enemy unit & uncover that enemy tile
def check_enemy_hit():
    pass


# Display separate small screen that holds player ships; player will drag & drop ships from this screen
def draw_ship_inventory(placed_ships, orientation):
    inventory_rectangle = pygame.Surface((832, 200))
    inventory_rectangle.fill(white)
    screen.blit(inventory_rectangle, (80, 450))

    text = game_font.render("Ships (drag n' drop)", 1, white)
    screen.blit(text, (100, 415))
    text = game_font.render("[R]otate", 1, white)
    screen.blit(text, (810, 415))

    ship_inventory = []

    if orientation == "horizontal":
        for m in range(5):
            if m == 0:
                ship_inventory.append(pygame.rect.Rect(135, 530, (unit_size *2) + unit_margin, unit_size))
            if m == 1:
                ship_inventory.append(pygame.rect.Rect(245, 530, (unit_size * 3) + (unit_margin * 2), unit_size))
            if m == 2:
                ship_inventory.append(pygame.rect.Rect(380, 530, (unit_size * 3) + (unit_margin * 2), unit_size))
            if m == 3:
                ship_inventory.append(pygame.rect.Rect(515, 530, (unit_size * 4) + (unit_margin * 3), unit_size))
            if m == 4:
                ship_inventory.append(pygame.rect.Rect(685, 530, (unit_size * 5) + (unit_margin * 4), unit_size))
            if m not in placed_ships:
                pygame.draw.rect(screen, black, ship_inventory[m])

    if orientation == "vertical":
        for m in range(5):
            if m == 0:
                ship_inventory.append(pygame.rect.Rect(155, 520, unit_size, (unit_size * 2) + unit_margin))
            if m == 1:
                ship_inventory.append(pygame.rect.Rect(270, 510, unit_size, (unit_size * 3) + (unit_margin * 2)))
            if m == 2:
                ship_inventory.append(pygame.rect.Rect(405, 510, unit_size, (unit_size * 3) + (unit_margin * 2)))
            if m == 3:
                ship_inventory.append(pygame.rect.Rect(545, 490, unit_size, (unit_size * 4) + (unit_margin * 3)))
            if m == 4:
                ship_inventory.append(pygame.rect.Rect(730, 475, unit_size, (unit_size * 5) + (unit_margin * 4)))
            if m not in placed_ships:
                pygame.draw.rect(screen, black, ship_inventory[m])

    return ship_inventory


def pre_game():
    prepping = True
    placed_ships = []
    selected_ship = None
    orientation = "horizontal"
    mouse_up = False

    player_grid = create_player_array()
    enemy_grid = create_enemy_array()

    ship_inventory, player_grid, enemy_grid = draw_starting_window(placed_ships, player_grid, enemy_grid, orientation)
    while prepping:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for m in range(5):
                        if ship_inventory[m].collidepoint(event.pos):
                            selected_ship = ship_inventory[m]
                            mouse_x, mouse_y = event.pos
                            offset_x = selected_ship.x - mouse_x
                            offset_y = selected_ship.y - mouse_y
                            placed_ships.append(m)
                            ship_number = m
                mouse_up = False

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if selected_ship is not None:
                        checking_ship = selected_ship
                        valid_space, player_grid = valid_player_space(checking_ship, ship_number, placed_ships, player_grid, enemy_grid, orientation)
                        if not valid_space:
                            placed_ships.remove(ship_number)
                            ship_inventory, player_grid, enemy_grid = draw_starting_window(placed_ships, player_grid, enemy_grid, orientation)
                        else:
                            pygame.display.flip()
                            if len(placed_ships) == 5:
                                prepping = False
                        selected_ship = None
                mouse_up = True

            elif event.type == pygame.MOUSEMOTION:
                if selected_ship is not None:
                    mouse_x, mouse_y = event.pos
                    selected_ship.x = mouse_x + offset_x
                    selected_ship.y = mouse_y + offset_y
                    draw_starting_window(placed_ships, player_grid, enemy_grid, orientation)
                    pygame.draw.rect(screen, black, selected_ship)
                    pygame.display.update()

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                if mouse_up:
                    if orientation == "horizontal":
                        orientation = "vertical"
                        ship_inventory, player_grid, enemy_grid = draw_starting_window(placed_ships, player_grid, enemy_grid, orientation)
                    else:
                        orientation = "horizontal"
                        ship_inventory, player_grid, enemy_grid = draw_starting_window(placed_ships, player_grid, enemy_grid, orientation)

    enemy_grid = get_enemy_positions(enemy_grid)

    return player_grid, enemy_grid


# Generate random guess for enemy on player grid
# Check if unit hit but not destroyed; if so, change enemy guess to check around hit piece
def enemy_turn():
    pass


# Handle all actions for a player turn
def player_turn(player_grid, enemy_grid):
    draw_playing_window(player_grid, enemy_grid)


# Main function
def main():

    prepping = True
    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if prepping:
            player_grid, enemy_grid = pre_game()
            time.sleep(3)
            prepping = False

        player_turn(player_grid, enemy_grid)

    pygame.display.flip()
    clock.tick(fps)


# Main menu before game starts that prompts player to either begin or quit; calls the Main function
def main_menu():
    pass


main()

pygame.quit()
