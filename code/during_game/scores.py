import pygame
from foundation import init_screen
from g_func import g_var


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
    score_rectangle.fill(g_var.white)
    init_screen.screen.blit(score_rectangle, (845, 450))

    text = g_var.game_font.render("{}".format(enemy_hit), 1, g_var.blue)
    init_screen.screen.blit(text, (875, 470))
    text = g_var.game_font.render("{}".format(enemy_missed), 1, g_var.blue)
    init_screen.screen.blit(text, (875, 510))
    text = g_var.game_font.render("{}".format(enemy_destroyed), 1, g_var.blue)
    init_screen.screen.blit(text, (875, 550))
    text = g_var.game_font.render("{}".format(enemy_left), 1, g_var.blue)
    init_screen.screen.blit(text, (875, 590))

    text = g_var.game_font.render("HITS", 1, g_var.white)
    init_screen.screen.blit(text, (785, 470))
    text = g_var.game_font.render("MISSES", 1, g_var.white)
    init_screen.screen.blit(text, (758, 510))
    text = g_var.game_font.render("DESTROYED", 1, g_var.white)
    init_screen.screen.blit(text, (720, 550))
    text = g_var.game_font.render("LEFT", 1, g_var.white)
    init_screen.screen.blit(text, (780, 590))


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
    score_rectangle.fill(g_var.white)
    init_screen.screen.blit(score_rectangle, (80, 450))

    text = g_var.game_font.render("{}".format(player_hit), 1, g_var.blue)
    init_screen.screen.blit(text, (110, 470))
    text = g_var.game_font.render("{}".format(player_missed), 1, g_var.blue)
    init_screen.screen.blit(text, (110, 510))
    text = g_var.game_font.render("{}".format(player_destroyed), 1, g_var.blue)
    init_screen.screen.blit(text, (110, 550))
    text = g_var.game_font.render("{}".format(player_left), 1, g_var.blue)
    init_screen.screen.blit(text, (110, 590))

    text = g_var.game_font.render("HITS", 1, g_var.white)
    init_screen.screen.blit(text, (170, 470))
    text = g_var.game_font.render("MISSES", 1, g_var.white)
    init_screen.screen.blit(text, (170, 510))
    text = g_var.game_font.render("DESTROYED", 1, g_var.white)
    init_screen.screen.blit(text, (170, 550))
    text = g_var.game_font.render("LEFT", 1, g_var.white)
    init_screen.screen.blit(text, (170, 590))
