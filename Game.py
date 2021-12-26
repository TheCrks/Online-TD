from random import randint
import pygame

class kareEnemy:
    def __init__(self, health, name, x, y,  color, width, height):
        self.name = name
        self.health = health
        self.x = x
        self.y = y
        self.color = color
        self.width = width
        self.height = height

    def draw(self, window):
        pygame.draw.rect(window, self.color, pygame.Rect(self.x, self.y, self.width, self.height))
        pygame.display.update()

    def move(self, x, y):
        self.x = x
        self.y = y

    def getX(self):
        return self.x
    def getY(self):
        return self.y


class ucgenEnemy:
    def __init__(self, health, name, x, y, color):
        self.name = name
        self.health = health
        self.x = x
        self.y = y
        self.color = color

    def draw(self,window):
        pygame.draw.polygon(window,self.color,[(self.x-10, self.y+10),(self.x+10,self.y+10),(self.x,self.y-10)])
        pygame.display.update()

    def move(self, x, y):
        self.x = x
        self.y = y

    def getX(self):
        return self.x
    def getY(self):
        return self.y

class daireEnemy:
    def __init__(self, health, name, x, y, color, radius):
        self.name = name
        self.health = health
        self.x = x
        self.y = y
        self.color = color
        self.radius = radius

    def draw(self, window):

        pygame.draw.circle(window, self.color, (self.x, self.y), self.radius, self.radius)
        pygame.display.update()

    def move(self, x, y):
        self.x = x
        self.y = y

    def getX(self):
        return self.x
    def getY(self):
        return self.y

class game:
    def __init__(self, id):
        self.id = id
        self.ready = False
        self.coordLists = [[300, 0, 0], [300, 30, 1], [300, 60, 2],[300,90,3],[300,120,4]]
        self.coordX = 300
        self.coordY = 120
        self.drawPath()
        self.Enemies = []

    def addEnemy(self, Enemy):
        self.Enemies.append(Enemy)

    def removeEnemy(self, Enemy):
        self.Enemies.remove(Enemy)

    def connected(self):
        return self.ready

    def indexof(self, List, index):
        out = False
        for i in range(0, len(List)):
            if index == List[i]:
                out = True
        return out

    def drawPathDown(self):
        self.coordY += 30
        self.coordLists.append([self.coordX, self.coordY, 3])

    def direction(self):
        if self.coordLists[len(self.coordLists) - 1][0] == self.coordLists[len(self.coordLists) - 2][0]:
            return "Down"
        else:
            if self.coordLists[len(self.coordLists) - 1][0] > self.coordLists[len(self.coordLists) - 2][0]:
                return "Right"
            else:
                return "Left"

    def drawPathRight(self):
        self.coordX += 30
        self.coordLists.append([self.coordX, self.coordY, 3])

    def drawPathLeft(self):
        self.coordX -= 30
        self.coordLists.append([self.coordX, self.coordY, 3])

    def turnChance(self, percent):
        number = randint(0, 100)
        randomList = []
        for i in range(0, percent):
            randomList.append(randint(0, 100))
        if self.indexof(randomList, number):
            return True
        else:
            return False

    def turnDown(self):
        turn = False
        if self.coordLists[len(self.coordLists) - 1][0] <= 120 or self.coordLists[len(self.coordLists) - 1][
            0] >= 600 - 120:
            turn = True
        if self.coordLists[len(self.coordLists) - 1][1] == self.coordLists[len(self.coordLists) - 2][1] == \
                self.coordLists[len(self.coordLists) - 3][1]:
            turn = self.turnChance(60)
        elif self.coordLists[len(self.coordLists) - 1][1] == self.coordLists[len(self.coordLists) - 2][1] != \
                self.coordLists[len(self.coordLists) - 3][1]:
            turn = self.turnChance(30)
        else:
            turn = False
        return turn

    def turnRL(self):
        turn = False
        if self.coordLists[len(self.coordLists) - 1][0] == self.coordLists[len(self.coordLists) - 2][0] == \
                self.coordLists[len(self.coordLists) - 3][0] == \
                self.coordLists[len(self.coordLists) - 4][0]:
            turn = self.turnChance(50)
        elif self.coordLists[len(self.coordLists) - 1][0] == self.coordLists[len(self.coordLists) - 2][0] == \
                self.coordLists[len(self.coordLists) - 3][
                    0] != self.coordLists[len(self.coordLists) - 4][0]:
            turn = self.turnChance(20)
        else:
            turn = False
        return turn

    def drawPath(self):
        counter = 3
        run = True
        self.drawPathDown()
        while run:
            if self.direction() == "Down":
                if self.turnRL():
                    if self.coordLists[len(self.coordLists) - 1][0] >= 600 - 240:
                        if self.turnChance(60):
                            self.drawPathLeft()
                        else:
                            self.drawPathRight()
                    elif self.coordLists[len(self.coordLists) - 1][0] >= 600 - 120:
                        if self.turnChance(80):
                            self.drawPathLeft()
                        else:
                            self.drawPathRight()
                    elif self.coordLists[len(self.coordLists) - 1][0] >= 600 - 90:
                        if self.turnChance(90):
                            self.drawPathLeft()
                        else:
                            self.drawPathRight()
                    elif self.coordLists[len(self.coordLists) - 1][0] <= 240:
                        if self.turnChance(60):
                            self.drawPathLeft()
                        else:
                            self.drawPathRight()
                    elif self.coordLists[len(self.coordLists) - 1][0] <= 120:
                        if self.turnChance(80):
                            self.drawPathLeft()
                        else:
                            self.drawPathRight()
                    elif self.coordLists[len(self.coordLists) - 1][0] <= 90:
                        if self.turnChance(90):
                            self.drawPathLeft()
                        else:
                            self.drawPathRight()
                    else:
                        if self.turnChance(50):
                            self.drawPathLeft()
                        else:
                            self.drawPathRight()
                else:
                    self.drawPathDown()
            elif self.direction() == "Left":
                if self.coordLists[len(self.coordLists) - 1][0] <= 90:
                    self.drawPathDown()
                else:
                    if self.turnDown():
                        self.drawPathDown()
                    else:
                        self.drawPathLeft()

            else:
                if self.coordLists[len(self.coordLists) - 1][0] >= 600 - 90:
                    self.drawPathDown()
                else:
                    if self.turnDown():
                        self.drawPathDown()
                    else:
                        self.drawPathRight()
            counter += 1
            if self.coordLists[counter][1] >= 730:
                run = False
