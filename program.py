import pygame
import os
pygame.font.init()  # font library
pygame.mixer.init() # sound library

# window of the game - size and title
WIDTH = 900
HEIGHT = 600
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Spaceship Duel")

# background image
BACKGROUND_IMAGE = pygame.image.load(
    os.path.join('Graphics', 'background.png'))
# border in the center of the window
BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

# sounds
BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Graphics', 'esm_8bit_explosion_medium_bomb_boom_blast_cannon_retro_old_school_classic_cartoon.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Graphics', 'zapsplat_warfare_bullet_whizz_by_001_61427.mp3'))

# frame per second of the game
FPS = 60

# speed of spaceships
SPEED = 5

# bullets
BULLET = 7
MAX_BULLETS = 6
BLUE_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

# display text
HEALTH_FONT = pygame.font.SysFont('consolas', 30)
WINNER_FONT = pygame.font.SysFont('consolas', 100)

# drawing spaceships
SPACESHIP_WIDTH = 79
SPACESHIP_HEIGHT = 91

BLUE_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Graphics', 'spaceship_1.png'))
BLUE_SPACESHIP = pygame.transform.rotate(BLUE_SPACESHIP_IMAGE, -90)

RED_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Graphics', 'spaceship_2.png'))
RED_SPACESHIP = pygame.transform.rotate(RED_SPACESHIP_IMAGE, 90)


def draw_window(blue, red, blueBullets, redBullets, blueHealth, redHealth):
    WINDOW.blit(BACKGROUND_IMAGE, (0, 0))
    pygame.draw.rect(WINDOW, (0, 0, 77), BORDER)

    blueHealthText = HEALTH_FONT.render(
        'Health:' + str(blueHealth), 1, (204, 204, 255))
    redHealthText = HEALTH_FONT.render(
        'Health:' + str(redHealth), 1, (204, 204, 255))
    WINDOW.blit(redHealthText, (WIDTH - blueHealthText.get_width() - 10, 10))
    WINDOW.blit(blueHealthText, (10, 10))

    WINDOW.blit(BLUE_SPACESHIP, (blue.x, blue.y))
    WINDOW.blit(RED_SPACESHIP, (red.x, red.y))

    for bullet in redBullets:
        pygame.draw.rect(WINDOW, (255, 255, 0), bullet)
    for bullet in blueBullets:
        pygame.draw.rect(WINDOW, (255, 255, 0), bullet)

    pygame.display.update()


def blue_spaceship_movement(keys_pressed, blue):
    if keys_pressed[pygame.K_w] and blue.y - SPEED > 0:  # up
        blue.y -= SPEED
    elif keys_pressed[pygame.K_s] and blue.y + SPEED + blue.height < HEIGHT:  # down
        blue.y += SPEED
    elif keys_pressed[pygame.K_a] and blue.x - SPEED > 0:  # left
        blue.x -= SPEED
    elif keys_pressed[pygame.K_d] and blue.x + SPEED + blue.width < BORDER.x:  # right
        blue.x += SPEED


def red_spaceship_movement(keys_pressed, red):
    if keys_pressed[pygame.K_UP] and red.y - SPEED > 0:  # up
        red.y -= SPEED
    elif keys_pressed[pygame.K_DOWN] and red.y + SPEED + red.height < HEIGHT:  # down
        red.y += SPEED
    elif keys_pressed[pygame.K_LEFT] and red.x - SPEED > BORDER.x + BORDER.width:  # left
        red.x -= SPEED
    elif keys_pressed[pygame.K_RIGHT] and red.x + SPEED + red.width < WIDTH:  # right
        red.x += SPEED


def handle_bullets(blueBullets, redBullets, blue, red):
    for bullet in blueBullets:
        bullet.x += BULLET
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            blueBullets.remove(bullet)
        elif bullet.x > WIDTH:      # bullet out of screen
            blueBullets.remove(bullet)

    for bullet in redBullets:
        bullet.x -= BULLET
        if blue.colliderect(bullet):
            pygame.event.post(pygame.event.Event(BLUE_HIT))
            redBullets.remove(bullet)
        elif bullet.x < 0:          # bullet out of screen
            redBullets.remove(bullet)

def draw_text(text):
    draw_text = WINNER_FONT.render(text, 1, (77, 77, 255))
    WINDOW.blit(draw_text, (WIDTH//2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(3000)
    

def main():
    # rectangle for spaceship
    blue = pygame.Rect(150, 240, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    red = pygame.Rect(680, 240, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    blueBullets = []
    redBullets = []

    blueHealth = 10
    redHealth = 10

    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(blueBullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        blue.x + blue.width, blue.y + blue.height//2 - 2, 10, 5)
                    blueBullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(redBullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        red.x, red.y + red.height//2 - 2, 10, 5)
                    redBullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == BLUE_HIT:
                blueHealth -= 1
                BULLET_HIT_SOUND.play()

            if event.type == RED_HIT:
                redHealth -= 1
                BULLET_HIT_SOUND.play()

        winner_text = ''
        if redHealth <= 0:
            winner_text = 'Blue Wins!'

        if blueHealth <= 0:
            winner_text = 'Red Wins!'

        if winner_text != '':
            draw_text(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()

        blue_spaceship_movement(keys_pressed, blue)
        red_spaceship_movement(keys_pressed, red)

        handle_bullets(blueBullets, redBullets, blue, red)
        draw_window(blue, red, blueBullets, redBullets, blueHealth, redHealth)

    main()


if __name__ == "__main__":
    main()
