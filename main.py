import pygame, sys, random


def p1_reset():
    global p1_top, p1_bottom
    p1_y = random.randint(100, 350)
    p1_top = pygame.Rect(screen_width, 0, 70, p1_y)
    p1_bottom = pygame.Rect(p1_top.x, p1_top.bottom + 150, 70,
                            screen_height - (p1_top.top + p1_top.bottom) - 150)


def p2_reset():
    global p2_top, p2_bottom, p2_indicator
    p2_y = random.randint(100, 350)
    p2_top = pygame.Rect(screen_width, 0, 70, p2_y)
    p2_bottom = pygame.Rect(p2_top.x, p2_top.bottom + 150, 70,
                            screen_height - (p2_top.top + p2_top.bottom) - 150)
    p2_indicator = False


def pillar1_animation():
    pygame.draw.rect(screen, (0, 0, 0), p1_top)
    pygame.draw.rect(screen, (0, 0, 0), p1_bottom)
    p1_top.left -= pillar_speed
    p1_bottom.left -= pillar_speed


def pillar2_animation():
    if p2_indicator:
        pygame.draw.rect(screen, (0, 0, 0), p2_top)
        pygame.draw.rect(screen, (0, 0, 0), p2_bottom)
        p2_top.left -= pillar_speed
        p2_bottom.left -= pillar_speed


def collision():
    global fall_speed, pillar_speed, player_jump, game_state
    if player.collidelistall((p1_top, p1_bottom, p2_top, p2_bottom)):
        fall_speed = 0
        pillar_speed = 0
        player_jump = 0
        game_state = "stopped"

    if game_state == "stopped":
        lose_text = game_font.render(f"GAME OVER", False, (255, 0, 0))
        lose_choice = game_font.render("Press 'y' to Restart 'q' to Quit", False, (255, 255, 255))
        screen.blit(lose_text, (410, 50))
        screen.blit(lose_choice, (300, 150))


def pillar_re_setter():
    global score, p2_indicator
    if p1_top.x < 500:
        p2_indicator = True

    if p1_top.right < 0:
        score += 1
        p1_reset()

    if p2_top.right < 0:
        score += 1
        p2_reset()


pygame.init()
clock = pygame.time.Clock()

# Game screen
screen_width = 940
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("flappy bird")

# initializing pillar1 and pillar2
p1_reset()
p2_reset()

# player image loading and placement
image = pygame.image.load("flappy_60x60.png")
player = image.get_rect()
player.center = (screen_width / 2 - 30, screen_height / 2 - 30)

# pillars
pillar_speed = 5
fall_speed = 2.3
player_jump = 60
game_state = "running"

score = 0

game_font = pygame.font.Font("freesansbold.ttf", 32)

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.top -= player_jump

            if game_state == "stopped":
                if event.key == pygame.K_y:
                    p1_reset()
                    p2_reset()
                    p2_indicator = False
                    pillar_speed = 5
                    fall_speed = 2.3
                    player_jump = 60
                    score = 0
                    game_state = "running"
                    player.center = [screen_width / 2 - 30, screen_height / 2 - 100]
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

    screen.fill((200, 200, 200))

    screen.blit(image, player)
    player.bottom += fall_speed

    pillar1_animation()
    pillar2_animation()

    pillar_re_setter()

    collision()

    score_text = game_font.render(f"Score : {score}", False, (255, 255, 255))
    screen.blit(score_text, (20, 30))

    pygame.display.flip()
    clock.tick(60)
