import pygame
import random
import time

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

font_size = 30
game_font = pygame.font.Font("game_font.otf", font_size)
title_font_size = 60
title_font = pygame.font.Font("game_font.otf", title_font_size)

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
    def __init__(self, alignment, color, status, number, rectangle):
        self.alignment = alignment
        self.number = number
        self.status = status
        self.color = color
        self.rectangle = rectangle


# Assign positions to a list array that is 10x10 units
def create_player_array():
    player_grid = []
    for row in range(10):
        player_grid.append([])
        for column in range(10):
            player_grid[row].append(0)
            player_grid[row][column] = Board("player", white, "empty", "empty", pygame.rect.Rect((unit_margin + unit_size) * column + 80, (unit_margin + unit_size) * row + 60, unit_size, unit_size))
    return player_grid


# Assign positions to a list array that is 10x10 units
def create_enemy_array():
    enemy_grid = []
    for row in range(10):
        enemy_grid.append([])
        for column in range(10):
            enemy_grid[row].append(0)
            enemy_grid[row][column] = Board("enemy", white, "empty", "empty", pygame.rect.Rect((unit_margin + unit_size) * column + 600, (unit_margin + unit_size) * row + 60, unit_size, unit_size))
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
                player_grid[row][column].status = "full"
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

    return "ongoing"


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

    draw_player_score(player_grid)
    draw_enemy_score(enemy_grid)

    pygame.display.flip()

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
            else:
                enemy_grid[enemy_x][enemy_y + n].number = str(m)
                enemy_grid[enemy_x][enemy_y + n].status = "full"

    return enemy_grid


# Update scores on screen for enemy based on units hit, missed, & destroyed
def draw_enemy_score(enemy_grid):
    enemy_hit = 0
    enemy_missed = 0
    enemy_destroyed = 0
    initial_ships = []
    final_ships = []

    for row in range(10):
        for column in range(10):
            if enemy_grid[row][column].status == "hit":
                enemy_hit += 1
            elif enemy_grid[row][column].status == "miss":
                enemy_missed += 1
            elif enemy_grid[row][column].status == "destroyed":
                enemy_hit += 1
                initial_ships.append((enemy_grid[row][column].alignment + "_" + enemy_grid[row][column].number))

    if len(initial_ships) > 0:
        for ship in initial_ships:
            if ship not in final_ships:
                final_ships.append(ship)
        enemy_destroyed = int(len(final_ships))

    enemy_left = 5 - enemy_destroyed

    score_rectangle = pygame.Surface((70, 180))
    score_rectangle.fill(white)
    screen.blit(score_rectangle, (845, 450))

    text = game_font.render("{}".format(enemy_hit), 1, blue)
    screen.blit(text, (875, 470))
    text = game_font.render("{}".format(enemy_missed), 1, blue)
    screen.blit(text, (875, 510))
    text = game_font.render("{}".format(enemy_destroyed), 1, blue)
    screen.blit(text, (875, 550))
    text = game_font.render("{}".format(enemy_left), 1, blue)
    screen.blit(text, (875, 590))

    text = game_font.render("HITS", 1, white)
    screen.blit(text, (785, 470))
    text = game_font.render("MISSES", 1, white)
    screen.blit(text, (758, 510))
    text = game_font.render("DESTROYED", 1, white)
    screen.blit(text, (720, 550))
    text = game_font.render("LEFT", 1, white)
    screen.blit(text, (780, 590))


# Update scores on screen for player based on units hit, missed, & destroyed
def draw_player_score(player_grid):
    player_hit = 0
    player_missed = 0
    player_destroyed = 0
    initial_ships = []
    final_ships = []

    for row in range(10):
        for column in range(10):
            if player_grid[row][column].status == "hit":
                player_hit += 1
            elif player_grid[row][column].status == "miss":
                player_missed += 1
            elif player_grid[row][column].status == "destroyed":
                player_hit += 1
                initial_ships.append((player_grid[row][column].alignment + "_" + player_grid[row][column].number))

    if len(initial_ships) > 0:
        for ship in initial_ships:
            if ship not in final_ships:
                final_ships.append(ship)
        player_destroyed = int(len(final_ships))

    player_left = 5 - player_destroyed

    score_rectangle = pygame.Surface((70, 180))
    score_rectangle.fill(white)
    screen.blit(score_rectangle, (80, 450))

    text = game_font.render("{}".format(player_hit), 1, blue)
    screen.blit(text, (110, 470))
    text = game_font.render("{}".format(player_missed), 1, blue)
    screen.blit(text, (110, 510))
    text = game_font.render("{}".format(player_destroyed), 1, blue)
    screen.blit(text, (110, 550))
    text = game_font.render("{}".format(player_left), 1, blue)
    screen.blit(text, (110, 590))

    text = game_font.render("HITS", 1, white)
    screen.blit(text, (170, 470))
    text = game_font.render("MISSES", 1, white)
    screen.blit(text, (170, 510))
    text = game_font.render("DESTROYED", 1, white)
    screen.blit(text, (170, 550))
    text = game_font.render("LEFT", 1, white)
    screen.blit(text, (170, 590))


