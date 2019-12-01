import os
import sys
import random
import pygame
import winsound
from pygame import mixer
from pygame.locals import *

#Initialiserer Mixer og Pygame.
mixer.init()
pygame.init()

#Erklerer variabel med fil. 
effect = pygame.mixer.Sound('nom.wav')
#Laster musikk filen
music = pygame.mixer.music.load("music.mp3")

#Plasserer vinduet i midten av skjermen.
os.environ['SDL_VIDEO_CENTERED'] = '1'

#Definerer størrelsen på vinduet.
screen_width = 600
screen_height = 400

#Lager vinduet med de spesifiserte målene.
screen = pygame.display.set_mode((screen_width, screen_height))
#Gir navn til vinduet.
pygame.display.set_caption('PYthon')

#Henter fonter fra Pygame, og spesifiserer 
font_style = pygame.font.SysFont("timesnewroman", 25)
score_font = pygame.font.SysFont("timesnewroman", 35)

#Farger.
white = (255, 255, 255)
purple = (186, 85, 211)
black = (0, 0, 0)
indigo = (75, 0, 130)
green = (0, 255, 127)
thistle = (216, 191, 216)

#Erklære variabler
clock = pygame.time.Clock()

snake_block = 10

#Definerer Font system, farge, font osv.
def Your_score(score):
    value = score_font.render("Your Score: " + str(score), True, purple)
    screen.blit(value, [0, 0])
 
#Definerer og tegner slange hodet.
def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(screen, purple, [x[0], x[1], snake_block, snake_block])
 
#Definerer message, plasserting.
def message(msg, color):
    message = font_style.render(msg, True, color)
    screen.blit(message, [screen_width / 20, screen_height / 3])

def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def message_display(text):
    largeText = pygame.font.Font('timesnewroman.ttf',115)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center

#Definerer gameLoop og erklærer noen variabler.
def gameLoop():
    game_over = False
    game_close = False

    xh = screen_width / 2
    yv = screen_height / 2
 
    xh_change = 0
    yv_change = 0
 
    snake_List = []
    Length_of_snake = 1

    foodx = round(random.randrange(0, screen_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, screen_height - snake_block) / 10.0) * 10.0

    #Spiller musikken konstant og looper når den er ferdig.
    pygame.mixer.music.play(-1)

    #Lager en loop som går helt til spillet ikke er tapt.
    while not game_over:
        #Hvis spillet blir tapt.
        while game_close == True:
            #Fyller skjermen med spesifiserte farge.
            screen.fill(black)
            message("Du tapte Trykk ENTER-Spill igjen eller ESC-Avslutte", indigo)
            #Din score er lenge på slange, minus 1 (hode).
            Your_score(Length_of_snake - 1)
            #Oppdaterer display
            pygame.display.update()
 
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    #Vis du trykker på ESC stopper spillet.
                    if event.key == pygame.K_ESCAPE:
                        game_over = True
                        game_close = False
                    #Hvis du trykker "Enter" starter spillet på nytt.
                    if event.key == pygame.K_RETURN:
                        gameLoop()
 
        for event in pygame.event.get():
            #Hvis du avslutter, stopper spillet.
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                #Hvis 'Venstre' piltasten blir trykt på beveger slangen seg negativt på X aksen, mot venstre.
                if event.key == pygame.K_LEFT:
                    yv_change = 0
                    xh_change = -snake_block
                #Hvis 'Høyre' piltasten blir trykt på beveger slangen seg positivt på X aksen, mot høyre.
                if event.key == pygame.K_RIGHT:
                    yv_change = 0
                    xh_change = snake_block
                #Hvis 'Opp' piltasten blir trykt på beveger slangen seg negativt på Y aksen, oppover.
                if event.key == pygame.K_UP:
                    yv_change = -snake_block
                    xh_change = 0
                #Hvis 'Ned' piltasten blir trykt på beveger slangen seg positivt på Y aksen, nedover.
                if event.key == pygame.K_DOWN:
                    yv_change = snake_block
                    xh_change = 0
                    
        #Vis slangen treffer veggene er spillet tapt.
        if xh >= screen_width or xh < 0 or yv >= screen_height or yv < 0:
            game_close = True

        #Her har vi start punktet (x og y) og her forteller den at vi beholder verdien til x og y,
        #men legger til verdien i x_change og y_change slik at slangen beveger seg rundt på skjermen.
        xh += xh_change
        yv += yv_change

        #Farger hele bakgrunnen
        screen.fill(thistle)
        #Tegner food-en.
        pygame.draw.rect(screen, green, [foodx, foody, snake_block, snake_block])
        #Lager en tom array for slange hodet.
        snake_Head = []
        #Legger til kordinatene til slangehodet, i array-en "snake_Head".
        snake_Head.append(xh)
        snake_Head.append(yv)
        #Legger til slangehodet til slangen's kropp.
        snake_List.append(snake_Head)
        #Nå er slangen en 1 unit lengere enn den får lov til å være, derfor sletter vi uniten bakerst for å simulere bevegelse.
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        #Gjør at vis slangen går in i seg selv taper du.
        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        our_snake(snake_block, snake_List)
        #Poengsummen er like stor some slangen, minus 1 (hode)
        Your_score(Length_of_snake - 1)
         
        pygame.display.update()

 
        #Vis Slangen (xh, Yv) og Fooden (Foodx, Foody) møtes spawner en ny 'food' 
        if xh == foodx and yv == foody:
            #Spiller av effekt lyden når slange hodet koliderer med mat.
            effect.play()

            #Spiller lyd klippet hver gang slangen spiser en food.
            
            #Spawner food-en randomly i vinduet.
            foodx = round(random.randrange(0, screen_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, screen_height - snake_block) / 10.0) * 10.0
            #Lengden til slangen blir det den er + en til. 
            Length_of_snake += 1
 
        clock.tick(30)
 
    pygame.quit()
    quit()
 
 
gameLoop()