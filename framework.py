import pygame
import math
import random


class Player():
    def __init__(self, x, y, width, height, colour, speed, state, cube_img, player_idle_spritesheet,
                 player_run_spritesheet, player_jump_spritesheet):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.colour = colour
        self.speed = speed
        self.state = state
        self.alive = True
        self.jump = False
        self.jump_cooldown = 300
        self.last_update = 0
        self.air_timer = 0
        self.movement = [0, 0]
        self.moving_right = False
        self.moving_left = False
        self.running = False
        self.idle = False
        self.last_animation_update = 0
        self.facing_right = True
        self.facing_left = False
        self.display_x = 0
        self.display_y = 0
        self.cube_rect = pygame.Rect(x, y, cube_img.get_width(), cube_img.get_height())
        self.cube_movement = [0, 0]
        self.cube_moving_right = False
        self.cube_moving_left = False
        self.cube_moving_down = False
        self.cube_moving_up = False
        self.cube_img = cube_img
        self.idle_animation = []
        self.run_animation = []
        self.jump_animation = []
        self.frame = 0
        self.frame_cooldown = 150
        for x in range(0, 3):
            self.idle_animation.append(self.get_image(player_idle_spritesheet, x, 32, 32, 1))
        for x in range(0, 3):
            self.run_animation.append(self.get_image(player_run_spritesheet, x, 32, 32, 1))
        for x in range(0, 1):
            self.jump_animation.append(self.get_image(player_jump_spritesheet, x, 32, 32, 1))
        self.rect = pygame.Rect(self.x, self.y, self.idle_animation[0].get_width(), self.idle_animation[0].get_height())
        self.centerofx = self.rect.centerx

    def draw(self, display, scroll):
        # self.l.update(self.rect.x - 49, self.rect.y - 49)
        # self.l.draw(display)
        if self.alive:
            if self.state == "player":
                self.display_x = self.rect.x
                self.display_y = self.rect.y
                self.rect.x = self.rect.x - scroll[0]
                self.rect.y = self.rect.y - scroll[1]
                if self.facing_right:
                    if self.idle:
                        display.blit(self.idle_animation[self.frame], self.rect)
                    if self.jump:
                        display.blit(self.jump_animation[0], self.rect)
                    if self.running:
                        display.blit(self.run_animation[self.frame], self.rect)
                if self.facing_left:
                    if self.idle:
                        flip = self.idle_animation[self.frame].copy()
                        flip = pygame.transform.flip(flip, True, False)
                        display.blit(flip, self.rect)
                    if self.jump:
                        flip = self.jump_animation[0].copy()
                        flip = pygame.transform.flip(flip, True, False)
                        display.blit(flip, self.rect)
                    if self.running:
                        flip = self.run_animation[self.frame].copy()
                        flip = pygame.transform.flip(flip, True, False)
                        display.blit(flip, self.rect)
                self.rect.x = self.display_x
                self.rect.y = self.display_y
            if self.state == "cube":
                self.display_x = self.cube_rect.x
                self.display_y = self.cube_rect.y
                self.cube_rect.x = self.cube_rect.x - scroll[0]
                self.cube_rect.y = self.cube_rect.y - scroll[1]
                display.blit(self.cube_img, self.cube_rect)
                self.cube_rect.x = self.display_x
                self.cube_rect.y = self.display_y

    def move(self, gravity, tiles, current_time, dt = 1):
        if self.alive:
            if self.state == "player":
                self.movement = [0, 0]
                if self.moving_right:
                    self.movement[0] += 4 * dt
                    self.running = True
                    self.moving_right = False
                    if self.facing_left:
                        self.facing_right = True
                        self.facing_left = False
                if self.moving_left:
                    self.movement[0] -= 4 * dt
                    self.running = True
                    self.moving_left = False
                    if self.facing_right:
                        self.facing_left = True
                        self.facing_right = False

                if self.movement[0] == 0:
                    self.running = False
                    self.running = False

                self.idle = True
                if self.jump:
                    self.idle = False
                if self.running:
                    self.idle = False


                if current_time - self.last_animation_update > self.frame_cooldown:
                    self.frame += 1
                    if self.frame >= 3:
                        self.frame = 0
                    self.last_animation_update = current_time


                key = pygame.key.get_pressed()
                current_time = pygame.time.get_ticks()
                if key[pygame.K_LEFT] or key[pygame.K_a]:
                    self.moving_left = True
                if key[pygame.K_RIGHT] or key[pygame.K_d]:
                    self.moving_right = True
                if key[pygame.K_SPACE] or key[pygame.K_w]:
                    if current_time - self.last_update > self.jump_cooldown:
                        self.jump = True
                        self.last_update = current_time
                        if self.air_timer < 6:
                            gravity = -60

                self.movement[1] += gravity
                gravity += 0.2
                if gravity > 8:
                    gravity = 8

                collision_type = self.collision_checker(tiles)
                if collision_type["bottom"]:
                    self.jump = False

            if self.state == "cube":
                self.cube_movement = [0, 0]
                if self.cube_moving_right:
                    self.cube_movement[0] += self.speed * dt
                    self.cube_moving_right = False
                if self.cube_moving_left:
                    self.cube_movement[0] -= self.speed * dt
                    self.cube_moving_left = False
                if self.cube_moving_down:
                    self.cube_movement[1] += self.speed * dt
                    self.cube_moving_down = False
                if self.cube_moving_up:
                    self.cube_movement[1] -= self.speed * dt
                    self.cube_moving_up = False

                key = pygame.key.get_pressed()
                current_time = pygame.time.get_ticks()
                if key[pygame.K_LEFT] or key[pygame.K_a]:
                    self.cube_moving_left = True
                if key[pygame.K_RIGHT] or key[pygame.K_d]:
                    self.cube_moving_right = True
                if key[pygame.K_UP] or key[pygame.K_w]:
                    self.cube_moving_up = True
                if key[pygame.K_s] or key[pygame.K_DOWN]:
                    self.cube_moving_down = True

                collision_type = self.cube_collision_checker(tiles)

    def get_image(self, sheet, frame, width, height, scale):
        image = pygame.Surface((width, height)).convert_alpha()
        image.blit(sheet, (0, 0), ((frame * width), 0, width, height))
        image = pygame.transform.scale(image, (width * scale, height * scale))
        image.set_colorkey((255, 255, 255))
        return image

    def get_rect(self):
        return self.rect

    def special_get_rect(self):
        if self.state == "player":
            return self.rect
        if self.state == "cube":
            return self.cube_rect

    def get_cube_rect(self):
        return self.cube_rect

    def collision_test(self, tiles):
        hitlist = []
        for tile in tiles:
            if self.rect.colliderect(tile):
                hitlist.append(tile)
        return hitlist

    def cube_collision_test(self, tiles):
        hitlist = []
        for tile in tiles:
            if self.cube_rect.colliderect(tile):
                hitlist.append(tile)
        return hitlist

    def collision_checker(self, tiles):
        collision_types = {"top": False, "bottom": False, "right": False, "left": False}
        self.rect.x += self.movement[0]
        hit_list = self.collision_test(tiles)
        for tile in hit_list:
            if self.movement[0] > 0:
                self.rect.right = tile.left
                collision_types["right"] = True
            elif self.movement[0] < 0:
                self.rect.left = tile.right
                collision_types["left"] = True
        self.rect.y += self.movement[1]
        hit_list = self.collision_test(tiles)
        for tile in hit_list:
            if self.movement[1] > 0:
                self.rect.bottom = tile.top
                collision_types["bottom"] = True
            if self.movement[1] < 0:
                self.rect.top = tile.bottom
                collision_types["top"] = True
        return collision_types

    def cube_collision_checker(self, tiles):
        collision_types = {"top": False, "bottom": False, "right": False, "left": False}
        self.cube_rect.x += self.cube_movement[0]
        hit_list = self.cube_collision_test(tiles)
        for tile in hit_list:
            if self.cube_movement[0] > 0:
                self.cube_rect.right = tile.left
                collision_types["right"] = True
            elif self.cube_movement[0] < 0:
                self.cube_rect.left = tile.right
                collision_types["left"] = True
        self.cube_rect.y += self.cube_movement[1]
        hit_list = self.cube_collision_test(tiles)
        for tile in hit_list:
            if self.cube_movement[1] > 0:
                self.cube_rect.bottom = tile.top
                collision_types["bottom"] = True
            if self.cube_movement[1] < 0:
                self.cube_rect.top = tile.bottom
                collision_types["top"] = True
        return collision_types

    def change_state(self, game_map, current_time):
        if self.state == "player":
            self.state = "cube"
            self.cube_rect.x = self.rect.x + 10
            self.cube_rect.y = self.rect.y - 10
        else:
            self.state = "player"
            self.rect.x = self.cube_rect.x - 10
            self.rect.y = self.cube_rect.y + 10
            self.move(5, game_map, current_time)


    def get_state(self):
        return self.state


