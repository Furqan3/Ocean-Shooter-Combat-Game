import pygame
import random
from pygame import mixer
import socket
import threading
import sys

IP = 0
Port= 0


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
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))

# Sound
mixer.music.load("background.mp3")
mixer.music.play(-1)

# Set the caption
pygame.display.set_caption("Ocean Shooter Combat Game")

# Set the icon
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

# player/submarine image
submarine = pygame.image.load("ship1.png")
submarine_two = pygame.image.load("ship1.png")

# bullet image
bullet = pygame.image.load("bullet.png")
bullet_two = pygame.image.load("bullet.png")

# enemy images
sharkLeft = pygame.image.load("shark.png")
sharkRight = pygame.image.load("shark2.png")
sharkMidlle = pygame.image.load("shark3.png")
stone = pygame.image.load("stone.png")
minifish = pygame.image.load("minifish.png")
mini = pygame.image.load("minifish2.png")
stoneOne = pygame.image.load("stone1.png")
stoneTwo = pygame.image.load("stone2.png")

# background images
bg = pygame.transform.scale(pygame.image.load("bbgg.jpg"), (screen_width, screen_height))
welcome_bg = pygame.transform.scale(pygame.image.load("wcbg.jpg"), (screen_width, screen_height))
stage_bg = pygame.transform.scale(pygame.image.load("wall1.jpg"), (screen_width, screen_height))
easy_bg = pygame.transform.scale(pygame.image.load("easy.jpg"), (screen_width, screen_height))
medium_bg = pygame.transform.scale(pygame.image.load("medium.jpg"), (screen_width, screen_height))

# Powerup images
healthpowerup = pygame.image.load("health.png")
livespowerup = pygame.image.load("lives.png")

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
easy_btn = pygame.image.load("easy.png").convert_alpha()
easy_X = 150
easy_Y = 400

medium_btn = pygame.image.load("medium.png").convert_alpha()
medium_X = 350
medium_Y = 400

hard_btn = pygame.image.load("hard.png").convert_alpha()
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
        return not (self.y <= height and self.y >= 0)

    def collision(self, obj):
        return collide(self, obj)


# for 1 player
class Ship:
    CoolDown = 30

    def __init__(self, x, y, health=100):
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
                explosionSound = mixer.Sound("explosion.wav")
                explosionSound.play()
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
            bulletSound = mixer.Sound("laser.wav")
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
                        explosion = mixer.Sound("explo.wav")
                        explosion.play()
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
##############################################################################################################

def send_screen_to_client(client_socket):
    # Initialize Pygame
    pygame.init()

    # Get the screen surface
    screen = pygame.display.get_surface()

    # Convert the screen surface to a bytes object
    screen_bytes = pygame.image.tostring(screen, 'RGB')

    # Send the screen bytes to the client
    client_socket.sendall(screen_bytes)

##############################################################################################################
def Connect_Creat_room():
    running = True
    fps = 80
    main_font = pygame.font.SysFont("comicsans", 30)

    default_port = "8080"

    # Get the system's IP address
    hostname = socket.gethostname()
    IP = socket.gethostbyname(hostname)

    # Create a server socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((IP, int(default_port)))

    def draw_window():
        screen.blit(bg, (0, 0))

        # Draw the IP label and value
        ip_label = main_font.render(f"IP: {IP}", 1, (0, 0, 0))
        screen.blit(ip_label, (100, 100))

        # Draw the default port label and value
        port_label = main_font.render(f"Port: {default_port}", 1, (0, 0, 0))
        screen.blit(port_label, (100, 200))

        # Draw the "Waiting..." label in the center of the window
        waiting_label = main_font.render("Waiting...", 1, (0, 0, 0))
        screen.blit(waiting_label, (300, 300))

        pygame.display.update()

    while running:
        clock.tick(fps)
        draw_window()

        # Listen for a connection
        server_socket.listen(1)

        # Accept the connection and return None
        conn, addr = server_socket.accept()
        print(f"Connected to {addr}")
        return None
    


#############################################################################################################

ip_input = pygame.Rect(100, 150, 200, 50)
port_input = pygame.Rect(100, 250, 200, 50)
proceed_button = pygame.Rect(130, 350, 140, 50)

def convert_ip(ip_string):
    # Allow input with dots
    if len(ip_string) > 15:
        return None

    # Split the input string by dots and validate each octet
    octets = ip_string.split('.')
    if len(octets) != 4:
        return None
    for octet in octets:
        if not octet.isdigit() or int(octet) < 0 or int(octet) > 255:
            return None
    
    return '.'.join(octets)
def convert_port(port_string):
    try:
        port = int(port_string)
        return None if port < 0 or port > 65535 else port
    except ValueError:
        return None
