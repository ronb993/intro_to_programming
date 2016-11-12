from math import *
from turtle import *
from random import *
import turtle
import random
import math

def mainSimulation():
    numberOfBears = 10
    numberOfFish = 10
    numberOfPlants = 10
    worldLifeTime = 2500
    worldWidth = 50
    worldHeight = 25

    myworld = World(worldWidth,worldHeight)
    myworld.draw()

    for i in range(numberOfFish):
        newfish = Fish()
        x = random.randrange(myworld.getMaxX())
        y = random.randrange(myworld.getMaxY())
        while not myworld.emptyLocation(x,y):
            x = random.randrange(myworld.getMaxX())
            y = random.randrange(myworld.getMaxY())
        myworld.addThing(newfish,x,y)

    for i in range(numberOfBears):
        newbear = Bear()
        x = random.randrange(myworld.getMaxX())
        y = random.randrange(myworld.getMaxY())
        while not myworld.emptyLocation(x,y):
            x = random.randrange(myworld.getMaxX())
            y = random.randrange(myworld.getMaxY())
        myworld.addThing(newbear,x,y)

    for i in range(numberOfPlants):
        newplant = Plant()
        x = random.randrange(myworld.getMaxX())
        y = random.randrange(myworld.getMaxY())
        while not myworld.emptyLocation(x,y):
            x = random.randrange(myworld.getMaxX())
            y = random.randrange(myworld.getMaxY())
        myworld.addThing(newplant,x,y)

    for i in range(worldLifeTime):
        myworld.liveALittle()


    myworld.freezeWorld()


############THIS IS THE WORLD CLASS################

class World:
    def __init__(self,mx,my):
        self.maxX = mx
        self.maxY = my
        self.thingList = []
        self.grid = []
        
        for arow in range(self.maxY):
            row=[]
            for acol in range (self.maxX):
                row.append(None)
            self.grid.append(row)

        self.wturtle = turtle.Turtle()
        self.wscreen = turtle.Screen()
        self.wscreen.setworldcoordinates(0,0,self.maxX-1,self.maxY-1)
        self.wscreen.addshape("Bear.gif")
        self.wscreen.addshape("Fish.gif")
        self.wscreen.addshape("Plant.gif") 
        self.wturtle.hideturtle()

    def draw(self):
        self.wscreen.tracer(0)
        self.wturtle.forward(self.maxX-1)
        self.wturtle.left(90)
        self.wturtle.forward(self.maxY-1)
        self.wturtle.left(90)
        self.wturtle.forward(self.maxX-1)
        self.wturtle.left(90)
        self.wturtle.forward(self.maxY-1)
        self.wturtle.left(90)
        for i in range(self.maxY-1):
            self.wturtle.forward(self.maxX-1)
            self.wturtle.backward(self.maxX-1)
            self.wturtle.left(90)
            self.wturtle.forward(1)
            self.wturtle.right(90)
        self.wturtle.forward(1)
        self.wturtle.right(90)
        for i in range(self.maxX-2):
            self.wturtle.forward(self.maxY-1)
            self.wturtle.backward(self.maxY-1)
            self.wturtle.left(90)
            self.wturtle.forward(1)
            self.wturtle.right(90)
        self.wscreen.tracer(1)
        
    
        
    def freezeWorld(self):
        self.wscreen.exitonclick()
        
    def addThing(self,athing,x,y):
        athing.setX(x)
        athing.setY(y)
        self.grid[y][x] = athing
        athing.setWorld(self)
        self.thingList.append(athing)
        athing.appear()

    def delThing (self, athing):
        athing.hide()
        self.grid[athing.getY()][athing.getX()] = None
        self.thingList.remove(athing)

    def moveThing(self,oldx,oldy,newx,newy):
        self.grid[newy][newx] = self.grid[oldy][oldx]
        self.grid[oldy][oldx] = None

    def getMaxX(self):
        return self.maxX

    def getMaxY(self):
        return self.maxY

    def liveALittle(self):
        if self.thingList != [ ]:
            athing = random.randrange(len(self.thingList))
            randomthing = self.thingList[athing]
            randomthing.liveALittle()

    def emptyLocation(self,x,y):
        if self.grid[y][x] == None:
            return True
        else:
            return False

    def lookAtLocation(self,x,y):
        return self.grid[y][x]


########This is the Bear Class####################

