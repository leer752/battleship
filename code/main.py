import pygame
from g_func import menus, g_var
from foundation import init_screen

pygame.init()
g_var.init()
init_screen.init()


# Main function
def main():

    prepping = True
    running = True
    clock = pygame.time.Clock()

    is_blind = True
    first_x = 0
    first_y = 0
    previous_x = 0
    previous_y = 0
    orientation = None
    direction = None
    guess_list = []

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if prepping:
            from foundation import prep
            player_grid, enemy_grid = prep.pre_game()
            prepping = False

        end_game = "ongoing"

        from during_game import player_turn
        from during_game import enemy_turn
        from during_game import during
        while end_game == "ongoing":
            player_grid, enemy_grid = player_turn.player_turn(player_grid, enemy_grid)
            end_game = during.check_end_game(player_grid, enemy_grid)
            if end_game == "ongoing":
                player_grid, enemy_grid, is_blind, first_x, first_y, previous_x, previous_y, orientation, direction, guess_list = enemy_turn.enemy_turn(player_grid, enemy_grid, is_blind, first_x, first_y, previous_x, previous_y, orientation, direction, guess_list)
                end_game = during.check_end_game(player_grid, enemy_grid)

        from g_func import menus
        if end_game == "victory":
            selection = menus.victory_menu(enemy_grid)
        elif end_game == "defeat":
            selection = menus.defeat_menu(player_grid)

        if selection == "quit":
            running = False
        elif selection == "play again":
            main()

    pygame.display.flip()
    clock.tick(g_var.fps)

    pygame.quit()


menus.main_menu()

pygame.quit()
