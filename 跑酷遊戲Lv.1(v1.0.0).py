import sys, pygame, time

from pygame import KEYDOWN


# 自訂錯誤
class YouDiedError(TypeError):pass
def die_error():raise YouDiedError("don't press \"R\" while in start screen!!")

# 初始化
pygame.init()
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("跑酷遊戲!!")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

# 顏色
WHITE, PURPLE, BLUE, BROWN = (255, 255, 255), (255, 0, 255), (0, 0, 255), (200, 100, 50)
GREEN, DARK_GREEN, GRAY = (0, 255, 0), (0, 100, 0), (150, 150, 150)
RED, RED_2, ORANGE, BLACK, YELLOW = (255, 0, 0), (215, 0, 0), (255, 100, 0), (0, 0, 0), (255, 255, 0)

# 地圖
LEVEL_WIDTH, LEVEL_HEIGHT, GROUND_Y = 10000, 7000, 300

# 玩家
player_size, player_speed, jump_speed, gravity = 40, 5, 15, 1
player_x, player_y, velocity_y, is_jumping = 6800, GROUND_Y - 0, 0, False
scroll_x, scroll_y = 0, 0

die_times = 0
die_on = True

timer = time.time()
time_on = True
tb = True

hint_on = True
hb = True
db = True

pass_finish = False

# 障礙物
obstacles = [
    pygame.Rect( 500, GROUND_Y -    0,   40,  40), pygame.Rect( 800, GROUND_Y -   40,  40,  80),
    pygame.Rect(1200, GROUND_Y -   20,   60,  60), pygame.Rect(1400, GROUND_Y -   70,  50, 110),
    pygame.Rect(1600, GROUND_Y -   20,   60,  60), pygame.Rect(1800, GROUND_Y -   80,  20, 120),
    pygame.Rect(2000, GROUND_Y -   70,   70,  10), pygame.Rect(2200, GROUND_Y -   70,  70,  10),
    pygame.Rect(2400, GROUND_Y -   80,   70,  10), pygame.Rect(2600, GROUND_Y -   80,  70,  10),
    pygame.Rect(2800, GROUND_Y -   90,   70,  10), pygame.Rect(3000, GROUND_Y -  100,  70,  10),
    pygame.Rect(3200, GROUND_Y -  120,   70,  10), pygame.Rect(3400, GROUND_Y -  150,  70,  10),
    pygame.Rect(3600, GROUND_Y -  180,   70,  10), pygame.Rect(3800, GROUND_Y -  200,  70,  10),
    pygame.Rect(4100, GROUND_Y -   80,   70,  10), pygame.Rect(4450, GROUND_Y -   40,  70,  10),
    pygame.Rect(4350, GROUND_Y -  120,   70,  10), pygame.Rect(4350, GROUND_Y -  140,  10,  25),
    pygame.Rect(4450, GROUND_Y -  180,   70,  10), pygame.Rect(4350, GROUND_Y -  240,  70,  10),
    pygame.Rect(4200, GROUND_Y -  250,   70,  10), pygame.Rect(4100, GROUND_Y -  280,  70,  10),
    pygame.Rect(3990, GROUND_Y -  340,   70,  10), pygame.Rect(3800, GROUND_Y -  380,  70,  10),
    pygame.Rect(3950, GROUND_Y -  470,   70,  10), pygame.Rect(4100, GROUND_Y -  470,  70,  10),
    pygame.Rect(4250, GROUND_Y -  470,   70,  10), pygame.Rect(4400, GROUND_Y -  470,  70,  10),
    pygame.Rect(4600, GROUND_Y -  365,   10,  10), pygame.Rect(4700, GROUND_Y -  365,  10,  10),
    pygame.Rect(4800, GROUND_Y -  365,   10,  10), pygame.Rect(4900, GROUND_Y -  365,  10,  10),
    pygame.Rect(5000, GROUND_Y -  365,   10,  10), pygame.Rect(4650, GROUND_Y -  200, 550,  40),
    pygame.Rect(5200, GROUND_Y -  400,   40, 240), pygame.Rect(4550, GROUND_Y -  310, 150,  10),
    pygame.Rect(4750, GROUND_Y -  310,   70,  10), pygame.Rect(4870, GROUND_Y -  310,  70,  10),
    pygame.Rect(4990, GROUND_Y -  310,   60,  10), pygame.Rect(5300, GROUND_Y -  150,  40, 130),
    pygame.Rect(5200, GROUND_Y -   50,   50,  10), pygame.Rect(5300, GROUND_Y -  150, 130,  10),
    pygame.Rect(5430, GROUND_Y -  270,   10, 130), pygame.Rect(5550, GROUND_Y -   30,  70,  10),
    pygame.Rect(5450, GROUND_Y -   80,   50,  10), pygame.Rect(5550, GROUND_Y -  130,  70,  10),
    pygame.Rect(5450, GROUND_Y -  170,   50,  10), pygame.Rect(5550, GROUND_Y -  300,  70,  10),
    pygame.Rect(5900, GROUND_Y -   50,   70,  10), pygame.Rect(6000, GROUND_Y -  100,  70,  10),
    pygame.Rect(6150, GROUND_Y -  150,   70,  10), pygame.Rect(6250, GROUND_Y -  200,  50,  10),
    pygame.Rect(6400, GROUND_Y -  250,   30,  10), pygame.Rect(6550, GROUND_Y -  310,  70,  10),
    pygame.Rect(6650, GROUND_Y - 1950,   70,  10), pygame.Rect(6500, GROUND_Y - 1600,  70,  10),
    pygame.Rect(6100, GROUND_Y - 1950,   70,  10), pygame.Rect(5900, GROUND_Y - 1950,  70,  10),
    pygame.Rect(5700, GROUND_Y - 1800,   50,  10), pygame.Rect(5500, GROUND_Y - 1850,  70,  10),
    pygame.Rect(4000, GROUND_Y - 1900, 1400,  10), pygame.Rect(3650, GROUND_Y - 1600,  70,  10),
    pygame.Rect(3450, GROUND_Y - 2500,   70,  10), pygame.Rect(3050, GROUND_Y - 1200,  80,  80),
    pygame.Rect(2900, GROUND_Y - 5700,   70,  10), pygame.Rect(6750, GROUND_Y - 10000, 50, 10040)
]

