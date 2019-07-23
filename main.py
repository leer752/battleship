import pygame
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
    def __init__(self, alignment, color, status, number, x, y, rectangle):
        self.alignment = alignment
        self.number = number
        self.status = status
        self.color = color
        self.x = x
        self.y = y
        self.rectangle = rectangle


# Assign positions to a list array that is 10x10 units
def create_player_array():
    player_grid = []
    for row in range(10):
        player_grid.append([])
        for column in range(10):
            player_grid[row].append(0)
            player_grid[row][column] = Board("player", white, "empty", "empty", row, column, pygame.rect.Rect((unit_margin + unit_size) * column + 80, (unit_margin + unit_size) * row + 60, unit_size, unit_size))
    return player_grid


# Assign positions to a list array that is 10x10 units
def create_enemy_array():
    enemy_grid = []
    for row in range(10):
        enemy_grid.append([])
        for column in range(10):
            enemy_grid[row].append(0)
            enemy_grid[row][column] = Board("enemy", white, "empty", "empty", row, column, pygame.rect.Rect((unit_margin + unit_size) * column + 600, (unit_margin + unit_size) * row + 60, unit_size, unit_size))
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


# Check if the player has won or lost the game
def check_end_game(player_grid, enemy_grid):
    not_destroyed = 0

    for row in range(10):
        for column in range(10):
            if player_grid[row][column].status == "full":
                not_destroyed += 1

    if not_destroyed == 0:
        return "defeat"

    not_destroyed = 0

    for row in range(10):
        for column in range(10):
            if enemy_grid[row][column].status == "full":
                not_destroyed += 1

    if not_destroyed == 0:
        return "victory"

    return False


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
    random.seed()

    for m in range(5):
        enemy_rotation = random.choice(("horizontal", "vertical"))

        space_taken = True

        if m == 0:
            enemy_units = 2
        elif m == 1:
            enemy_units = 3
        else:
            enemy_units = m + 1

        while space_taken:
            enemy_x = random.randrange(horizontal_units)
            enemy_y = random.randrange(vertical_units)
            space_taken = False
            for n in range(enemy_units):
                if enemy_rotation == "horizontal":
                    if (enemy_x + n) >= horizontal_units:
                        space_taken = True
                    else:
                        if enemy_grid[enemy_x + n][enemy_y].number != "empty":
                            space_taken = True
                else:
                    if (enemy_y + n) >= vertical_units:
                        space_taken = True
                    else:
                        if enemy_grid[enemy_x][enemy_y + n].number != "empty":
                            space_taken = True

        for n in range(enemy_units):
            if enemy_rotation == "horizontal":
                enemy_grid[enemy_x + n][enemy_y].number = str(m)
                enemy_grid[enemy_x + n][enemy_y].status = "full"
                # Testing purposes only
                enemy_grid[enemy_x + n][enemy_y].color = green
            else:
                enemy_grid[enemy_x][enemy_y + n].number = str(m)
                enemy_grid[enemy_x][enemy_y + n].status = "full"
                # Testing purposes only
                enemy_grid[enemy_x][enemy_y + n].color = green

    return enemy_grid


# Update scores on screen for enemy based on units hit, missed, & destroyed
def draw_enemy_score():
    pass


# Update scores on screen for player based on units hit, missed, & destroyed
def draw_player_score():
    pass


# Check if enemy hit a player unit & change the player tile
def check_player_hit(player_grid, guess_x, guess_y):
    selected_unit = player_grid[guess_x][guess_y]

    if selected_unit.status == "hit" or selected_unit.status == "miss" or selected_unit.status == "destroyed":
        return "invalid", player_grid

    if selected_unit.status == "empty":
        selected_unit.status = "miss"
        selected_unit.color = blue
        return False, player_grid

    elif selected_unit.status == "full":
        counting_units = 1
        selected_identity = selected_unit.alignment + "_" + selected_unit.number
        if selected_unit.number == "0":
            units = 2
        elif selected_unit.number == "1" or selected_unit.number == "2":
            units = 3
        elif selected_unit.number == "3":
            units = 4
        else:
            units = 5
        for row in range(10):
            for column in range(10):
                ship_identity = player_grid[row][column].alignment + "_" + player_grid[row][column].number
                if ship_identity == selected_identity:
                    if player_grid[row][column].status == "hit":
                        counting_units += 1
        if units == counting_units:
            for row in range(10):
                for column in range(10):
                    ship_identity = player_grid[row][column].alignment + "_" + player_grid[row][column].number
                    if ship_identity == selected_identity:
                        player_grid[row][column].status = "destroyed"
                        player_grid[row][column].color = red
        else:
            selected_unit.status = "hit"
            selected_unit.color = orange

    return True, player_grid


