
import sys
import time
import pygame
from random import *

#setting x-y-axis
class Position(object):#defines a new class named Position
    def __init__(self, x,y):#__init__method is a special method in Python that serves as the constructor for the class.
        self.x=x
        self.y=y
#example: How to create a new instance of Position
#         pos =Position(10,20)
#         print(pos.x)-->10
#         print(pos.y)-->20


def new_food(head):#generate random new food spot
    while True:
        new_food=Position(randint(0,48)*20, randint(0,29)*20)#generate random number bewteen 0 and 48 and multiplies it by 20 to get a multiple of 20. Similarly......
        #check that the coordinate of snake head and the new food spot are overlap or not
        if new_food.x != head.x and new_food.y != head.y:
            break#if overlap then stop
        else:
            continue
    return new_food

def rect(color, position):#to draw the snake and food
    pygame.draw.circle(window, color, (position.x, position.y), 10)#window: represents the Pygame window surface on which the circle will be drawn. Color is the color of the circle. x and y are the coordinates of the circle's centre, 10 is the radius of the circle

def exit_end():#define how to quit game
    pygame.quit()
    quit()

def show_end():#define the end window
    #design the window
    small_window = pygame.display.set_mode((960, 600))

    init_background = pygame.Surface((800,600)) #set the dimensions of the image
    init_background.fill((227,207,87))#fill the image with white color

    small_window.blit(init_background, (0,0))

    #design the caption
    pygame.display.set_caption("贪吃蛇大冒险")

    #design background
    font = pygame.font.SysFont("simHei", 40)
    fontsurf = font.render("游戏结束！你的得分: %s" %score, False, black)
    small_window.blit(fontsurf,(250,200))
    pygame.display.update()
    time.sleep(2)
    pygame.quit()
    sys.exit()

def die_snake(head,snake_body):
    die_flag=False
    for body in snake_body[1:]:#skip 0, cuz 0 is the snake head
        if head.x == body.x and head.y == body.y:#if body and head collide
            die_flag = True

    if head.x < 0 or head.x > 960 or head.y < 0 or head.y > 600 or die_flag:
        pygame.mixer.music.stop()
        show_end#then game over

def start_game():
    global score
    global color
    color = (randint(10, 255), randint(10, 255), randint(10, 255))
    run_direction = "right"#define the input movement direction variable of player
    run = run_direction
    head = Position(160, 160)#setting snake head
    snake_body = [Position(head.x, head.y+20), Position(head.x, head.y+40), Position(head.x, head.y+60)]# the length of snake is 3 units
    
    food = Position(300, 300)#coordinate of food

    #dead loop
    while True:
        window.blit(background, (0,0))
        #transmit keyboard input message to the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                show_end()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    run_direction = "up"
                elif event.key == pygame.K_RIGHT:
                    run_direction = "right"
                elif event.key == pygame.K_LEFT:
                    run_direction = "left"
                elif event.key == pygame.K_DOWN:
                    run_direction = "down"

        #food
        rect(color, food)

        #snake head
        rect(black,head)

        #snake body
        for pos in snake_body:
            rect(white,pos)

        #determine that the movement of snake is corresponding to the player's input
        if run=="up" and not run_direction=="down":
            run = run_direction
        elif run=="down" and not run_direction=="up":
            run = run_direction
        elif run=="left" and not run_direction=="right":
            run = run_direction
        elif run=="right" and not run_direction=="left":
            run = run_direction

        #insert the position of snake head into the list of snake body
        snake_body.insert(0, Position(head.x, head.y))

        #update the position of snake head
        if run=="up":
            head.y-=20
        elif run=="down":
            head.y+=20
        elif run=="left":
            head.x-=20
        elif run=="right":
            head.x+=20

        #check dead or live
        die_snake(head, snake_body)

        #check if snake head = food, then plus score and generate new food
        if head.x == food.x and head.y == food.y:
            score+=1
            food = new_food(head)
            color = (randint(10,255), randint(10, 255), randint(10, 255))
        else:
            snake_body.pop()

        font = pygame.font.SysFont("simHei", 25)
        mode_title = font.render("正常模式", False, grey)
        score_title = font.render("得分: %s" %score, False, grey)
        window.blit(mode_title, (50,30))
        window.blit(score_title, (50,65))

        #update drawing
        pygame.display.update()
        #setting the speed of snake
        clock.tick(8)

def buttom(msg,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(window, ac, (x,y,w,h))
        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(window, ic, (x,y,w,h))

    font = pygame.font.SysFont("simHei", 20)
    smallfont = font.render(msg, True, white)
    smallrect = smallfont.get_rect()
    smallrect.center = ((x + (w/2)), (y+(h/2)))
    window.blit(smallfont,smallrect)

def into_game():
    into = True
    while into:
        window.blit(init_background, (0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_end()

        font = pygame.font.SysFont("simHei", 50)

        pygame.init()
        font=pygame.font.Font(None, 36)#Initialize the font
        fontsurf = font.render("欢迎来到贪吃蛇大冒险!", True, black)
        fontrect = fontsurf.get_rect()
        fontrect.center = ((width/2), 200)
        window.blit(fontsurf, fontrect)
        buttom("正常模式",370,370,200,40,blue,brightred,start_game)
        buttom("退出",370,470,200,40,red,brightred,exit_end)
        pygame.display.update()
        clock.tick(15)

if __name__=="__main__":
    white = (255,255,255)
    red = (200,0,0)
    green = (0,128,0)
    blue = (0,202,254)
    violet = (194,8,234)
    brightred = (255,0,0)
    brightgreen = (0,255,0)
    black = (0,0,0)
    grey = (129,131,129)
    score = 0
    width = 960
    height = 600
    window = pygame.display.set_mode((width, height))
    pygame.display.set_caption("贪吃蛇大冒险")

    
    init_background = pygame.Surface((800,600)) #set the dimensions of the image
    init_background.fill((255,255,255))#fill the image with white color

    background = pygame.Surface((640,480))#set the dimensions of the image
    #fill the image with a gradient from blue to green
    pygame.draw.rect(background, (0,0,255), (0,0,640,240))
    pygame.draw.rect(background, (0,255,0), (0,240,640,240))

    #bgm
    pygame.mixer.init()#initialize the mixer module
    try:
        pygame.mixer.music.load("background.mp3")#load the background music file
        pygame.mixer.music.play(-1)#play the bgm in an infinite loop
    except pygame.error:
        print("NO BGM")

    #create clock
    clock = pygame.time.Clock()

    pygame.init()
    into_game()

# first you need to navigate to the path of this game file in command prompt
# then try: pip install pygame
# then enter: python snake_game.py