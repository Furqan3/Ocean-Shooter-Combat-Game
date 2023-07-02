import pygame
import random
from pygame import mixer
from Connect_Window import *
pygame.font.init()

# Initialize the colors
blue = (177, 201, 222)
magenta = (153, 0, 76)
pink = (255, 0, 127)
black = (0, 0, 0)
white = (255, 255, 255)
red	=(255, 0, 0)
lime = (0, 255, 0)

# Pygame Initialization
pygame.init()

# Create the screen
screen_width = 800
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))

# Sound
# mixer.music.load("Music/background.mp3")
# mixer.music.play(-1)

# Set the caption
pygame.display.set_caption("Ocean Shooter Combat Game")

# Set the icon
icon = pygame.image.load('Image/icon.png')
pygame.display.set_icon(icon)

# player/submarine image
submarine = pygame.image.load("Image/ship1.png")
submarine_two = pygame.image.load("Image/ship.png")

# bullet image
bullet = pygame.image.load("Image/bullet.png")
bullet_two = pygame.image.load("Image/bullet.png")

# enemy images
sharkLeft = pygame.image.load("Image/shark.png")
sharkRight = pygame.image.load("Image/shark2.png")
sharkMidlle = pygame.image.load("Image/shark3.png")
stone = pygame.image.load("Image/stone.png")
minifish = pygame.image.load("Image/minifish.png")
mini = pygame.image.load("Image/minifish2.png")
stoneOne = pygame.image.load("Image/stone1.png")
stoneTwo = pygame.image.load("Image/stone2.png")

# background images
bg = pygame.transform.scale(pygame.image.load("Image/bbgg.jpg"), (screen_width, screen_height))
welcome_bg = pygame.transform.scale(pygame.image.load("Image/wcbg.jpg"), (screen_width, screen_height))
stage_bg = pygame.transform.scale(pygame.image.load("Image/wall1.jpg"), (screen_width, screen_height))
easy_bg = pygame.transform.scale(pygame.image.load("Image/easy.jpg"), (screen_width, screen_height))
medium_bg = pygame.transform.scale(pygame.image.load("Image/medium.jpg"), (screen_width, screen_height))

# Powerup images
healthpowerup = pygame.image.load("Image/health.png")
livespowerup = pygame.image.load("Image/lives.png")

# initializing fonts and clock for welcome or other screens as are not part of the game loop
clock = pygame.time.Clock()
font = pygame.font.SysFont("Bahnschrift Condensed", 54)

score = 0

# multiplayer
multiplayer = False
player1 = True
player2 = True


def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    screen.blit(screen_text, [x, y])


# Images for quit, multiplayer, stages and high score buttons on welcome screen
stages_btn = pygame.image.load("Image/level.png").convert_alpha()
stagebtn_X = 170
stagebtn_Y = 330

highscore_btn = pygame.image.load("Image/highscore.png").convert_alpha()
highscorebtn_X = 380
highscorebtn_Y = 250

multiplayer_btn = pygame.image.load("Image/com.png").convert_alpha()
multiplayer_X = 580
multiplayer_Y = 380

multiplayerg_btn = pygame.image.load("Image/player.png").convert_alpha()
multiplayerg_X = 30
multiplayerg_Y = 250

quit_btn = pygame.image.load("Image/quit.png").convert_alpha()
quit_X = 720
quit_Y = 550

# Images for stage based icons
easy_btn = pygame.image.load("Image/easy.png").convert_alpha()
easy_X = 150
easy_Y = 400

medium_btn = pygame.image.load("Image/medium.png").convert_alpha()
medium_X = 350
medium_Y = 400

hard_btn = pygame.image.load("Image/hard.png").convert_alpha()
hard_X = 560
hard_Y = 400


# Stage window icon functions
def easybtn(x, y):
    screen.blit(easy_btn, (x, y))


def mediumbtn(x, y):
    screen.blit(medium_btn, (x, y))


def hardbtn(x, y):
    screen.blit(hard_btn, (x, y))


