import pygame
import random

pygame.init()

WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Break-it Game")

WHITE = (255, 255, 255)
GREY = (100, 100, 100)
ORANGE = (255, 165, 0)
BROWN = (165, 42, 42)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

FPS = 60
BRICK_ROWS = 6
BRICK_COLS = 10
BRICK_WIDTH = WIDTH // BRICK_COLS
BRICK_HEIGHT = 30

bar = pygame.Rect(WIDTH // 2 - 50, HEIGHT - 30, 100, 10)
ball = pygame.Rect(WIDTH // 2, HEIGHT // 2, 15, 15)
ball_speed = [4, -4]

score = 0
font = pygame.font.SysFont(None, 36)

brick_map = []
for row in range(BRICK_ROWS):
    brick_row = []
    for col in range(BRICK_COLS):
        brick_type = random.choices([GREY, ORANGE, BROWN, GREEN], weights=[40, 40, 15, 5])[0]
        brick_row.append({'rect': pygame.Rect(col * BRICK_WIDTH + 1, row * BRICK_HEIGHT + 1, BRICK_WIDTH - 2, BRICK_HEIGHT - 2), 'color': brick_type})
    brick_map.append(brick_row)

paused = False
bar_bonus = False
explosive_bonus = False
projectile_bonus = False
projectiles = []
max_projectiles = 5
speed_boost = False

clock = pygame.time.Clock()

running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            paused = not paused
        if event.type == pygame.KEYDOWN and event.key == pygame.K_v:
            speed_boost = not speed_boost
            if speed_boost:
                ball_speed = [s * 1.5 for s in ball_speed]
            else:
                ball_speed = [4 if s > 0 else -4 for s in ball_speed]
        if event.type == pygame.KEYDOWN and event.key == pygame.K_f and projectile_bonus and len(projectiles) < max_projectiles:
            projectiles.append(pygame.Rect(bar.centerx - 2, bar.top - 10, 4, 10))

    if paused:
        continue

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and bar.left > 0:
        bar.left -= 7
    if keys[pygame.K_RIGHT] and bar.right < WIDTH:
        bar.right += 7

    ball.x += ball_speed[0]
    ball.y += ball_speed[1]

    if ball.left <= 0 or ball.right >= WIDTH:
        ball_speed[0] = -ball_speed[0]
    if ball.top <= 0:
        ball_speed[1] = -ball_speed[1]

    if ball.colliderect(bar):
        ball_speed[1] = -ball_speed[1]

    for projectile in projectiles:
        projectile.y -= 8

    projectiles = [p for p in projectiles if p.bottom > 0]

    for projectile in projectiles:
        for row in brick_map:
            for brick in row:
                if brick['color'] != None and projectile.colliderect(brick['rect']):
                    if brick['color'] == ORANGE:
                        brick['color'] = None
                        score += 1
                    elif brick['color'] == BROWN:
                        brick['color'] = ORANGE
                    elif brick['color'] == GREEN:
                        bonus = random.choice([1, 2, 3])
                        if bonus == 1:
                            bar_bonus = True
                            bar.width = 200
                        elif bonus == 2:
                            explosive_bonus = True
                        elif bonus == 3:
                            projectile_bonus = True
                        brick['color'] = None
                        score += 1
                    projectiles.remove(projectile)
                    break

    for row in brick_map:
        for brick in row:
            if brick['color'] != None and ball.colliderect(brick['rect']):
                ball_speed[1] = -ball_speed[1]
                if brick['color'] == ORANGE:
                    brick['color'] = None
                    score += 1
                elif brick['color'] == BROWN:
                    brick['color'] = ORANGE
                elif brick['color'] == GREEN:
                    bonus = random.choice([1, 2, 3])
                    if bonus == 1:
                        bar_bonus = True
                        bar.width = 200
                    elif bonus == 2:
                        explosive_bonus = True
                    elif bonus == 3:
                        projectile_bonus = True
                    brick['color'] = None
                    score += 1
                if explosive_bonus:
                    neighbors = []
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue
                            r = brick_map.index(row)
                            c = row.index(brick)
                            nr, nc = r + dr, c + dc
                            if 0 <= nr < BRICK_ROWS and 0 <= nc < BRICK_COLS:
                                neighbor = brick_map[nr][nc]
                                if neighbor['color'] in [ORANGE, BROWN, GREEN]:
                                    neighbors.append(neighbor)
                    for neighbor in neighbors:
                        if neighbor['color'] == ORANGE:
                            neighbor['color'] = None
                            score += 1
                        elif neighbor['color'] == BROWN:
                            neighbor['color'] = ORANGE
                        elif neighbor['color'] == GREEN:
                            bonus = random.choice([1, 2, 3])
                            if bonus == 1:
                                bar_bonus = True
                                bar.width = 200
                            elif bonus == 2:
                                explosive_bonus = True
                            elif bonus == 3:
                                projectile_bonus = True
                            neighbor['color'] = None
                            score += 1

    if ball.bottom >= HEIGHT:
        running = False

    SCREEN.fill(BLACK)
    pygame.draw.rect(SCREEN, WHITE, pygame.Rect(0, 0, WIDTH, HEIGHT), 2)
    pygame.draw.rect(SCREEN, WHITE, bar)
    pygame.draw.ellipse(SCREEN, WHITE, ball)

    for projectile in projectiles:
        pygame.draw.rect(SCREEN, (0, 255, 255), projectile)

    for row in brick_map:
        for brick in row:
            if brick['color'] != None:
                pygame.draw.rect(SCREEN, brick['color'], brick['rect'])

    score_text = font.render(f"Score: {score}", True, WHITE)
    SCREEN.blit(score_text, (10, HEIGHT - 40))

    pygame.display.flip()

pygame.quit()