def Connect_existance_room():
    running = True
    fps = 80
    main_font = pygame.font.SysFont("comicsans", 30)
    ip_font = pygame.font.SysFont("comicsans", 20)
    port_font = pygame.font.SysFont("comicsans", 20)
    input_ip = ""
    input_port = ""

    def draw_window():
        screen.blit(bg, (0, 0))

        # Draw the input fields and labels
        pygame.draw.rect(screen, (255, 255, 255), ip_input)
        pygame.draw.rect(screen, (255, 255, 255), port_input)
        ip_label = main_font.render("Enter IP:", 1, (0, 0, 0))
        screen.blit(ip_label, (100, 100))
        port_label = main_font.render("Enter Port:", 1, (0, 0, 0))
        screen.blit(port_label, (100, 200))
        ip_text = ip_font.render(input_ip, 1, (0, 0, 0))
        screen.blit(ip_text, (110, 165))
        port_text = port_font.render(input_port, 1, (0, 0, 0))
        screen.blit(port_text, (110, 265))

        # Draw the Proceed button
        pygame.draw.rect(screen, (0, 255, 0), proceed_button)
        proceed_label = main_font.render("Proceed", 1, (255, 255, 255))
        screen.blit(proceed_label, (145, 360))

        pygame.display.update()

    while running:
        clock.tick(fps)
        draw_window()

        # Event loop for mouse clicks and keyboard input
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                if proceed_button.collidepoint(pos):
                    input_ip = convert_ip(input_ip)
                    IP = input_ip
                    input_port = convert_port(input_port)
                    Port = input_port
                    print("Entered IP:", input_ip)
                    print("Entered Port:", input_port)
                    try:
                        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        client_socket.connect((IP, Port))
                        print("Connection successful!")
                        return None
                    except Exception as e:
                        print("Connection failed:", e)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    if ip_input.collidepoint(pygame.mouse.get_pos()):
                        input_ip = input_ip[:-1]
                    elif port_input.collidepoint(pygame.mouse.get_pos()):
                        input_port = input_port[:-1]
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        if ip_input.collidepoint(pygame.mouse.get_pos()):
                            input_ip = input_ip[:-1]
                        elif port_input.collidepoint(pygame.mouse.get_pos()):
                            input_port = input_port[:-1]
                    elif event.unicode.isnumeric():
                        if ip_input.collidepoint(pygame.mouse.get_pos()) and len(input_ip) < 15:
                            input_ip += event.unicode
                        elif port_input.collidepoint(pygame.mouse.get_pos()) and len(input_port) < 5:
                            input_port += event.unicode
                    elif event.unicode == '.':
                        if ip_input.collidepoint(pygame.mouse.get_pos()) and len(input_ip) < 15:
                            input_ip += event.unicode


##############################################################################################################################################################################
# Define buttons as global variables
create_button = pygame.Rect(100, 150, 210, 50)
connect_button = pygame.Rect(100, 250, 210, 50)

def connect_window():
    running = True
    fps = 80
    main_font = pygame.font.SysFont("comicsans", 30)
    def draw_window():
        screen.blit(bg, (0, 0))

        # Draw the buttons
        pygame.draw.rect(screen, (0, 255, 0), create_button)
        create_label = main_font.render("Create Room", 1, (255, 255, 255))
        screen.blit(create_label, (110, 160))
        pygame.draw.rect(screen, (0, 255, 0), connect_button)
        connect_label = main_font.render("Connect Room", 1, (255, 255, 255))
        screen.blit(connect_label, (110, 260))

        pygame.display.update()

    while running:
        clock.tick(fps)
        draw_window()

        # Event loop for mouse clicks
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                if create_button.collidepoint(pos):
                    print("Create Room button clicked")
                    Connect_Creat_room()
                    return None
                elif connect_button.collidepoint(pos):
                    
                    print("Connect Room button clicked")
                    Connect_existance_room()
                    return None

########################################################################################################################


def multiplayer():
    
    running = True
    fps = 80

    level = 0
    lives = 5

    main_font = pygame.font.SysFont("comicsans", 30)
    lost_font = pygame.font.SysFont("comicsans", 70)

    enemies = []
    wave_length = 5
    enemy_vel = 1

    player_vel = 7
    user_vel = 7
    laser_vel = 7
    player = Player(80, 650)
    ship_one = user(650, 650)


    lost = False
    lost_count = 0

    global score
    score = 0
    clock = pygame.time.Clock()

    def draw_window():
        screen.blit(bg, (0, 0))

        # draw text labels
        lives_label = main_font.render(f"lives : {lives}", 1, (255, 255, 255))
        level_label = main_font.render(f"level : {level}", 1, (255, 255, 255))
        score_label = main_font.render(f"score : {score}", 1, (255, 255, 255))

        screen.blit(lives_label, (10, 10))
        screen.blit(level_label, (screen_width - level_label.get_width() - 20, 10))
        screen.blit(score_label, (screen_width - score_label.get_width() - 20, 50))

        for enemy in enemies:
            enemy.draw(screen)

        if multiplayer:  # Display lives left & players
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

        if multiplayer:
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

        if len(enemies) == 0:
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

        if len(enemies) == 0:
            level += 1
            wave_length += 5
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, screen_width - 100), random.randrange(-1230, -100),
                                random.choice(["red", "green", "yellow"]))  # [red, green]
                enemies.append(enemy)


        if len(powerups) == 0:
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

        if len(enemies) == 0:
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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
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
        # text_screen("Stage Based/ Highscore Based", pink, 120, 280)
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
                    connect_window()
                    multiplayer()
                if (pos >= (720, 20)) and (pos <= (784, 84)):
                    exit_game = True
                    pygame.quit()
                    quit()

        pygame.display.update()
        clock.tick(60)

    pygame.quit()


welcome()
