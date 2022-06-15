import pygame
import random
from screen import *

pygame.init() 
pad = screen

def back(x,y): 
    global pad, background
    pad.blit(background,(x,y))

def rain():
    pad.fill((0, 0, 255)) 
    pad.blit(background, (0, 0)) 
    
    for i in range(len(rain_list)):     
        radius = 3             
        pygame.draw.circle(pad, BLUE, rain_list[i],radius)

        rain_list[i][1] += 10       

        if rain_list[i][1] > SIZE[1]:
            rain_list[i][1] = random.randint(-5, 0)           
            rain_list[i][0] = random.randint(0, SIZE[0])        
    clock.tick(30)

def runGame(): 
    global pad, clock,rain_list, background
    
    x = pad_width*0.05
    y = pad_height*0.7
    background_x=0
    
    male = pygame.image.load(r"C:\Users\dhrn4\OneDrive\바탕 화면\Python\자작곡\man.png")   
    male = pygame.transform.scale(male, (130,200)) 
    male_Rect = male.get_rect()   
    
    female = pygame.image.load(r"C:\Users\dhrn4\OneDrive\바탕 화면\Python\자작곡\woman.jpg")  
    female = pygame.transform.scale(female, (130,200))  
    female_Rect = female.get_rect()  
   
    male_Rect.centerx = x
    male_Rect.centery = y
    
    x = pad_width*0.7
    y = pad_height*0.7
    
    female_Rect.centerx = x
    female_Rect.centery = y
    male_speed = 10               
    crashed = False

    for i in range(rain_CNT):      
        x = random.randint(0, SIZE[0])    
        y = random.randint(0, SIZE[1])    
        rain_list.append([x, y])

    while not crashed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed = True

        pad.fill(WHITE)
        back(background_x,0)

        if male_Rect.colliderect(female_Rect) == 0 :      
            rain()   
        pad.blit(male, male_Rect)    
        pad.blit(female, female_Rect)
        if male_Rect.colliderect(female_Rect) == 0 :      
            male_Rect.x += male_speed  
        
        pygame.display.update()

    pygame.quit()
    quit()

def initScreen(): 
    global pad, clock, background, rain_list, pad_width, pad_height

    pygame.mixer.init()
    pad = pygame.display.set_mode((pad_width, pad_height))
    
    pygame.mixer.music.load(r'C:\Users\dhrn4\OneDrive\바탕 화면\Python\자작곡\winter_rain.mp3') 
    pygame.mixer.music.play()
    pygame.init()
    pad = pygame.display.set_mode((pad_width, pad_height)) 
    
    pygame.display.set_caption('Rain Drop')
    background = pygame.image.load(r"C:\Users\dhrn4\OneDrive\바탕 화면\Python\자작곡\backimage.jpg") 
    clock = pygame.time.Clock()
    
    runGame()

if __name__ == "__main__":
    pad_width = 1250 
    pad_height = 800 
    BLUE = [0,0,255]
    WHITE = [255, 255, 255]
    rain_CNT = 30
    SIZE = [1250,800]
    rain_list = []     

    initScreen()
