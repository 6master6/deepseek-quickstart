#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
import random
import os
import sys
from pygame import gfxdraw

# 初始化pygame
pygame.init()
pygame.display.set_caption('贪吃蛇游戏 - 设置版')

# 颜色定义
COLORS = {
    'white': (255, 255, 255),
    'black': (0, 0, 0),
    'red': (213, 50, 80),
    'green': (0, 255, 0),
    'blue': (50, 153, 213),
    'gray': (200, 200, 200),
    'dark_green': (0, 180, 0),
    'light_blue': (173, 216, 230),
    'dark_blue': (0, 0, 139)
}

# 游戏设置类
class GameSettings:
    def __init__(self):
        self.difficulty = "medium"  # 默认中等难度
        self.bg_color = COLORS['white']  # 默认白色背景
        self.show_grid = False  # 默认不显示网格
        self.snake_speed = 12  # 默认速度
        self.snake_block = 20  # 蛇身大小

    def set_difficulty(self, level):
        if level == "easy":
            self.snake_speed = 10
        elif level == "medium":
            self.snake_speed = 15
        elif level == "hard":
            self.snake_speed = 20
        self.difficulty = level

    def set_bg_color(self, color_name):
        self.bg_color = COLORS.get(color_name, COLORS['white'])

# 初始化游戏窗口
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
settings = GameSettings()

# 字体初始化
def init_fonts():
    font_paths = [
        "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/truetype/arphic/uming.ttc"
    ]
    
    for path in font_paths:
        if os.path.exists(path):
            try:
                font_normal = pygame.font.Font(path, 24)
                font_large = pygame.font.Font(path, 36)
                return font_normal, font_large
            except:
                continue
    
    return pygame.font.SysFont(None, 24), pygame.font.SysFont(None, 36)

font_normal, font_large = init_fonts()

# 绘制带阴影的文字
def draw_text(surface, text, size, x, y, color=COLORS['black'], shadow=True):
    if shadow:
        text_surface = font_large.render(text, True, COLORS['gray'])
        surface.blit(text_surface, (x+2, y+2))
    text_surface = font_large.render(text, True, color)
    surface.blit(text_surface, (x, y))

