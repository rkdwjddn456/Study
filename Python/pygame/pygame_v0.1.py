import pygame
import random

pygame.mixer.init()
pygame.mixer.music.load(r"C:\Users\dhrn4\OneDrive\바탕 화면\Python\자작곡\winter_rain.mp3")
pygame.mixer.music.play()
pygame.init() 
pygame.display.set_caption("Rain Drop")

screen_width = 1250 
screen_height = 800

screen = pygame.display.set_mode((screen_width, screen_height))
background = pygame.image.load(r"C:\Users\dhrn4\OneDrive\바탕 화면\Python\자작곡\backimage.jpg")
man = pygame.image.load(r"C:\Users\dhrn4\OneDrive\바탕 화면\Python\자작곡\man.png")
man = pygame.transform.scale(man, (50,50))

BLUE = [0,0,50]
WHITE = [255, 255, 255]
rain_CNT = 30		#비의 갯수
SIZE = [1250,800]
rain_list = []

for i in range(rain_CNT):		
    x = random.randint(0, SIZE[0]) 	
    y = random.randint(0, SIZE[1]) 	
    rain_list.append([x, y]) 	        

clock = pygame.time.Clock()
done = False

while not done:
    for event in pygame.event.get():   
        if event.type == pygame.QUIT:  
            done = True

    screen.fill((0, 0, 255)) 
    screen.blit(background, (0, 0)) 
    pygame.display.update() 

    for i in range(len(rain_list)):		
        radius = 3		 			
        pygame.draw.circle(screen, BLUE, rain_list[i],radius) 
        
        rain_list[i][1] += 1
 
        if rain_list[i][1] > SIZE[1]: 			
            rain_list[i][1] = random.randint(-5, 0)	        
            rain_list[i][0] = random.randint(0, SIZE[0])     	
 
    pygame.display.update()    
    clock.tick(400)

pygame.quit()