# Stage button function
def stagebtn(x, y):
    screen.blit(stages_btn, (x, y))


# Highscore button function
def highscorebtn(x, y):
    screen.blit(highscore_btn, (x, y))


# Multiplayer button function
def multiplayerbtn(x, y):
    screen.blit(multiplayer_btn, (x, y))

def multiplayerbtng(x, y):
    screen.blit(multiplayerg_btn, (x, y))

# Quit button function
def quitbtn(x, y):
    screen.blit(quit_btn, (x, y))


class Bullets:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x + 10, self.y))

    def move(self, vel):
        self.y += vel

    def off_screen(self, height):
        return self.y > height or self.y < 0

    def collision(self, obj):
        return collide(self, obj)


# for 1 player
class Ship:
    CoolDown = 30

    def __init__(self, x, y, health=10):
        self.x = x
        self.y = y
        self.health = health

        # allow us to draw a ship/submarine image
        self.shipimg = None

        # allow us to draw a bullet image
        self.bulletimg = None

        self.bullets = []

        # when we start shooting bullet we make sure to spam a bullet
        self.cool_down_counter = 0

    def draw(self, window):
        window.blit(self.shipimg, (self.x, self.y))
        # pygame.draw.rect(window, (255, 0, 0), (self.x, self.y, 50 , 50))
        for bullet in self.bullets:
            bullet.draw(window)

    def move_bullets(self, vel, obj):
        self.cooldown()
        for bullet in self.bullets:
            bullet.move(vel)
            if bullet.off_screen(screen_height):
                self.bullets.remove(bullet)
            elif bullet.collision(obj):
                # explosionSound = mixer.Sound("Music/explosion.wav")
                # explosionSound.play()
                obj.health -= 10
                self.bullets.remove(bullet)

    def cooldown(self):
        if self.cool_down_counter >= self.CoolDown:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self):
        if self.cool_down_counter == 0:
            bullet = Bullets(self.x + 40, self.y, self.bulletimg)
            self.bullets.append(bullet)
            bulletSound = mixer.Sound("Music/laser.wav")
            bulletSound.play()
            self.cool_down_counter = 1

    # these two methods <<<  get.width() and get.height()  >>> are getters
    # these methods just turning a value to us
    def get_width(self):
        return self.shipimg.get_width()

    def get_height(self):
        return self.shipimg.get_height()


# player is going to inherit from ship
class Player(Ship):
    def __init__(self, x, y, health=100):
        # calling all intiliaztions methods from ship class
        super().__init__(x, y, health)
        self.shipimg = submarine
        self.bulletimg = bullet

        # mask --> do pixel perfect collision
        self.mask = pygame.mask.from_surface(self.shipimg)
        self.max_health = health

    def move_bullets(self, vel, objs):
        global score
        self.cooldown()
        for bullet in self.bullets:
            bullet.move(vel)
            if bullet.off_screen(screen_height):
                self.bullets.remove(bullet)
            else:
                for obj in objs:
                    if bullet.collision(obj):
                        objs.remove(obj)
                        score += 2
                        # explosion = mixer.Sound("Music/explo.wav")
                        # explosion.play()
                        if bullet in self.bullets:
                            self.bullets.remove(bullet)

    def healthbar(self, window):
        pygame.draw.rect(window, (255, 0, 0),
                            (self.x, self.y + self.shipimg.get_height() - 20, self.shipimg.get_width(), 12))
        pygame.draw.rect(window, (0, 255, 0), (
            self.x, self.y + self.shipimg.get_height() - 20, self.shipimg.get_width() * (self.health / self.max_health),
            12))

    def draw(self, window):
        super().draw(window)
        self.healthbar(window)


