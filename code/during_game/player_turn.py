from g_func import g_var
import pygame


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
        selected_unit.color = g_var.blue

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
                        enemy_grid[row][column].color = g_var.red
        else:
            selected_unit.status = "hit"
            selected_unit.color = g_var.orange

    else:
        return True, enemy_grid

    return False, enemy_grid


# Handle all actions for a player turn
def player_turn(player_grid, enemy_grid):
    from during_game import during
    guessing = True

    during.draw_playing_window(player_grid, enemy_grid)

    while guessing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    guessing, enemy_grid = check_enemy_hit(event.pos, enemy_grid)

    during.draw_playing_window(player_grid, enemy_grid)

    return player_grid, enemy_grid
