import pygame
from pygame.locals import *
import os
import random

pygame.init()

W, H = 800, 437
win = pygame.display.set_mode((W, H))
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption('Side Scroller')

# Clock and font
clock = pygame.time.Clock()
font = pygame.font.SysFont("comicsans", 72)  # You can change font
small_font = pygame.font.SysFont("comicsans", 30)

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
    pygame.image.load(os.path.join('images', 'factory.png')).convert(),
    pygame.image.load(os.path.join('images', 'snow.png')).convert(),
    pygame.image.load(os.path.join('images', 'night.png')).convert()
]

# Scale all backgrounds to fit the screen
for i in range(len(backgrounds)):
    backgrounds[i] = pygame.transform.scale(backgrounds[i], (W, H))

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
        self.width = 35
        self.height = 35
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
    def collides_with_obstacle(self, obstacles):
        for obstacle in obstacles:
            # 100 pixel safe zone horizontally
            if abs(self.x - obstacle.x) < 100:
                # Check vertical overlap
                if self.y + self.height > obstacle.y and self.y < obstacle.y + obstacle.height:
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




class EndPoint(object):
    img = pygame.image.load(os.path.join('images', 'flag.png'))
    def __init__(self, x, y, width=64, height=64):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        # Scale the image
        self.scaled_img = pygame.transform.scale(self.img, (width, height))
        self.visible = False
        self.active = False
        
    def draw(self, win):
        if self.visible:
            win.blit(self.scaled_img, (self.x, self.y))
            
    def collide(self, rect):
        if not self.visible or not self.active: 
            return False
        endpoint_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        player_rect = pygame.Rect(rect[0], rect[1], rect[2], rect[3])
        return endpoint_rect.colliderect(player_rect)
    def collides_with_obstacle(self, obstacles):
        for obstacle in obstacles:
            # Check horizontal distance
            if abs(self.x - obstacle.x) < 100:
                # Check vertical overlap
                if self.y + self.height > obstacle.y and self.y < obstacle.y + obstacle.height:
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


def updateLevel():
    if not os.path.exists("level.txt"):
        with open("level.txt", "w") as f:
            f.write("1")
    with open('level.txt','r') as f:
        file = f.readlines()
        last = int(file[0])

    if last < current_level:
        with open('level.txt', 'w') as f:
            f.write(str(current_level))
        return current_level

    return last