class user(Ship):
    def __init__(self, x, y, health=100):
        # calling all intiliaztions methods from ship class
        super().__init__(x, y, health)
        self.shipimg = submarine_two
        self.bulletimg = bullet_two

        # mask --> do pixel perfect collosion
        self.mask = pygame.mask.from_surface(self.shipimg)
        self.max_health = health

    def draw(self, window):
        super().draw(window)
        self.healthbar(window)

    def healthbar(self, window):
        pygame.draw.rect(window, (255, 0, 0),
                            (self.x, self.y + self.shipimg.get_height() - 20, self.shipimg.get_width(), 12))
        pygame.draw.rect(window, (0, 255, 0),
                            (self.x, self.y + self.shipimg.get_height() - 20,
                          self.shipimg.get_width() * (self.health / self.max_health), 12))

    def move_bullets(self, vel, objs):
        global score
        self.cooldown()
        for bullet_two in self.bullets:
            bullet_two.move(vel)
            if bullet_two.off_screen(screen_height):
                self.bullets.remove(bullet_two)
            else:
                for obj in objs:
                    if bullet_two.collision(obj):
                        objs.remove(obj)
                        score += 2
                        self.bullets.remove(bullet_two)
                        if bullet_two in self.bullets:
                            self.bullets.remove(bullet_two)

    def get_width(self):
        return self.shipimg.get_width()

    def get_height(self):
        return self.shipimg.get_height()


# for both single and multiplayer
class Enemy(Ship):
    color_map = {
        "red": (sharkLeft, stone),
        "green": (sharkRight, minifish),
        "blue": (sharkMidlle, mini),
        "yellow": (stoneOne,stoneTwo)
    }

    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.shipimg, self.bulletimg = self.color_map[color]
        self.mask = pygame.mask.from_surface(self.shipimg)

    def shoot(self):
        if self.cool_down_counter == 0:
            bullet = Bullets(self.x - 10, self.y, self.bulletimg)
            self.bullets.append(bullet)
            self.cool_down_counter = 1

    # moving the enemy downwards..
    def move(self, vel):
        self.y += vel


def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

class PowerUps(Ship):
    color_map = {
        "orange": (livespowerup, healthpowerup)
    }

    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.shipimg, self.bulletimg = self.color_map[color]
        self.mask = pygame.mask.from_surface(self.shipimg)

    # moving the enemy downwards..
    def move(self, vel):
        self.y += vel


def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None