class Bear:
    def __init__(self):
        self.turtle=turtle.Turtle()
        self.turtle.up()
        self.turtle.hideturtle()
        self.turtle.shape("Bear.gif")

        self.xpos=0
        self.ypos=0
        self.world=None

        self.starveTick=0
        self.breedTick=0
        
    def setX(self, newx):
        self.xpos = newx

    def setY(self, newy):
        self.ypos = newy

    def getX(self):
        return self.xpos

    def getY(self):
        return self.ypos

    def setWorld(self, aworld):
        self.world = aworld

    def appear(self):
        self.turtle.goto(self.xpos, self.ypos)
        self.turtle.showturtle()

    def hide(self):
        self.turtle.hideturtle()

    def move(self, newx, newy):
        self.world.moveThing(self.xpos, self.ypos, newx, newy)
        self.xpos = newx
        self.ypos = newy
        self.turtle.goto(self.xpos, self.ypos)

        
    def liveALittle(self):
        self.breedTick = self.breedTick + 1
        if self.breedTick >= 8:
            self.tryToBreed()

        self.tryToEat()

        if self.starveTick == 10:
            self.world.delThing(self)
        else:
            self.tryToMove()
            
    def tryToMove(self):
        offsetList = [(-1,1) ,(0,1) ,(1,1),
                      (-1,0)        ,(1,0),
                      (-1,-1),(0,-1),(1,-1)]
        randomOffsetIndex = random.randrange(len(offsetList))
        randomOffset = offsetList[randomOffsetIndex]
        nextx=self.xpos + randomOffset[0]
        nexty=self.ypos + randomOffset[1]
        while not(0 <= nextx < self.world.getMaxX() and
                  0 <= nexty < self.world.getMaxY() ):
            randomOffsetIndex = random.randrange(len(offsetList))
            randomOffset = offsetList[randomOffsetIndex]
            nextx=self.xpos + randomOffset[0]
            nexty=self.ypos + randomOffset[1]

        if self.world.emptyLocation(nextx,nexty):
            self.move(nextx,nexty)


    def tryToBreed(self):
        offsetList = [(-1, 1), (0, 1), (1, 1),
                      (-1, 0)        , (1, 0),
                      (-1, -1), (0, -1), (1, -1)]
        randomOffsetIndex = random.randrange(len(offsetList))
        randomOffset = offsetList[randomOffsetIndex]
        nextx = self.xpos + randomOffset[0]
        nexty = self.ypos + randomOffset[1]
        while not(0 <= nextx < self.world.getMaxX() and 0 <= nexty < self.world.getMaxY()):
            randomOffsetIndex = random.randrange(len(offsetList))
            randomOffset = offsetList[randomOffsetIndex]
            nextx = self.xpos + randomOffset[0]
            nexty = self.ypos + randomOffset[1]

        if self.world.emptyLocation(nextx, nexty):
            childThing = Bear()
            self.world.addThing(childThing, nextx, nexty)
            self.breedTick = 0
            


    def tryToEat(self):
        offsetList = [(-1,1) ,(0,1) ,(1,1),
                      (-1,0)        ,(1,0),
                      (-1,-1),(0,-1),(1,-1)]
        adjprey = []
        for offset in offsetList:
            newx = self.xpos + offset[0]
            newy = self.ypos + offset[1]
            if 0 <= newx < self.world.getMaxX() and 0 <= newy < self.world.getMaxY():
                if (not self.world.emptyLocation(newx,newy)) and isinstance(self.world.lookAtLocation(newx,newy),Fish):
                    adjprey.append(self.world.lookAtLocation(newx,newy))

        if len(adjprey)>0:
            randomprey = adjprey[random.randrange(len(adjprey))]
            preyx = randomprey.getX()
            preyy = randomprey.getY()

            self.world.delThing(randomprey)
            self.move(preyx,preyy)
            self.starveTrick = 0

        else:
            self.starveTick = self.starveTick + 1


