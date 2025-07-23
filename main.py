# -*- coding: utf-8 -*-
import pygame
import random
import sys

# 初始化
pygame.init()

# 畫面尺寸
WIDTH, HEIGHT = 500, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sheep chiikawa game")

# 顏色
WHITE = (255, 255, 255)
BLUE = (100, 150, 255)
RED = (255, 100, 100)

# 角色參數
player_size = 50
player_x = WIDTH // 2 - player_size // 2
player_y = HEIGHT - player_size - 10
player_speed = 5

# 障礙物參數
obstacle_size = 30
obstacle_speed = 5
obstacles = []

# 遊戲時鐘
clock = pygame.time.Clock()

# 字型
font = pygame.font.SysFont(None, 48)

def draw_player(x, y):
    player_img = pygame.image.load("assets/player.png")
    player_img = pygame.transform.scale(player_img, (player_size, player_size))
    screen.blit(player_img, (x, y))
    # pygame.draw.rect(screen, BLUE, (x, y, player_size, player_size))

def draw_obstacle(x, y):
    tako_image = pygame.image.load("assets/tako.png")
    tako_image = pygame.transform.scale(tako_image, (obstacle_size, obstacle_size))
    screen.blit(tako_image, (x, y))
    # pygame.draw.circle(screen, RED, (x + obstacle_size // 2, y + obstacle_size // 2), obstacle_size // 2)

def show_game_over(): 
    font = pygame.font.Font("Fonts/msjh.ttc", 24)#本文主角
    text = font.render("兩周年快樂寶寶!", True, (0, 0, 0))
    rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, rect)
    pygame.display.update()
    pygame.time.wait(2000)


def draw_score():
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))



score = 0
running = True

# 主迴圈
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 鍵盤控制
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < WIDTH - player_size:
        player_x += player_speed

    # 生出障礙物
    if random.random() < 0.05:
        obstacle_x = random.randint(0, WIDTH - obstacle_size)
        obstacles.append([obstacle_x, 0])

    # 更新障礙物位置
    new_obstacles = []
    for x, y in obstacles:
        y += obstacle_speed
        if y < HEIGHT:
            new_obstacles.append([x, y])
        # 碰撞偵測
        if (player_x < x + obstacle_size and
            player_x + player_size > x and
            player_y < y + obstacle_size and
            player_y + player_size > y):
            show_game_over()
            pygame.quit()
            sys.exit()
    obstacles = new_obstacles

    # 畫出角色和障礙物
    draw_player(player_x, player_y)
    score +=1
    draw_score()
    for x, y in obstacles:
        draw_obstacle(x, y)
        
    
    pygame.display.update()
    clock.tick(60)

pygame.quit()

#test in the final 
#test 2 