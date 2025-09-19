import pygame as pg
from random import randrange

# Konstanter
WINDOW = 1000
TILE_SIZE = 50
RANGE = (TILE_SIZE // 2, WINDOW - TILE_SIZE // 2, TILE_SIZE)
get_random_position = lambda: [randrange(*RANGE), randrange(*RANGE)]

# Ormen
snake = pg.Rect([0, 0, TILE_SIZE - 2, TILE_SIZE - 2])
snake.center = get_random_position()
length = 1
segments = [snake.copy()]
snake_dir = (0, 0)

# Mat
food = snake.copy()
food.center = get_random_position()

# Setup
pg.init()  # NYTT: Initiera pygame
screen = pg.display.set_mode([WINDOW] * 2)
clock = pg.time.Clock()
time, time_step = 0, 110
dirs = {pg.K_w: 1, pg.K_s: 1, pg.K_a: 1, pg.K_d: 1}

# NYTT: Font och score
font = pg.font.SysFont("Arial", 30)
score = 0

# Game loop
while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_w and dirs[pg.K_w]:
                snake_dir = (0, -TILE_SIZE)
                dirs = {pg.K_w: 1, pg.K_s: 0, pg.K_a: 1, pg.K_d: 1}
            if event.key == pg.K_s and dirs[pg.K_s]:
                snake_dir = (0, TILE_SIZE)
                dirs = {pg.K_w: 0, pg.K_s: 1, pg.K_a: 1, pg.K_d: 1}
            if event.key == pg.K_a and dirs[pg.K_a]:
                snake_dir = (-TILE_SIZE, 0)
                dirs = {pg.K_w: 1, pg.K_s: 1, pg.K_a: 1, pg.K_d: 0}
            if event.key == pg.K_d and dirs[pg.K_d]:
                snake_dir = (TILE_SIZE, 0)
                dirs = {pg.K_w: 1, pg.K_s: 1, pg.K_a: 0, pg.K_d: 1}

    screen.fill('black')

    # Kollision med väggar eller sig själv
    self_eating = pg.Rect.collidelist(snake, segments[:-1]) != -1
    if (
        snake.left < 0 or snake.right > WINDOW or
        snake.top < 0 or snake.bottom > WINDOW or
        self_eating
    ):
        snake.center, food.center = get_random_position(), get_random_position()
        length, snake_dir, score = 1, (0, 0), 0   # NYTT: Reset poäng
        segments = [snake.copy()]

    # Kolla om ormen äter mat
    if snake.center == food.center:
        food.center = get_random_position()
        length += 1
        score += 10   # NYTT: +10 poäng per äpple

    # Rita mat
    pg.draw.rect(screen, 'red', food)

    # Rita orm
    [pg.draw.rect(screen, 'green', segment) for segment in segments]

    # Flytta ormen
    time_now = pg.time.get_ticks()
    if time_now - time > time_step:
        time = time_now
        snake.move_ip(snake_dir)
    segments.append(snake.copy())
    segments = segments[-length:]

    # NYTT: Rita poäng på skärmen
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    # Uppdatera display
    pg.display.flip()
    clock.tick(60)