class Enemy():

    def __init__(self, x , y, type=1, image=""):
        self.colors = [[(255, 0, 0)], [(255, 255, 0)], [(0, 0, 255)], [(255, 255, 255)], [(0, 255, 0)], [(255, 102, 0)]]
        self.color = self.get_color()
        self.display_x = 0
        self.display_y = 0
        self.width = 16
        self.height = 16
        self.type = type
        self.image = image
        if self.image != "":
            self.snake_img = pygame.image.load(self.image)
            self.snake_img = pygame.transform.scale(self.snake_img, (self.snake_img.get_width() * 2, self.snake_img.get_height() * 2))
            self.snake_img.set_colorkey((255,255,255))
            self.width = self.snake_img.get_width()
            self.height = self.snake_img.get_height()
        self.alive = True
        self.speed = 3
        self.rect = pygame.Rect(x, y, self.width, self.height)

    def get_color(self):
        return self.colors[random.randint(0, 5)][0]

    def draw(self, display, scroll, screen_height, dt):
        self.display_x = self.rect.x
        self.display_y = self.rect.y
        self.rect.x -= scroll[0]
        self.rect.y -= scroll[1]
        if self.image == "":
            pygame.draw.rect(display, self.color, self.rect)
        else:
            #pygame.draw.rect(display, (0,0,0), self.rect)
            display.blit(self.snake_img, self.rect)
        self.rect.x = self.display_x
        self.rect.y = self.display_y
        if self.type == 1:
            self.rect.y += self.speed + dt
            if self.rect.y > screen_height + 200:
                self.alive = False
        if self.type == 0:
            self.rect.x -= self.speed + dt
            if self.rect.x < 0:
                self.alive = False


    def get_rect(self):
        return self.rect


