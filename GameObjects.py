import pygame
import math
import random

from config import *


class GameObject(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()

        self.original_image = pygame.image.load(image).convert_alpha()
        self.image = self.original_image

        self.pos = pygame.Vector2(-400.0, -300.0)
        self.rect: pygame.FRect = self.image.get_rect(center=self.pos)

        self.angle = 0
        self.dt = 0

    def rotate(self, r_speed):
        self.angle += r_speed * self.dt
        self.angle %= 360

        self.image = pygame.transform.rotate(self.original_image, -self.angle)

        self.rect = self.image.get_rect(center=self.rect.center)


class Bullet(GameObject):
    def __init__(self, image, pos, velocity, r):
        super().__init__(image)
        self.angle = r + 90
        self.velocity = velocity.copy()
        self.pos = pos.copy()

        self.time = 0
        self.life_time = 3
        self.image = pygame.transform.rotate(self.original_image, -self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self, dt):
        self.dt = dt
        self.time += self.dt
        if self.time >= self.life_time:
            self.kill()

        self.pos += self.velocity * self.dt
        self.rect.center = self.pos

    def check_collision(self, asteroids):
        for asteroid in asteroids:
            collision_point = pygame.sprite.collide_mask(self, asteroid)
            if collision_point:
                self.kill()
                asteroid.kill()


class Player(GameObject):
    def __init__(self, image, game):
        super().__init__(image)

        self.velocity = pygame.Vector2(0, 0)
        self.acceleration = 600
        self.friction = 0.999

        self.rotation_speed = 120

        self.bullets = pygame.sprite.Group()

        self.shoot_time = 0
        self.cd = 0.5
        self.game = game
        self.pos = pygame.Vector2(self.game.window.get_size()[0] / 2, self.game.window.get_size()[1] / 2)
        self.rect.center = self.pos

    def get_bullets_group(self):
        return self.bullets

    def update(self, m_keys, dt):
        self.bullets.update(self.dt)
        self.dt = dt
        self.handle_input(m_keys)

        self.pos += self.velocity * self.dt
        self.check_bounds()

        self.velocity *= self.friction / 1.5 ** self.dt

        self.rect.center = self.pos
        self.shoot_time += self.dt

    def check_bounds(self):
        window_width, window_height = self.game.window.get_size()
        image_width, image_height = self.image.get_size()

        # Проверка границ по оси X
        if self.pos.x > window_width:
            self.pos.x = -image_width
        elif self.pos.x < -image_width:
            self.pos.x = window_width

        # Проверка границ по оси Y
        if self.pos.y > window_height:
            self.pos.y = -image_height
        elif self.pos.y < -image_height:
            self.pos.y = window_height

    def handle_input(self, m_keys):
        if m_keys[pygame.K_UP] or m_keys[pygame.K_w]:
            self.velocity += self.move() * self.dt
        elif m_keys[pygame.K_DOWN] or m_keys[pygame.K_s]:
            self.velocity *= self.friction / 16 ** self.dt

        if m_keys[pygame.K_LEFT] or m_keys[pygame.K_a]:
            self.rotate(-self.rotation_speed)
        elif m_keys[pygame.K_RIGHT] or m_keys[pygame.K_d]:
            self.rotate(self.rotation_speed)

        if m_keys[pygame.K_SPACE] and self.shoot_time > self.cd:
            self.shoot()
            self.shoot_time = 0

    def move(self):
        r_ang = math.radians(self.angle - 90)
        return pygame.Vector2(math.cos(r_ang) * self.acceleration, math.sin(r_ang) * self.acceleration)

    def shoot(self):
        self.bullets.add(
            Bullet("Images/Laser.png", self.pos, pygame.Vector2(math.cos(math.radians(self.angle - 90)) *
                                                                         self.acceleration / 2, math.sin(
                math.radians(self.angle - 90)) * self.acceleration / 2), self.angle))

    def check_collision(self, asteroids):
        for asteroid in asteroids:
            collision_point = pygame.sprite.collide_mask(self, asteroid)
            if collision_point:
                return True
        return False

    def stop(self):
        self.velocity *= 0
        self.acceleration += 0
        self.cd = 999
        self.friction = 0
        self.dt = 0
        self.rotation_speed = 0


class Small_Asteroid(GameObject):
    def __init__(self, image, group, game):
        super().__init__(image)
        self.velocity = pygame.Vector2(random.randrange(*VELOCITY_SMALL_ASTEROID),
                                       random.randrange(*VELOCITY_SMALL_ASTEROID))
        self.rot_angle = random.randint(*ROTATION_SMALL_ASTEROID)
        self.group = group
        self.game = game

    def setPos(self, pos):
        self.pos = pos

    def update(self, dt):
        self.dt = dt

        self.pos += self.velocity * self.dt
        self.check_bounds()

        self.rect.center = self.pos
        self.rotate(self.rot_angle)

    def check_bounds(self):
        window_width, window_height = self.game.window.get_size()
        image_width, image_height = self.image.get_size()

        # Проверка границ по оси X
        if self.pos.x > window_width:
            self.pos.x = -image_width
        elif self.pos.x < -image_width:
            self.pos.x = window_width

        # Проверка границ по оси Y
        if self.pos.y > window_height:
            self.pos.y = -image_height
        elif self.pos.y < -image_height:
            self.pos.y = window_height

    def kill(self):
        super().kill()
        self.game.score += 50


class Medium_Asteroid(Small_Asteroid):
    def __init__(self, image, group, game):
        super().__init__(image, group, game)
        self.rot_angle = random.randint(*ROTATION_MEDIUM_ASTEROID)
        self.velocity = pygame.Vector2(random.randrange(*VELOCITY_MEDIUM_ASTEROID),
                                       random.randrange(*VELOCITY_MEDIUM_ASTEROID))

    def explode(self):
        for _ in range(ASTEROIDS_COUNT):
            a = Small_Asteroid("Images/Small_Asteroid.png", self.group, self.game)
            a.setPos(self.pos.copy())
            self.group.add(a)

    def kill(self):
        self.game.score += 50
        self.explode()
        super().kill()


class Big_Asteroid(Small_Asteroid):
    def __init__(self, image, group, game):
        super().__init__(image, group, game)
        self.rot_angle = random.randint(*ROTATION_BIG_ASTEROID)
        self.velocity = pygame.Vector2(random.randrange(*VELOCITY_BIG_ASTEROID),
                                       random.randrange(*VELOCITY_BIG_ASTEROID))

    def explode(self):
        for _ in range(ASTEROIDS_COUNT):
            a = Medium_Asteroid("Images/Medium_Asteroid.png", self.group, self.game)
            a.setPos(self.pos.copy())
            self.group.add(a)

    def kill(self):
        self.game.score += 100
        self.explode()
        super().kill()

 
class TextLayer:
    def __init__(self, text, font_name='Images/p_emu.otf', font_size=30, color=(255, 255, 255), position=(0, 0)):
        self.text = text
        self.font_name = font_name
        self.font_size = font_size
        self.color = color
        self.position = position
        self.font = pygame.font.Font(self.font_name, self.font_size)
        self.surface = self.font.render(self.text, True, self.color)
        self.rect = self.surface.get_rect(topleft=self.position)

    def update_text(self, new_text):
        self.text = new_text
        self.surface = self.font.render(self.text, True, self.color)
        self.rect = self.surface.get_rect(topleft=self.position)

    def draw(self, screen):
        screen.blit(self.surface, self.rect)
