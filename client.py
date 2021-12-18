import pygame
from network import network
pygame.font.init()


width = 700
height = 700
clientNumber = 0
backgroundColourRed = (255, 50, 50)
backgroundColourBlue = (0, 0, 255)

window = pygame.display.set_mode((width, height))
pygame.display.set_caption("R-P-S Online")

class Button:
    def __init__(self, text, x, y, colour):
        self.text = text
        self.x = x
        self.y = y
        self.colour = colour
        self.width = 150
        self.height = 100

    def draw(self,win):
        pygame.draw.rect(win, self.colour, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("comicsans", 20)
        text = font.render(self.text, 1, (255,255,255))
        win.blit(text, (self.x + round(self.width/2)-round(text.get_width()/2),self.y + round(self.height/2)-round(text.get_height()/2)))


    def click(self, pos):
        x1= pos[0]
        y1=pos[1]

        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False




def redrawWindow(win, game, player):
    win.fill(backgroundColourBlue)

    if not(game.connected()):
        font= pygame.font.SysFont("comicsans",30)
        text = font.render("Waiting for player...",1,(255,0,0),True)
        win.blit(text, (width/2 - text.get_width()/2,height/2 - text.get_height()/2))
    else:
        font= pygame.font.SysFont("comicsans",15)
        text = font.render("Your Move",1, (0,255,255))
        win.blit(text,(80,200))

        text = font.render("Opponents Move",1, (0,255,255))
        win.blit(text,(380,200))

        move1 = game.getPlayerMove(0)
        move2 = game.getPlayerMove(1)
        if game.bothWent():
            text1 = font.render(move1, 1 , (0,0,0))
            text2 = font.render(move2, 1 , (0,0,0))
        else:
            if game.p1Went and player==0:
                text1 = font.render(move1,1,(0,0,0))
            elif game.p1Went:
                text1 = font.render("Locked In",1,(0,0,0))
            else:
                text1 = font.render("Waiting...",1, (0,0,0))

            if game.p2Went and player==1:
                text2 = font.render(move2,1,(0,0,0))
            elif game.p2Went:
                text2 = font.render("Locked In",1,(0,0,0))
            else:
                text2 = font.render("Waiting...",1, (0,0,0))

        if player == 1:
            win.blit(text2, (100,350))
            win.blit(text1, (400,350))
        else:
            win.blit(text1, (100, 350))
            win.blit(text2, (400, 350))
        for btn in button:
            btn.draw(win)
    pygame.display.update()


button= [Button("Rock", 50, 500, (0,0,0)), Button("Scisors", 250, 500,(0,0,0)), Button("Paper",450,500,(0,0,0)),Button("Back",250,10,(250,0,0))]
def mainLoop():
    run = True
    clock = pygame.time.Clock()
    n = network()
    player = int(n.getPlayer())
    print("You are player" , player)
    while run:
        clock.tick(60)
        try:
            game = n.send("get")
        except:
            run=False
            print("Cant connect")
            break

        if game.bothWent():
            redrawWindow(window,game,player)
            pygame.time.delay(200)
            try:
                game = n.send("reset")
            except:
                run = False
                print("cant get game")
                break

            font = pygame.font.SysFont("comicsans", 90)
            if (game.winner()==1 and player ==1) or (game.winner()==0 and player == 0):
                text = font.render("You Won!", 1, (255,0,0))
            elif game.winner() ==-1:
                text = font.render("Tie!",1, (255,0,0))
            else:
                text= font. render("You Lost!",1, (255,0,0))


            window.blit(text, (width/2 - text.get_width()/2,height/2 - text.get_height()/2+55))
            pygame.display.update()
            pygame.time.delay(2000)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run=False
                pygame.quit()


            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for btn in button:
                    if btn.click(pos) and game.connected():
                        if player == 0:
                            if not game.p1Went:
                                if not btn.text == "Back":
                                    n.send(btn.text)
                                else:
                                    run=False
                                    break
                        else:
                            if not game.p2Went:
                                if not btn.text == "Back":
                                    n.send(btn.text)
                                else:
                                    run=False
                                    break

        redrawWindow(window, game, player)

def menuScreen(win):
    run = True
    clock = pygame.time.Clock()
    while run:
        clock.tick(60)
        win.fill(backgroundColourRed)
        font = pygame.font.SysFont("comicsans",30)
        text = font.render("Click to Play!",1,(0,0,0))
        win.blit(text,(100,350))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run=False
            if event.type == pygame.MOUSEBUTTONDOWN:
                run=False
            else:
                pass
        pygame.display.update()
    mainLoop()

while True:
    menuScreen(window)