def levelCompleteScreen():
    global pause, score, speed, obstacles, coins_collected, coins_required, current_level
    
    pause = 0
    obstacles.clear()
    
    updateCoins()
    updateLevel()
    
    # Check if player collected enough coins
    success = coins_collected >= coins_required
    
    # Check if this is the final level
    is_final_level = current_level >= highest_level
    
    run = True
    while run:
        pygame.time.delay(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                # Check if button was clicked
                if 300 <= mouse_pos[0] <= 500 and 350 <= mouse_pos[1] <= 400:
                    if success and not is_final_level:
                        # Next Level button was clicked
                        current_level += 1
                        resetGame(keep_score=True)
                    else:
                        # Play Again button was clicked
                        current_level = 1  # Reset to level 1 when restarting
                        resetGame(keep_score=False)
                    run = False
        
        win.blit(bg, (0,0))
        
        largeFont = pygame.font.SysFont('comicsans', 40)
        smallFont = pygame.font.SysFont('comicsans', 30)
        
        if is_final_level and success:
            # Game completed message
            msg = largeFont.render('Game Completed!', 1, (0,255,0))
            next_level_btn = smallFont.render('Play Again', 1, (255,255,255))
        elif success:
            msg = largeFont.render('Level ' + str(current_level) + ' Complete!', 1, (0,255,0))
            next_level_btn = smallFont.render('Next Level', 1, (255,255,255))
        else:
            msg = largeFont.render('Level ' + str(current_level) + ' Failed!', 1, (255,0,0))
            next_level_btn = smallFont.render('Play Again', 1, (255,255,255))
            
        win.blit(msg, (W/2 - msg.get_width()/2, 100))
        
        currentScore = smallFont.render('Score: '+ str(score), 1, (255,255,255))
        coinScore = smallFont.render('Coins Collected: ' + str(coins_collected) + '/' + str(coins_required), 1, (255,255,255))
        levelText = smallFont.render('Current Level: ' + str(current_level), 1, (255,255,255))
        
        win.blit(currentScore, (W/2 - currentScore.get_width()/2, 170))
        win.blit(coinScore, (W/2 - coinScore.get_width()/2, 210))
        win.blit(levelText, (W/2 - levelText.get_width()/2, 250))
        
        # If the final level was completed, show additional "Game Completed" text
        if is_final_level and success:
            finalMsg = smallFont.render('Congratulations! You finished the game!', 1, (255,215,0))
            win.blit(finalMsg, (W/2 - finalMsg.get_width()/2, 290))
        
        # Draw button
        pygame.draw.rect(win, (0,128,255), (300, 350, 200, 50))
        win.blit(next_level_btn, (W/2 - next_level_btn.get_width()/2, 360))
        
        pygame.display.update()

def gameOverScreen():
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
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                # Check if play again button was clicked
                if 300 <= mouse_pos[0] <= 500 and 350 <= mouse_pos[1] <= 400:
                    run = False
                    resetGame(keep_score=False)
        
        win.blit(bg, (0,0))
        
        largeFont = pygame.font.SysFont('comicsans', 30)
        
        lastScore = largeFont.render('Best Score: ' + str(updateFile()), 1, (255,255,255))
        currentScore = largeFont.render('Score: '+ str(score), 1, (255,255,255))
        win.blit(lastScore, (W/2 - lastScore.get_width()/2, 150))
        win.blit(currentScore, (W/2 - currentScore.get_width()/2, 190))
        
        coinScore = largeFont.render('Coins Collected: ' + str(coins_collected), 1, (255,255,255))
        bestCoinScore = largeFont.render('Best Coins: ' + str(updateCoins()), 1, (255,255,255))
        levelText = largeFont.render('Level: ' + str(current_level), 1, (255,255,255))
        
        win.blit(coinScore, (W/2 - coinScore.get_width()/2, 230))
        win.blit(bestCoinScore, (W/2 - bestCoinScore.get_width()/2, 270))
        win.blit(levelText, (W/2 - levelText.get_width()/2, 310))
        
        # Draw play again button
        pygame.draw.rect(win, (0,128,255), (300, 350, 200, 50))
        playAgain = largeFont.render('Play Again', 1, (255,255,255))
        win.blit(playAgain, (W/2 - playAgain.get_width()/2, 360))
        
        pygame.display.update()


def resetGame(keep_score=False):
    global runner, obstacles, coins, energy_boosts, pause, fallSpeed
    global energy_boost_collected, energy_boost_used, endpoint, bgX, bgX2
    global speed, coins_collected, distance_traveled, current_level, coins_required
    
    runner.reset()
    obstacles.clear()
    coins.clear()
    energy_boosts.clear()
    
    energy_boost_collected = False
    energy_boost_used = False
    
    pause = 0
    fallSpeed = 0
    
    bgX = 0
    bgX2 = bg.get_width()
    
    # Reset endpoint
    endpoint.x = 1000 + (current_level - 1) * 1000  # Level 1: 5000, Level 2: 6000, etc.
    endpoint.visible = False
    endpoint.active = False
    
    # Reset speed depending on level
    speed = 30 + (current_level - 1) * 5
    
    # Reset distance traveled
    distance_traveled = 0
    
    # Update level settings
    level_settings = get_level_settings(current_level)
    coins_required = level_settings["coins_required"]
    
    if not keep_score:
        global score
        score = 0
        coins_collected = 0
    else:
        # This is the key change - reset coins when moving to a new level
        coins_collected = 0


def redrawWindow():
    largeFont = pygame.font.SysFont('comicsans', 30)
    win.blit(bg, (bgX, 0))
    win.blit(bg, (bgX2, 0))
    
    # Draw UI
    score_text = largeFont.render('Score: ' + str(score), 1, (255,255,255))
    level_text = small_font.render('Level: ' + str(current_level), 1, (255,255,255))
    coins_text = small_font.render('Coins: ' + str(coins_collected) + '/' + str(coins_required), 1, (255,255,255))
    
    # Draw shield indicator if collected
    if energy_boost_collected and not energy_boost_used:
        shield_text = small_font.render('Shield: Active', 1, (0,255,0))
        win.blit(shield_text, (10, 80))
    
    win.blit(score_text, (650, 10))
    win.blit(level_text, (10, 10))
    win.blit(coins_text, (10, 40))
    
    # Draw entities
    runner.draw(win)
    endpoint.draw(win)
    
    for obstacle in obstacles:
        obstacle.draw(win)
    
    for c in coins:
        c.draw(win)
    
    for b in energy_boosts:
        b.draw(win)
    
    # Draw endpoint/flag distance indicator when flag is not visible
    if not endpoint.visible:
        distance_to_flag = endpoint.x - runner.x
        if distance_to_flag > 0:
            flag_dist_text = small_font.render('Flag: ' + str(int(distance_to_flag//100)) + 'm', 1, (255,200,0))
            win.blit(flag_dist_text, (650, 40))
    
    pygame.display.update()


# Set up game timers
pygame.time.set_timer(USEREVENT+1, 500)    # Speed increase
pygame.time.set_timer(USEREVENT+2, 3000)   # Obstacle spawn
pygame.time.set_timer(USEREVENT+3, 4000)   # Coin spawn
pygame.time.set_timer(USEREVENT+4, 10000)  # Energy boost spawn

# Game variables
speed = 30
score = 0
coins = []
coins_collected = 0
energy_boosts = []
energy_boost_collected = False
energy_boost_used = False
obstacles = []
pause = 0
fallSpeed = 0
distance_traveled = 0

# Level setup
current_level = 1
highest_level = 3  # Total number of levels in the game

# Create player
runner = player(200, 313, 64, 64)

# Create endpoint/flag
endpoint = EndPoint(1000, 313)  # Start far off-screen

# Level-specific settings
def get_level_settings(level):
    settings = {
        1: {"coins_required": 1, "bg_index": 0, "obstacle_frequency": 5000, "coin_frequency": 3000},
        2: {"coins_required": 5, "bg_index": 1, "obstacle_frequency": 2500, "coin_frequency": 3500},
        3: {"coins_required": 10, "bg_index": 2, "obstacle_frequency": 2000, "coin_frequency": 3000},
    }
    return settings.get(level, settings[1])  # Default to level 1 settings if level not found

# Set initial level settings
level_settings = get_level_settings(current_level)
coins_required = level_settings["coins_required"]
current_bg_index = level_settings["bg_index"]
bg = backgrounds[current_bg_index]
bgX = 0
bgX2 = bg.get_width()

# Update timers based on level
pygame.time.set_timer(USEREVENT+2, level_settings["obstacle_frequency"])
pygame.time.set_timer(USEREVENT+3, level_settings["coin_frequency"])

# Start game with countdown
countdown_timer(screen, font, clock)

# Main game loop
run = True
while run:
    if pause > 0:
        pause += 1
        if pause > fallSpeed * 2:
            gameOverScreen()
    
    # Update score based on speed
    score = speed//10 - 3 + (current_level - 1) * 10
    
    # Update endpoint visibility based on distance
    if distance_traveled > endpoint.x - 800:
        # Check if endpoint would collide with obstacles
        if endpoint.collides_with_obstacle(obstacles):
            # Move endpoint slightly to avoid collision
            endpoint.x += 150
        endpoint.visible = True
        endpoint.active = True
    
    # Process obstacles
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
            if obstacle in obstacles:  # Check if still in list to avoid errors
                obstacles.remove(obstacle)
        else:
            obstacle.x -= 1.4
    
    # Process coins
    for c in coins:
        if c.collide(runner.hitbox):
            coins_collected += 1
        if c.x < -32:
            if c in coins:  # Check if still in list to avoid errors
                coins.remove(c)
        else:
            c.x -= 1.4
    
    # Process energy boosts
    for b in energy_boosts:
        if b.collide(runner.hitbox):
            energy_boost_collected = True
        if b.x < -32:
            if b in energy_boosts:  # Check if still in list to avoid errors
                energy_boosts.remove(b)
        else:
            b.x -= 1.4
    
    # Move endpoint
    if endpoint.visible:
        endpoint.x -= 1.4
        # Check if player reached endpoint
        if endpoint.collide(runner.hitbox):
            levelCompleteScreen()
            
    # Update background positions
    bgX -= 1.4
    bgX2 -= 1.4
    
    if bgX < bg.get_width() * -1:
        bgX = bg.get_width()
    if bgX2 < bg.get_width() * -1:
        bgX2 = bg.get_width()
    
    # Update distance traveled
    distance_traveled += 1.4
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            quit()
        
        # Speed increase event
        if event.type == USEREVENT+1:
            speed += 1
        
        # Obstacle spawn event
        if event.type == USEREVENT+2:
            r = random.randrange(0, 2)
            if r == 0:
                obstacles.append(saw(810, 310, 64, 64))
            elif r == 1:
                # Platforms get bigger with difficulty
                size = 30 + (current_level - 1) * 5  # Bigger spikes in higher levels
                obstacles.append(spike(810, 0, 48, 410))
        
        # Coin spawn event
        if event.type == pygame.USEREVENT + 3:
            coin_y = random.choice([250, 280, 300])
            coin_x = 810  # Start at 810
            new_coin = coin(coin_x, coin_y)
            
            if not new_coin.collides_with_obstacle(obstacles):
                coins.append(new_coin)
            else:
                # Try slightly different positions if collision detected
                offset = random.randint(50, 150)
                coin_x += offset
                new_coin = coin(coin_x, coin_y)
                if not new_coin.collides_with_obstacle(obstacles):
                    coins.append(new_coin)
        
        # Energy boost spawn event
        if event.type == pygame.USEREVENT + 4:
            # Only spawn if player doesn't have one
            if not energy_boost_collected and not energy_boost_used:
                bx = 810
                by = random.choice([250, 280, 300])
                new_boost = EnergyBoost(bx, by)
                
                if not new_boost.collides_with_obstacle(obstacles):
                    energy_boosts.append(new_boost)
                else:
                    # Try slightly different position if collision detected
                    offset = random.randint(50, 150)
                    bx += offset
                    new_boost = EnergyBoost(bx, by)
                    if not new_boost.collides_with_obstacle(obstacles):
                        energy_boosts.append(new_boost)
        
        # Background change key
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_b:  # Press 'B' to change background
                current_bg_index = (current_bg_index + 1) % len(backgrounds)
                bg = backgrounds[current_bg_index]
                bgX = 0
                bgX2 = bg.get_width()
    
    # Player controls
    if not runner.falling:
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
            if not runner.jumping:
                runner.jumping = True
        
        if keys[pygame.K_DOWN]:
            if not runner.sliding:
                runner.sliding = True
    
    # Update display
    clock.tick(speed)
    redrawWindow()

pygame.quit()