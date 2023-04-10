from pygame import *
from random import randint
import threading
import time as t

# клас-шаблон для створення спрайтів
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed,size_x,size_y):
        super().__init__()
        # для збереження зображення спрайту
        self.image = transform.scale(image.load(player_image),(size_x,size_y))
        self.speed = player_speed




        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y




    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))




# клас для головного персонажу
class Player(GameSprite):
    def move(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[K_UP] and self.rect.y > 0:
            self.rect.y -= self.speed
        if keys[K_RIGHT] and self.rect.x < width-60:
            self.rect.x += self.speed
        if keys[K_DOWN] and self.rect.y < height-60:
            self.rect.y += self.speed
   
    def fire(self):
        bullet = Bullet('bullet.png',self.rect.centerx, self.rect.top,10,15,20)
        bullets.add(bullet)



class Monster(GameSprite):
    #рух ворога
    def update(self):  
        global lost, a
        self.rect.y += self.speed
        if self.rect.y > height:
            self.rect.y = randint(-55, 0)
            self.rect.x = randint(20,width-160)
            lost += 1
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()


bullets = sprite.Group()






# розміри екрану
width = 800
height = 600
lost = 0
kd = 0
text_score = 0
bullet_count = 0
text_score = 0

#підключення шрифтів
font.init()
font1 = font.SysFont('Arial',36)
font2 = font.SysFont('Arial',56)
font3 = font.SysFont('Arial',46)


# pyinstaller --onefile <ім'я_файлу>.py



# Створення персонажів гри
player = Player('rocket.png',350,height-100,10,80,100)

monsters = sprite.Group()
for i in range(1,6):
    monster = Monster('enemy.png',randint(20,width-100),0,2,80,50)
    monsters.add(monster)







#Стоворення головного вікна
window = display.set_mode((width,height))
display.set_caption('Шутер')
background = transform.scale(image.load('galaxy.jpg'),(width,height))

reloads = 0
time_count = 0
b = False
a = 2
game = True
clock = time.Clock()
player_speed = 10
c = 30

lose1 = font2.render('Ти програв',1,(253, 23, 42))
def stats():
    gamestat = True
    while gamestat:
        for e in event.get():
            if e.type == QUIT:
                gamestat = False
        window.blit(background,(0,0))
        window.blit(stat,(300,60))
        window.blit(stat1,(150,140))
        window.blit(stat2,(150,180))
        window.blit(stat3,(150,220))
        window.blit(stat4,(150,260))
        window.blit(stat5,(150,300))
        window.blit(stat6,(150,340))
        display.update()
        clock.tick(60)


def display_text():
    global c, b, text_score, a, reloads
    while True:
        if c == 0 or b == True:
            t.sleep(1)
            c = 30
            b = False
            reloads += 1

text_thread = threading.Thread(target=display_text)
text_thread.daemon = True
text_thread.start()
t0 = t.time()
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if c > 0 and b == False:
                    player.fire()
                    c -= 1
                    bullet_count += 1
            if e.key == K_r:
                b = True

   
    window.blit(background,(0,0))
    text_lose = font1.render('Пропущено: '+str(lost),1,(255,255,255))
    window.blit(text_lose,(10,20))
    text_lose = font1.render('Рахунок: '+str(text_score),1,(255,255,255))
    window.blit(text_lose,(10,50))
    text_lose = font1.render('Пулі: '+str(c),1,(255,255,255))
    window.blit(text_lose,(10,80))

    # window.blit(lose1,(300,300))

    stat = font2.render('Статистика',1,(2, 173, 252))
    stat1 = font3.render(f'Вбито монстрів:{str(text_score)}.',1,(2, 173, 252))
    stat2 = font3.render(f'Випущено пуль:{str(bullet_count)}.',1,(2, 173, 252))
    stat3 = font3.render(f'Кількість перезарядок:{str(reloads)}.',1,(2, 173, 252))
    stat4 = font3.render(f'Швидкість мрнстрів:{str(a)}.',1,(2, 173, 252))

    player.reset()
    player.move()


    monsters.update()
    bullets.update()


    monsters.draw(window)


 
    bullets.draw(window)




    if sprite.groupcollide(monsters,bullets,True, True):
        if text_score >= 80:
            a = 4.5
            player.speed = 15
        elif text_score >= 65:
            a = 4
        elif text_score >= 50:
            a = 3.5
        elif text_score >= 45:
            a = 3.25
            player.speed = 13
        elif text_score >= 30:
            a = 3
        elif text_score >= 20:
            a = 2.5
        elif text_score >= 10:
            a = 2.25
        monster = Monster('enemy.png',randint(20,width-70),randint(-55, 0),a,80,50)
        monsters.add(monster)
        text_score += 1
    
    if lost >= 5:
        t1 = t.time()
        time_count = t1 - t0
        kd = round((text_score/time_count),1)
        time_count = round(time_count, 2)
        window.blit(lose1,(300,300))
        stat5 = font3.render(f'Швидкість вбивств:{str(kd)} м/с.',1,(2, 173, 252))
        stat6 = font3.render(f'Час гри:{str(time_count)} сек.',1,(2, 173, 252))
        i = 0
        while i <= 1:
            display.update()
            clock.tick(3)
            i = i + 1
        game = False
        stats()
    display.update()
    clock.tick(60)
