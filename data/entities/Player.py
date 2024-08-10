import pygame

from controllers.HandGestureController import HandGestureController
from data.entities import Laser


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, constraint, speed, margin_x):
        super().__init__()
        self.image = pygame.image.load('ui/graphics/player.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom=pos)
        self.speed = speed
        self.max_x_constraint = constraint
        self.margin_x = margin_x
        self.ready = True
        self.laser_time = 0
        self.laser_cooldown = 600

        self.lasers = pygame.sprite.Group()

        self.laser_sound = pygame.mixer.Sound('audio/laser.wav')
        self.laser_sound.set_volume(0.5)

    def get_input(self, fingers, buttons):
        if not fingers:
            return None, None
        clicking, click_index = HandGestureController.check_if_click(fingers, buttons)
        if clicking:
            if buttons[click_index]["key"] == ">":
                self.rect.x += self.speed
            elif buttons[click_index]["key"] == "<":
                self.rect.x -= self.speed
            elif buttons[click_index]["key"] == "shoot" and self.ready:
                self.shoot_laser()
                self.ready = False
                self.laser_time = pygame.time.get_ticks()
                self.laser_sound.play()

    def recharge(self):
        if not self.ready:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_time >= self.laser_cooldown:
                self.ready = True

    def constraint(self):
        if self.rect.left <= self.margin_x:
            self.rect.left = self.margin_x
        if self.rect.right >= self.max_x_constraint + self.margin_x:
            self.rect.right = self.max_x_constraint + self.margin_x

    def shoot_laser(self):
        self.lasers.add(Laser.Laser(self.rect.center, -8, self.rect.bottom))

    def update(self, fingers, buttons):
        self.get_input(fingers, buttons)
        self.constraint()
        self.recharge()
        self.lasers.update()