lava = [
    pygame.Rect(1900, GROUND_Y, 40, 40),
    pygame.Rect(680, GROUND_Y, 30, 40),
    pygame.Rect(2300, GROUND_Y, 2000, 40),
    pygame.Rect(4550, GROUND_Y - 450, 40, 490),
    pygame.Rect(4550, GROUND_Y - 350, 500, 40),
    pygame.Rect(5750, GROUND_Y - 260, 50, 300),
    pygame.Rect(5800, GROUND_Y - 10, 900, 50)
]

flow_lava = [
    {"rect": pygame.Rect(4700, GROUND_Y - 310, 50, 10), "speed": 1, "y_range": (210, 310)},
    {"rect": pygame.Rect(4820, GROUND_Y - 310, 50, 10), "speed": 1, "y_range": (210, 310)},
    {"rect": pygame.Rect(4940, GROUND_Y - 310, 50, 10), "speed": 1, "y_range": (210, 310)},
    {"rect": pygame.Rect(5360, GROUND_Y - 2500, 50, 10), "speed": 1, "y_range": (1900, 2130)},
    {"rect": pygame.Rect(5200, GROUND_Y - 2500, 50, 10), "speed": 1, "y_range": (1800, 2100)},
    {"rect": pygame.Rect(5080, GROUND_Y - 2500, 50, 10), "speed": 2, "y_range": (1890, 2110)},
    {"rect": pygame.Rect(4980, GROUND_Y - 2500, 50, 10), "speed": 1, "y_range": (1840, 2050)},
    {"rect": pygame.Rect(4890, GROUND_Y - 2500, 50, 10), "speed": 1, "y_range": (1850, 2110)},
    {"rect": pygame.Rect(4840, GROUND_Y - 2500, 50, 10), "speed": 1, "y_range": (1870, 2080)},
    {"rect": pygame.Rect(4750, GROUND_Y - 2500, 50, 10), "speed": 2, "y_range": (1860, 2210)},
    {"rect": pygame.Rect(4700, GROUND_Y - 2500, 50, 10), "speed": 1, "y_range": (1850, 2050)},
    {"rect": pygame.Rect(4620, GROUND_Y - 2500, 50, 10), "speed": 1, "y_range": (1870, 2110)},
    {"rect": pygame.Rect(4570, GROUND_Y - 2500, 50, 10), "speed": 1, "y_range": (1870, 2080)},
    {"rect": pygame.Rect(4490, GROUND_Y - 2500, 50, 10), "speed": 2, "y_range": (1810, 2210)},
]

