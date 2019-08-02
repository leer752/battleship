import pygame
from foundation import init_screen
from g_func import g_var


# Draw the player grid & display it on the screen for the user
def draw_player_grid(player_grid):
    for row in range(10):
        for col in range(10):
            pygame.draw.rect(init_screen.screen, player_grid[row][col].color, player_grid[row][col].rectangle)
    text = g_var.game_font.render("Player (YOU)", 1, g_var.white)
    init_screen.screen.blit(text, (175, 23))


# Draw the enemy grid & display it on the screen for the user
# Keep in mind that enemy tiles are "covered"; the user cannot see the enemy ships
def draw_enemy_grid(enemy_grid):
    for row in range(10):
        for col in range(10):
            pygame.draw.rect(init_screen.screen, enemy_grid[row][col].color, enemy_grid[row][col].rectangle)
    text = g_var.game_font.render("Enemy", 1, g_var.white)
    init_screen.screen.blit(text, (735, 23))
