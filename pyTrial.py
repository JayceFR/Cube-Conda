import pygame
# TODO Create Timer for cube
# TODO Create door to exit level
# TODO Reformat the map for level
# TODO Create level generator
import fps
import framework
import sys
import random
import math
from fps import *
import time as t

pygame.init()
screen_width = 1000
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
display = pygame.Surface((screen_width / 2, screen_height / 2))

pygame.display.set_caption("Cube Conda")

clientNumber = 0
entities = []
enemies = []
snakes = []
clock = pygame.time.Clock()



def get_color():
    colors = [[(255, 0, 0)], [(255, 255, 0)], [(0, 0, 255)], [(255, 255, 255)], [(0, 255, 0)], [(255, 102, 0)]]
    return colors[random.randint(0, 5)][0]


def load_enemy(x, y):
    enemies.append(framework.Enemy(x, y))


def load_snake(x, y):
    snakes.append(framework.Enemy(x, y - 4, 0, "Sprites/snake.png"))


def createEntity(key_spawn_loc, key_img):
    for key_locs in key_spawn_loc:
        entities.append(framework.Entity(key_img.get_height(), key_img.get_width(), key_locs[0], key_locs[1], key_img))


def draw_timer(screen, time, x, y):
    ratio = time / 100
    pygame.draw.rect(screen, (255, 255, 255), (x - 2, y - 2, 104, 24))
    pygame.draw.rect(screen, (255, 0, 0), (x, y, 100, 20))
    pygame.draw.rect(screen, (255, 255, 0), (x, y, 100 * ratio, 20))


def get_image(sheet, frame, width, height, scale):
    image = pygame.Surface((width, height)).convert_alpha()
    image.blit(sheet, (0, 0), ((frame * width), 0, width, height))
    image = pygame.transform.scale(image, (width * scale, height * scale))
    image.set_colorkey((255, 255, 255))
    return image


