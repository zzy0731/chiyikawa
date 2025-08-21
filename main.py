# -*- coding: utf-8 -*-
import pygame
import random
import sys
from messages import love_messages
from function import *

# 初始化
pygame.init()
pygame.mixer.init()

# 畫面尺寸
WIDTH, HEIGHT = 500, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Love Sheep Game")

# 背景
background = pygame.image.load("assets/background.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# 顏色
WHITE = (255, 255, 255)
BLUE = (100, 150, 255)
RED = (255, 100, 100)

# 共用參數
player_size = 50
player_speed = 5

HP_icon_size = 30
HP_icon_speed = 2
HP_MAX = 5

cooldown_time = 1000  # 毫秒

obstacle_size = 30
letter_size = 30
letter_speed = 3

difficulty = "Normal"  # 預設難度

# 遊戲時鐘
clock = pygame.time.Clock()

# 字型（依你的環境調整字型路徑）
ui_font_path = "Fonts/msjh.ttc"
game_font_path = "Fonts/ChenYuluoyan_v1.ttf"
font = pygame.font.Font(game_font_path, 24)

# 玩家與素材圖片
player_img = pygame.image.load("assets/player.png")
player_img = pygame.transform.scale(player_img, (player_size, player_size))
lobster_img = pygame.image.load("assets/lobster_resize.png")
dog_img = pygame.image.load("assets/dog_resize.png")
youshi_img = pygame.image.load("assets/youshi_resize.png")
pokemon_img = pygame.image.load("assets/mouse_resize.png")
player_img_list = [player_img, lobster_img, dog_img, youshi_img, pokemon_img]

tako_image = pygame.image.load("assets/tako.png")
tako_image = pygame.transform.scale(tako_image, (obstacle_size, obstacle_size))
ice_cream_image = pygame.image.load("assets/ice_cream.png")
ice_cream_image = pygame.transform.scale(ice_cream_image, (obstacle_size, obstacle_size))
meat_image = pygame.image.load("assets/meat.png")
meat_image = pygame.transform.scale(meat_image, (obstacle_size, obstacle_size))
obstacle_list = [tako_image, ice_cream_image, meat_image]

letter_image = pygame.image.load("assets/love_letter.png")  # 可視需要再 scale
Drop_HP_icon = pygame.image.load("assets/heart_resize.png")
HP_icon = pygame.image.load("assets/heart_resize.png")

# 音效
hit_sound = pygame.mixer.Sound("music/hurt2.mp3")
hit_sound.set_volume(0.5)
get_HP_sound = pygame.mixer.Sound("music/oola.mp3")
get_HP_sound.set_volume(0.5)
get_letter_sound = pygame.mixer.Sound("music/oola_happy.mp3")
get_letter_sound.set_volume(0.5)

# 會在一局內變動的狀態（透過 reset_game_state() 初始化）
player_x = WIDTH // 2 - player_size // 2
player_y = HEIGHT - player_size - 10
HP = 1
score = 0
obstacles = []
letters = []
HP_icon_list = []
current_message = ""
message_timer = 0
last_collistion_time = 0
text_idx = 0
obstacle_id = 0  # 用於輪流切換障礙物造型


# ------------------ UI 畫面 ------------------

def show_start_screen():
    """顯示遊戲初始畫面 + 難度選擇"""
    selected = 1  # 0: Easy, 1: Normal, 2: Hard
    global difficulty
    while True:
        screen.blit(background, (0, 0))
        title_font = pygame.font.Font(game_font_path, 25)
        system_font = pygame.font.Font(game_font_path, 20)

        title_text = title_font.render("Love Sheep Game", True, (255, 0, 100))
        title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
        screen.blit(title_text, title_rect)

        # 難度選項
        difficulties = ["Easy", "Normal", "Hard"]
        for i, text in enumerate(difficulties):
            color = (255, 0, 0) if i == selected else (0, 0, 0)
            option_text = title_font.render(text, True, color)
            option_rect = option_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + i * 40))
            screen.blit(option_text, option_rect)

        tip_text = system_font.render(
            "左右閃躲，避開障礙物的同時想辦法獲得最多手寫信",
            True, (0, 0, 0)
        )
        tip_rect = tip_text.get_rect(center=(WIDTH // 2, HEIGHT - 400))
        screen.blit(tip_text, tip_rect)

        tip_text2 = system_font.render(
            "吃愛心增加活下去的機率!",
            True, (0, 0, 0)
        )
        tip_rect2 = tip_text2.get_rect(center=(WIDTH // 2, HEIGHT - 380))
        screen.blit(tip_text2, tip_rect2)
        
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
    """角色選擇畫面"""
    selected_character = 0
    n = len(player_img_list)
    while True:
        screen.blit(background, (0, 0))
        for i in range(n):
            x = WIDTH // 2 - 200 + i * 100
            y = HEIGHT // 2
            screen.blit(player_img_list[i], (x, y))
            if i == selected_character:
                pygame.draw.rect(
                    screen, (255, 0, 0),
                    (x - 5, y - 5, player_img_list[i].get_width() + 10,
                     player_img_list[i].get_height() + 10), 3
                )
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    selected_character = (selected_character - 1) % n
                elif event.key == pygame.K_RIGHT:
                    selected_character = (selected_character + 1) % n
                elif event.key == pygame.K_RETURN:
                    return selected_character

        clock.tick(30)


def show_game_over():
    """死亡時顯示 2 秒祝福畫面"""
    text = font.render("兩周年快樂寶寶!", True, (0, 0, 0))
    rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, rect)
    pygame.display.update()
    pygame.time.wait(2000)


# ------------------ 畫圖工具 ------------------

def draw_player(x, y, player_id):
    screen.blit(player_img_list[player_id], (x, y))


def draw_obstacle(x, y, cur_obstacle_id):
    obstacle_image = obstacle_list[cur_obstacle_id]
    screen.blit(obstacle_image, (x, y))


def draw_letter(x, y):
    screen.blit(letter_image, (x, y))


def draw_drop_HP_icon(x, y):
    screen.blit(Drop_HP_icon, (x, y))


def draw_HP_icon(cur_HP):
    for i in range(cur_HP):
        screen.blit(HP_icon, (10 + i * (HP_icon_size + 6), 10))


def draw_score():
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (WIDTH - 200, 10))


def draw_message():
    if current_message:
        message_text = font.render(current_message, True, (0, 0, 0))
        rect = message_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
        screen.blit(message_text, rect)


# ------------------ 遊戲狀態控制 ------------------

def select_cur_text(love_messages_list, idx):
    """安全循環取用情書內容"""
    if not love_messages_list:
        return ""
    return love_messages_list[idx % len(love_messages_list)]


def reset_game_state():
    """重置單局狀態"""
    global player_x, player_y, HP, score, obstacles, letters, HP_icon_list
    global last_collistion_time, current_message, message_timer, text_idx, obstacle_id

    player_x = WIDTH // 2 - player_size // 2
    player_y = HEIGHT - player_size - 10
    HP = 1
    score = 0
    obstacles = []
    letters = []
    HP_icon_list = []
    last_collistion_time = 0
    current_message = ""
    message_timer = 0
    text_idx = 0
    obstacle_id = 0


def play_one_game(player_id):
    """執行一局；死亡時 return 回到初始畫面"""
    global HP, last_collistion_time, score, current_message, message_timer
    global obstacles, letters, HP_icon_list, obstacle_id, player_x, player_y, text_idx

    running = True
    while running:
        # 事件處理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.blit(background, (0, 0))

        # 難度調速
        if difficulty == "Easy":
            obstacle_speed_local = 3
            obstacle_opptunity = obstacle_opptunity = 0.02
        elif difficulty == "Normal":
            obstacle_opptunity = 0.05
            obstacle_speed_local = 5
        else:
            obstacle_opptunity = 0.1
            obstacle_speed_local = 7

        # 鍵盤控制
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < WIDTH - player_size:
            player_x += player_speed

        # 生出障礙物
        if random.random() < obstacle_opptunity:
            obstacle_id = (obstacle_id + 1) % len(obstacle_list)
            obstacle_x = random.randint(0, WIDTH - obstacle_size)
            obstacles.append([obstacle_x, 0, obstacle_id])

        # 生出信件
        if random.random() < 0.01:
            letter_x = random.randint(0, WIDTH - letter_size)
            text = select_cur_text(love_messages, text_idx)
            letters.append([letter_x, 0, text])

        # 生出 HP icon
        if random.random() < 0.01:
            HP_icon_x = random.randint(0, WIDTH - letter_size)
            HP_icon_list.append([HP_icon_x, 0])

        # 更新 HP icon
        new_HP_icon_list = []
        for x, y in HP_icon_list:
            y += HP_icon_speed
            if y < HEIGHT:
                # 撞到回復血量
                if (player_x < x + HP_icon_size and
                    player_x + player_size > x and
                    player_y < y + HP_icon_size and
                    player_y + player_size > y):
                    current_time = pygame.time.get_ticks()
                    if current_time - last_collistion_time > cooldown_time:
                        get_HP_sound.play()
                        HP = min(HP_MAX, HP + 1)  # 上限 5
                        last_collistion_time = current_time
                    # 撿到就不加回列表
                    continue
                new_HP_icon_list.append([x, y])
        HP_icon_list = new_HP_icon_list

        # 更新障礙物
        new_obstacles = []
        for x, y, oid in obstacles:
            y += obstacle_speed_local
            if y < HEIGHT:
                new_obstacles.append([x, y, oid])

            # 撞到扣血
            if (player_x < x + obstacle_size and
                player_x + player_size > x and
                player_y < y + obstacle_size and
                player_y + player_size > y):
                current_time = pygame.time.get_ticks()
                if current_time - last_collistion_time > cooldown_time:
                    hit_sound.play()
                    HP -= 1
                    last_collistion_time = current_time
                    if HP <= 0:
                        show_game_over()
                        return  # 結束本局，回初始畫面
        obstacles = new_obstacles

        # 更新信件
        new_letters = []
        for x, y, text in letters:
            y += letter_speed
            if y < HEIGHT:
                # 撿到加分 + 顯示訊息 + 音效
                if (player_x < x + letter_size and
                    player_x + player_size > x and
                    player_y < y + letter_size and
                    player_y + player_size > y):
                    current_message = text
                    message_timer = pygame.time.get_ticks()
                    score += 10
                    get_letter_sound.play()
                else:
                    new_letters.append([x, y, text])
        letters = new_letters

        # 顯示訊息 2 秒後消失（保留你的行為：結束時播一次 get_HP_sound）
        if current_message and pygame.time.get_ticks() - message_timer > 2000:
            text_idx += 1
            current_message = ""

        # 繪製
        draw_player(player_x, player_y, player_id)
        draw_HP_icon(HP)
        draw_score()
        draw_message()
        for x, y, cur_obstacle_id in obstacles:
            draw_obstacle(x, y, cur_obstacle_id)
        for x, y, text in letters:
            draw_letter(x, y)
        for x, y in HP_icon_list:
            draw_drop_HP_icon(x, y)

        pygame.display.update()
        clock.tick(60)


# ------------------ 遊戲主流程（外層：死掉就回來再玩一局） ------------------

while True:
    show_start_screen()
    player_id = choose_player()

    # 每局開始設定背景音樂
    pygame.mixer.music.load("music/chiikawa_music.mp3")
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)

    # 重置單局狀態
    reset_game_state()

    # 開始一局；死亡會 return 回到這裡，重新顯示開始畫面
    play_one_game(player_id)
