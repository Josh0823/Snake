import pygame, sys, random
from pygame.locals import *

#Class that represents onscreen snake
class Snake:
    def __init__(self, xsnake, ysnake, direction, body, size, speed):
        self.xsnake = xsnake
        self.ysnake = ysnake
        self.direction = direction
        self.body = body
        self.size = size
        self.speed = speed

    #Moves the snake based on whether it has eaten food or not
    def move(self, food, screenWidth, screenHeight, display, foodColor, stemColor):
        #If the snake's head and food are in the same location:
        if self.xsnake == food.xfood and self.ysnake == food.yfood:
            #Shifts the body array back one and adds new location to front
            lastSpot = self.body[len(self.body) -1]
            for i in range(len(self.body) - 1, 0, -1):
                self.body[i] = self.body[i-1]
            self.body[0] = (self.xsnake, self.ysnake)
            self.body.append(lastSpot)

            #Increases the speed of the snake by 0.5 fps
            self.speed += 0.25

            #Creates a new food object and displays it to the screen
            food.newFood(self)
            food.drawFood(display, foodColor, stemColor)

        #If the snake has not eaten the food:
        else:
            #Shifts body array to represent new location
            for i in range(len(self.body) - 1, 0, -1):
                self.body[i] = self.body[i-1]
            self.body[0] = (self.xsnake, self.ysnake)

    #Changes the position by 1 unit size based on the direction of the snake
    def updateHeadPosition(self):
        if self.direction == 'right':
            self.xsnake += self.size
        elif self.direction == 'left':
            self.xsnake -= self.size
        elif self.direction == 'down':
            self.ysnake += self.size
        elif self.direction == 'up':
            self.ysnake -= self.size

    #Changes the direction of the snake based on user input
    #Currently supports WASD and arrow keys
    def updateDirection(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.direction = 'down'
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.direction = 'up'
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.direction = 'right'
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.direction = 'left'
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            elif event.type == QUIT:
                pygame.display.quit()
                pygame.quit()
                sys.exit()
                
    #Draws the square the makes up the head of the snake to display surface
    def drawHead(self, display, color, eyeColor, tongueColor):
        pygame.draw.rect(display, color, (self.body[0][0], self.body[0][1], self.size, self.size))
        if self.direction == 'right':
            pygame.draw.rect(display, eyeColor, (self.xsnake+8, self.ysnake+3, 3, 3))
            pygame.draw.rect(display, eyeColor, (self.xsnake+8, self.ysnake+10, 3, 3))
        elif self.direction == 'left':
            pygame.draw.rect(display, eyeColor, (self.xsnake+5, self.ysnake+3, 3, 3))
            pygame.draw.rect(display, eyeColor, (self.xsnake+5, self.ysnake+10, 3, 3))
        elif self.direction == 'up':
            pygame.draw.rect(display, eyeColor, (self.xsnake+3, self.ysnake+5, 3, 3))
            pygame.draw.rect(display, eyeColor, (self.xsnake+10, self.ysnake+5, 3, 3))
            pygame.draw.rect(display, tongueColor, (self.xsnake+7, self.ysnake-1, 2, 4))
        elif self.direction == 'down':
            pygame.draw.rect(display, eyeColor, (self.xsnake+3, self.ysnake+8, 3, 3))
            pygame.draw.rect(display, eyeColor, (self.xsnake+10, self.ysnake+8, 3, 3))
            pygame.draw.rect(display, tongueColor, (self.xsnake+7, self.ysnake+13, 2, 4))
        else:
            pygame.draw.rect(display, eyeColor, (self.xsnake+8, self.ysnake+3, 3, 3))
            pygame.draw.rect(display, eyeColor, (self.xsnake+8, self.ysnake+10, 3, 3))

    #Draws the rest of the snake's body to display surface
    def drawBody(self, display, color):
        for i in range(1, len(self.body)):
            pygame.draw.rect(display, color, (self.body[i][0], self.body[i][1], self.size, self.size))

    #Calls both draw methods to display full snake
    def drawSnake(self, display, color, eyeColor, tongueColor):
        self.drawBody(display, color)
        self.drawHead(display, color, eyeColor, tongueColor)

    def drawGrid(self, display, width, height, color):
        for x in range(0, width, self.size): # draw vertical lines
            pygame.draw.line(display, color, (x, 0), (x, height))
        for y in range(0, height, self.size): # draw horizontal lines
            pygame.draw.line(display, color, (0, y), (width, y))

    #Checks the conditions for losing and return True if the player has lost
    def losing(self, screenWidth, screenHeight):
        result = False
        for i in range(1, len(self.body) - 1):
            if self.body[i][0] == self.xsnake and self.body[i][1] == self.ysnake:
                result = True
        if self.xsnake > screenWidth - self.size or self.xsnake < 0:
            result = True
        if self.ysnake > screenHeight - self.size or self.ysnake < 0:
            result = True
        return result

#Class that represents onscreen food item
class Food:
    def __init__(self, width, height, size, snake):
        self.width = width
        self.height = height
        self.size = size
        self.newFood(snake)

    #Randomly places a new food object on the screen
    def newFood(self, snake):
        self.xfood = random.randint(0, self.width-self.size)
        self.xfood = self.xfood - (self.xfood % self.size)
        if self.xfood < 0:
            self.xfood = 0
        self.yfood = random.randint(0, self.height-self.size)
        self.yfood = self.yfood - (self.yfood % self.size)
        if self.yfood < 0:
            self.yfood = 0

        #Checks to make sure the food isn't located on top of snake
        for i in range(len(snake.body)):
            if snake.body[i] == (self.xfood, self.yfood):
                self.newFood(snake)

    #Displays food to screen
    def drawFood(self, display, color, stemColor):
        pygame.draw.rect(display, color, (self.xfood, self.yfood, self.size, self.size))
        pygame.draw.rect(display, stemColor, (self.xfood + 0.5*self.size - 1, self.yfood-2, 2, 4))  

def main():
    #Initiates the pygame frame and fpsClock
    pygame.init()
    fpsClock = pygame.time.Clock()

    #Constant screen size variables and snake size variable
    SNAKE_SIZE = 16
    WIDTH = 400
    HEIGHT = 368

    #Constant color variables
                #RED  #GREEN  #BLUE  
    RED =       (196,   0,    22)
    GREEN =     (61,    193,  40)
    BLUE =      (3,     66,   160)
    BLACK =     (0,     0,    0)
    WHITE =     (255,   255,  255)
    BROWN =     (155,   93,   27)
    DARKBROWN = (145,   85,   21)

    #Initializes surface object and captions it
    DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Frankie's Tiny Green Python")

    #Creates a snake and food objects to represent what is shown on screen
    x, y = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    x, y = x - x % SNAKE_SIZE, y - y % SNAKE_SIZE
    mySnake = Snake(x, y, '', [(x, y)], SNAKE_SIZE, 10)
    myFood = Food(WIDTH, HEIGHT, SNAKE_SIZE, mySnake)
    musicLoop = True

    #Main game loop
    while True:
        while not mySnake.losing(WIDTH, HEIGHT):
            #Draws a blue background
            if len(mySnake.body) > 1:
                pygame.display.set_caption("Score: " + str(len(mySnake.body) - 1))
            DISPLAYSURF.fill(BROWN)
            mySnake.drawGrid(DISPLAYSURF, WIDTH, HEIGHT, DARKBROWN)

            #Draws the snake and food
            mySnake.drawSnake(DISPLAYSURF, GREEN, BLACK, RED)  
            myFood.drawFood(DISPLAYSURF, RED, GREEN)
            
            #Updates direction of snake based on user input
            #Also inclues sys.exit() method
            mySnake.updateDirection(pygame.event.get())

            #Updates location of snake based on the direction it is going and its speed
            mySnake.updateHeadPosition()
            
            #Checks to see if snake ate any food, and grows and gets faster if it does
            #Otherwise it moves according to updated location
            mySnake.move(myFood, WIDTH, HEIGHT, DISPLAYSURF, RED, GREEN)
            
            #Redraws screen and maintains fps at the snake's speed
            pygame.display.update()
            fpsClock.tick(mySnake.speed)

        fpsClock.tick(3)
        finalScore = len(mySnake.body) -1

        #Checks file for high score
        try:
            highScoreFile = open(".highScore.txt", "r")
            highScore = int(highScoreFile.readline())
            highScoreFile.close()
        except:
            highScore = 0


        #If there is a new high score, display Nick
        if (finalScore >= highScore):
            pygame.display.set_caption("New High Score: " + str(finalScore))
            
            highScoreFile = open(".highScore.txt", "w")
            highScoreFile.write(str(finalScore))
            highScoreFile.close()
            try:
                winImg = pygame.image.load("win.jpg")
                DISPLAYSURF.blit(winImg, (0,0))
                pygame.display.update()
            except:
                pass
        #Otherwise display Frankie    
        else:
            pygame.display.set_caption("Final Score: " + str(finalScore) + ", High Score: " + str(highScore))
            try:
                if musicLoop:
                    pygame.mixer.music.load('Uh-oh.wav')
                    pygame.mixer.music.play(1)
                    musicLoop = False
                loseImg = pygame.image.load("img.jpg")
                DISPLAYSURF.blit(loseImg, (0,0))
                pygame.draw.rect(DISPLAYSURF, WHITE, (0, 224, 5, 111))
                pygame.display.update()
            except:
                pass

        #Wait for enter key to restart or esc to exit
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    #Restarts game by resetting variables
                    pygame.display.set_caption("Frankie's Tiny Green Python")
                    x, y = random.randint(0, WIDTH), random.randint(0, HEIGHT)
                    x, y = x - x % SNAKE_SIZE, y - y % SNAKE_SIZE
                    mySnake = Snake(x, y, '', [(x, y)], SNAKE_SIZE, 10)
                    myFood = Food(WIDTH, HEIGHT, SNAKE_SIZE, mySnake)
                    musicLoop = True
                elif event.key == pygame.K_ESCAPE:
                    pygame.display.quit()
                    pygame.quit()
                    sys.exit()
            elif event.type == QUIT:
                pygame.display.quit()
                pygame.quit()
                sys.exit()

if __name__ == '__main__':
    main()