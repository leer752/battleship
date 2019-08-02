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


def blind_guess(guesses):
    import random
    random.seed()

    already_guessed = True

    while already_guessed:
        guess_x = random.randrange(g_var.horizontal_units)
        guess_y = random.randrange(g_var.vertical_units)
        if (guess_x, guess_y) not in guesses:
            already_guessed = False
    guesses.append((guess_x, guess_y))

    return guesses, guess_x, guess_y


def find_hits(player_grid):
    hit_found = 0

    for row in range(10):
        for column in range(10):
            if player_grid[row][column].status == "hit" and hit_found == 0:
                prev_x = row
                prev_y = column
                init_x = row
                init_y = column
                hit_found = 1
                blind = False
    if hit_found != 1:
        blind = True
        prev_x = 0
        prev_y = 0
        init_x = 0
        init_y = 0

    return blind, prev_x, prev_y, init_x, init_y


# Generate random guess for enemy on player grid
# Check if unit hit but not destroyed; if so, change enemy guess to check around hit piece
def enemy_turn(player_grid, enemy_grid, is_blind, init_x, init_y, prev_x, prev_y, align, way, guesses):
    import time
    import random
    from during_game import valid

    time.sleep(1)
    random.seed()
    pygame.event.pump()

    if is_blind:
        guesses, x, y = blind_guess(guesses)
        success, player_grid = check_player_hit(player_grid, x, y)
        if success:
            init_x = x
            init_y = y
            prev_x = x
            prev_y = y
            is_blind = False
            align = random.choice(("horizontal", "vertical"))
            if align == "horizontal":
                way = random.choice(("right", "left"))
            else:
                way = random.choice(("up", "down"))

    else:
        if align == "horizontal":
            if way == "right":
                is_valid = valid.valid_guess(prev_x, prev_y, guesses, "right")
                if is_valid:
                    success, player_grid, x, y = check_space(player_grid, prev_x, prev_y, guesses, "right")
                    if success:
                        if player_grid[x][y].status == "destroyed":
                            is_blind, prev_x, prev_y, init_x, init_y = find_hits(player_grid)
                        else:
                            prev_x = x
                            prev_y = y
                    else:
                        prev_x = init_x
                        prev_y = init_y
                        way = "left"
                else:
                    is_valid = valid.valid_guess(init_x, init_y, guesses, "left")
                    if is_valid:
                        success, player_grid, x, y = check_space(player_grid, init_x, init_y, guesses, "left")
                        if success:
                            if player_grid[x][y].status == "destroyed":
                                is_blind, prev_x, prev_y, init_x, init_y = find_hits(player_grid)
                            else:
                                prev_x = x
                                prev_y = y
                                way = "left"
                        else:
                            prev_x = init_x
                            prev_y = init_y
                            align = "vertical"
                            way = random.choice(("up", "down"))
                    else:
                        is_valid = valid.valid_guess(init_x, init_y, guesses, "up")
                        if is_valid:
                            success, player_grid, x, y = check_space(player_grid, init_x, init_y, guesses, "up")
                            if success:
                                if player_grid[x][y].status == "destroyed":
                                    is_blind, prev_x, prev_y, init_x, init_y = find_hits(player_grid)
                                else:
                                    prev_x = x
                                    prev_y = y
                                    align = "vertical"
                                    way = "up"
                            else:
                                prev_x = init_x
                                prev_y = init_y
                                align = "vertical"
                                way = "down"
                        else:
                            is_valid = valid.valid_guess(init_x, init_y, guesses, "down")
                            if is_valid:
                                success, player_grid, x, y = check_space(player_grid, init_x, init_y, guesses, "down")
                                if success:
                                    if player_grid[x][y].status == "destroyed":
                                        is_blind, prev_x, prev_y, init_x, init_y = find_hits(player_grid)
                                    else:
                                        prev_x = x
                                        prev_y = y
                                        align = "vertical"
                                        way = "down"
                                else:
                                    is_blind, prev_x, prev_y, init_x, init_y = find_hits(player_grid)
                            else:
                                is_blind, prev_x, prev_y, init_x, init_y = find_hits(player_grid)
                                if is_blind:
                                    guesses, x, y = blind_guess(guesses)
                                    success, player_grid = check_player_hit(player_grid, x, y)
                                    if success:
                                        init_x = x
                                        init_y = y
                                        prev_x = x
                                        prev_y = y
                                        is_blind = False
                                        align = random.choice(("horizontal", "vertical"))
                                        if align == "horizontal":
                                            way = random.choice(("right", "left"))
                                        else:
                                            way = random.choice(("up", "down"))
                                else:
                                    enemy_turn(player_grid, enemy_grid, is_blind, init_x, init_y, prev_x, prev_y, align,
                                               way, guesses)
            elif way == "left":
                is_valid = valid.valid_guess(prev_x, prev_y, guesses, "left")
                if is_valid:
                    success, player_grid, x, y = check_space(player_grid, prev_x, prev_y, guesses, "left")
                    if success:
                        if player_grid[x][y].status == "destroyed":
                            is_blind, prev_x, prev_y, init_x, init_y = find_hits(player_grid)
                        else:
                            prev_x = x
                            prev_y = y
                    else:
                        prev_x = init_x
                        prev_y = init_y
                        way = "right"
                else:
                    is_valid = valid.valid_guess(init_x, init_y, guesses, "right")
                    if is_valid:
                        success, player_grid, x, y = check_space(player_grid, init_x, init_y, guesses, "right")
                        if success:
                            if player_grid[x][y].status == "destroyed":
                                is_blind, prev_x, prev_y, init_x, init_y = find_hits(player_grid)
                            else:
                                prev_x = x
                                prev_y = y
                                way = "right"
                        else:
                            prev_x = init_x
                            prev_y = init_y
                            align = "vertical"
                            way = random.choice(("up", "down"))
                    else:
                        is_valid = valid.valid_guess(init_x, init_y, guesses, "up")
                        if is_valid:
                            success, player_grid, x, y = check_space(player_grid, init_x, init_y, guesses, "up")
                            if success:
                                if player_grid[x][y].status == "destroyed":
                                    is_blind, prev_x, prev_y, init_x, init_y = find_hits(player_grid)
                                else:
                                    prev_x = x
                                    prev_y = y
                                    align = "vertical"
                                    way = "up"
                            else:
                                prev_x = init_x
                                prev_y = init_y
                                align = "vertical"
                                way = "down"
                        else:
                            is_valid = valid.valid_guess(init_x, init_y, guesses, "down")
                            if is_valid:
                                success, player_grid, x, y = check_space(player_grid, init_x, init_y, guesses, "down")
                                if success:
                                    if player_grid[x][y].status == "destroyed":
                                        is_blind, prev_x, prev_y, init_x, init_y = find_hits(player_grid)
                                    else:
                                        prev_x = x
                                        prev_y = y
                                        align = "vertical"
                                        way = "down"
                                else:
                                    is_blind, prev_x, prev_y, init_x, init_y = find_hits(player_grid)
                            else:
                                is_blind, prev_x, prev_y, init_x, init_y = find_hits(player_grid)
                                if is_blind:
                                    guesses, x, y = blind_guess(guesses)
                                    success, player_grid = check_player_hit(player_grid, x, y)
                                    if success:
                                        init_x = x
                                        init_y = y
                                        prev_x = x
                                        prev_y = y
                                        is_blind = False
                                        align = random.choice(("horizontal", "vertical"))
                                        if align == "horizontal":
                                            way = random.choice(("right", "left"))
                                        else:
                                            way = random.choice(("up", "down"))
                                else:
                                    enemy_turn(player_grid, enemy_grid, is_blind, init_x, init_y, prev_x, prev_y, align,
                                               way, guesses)
        elif align == "vertical":
            if way == "up":
                is_valid = valid.valid_guess(prev_x, prev_y, guesses, "up")
                if is_valid:
                    success, player_grid, x, y = check_space(player_grid, prev_x, prev_y, guesses, "up")
                    if success:
                        if player_grid[x][y].status == "destroyed":
                            is_blind, prev_x, prev_y, init_x, init_y = find_hits(player_grid)
                        else:
                            prev_x = x
                            prev_y = y
                    else:
                        prev_x = init_x
                        prev_y = init_y
                        way = "down"
                else:
                    is_valid = valid.valid_guess(init_x, init_y, guesses, "down")
                    if is_valid:
                        success, player_grid, x, y = check_space(player_grid, init_x, init_y, guesses, "down")
                        if success:
                            if player_grid[x][y].status == "destroyed":
                                is_blind, prev_x, prev_y, init_x, init_y = find_hits(player_grid)
                            else:
                                prev_x = x
                                prev_y = y
                                way = "down"
                        else:
                            prev_x = init_x
                            prev_y = init_y
                            align = "horizontal"
                            way = random.choice(("right", "left"))
                    else:
                        is_valid = valid.valid_guess(init_x, init_y, guesses, "right")
                        if is_valid:
                            success, player_grid, x, y = check_space(player_grid, init_x, init_y, guesses, "right")
                            if success:
                                if player_grid[x][y].status == "destroyed":
                                    is_blind, prev_x, prev_y, init_x, init_y = find_hits(player_grid)
                                else:
                                    prev_x = x
                                    prev_y = y
                                    align = "horizontal"
                                    way = "right"
                            else:
                                prev_x = init_x
                                prev_y = init_y
                                align = "horizontal"
                                way = "left"
                        else:
                            is_valid = valid.valid_guess(init_x, init_y, guesses, "left")
                            if is_valid:
                                success, player_grid, x, y = check_space(player_grid, init_x, init_y, guesses, "left")
                                if success:
                                    if player_grid[x][y].status == "destroyed":
                                        is_blind, prev_x, prev_y, init_x, init_y = find_hits(player_grid)
                                    else:
                                        prev_x = x
                                        prev_y = y
                                        align = "horizontal"
                                        way = "left"
                                else:
                                    is_blind, prev_x, prev_y, init_x, init_y = find_hits(player_grid)
                            else:
                                is_blind, prev_x, prev_y, init_x, init_y = find_hits(player_grid)
                                if is_blind:
                                    guesses, x, y = blind_guess(guesses)
                                    success, player_grid = check_player_hit(player_grid, x, y)
                                    if success:
                                        init_x = x
                                        init_y = y
                                        prev_x = x
                                        prev_y = y
                                        is_blind = False
                                        align = random.choice(("horizontal", "vertical"))
                                        if align == "horizontal":
                                            way = random.choice(("right", "left"))
                                        else:
                                            way = random.choice(("up", "down"))
                                else:
                                    enemy_turn(player_grid, enemy_grid, is_blind, init_x, init_y, prev_x, prev_y, align,
                                               way, guesses)
            elif way == "down":
                is_valid = valid.valid_guess(prev_x, prev_y, guesses, "down")
                if is_valid:
                    success, player_grid, x, y = check_space(player_grid, prev_x, prev_y, guesses, "down")
                    if success:
                        if player_grid[x][y].status == "destroyed":
                            is_blind, prev_x, prev_y, init_x, init_y = find_hits(player_grid)
                        else:
                            prev_x = x
                            prev_y = y
                    else:
                        prev_x = init_x
                        prev_y = init_y
                        way = "up"
                else:
                    is_valid = valid.valid_guess(init_x, init_y, guesses, "up")
                    if is_valid:
                        success, player_grid, x, y = check_space(player_grid, init_x, init_y, guesses, "up")
                        if success:
                            if player_grid[x][y].status == "destroyed":
                                is_blind, prev_x, prev_y, init_x, init_y = find_hits(player_grid)
                            else:
                                prev_x = x
                                prev_y = y
                                way = "up"
                        else:
                            prev_x = init_x
                            prev_y = init_y
                            align = "horizontal"
                            way = random.choice(("right", "left"))
                    else:
                        is_valid = valid.valid_guess(init_x, init_y, guesses, "right")
                        if is_valid:
                            success, player_grid, x, y = check_space(player_grid, init_x, init_y, guesses, "right")
                            if success:
                                if player_grid[x][y].status == "destroyed":
                                    is_blind, prev_x, prev_y, init_x, init_y = find_hits(player_grid)
                                else:
                                    prev_x = x
                                    prev_y = y
                                    align = "horizontal"
                                    way = "right"
                            else:
                                prev_x = init_x
                                prev_y = init_y
                                align = "horizontal"
                                way = "left"
                        else:
                            is_valid = valid.valid_guess(init_x, init_y, guesses, "left")
                            if is_valid:
                                success, player_grid, x, y = check_space(player_grid, init_x, init_y, guesses, "left")
                                if success:
                                    if player_grid[x][y].status == "destroyed":
                                        is_blind, prev_x, prev_y, init_x, init_y = find_hits(player_grid)
                                    else:
                                        prev_x = x
                                        prev_y = y
                                        align = "horizontal"
                                        way = "left"
                                else:
                                    is_blind, prev_x, prev_y, init_x, init_y = find_hits(player_grid)
                            else:
                                is_blind, prev_x, prev_y, init_x, init_y = find_hits(player_grid)
                                if is_blind:
                                    guesses, x, y = blind_guess(guesses)
                                    success, player_grid = check_player_hit(player_grid, x, y)
                                    if success:
                                        init_x = x
                                        init_y = y
                                        prev_x = x
                                        prev_y = y
                                        is_blind = False
                                        align = random.choice(("horizontal", "vertical"))
                                        if align == "horizontal":
                                            way = random.choice(("right", "left"))
                                        else:
                                            way = random.choice(("up", "down"))
                                else:
                                    enemy_turn(player_grid, enemy_grid, is_blind, init_x, init_y, prev_x, prev_y, align,
                                               way, guesses)

    from during_game import during
    during.draw_playing_window(player_grid, enemy_grid)

    return player_grid, enemy_grid, is_blind, init_x, init_y, prev_x, prev_y, align, way, guesses