class MapFetcher():
    def __init__(self, filename):
        self.filename = filename
        self.map = []

    def fetch_map(self):
        f = open(self.filename, "r")
        data = f.read()
        f.close()
        data = data.split('\n')
        for row in data:
            self.map.append((list(row)))

    def draw_map(self, screen, grass, dirt1, dirt2, scroll):
        y = 0
        tile_rects = []
        enemy_spawn_loc = []
        key_spawn_loc = []
        snake_spawn_loc = []
        door_loc = []

        for row in self.map:
            x = 0
            for tile in row:
                if tile == "1":
                    screen.blit(grass, (x * 16 - scroll[0], y * 16 - scroll[1]))
                if tile == "2":
                    screen.blit(dirt1, (x * 16 - scroll[0], y * 16 - scroll[1]))
                if tile == "3":
                    screen.blit(dirt2, (x * 16 - scroll[0], y * 16 - scroll[1]))
                if tile == "4":
                    enemy_spawn_loc.append(list((x*16, y * 16)))
                if tile == "5":
                    key_spawn_loc.append(list((x*16, y*16)))
                if tile == "6":
                    snake_spawn_loc.append(list((x*16, y*16)))
                if tile == "7":
                    door_loc.append(list((x*16, y*16)))
                if tile != "0" and tile != "5" and tile != "7":
                    tile_rects.append(pygame.Rect(x * 16, y * 16, 16, 16))
                x = x + 1
            y = y + 1

        return tile_rects, enemy_spawn_loc, key_spawn_loc, snake_spawn_loc, door_loc