# Check if enemy hit a player unit & change the player tile
def check_player_hit(player_grid, guess_x, guess_y):
    selected_unit = player_grid[guess_x][guess_y]

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
        return True, enemy_grid

    if selected_unit.status == "hit" or selected_unit.status == "miss" or selected_unit.status == "destroyed":
        return True, enemy_grid

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

    else:
        return True, enemy_grid

    return False, enemy_grid


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


# See if right/left/up/down of designated unit on player grid is a valid space
def valid_guess(x, y, guess_list, space):
    if space == "right":
        guess_x = x + 1
        guess_y = y
        if (guess_x, guess_y) in guess_list:
            return False
        elif guess_x >= horizontal_units:
            return False
        else:
            return True

    elif space == "left":
        guess_x = x - 1
        guess_y = y
        if (guess_x, guess_y) in guess_list:
            return False
        elif guess_x < 0:
            return False
        else:
            return True

    elif space == "up":
        guess_x = x
        guess_y = y - 1
        if (guess_x, guess_y) in guess_list:
            return False
        elif guess_y < 0:
            return False
        else:
            return True

    elif space == "down":
        guess_x = x
        guess_y = y + 1
        if (guess_x, guess_y) in guess_list:
            return False
        elif guess_y >= vertical_units:
            return False
        else:
            return True

    else:
        return False


# Check right/left/up/down of designated unit on player grid
def check_space(player_grid, x, y, guess_list, space):
    if space == "right":
        guess_x = x + 1
        guess_y = y
        guess_list.append((guess_x, guess_y))
        success, player_grid = check_player_hit(player_grid, guess_x, guess_y)

    elif space == "left":
        guess_x = x - 1
        guess_y = y
        guess_list.append((guess_x, guess_y))
        success, player_grid = check_player_hit(player_grid, guess_x, guess_y)

    elif space == "up":
        guess_x = x
        guess_y = y - 1
        guess_list.append((guess_x, guess_y))
        success, player_grid = check_player_hit(player_grid, guess_x, guess_y)

    elif space == "down":
        guess_x = x
        guess_y = y + 1
        guess_list.append((guess_x, guess_y))
        success, player_grid = check_player_hit(player_grid, guess_x, guess_y)

    return success, player_grid, guess_x, guess_y


def blind_guess(guess_list):
    random.seed()

    already_guessed = True

    while already_guessed:
        guess_x = random.randrange(horizontal_units)
        guess_y = random.randrange(vertical_units)
        if (guess_x, guess_y) not in guess_list:
            already_guessed = False
    guess_list.append((guess_x, guess_y))

    return guess_list, guess_x, guess_y


def find_hits(player_grid):
    hit_found = 0

    for row in range(10):
        for column in range(10):
            if player_grid[row][column].status == "hit" and hit_found == 0:
                previous_x = row
                previous_y = column
                first_x = row
                first_y = column
                hit_found = 1
                is_blind = False
    if hit_found != 1:
        is_blind = True
        previous_x = 0
        previous_y = 0
        first_x = 0
        first_y = 0

    return is_blind, previous_x, previous_y, first_x, first_y


