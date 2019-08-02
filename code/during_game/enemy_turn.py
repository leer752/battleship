import pygame
from g_func import g_var


# Check if enemy hit a player unit & change the player tile
def check_player_hit(player_grid, guess_x, guess_y):
    selected_unit = player_grid[guess_x][guess_y]

    if selected_unit.status == "empty":
        selected_unit.status = "miss"
        selected_unit.color = g_var.blue
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
                        player_grid[row][column].color = g_var.red
        else:
            selected_unit.status = "hit"
            selected_unit.color = g_var.orange

    return True, player_grid


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
    import random
    random.seed()

    already_guessed = True

    while already_guessed:
        guess_x = random.randrange(g_var.horizontal_units)
        guess_y = random.randrange(g_var.vertical_units)
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
    import time
    import random
    from during_game import valid

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
                is_valid = valid.valid_guess(previous_x, previous_y, guess_list, "right")
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
                    is_valid = valid.valid_guess(first_x, first_y, guess_list, "left")
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
                        is_valid = valid.valid_guess(first_x, first_y, guess_list, "up")
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
                            is_valid = valid.valid_guess(first_x, first_y, guess_list, "down")
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
                is_valid = valid.valid_guess(previous_x, previous_y, guess_list, "left")
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
                    is_valid = valid.valid_guess(first_x, first_y, guess_list, "right")
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
                        is_valid = valid.valid_guess(first_x, first_y, guess_list, "up")
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
                            is_valid = valid.valid_guess(first_x, first_y, guess_list, "down")
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
                is_valid = valid.valid_guess(previous_x, previous_y, guess_list, "up")
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
                    is_valid = valid.valid_guess(first_x, first_y, guess_list, "down")
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
                        is_valid = valid.valid_guess(first_x, first_y, guess_list, "right")
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
                            is_valid = valid.valid_guess(first_x, first_y, guess_list, "left")
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
                is_valid = valid.valid_guess(previous_x, previous_y, guess_list, "down")
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
                    is_valid = valid.valid_guess(first_x, first_y, guess_list, "up")
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
                        is_valid = valid.valid_guess(first_x, first_y, guess_list, "right")
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
                            is_valid = valid.valid_guess(first_x, first_y, guess_list, "left")
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

    from during_game import during
    during.draw_playing_window(player_grid, enemy_grid)

    return player_grid, enemy_grid, is_blind, first_x, first_y, previous_x, previous_y, rotation, direction, guess_list