# 设置界面
def show_settings():
    setting_active = True
    color_options = ["white", "light_blue", "black"]
    
    while setting_active:
        screen.fill(COLORS['white'])
        
        draw_text(screen, "游戏设置", 36, WIDTH//2 - 70, 30, COLORS['dark_blue'])
        
        # 显示当前设置
        draw_text(screen, f"当前难度: {settings.difficulty}", 24, 50, 100)
        draw_text(screen, f"当前背景: {settings.bg_color}", 24, 50, 150)
        draw_text(screen, f"显示网格: {'是' if settings.show_grid else '否'}", 24, 50, 200)
        
        # 绘制按钮
        pygame.draw.rect(screen, COLORS['green'], (50, 300, 200, 50))
        draw_text(screen, "简单难度", 22, 70, 310)
        
        pygame.draw.rect(screen, COLORS['blue'], (300, 300, 200, 50))
        draw_text(screen, "中等难度", 22, 320, 310)
        
        pygame.draw.rect(screen, COLORS['red'], (550, 300, 200, 50))
        draw_text(screen, "困难难度", 22, 580, 310)
        
        # 背景颜色选择
        for i, color in enumerate(color_options):
            pygame.draw.rect(screen, COLORS[color], (50 + i*250, 400, 200, 50))
            draw_text(screen, f"{color}背景", 22, 70 + i*250, 410)
        
        # 网格开关
        grid_text = "隐藏网格" if settings.show_grid else "显示网格"
        pygame.draw.rect(screen, COLORS['gray'], (300, 500, 200, 50))
        draw_text(screen, grid_text, 22, 330, 510)
        
        # 开始游戏按钮
        pygame.draw.rect(screen, COLORS['dark_green'], (550, 500, 200, 50))
        draw_text(screen, "开始游戏", 22, 590, 510)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                
                # 难度选择
                if 50 <= x <= 250 and 300 <= y <= 350:
                    settings.set_difficulty("easy")
                elif 300 <= x <= 500 and 300 <= y <= 350:
                    settings.set_difficulty("medium")
                elif 550 <= x <= 750 and 300 <= y <= 350:
                    settings.set_difficulty("hard")
                
                # 背景颜色选择
                for i, color in enumerate(color_options):
                    if 50 + i*250 <= x <= 250 + i*250 and 400 <= y <= 450:
                        settings.set_bg_color(color)
                
                # 网格开关
                if 300 <= x <= 500 and 500 <= y <= 550:
                    settings.show_grid = not settings.show_grid
                
                # 开始游戏
                if 550 <= x <= 750 and 500 <= y <= 550:
                    setting_active = False

# 绘制网格
def draw_grid():
    for x in range(0, WIDTH, settings.snake_block):
        pygame.draw.line(screen, COLORS['gray'], (x, 0), (x, HEIGHT), 1)
    for y in range(0, HEIGHT, settings.snake_block):
        pygame.draw.line(screen, COLORS['gray'], (0, y), (WIDTH, y), 1)

# 游戏主函数
def game_loop():
    game_over = False
    game_pause = False
    
    # 蛇的初始位置
    x, y = WIDTH // 2, HEIGHT // 2
    x_change, y_change = 0, 0
    snake = []
    snake_length = 1
    
    # 食物位置
    foodx = round(random.randrange(0, WIDTH - settings.snake_block) / settings.snake_block) * settings.snake_block
    foody = round(random.randrange(0, HEIGHT - settings.snake_block) / settings.snake_block) * settings.snake_block
    
    clock = pygame.time.Clock()
    
    while not game_over:
        # 游戏结束画面
        while game_pause:
            screen.fill(settings.bg_color)
            draw_text(screen, "游戏结束! 得分: {}".format(snake_length-1), 36, WIDTH//2 - 150, HEIGHT//2 - 100, COLORS['red'])
            draw_text(screen, "按Q退出 或R重新开始", 24, WIDTH//2 - 120, HEIGHT//2)
            
            pygame.display.update()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                    game_pause = False
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_pause = False
                    if event.key == pygame.K_r:
                        game_loop()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x_change == 0:
                    x_change = -settings.snake_block
                    y_change = 0
                elif event.key == pygame.K_RIGHT and x_change == 0:
                    x_change = settings.snake_block
                    y_change = 0
                elif event.key == pygame.K_UP and y_change == 0:
                    x_change = 0
                    y_change = -settings.snake_block
                elif event.key == pygame.K_DOWN and y_change == 0:
                    x_change = 0
                    y_change = settings.snake_block
                elif event.key == pygame.K_p:  # 暂停游戏
                    game_pause = True
        
        # 边界检测
        if x >= WIDTH or x < 0 or y >= HEIGHT or y < 0:
            game_pause = True
        
        x += x_change
        y += y_change
        
        # 绘制游戏
        screen.fill(settings.bg_color)
        
        if settings.show_grid:
            draw_grid()
        
        # 绘制食物
        pygame.draw.rect(screen, COLORS['red'], [foodx, foody, settings.snake_block, settings.snake_block])
        
        # 更新蛇
        snake_head = [x, y]
        snake.append(snake_head)
        if len(snake) > snake_length:
            del snake[0]
        
        # 检测碰撞自身
        for block in snake[:-1]:
            if block == snake_head:
                game_pause = True
        
        # 绘制蛇
        for i, block in enumerate(snake):
            color = COLORS['dark_green'] if i == len(snake)-1 else COLORS['green']
            pygame.draw.rect(screen, color, [block[0], block[1], settings.snake_block, settings.snake_block])
            pygame.draw.rect(screen, COLORS['black'], [block[0], block[1], settings.snake_block, settings.snake_block], 1)
        
        # 显示分数
        draw_text(screen, f"得分: {snake_length-1}", 24, 20, 20, COLORS['black'])
        draw_text(screen, f"难度: {settings.difficulty}", 24, 20, 50, COLORS['black'])
        
        pygame.display.update()
        
        # 检测是否吃到食物
        if x == foodx and y == foody:
            foodx = round(random.randrange(0, WIDTH - settings.snake_block) / settings.snake_block) * settings.snake_block
            foody = round(random.randrange(0, HEIGHT - settings.snake_block) / settings.snake_block) * settings.snake_block
            snake_length += 1
        
        clock.tick(settings.snake_speed)

# 主程序
def main():
    show_settings()  # 显示设置界面
    game_loop()      # 开始游戏
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()