# Generate random guess for enemy on player grid
# Check if unit hit but not destroyed; if so, change enemy guess to check around hit piece
def enemy_turn(player_grid, enemy_grid, is_blind, first_x, first_y, previous_x, previous_y, rotation, direction, guess_list):
    time.sleep(1)
    random.seed()
    pygame.event.pump()

    if is_blind:
        guess_list, guess_x, guess_y = blind_guess(guess_list)
        success, player_grid = check_player_hit(player_grid, guess_x, guess_y)
        if success:
            first_x = guess_x
            first_y = guess_y
            previous_x = guess_x
            previous_y = guess_y
            is_blind = False
            rotation = random.choice(("horizontal", "vertical"))
            if rotation == "horizontal":
                direction = random.choice(("right", "left"))
            else:
                direction = random.choice(("up", "down"))

    else:
        if rotation == "horizontal":
            if direction == "right":
                is_valid = valid_guess(previous_x, previous_y, guess_list, "right")
                if is_valid:
                    success, player_grid, guess_x, guess_y = check_space(player_grid, previous_x, previous_y, guess_list, "right")
                    if success:
                        if player_grid[guess_x][guess_y].status == "destroyed":
                            is_blind, previous_x, previous_y, first_x, first_y = find_hits(player_grid)
                        else:
                            previous_x = guess_x
                            previous_y = guess_y
                    else:
                        previous_x = first_x
                        previous_y = first_y
                        direction = "left"
                else:
                    is_valid = valid_guess(first_x, first_y, guess_list, "left")
                    if is_valid:
                        success, player_grid, guess_x, guess_y = check_space(player_grid, first_x, first_y, guess_list, "left")
                        if success:
                            if player_grid[guess_x][guess_y].status == "destroyed":
                                is_blind, previous_x, previous_y, first_x, first_y = find_hits(player_grid)
                            else:
                                previous_x = guess_x
                                previous_y = guess_y
                                direction = "left"
                        else:
                            previous_x = first_x
                            previous_y = first_y
                            rotation = "vertical"
                            direction = random.choice(("up", "down"))
                    else:
                        is_valid = valid_guess(first_x, first_y, guess_list, "up")
                        if is_valid:
                            success, player_grid, guess_x, guess_y = check_space(player_grid, first_x, first_y, guess_list, "up")
                            if success:
                                if player_grid[guess_x][guess_y].status == "destroyed":
                                    is_blind, previous_x, previous_y, first_x, first_y = find_hits(player_grid)
                                else:
                                    previous_x = guess_x
                                    previous_y = guess_y
                                    rotation = "vertical"
                                    direction = "up"
                            else:
                                previous_x = first_x
                                previous_y = first_y
                                rotation = "vertical"
                                direction = "down"
                        else:
                            is_valid = valid_guess(first_x, first_y, guess_list, "down")
                            if is_valid:
                                success, player_grid, guess_x, guess_y = check_space(player_grid, first_x, first_y, guess_list, "down")
                                if success:
                                    if player_grid[guess_x][guess_y].status == "destroyed":
                                        is_blind, previous_x, previous_y, first_x, first_y = find_hits(player_grid)
                                    else:
                                        previous_x = guess_x
                                        previous_y = guess_y
                                        rotation = "vertical"
                                        direction = "down"
                                else:
                                    is_blind, previous_x, previous_y, first_x, first_y = find_hits(player_grid)
                            else:
                                is_blind, previous_x, previous_y, first_x, first_y = find_hits(player_grid)
                                if is_blind:
                                    guess_list, guess_x, guess_y = blind_guess(guess_list)
                                    success, player_grid = check_player_hit(player_grid, guess_x, guess_y)
                                    if success:
                                        first_x = guess_x
                                        first_y = guess_y
                                        previous_x = guess_x
                                        previous_y = guess_y
                                        is_blind = False
                                        rotation = random.choice(("horizontal", "vertical"))
                                        if rotation == "horizontal":
                                            direction = random.choice(("right", "left"))
                                        else:
                                            direction = random.choice(("up", "down"))
                                else:
                                    enemy_turn(player_grid, enemy_grid, is_blind, first_x, first_y, previous_x, previous_y, rotation, direction, guess_list)
            elif direction == "left":
                is_valid = valid_guess(previous_x, previous_y, guess_list, "left")
                if is_valid:
                    success, player_grid, guess_x, guess_y = check_space(player_grid, previous_x, previous_y, guess_list, "left")
                    if success:
                        if player_grid[guess_x][guess_y].status == "destroyed":
                            is_blind, previous_x, previous_y, first_x, first_y = find_hits(player_grid)
                        else:
                            previous_x = guess_x
                            previous_y = guess_y
                    else:
                        previous_x = first_x
                        previous_y = first_y
                        direction = "right"
                else:
                    is_valid = valid_guess(first_x, first_y, guess_list, "right")
                    if is_valid:
                        success, player_grid, guess_x, guess_y = check_space(player_grid, first_x, first_y, guess_list, "right")
                        if success:
                            if player_grid[guess_x][guess_y].status == "destroyed":
                                is_blind, previous_x, previous_y, first_x, first_y = find_hits(player_grid)
                            else:
                                previous_x = guess_x
                                previous_y = guess_y
                                direction = "right"
                        else:
                            previous_x = first_x
                            previous_y = first_y
                            rotation = "vertical"
                            direction = random.choice(("up", "down"))
                    else:
                        is_valid = valid_guess(first_x, first_y, guess_list, "up")
                        if is_valid:
                            success, player_grid, guess_x, guess_y = check_space(player_grid, first_x, first_y,
                                                                                 guess_list, "up")
                            if success:
                                if player_grid[guess_x][guess_y].status == "destroyed":
                                    is_blind, previous_x, previous_y, first_x, first_y = find_hits(player_grid)
                                else:
                                    previous_x = guess_x
                                    previous_y = guess_y
                                    rotation = "vertical"
                                    direction = "up"
                            else:
                                previous_x = first_x
                                previous_y = first_y
                                rotation = "vertical"
                                direction = "down"
                        else:
                            is_valid = valid_guess(first_x, first_y, guess_list, "down")
                            if is_valid:
                                success, player_grid, guess_x, guess_y = check_space(player_grid, first_x, first_y,
                                                                                     guess_list, "down")
                                if success:
                                    if player_grid[guess_x][guess_y].status == "destroyed":
                                        is_blind, previous_x, previous_y, first_x, first_y = find_hits(player_grid)
                                    else:
                                        previous_x = guess_x
                                        previous_y = guess_y
                                        rotation = "vertical"
                                        direction = "down"
                                else:
                                    is_blind, previous_x, previous_y, first_x, first_y = find_hits(player_grid)
                            else:
                                is_blind, previous_x, previous_y, first_x, first_y = find_hits(player_grid)
                                if is_blind:
                                    guess_list, guess_x, guess_y = blind_guess(guess_list)
                                    success, player_grid = check_player_hit(player_grid, guess_x, guess_y)
                                    if success:
                                        first_x = guess_x
                                        first_y = guess_y
                                        previous_x = guess_x
                                        previous_y = guess_y
                                        is_blind = False
                                        rotation = random.choice(("horizontal", "vertical"))
                                        if rotation == "horizontal":
                                            direction = random.choice(("right", "left"))
                                        else:
                                            direction = random.choice(("up", "down"))
                                else:
                                    enemy_turn(player_grid, enemy_grid, is_blind, first_x, first_y, previous_x, previous_y, rotation, direction, guess_list)
        elif rotation == "vertical":
            if direction == "up":
                is_valid = valid_guess(previous_x, previous_y, guess_list, "up")
                if is_valid:
                    success, player_grid, guess_x, guess_y = check_space(player_grid, previous_x, previous_y, guess_list, "up")
                    if success:
                        if player_grid[guess_x][guess_y].status == "destroyed":
                            is_blind, previous_x, previous_y, first_x, first_y = find_hits(player_grid)
                        else:
                            previous_x = guess_x
                            previous_y = guess_y
                    else:
                        previous_x = first_x
                        previous_y = first_y
                        direction = "down"
                else:
                    is_valid = valid_guess(first_x, first_y, guess_list, "down")
                    if is_valid:
                        success, player_grid, guess_x, guess_y = check_space(player_grid, first_x, first_y, guess_list, "down")
                        if success:
                            if player_grid[guess_x][guess_y].status == "destroyed":
                                is_blind, previous_x, previous_y, first_x, first_y = find_hits(player_grid)
                            else:
                                previous_x = guess_x
                                previous_y = guess_y
                                direction = "down"
                        else:
                            previous_x = first_x
                            previous_y = first_y
                            rotation = "horizontal"
                            direction = random.choice(("right", "left"))
                    else:
                        is_valid = valid_guess(first_x, first_y, guess_list, "right")
                        if is_valid:
                            success, player_grid, guess_x, guess_y = check_space(player_grid, first_x, first_y, guess_list, "right")
                            if success:
                                if player_grid[guess_x][guess_y].status == "destroyed":
                                    is_blind, previous_x, previous_y, first_x, first_y = find_hits(player_grid)
                                else:
                                    previous_x = guess_x
                                    previous_y = guess_y
                                    rotation = "horizontal"
                                    direction = "right"
                            else:
                                previous_x = first_x
                                previous_y = first_y
                                rotation = "horizontal"
                                direction = "left"
                        else:
                            is_valid = valid_guess(first_x, first_y, guess_list, "left")
                            if is_valid:
                                success, player_grid, guess_x, guess_y = check_space(player_grid, first_x, first_y, guess_list, "left")
                                if success:
                                    if player_grid[guess_x][guess_y].status == "destroyed":
                                        is_blind, previous_x, previous_y, first_x, first_y = find_hits(player_grid)
                                    else:
                                        previous_x = guess_x
                                        previous_y = guess_y
                                        rotation = "horizontal"
                                        direction = "left"
                                else:
                                    is_blind, previous_x, previous_y, first_x, first_y = find_hits(player_grid)
                            else:
                                is_blind, previous_x, previous_y, first_x, first_y = find_hits(player_grid)
                                if is_blind:
                                    guess_list, guess_x, guess_y = blind_guess(guess_list)
                                    success, player_grid = check_player_hit(player_grid, guess_x, guess_y)
                                    if success:
                                        first_x = guess_x
                                        first_y = guess_y
                                        previous_x = guess_x
                                        previous_y = guess_y
                                        is_blind = False
                                        rotation = random.choice(("horizontal", "vertical"))
                                        if rotation == "horizontal":
                                            direction = random.choice(("right", "left"))
                                        else:
                                            direction = random.choice(("up", "down"))
                                else:
                                    enemy_turn(player_grid, enemy_grid, is_blind, first_x, first_y, previous_x, previous_y, rotation, direction, guess_list)
            elif direction == "down":
                is_valid = valid_guess(previous_x, previous_y, guess_list, "down")
                if is_valid:
                    success, player_grid, guess_x, guess_y = check_space(player_grid, previous_x, previous_y, guess_list, "down")
                    if success:
                        if player_grid[guess_x][guess_y].status == "destroyed":
                            is_blind, previous_x, previous_y, first_x, first_y = find_hits(player_grid)
                        else:
                            previous_x = guess_x
                            previous_y = guess_y
                    else:
                        previous_x = first_x
                        previous_y = first_y
                        direction = "up"
                else:
                    is_valid = valid_guess(first_x, first_y, guess_list, "up")
                    if is_valid:
                        success, player_grid, guess_x, guess_y = check_space(player_grid, first_x, first_y, guess_list, "up")
                        if success:
                            if player_grid[guess_x][guess_y].status == "destroyed":
                                is_blind, previous_x, previous_y, first_x, first_y = find_hits(player_grid)
                            else:
                                previous_x = guess_x
                                previous_y = guess_y
                                direction = "up"
                        else:
                            previous_x = first_x
                            previous_y = first_y
                            rotation = "horizontal"
                            direction = random.choice(("right", "left"))
                    else:
                        is_valid = valid_guess(first_x, first_y, guess_list, "right")
                        if is_valid:
                            success, player_grid, guess_x, guess_y = check_space(player_grid, first_x, first_y, guess_list, "right")
                            if success:
                                if player_grid[guess_x][guess_y].status == "destroyed":
                                    is_blind, previous_x, previous_y, first_x, first_y = find_hits(player_grid)
                                else:
                                    previous_x = guess_x
                                    previous_y = guess_y
                                    rotation = "horizontal"
                                    direction = "right"
                            else:
                                previous_x = first_x
                                previous_y = first_y
                                rotation = "horizontal"
                                direction = "left"
                        else:
                            is_valid = valid_guess(first_x, first_y, guess_list, "left")
                            if is_valid:
                                success, player_grid, guess_x, guess_y = check_space(player_grid, first_x, first_y, guess_list, "left")
                                if success:
                                    if player_grid[guess_x][guess_y].status == "destroyed":
                                        is_blind, previous_x, previous_y, first_x, first_y = find_hits(player_grid)
                                    else:
                                        previous_x = guess_x
                                        previous_y = guess_y
                                        rotation = "horizontal"
                                        direction = "left"
                                else:
                                    is_blind, previous_x, previous_y, first_x, first_y = find_hits(player_grid)
                            else:
                                is_blind, previous_x, previous_y, first_x, first_y = find_hits(player_grid)
                                if is_blind:
                                    guess_list, guess_x, guess_y = blind_guess(guess_list)
                                    success, player_grid = check_player_hit(player_grid, guess_x, guess_y)
                                    if success:
                                        first_x = guess_x
                                        first_y = guess_y
                                        previous_x = guess_x
                                        previous_y = guess_y
                                        is_blind = False
                                        rotation = random.choice(("horizontal", "vertical"))
                                        if rotation == "horizontal":
                                            direction = random.choice(("right", "left"))
                                        else:
                                            direction = random.choice(("up", "down"))
                                else:
                                    enemy_turn(player_grid, enemy_grid, is_blind, first_x, first_y, previous_x, previous_y, rotation, direction, guess_list)

    draw_playing_window(player_grid, enemy_grid)

    return player_grid, enemy_grid, is_blind, first_x, first_y, previous_x, previous_y, rotation, direction, guess_list


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
                    guessing, enemy_grid = check_enemy_hit(event.pos, enemy_grid)

    draw_playing_window(player_grid, enemy_grid)

    return player_grid, enemy_grid


