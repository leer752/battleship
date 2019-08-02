from foundation import class_Board
from g_func import g_var
import pygame


# Assign positions to a list array that is 10x10 units
def create_player_array():
    player_grid = []
    for row in range(10):
        player_grid.append([])
        for column in range(10):
            player_grid[row].append(0)
            player_grid[row][column] = class_Board.Board("player", g_var.white, "empty", "empty", pygame.Rect((g_var.unit_margin + g_var.unit_size) * column + 80, (g_var.unit_margin + g_var.unit_size) * row + 60, g_var.unit_size, g_var.unit_size))
    return player_grid


# Assign positions to a list array that is 10x10 units
def create_enemy_array():
    enemy_grid = []
    for row in range(10):
        enemy_grid.append([])
        for column in range(10):
            enemy_grid[row].append(0)
            enemy_grid[row][column] = class_Board.Board("enemy", g_var.white, "empty", "empty", pygame.Rect((g_var.unit_margin + g_var.unit_size) * column + 600, (g_var.unit_margin + g_var.unit_size) * row + 60, g_var.unit_size, g_var.unit_size))
    return enemy_grid