def multiplayerg():

    running = True
    fps = 80

    level = 0
    lives = 5

    main_font = pygame.font.SysFont("comicsans", 30)
    lost_font = pygame.font.SysFont("comicsans", 70)
   # font = pygame.font.SysFont("arial", 30)
    enemies = []
    wave_length = 5
    enemy_vel = 1

    player_vel = 7
    user_vel = 7
    laser_vel = 7
    player = Player(80, 650)
    ship_one = user(650, 650)
    clock = pygame.time.Clock()

    lost = False
    lost_count = 0


    global score
    score = 0

    def draw_window():
        screen.blit(bg, (0, 0))

        lives_label = main_font.render(f"lives : {lives}", 1, (255, 255, 255))
        score_label = main_font.render(f"score : {score}", 1, (255, 255, 255))
        level_label = main_font.render(f"level : {level}", 1, (255, 255, 255))

        screen.blit(lives_label, (10, 10))
        screen.blit(level_label, (screen_width - level_label.get_width() - 20, 10))
        screen.blit(score_label, (screen_width - score_label.get_width() - 20, 50))


        for enemy in enemies:
            enemy.draw(screen)

        if multiplayerg:  # Display lives left & players
            if player1:
                player.draw(screen)  # player1
            if player2:
                ship_one.draw(screen)  # player2

        if lost:
            lost_label = lost_font.render("You Lost!!", 1, (255, 255, 255))
            screen.blit(lost_label, (screen_width / 2 - lost_label.get_width() / 2, 350))

        pygame.display.update()

    global player1, player2

    while running:

        clock.tick(fps)
        draw_window()

        if multiplayerg:
            if lives <= 0 or (player.health <= 0 and ship_one.health <= 0):
                lost = True
                lost_count += 1

            if player.health <= 0:
                player1 = False
            if ship_one.health <= 0:
                player2 = False

        if lost:
            if lost_count > fps * 3:
                running = False
            else:
                continue

        if not enemies:
            level += 1
            wave_length += 5
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, screen_width - 100), random.randrange(-1230, -100),
                              random.choice(["red", "green"]))  # [red, green]
                enemies.append(enemy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - player_vel > 0:
            player.x -= player_vel
        if keys[pygame.K_RIGHT] and player.x + player_vel + player.get_width() < screen_width:
            player.x += player_vel
        if keys[pygame.K_UP] and player.y - player_vel > 0:
            player.y -= player_vel
        if keys[pygame.K_DOWN] and player.y + player_vel + player.get_height() < screen_height:
            player.y += player_vel
        if keys[pygame.K_SPACE]:
            player.shoot()

        if keys[pygame.K_a] and ship_one.x - user_vel > 0:
            ship_one.x -= user_vel
        if keys[pygame.K_d] and ship_one.x + user_vel + player.get_width() < screen_width:
            ship_one.x += user_vel
        if keys[pygame.K_w] and ship_one.y - user_vel > 0:
            ship_one.y -= user_vel
        if keys[pygame.K_s] and ship_one.y + user_vel + player.get_height() < screen_height:
            ship_one.y += user_vel
        if keys[pygame.K_LCTRL]:
            ship_one.shoot()

        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_bullets(laser_vel, player)
            enemy.move_bullets(laser_vel, ship_one)

            if random.randrange(0, 2 * 60) == 1:
                enemy.shoot()

            if collide(enemy, player):
                player.health -= 10
                enemies.remove(enemy)
            if collide(enemy, ship_one):
                ship_one.health -= 10
                enemies.remove(enemy)

            elif enemy.y + enemy.get_height() > screen_height:
                lives -= 1
                enemies.remove(enemy)

        player.move_bullets(-laser_vel, enemies)
        ship_one.move_bullets(-laser_vel, enemies)


def highscores():
    running = True
    fps = 80

    level = 0
    lives = 5

    with open("highscore.txt", "r") as f:
        highscore = f.read()

    main_font = pygame.font.SysFont("comicsans", 30)
    lost_font = pygame.font.SysFont("comicsans", 70)

    # this will store where all our enemies are.
    enemies = []
    wave_length = 5
    enemy_vel = 1
    player_vel = 10
    player = Player(380, 670)

    powerups = []
    powerup_waveLength = 1
    powerup_vel = 3
    laser_vel = 5

    lost = False
    lost_count = 0

    global score
    score = 0
    clock = pygame.time.Clock()

    def draw_window():
        screen.blit(bg, (0, 0))

        # draw text labels
        lives_label = main_font.render(f"lives : {lives}", 1, (255, 255, 255))
        score_label = main_font.render(f"Score: {score}", 1, (255, 255, 255))
        highscore_label = main_font.render(f"highscores: {highscore}", 1, (255, 255, 255))

        # to blit these labels on screen
        screen.blit(lives_label, (10, 10))
        screen.blit(score_label, (screen_width - score_label.get_width() - 20, 5))
        screen.blit(highscore_label, (screen_width - highscore_label.get_width() - 20, 39))

        for enemy in enemies:
            enemy.draw(screen)

        for powerup in powerups:
            powerup.draw(screen)

        player.draw(screen)

        if lost:
            lost_label = lost_font.render("You Lost!!", 1, (255, 255, 255))
            score_label = main_font.render(f"Score:{score}", 1, (255, 255, 255))
            screen.blit(lost_label, (screen_width / 2 - lost_label.get_width() / 2, 350))
            screen.blit(score_label, (screen_width / 2 - score_label.get_width() / 2, 450))

        pygame.display.update()

    while running:
        with open("highscore.txt", "w") as f:
            f.write(str(highscore))
        clock.tick(fps)
        draw_window()

        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > fps * 3:
                running = False
            else:
                continue

        if not enemies:
            level += 1
            wave_length += 5
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, screen_width - 100), random.randrange(-1230, -100),
                                random.choice(["red", "green", "yellow"]))  # [red, green]
                enemies.append(enemy)


        if not powerups:
            level += 1
            #powerup_waveLength +=1
            for j in range(powerup_waveLength):
                powerup = PowerUps(random.randrange(50, screen_width - 100), random.randrange(-1230, -100),
                                random.choice(["orange"]))  # [red, green]
                powerups.append(powerup)



        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        # return a dictionary of ALL keys and tell whether that keys are pressed or not at the current time
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - player_vel > 0:  # left
            player.x -= player_vel
        if keys[pygame.K_RIGHT] and player.x + player_vel + player.get_width() < screen_width:  # right
            player.x += player_vel
        if keys[pygame.K_UP] and player.y - player_vel > 0:  # up
            player.y -= player_vel
        if keys[pygame.K_DOWN] and player.y + player_vel + player.get_height() < screen_height:  # down
            player.y += player_vel
        if keys[pygame.K_SPACE]:
            player.shoot()

        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_bullets(laser_vel, player)

            if random.randrange(0, 2 * 60) == 1:
                enemy.shoot()

            if collide(enemy, player):
                player.health -= 10
                enemies.remove(enemy)
            elif enemy.y + enemy.get_height() > screen_height:
                lives -= 1
                enemies.remove(enemy)

        player.move_bullets(-laser_vel, enemies)
        if score > int(highscore):
            highscore = score



        for powerup in powerups[:]:
            powerup.move(powerup_vel)
            powerup.move_bullets(laser_vel, player)

            #if random.randrange(0, 2 * 60) == 1:
                #   powerup.shoot()

            if collide(powerup, player):
                player.health += 10
                powerups.remove(powerup)
                if player.max_health and lives < 5:
                    lives += 1

        #player.move_bullets(-laser_vel, powerups)