# 紀錄點 & 技能
checkpoint_rects = [
    pygame.Rect(1500, GROUND_Y, 20, 40),
    pygame.Rect(4400, GROUND_Y, 20, 40),
    pygame.Rect(5200, GROUND_Y, 20, 40),
    pygame.Rect(6670, GROUND_Y - 1990, 20, 40),
    pygame.Rect(4300, GROUND_Y - 1940, 20, 40)
]
checkpoint_x, checkpoint_y = 100, GROUND_Y

# 敵人 list
enemies = [
    {"rect": pygame.Rect(1000, GROUND_Y + player_size - 30, 40, 30), "speed": 2, "direction": 1, "range": (950, 1150)},
    {"rect": pygame.Rect(4800, GROUND_Y + player_size - 30, 40, 30), "speed": 3, "direction": -1, "range": (4750, 5150)},
]

#門(需要鑰匙)
doors  = [
    {"rect": pygame.Rect(5300, GROUND_Y + player_size - 60, 39, 60), "is_open": False},
]
# 鑰匙
keys2 = [
    {"rect": pygame.Rect(5400, GROUND_Y + player_size - 220, 20, 20), "collected": False}
]

# 玩家是否持有鑰匙
has_key = False

portal_entrance = [
    pygame.Rect(6650, GROUND_Y - 310, 50, 50),
    pygame.Rect(2700, GROUND_Y - 5700, 50, 50)
]
portal_exit = [
    pygame.Rect(6650, GROUND_Y - 2200, 50, 50),
    pygame.Rect(7000, GROUND_Y - 50, 50, 50)
]

# 遊戲狀態
game_state, running, game_over, game_over_timer = "start screen", True, False, 0

def reset_player():
    global player_x, player_y, velocity_y, is_jumping
    player_x = checkpoint_x
    player_y = checkpoint_y
    velocity_y = 0
    is_jumping = False
    return pygame.Rect(player_x, player_y, player_size, player_size)
def close_game():
    pygame.quit()
    sys.exit()
def py_text(text, color, x, y):
    text_surface = font.render(text, True, color)
    return screen.blit(text_surface, (x, y))
# 全域變數
start_time = None
elapsed_time = 0

def py_timer(start=False):
    global start_time, elapsed_time

    if start and not pass_finish:
        if start_time is None:  # 第一次開始
            start_time = time.time()
        elapsed_time = time.time() - start_time
        return int(elapsed_time)  # 回傳秒數
    else:
        elapsed_time = elapsed_time
        return int(elapsed_time)
