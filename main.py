# -*- coding: utf-8 -*-
import pygame
import random
import sys
from messages import love_messages
from function import *
# 初始化
pygame.init()


# global variable

# 畫面尺寸
WIDTH, HEIGHT = 500, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Love Sheep Game")
background = pygame.image.load("assets/background.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
# 顏色
WHITE = (255, 255, 255)
BLUE = (100, 150, 255)
RED = (255, 100, 100)

# 角色參數
player_size = 50
player_x = WIDTH // 2 - player_size // 2
player_y = HEIGHT - player_size - 10
player_speed = 5
HP = 1
HP_icon_size = 30
cooldown_time =1000
last_collistion_time = 0
HP_icon_list = []
HP_icon_speed = 2
# 障礙物參數
obstacle_size = 30
obstacle_speed = 5
obstacles = []

# 信件參數
letter_size = 40
letter_speed = 3
letters = []

current_message = ""
message_timer = 0

# 遊戲時鐘
clock = pygame.time.Clock()

# 字型
# font = pygame.font.SysFont(None, 32)
font = pygame.font.Font("Fonts/msjh.ttc", 24)#本文主角
player_img = pygame.image.load("assets/player.png")
player_img = pygame.transform.scale(player_img, (player_size, player_size))

lobster_img = pygame.image.load("assets/lobster_resize.png")

player_img_list = [player_img, lobster_img]

tako_image = pygame.image.load("assets/tako.png")
tako_image = pygame.transform.scale(tako_image, (obstacle_size, obstacle_size))

letter_image = pygame.image.load("assets/love_letter.png")

Drop_HP_icon = pygame.image.load("assets/heart_resize.png")
HP_icon = pygame.image.load("assets/heart_resize.png")
difficulty = "Normal"

def show_start_screen():
    """顯示遊戲初始畫面 + 難度選擇"""
    selected = 1  # 0: Easy, 1: Normal, 2: Hard
    global difficulty
    while True:
        screen.blit(background, (0, 0))
        title_font = pygame.font.Font("Fonts/msjh.ttc", 40)
        start_font = pygame.font.Font("Fonts/msjh.ttc", 28)
        
        title_text = title_font.render("Love Sheep Game", True, (255, 0, 100))
        title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
        screen.blit(title_text, title_rect)
        
        # 難度選項
        difficulties = ["Easy", "Normal", "Hard"]
        for i, text in enumerate(difficulties):
            color = (255, 0, 0) if i == selected else (0, 0, 0)
            option_text = start_font.render(text, True, color)
            option_rect = option_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + i * 40))
            screen.blit(option_text, option_rect)

        tip_text = start_font.render("使用 ↑↓ 選擇, Enter 開始", True, (50, 50, 50))
        tip_rect = tip_text.get_rect(center=(WIDTH // 2, HEIGHT - 50))
        screen.blit(tip_text, tip_rect)
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % 3
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % 3
                elif event.key == pygame.K_RETURN:
                    difficulty = difficulties[selected]
                    return  # 離開開始畫面
        
        clock.tick(30)


def choose_player():
    selected_character = 0

    
    while True:
        screen.blit(background, (0, 0))
        for i, text in enumerate(range(len(player_img_list))):
            x = WIDTH // 2 - 100 + i * 200
            y = HEIGHT // 2

            # 畫角色圖片
            screen.blit(player_img_list[i], (x, y))
            if i == selected_character:
                pygame.draw.rect(screen, (255, 0, 0), (x - 5, y - 5, player_img_list[i].get_width() + 10, player_img_list[i].get_height() + 10), 3)
        pygame.display.update()        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    selected_character = (selected_character - 1) % 2
                elif event.key == pygame.K_RIGHT:
                    selected_character = (selected_character + 1) % 2
                elif event.key == pygame.K_RETURN:
                    return selected_character

        clock.tick(30)
    
def draw_player(x, y, player_id):
    screen.blit(player_img_list[player_id], (x, y))

def draw_obstacle(x, y):
    screen.blit(tako_image, (x, y))

def draw_letter(x, y, text):

    screen.blit(letter_image, (x, y))

def draw_drop_HP_icon(x,y):
    screen.blit(Drop_HP_icon, (x, y))

def draw_HP_icon(HP):
    for i in range(HP):
        screen.blit(HP_icon, (WIDTH//2+i*50, 0))
    

def show_game_over():
    text = font.render("兩周年快樂寶寶!", True, (0, 0, 0))
    rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, rect)
    pygame.display.update()
    pygame.time.wait(2000)

def draw_score():
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

def draw_message():
    if current_message:
        message_text = font.render(current_message, True, (255, 0, 100))
        rect = message_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
        screen.blit(message_text, rect)


score = 0
running = True

show_start_screen()
player_id = choose_player()
# 主迴圈
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(background, (0,0))

    if difficulty == "Easy":
        obstacle_speed = 3
    elif difficulty == "Normal":
        obstacle_speed = 5
    elif difficulty == "Hard":
        obstacle_speed =7

    
    
    # 鍵盤控制
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < WIDTH - player_size:
        player_x += player_speed

    # 生出障礙物
    if random.random() < 0.02:
        obstacle_x = random.randint(0, WIDTH - obstacle_size)
        obstacles.append([obstacle_x, 0])

    # 生出信件
    if random.random() < 0.02:
        letter_x = random.randint(0, WIDTH - letter_size)
        text = random.choice(love_messages)
        letters.append([letter_x, 0, text])
    #生出HP icon 
    if random.random() < 0.01:
        HP_icon_x = random.randint(0, WIDTH - letter_size)
        HP_icon_list.append([HP_icon_x , 0])


    new_HP_icon_list = []
    for x, y in HP_icon_list:
        y += HP_icon_speed 
        if y < HEIGHT:
            new_HP_icon_list.append([x,y])
            if (player_x < x + HP_icon_size and
                player_x + player_size > x and
                player_y < y + HP_icon_size and
                player_y + player_size > y):
                current_time = pygame.time.get_ticks()
                if current_time - last_collistion_time > cooldown_time:
                    HP += 1
                    last_collistion_time = current_time
                continue  # 不再加入列表 (移除愛心)
                
    HP_icon_list = new_HP_icon_list    
    


    # 更新障礙物位置
    new_obstacles = []
    for x, y in obstacles:
        y += obstacle_speed
        if y < HEIGHT:
            new_obstacles.append([x, y])
        if (player_x < x + obstacle_size and
            player_x + player_size > x and
            player_y < y + obstacle_size and
            player_y + player_size > y):
            current_time = pygame.time.get_ticks()
            if current_time - last_collistion_time >cooldown_time:
                HP-=1
                last_collistion_time = current_time
                if (HP<=0):
                    show_game_over()
                    pygame.quit()
                    sys.exit()
    obstacles = new_obstacles

    # 更新信件位置
    new_letters = []
    for x, y, text in letters:
        y += letter_speed
        if y < HEIGHT:
            new_letters.append([x, y, text])
        if (player_x < x + letter_size and
            player_x + player_size > x and
            player_y < y + letter_size and
            player_y + player_size > y):
            current_message = text
            message_timer = pygame.time.get_ticks()
            score += 10  # 碰到信件加分
            
    letters = new_letters

    # 顯示訊息 2 秒後消失
    if current_message and pygame.time.get_ticks() - message_timer > 2000:
        current_message = ""

    # 畫出角色、障礙物、信件、血量
    
    draw_player(player_x, player_y, player_id)
    draw_HP_icon(HP)
    draw_score()
    draw_message()
    for x, y in obstacles:
        draw_obstacle(x, y)
    for x, y, text in letters:
        draw_letter(x, y, text)
    for x,y, in HP_icon_list:
        draw_drop_HP_icon(x,y)

    pygame.display.update()
    clock.tick(60)

pygame.quit()