class Entity():
    def __init__(self, height, width, x, y, img):
        self.height = height
        self.width = width
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, width, height)
        self.colors = [[(255, 0, 0)], [(255, 255, 0)], [(0, 0, 255)], [(255, 255, 255)], [(0, 255, 0)], [(255, 102, 0)]]
        self.color = self.get_color()
        self.display_x = 0
        self.display_y = 0
        self.image = img

    def draw(self, win, scroll):
        self.display_x = self.rect.x
        self.display_y = self.rect.y
        self.rect.x = self.rect.x - scroll[0]
        self.rect.y = self.rect.y - scroll[1]
        win.blit(self.image, self.rect)
        self.rect.x = self.display_x
        self.rect.y = self.display_y

    def get_color(self):
        return self.colors[random.randint(0, 5)][0]

    def get_rect(self):
        return self.rect


class Spark():
    def __init__(self, loc, angle, speed, color, scale=1, type=0):
        self.loc = loc
        self.angle = angle
        self.speed = speed
        self.scale = scale
        self.color = color
        self.alive = True
        self.type = type

    def point_towards(self, angle, rate):
        rotate_direction = ((angle - self.angle + math.pi * 3) % (math.pi * 2)) - math.pi
        try:
            rotate_sign = abs(rotate_direction) / rotate_direction
        except ZeroDivisionError:
            rotate_sign = 1
        if abs(rotate_direction) < rate:
            self.angle = angle
        else:
            self.angle += rate * rotate_sign

    def calculate_movement(self, dt):
        return [math.cos(self.angle) * self.speed * dt, math.sin(self.angle) * self.speed * dt]

    # gravity and friction
    def velocity_adjust(self, friction, force, terminal_velocity, dt):
        movement = self.calculate_movement(dt)
        movement[1] = min(terminal_velocity, movement[1] + force * dt)
        movement[0] *= friction
        self.angle = math.atan2(movement[1], movement[0])
        # if you want to get more realistic, the speed should be adjusted here

    def move(self, dt):
        movement = self.calculate_movement(dt)
        self.loc[0] += movement[0]
        self.loc[1] += movement[1]

        #Type of sparks
        if self.type == 0:
            self.point_towards(math.pi / 2, 0.02)
        if self.type == 1:
            self.velocity_adjust(0.975, 0.2, 8, dt)
        if self.type == 2:
            self.angle += 0.1

        self.speed -= 0.1

        if self.speed <= 0:
            self.alive = False

    def draw(self, surf, offset=[0, 0]):
        if self.alive:
            points = [
                [self.loc[0] + math.cos(self.angle) * self.speed * self.scale,
                 self.loc[1] + math.sin(self.angle) * self.speed * self.scale],
                [self.loc[0] + math.cos(self.angle + math.pi / 2) * self.speed * self.scale * 0.3,
                 self.loc[1] + math.sin(self.angle + math.pi / 2) * self.speed * self.scale * 0.3],
                [self.loc[0] - math.cos(self.angle) * self.speed * self.scale * 3.5,
                 self.loc[1] - math.sin(self.angle) * self.speed * self.scale * 3.5],
                [self.loc[0] + math.cos(self.angle - math.pi / 2) * self.speed * self.scale * 0.3,
                 self.loc[1] - math.sin(self.angle + math.pi / 2) * self.speed * self.scale * 0.3],
            ]
            pygame.draw.polygon(surf, self.color, points)


