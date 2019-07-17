import pygame
import random

pygame.init()

# Global variables
screen_width = 1200
screen_height = 800
screen_height_margin = 100
screen_width_margin = 50

horizontal_units = 10
vertical_units = 10

unit_margin = 10
unit_size = 25

between_grids = 300

fontsize = 30
game_font = pygame.font.Font("C:\\Users\\bnr752\\PycharmProjects\\battleship\\assets\\molor.otf", fontsize)

red = (255, 51, 51)
blue = (153, 204, 255)
green = (205, 235, 139)
orange = (255, 128, 0)
white = (255, 255, 255)
black = (0, 0, 0)

# Initialize screen & set sentinel value for main
screen = pygame.display.set_mode(screen_width, screen_height)
pygame.display.set_caption("Battleship")


# Create a class object that represents a ship as a whole
# __init__ function defines the ship's X & Y values, how many units it has, & if it is vertical or horizontal
class Ship(object):
    def __init__(self, x, y, units):
        self.x = x
        self.y = y
        self.units = units
        self.rotation = 0


# Assign positions to a list array that is 10x10 units
def create_player_array():
    pass


# Assign positions to a list array that is 10x10 units
def create_enemy_array():
    pass


# Draw the player grid & display it on the screen for the user
def draw_player_grid():
    pass


# Draw the enemy grid & display it on the screen for the user
# Keep in mind that enemy tiles are "covered"; the user cannot see the enemy ships
def draw_enemy_grid():
    pass


# Check that a ship piece is being placed in a valid area on the player grid
# Piece must not overlap another ship or be placed off the grid
def valid_player_space():
    pass


# Check that a ship piece is being placed in a valid area on the enemy grid
# Piece must not overlap another ship or be placed off the grid
def valid_enemy_space():
    pass


# Check if the player has lost the game
def check_lost():
    pass


# Check if the player has won the game
def check_win():
    pass


# Draw the game preparation screen
# Shows both grids (player & enemy) & ship inventory
def draw_starting_window():
    pass


# Draw the ongoing game screen
# Shows both grids & scores
def draw_playing_window():
    pass


# Draw the victory screen
# Shows enemy grid & score with victory menu
def draw_victory_window():
    pass


# Draw the defeat screen
# Shows player grid & score with defeat menu
def draw_defeat_window():
    pass


# Generate positions for enemy ships & place them on enemy grid
def get_enemy_positions():
    pass


# Convert dropped ship to X & Y units for the player grid list array
# i.e. if a 3-unit player ship is dropped in the top-left corner horizontally,
# this function should translate the sprite into array positions (1,1), (2,1), & (3,1)
def convert_ship_units():
    pass


# Update scores for player & enemy based on units hit, missed, & destroyed
def update_scores():
    pass


# Let user click on a ship from the ship inventory & drag it to the player grid
# If drop position is valid, record positions that the image is dropped on
def drag_and_drop_ship():
    pass


# Add player ship to grid & list array & remove placed ship image
def add_player_ship():
    pass


# Check if enemy hit a player unit & change the player tile
def check_player_hit():
    pass


# Check if player hit an enemy unit & uncover that enemy tile
def check_enemy_hit():
    pass


# Change grid unit color based on hit (orange), missed (blue), or destroyed (red)
def change_unit_color():
    pass


# Display separate small screen that holds player ships; player will drag & drop ships from this screen
def display_ship_inventory():
    pass


# Generate random guess for enemy on player grid
# Check if unit hit but not destroyed; if so, change enemy guess to check around hit piece
def enemy_turn():
    pass


# Main function
def main():
    grid_width = (unit_size * unit_size) + (unit_margin * horizontal units) 
    grid_height = (unit_size * unit_size) + (unit_margin * vertical_units)
    
    running = True
    clock = pygame.time.Clock()

    
# Main menu before game starts that prompts player to either begin or quit; calls the Main function
def main_menu():
    pass
  
pygame.quit()