################This is the CLass Fish################
class Fish:
    def __init__(self):
        self.turtle = turtle.Turtle()
        self.turtle.up()
        self.turtle.hideturtle()
        self.turtle.shape("Fish.gif")

        self.xpos = 0
        self.ypos = 0
        self.world = None

        self.breedTick = 0

    def setX(self, newx):
        self.xpos  = newx

    def setY(self, newy):
        self.ypos = newy

    def getX(self):
        return self.xpos

    def getY(self):
        return self.ypos

    def setWorld(self, aworld):
        self.world = aworld

    def appear(self):
        self.turtle.goto(self.xpos, self.ypos)
        self.turtle.showturtle()

    def hide(self):
        self.turtle.hideturtle()

    def move(self, newx, newy):
        self.world.moveThing(self.xpos, self.ypos, newx, newy)
        self.xpos = newx
        self.ypos = newy
        self.turtle.goto(self.xpos, self.ypos)

    def liveALittle(self):
        offsetList = [(-1, 1), (0, 1), (1, 1),
                      (-1, 0)        , (1, 0),
                      (-1, -1), (0, -1), (1, -1)]
        adjfish = 0
        for offset in offsetList:
            newx = self.xpos + offset[0]
            newy = self.ypos + offset[1]
            if 0 <= newx < self.world.getMaxX() and 0 <= newy < self.world.getMaxY():
                if (not self.world.emptyLocation(newx, newy)) and isinstance(self.world.lookAtLocation(newx, newy), Fish):
                    adjfish = adjfish + 1

        if adjfish >= 2:
            self.world.delThing(self)
        else:
            self.breedTick = self.breedTick + 1
            if self.breedTick >= 12:
                self.tryToBreed()

        self.tryToMove()

    def tryToBreed(self):
        offsetList = [(-1, 1), (0, 1), (1, 1),
                      (-1, 0)        , (1, 0),
                      (-1, -1), (0, -1), (1, -1)]
        randomOffsetIndex = random.randrange(len(offsetList))
        randomOffset = offsetList[randomOffsetIndex]
        nextx = self.xpos + randomOffset[0]
        nexty = self.ypos + randomOffset[1]
        while not(0 <= nextx < self.world.getMaxX() and 0 <= nexty < self.world.getMaxY()):
            randomOffsetIndex = random.randrange(len(offsetList))
            randomOffset = offsetList[randomOffsetIndex]
            nextx = self.xpos + randomOffset[0]
            nexty = self.ypos + randomOffset[1]

        if self.world.emptyLocation(nextx, nexty):
            childThing = Fish()
            self.world.addThing(childThing, nextx, nexty)
            self.breedTick = 0

    def tryToMove(self):
        offsetList = [(-1, 1), (0, 1), (1, 1),
                  (-1, 0)        , (1, 0),
                  (-1, -1), (0, -1), (1, -1)]
        randomOffsetIndex = random.randrange(len(offsetList))
        randomOffset = offsetList[randomOffsetIndex]
        nextx = self.xpos + randomOffset[0]
        nexty = self.ypos + randomOffset[1]
        while not(0 <= nextx < self.world.getMaxX() and 0 <= nexty < self.world.getMaxY()):
            randomOffsetIndex = random.randrange(len(offsetList))
            randomOffset = offsetList[randomOffsetIndex]
            nextx = self.xpos + randomOffset[0]
            nexty = self.ypos + randomOffset[1]

        if self.world.emptyLocation(nextx, nexty):
            self.move(nextx, nexty)

###################This is the Class Plant ######################

class Plant:
    def __init__(self):
        self.turtle = turtle.Turtle()
        self.turtle.up()
        self.turtle.hideturtle()
        self.turtle.shape("Plant.gif")

        self.xpos = 0
        self.ypos = 0
        self.world = None

        self.breedTick = 0

####Accessor and mutators###########

    def setX(self, newx):
        self.xpos = newx

    def setY(self, newy):
        self.ypos = newy

    def getX(self):
        return self.xpos

    def getY(self):
        return self.ypos

    def setWorld(self, aworld):
        self.world = aworld

    def appear(self):
        self.turtle.goto(self.xpos, self.ypos)
        self.turtle.showturtle()

    def hide(self):
        self.turtle.hideturtle()

    def tryToBreed(self):
        offsetList=[(-1,1),(0,1),(1,1),
                    (-1,0)      ,(1,0),
                    (-1,-1),(0,-1),(1,-1)]
        randomOffsetIndex=random.randrange(len(offsetList))
        randomOffset=offsetList[randomOffsetIndex]
        nextx=self.xpos+randomOffset[0]
        nexty=self.ypos+randomOffset[1]
        while not(0<=nextx<self.world.getMaxX()and
                  0<=nexty<self.world.getMaxY() ):
            randomOffsetIndex=random.randrange(len(offsetList))
            randomOffset=offsetList[randomOffsetIndex]
            nextx=self.xpos+randomOffset[0]
            nexty=self.ypos+randomOffset[1]

        if self.world.emptyLocation(nextx,nexty):
            childThing=Plant()
            self.world.addThing(childThing,nextx,nexty)
            self.breedTick=0
        
    def liveALittle(self):
        offsetList = [(-1, 1), (0, 1), (1, 1),
                      (-1, 0)        , (1, 0),
                      (-1, -1), (0, -1), (1, -1)]
        self.breedTick = self.breedTick + 1
        if self.breedTick >= 5:
            self.tryToBreed()
        adjplant = 0
        for offset in offsetList:
            newx = self.xpos + offset[0]
            newy = self.ypos + offset[1]
            if 0 <= newx < self.world.getMaxX() and 0 <= newy < self.world.getMaxY():
               if (not self.world.emptyLocation(newx, newy)) and isinstance(self.world.lookAtLocation(newx, newy), Plant):
                       adjplant = adjplant + 1

        if adjplant >= 2:
            self.world.delThing(self)
        else:
            self.breedTick = self.breedTick + 1
            if self.breedTick >= 12:
                self.tryToBreed()

        
if __name__ == '__main__':
    mainSimulation()
