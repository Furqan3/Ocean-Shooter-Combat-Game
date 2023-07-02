import pygame
import random
from pygame import mixer
from main import *
from creat_server import *
from Connect_server import *
from Multiplayer import *

# write server IP address here
Server_Ip='localhost' 
# write server port here
Server_Port=5000
# write client IP here
Client_Ip='localhost'
# write client port here
Client_Port=5001


def connect():
    str1="Connect to a server"
    str2="Create a server"
    mixer.init()
    # mixer.music.load("Music/background.mp3")
    # mixer.music.play(-1)
    pygame.init()
    screen = pygame.display.set_mode((800, 730))
    screen.fill(blue)
    screen.blit(welcome_bg, (0, 0))
    pygame.display.set_caption("Connect to a server")
    font = pygame.font.SysFont("arial", 30)
    text = font.render(str1, True, (255, 255, 255))
    textRect = text.get_rect()
    textRect.center = (400, 275)
    screen.blit(text, textRect)
    font = pygame.font.SysFont("arial", 30)
    text = font.render(str2, True, (255, 255, 255))
    textRect = text.get_rect()
    textRect.center = (400, 475)
    screen.blit(text, textRect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if 300 + 200 > mouse[0] > 300 and 250 + 50 > mouse[1] > 250:
            pygame.draw.rect(screen, (0, 255, 0), (285, 250, 230, 50))
            font = pygame.font.SysFont("arial", 30)
            text = font.render(str1, True, (0, 0, 0))
            textRect = text.get_rect()
            textRect.center = (400, 275)
            screen.blit(text, textRect)
            if click[0] == 1:
                print("Connect to a server")
                c=client('192.168.18.107',5000)
                multiplayer(c)
                return
        else:
            pygame.draw.rect(screen, (0, 0, 255), (285, 250, 230, 50))
            font = pygame.font.SysFont("arial", 30)
            text = font.render(str1, True, (255, 255, 255))
            textRect = text.get_rect()
            textRect.center = (400, 275)
            screen.blit(text, textRect)
        if 300 + 200 > mouse[0] > 300 and 450 + 50 > mouse[1] > 450:
            pygame.draw.rect(screen, (0, 255, 0), (300, 450, 200, 50))
            font = pygame.font.SysFont("arial", 30)
            text = font.render(str2, True, (0, 0, 0))
            textRect = text.get_rect()
            textRect.center = (400, 475)
            screen.blit(text, textRect)
            if click[0] == 1:
                print("Create a server")
                s=server('192.168.18.70',5000)
                multiplayer(s)
                return
        else:
            pygame.draw.rect(screen, (0, 0, 255), (300, 450, 200, 50))
            font = pygame.font.SysFont("arial", 30)
            text = font.render(str2, True, (255, 255, 255))
            textRect = text.get_rect()
            textRect.center = (400, 475)
            screen.blit(text, textRect)
        pygame.display.update()

if __name__ == '__main__':
    connect()
