import pygame
from g_func import g_var


# Initialize screen & set sentinel value for main
def init():
    global screen
    screen = pygame.display.set_mode((g_var.screen_width, g_var.screen_height))
    pygame.display.set_caption("Battleship")