# Victory sub-menu
def victory_menu(enemy_grid):
    screen.fill(blue)

    draw_enemy_grid(enemy_grid)
    draw_enemy_score(enemy_grid)

    text = title_font.render("YOU WON!", 1, white)
    screen.blit(text, (210, 110))

    play_again_button = pygame.Rect(150, 170, 300, 60)
    quit_button = pygame.Rect(150, 250, 300, 60)

    pygame.draw.rect(screen, white, play_again_button)
    pygame.draw.rect(screen, white, quit_button)

    text = game_font.render("play again", 1, blue)
    screen.blit(text, (250, 190))
    text = game_font.render("quit", 1, blue)
    screen.blit(text, (280, 270))

    pygame.display.flip()

    pygame.event.pump()
    selecting = True

    while selecting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if play_again_button.collidepoint(event.pos):
                        return "play again"
                    elif quit_button.collidepoint(event.pos):
                        return "quit"


# Defeat sub-menu
def defeat_menu(player_grid):
    screen.fill(blue)

    draw_player_grid(player_grid)
    draw_player_score(player_grid)

    text = title_font.render("YOU LOST!", 1, white)
    screen.blit(text, (660, 110))

    play_again_button = pygame.Rect(600, 170, 300, 60)
    quit_button = pygame.Rect(600, 250, 300, 60)

    pygame.draw.rect(screen, white, play_again_button)
    pygame.draw.rect(screen, white, quit_button)

    text = game_font.render("play again", 1, blue)
    screen.blit(text, (700, 190))
    text = game_font.render("quit", 1, blue)
    screen.blit(text, (730, 270))

    pygame.display.flip()

    pygame.event.pump()
    selecting = True

    while selecting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if play_again_button.collidepoint(event.pos):
                        return "play again"
                    elif quit_button.collidepoint(event.pos):
                        return "quit"


