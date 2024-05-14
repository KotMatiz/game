import pygame
import random
import sys

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FPS = 60
ENEMY_SPAWN_RATE = 50

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Великий Рус против ящеров')
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        raw_image = pygame.image.load("Рус.png").convert_alpha()
        self.image = pygame.transform.scale(raw_image, (50, 50))
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.speed = 5

    def update(self, keys_pressed):
        if keys_pressed[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys_pressed[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed
        if keys_pressed[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys_pressed[pygame.K_DOWN] and self.rect.bottom < SCREEN_HEIGHT:
            self.rect.y += self.speed

class Enemy(pygame.sprite.Sprite):
    def __init__(self, level):
        super().__init__()
        raw_image = pygame.image.load("Ящер.png").convert_alpha()
        self.image = pygame.transform.scale(raw_image, (45, 45))
        if level == 1:
            self.rect = self.image.get_rect(center=(random.randint(20, SCREEN_WIDTH - 20), -30))
            self.speed_x = 0
            self.speed_y = random.randint(3, 6)
        elif level == 2:
            if random.choice([True, False]):
                self.rect = self.image.get_rect(center=(0, random.randint(20, SCREEN_HEIGHT - 20)))
                self.speed_x = random.randint(3, 6)
                self.speed_y = 0
            else:
                self.rect = self.image.get_rect(center=(random.randint(20, SCREEN_WIDTH - 20), 0))
                self.speed_x = 0
                self.speed_y = random.randint(3, 6)

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.top > SCREEN_HEIGHT or self.rect.left > SCREEN_WIDTH or self.rect.right < 0:
            self.kill()

def show_menu():
    menu_font = pygame.font.Font(None, 48)
    button_play = menu_font.render('Играть', True, WHITE)
    button_exit = menu_font.render('Выход', True, WHITE)
    button_play_rect = button_play.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
    button_exit_rect = button_exit.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 2 // 3))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if button_play_rect.collidepoint(x, y):
                    return 1
                elif button_exit_rect.collidepoint(x, y):
                    sys.exit()

        screen.fill(BLACK)
        screen.blit(button_play, button_play_rect)
        screen.blit(button_exit, button_exit_rect)
        pygame.display.flip()
        clock.tick(FPS)

def show_win_screen():
    win_font = pygame.font.Font(None, 72)
    win_text = win_font.render('YOU WIN', True, WHITE)
    win_rect = win_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                return

        screen.fill(BLACK)
        screen.blit(win_text, win_rect)
        pygame.display.flip()
        clock.tick(FPS)

def main(level):
    global ENEMY_SPAWN_RATE
    player = Player()
    all_sprites = pygame.sprite.Group(player)
    enemies = pygame.sprite.Group()
    score = 0
    frame_count = 0
    time_count = 0
    lives = 3

    running = True
    while running:
        screen.fill(WHITE)
        frame_count += 1
        time_count += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        if time_count % (FPS * 5) == 0:
            ENEMY_SPAWN_RATE -= 1
            if ENEMY_SPAWN_RATE < 5:
                ENEMY_SPAWN_RATE = 5

        if frame_count % ENEMY_SPAWN_RATE == 0:
            new_enemy = Enemy(level)
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

        keys_pressed = pygame.key.get_pressed()
        player.update(keys_pressed)
        enemies.update()

        if pygame.sprite.spritecollide(player, enemies, True):
            lives -= 1
            if lives <= 0:
                with open("scores.txt", "a") as file:
                    file.write(f"Level: {level}, Score: {score}\n")
                break

        if not pygame.sprite.spritecollide(player, enemies, False):
            score += 1

        if score >= 1000 and level == 1:
            level = 2
            score = 0
            lives = 3
            ENEMY_SPAWN_RATE = 18
            for enemy in enemies:
                enemy.kill()
            enemies.empty()

        if score >= 2000 and level == 2:
            show_win_screen()
            return

        screen.fill(BLACK)
        all_sprites.draw(screen)
        font = pygame.font.Font(None, 36)
        level_text = font.render(f"Level: {level}", True, WHITE)
        screen.blit(level_text, (SCREEN_WIDTH - 150, 10))
        text = font.render(f"Score: {score} Lives: {lives}", True, WHITE)
        screen.blit(text, (10, 10))
        pygame.display.flip()
        clock.tick(FPS)

    return

while True:
    selected_level = show_menu()
    if selected_level is None:
        break
    main(selected_level)