def easy():
    running = True
    fps = 80

    level = 0
    lives = 5

    main_font = pygame.font.SysFont("comicsans", 30)
    lost_font = pygame.font.SysFont("comicsans", 70)

    # this will store where all our enemies are.
    enemies = []
    wave_length = 5
    enemy_vel = 1
    player_vel = 10
    player = Player(380, 670)

    laser_vel = 5

    lost = False
    lost_count = 0

    clock = pygame.time.Clock()

    def draw_window():
        screen.blit(easy_bg, (0, 0))

        # draw text labels
        lives_label = main_font.render(f"lives : {lives}", 1, (153, 0, 76))
        level_label = main_font.render(f"level : {level}", 1, (153, 0, 76))

        # to blit these labels on screen
        screen.blit(lives_label, (10, 10))
        screen.blit(level_label, (screen_width - level_label.get_width() - 20, 10))

        for enemy in enemies:
            enemy.draw(screen)

        player.draw(screen)

        if lost:
            lost_label = lost_font.render("You Lost!!", 1, (255, 255, 255))
            screen.blit(lost_label, (screen_width / 2 - lost_label.get_width() / 2, 350))

        pygame.display.update()

    while running:
        clock.tick(fps)
        draw_window()

        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > fps * 3:
                running = False
            else:
                continue

        if not enemies:
            level += 1
            wave_length += 5
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, screen_width - 100), random.randrange(-1230, -100),
                                random.choice(["red", "green", "blue"]))  # [red, green]
                enemies.append(enemy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        # return a dictionary of ALL keys and tell whether that keys are pressed or not at the current time
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - player_vel > 0:  # left
            player.x -= player_vel
        if keys[pygame.K_RIGHT] and player.x + player_vel + player.get_width() < screen_width:  # right
            player.x += player_vel
        if keys[pygame.K_UP] and player.y - player_vel > 0:  # up
            player.y -= player_vel
        if keys[pygame.K_DOWN] and player.y + player_vel + player.get_height() < screen_height:  # down
            player.y += player_vel
        if keys[pygame.K_SPACE]:
            player.shoot()

        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_bullets(laser_vel, player)

            if random.randrange(0, 2 * 60) == 1:
                enemy.shoot()

            if collide(enemy, player):
                player.health -= 10
                enemies.remove(enemy)

            elif enemy.y + enemy.get_height() > screen_height:
                lives -= 1
                enemies.remove(enemy)

        player.move_bullets(-laser_vel, enemies)


def medium():
    running = True
    fps = 80

    level = 0
    lives = 5

    main_font = pygame.font.SysFont("comicsans", 30)
    lost_font = pygame.font.SysFont("comicsans", 70)

    # this will store where all our enemies are.
    enemies = []
    wave_length = 5
    enemy_vel = 1
    player_vel = 10
    player = Player(380, 670)

    laser_vel = 5

    lost = False
    lost_count = 0

    clock = pygame.time.Clock()

    def draw_window():
        screen.blit(medium_bg, (0, 0))

        # draw text labels
        lives_label = main_font.render(f"lives : {lives}", 1, (255, 255, 255))
        level_label = main_font.render(f"level : {level}", 1, (255, 255, 255))

        # to blit these labels on screen
        screen.blit(lives_label, (10, 10))
        screen.blit(level_label, (screen_width - level_label.get_width() - 20, 10))

        for enemy in enemies:
            enemy.draw(screen)

        player.draw(screen)

        if lost:
            lost_label = lost_font.render("You Lost!!", 1, (255, 255, 255))
            screen.blit(lost_label, (screen_width / 2 - lost_label.get_width() / 2, 350))

        pygame.display.update()

    while running:
        clock.tick(fps)
        draw_window()

        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > fps * 3:
                running = False
            else:
                continue

        if len(enemies) == 0:
            level += 1
            wave_length += 5
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, screen_width - 100), random.randrange(-1230, -100),
                              random.choice(["red", "green", "blue", "yellow"]))  # [red, green]
                enemies.append(enemy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        # return a dictionary of ALL keys and tell whether that keys are pressed or not at the current time
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - player_vel > 0:  # left
            player.x -= player_vel
        if keys[pygame.K_RIGHT] and player.x + player_vel + player.get_width() < screen_width:  # right
            player.x += player_vel
        if keys[pygame.K_UP] and player.y - player_vel > 0:  # up
            player.y -= player_vel
        if keys[pygame.K_DOWN] and player.y + player_vel + player.get_height() < screen_height:  # down
            player.y += player_vel
        if keys[pygame.K_SPACE]:
            player.shoot()

        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_bullets(laser_vel, player)

            if random.randrange(0, 2 * 60) == 1:
                enemy.shoot()

            if collide(enemy, player):
                player.health -= 10
                enemies.remove(enemy)

            elif enemy.y + enemy.get_height() > screen_height:
                lives -= 1
                enemies.remove(enemy)

        player.move_bullets(-laser_vel, enemies)


def hard():
    running = True
    fps = 80

    level = 0
    lives = 5

    main_font = pygame.font.SysFont("comicsans", 30)
    lost_font = pygame.font.SysFont("comicsans", 70)

    # this will store where all our enemies are.
    enemies = []
    wave_length = 5
    enemy_vel = 2
    player_vel = 10
    player = Player(380, 670)

    laser_vel = 5

    lost = False
    lost_count = 0

    clock = pygame.time.Clock()

    def draw_window():
        screen.blit(bg, (0, 0))

        # draw text labels
        lives_label = main_font.render(f"lives : {lives}", 1, (255, 255, 255))
        level_label = main_font.render(f"level : {level}", 1, (255, 255, 255))

        # to blit these labels on screen
        screen.blit(lives_label, (10, 10))
        screen.blit(level_label, (screen_width - level_label.get_width() - 20, 10))

        for enemy in enemies:
            enemy.draw(screen)

        player.draw(screen)

        if lost:
            lost_label = lost_font.render("You Lost!!", 1, (255, 255, 255))
            screen.blit(lost_label, (screen_width / 2 - lost_label.get_width() / 2, 350))

        pygame.display.update()

    while running:
        clock.tick(fps)
        draw_window()

        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > fps * 3:
                running = False
            else:
                continue

        if not enemies:
            level += 1
            wave_length += 5
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, screen_width - 100), random.randrange(-1230, -100),
                                random.choice(["red", "green", "blue", "yellow"]))  # [red, green]
                enemies.append(enemy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        # return a dictionary of ALL keys and tell whether that keys are pressed or not at the current time
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - player_vel > 0:  # left
            player.x -= player_vel
        if keys[pygame.K_RIGHT] and player.x + player_vel + player.get_width() < screen_width:  # right
            player.x += player_vel
        if keys[pygame.K_UP] and player.y - player_vel > 0:  # up
            player.y -= player_vel
        if keys[pygame.K_DOWN] and player.y + player_vel + player.get_height() < screen_height:  # down
            player.y += player_vel
        if keys[pygame.K_SPACE]:
            player.shoot()

        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_bullets(laser_vel, player)

            if random.randrange(0, 2 * 60) == 1:
                enemy.shoot()

            if collide(enemy, player):
                player.health -= 10
                enemies.remove(enemy)

            elif enemy.y + enemy.get_height() > screen_height:
                lives -= 1
                enemies.remove(enemy)

        player.move_bullets(-laser_vel, enemies)


def stagebased():
    exit_game = True
    while exit_game:

        screen.fill(blue)
        screen.blit(stage_bg, (0, 0))
        text_screen("DIFFICULTY LEVELS", magenta, 220, 130)
        text_screen("Easy", black, 150, 490)
        text_screen("Medium", black, 330, 490)
        text_screen("Hard", black, 550, 490)
        text_screen("Press 'SPACE BAR' For Main Menu", magenta, 120, 600)
        easybtn(easy_X, easy_Y)
        mediumbtn(medium_X, medium_Y)
        hardbtn(hard_X, hard_Y)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                welcome()

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Get the Mouse position
                pos = pygame.mouse.get_pos()
                if (pos >= (150, 400)) and (pos <= (214, 500)):
                    easy()
                if (pos >= (350, 400)) and (pos <= (414, 500)):
                    medium()
                if (pos >= (560, 400)) and (pos <= (624, 500)):
                    hard()

        pygame.display.update()
        clock.tick(60)

    pygame.quit()




# Welcome Screen
def welcome():
    exit_game = True
    while exit_game:

        screen.fill(blue)
        screen.blit(welcome_bg, (0, 0))
        text_screen("OCEAN SHOOTER COMBAT GAME", magenta, 80, 100)
        #text_screen("Stage Based/ Highscore Based", pink, 120, 280)
        stagebtn(stagebtn_X, stagebtn_Y)
        highscorebtn(highscorebtn_X, highscorebtn_Y)
        text_screen("staged", black, 170, 460)
        text_screen("high scored", black, 340, 380)
        text_screen("multiplayer", black, 530, 450)
        text_screen("2 players", black, 1, 330)
        text_screen("quit !", black, 700, 600)
        multiplayerbtn(multiplayer_X, multiplayer_Y)
        multiplayerbtng(multiplayerg_X, multiplayerg_Y)
        quitbtn(quit_X, quit_Y)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Get the Mouse position
                pos = pygame.mouse.get_pos()
                if (pos >= (170, 300)) and (pos <= (270, 460)):
                    stagebased()
                if (pos >= (340, 280)) and (pos <= (440, 380)):
                    highscores()
                if (pos >= (1, 230)) and (pos <= (100, 330)):
                    multiplayerg()
                if (pos >= (550, 350)) and (pos <= (650, 450)):
                #     # multiplayer()
                    connect()
                if (pos >= (700, 400)) and (pos <= (784, 600)):
                    exit_game = True
                    pygame.quit()
                    quit()

        pygame.display.update()
        clock.tick(60)

    pygame.quit()

if __name__=='__main__':
    welcome()

