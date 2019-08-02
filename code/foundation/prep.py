import pygame
from foundation import init_screen
from g_func import g_var


# Display separate small screen that holds player ships; player will drag & drop ships from this screen
def draw_ship_inventory(placed_ships, orientation):
    inventory_rectangle = pygame.Surface((832, 200))
    inventory_rectangle.fill(g_var.white)
    init_screen.screen.blit(inventory_rectangle, (80, 450))

    text = g_var.game_font.render("Ships (drag n' drop)", 1, g_var.white)
    init_screen.screen.blit(text, (100, 415))
    text = g_var.game_font.render("[R]otate", 1, g_var.white)
    init_screen.screen.blit(text, (810, 415))

    ship_inventory = []

    if orientation == "horizontal":
        for m in range(5):
            if m == 0:
                ship_inventory.append(pygame.rect.Rect(135, 530, (g_var.unit_size * 2) + g_var.unit_margin, g_var.unit_size))
            if m == 1:
                ship_inventory.append(pygame.rect.Rect(245, 530, (g_var.unit_size * 3) + (g_var.unit_margin * 2), g_var.unit_size))
            if m == 2:
                ship_inventory.append(pygame.rect.Rect(380, 530, (g_var.unit_size * 3) + (g_var.unit_margin * 2), g_var.unit_size))
            if m == 3:
                ship_inventory.append(pygame.rect.Rect(515, 530, (g_var.unit_size * 4) + (g_var.unit_margin * 3), g_var.unit_size))
            if m == 4:
                ship_inventory.append(pygame.rect.Rect(685, 530, (g_var.unit_size * 5) + (g_var.unit_margin * 4), g_var.unit_size))
            if m not in placed_ships:
                pygame.draw.rect(init_screen.screen, g_var.black, ship_inventory[m])

    if orientation == "vertical":
        for m in range(5):
            if m == 0:
                ship_inventory.append(pygame.rect.Rect(155, 520, g_var.unit_size, (g_var.unit_size * 2) + g_var.unit_margin))
            if m == 1:
                ship_inventory.append(pygame.rect.Rect(270, 510, g_var.unit_size, (g_var.unit_size * 3) + (g_var.unit_margin * 2)))
            if m == 2:
                ship_inventory.append(pygame.rect.Rect(405, 510, g_var.unit_size, (g_var.unit_size * 3) + (g_var.unit_margin * 2)))
            if m == 3:
                ship_inventory.append(pygame.rect.Rect(545, 490, g_var.unit_size, (g_var.unit_size * 4) + (g_var.unit_margin * 3)))
            if m == 4:
                ship_inventory.append(pygame.rect.Rect(730, 475, g_var.unit_size, (g_var.unit_size * 5) + (g_var.unit_margin * 4)))
            if m not in placed_ships:
                pygame.draw.rect(init_screen.screen, g_var.black, ship_inventory[m])

    return ship_inventory


def pre_game():
    prepping = True
    placed_ships = []
    selected_ship = None
    orientation = "horizontal"
    mouse_up = False

    from foundation import create_arrays
    player_grid = create_arrays.create_player_array()
    enemy_grid = create_arrays.create_enemy_array()

    ship_inventory, player_grid, enemy_grid = draw_starting_window(placed_ships, player_grid, enemy_grid, orientation)

    from during_game import valid
    while prepping:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for m in range(5):
                        if ship_inventory[m].collidepoint(event.pos):
                            selected_ship = ship_inventory[m]
                            mouse_x, mouse_y = event.pos
                            offset_x = selected_ship.x - mouse_x
                            offset_y = selected_ship.y - mouse_y
                            placed_ships.append(m)
                            ship_number = m
                mouse_up = False

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if selected_ship is not None:
                        checking_ship = selected_ship
                        valid_space, player_grid = valid.valid_player_space(checking_ship, ship_number, placed_ships, player_grid, enemy_grid, orientation)
                        if not valid_space:
                            placed_ships.remove(ship_number)
                            ship_inventory, player_grid, enemy_grid = draw_starting_window(placed_ships, player_grid, enemy_grid, orientation)
                        else:
                            pygame.display.flip()
                            if len(placed_ships) == 5:
                                prepping = False
                        selected_ship = None
                mouse_up = True

            elif event.type == pygame.MOUSEMOTION:
                if selected_ship is not None:
                    mouse_x, mouse_y = event.pos
                    selected_ship.x = mouse_x + offset_x
                    selected_ship.y = mouse_y + offset_y
                    draw_starting_window(placed_ships, player_grid, enemy_grid, orientation)
                    pygame.draw.rect(init_screen.screen, g_var.black, selected_ship)
                    pygame.display.update()

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                if mouse_up:
                    if orientation == "horizontal":
                        orientation = "vertical"
                        ship_inventory, player_grid, enemy_grid = draw_starting_window(placed_ships, player_grid, enemy_grid, orientation)
                    else:
                        orientation = "horizontal"
                        ship_inventory, player_grid, enemy_grid = draw_starting_window(placed_ships, player_grid, enemy_grid, orientation)

    enemy_grid = get_enemy_positions(enemy_grid)
    draw_starting_window(placed_ships, player_grid, enemy_grid, orientation)

    return player_grid, enemy_grid


# Generate positions for enemy ships & place them on enemy grid
def get_enemy_positions(enemy_grid):
    import random
    random.seed()

    for m in range(5):
        enemy_rotation = random.choice(("horizontal", "vertical"))

        space_taken = True

        if m == 0:
            enemy_units = 2
        elif m == 1:
            enemy_units = 3
        else:
            enemy_units = m + 1

        while space_taken:
            enemy_x = random.randrange(g_var.horizontal_units)
            enemy_y = random.randrange(g_var.vertical_units)
            space_taken = False
            for n in range(enemy_units):
                if enemy_rotation == "horizontal":
                    if (enemy_x + n) >= g_var.horizontal_units:
                        space_taken = True
                    else:
                        if enemy_grid[enemy_x + n][enemy_y].number != "empty":
                            space_taken = True
                else:
                    if (enemy_y + n) >= g_var.vertical_units:
                        space_taken = True
                    else:
                        if enemy_grid[enemy_x][enemy_y + n].number != "empty":
                            space_taken = True

        for n in range(enemy_units):
            if enemy_rotation == "horizontal":
                enemy_grid[enemy_x + n][enemy_y].number = str(m)
                enemy_grid[enemy_x + n][enemy_y].status = "full"
            else:
                enemy_grid[enemy_x][enemy_y + n].number = str(m)
                enemy_grid[enemy_x][enemy_y + n].status = "full"

    return enemy_grid


# Draw the game preparation screen
# Shows both grids (player & enemy) & ship inventory
def draw_starting_window(placed_ships, player_grid, enemy_grid, orientation):
    from foundation import init_screen
    from g_func import g_var
    init_screen.screen.fill(g_var.blue)

    from g_func import draw_grids
    draw_grids.draw_player_grid(player_grid)
    draw_grids.draw_enemy_grid(enemy_grid)
    ship_inventory = draw_ship_inventory(placed_ships, orientation)

    pygame.display.flip()

    return ship_inventory, player_grid, enemy_grid
