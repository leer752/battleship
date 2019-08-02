import pygame


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


# Draw the ongoing game screen
# Shows both grids & scores
def draw_playing_window(player_grid, enemy_grid):
    from foundation import init_screen
    from g_func import g_var, draw_grids
    from during_game import scores

    init_screen.screen.fill(g_var.blue)

    draw_grids.draw_player_grid(player_grid)
    draw_grids.draw_enemy_grid(enemy_grid)

    scores.draw_player_score(player_grid)
    scores.draw_enemy_score(enemy_grid)

    pygame.display.flip()
