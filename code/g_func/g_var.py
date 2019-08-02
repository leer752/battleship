import pygame


# Global variables
def init():
    global fps
    fps = 60

    global screen_width, screen_height, screen_height_margin, screen_width_margin
    screen_width = 1000
    screen_height = 700
    screen_height_margin = 100
    screen_width_margin = 50

    global horizontal_units, vertical_units
    horizontal_units = 10
    vertical_units = 10

    global unit_margin, unit_size
    unit_margin = 7
    unit_size = 25

    global font_size, game_font, title_font_size, title_font
    font_size = 30
    game_font = pygame.font.Font(".//assets//game_font.otf", font_size)
    title_font_size = 60
    title_font = pygame.font.Font(".//assets//game_font.otf", title_font_size)

    global red, blue, green, orange, white, black
    red = (255, 51, 51)
    blue = (153, 204, 255)
    green = (205, 235, 139)
    orange = (255, 128, 0)
    white = (255, 255, 255)
    black = (0, 0, 0)