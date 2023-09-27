import pygame
import random

pygame.init()
# ----------COLORS---------------------
green = (0, 255, 0)
red = (255, 0, 0)

# -------------WINDOW SETTINGS----------------
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Space invaders')
Icon = pygame.image.load('images/ico.png')
pygame.display.set_icon(Icon)

background_img = pygame.image.load("images/background.png")
background_y = 0
# ---------------------------------------------

# ------------------spaceship properties-----------------------
spaceship_img = pygame.image.load("images/spaceship.png")

spaceship_width = 50
spaceship_height = 50
spaceship_x = (SCREEN_WIDTH - spaceship_width) // 2
spaceship_y = SCREEN_HEIGHT - spaceship_height - 10
spaceship_speed = 5
move_left = False
move_right = False

# ------------------Bullet properties----------------------------
bullet_img = pygame.image.load("images/bullet.png")
bullet_width = 5
bullet_height = 15
bullet_velocity = 10
bullet_delay = 600
last_bullet_time = pygame.time.get_ticks()
bullets = []

# -----------------Alien properties-----------------------------
alien_img = pygame.image.load("images/alien.png")
alien_width = 100
alien_height = 50
alien_speed = 0.7
aliens = []

# -----------------Alien bullet properties----------------------
alien_bullet_width = 5
alien_bullet_height = 20
alien_bullet_velocity = 7
alien_bullet_delay = 1000
last_alien_bullet_time = pygame.time.get_ticks()
alien_bullets = []


# -----------------------------SCORE----------------------------
score = 0
font = pygame.font.Font(None, 36)

# ---------------------------Functions---------------------------


def draw_aliens(aliens):
    for alien in aliens:
        screen.blit(alien_img, (alien[0], alien[1]))


def draw_spaceship(x, y):
    screen.blit(spaceship_img, (x, y))


def draw_bullets(bullets):
    for bullet in bullets:
        screen.blit(bullet_img, (bullet[0], bullet[1]))


def background(y):
    screen.blit(background_img, (0, y))
    screen.blit(background_img, (0, y - SCREEN_HEIGHT))


def create_alien_bullet(alien_x, alien_y):
    return [alien_x + alien_width - alien_bullet_width / 2, alien_y + 100]


def draw_alien_bullets(alien_bullets):
    for bullet in alien_bullets:
        pygame.draw.rect(screen, red, (bullet[0], bullet[1], alien_bullet_width, alien_bullet_height))


def move_alien_bullets(alien_bullets):
    for bullet in alien_bullets:
        bullet[1] += alien_bullet_velocity
        if bullet[1] > SCREEN_HEIGHT:
            alien_bullets.remove(bullet)


def alien_bullet_hit(spaceship_x, spaceship_y, spaceship_width, spaceship_height):
    for bullet in alien_bullets:
        bullet_rect = pygame.Rect(bullet[0], bullet[1], alien_bullet_width, alien_bullet_height)
        spaceship_rect = pygame.Rect(spaceship_x, spaceship_y, spaceship_width, spaceship_height)
        if bullet_rect.colliderect(spaceship_rect):
            return True
    return False


# ------------Game loop-----------------
game_over = False
game_on = True
clock = pygame.time.Clock()

while game_on:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_on = False
            pygame.quit()
            break
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                move_left = True
            elif event.key == pygame.K_RIGHT:
                move_right = True
            elif event.key == pygame.K_SPACE:
                current_time = pygame.time.get_ticks()
                if current_time - last_bullet_time > bullet_delay:
                    bullets.append([spaceship_x + spaceship_width / 2 - bullet_width*6, spaceship_y-50])
                    last_bullet_time = current_time

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                move_left = False
            elif event.key == pygame.K_RIGHT:
                move_right = False

    if not game_over:
        if move_left and spaceship_x > 0:
            spaceship_x -= spaceship_speed
        if move_right and spaceship_x < SCREEN_WIDTH - spaceship_width:
            spaceship_x += spaceship_speed

        # ----------------bullets position-----------------
        for bullet in bullets:
            bullet[1] -= bullet_velocity
            if bullet[1] < 0:
                bullets.remove(bullet)

        for bullet in bullets:
            bullet_rect = pygame.Rect(bullet[0], bullet[1], bullet_width, bullet_height)
            for alien in aliens:
                alien_rect = pygame.Rect(alien[0], alien[1], alien_width, alien_height)
                if bullet_rect.colliderect(alien_rect):
                    bullets.remove(bullet)
                    aliens.remove(alien)
                    score += 1

        for alien in aliens:
            alien[1] += alien_speed

        for alien in aliens:
            if alien[1] + alien_height >= SCREEN_HEIGHT:
                game_over = True

        if random.random() < 0.01:
            alien_x = random.randint(0, SCREEN_WIDTH - alien_width)
            alien_y = - alien_height
            aliens.append([alien_x, alien_y])

        move_alien_bullets(alien_bullets)

        if alien_bullet_hit(spaceship_x, spaceship_y, spaceship_width, spaceship_height):
            game_over = True

        current_time = pygame.time.get_ticks()
        if current_time - last_alien_bullet_time > alien_bullet_delay:
            for alien in aliens:
                if random.random() < 0.1:
                    alien_bullets.append(create_alien_bullet(alien[0], alien[1]))
            last_alien_bullet_time = current_time

    background_y = (background_y + 1) % SCREEN_HEIGHT

    screen.fill((0, 0, 0))

    background(background_y)

    draw_spaceship(spaceship_x, spaceship_y)

    draw_bullets(bullets)

    draw_aliens(aliens)

    draw_alien_bullets(alien_bullets)

    score_text = font.render("Score: {}".format(score), True, green)
    screen.blit(score_text, (10, 10))

    if game_over:
        game_over_text = font.render("Game over - Press SPACE to restart", True, red)
        screen.blit(game_over_text, (SCREEN_HEIGHT//2 - game_over_text.get_width() // 2, 250 ))

    pygame.display.update()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and game_over:
        game_over = False
        score = 0
        bullets.clear()
        aliens.clear()
        alien_bullets.clear()