# Main function
def main():

    prepping = True
    running = True
    clock = pygame.time.Clock()

    is_blind = True
    first_x = 0
    first_y = 0
    previous_x = 0
    previous_y = 0
    orientation = None
    direction = None
    guess_list = []

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if prepping:
            player_grid, enemy_grid = pre_game()
            prepping = False

        end_game = "ongoing"
        while end_game == "ongoing":
            player_grid, enemy_grid = player_turn(player_grid, enemy_grid)
            end_game = check_end_game(player_grid, enemy_grid)
            if end_game == "ongoing":
                player_grid, enemy_grid, is_blind, first_x, first_y, previous_x, previous_y, orientation, direction, guess_list = enemy_turn(player_grid, enemy_grid, is_blind, first_x, first_y, previous_x, previous_y, orientation, direction, guess_list)
                end_game = check_end_game(player_grid, enemy_grid)

        if end_game == "victory":
            selection = victory_menu(enemy_grid)
        elif end_game == "defeat":
            selection = defeat_menu(player_grid)

        if selection == "quit":
            running = False
        elif selection == "play again":
            main()

    pygame.display.flip()
    clock.tick(fps)

    pygame.quit()


# Main menu before game starts that prompts player to either begin or quit; calls the Main function
def main_menu():
    screen.fill(blue)

    text = title_font.render("BATTLESHIP", 1, white)
    screen.blit(text, (393, 200))

    start_button = pygame.Rect(350, 270, 300, 60)
    quit_button = pygame.Rect(350, 350, 300, 60)

    pygame.draw.rect(screen, white, start_button)
    pygame.draw.rect(screen, white, quit_button)

    text = game_font.render("start game", 1, blue)
    screen.blit(text, (440, 290))
    text = game_font.render("quit", 1, blue)
    screen.blit(text, (485, 370))

    pygame.display.flip()

    selecting = True

    while selecting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if start_button.collidepoint(event.pos):
                        main()
                    elif quit_button.collidepoint(event.pos):
                        pygame.quit()


main_menu()

pygame.quit()
