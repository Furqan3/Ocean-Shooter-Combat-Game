import pygame
import pygame
import random
import threading
from main import *
import time


def multiplayer(soc):
    running = True
    fps = 80

    level = 0
    lives = 1000

    main_font = pygame.font.SysFont("comicsans", 30)
    lost_font = pygame.font.SysFont("comicsans", 70)
    font = pygame.font.SysFont("arial", 30)
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

    input_text = ""
    user_input = "" 

    global score
    score = 0
    textbox_rect = pygame.Rect(50, 50, 400, 50)
    send_button_rect = pygame.Rect(460, 50, 80, 50)
    #audio_button_rect = pygame.Rect(560, 50, 80, 50)
    def draw_window():
        screen.blit(bg, (0, 0))
        # draw text labels
        text_message = ""
        with open("textmessage.txt", "r") as file:
            text_message = file.read()
        text_message=text_message.replace("\n","")
        lives_label = main_font.render(f"lives : {lives}", 1, (255, 255, 255))
        score_label = main_font.render(f"score : {score}", 1, (255, 255, 255))
        message = main_font.render("Message", 1, (255, 255, 255))
        level_label = main_font.render(f"level : {level}", 1, (255, 255, 255))
        text = main_font.render(f"Message : {text_message}", 1, (255, 255, 255))
        
        screen.blit(text, (100, 100))
        screen.blit(lives_label, (10, 10))
        screen.blit(message, (370, 10))
        screen.blit(level_label, (screen_width - level_label.get_width() - 20, 10))
        screen.blit(score_label, (screen_width - score_label.get_width() - 20, 50))
        pygame.draw.rect(screen, (255, 255, 255), textbox_rect, 2)
        pygame.draw.rect(screen, (0, 255, 0), send_button_rect)
        #pygame.draw.rect(screen, (0, 255, 0), audio_button_rect)
        send_text = font.render("Send", True, (255, 255, 255))
        #audio_text = font.render("Audio", True, (255, 255, 255))
        screen.blit(send_text, send_button_rect.move(10, 10))
        #screen.blit(audio_text, audio_button_rect.move(10, 10))

        # Draw input text in textbox
        text_surface = font.render(input_text, True, (0, 0, 0))
        screen.blit(text_surface, textbox_rect.move(5, 5))

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
        t2=threading.Thread(target=soc.recive_text)
        t2.start()
        t2.join()
        if pygame.mouse.get_pressed()[0]:
            mouse_pos = pygame.mouse.get_pos()
            if send_button_rect.collidepoint(mouse_pos):
                user_input = input_text
                soc.send_text(user_input)
            
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
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                elif event.key == pygame.K_RETURN:
                    user_input = input_text
                    input_text = ""
                else:
                    input_text += event.unicode
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
        
        
        
if __name__ == "__main__":
    print("hello")