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


def load_level(level, snake_loading_time_delay):
    last_time = t.time()
    enemies.clear()
    snakes.clear()
    entities.clear()
    run = True
    ticks = 0
    time = 1
    sparks_x = 0
    sparks_y = 0
    danger = False
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
    snake_loading_delay = snake_loading_time_delay
    cube_time = 100
    snake_home = pygame.image.load("Sprites/cube.png")
    snake_home.set_colorkey((255,255,255))
    # sparks.append(framework.Spark([700, 250], math.radians(random.randint(0, 360)), random.randint(1, 3), (0, 255, 0), 1))
    m = framework.MapFetcher(level)
    m.fetch_map()
    game_map = []
    enemy_spawn_loc = []
    key_spawn_loc = []
    snake_spawn_loc = []
    up_arrow = pygame.image.load("Sprites/Up_Arrow.png")
    up_arrow.set_colorkey((255,255,255))
    tutorial_text = [ "Press J to transform into a cube", "Turn into a cube and dodge the ", "Collect the keys on the way by ", "WELL DONE! YOU HAVE LEARNT THE MECHANICS!",  "which does not obey gravity", "cube pieces as well as condas", "transforming into cube and then man", "Arrow keys or WASD for movement", "And Space for jump"]
    ticks_after_death = 0
    time_after_death = 0
    death_time_delay = 100
    summon = 0
    danger_sign = pygame.image.load("Sprites/Danger_sign.png").convert_alpha()
    danger_sign.set_colorkey((255,255,255))
    level_over = False
    screen_shake = 0
    game_map, enemy_spawn_loc, key_spawn_loc, snake_spawn_loc, door_loc, end, text_loc = m.draw_map(display, grass, dirt1, dirt2, up_arrow, scroll)
    font = pygame.font.Font("Fonts/jayce.ttf", 16)
    door_img = pygame.image.load("Sprites/door.png")
    door_img.set_colorkey((116, 68, 56))
    door_img = pygame.transform.scale(door_img, (door_img.get_height() * 3, door_img.get_width() * 3))
    door = framework.Entity(door_img.get_height(), door_img.get_width(), door_loc[0][0] - 16 * 2, door_loc[0][1] - 24,
                            door_img)
    p = framework.Player(50, 70, 32, 32, (255, 0, 0), 4, "player", cube_img, player_idle_spritesheet,
                         player_run_spritesheet, player_jump_spritesheet)
    while run:
        display.fill((100, 100, 100))
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

        display.blit(snake_home, (snake_spawn_loc[0][0] - scroll[0], snake_spawn_loc[0][1] - scroll[1] - 15))

        if level == "Map/level_0.txt":
            if p.special_get_rect().x >= 1100:
                summon += 1
                if summon == 1:
                    screen_shake = 30
                    for snake_loc in snake_spawn_loc:
                        load_snake(snake_loc[0], snake_loc[1])
        else:
            if ticks - snake_loading_last_update > snake_loading_delay:
                if snake_spawn_loc != []:
                    for snake_loc in snake_spawn_loc:
                        load_snake(snake_loc[0], snake_loc[1])
                screen_shake = 30
                snake_loading_last_update = ticks

        if screen_shake > 0:
            screen_shake -= 1

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
        game_map, enemy_spawn_loc, key_spawn_loc1, snake_spawn_loc, door_loc, end, text_loc = m.draw_map(display, grass, dirt1, dirt2, up_arrow,
                                                                                          scroll)
        if text_loc != []:
            for te, text in enumerate(text_loc):
                draw_text(tutorial_text[te], font, (255,255,255), text[0] - scroll[0], text[1] - scroll[1], display)

        if screen_shake:
            danger = True
            scroll[0] += random.randint(1, 4) - 2
            scroll[1] += random.randint(1,4) - 2
        else:
            danger = False


        if danger:
            display.blit(danger_sign, (170, 24))
            draw_text(" Conda Incoming", font, (255, 0, 0), 185, 20, display)
            display.blit(danger_sign, (295, 24))

        p.move(5, game_map, current_time, dt)
        p.draw(display, scroll)
        draw_timer(display, cube_time, 20, 20)
        door.draw(display, scroll)

        if level_over:
            p.alive = False


        if p.alive:
            ticks_after_death = 0
            if p.special_get_rect().y > end[0][1]:
                print("I am dead")
                p.alive = False
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


def draw_text(text, font, text_col, x, y, display):
    img = font.render(text, True, text_col)
    display.blit(img, (x, y))


