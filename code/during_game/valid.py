from g_func import g_var
from foundation import prep
import pygame


# Check that a ship piece is being placed in a valid area on the player grid
# Piece must not overlap another ship or be placed off the grid
def valid_player_space(checking_ship, ship_number, placed_ships, player_grid, enemy_grid, orientation):
    grid_width = (g_var.unit_size * g_var.horizontal_units) + (g_var.unit_margin * (g_var.horizontal_units - 1))
    grid_height = (g_var.unit_size * g_var.vertical_units) + (g_var.unit_margin * (g_var.vertical_units - 1))
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
                if player_grid[row][column].color != g_var.white:
                    return False, player_grid
                else:
                    counting_units += 1

    if counting_units > units:
        return False, player_grid

    for row in range(10):
        for column in range(10):
            if pygame.Rect.colliderect(checking_ship, player_grid[row][column].rectangle):
                player_grid[row][column].color = g_var.green
                player_grid[row][column].number = str(ship_number)
                player_grid[row][column].status = "full"
                prep.draw_starting_window(placed_ships, player_grid, enemy_grid, orientation)

    return True, player_grid


# See if right/left/up/down of designated unit on player grid is a valid space
def valid_guess(x, y, guess_list, space):
    if space == "right":
        guess_x = x + 1
        guess_y = y
        if (guess_x, guess_y) in guess_list:
            return False
        elif guess_x >= g_var.horizontal_units:
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
        elif guess_y >= g_var.vertical_units:
            return False
        else:
            return True

    else:
        return False