def load_level(level):
    last_time = t.time()
    enemies.clear()
    snakes.clear()
    entities.clear()
    run = True
    ticks = 0
    time = 1
    sparks_x = 0
    sparks_y = 0
    enemy_loading_time_delay = 500
    enemy_load_last_update = 0
    grass = pygame.image.load("Tiles/grass.png").convert_alpha()
    dirt1 = pygame.image.load("Tiles/dirt1.png").convert_alpha()
    dirt1 = pygame.transform.rotate(dirt1, 90)
    dirt2 = pygame.image.load("Tiles/dirt2.png").convert_alpha()
    frames_per_sec = fpsClass(60)
    cube_img2 = pygame.image.load("Sprites/cube.png").convert_alpha()
    cube_img = pygame.transform.scale(cube_img2, (cube_img2.get_width() / 2, cube_img2.get_height() / 2))
    cube_img.set_colorkey((255, 255, 255))
    player_idle_spritesheet = pygame.image.load("Sprites/player_idle.png").convert_alpha()
    player_run_spritesheet = pygame.image.load("Sprites/player_run.png").convert_alpha()
    player_jump_spritesheet = pygame.image.load("Sprites/player_jump.png").convert_alpha()
    key_img = pygame.image.load("Sprites/key.png").convert_alpha()
    true_scroll = [0, 0]
    scroll = [0, 0]
    sparks = []
    create = 0
    circle_radius = 5
    cube_time_limit = 100
    snake_loading_last_update = 0
    snake_loading_delay = 5000
    cube_time = 100
    # sparks.append(framework.Spark([700, 250], math.radians(random.randint(0, 360)), random.randint(1, 3), (0, 255, 0), 1))
    m = framework.MapFetcher(level)
    m.fetch_map()
    game_map = []
    enemy_spawn_loc = []
    key_spawn_loc = []
    snake_spawn_loc = []
    ticks_after_death = 0
    time_after_death = 0
    death_time_delay = 100
    level_over = False
    game_map, enemy_spawn_loc, key_spawn_loc, snake_spawn_loc, door_loc = m.draw_map(display, grass, dirt1, dirt2,
                                                                                     scroll)
    door_img = pygame.image.load("Sprites/door.png")
    door_img.set_colorkey((116, 68, 56))
    door_img = pygame.transform.scale(door_img, (door_img.get_height() * 3, door_img.get_width() * 3))
    door = framework.Entity(door_img.get_height(), door_img.get_width(), door_loc[0][0] - 16 * 2, door_loc[0][1] - 24,
                            door_img)
    p = framework.Player(50, 70, 32, 32, (255, 0, 0), 4, "player", cube_img, player_idle_spritesheet,
                         player_run_spritesheet, player_jump_spritesheet)
    while run:
        display.fill((100, 100, 255))
        clock.tick(frames_per_sec.get_fps())
        ticks = pygame.time.get_ticks()
        ticks_after_death += 1
        dt = t.time() - last_time
        dt *= 60
        last_time = t.time()
        if key_spawn_loc != []:
            if create == 0:
                create = 1
                createEntity(key_spawn_loc, key_img)
            if entities != []:
                for e, entity in sorted(enumerate(entities), reverse=True):
                    entity.draw(display, scroll)
                    if entity.get_rect().colliderect(p.get_rect()):
                        entities.remove(entity)
                        if list((entity.x, entity.y)) in key_spawn_loc:
                            key_spawn_loc.remove(list((entity.x, entity.y)))
                        for x in range(20):
                            sparks.append(framework.Spark([entity.get_rect().x - scroll[0], p.get_rect().y - scroll[1]],
                                                          math.radians(random.randint(0, 360)), random.randint(3, 5),
                                                          (212, 175, 55), 1, 2))
                        createEntity(key_spawn_loc, key_img)
        if ticks - enemy_load_last_update > enemy_loading_time_delay:
            if enemy_spawn_loc != []:
                for enemy_loc in enemy_spawn_loc:
                    load_enemy(enemy_loc[0], enemy_loc[1])
            enemy_load_last_update = ticks

        if ticks - snake_loading_last_update > snake_loading_delay:
            if snake_spawn_loc != []:
                for snake_loc in snake_spawn_loc:
                    load_snake(snake_loc[0], snake_loc[1])
            snake_loading_last_update = ticks

        if p.get_state() == "player":
            true_scroll[0] += (p.get_rect().x - true_scroll[0] - 262) / 20
            true_scroll[1] += (p.get_rect().y - true_scroll[1] - 162) / 20
            scroll = true_scroll.copy()
            scroll[0] = int(scroll[0])
            scroll[1] = int(scroll[1])
        if p.get_state() == "cube":
            true_scroll[0] += (p.get_cube_rect().x - true_scroll[0] - 262) / 20
            true_scroll[1] += (p.get_cube_rect().y - true_scroll[1] - 162) / 20
            scroll = true_scroll.copy()
            scroll[0] = int(scroll[0])
            scroll[1] = int(scroll[1])
        current_time = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_j:
                    p.change_state(game_map, current_time)
        game_map, enemy_spawn_loc, key_spawn_loc1, snake_spawn_loc, door_loc = m.draw_map(display, grass, dirt1, dirt2,
                                                                                          scroll)
        p.move(5, game_map, current_time, dt)
        p.draw(display, scroll)
        draw_timer(display, cube_time, 20, 20)
        door.draw(display, scroll)

        if level_over:
            p.alive = False

        if p.alive:
            ticks_after_death = 0
            if p.state == "cube":
                if cube_time > 0:
                    # pass
                    cube_time -= 0.5
            if p.state == "player":
                if cube_time < cube_time_limit:
                    cube_time += 0.5
            if cube_time <= 0:
                p.change_state(game_map, current_time)
            if p.get_rect().colliderect(door.get_rect()):
                if key_spawn_loc == []:
                    level_over = True
            if enemies != []:
                for e, enemy in sorted(enumerate(enemies), reverse=True):
                    enemy.draw(display, scroll, screen_height / 2, dt)
                    if enemy.get_rect().colliderect(p.special_get_rect()):
                        p.alive = False
                        sparks_x = enemy.get_rect().x - scroll[0]
                        sparks_y = p.special_get_rect().y - scroll[1]

                    if not enemy.alive:
                        enemies.pop(e)
            if snakes != []:
                for s, snake in sorted(enumerate(snakes), reverse=True):
                    snake.draw(display, scroll, screen_height / 2, dt)
                    if snake.get_rect().colliderect(p.special_get_rect()):
                        p.alive = False
                        sparks_x = snake.get_rect().x - scroll[0]
                        sparks_y = p.special_get_rect().y - scroll[1]
                    if not snake.alive:
                        snakes.pop(s)
        else:
            if not level_over:
                if ticks_after_death - time_after_death > death_time_delay:
                    del p
                    del door
                    return 1
                if time == 1:
                    for x in range(50):
                        time += 1
                        sparks.append(framework.Spark([sparks_x, sparks_y],
                                                      math.radians(random.randint(0, 360)), random.randint(8, 10),
                                                      get_color(), 1, 1))
            else:
                pygame.draw.circle(display, (0, 0, 0), (door_loc[0][0], door_loc[0][1]), circle_radius)
                if circle_radius <= 2200:
                    circle_radius += 20
                if circle_radius >= 2200:
                    del p
                    del door
                    return 0

        for i, spark in sorted(enumerate(sparks), reverse=True):
            spark.move(1)
            spark.draw(display)
            if not spark.alive:
                sparks.pop(i)

        # sparks.append(framework.Spark([700, 250], math.radians(random.randint(0, 360)), random.randint(1, 3), (0, 255, 0), 1))
        surf = pygame.transform.scale(display, (screen_width, screen_height))
        screen.blit(surf, (0, 0))
        pygame.display.update()


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    display.blit(img, (x, y))


