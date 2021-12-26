import pygame
from random import randint
import Network
from Network import network

pygame.font.init()

width = 600
height = 730
red = (255, 0, 0)
pathColour = (100, 100, 100)
coordX = width / 2
coordY = 0
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")
coordLists = [[300, 0, 0], [300, 30, 1], [300, 60, 2]]
backgroundColourRed = (255, 50, 50)
backgroundColourBlue = (0, 0, 255)


class Button:
    def __init__(self, text, x, y, colour,width,height):
        self.text = text
        self.x = x
        self.y = y
        self.colour = colour
        self.width = width
        self.height = height

    def draw(self, win):
        pygame.draw.rect(win, self.colour, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("comicsans", 20)
        text = font.render(self.text, 1, (255, 255, 255))
        win.blit(text, (self.x + round(self.width / 2) - round(text.get_width() / 2),
                        self.y + round(self.height / 2) - round(text.get_height() / 2)))

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]

        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False


def redrawWindow(win, game):
    win.fill(backgroundColourBlue)

    if not (game.connected()):
        font = pygame.font.SysFont("comicsans", 30)
        text = font.render("Waiting for player...", 1, (255, 0, 0), True)
        win.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2))
    else:
        win.fill((0, 0, 0))
        for btn in button:
            btn.draw(win)
        for i in game.coordLists:
            pygame.draw.rect(window, pathColour, pygame.Rect(i[0], i[1], 30, 30))
        for i in game.Enemies:
            i.draw(window)

    pygame.display.update()


button = [Button("Back", 10, 10, (250, 0, 0),250,100), Button("Üçgen",400,0,(255,0,0),100,30),Button("Kare",400,35,(0,255,0),100,30),Button("Daire",400,70,(0,0,255),100,30),Button("del",400,105,(0,0,0),100,30)]


def drawBackGround():
    window.fill((255, 255, 255))
    pygame.display.update()


def mainLoop():
    loop = True
    clock = pygame.time.Clock()
    n = network()
    player = int(n.getPlayer())
    print("player : ",player)
    while loop:
        try:
            game = n.sendStr("get")
        except:
            loop = False
            print("Cant connect")
            break
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for btn in button:
                    if btn.click(pos) and game.connected():
                        if btn.text == "Back":
                            loop = False
                            break
                        else :
                            n.sendStr(btn.text)

        redrawWindow(window, game)
        clock.tick(400)
        pygame.display.update()


def menuScreen(win):
    run = True
    clock = pygame.time.Clock()
    while run:
        clock.tick(60)
        win.fill(backgroundColourRed)
        font = pygame.font.SysFont("comicsans", 30)
        text = font.render("Click to Play!", 1, (0, 0, 0))
        win.blit(text, (100, 350))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False
            else:
                pass
        pygame.display.update()
    mainLoop()


while True:
    menuScreen(window)