# Check if player hit an enemy unit & uncover that enemy tile
def check_enemy_hit(event_pos, enemy_grid):
    valid_space = False

    for row in range(10):
        for column in range(10):
            if enemy_grid[row][column].rectangle.collidepoint(event_pos):
                valid_space = True
                selected_unit = enemy_grid[row][column]

    if not valid_space:
        return False, enemy_grid

    if selected_unit.status == "hit" or selected_unit.status == "miss" or selected_unit.status == "destroyed":
        return False, enemy_grid

    if selected_unit.status == "empty":
        selected_unit.status = "miss"
        selected_unit.color = blue

    elif selected_unit.status == "full":
        counting_units = 1
        selected_identity = selected_unit.alignment + "_" + selected_unit.number
        if selected_unit.number == "0":
            units = 2
        elif selected_unit.number == "1" or selected_unit.number == "2":
            units = 3
        elif selected_unit.number == "3":
            units = 4
        else:
            units = 5
        for row in range(10):
            for column in range(10):
                ship_identity = enemy_grid[row][column].alignment + "_" + enemy_grid[row][column].number
                if ship_identity == selected_identity:
                    if enemy_grid[row][column].status == "hit":
                        counting_units += 1
        if units == counting_units:
            for row in range(10):
                for column in range(10):
                    ship_identity = enemy_grid[row][column].alignment + "_" + enemy_grid[row][column].number
                    if ship_identity == selected_identity:
                        enemy_grid[row][column].status = "destroyed"
                        enemy_grid[row][column].color = red
        else:
            selected_unit.status = "hit"
            selected_unit.color = orange

    return True, enemy_grid


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
    draw_starting_window(placed_ships, player_grid, enemy_grid, orientation)

    return player_grid, enemy_grid


# Generate random guess for enemy on player grid
# Check if unit hit but not destroyed; if so, change enemy guess to check around hit piece
def enemy_turn(player_grid, enemy_grid):
    try:
        turn_number
    except NameError:
        turn_number = 1
    else:
        pass

    if turn_number == 1:
        blind_guess = True
        first_x = 0
        first_y = 0
        previous_x = 0
        previous_y = 0
        orientation = None
        direction = None

    if blind_guess:
        guess_x = random.randrange(horizontal_units)
        guess_y = random.randrange(vertical_units)
        success, player_grid = check_player_hit(guess_x, guess_y, player_grid)
        while success == "invalid":
            guess_x = random.randrange(horizontal_units)
            guess_y = random.randrange(vertical_units)
        if success:
            first_x = guess_x
            first_y = guess_y
            previous_x = guess_x
            previous_y = guess_y
            blind_guess = False
    else:
        if orientation is not None:
            pass
        if direction is not None:
            pass


# Handle all actions for a player turn
def player_turn(player_grid, enemy_grid):
    guessing = True

    draw_playing_window(player_grid, enemy_grid)

    while guessing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    guessed, enemy_grid = check_enemy_hit(event.pos, enemy_grid)

            elif event.type == pygame.MOUSEBUTTONUP:
                if guessed:
                    guessing = False

    draw_playing_window(player_grid, enemy_grid)

    return player_grid, enemy_grid


# Victory sub-menu
def victory_menu():
    pass


# Defeat sub-menu
def defeat_menu():
    pass


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
            prepping = False

        end_game = False
        while not end_game:
            player_grid, enemy_grid = player_turn(player_grid, enemy_grid)
            end_game = check_end_game(player_grid, enemy_grid)
            if not end_game:
                player_grid, enemy_grid = enemy_turn(player_grid, enemy_grid)
                end_game = check_end_game(player_grid, enemy_grid)

        if end_game == "victory":
            victory_menu()
        elif end_game == "defeat":
            defeat_menu()

    pygame.display.flip()
    clock.tick(fps)


# Main menu before game starts that prompts player to either begin or quit; calls the Main function
def main_menu():
    pass


main()

pygame.quit()
