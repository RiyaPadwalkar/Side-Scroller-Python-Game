import pygame
from pygame.locals import *
import os
import random



pygame.init()



W, H = 800, 437
win = pygame.display.set_mode((W,H))
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption('Side Scroller')


# Clock and font
clock = pygame.time.Clock()
font = pygame.font.SysFont("comicsans", 72)  # You can change font

def countdown_timer(screen, font, clock):
    countdown_values = ["3", "2", "1", "Game Begins!"]
    for count in countdown_values:
        screen.fill((0, 0, 0))  # Clear screen with black
        text_surface = font.render(count, True, (255, 255, 255))  # White text
        text_rect = text_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        screen.blit(text_surface, text_rect)
        pygame.display.update()
        pygame.time.delay(1000)  # Wait 1 second
        clock.tick(60)

backgrounds = [
    pygame.image.load(os.path.join('images', 'night.png')).convert(),
    pygame.image.load(os.path.join('images', 'factory.png')).convert(),
    pygame.image.load(os.path.join('images', 'snow.png')).convert()
]

current_bg_index = 0
bg = backgrounds[current_bg_index]
bgX = 0
bgX2 = bg.get_width()

clock = pygame.time.Clock()

class player(object):
    run = [pygame.image.load(os.path.join('images', str(x) + '.png')) for x in range(8, 16)]
    jump = [pygame.image.load(os.path.join('images', str(x) + '.png')) for x in range(1, 8)]
    slide = [pygame.image.load(os.path.join('images', 'S1.png')), pygame.image.load(os.path.join('images', 'S2.png')), pygame.image.load(os.path.join('images', 'S2.png')), pygame.image.load(os.path.join('images', 'S2.png')), pygame.image.load(os.path.join('images', 'S2.png')),pygame.image.load(os.path.join('images', 'S2.png')), pygame.image.load(os.path.join('images', 'S2.png')), pygame.image.load(os.path.join('images', 'S2.png')), pygame.image.load(os.path.join('images', 'S3.png')), pygame.image.load(os.path.join('images', 'S4.png')), pygame.image.load(os.path.join('images', 'S5.png'))]
    fall = pygame.image.load(os.path.join('images', '0.png'))
    jumpList = [1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,3,3,3,4,4,4,4,4,4,4,4,4,4,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-1,-1,-1,-1,-1,-1,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4]

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.jumping = False
        self.sliding = False
        self.falling = False
        self.slideCount = 0
        self.jumpCount = 0
        self.runCount = 0
        self.slideUp = False

    def draw(self, win):
        if self.falling:
            win.blit(self.fall, (self.x, self.y + 30))
        elif self.jumping:
            self.y -= self.jumpList[self.jumpCount] * 1.3
            win.blit(self.jump[self.jumpCount//18], (self.x, self.y))
            self.jumpCount += 1
            if self.jumpCount > 108:
                self.jumpCount = 0
                self.jumping = False
                self.runCount = 0
            self.hitbox = (self.x+ 4, self.y, self.width-24, self.height-10)
        elif self.sliding or self.slideUp:
            if self.slideCount < 20:
                self.y += 1
                self.hitbox = (self.x+ 4, self.y, self.width-24, self.height-10)
            elif self.slideCount == 80:
                self.y -= 19
                self.sliding = False
                self.slideUp = True
            elif self.slideCount > 20 and self.slideCount < 80:
                self.hitbox = (self.x, self.y+3, self.width-8, self.height-35)

            if self.slideCount >= 110:
                self.slideCount = 0
                self.runCount = 0
                self.slideUp = False
                self.hitbox = (self.x+ 4, self.y, self.width-24, self.height-10)
            win.blit(self.slide[self.slideCount//10], (self.x, self.y))
            self.slideCount += 1

        else:
            if self.runCount > 42:
                self.runCount = 0
            win.blit(self.run[self.runCount//6], (self.x,self.y))
            self.runCount += 1
            self.hitbox = (self.x+ 4, self.y, self.width-24, self.height-13)
 
    def reset(self):
       self.jumping = False
       self.sliding = False
       self.falling = False
       self.jumpCount = 0
       self.slideCount = 0
       self.runCount = 0
       self.y = 313  # reset to ground level
       global energy_boost_collected, energy_boost_used
       energy_boost_collected = False
       energy_boost_used = False

        #pygame.draw.rect(win, (255,0,0),self.hitbox, 2)



class coin(object):
    imgs = [pygame.image.load(os.path.join('images', 'coin1.png')),
            pygame.image.load(os.path.join('images', 'coin2.png')),
            pygame.image.load(os.path.join('images', 'coin3.png'))]

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 32
        self.height = 32
        self.count = 0
        self.visible = True



    def draw(self, win):

    

        if self.visible:
            win.blit(pygame.transform.scale(self.imgs[self.count // 5], (32, 32)), (self.x, self.y))
            self.count += 1
            if self.count >= 15:
                self.count = 0

    def collide(self, rect):
        if self.visible:
            coin_rect = pygame.Rect(self.x, self.y, self.width, self.height)
            player_rect = pygame.Rect(rect[0], rect[1], rect[2], rect[3])
            if coin_rect.colliderect(player_rect):
                self.visible = False
                return True
        return False
    

  
    def collides_with_obstacle(self, obstacles):
       for obstacle in obstacles:
         # 100 pixel safe zone horizontally
         if abs(self.x - obstacle.x) < 100:
            # Also check vertical overlap (even better)
             if self.y + self.height > obstacle.y and self.y < obstacle.y + obstacle.height:
                return True
       return False


class EnergyBoost(object):
    img = pygame.image.load(os.path.join('images', 'energy-boost.png')).convert_alpha()
    img = pygame.transform.scale(img, (32, 32))
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 32
        self.height = 32
        self.visible = True
    def draw(self, win):
        if self.visible:
            win.blit(self.img, (self.x, self.y))
    def collide(self, rect):
        if not self.visible: return False
        boost_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        player_rect = pygame.Rect(rect[0], rect[1], rect[2], rect[3])
        if boost_rect.colliderect(player_rect):
            self.visible = False
            return True
        return False



class saw(object):
    rotate = [pygame.image.load(os.path.join('images', 'SAW0.png')), pygame.image.load(os.path.join('images', 'SAW1.png')), pygame.image.load(os.path.join('images', 'SAW2.png')), pygame.image.load(os.path.join('images', 'SAW3.png'))]

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rotateCount = 0
        self.vel = 1.4

    def draw(self, win):
        self.hitbox = (self.x + 10, self.y + 5, self.width - 20, self.height - 5)
        
        #pygame.draw.rect(win, (255,0,0), self.hitbox, 2)
        
        if self.rotateCount >= 8:
            self.rotateCount = 0
        win.blit(pygame.transform.scale(self.rotate[self.rotateCount//2], (64,64)), (self.x,self.y))
        self.rotateCount += 1

    def collide(self, rect):
        if rect[0] + rect[2] > self.hitbox[0] and rect[0] < self.hitbox[0] + self.hitbox[2]:
            if rect[1] + rect[3] > self.hitbox[1]:
                return True
        return False


class spike(saw):
    img = pygame.image.load(os.path.join('images', 'spike.png'))

    def draw(self, win):
        self.hitbox = (self.x + 10, self.y, 28,315)
        
        
        #pygame.draw.rect(win, (255,0,0), self.hitbox, 2)
        
        win.blit(self.img, (self.x, self.y))

    def collide(self, rect):
        if rect[0] + rect[2] > self.hitbox[0] and rect[0] < self.hitbox[0] + self.hitbox[2]:
            if rect[1] < self.hitbox[3]:
                return True
        return False


def updateFile():
# Create scores.txt file if it doesn't exist
    if not os.path.exists("scores.txt"):
     with open("scores.txt", "w") as f:
        f.write("0")
    f = open('scores.txt','r')
    file = f.readlines()
    last = int(file[0])

    if last < int(score):
        f.close()
        file = open('scores.txt', 'w')
        file.write(str(score))
        file.close()

        return score

    return last


def updateCoins():
    if not os.path.exists("coins.txt"):
        with open("coins.txt", "w") as f:
            f.write("0")
    with open('coins.txt','r') as f:
        file = f.readlines()
        last = int(file[0])

    if last < coins_collected:
        with open('coins.txt', 'w') as f:
            f.write(str(coins_collected))
        return coins_collected

    return last




def endScreen():


    global pause, score, speed, obstacles, coins_collected

   
    pause = 0
    speed = 30
    obstacles = []

    updateCoins()

    run = True
    while run:
        pygame.time.delay(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False
                runner.falling = False
                runner.sliding = False
                runner.jumping = False

        win.blit(bg, (0,0))

        largeFont = pygame.font.SysFont('comicsans', 30)

        lastScore = largeFont.render('Best Score: ' + str(updateFile()),1,(255,255,255))
        currentScore = largeFont.render('Score: '+ str(score),1,(255,255,255))
        win.blit(lastScore, (W/2 - lastScore.get_width()/2,150))
        win.blit(currentScore, (W/2 - currentScore.get_width()/2, 190))

        coinScore = largeFont.render('Coins Collected: ' + str(coins_collected),1,(255,255,255))
        bestCoinScore = largeFont.render('Best Coins: ' + str(updateCoins()),1,(255,255,255))
        win.blit(coinScore, (W/2 - coinScore.get_width()/2, 230))
        win.blit(bestCoinScore, (W/2 - bestCoinScore.get_width()/2, 270))


 
        pygame.display.update()


    score = 0
    coins.clear()
    coins_collected = 0

    runner.reset()

def redrawWindow():
    largeFont = pygame.font.SysFont('comicsans', 30)
    win.blit(bg, (bgX, 0))
    win.blit(bg, (bgX2,0))
    text = largeFont.render('Score: ' + str(score), 1, (255,255,255))
    runner.draw(win)
    for obstacle in obstacles:
        obstacle.draw(win)

    for c in coins:
        c.draw(win)

    for b in energy_boosts:
        b.draw(win)



    win.blit(text, (700, 10))
    pygame.display.update()


pygame.time.set_timer(USEREVENT+1, 500)
pygame.time.set_timer(USEREVENT+2, 3000)
pygame.time.set_timer(USEREVENT+3, 4000)  # every 4 seconds spawn a coin
pygame.time.set_timer(USEREVENT+4, 10000)  # every 10s try to spawn a boost


speed = 30

score = 0
coins = []
coins_collected = 0

energy_boosts = []              # will hold on-screen boosts
energy_boost_collected = False  # have we picked one up?
energy_boost_used = False       # has the shield been consumed?


run = True
runner = player(200, 313, 64, 64)

obstacles = []
pause = 0
fallSpeed = 0

countdown_timer(screen, font, clock)

while run:


    if pause > 0:
        pause += 1
        if pause > fallSpeed * 2:
            endScreen()

    score = speed//10 - 3



    # for obstacle in obstacles:
    # # did we hit a saw or spike?
    #  if obstacle.collide(runner.hitbox):
    #     # 1st hit after boost → consume shield, keep playing
    #     if energy_boost_collected and not energy_boost_used:
    #         energy_boost_used = True
    #         energy_boost_collected = False
    #         print("🛡 Shield used – you survived!")
    #     else:
    #         # no shield (or already used) → normal death
    #         runner.falling = True
    #         if pause == 0:
    #             pause = 1
    #             fallSpeed = speed

    # # always move the obstacle left, then remove when off-screen
    #  if obstacle.x < -64:
    #     obstacles.pop(obstacles.index(obstacle))
    #  else:
    #     obstacle.x -= 1.4

    for obstacle in obstacles:
        if obstacle.collide(runner.hitbox):
            if energy_boost_collected and not energy_boost_used:
                energy_boost_used = True  # Use the shield
                obstacles.remove(obstacle)  # Remove obstacle
            else:
                runner.falling = True
                if pause == 0:
                    pause = 1
                    fallSpeed = speed

        if obstacle.x < -64:
            obstacles.remove(obstacle)
        else:
            obstacle.x -= 1.4




    for c in coins:
        if c.collide(runner.hitbox):
            coins_collected += 1
        if c.x < -32:
            coins.pop(coins.index(c))
        else:
            c.x -= 1.4


    for b in energy_boosts:
        if b.collide(runner.hitbox):
            energy_boost_collected = True
        if b.x < -32:
            energy_boosts.pop(energy_boosts.index(b))
        else:
            b.x -= 1.4




    bgX -= 1.4
    bgX2 -= 1.4

    if bgX < bg.get_width() * -1:
        bgX = bg.get_width()
    if bgX2 < bg.get_width() * -1:
        bgX2 = bg.get_width()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            quit()

        if event.type == USEREVENT+1:
            speed += 1

        if event.type == USEREVENT+2:
            r = random.randrange(0,2)
            if r == 0:
                obstacles.append(saw(810, 310, 64, 64))
            elif r == 1:
                obstacles.append(spike(810, 0, 48, 310))
 
        if event.type == pygame.USEREVENT + 3:
            coin_y = random.choice([250, 280, 300])
            coin_x = 810  # Start at 810
            new_coin = coin(coin_x, coin_y)

            if not new_coin.collides_with_obstacle(obstacles):
               coins.append(new_coin)
               coin_added = True
            else:
             # Try slightly different positions if collision detected
               offset = random.randint(50, 150)
               coin_x += offset
               new_coin = coin(coin_x, coin_y)
               if not new_coin.collides_with_obstacle(obstacles):
                 coins.append(new_coin)
                 coin_added = True

        
        if event.type == pygame.USEREVENT + 4:
            bx = 810
            by = random.choice([250, 280, 300])
            new_boost = EnergyBoost(bx, by)
            if not new_boost.collide((0,0,0,0)):  # quick obstacle-free check
              energy_boosts.append(new_boost)



        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_b:  # Press 'B' to change background
              current_bg_index = (current_bg_index + 1) % len(backgrounds)
              bg = backgrounds[current_bg_index]
              bgX = 0
              bgX2 = bg.get_width()


    if runner.falling == False:
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
            if not(runner.jumping):
                runner.jumping = True

        if keys[pygame.K_DOWN]:
            if not(runner.sliding):
                runner.sliding = True

    clock.tick(speed)
    redrawWindow()
