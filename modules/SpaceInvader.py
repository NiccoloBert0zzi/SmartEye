import pygame
import sys
from data.entities import Player
import data.entities.Obstacle as Obstacle
from data.entities import Alien
from random import choice, randint
from data.entities import Laser
from geometry.Geometry import Geometry
from modules.IModule import Module


class SpaceInvader(Module):
    def __init__(self, width, height):
        margin_percentage = 0.3  # 10% margin on each side
        self.screen_original_width = width
        self.screen_width = width * (1 - 2 * margin_percentage)
        self.screen_height = height
        self.margin_x = width * margin_percentage

        # Adjust player position to be closer to the bottom
        player_sprite = Player.Player((self.screen_width / 2 + self.margin_x, self.screen_height - 50),
                                      self.screen_width,
                                      5, self.margin_x)
        self.player = pygame.sprite.GroupSingle(player_sprite)

        self.lives = 4
        self.live_surf = pygame.image.load('ui/graphics/heart.png').convert_alpha()
        # Adjust lives display position to be closer to the bottom
        self.live_x_start_pos = self.screen_width - (self.live_surf.get_size()[0] * 2 + 20) + self.margin_x
        self.live_y_pos = self.screen_height - self.live_surf.get_size()[1] - 10
        self.score = 0
        self.font = pygame.font.Font('ui/font/Pixeled.ttf', 20)

        self.shape = Obstacle.shape
        self.block_size = 6
        self.blocks = pygame.sprite.Group()
        self.obstacle_amount = 4
        self.obstacle_x_positions = [num * (self.screen_width / self.obstacle_amount) for num in
                                     range(self.obstacle_amount)]
        self.create_multiple_obstacles(*self.obstacle_x_positions, x_start=self.screen_width / 15 + self.margin_x,
                                       y_start=480)

        self.aliens = pygame.sprite.Group()
        self.alien_lasers = pygame.sprite.Group()
        self.alien_setup(rows=6, cols=8)
        self.alien_direction = 1

        self.extra = pygame.sprite.GroupSingle()
        self.extra_spawn_time = randint(40, 80)

        self.music = pygame.mixer.Sound('audio/music.wav')
        self.music.set_volume(0.2)

        self.laser_sound = pygame.mixer.Sound('audio/laser.wav')
        self.laser_sound.set_volume(0.5)
        self.explosion_sound = pygame.mixer.Sound('audio/explosion.wav')
        self.explosion_sound.set_volume(0.3)

        self.alien_laser_event = pygame.USEREVENT + 1
        self.alien_laser_initialized = False

        # CRT
        self.crt = CRT(width, height)

        # Initialize buttons
        self.buttons = self.create_buttons()

    def create_buttons(self):
        button_width = 150
        button_height = 70
        margin = 30

        vertical_center = (self.screen_height - button_height) // 2

        # Calculate horizontal center position for the left and right buttons
        lateral_space = (self.screen_original_width - self.screen_width) // 2
        horizontal_center_left = (lateral_space - button_width) // 2

        buttons = [
            {
                "top_left": (horizontal_center_left, vertical_center),
                "bottom_right": (horizontal_center_left + button_width, vertical_center + button_height),
                "text": "Spara",
                "key": "shoot"
            }
        ]
        return buttons

    def create_obstacle(self, x_start, y_start, offset_x):
        for row_index, row in enumerate(self.shape):
            for col_index, col in enumerate(row):
                if col == 'x':
                    x = x_start + col_index * self.block_size + offset_x
                    y = y_start + row_index * self.block_size
                    block = Obstacle.Block(self.block_size, (241, 79, 80), x, y)
                    self.blocks.add(block)

    def create_multiple_obstacles(self, *offset, x_start, y_start):
        for offset_x in offset:
            self.create_obstacle(x_start, y_start, offset_x)

    def alien_setup(self, rows, cols, x_distance=60, y_distance=48, x_offset=70, y_offset=100):
        for row_index in range(rows):
            for col_index in range(cols):
                x = col_index * x_distance + x_offset + self.margin_x
                y = row_index * y_distance + y_offset

                if row_index == 0:
                    alien_sprite = Alien.Alien('yellow', x, y)
                elif 1 <= row_index <= 2:
                    alien_sprite = Alien.Alien('green', x, y)
                else:
                    alien_sprite = Alien.Alien('red', x, y)
                self.aliens.add(alien_sprite)

    def alien_position_checker(self):
        all_aliens = self.aliens.sprites()
        for alien in all_aliens:
            if alien.rect.right >= self.screen_width + self.margin_x:
                self.alien_direction = -1
                self.alien_move_down(2)
            elif alien.rect.left <= self.margin_x:
                self.alien_direction = 1
                self.alien_move_down(2)

    def alien_move_down(self, distance):
        if self.aliens:
            for alien in self.aliens.sprites():
                alien.rect.y += distance

    def alien_shoot(self):
        if self.aliens.sprites():
            random_alien = choice(self.aliens.sprites())
            laser_sprite = Laser.Laser(random_alien.rect.center, 6, self.screen_height)
            self.alien_lasers.add(laser_sprite)
            self.laser_sound.play()

    def collision_checks(self):
        if self.player.sprite.lasers:
            for laser in self.player.sprite.lasers:
                if pygame.sprite.spritecollide(laser, self.blocks, True):
                    laser.kill()

                aliens_hit = pygame.sprite.spritecollide(laser, self.aliens, True)
                if aliens_hit:
                    for alien in aliens_hit:
                        self.score += alien.value
                    laser.kill()
                    self.explosion_sound.play()

                if pygame.sprite.spritecollide(laser, self.extra, True):
                    self.score += 500
                    laser.kill()

        if self.alien_lasers:
            for laser in self.alien_lasers:
                if pygame.sprite.spritecollide(laser, self.blocks, True):
                    laser.kill()

                if pygame.sprite.spritecollide(laser, self.player, False):
                    laser.kill()
                    self.lives -= 1
                    if self.lives <= 0:
                        pygame.quit()
                        sys.exit()

        if self.aliens:
            for alien in self.aliens:
                pygame.sprite.spritecollide(alien, self.blocks, True)

                if pygame.sprite.spritecollide(alien, self.player, False):
                    pygame.quit()
                    sys.exit()

    def display_lives(self, screen):
        for live in range(self.lives - 1):
            x = self.live_x_start_pos + (live * (self.live_surf.get_size()[0] + 10))
            screen.blit(self.live_surf, (x, self.live_y_pos))

    def display_score(self, screen):
        # Adjust score display position to be closer to the center
        score_surf = self.font.render(f'score: {self.score}', False, 'white')
        score_rect = score_surf.get_rect(center=(self.screen_width / 2, 20))
        screen.blit(score_surf, score_rect)

    def check_victory(self, screen):
        if not self.aliens.sprites():
            victory_surf = self.font.render('You won', False, 'white')
            victory_rect = victory_surf.get_rect(center=(self.screen_width / 2, self.screen_height / 2))
            screen.blit(victory_surf, victory_rect)

    def run(self, image_data, **kwargs):
        fingers = kwargs.get('fingers', [])
        if not self.alien_laser_initialized:
            self.music.play(loops=-1)
            pygame.time.set_timer(self.alien_laser_event, 1000)
            self.alien_laser_initialized = True

        for event in pygame.event.get():
            if event.type == self.alien_laser_event:
                self.alien_shoot()
        self.player.update(fingers)
        self.alien_lasers.update()
        self.extra.update()

        self.aliens.update(self.alien_direction)
        self.alien_position_checker()
        self.collision_checks()

    def draw_buttons(self, screen):
        for button in self.buttons:
            Geometry.draw_square_with_text(screen,
                                           button["top_left"],
                                           button["bottom_right"],
                                           button["text"])

    def draw(self, screen, **kwargs):
        self.player.sprite.lasers.draw(screen)
        self.player.draw(screen)
        self.blocks.draw(screen)
        self.aliens.draw(screen)
        self.alien_lasers.draw(screen)
        self.display_lives(screen)
        self.display_score(screen)
        self.check_victory(screen)
        self.draw_buttons(screen)

        self.crt.draw(screen)

    def destroy(self, **kwargs):
        pass

    def get_module_name(self):
        return 'Space Invader'


class CRT:
    def __init__(self, width, height):
        self.tv = pygame.image.load('ui/graphics/tv.png').convert_alpha()
        self.tv = pygame.transform.scale(self.tv, (width, height))
        self.width = width
        self.height = height

    def create_crt_lines(self):
        line_height = 3
        line_amount = int(self.width / self.height)
        for line in range(line_amount):
            y_pos = line * line_height
            pygame.draw.line(self.tv, 'black', (0, y_pos), (self.width, y_pos), 1)

    def draw(self, screen):
        self.tv.set_alpha(randint(75, 90))
        self.create_crt_lines()
        screen.blit(self.tv, (0, 0))