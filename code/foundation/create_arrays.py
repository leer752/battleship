from foundation import class_Board
from g_func import g_var
import pygame


# Assign positions to a list array that is 10x10 units
def create_player_array():
    player_grid = []
    size_margin = g_var.unit_margin + g_var.unit_size
    for row in range(10):
        player_grid.append([])
        for col in range(10):
            player_grid[row].append(0)
            square = [size_margin * col + 80, size_margin * row + 60, g_var.unit_size, g_var.unit_size]
            player_grid[row][col] = class_Board.Board("player", g_var.white, "empty", "empty", pygame.Rect(square))
    return player_grid


# Assign positions to a list array that is 10x10 units
def create_enemy_array():
    enemy_grid = []
    size_margin = g_var.unit_margin + g_var.unit_size
    for row in range(10):
        enemy_grid.append([])
        for col in range(10):
            enemy_grid[row].append(0)
            square = [size_margin * col + 600, size_margin * row + 60, g_var.unit_size, g_var.unit_size]
            enemy_grid[row][col] = class_Board.Board("enemy", g_var.white, "empty", "empty", pygame.Rect(square))
    return enemy_grid