py_timer(False)
while running:
    screen.fill(WHITE)
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if game_state == "start screen":
        screen.fill(BLACK)
        py_timer(False)
        start_button = pygame.draw.rect(screen, WHITE, (220, 150, 150, 50))
        settings_button = pygame.draw.rect(screen,WHITE, (220, 250, 150, 50))
        start_text = py_text("start", BLACK, 265, 160)
        settings_text = py_text("settings", BLACK, 245, 260)
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if start_button.collidepoint(event.pos):
                    game_state = "start!"
                if settings_button.collidepoint(event.pos):
                    game_state = "settings"
        if keys[pygame.K_r]: die_error()

    elif game_state == "settings":
        screen.fill(BLACK)
        py_timer(False)
        hint_set_button = pygame.draw.rect(screen, WHITE, (220, 130, 150, 50))
        go_back_button = pygame.draw.rect(screen, WHITE, (220, 230, 150, 50))
        more_button = pygame.draw.rect(screen, WHITE, (220, 330, 150, 50))
        go_back_text = py_text("go back", BLACK, 250, 240)
        more_text = py_text("more settings", BLACK, 220, 340)
        if hb:
            hint_set_text = py_text("hint on", BLACK, 265, 140)
            hint_on = True
        else:
            hint_set_text = py_text("hint off", BLACK, 265, 140)
            hint_on = False
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if hint_set_button.collidepoint(event.pos):
                    hb = not hb
                if go_back_button.collidepoint(event.pos):
                    game_state = "start screen"
                if more_button.collidepoint(event.pos):
                    game_state = "more settings"

    elif game_state == "more settings":
        screen.fill(BLACK)
        py_timer(False)
        death_time_button = pygame.draw.rect(screen, WHITE, (190, 130, 200, 50))
        timer_button = pygame.draw.rect(screen, WHITE, (200, 230, 170, 50))
        back_button = pygame.draw.rect(screen, WHITE, (50, 300, 120, 50))
        py_text("back", BLACK, 70, 310)
        #這邊要改
        if db:
            death_time_text = py_text("death time on", BLACK, 210, 140)
            die_on = True
        else:
            death_time_text = py_text("death time off", BLACK, 210, 140)
            die_on = False
        if tb:
            timer_text = py_text("timer on", BLACK, 230, 240)
            time_on = True
        else:
            timer_text = py_text("timer off", BLACK, 230, 240)
            time_on = False
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if death_time_button.collidepoint(event.pos):
                    db = not db
                if timer_button.collidepoint(event.pos):
                    tb = not tb
                if back_button.collidepoint(event.pos):
                    game_state = "start screen"

    elif game_state == "start!":
        # now = time.time()  # 現在時間（秒，浮點數）
        # elapsed = now - timer  # 經過時間
        if not game_over and not pass_finish:
            timer = py_timer(True)
            # 玩家
            player_rect = pygame.Rect(player_x, player_y, player_size, player_size)

            # 更新紀錄點
            for cp in checkpoint_rects:
                if player_rect.colliderect(cp):
                    checkpoint_x = cp.x
                    checkpoint_y = cp.y - player_size  # 站在旗子上方
            # 移動
            dx = (keys[pygame.K_d] - keys[pygame.K_a]) * player_speed
            player_rect.x += dx
            for obstacle in obstacles:
                if player_rect.colliderect(obstacle):
                    player_rect.right = obstacle.left if dx > 0 else player_rect.right
                    player_rect.left = obstacle.right if dx < 0 else player_rect.left

            for event in events:
                if event.type == KEYDOWN:
                    if keys[pygame.K_p]:
                        game_state = "settings"

            # 跳躍 & 重力
            if keys[pygame.K_w] and not is_jumping:
                is_jumping, velocity_y = True, -jump_speed
            velocity_y += gravity
            player_rect.y += velocity_y
            for obstacle in obstacles:
                if player_rect.colliderect(obstacle):
                    if velocity_y > 0: player_rect.bottom, is_jumping, velocity_y = obstacle.top, False, 0
                    elif velocity_y < 0: player_rect.top, velocity_y = obstacle.bottom, 0
             # 開門
            for door in doors:
                if has_key and player_rect.colliderect(door["rect"]):
                    door["is_open"] = True  # 碰到門就打開
            for door in doors:
                if player_rect.colliderect(door["rect"]) and not door["is_open"]:
                    player_rect.right = door["rect"].left if dx > 0 else player_rect.right
                    player_rect.left = door["rect"].right if dx < 0 else player_rect.left
                elif player_rect.colliderect(door["rect"]) and door["is_open"]:
                    pass
            for door in doors:
                if player_rect.colliderect(door["rect"]) and not door["is_open"]:
                    if velocity_y > 0: player_rect.bottom, is_jumping, velocity_y = door["rect"].top, False, 0
                    elif velocity_y < 0: player_rect.top, velocity_y = door["rect"].bottom, 0
                elif player_rect.colliderect(door["rect"]) and door["is_open"]:
                    pass

            # 地板
            if player_rect.bottom >= GROUND_Y + player_size:
                player_rect.bottom, is_jumping, velocity_y = GROUND_Y + player_size, False, 0

            # 更新位置
            player_x, player_y = player_rect.x, player_rect.y
            scroll_x = min(max(player_x - WIDTH // 2, 0), LEVEL_WIDTH - WIDTH)
            scroll_y = max(-10000, min(player_y - HEIGHT // 2, LEVEL_HEIGHT - HEIGHT))

            # 更新敵人
            for enemy in enemies:
                rect = enemy["rect"]
                rect.x += enemy["speed"] * enemy["direction"]
                if rect.left < enemy["range"][0] or rect.right > enemy["range"][1]:
                    enemy["direction"] *= -1

            # 更新岩漿
            for lava_rect in flow_lava:
                lava_rect["rect"].y += lava_rect["speed"]
                if lava_rect["rect"].y > GROUND_Y - lava_rect["y_range"][0]:
                    lava_rect["rect"].y = GROUND_Y - lava_rect["y_range"][1]

            # 假設每個入口對應同索引的出口
            for i, pre in enumerate(portal_entrance):
                if player_rect.colliderect(pre):
                    player_rect.x = portal_exit[i].x
                    player_rect.y = portal_exit[i].y
                    player_x, player_y = player_rect.x, player_rect.y
                    velocity_y = 0  # 避免傳送後掉落
                    break  # 傳送一次就跳出


            # 撿鑰匙
            for key in keys2:
                if not key["collected"] and player_rect.colliderect(key["rect"]):
                    key["collected"] = True
                    has_key = True  # 玩家拿到鑰匙

            # 先把所有 lava rect 整理出來
            all_lava_rects = lava + [fl["rect"] for fl in flow_lava]

            # 死亡判定
            if any(player_rect.colliderect(enemy["rect"]) for enemy in enemies) or \
                    any(player_rect.colliderect(lr) for lr in all_lava_rects) or keys[pygame.K_r]:
                game_over, game_over_timer = True, pygame.time.get_ticks()
                die_times += 1


        # 繪製
        for i in range(0, LEVEL_WIDTH, 100):
            pygame.draw.rect(screen, GREEN, (i - scroll_x, GROUND_Y + player_size - scroll_y, 80, 20))
        [pygame.draw.rect(screen, ORANGE, (o.x - scroll_x, o.y - scroll_y, o.w, o.h)) for o in obstacles]
        [pygame.draw.rect(screen, RED, (lv.x - scroll_x, lv.y - scroll_y, lv.w, lv.h)) for lv in lava]
        [pygame.draw.rect(screen, RED_2, (lv["rect"].x - scroll_x, lv["rect"].y - scroll_y, lv["rect"].w, lv["rect"].h)) for lv in flow_lava]
        [pygame.draw.rect(screen, YELLOW, (cp.x - scroll_x, cp.y - scroll_y, cp.w, cp.h)) for cp in checkpoint_rects]
        [pygame.draw.rect(screen, DARK_GREEN, (pr.x - scroll_x, pr.y - scroll_y, pr.w, pr.h)) for pr in portal_entrance]
        [pygame.draw.rect(screen, DARK_GREEN, (prx.x - scroll_x, prx.y - scroll_y, prx.w, prx.h)) for prx in portal_exit]
        for enemy in enemies:
            pygame.draw.rect(screen, BLACK, (enemy["rect"].x - scroll_x, enemy["rect"].y - scroll_y, enemy["rect"].w, enemy["rect"].h))
        for door in doors:
            if door["is_open"]:
                door_color = GRAY
                has_key = False
            else:
                door_color = BROWN
            pygame.draw.rect(screen, door_color, (door["rect"].x - scroll_x, door["rect"].y - scroll_y, door["rect"].w, door["rect"].h))
        for key in keys2:
            if not key["collected"]:
                pygame.draw.rect(screen,(255, 0, 150),(key["rect"].x - scroll_x, key["rect"].y - scroll_y, key["rect"].w, key["rect"].h))
        pygame.draw.rect(screen, BLUE, (player_x - scroll_x, player_y - scroll_y, player_size, player_size))

        if time_on:
            py_text(f"time:{int(timer)}", BLACK, 400, 20)

        # if player_x > 7200:
        #     game_state = "finish!"
    elif game_state == "finish!":
        pass_finish = True
        if player_x > 6800:
            py_text("finish!", BLACK, 7200 - scroll_x, 120 - scroll_y)
            py_text("wow you pass this parcort!! remember to play Lv.2!!", BLACK, 7200 - scroll_x, GROUND_Y - 150 - scroll_y)


    # 提示文字
    if hint_on:
        if 1400 < player_x < 1550:
            py_text("this is the check point!", BLACK, 1400 - scroll_x, 80 - scroll_y)
            py_text("touch it to set you check point", BLACK, 1380 - scroll_x, 130 - scroll_y)

        if 3750 < player_x < 3980 and -45 < player_y < 90:
            py_text("if you did\'nt jump on the platform,", BLACK, 3700 - scroll_x, 120 - scroll_y)
            py_text("you can jump in the air 1 time!", BLACK, 3700 - scroll_x, 140 - scroll_y)

        if 5150 < player_x < 5450:
            py_text("this is the key!", BLACK, 5400 - scroll_x, 140 - scroll_y)
            py_text("use the key to open the brown door!", BLACK, 5270 - scroll_x, 160 - scroll_y)

        if 6600 < player_x < 6700:
            py_text("go left!  <-", BLACK, 6650 - scroll_x, -1800 - scroll_y)
        if 6350 < player_x < 6600:
            py_text("trust your self!", BLACK, 6400 - scroll_x, -1400 - scroll_y)
        if 6050 < player_x < 6150:
            py_text("you did it!!!", BLACK, 6120 - scroll_x, -1700 - scroll_y)
        if 4200 < player_x < 4400:
            py_text("congratulations!!! you did it!!", BLACK, 4250 - scroll_x, -1700 - scroll_y)

    py_text(f"your X:{player_x}    your Y:{-player_y + GROUND_Y}", BLACK, 50, 0)
    if die_on:
        py_text(f"times of death:{die_times}", BLACK, 400, 0)
    py_text(game_state, BLACK, 200, 100)

    #跳躍加強
    if 6200 < player_x < 6550 and -1300 > player_y > -1690:
        jump_speed = 30
        player_speed = 20
    elif 3550 < player_x < 3700 and -1650 < player_y < - 1300:
        jump_speed = 49
    elif 2900 < player_x < 3200 and -2000 < player_y < -900:
        jump_speed = 99
    else:
        jump_speed = 15
        player_speed = 5
    # 遊戲結束畫面
    if game_over:
        py_timer(False)
        # --- 先把當前畫面存成 Surface ---
        snapshot = screen.copy()

        # --- 簡單模糊：縮小再放大 ---
        small = pygame.transform.smoothscale(snapshot, (WIDTH // 10, HEIGHT // 10))  # 縮小
        blurred = pygame.transform.smoothscale(small, (WIDTH, HEIGHT))  # 放大
        screen.blit(blurred, (0, 0))  # 畫回畫面

        # --- 半透明黑色遮罩 ---
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(150)  # 透明度 (越大越暗)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        py_text("Game Over!", RED, WIDTH // 2 - 100, HEIGHT // 2 - 20)

        # Restart 按鈕
        restart_button = pygame.Rect(180, 250, 200, 60)
        pygame.draw.rect(screen, BLUE, restart_button, border_radius=15)
        py_text("Restart", WHITE, restart_button.x + 60, restart_button.y + 15)

        # Close 按鈕
        close_button = pygame.Rect(180, 330, 200, 60)
        pygame.draw.rect(screen, RED, close_button, border_radius=15)
        py_text("Close", WHITE, close_button.x + 60, close_button.y + 15)

        # 用剛剛已經讀到的 events 來檢查
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if restart_button.collidepoint(event.pos):
                    player_x, player_y = checkpoint_x, checkpoint_y
                    velocity_y = 0
                    is_jumping = False
                    game_over = False
                if close_button.collidepoint(event.pos):
                    close_game()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                player_x, player_y = checkpoint_x, checkpoint_y
                velocity_y = 0
                is_jumping = False
                game_over = False
            if keys[pygame.K_c]:
                close_game()

    pygame.display.flip()
    clock.tick(70)

close_game()