def main():
    run = True
    #https://www.beepbox.co/#9n31s6k0l00e03t2ma7g0fj07r1i0o432T1v1u66f0q0x10p51d08A5F4B5Q1753Pca88E4b762863877T5v1u43f0qwx10n511d03HT_QT_ItRAJJAAzh0E1b7T1v1ub4f20o72laq011d23A5F4B3Q0001Pfca8E362963479T4v1uf0f0q011z6666ji8k8k3jSBKSJJAArriiiiii07JCABrzrrrrrrr00YrkqHrsrrrrjr005zrAqzrjzrrqr1jRjrqGGrrzsrsA099ijrABJJJIAzrrtirqrqjqixzsrAjrqjiqaqqysttAJqjikikrizrHtBJJAzArzrIsRCITKSS099ijrAJS____Qg99habbCAYrDzh00E0b4h400000000PcM000000014h000000004h400000000p21nISnQG8Sr5Ml4RfcCkFILJdvF02CzVgc3j8i1vpohTmRAt8aqf36n05Y6hQBY4hMdw2hFEN2OQzGGwaOeSYLLw00
    #https://www.beepbox.co/#9n31s6k0l00e07t2ma7g0fj07r1i0o332T1v1u17f0q00d03A1F0B0Q200ePb793E3617628637T1v1ub2f10k8q011d23A0F1B8Q0000Pe600E179T5v1ua6f10i8q8141d23HYr901i8ah00000h0E0T2v1u15f10w4qw02d03w0E0b4h4y8w00000h4g000000014h000000004h400000000p1DFK3MjdMuw0PrLo1jjh-aGqAR_B6lnjnCk000000
    bmusic = pygame.mixer.Sound("Music/trial_song.wav")
    snake = pygame.image.load("Sprites/snake.png").convert_alpha()
    snake = pygame.transform.scale(snake, (snake.get_width()* 5, snake.get_height() * 5))
    snake.set_colorkey((255, 255, 255))
    snake_lft = pygame.image.load("Sprites/snake.png").convert_alpha()
    snake_lft = pygame.transform.scale(snake_lft, (snake_lft.get_width() * 5, snake_lft.get_height() * 5))
    snake_lft = pygame.transform.flip(snake_lft, True, False)
    snake_lft.set_colorkey((255,255,255))
    cube = pygame.image.load("Sprites/cube.png")
    cube = pygame.transform.scale(cube, (cube.get_width() * 2, cube.get_height() * 2))
    cube.set_colorkey((255,255,255))
    font = pygame.font.Font("Fonts/jayce.ttf", 30)
    font2 = pygame.font.Font("Fonts/jayce.ttf", 60)
    inside_color = [(255, 0, 102)]
    outside_color = [(10, 10, 10)]
    player_idle_spritesheet = pygame.image.load("Sprites/player_idle.png").convert_alpha()
    player = []
    for x in range(3):
        player.append(get_image(player_idle_spritesheet, x, 32, 32, 2))
    frame = 0
    last_update = 0
    animation_delay = 300
    circle_last_update = 0
    circle_animation_delay = 50
    completed = -1
    text_x = 220
    text_y = 252
    click = False
    text = "PLAY"
    circles = []
    level = 0
    levels = ["Map/level_0.txt", "Map/level_1.txt", "Map/level_2.txt", "Map/level_3.txt"]
    #levels = ["Map/level_2.txt"]
    snake_loading_time_delays = [5000, 10000, 9000, 8000]
    completed_levels = [-1, -1, -1, -1]
    #snake_loading_time_delays = [10000]
    #location, radius
    while run:
        display.fill((0, 0, 0))
        time = pygame.time.get_ticks()
        if time - last_update > animation_delay:
            frame+=1
            if frame >= 3:
                frame = 0
            last_update = time
        if time - circle_last_update > circle_animation_delay:
            circles.append(list((list((random.randint(0, 1000) / 2, random.randint(0, 1) )), random.randint(1,2), get_color())))
            circle_last_update = time
        mx, my = pygame.mouse.get_pos()
        mx = mx / 2
        my = my / 2
        # Circles
        for circle in sorted(circles, reverse= True):
            pygame.draw.circle(display, circle[2], (circle[0][0], circle[0][1]), circle[1])
            pygame.draw.circle(display, (0,0,0), (circle[0][0], circle[0][1]), circle[1] - 2)
            circle[0][1] += 0.5
            #circle[1] -= 0.1
            if circle[1] <= 0:
                circles.remove(circle)
            if circle[0][1] > 300:
                circles.remove(circle)
        play_btn_outline = pygame.Rect(150, 250, 200, 50)
        pygame.draw.rect(display, outside_color[0], play_btn_outline, 20, 50)
        play_btn_inside = pygame.Rect(157, 255, 185, 35)
        pygame.draw.rect(display, inside_color[0], play_btn_inside, 0, 50)
        draw_text(text, font, (255, 255, 255), text_x, text_y, display)
        draw_text("CUBE  CONDA", font2, (255,255,255), 100, 10, display)
        draw_text("JayJan", font, (255,255,255),195,60, display)
        display.blit(snake, (370,240))
        display.blit(snake_lft, (0, 240))
        display.blit(player[frame], (150, 187))
        display.blit(cube, (210, 194))
        if play_btn_inside.collidepoint(mx, my):
            inside_color.clear()
            inside_color.append((10, 10, 10))
            outside_color.clear()
            outside_color.append((255, 0, 255))
            if click:
                circles.clear()
                entities = []
                completed_levels[level] = load_level(levels[level], snake_loading_time_delays[level])
                if completed_levels[level] == 0:
                    text = "Next Level!"
                    text_x = 180
                    level += 1
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
