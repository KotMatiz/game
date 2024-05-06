import pygame
import sys
import random

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FPS = 60
ENEMY_SPAWN_RATE = 50

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Игра')
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.speed = 5

    def update(self, *args):
        keys_pressed = args[0]
        if keys_pressed[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys_pressed[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed
        if keys_pressed[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys_pressed[pygame.K_DOWN] and self.rect.bottom < SCREEN_HEIGHT:
            self.rect.y += self.speed

class Enemy(pygame.sprite.Sprite):
    def __init__(self, speed_multiplier=1):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(RED)
        self.rect = self.image.get_rect(center=(random.randint(20, SCREEN_WIDTH - 20), -30))
        self.speed = random.randint(3, 6) * speed_multiplier

    def update(self, *args):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

def show_menu():
    menu_font = pygame.font.Font(None, 48)
    button_1 = menu_font.render('Уровень 1', True, WHITE)
    button_2 = menu_font.render('Уровень 2', True, WHITE)
    button_exit = menu_font.render('Выход', True, WHITE)

    button_1_rect = button_1.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
    button_2_rect = button_2.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    button_exit_rect = button_exit.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 2 // 3))

    buttons = [(button_1, button_1_rect, 1), (button_2, button_2_rect, 2), (button_exit, button_exit_rect, 0)]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None  # Если пользователь закрыл окно, возвращаем None
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                for button, rect, level in buttons:
                    if rect.collidepoint(x, y):
                        if level == 0:
                            return None  # Если пользователь выбрал выход, возвращаем None
                        else:
                            return level  # Возвращаем выбранный уровень

        screen.fill(BLACK)
        for button, rect, _ in buttons:
            screen.blit(button, rect)
        pygame.display.flip()
        clock.tick(FPS)

def main(level):
    global ENEMY_SPAWN_RATE
    if level == 1:
        target_score = 500
        ENEMY_SPAWN_RATE = 50
    elif level == 2:
        target_score = 1000
        ENEMY_SPAWN_RATE = 25

    player = Player()
    all_sprites = pygame.sprite.Group(player)
    enemies = pygame.sprite.Group()
    score = 0
    frame_count = 0

    running = True
    while running:
        frame_count += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return  # Выход из функции и возвращение в главное меню
        if frame_count % ENEMY_SPAWN_RATE == 0:
            new_enemy = Enemy(speed_multiplier=1.5 if level == 2 else 1)
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

        keys_pressed = pygame.key.get_pressed()
        all_sprites.update(keys_pressed)

        if pygame.sprite.spritecollide(player, enemies, True):
            score -= 100
        else:
            score += 1

        if score >= target_score:
            break  # Достигнута целевая оценка, выход из цикла

        screen.fill(BLACK)
        all_sprites.draw(screen)
        font = pygame.font.Font(None, 36)
        text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(text, (10, 10))
        pygame.display.flip()
        clock.tick(FPS)

    return  # Возвращение в главное меню

while True:
    selected_level = show_menu()
    if selected_level is None:
        break  # Если функция show_menu вернула None, завершаем программу
    main(selected_level)