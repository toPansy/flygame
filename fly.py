import pygame
import random
import math
#初始化界面
pygame.init()
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption('打飞机')
icon = pygame.image.load('fly_dir/resource/ufo.png')
pygame.display.set_icon(icon) #设置左上图标
bgImg = pygame.image.load('fly_dir/resource/bg.png')
#添加音效
pygame.mixer.music.load('fly_dir/resource/bg.wav')
pygame.mixer.music.play(-1)

boom = pygame.mixer.Sound('fly_dir/resource/exp.wav')
bullets_sound = pygame.mixer.Sound('fly_dir/resource/laser.wav')
#分数
score = 0
#font = pygame.font.Font('freesansbold.ttf',32)
font = pygame.font.SysFont('simsunnsimsun', 32)
def show_score():
    text = f"分数：{score}"
    score_render = font.render(text, True, (0,255,0)) #字体渲染
    screen.blit(score_render, (10, 10))
#游戏结束
is_over = False
font2 = pygame.font.SysFont('simsunnsimsun', 64)
def check_is_over():
    if is_over:
        text2 = f"game over"
        text2_render = font2.render(text2, True, (250,0,0))
        screen.blit(text2_render,(250, 250))
#飞机
class Airport:
   def __init__(self):
        self.Img = pygame.image.load('fly_dir/resource/player.png')
        self.x = 400
        self.y = 500
        self.step = 0
   def move_player(self):
       self.x += self.step
       # 防止飞机出界
       if self.x > 736:
           self.x = 736
       if self.x < 0:
           self.x = 0
a = Airport()
#敌人
number_of_enemies = 6
class Enemy():
    def __init__(self):
        self.img = pygame.image.load('fly_dir/resource/enemy.png')
        self.x = random.randint(200, 600)
        self.y = random.randint(50, 250)
        self.step = random.randint(2, 6)
    def reset(self):
        self.x = random.randint(200, 600)
        self.y = random.randint(50, 250)
enemies = []
for i in range(number_of_enemies):
    enemies.append(Enemy())
#子彈
class Bullet():
    def __init__(self):
        self.img = pygame.image.load('fly_dir/resource/bullet.png')
        self.x = a.x + 16
        self.y = a.y + 10
        self.step = 10 #子弹速度
    def hit(self):
        global score
        for e in enemies:
            if(distance(self.x,self.y,e.x,e.y)<30):
                boom.play()
                bullets.remove(self)
                score += 1
                e.reset()
bullets = []

#enemyImg = pygame.image.load('fly_dir/resource/enemy.png')
#enemyX = random.randint(200,600)
#enemyY = random.randint(50,250)
#enemyStep = 4
#方法
def distance(bx,by,ex,ey):  #求两点距离
    a = ex - bx
    b = ey - by
    return math.sqrt(a*a + b*b)
def show_bullet():
    for b in bullets:
        screen.blit(b.img, (b.x, b.y))
        b.hit()
        b.y -= b.step #移动子弹
        if b.y < 0:    #到边界后移除子弹
            bullets.remove(b)
def show_enemy():
    #global enemyX, enemyY, enemyStep
    for e in enemies:
        screen.blit(e.img, (e.x, e.y))
    #enemyX += enemyStep
        e.x += e.step
        if(e.x > 736 or e.x < 0):
            e.step *= -1
            e.y += 40
            if e.y > 450:
                global is_over
                is_over = True
                enemies.clear()

def process_events():
    global running
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                 running = False
            # 飞机的按键控制
            if not is_over:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        a.step = 5
                    elif event.key == pygame.K_LEFT:
                        a.step = -5
                    elif event.key == pygame.K_SPACE:
                        bullets_sound.play()
                        bullets.append(Bullet())
                if event.type == pygame.KEYUP:
                    a.step = 0
#游戏主循环
running = True
while running:
    screen.blit(bgImg, (0, 0))
    show_score()
    process_events()
    screen.blit(a.Img, (a.x, a.y))
    show_enemy()
    show_bullet()
    a.move_player()
    check_is_over()
    pygame.display.update() #不停刷新