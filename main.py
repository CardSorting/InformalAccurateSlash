import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PyQuest")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Player
player_pos = [WIDTH // 2, HEIGHT // 2]
player_size = 40
player_speed = 5
player_hp = 100
player_attack = 10

# Map
tile_size = 50
map_width = WIDTH // tile_size
map_height = HEIGHT // tile_size
game_map = [[0 for _ in range(map_width)] for _ in range(map_height)]

# Generate random obstacles
for _ in range(20):
    x, y = random.randint(0, map_width - 1), random.randint(0, map_height - 1)
    game_map[y][x] = 1

# Enemy
enemy_pos = [random.randint(0, WIDTH - player_size), random.randint(0, HEIGHT - player_size)]
enemy_size = 40
enemy_hp = 50
enemy_attack = 5

# Game state
in_battle = False

# Font
font = pygame.font.Font(None, 36)

def draw_map():
    for y in range(map_height):
        for x in range(map_width):
            if game_map[y][x] == 1:
                pygame.draw.rect(screen, GREEN, (x * tile_size, y * tile_size, tile_size, tile_size))

def draw_player():
    pygame.draw.rect(screen, BLUE, (*player_pos, player_size, player_size))

def draw_enemy():
    if not in_battle:
        pygame.draw.rect(screen, RED, (*enemy_pos, enemy_size, enemy_size))

def check_collision(pos):
    tile_x = pos[0] // tile_size
    tile_y = pos[1] // tile_size
    return 0 <= tile_x < map_width and 0 <= tile_y < map_height and game_map[tile_y][tile_x] == 0

def move_player(dx, dy):
    new_pos = [player_pos[0] + dx, player_pos[1] + dy]
    if check_collision(new_pos) and check_collision([new_pos[0] + player_size, new_pos[1] + player_size]):
        player_pos[0] = new_pos[0]
        player_pos[1] = new_pos[1]

def check_enemy_collision():
    return (abs(player_pos[0] - enemy_pos[0]) < player_size and
            abs(player_pos[1] - enemy_pos[1]) < player_size)

def battle_screen():
    global player_hp, enemy_hp, in_battle

    screen.fill(BLACK)

    # Draw player and enemy HP
    player_hp_text = font.render(f"Player HP: {player_hp}", True, WHITE)
    enemy_hp_text = font.render(f"Enemy HP: {enemy_hp}", True, WHITE)
    screen.blit(player_hp_text, (10, 10))
    screen.blit(enemy_hp_text, (10, 50))

    # Draw battle options
    attack_text = font.render("1. Attack", True, WHITE)
    screen.blit(attack_text, (10, HEIGHT - 100))

    pygame.display.flip()

    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:  # Attack
                    enemy_hp -= player_attack
                    if enemy_hp <= 0:
                        in_battle = False
                        return True
                    player_hp -= enemy_attack
                    if player_hp <= 0:
                        return False
                    waiting_for_input = False

    return True

def main():
    global in_battle
    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if not in_battle:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                move_player(-player_speed, 0)
            if keys[pygame.K_RIGHT]:
                move_player(player_speed, 0)
            if keys[pygame.K_UP]:
                move_player(0, -player_speed)
            if keys[pygame.K_DOWN]:
                move_player(0, player_speed)

            if check_enemy_collision():
                in_battle = True

            screen.fill(BLACK)
            draw_map()
            draw_player()
            draw_enemy()
        else:
            if not battle_screen():
                running = False

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()