def main():
    run = True
    font = pygame.font.Font("Fonts/jayce.ttf", 30)
    font2 = pygame.font.Font("Fonts/jayce.ttf", 60)
    inside_color = [(255, 0, 255)]
    outside_color = [(10, 10, 10)]
    player_idle_spritesheet = pygame.image.load("Sprites/player_idle.png").convert_alpha()
    player = []
    for x in range(3):
        player.append(get_image(player_idle_spritesheet, x, 32, 32, 2))
    frame = 0
    last_update = 0
    animation_delay = 300
    completed = -1
    text_x = 220
    click = False
    text = "PLAY"
    while run:
        display.fill((50, 10, 10))
        time = pygame.time.get_ticks()
        if time - last_update > animation_delay:
            frame+=1
            if frame >= 3:
                frame = 0
            last_update = time
        mx, my = pygame.mouse.get_pos()
        mx = mx / 2
        my = my / 2
        play_btn_outline = pygame.Rect(150, 250, 200, 50)
        pygame.draw.rect(display, outside_color[0], play_btn_outline, 20, 50)
        play_btn_inside = pygame.Rect(157, 255, 185, 35)
        pygame.draw.rect(display, inside_color[0], play_btn_inside, 0, 50)
        draw_text(text, font, (255, 255, 255), text_x, 252)
        draw_text("CUBE  CONDA", font2, (255,255,255), 100, 10)
        draw_text("JayJan", font, (255,255,255),195,60)
        display.blit(player[frame], (150, 187))
        if play_btn_inside.collidepoint(mx, my):
            inside_color.clear()
            inside_color.append((10, 10, 10))
            outside_color.clear()
            outside_color.append((255, 0, 255))
            if click:
                entities = []
                completed = load_level("Map/map.txt")
                if completed == 0:
                    print("Level 1 done")
                else:
                    text = "RETRY"
                    text_x = 210
        else:
            inside_color.clear()
            inside_color.append((255, 0, 255))
            outside_color.clear()
            outside_color.append((10, 10, 10))
        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True
        surf = pygame.transform.scale(display, (screen_width, screen_height))
        screen.blit(surf, (0, 0))
        pygame.display.update()


main()