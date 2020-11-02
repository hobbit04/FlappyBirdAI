import pygame as py
import sys, random
import numpy as np


def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, 450))
    screen.blit(floor_surface, (floor_x_pos + 288, 450))


def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop=(288, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom=(288, random_pipe_pos - 120))
    return bottom_pipe, top_pipe


def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 3
        if pipe.centerx <= -20:
            pipes.remove(pipe)
    return pipes


def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 512:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = py.transform.flip(pipe_surface, False, True)  # x축 회전 : F, y축 회전 : T
            screen.blit(flip_pipe, pipe)


def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return False
    if bird_rect.top <= -50 or bird_rect.bottom >= 450:
        return False

    return True


def rotate_bird(bird):
    new_bird = py.transform.rotozoom(bird, bird_movement * -3, 1)
    return new_bird


def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center=(50, bird_rect.centery))
    return new_bird, new_bird_rect


def score_display():
    score_surface = game_font.render(str(int(score)), True, (255, 255, 255))
    score_rect = score_surface.get_rect(center=(144, 100))
    screen.blit(score_surface, score_rect)


py.init()
screen = py.display.set_mode((288, 512))
clock = py.time.Clock()
game_font = py.font.Font('04B_19.TTF', 40)

# Game Variables
gravity = 0.25
bird_movement = 0
game_active = True
score = 0
high_score = 0

bg_surface = py.image.load('assets/background-day.png').convert()
floor_surface = py.image.load('assets/base.png').convert()
floor_x_pos = 0

bird_downflap = py.image.load('assets/bluebird-downflap.png').convert_alpha()
bird_midflap = py.image.load('assets/bluebird-midflap.png').convert_alpha()
bird_upflap = py.image.load('assets/bluebird-upflap.png').convert_alpha()
bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center=(50, 256))

birds = list()
for i in range(15):  # 우선은 하나의 새로만 (나중에 숫자 추가)
    birds.append(random.random())  # 0~1까지의 무작위 실수


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def jump_or_not(y_pos, up_dis, down_dis):  # 0과 1사이의 어떤 값을 리턴, 그 값이 0.6 이상이면 점프하도록, 새의 y좌표, 위 파이프와의 거리, 아래 파이프와의 거리
    h = [0 for i in range(5)]
    res1 = 0
    res2 = 0
    res3 = 0
    for k in range(15):
        res1 += birds[k] * y_pos
        res2 += birds[k] * up_dis
        res3 += birds[k] * down_dis
    for k in range(3):
        h[k] = sigmoid(res1 + res2 + res2)




BIRDFLAP = py.USEREVENT + 1
py.time.set_timer(BIRDFLAP, 200)

# bird_surface = py.image.load('assets/bluebird-midflap.png').convert_alpha()
# bird_rect = bird_surface.get_rect(center=(50, 256))

pipe_surface = py.image.load('assets/pipe-green.png').convert()
pipe_list = []
SPAWNPIPE = py.USEREVENT
py.time.set_timer(SPAWNPIPE, 1200)
pipe_height = [200, 300, 400]

while True:
    for event in py.event.get():
        if event.type == py.QUIT:
            py.quit()
            sys.exit()
        if event.type == py.KEYDOWN:
            if event.key == py.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 6

            if event.key == py.K_SPACE and not game_active:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (50, 256)
                bird_movement = 0
                bird_movement -= 6
                score = 0

        if event.type == SPAWNPIPE:  # 일정한 시간을 주기로 새로운 파이프 생성
            pipe_list.extend(create_pipe())

        if event.type == BIRDFLAP:  # 애니메이션 구현
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0

            bird_surface, bird_rect = bird_animation()

    screen.blit(bg_surface, (0, 0))

    if game_active:
        # Bird
        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird, bird_rect)
        game_active = check_collision(pipe_list)
        # Pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)
        score += 0.01

        score_display()

    # Floor
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -288:
        floor_x_pos = 0

    py.display.update()
    clock.tick(60)
