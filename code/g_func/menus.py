from foundation import init_screen
from g_func import g_var, draw_grids
from during_game import scores
import pygame


# Main menu before game starts that prompts player to either begin or quit; calls the Main function
def main_menu():
    init_screen.screen.fill(g_var.blue)

    text = g_var.title_font.render("BATTLESHIP", 1, g_var.white)
    init_screen.screen.blit(text, (393, 200))

    start_button = pygame.Rect(350, 270, 300, 60)
    quit_button = pygame.Rect(350, 350, 300, 60)

    pygame.draw.rect(init_screen.screen, g_var.white, start_button)
    pygame.draw.rect(init_screen.screen, g_var.white, quit_button)

    text = g_var.game_font.render("start game", 1, g_var.blue)
    init_screen.screen.blit(text, (440, 290))
    text = g_var.game_font.render("quit", 1, g_var.blue)
    init_screen.screen.blit(text, (485, 370))

    pygame.display.flip()

    selecting = True

    import main
    while selecting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if start_button.collidepoint(event.pos):
                        main.main()
                    elif quit_button.collidepoint(event.pos):
                        pygame.quit()


# Victory sub-menu
def victory_menu(enemy_grid):
    init_screen.screen.fill(g_var.blue)

    draw_grids.draw_enemy_grid(enemy_grid)
    scores.draw_enemy_score(enemy_grid)

    text = g_var.title_font.render("YOU WON!", 1, g_var.white)
    init_screen.screen.blit(text, (210, 110))

    play_again_button = pygame.Rect(150, 170, 300, 60)
    quit_button = pygame.Rect(150, 250, 300, 60)

    pygame.draw.rect(init_screen.screen, g_var.white, play_again_button)
    pygame.draw.rect(init_screen.screen, g_var.white, quit_button)

    text = g_var.game_font.render("play again", 1, g_var.blue)
    init_screen.screen.blit(text, (250, 190))
    text = g_var.game_font.render("quit", 1, g_var.blue)
    init_screen.screen.blit(text, (280, 270))

    pygame.display.flip()

    pygame.event.pump()
    selecting = True

    while selecting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if play_again_button.collidepoint(event.pos):
                        return "play again"
                    elif quit_button.collidepoint(event.pos):
                        return "quit"


# Defeat sub-menu
def defeat_menu(player_grid):
    init_screen.screen.fill(g_var.blue)

    draw_grids.draw_player_grid(player_grid)
    scores.draw_player_score(player_grid)

    text = g_var.title_font.render("YOU LOST!", 1, g_var.white)
    init_screen.screen.blit(text, (660, 110))

    play_again_button = pygame.Rect(600, 170, 300, 60)
    quit_button = pygame.Rect(600, 250, 300, 60)

    pygame.draw.rect(init_screen.screen, g_var.white, play_again_button)
    pygame.draw.rect(init_screen.screen, g_var.white, quit_button)

    text = g_var.game_font.render("play again", 1, g_var.blue)
    init_screen.screen.blit(text, (700, 190))
    text = g_var.game_font.render("quit", 1, g_var.blue)
    init_screen.screen.blit(text, (730, 270))

    pygame.display.flip()

    pygame.event.pump()
    selecting = True

    while selecting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if play_again_button.collidepoint(event.pos):
                        return "play again"
                    elif quit_button.collidepoint(event.pos):
                        return "quit"
